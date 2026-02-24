import { readFile, readdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { parseStatusDocument } from '../lifecycle/status-parser';

const MAX_TREE_ENTRIES_PER_DIRECTORY = 60;
const MAX_SCOPE_SCAN_DIRECTORIES = 2500;
const SKIP_DIRECTORY_NAMES = new Set([
  '.git',
  '.next',
  'node_modules',
  'dist',
  'dist-electron',
  'out'
]);

export class WorkspaceValidationError extends Error {
  status: number;
  code: string;

  constructor(code: string, status: number, message: string) {
    super(message);
    this.name = 'WorkspaceValidationError';
    this.status = status;
    this.code = code;
  }
}

export class WorkspaceOperationError extends Error {
  status: number;
  code: string;
  details?: unknown;

  constructor(code: string, status: number, message: string, details?: unknown) {
    super(message);
    this.name = 'WorkspaceOperationError';
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

export type TreeNode = {
  name: string;
  path: string;
  kind: 'directory' | 'file' | 'symlink';
  children?: TreeNode[];
  truncated?: boolean;
};

export type ScopeItem = {
  id: string;
  label: string;
  path: string;
};

export type ScopeScanResult = {
  deliverables: ScopeItem[];
  knowledgeTypes: ScopeItem[];
  hasKnowledgeDecomposition: boolean;
  truncated: boolean;
};

export type ProjectDeliverable = {
  id: string;
  name: string;
  pkg: string;
  status: string;
  path: string;
};

export type KnowledgeTypeOption = {
  id: string;
  label: string;
  matchingDeliverableKeys: string[];
};

export type ProjectDeliverablesScanResult = {
  deliverables: ProjectDeliverable[];
  knowledgeDecomposition: {
    enabled: boolean;
    markerFile: string | null;
  };
  knowledgeTypes: KnowledgeTypeOption[];
  truncated: boolean;
};

const KNOWLEDGE_MARKER_PATTERNS = [
  /\bknowledge\s+categories\b/i,
  /\bknowledge\s+types\b/i,
  /\bdomain[_\s-]*decomp/i,
  /\bdomain\s+decomposition\b/i
];

const KNOWLEDGE_TYPE_BUCKETS: Array<{
  id: string;
  label: string;
  matches: (fileNames: Set<string>) => boolean;
}> = [
  {
    id: 'datasheet',
    label: 'Datasheet',
    matches: (fileNames) => fileNames.has('Datasheet.md')
  },
  {
    id: 'specification',
    label: 'Specification',
    matches: (fileNames) => fileNames.has('Specification.md')
  },
  {
    id: 'guidance',
    label: 'Guidance',
    matches: (fileNames) => fileNames.has('Guidance.md')
  },
  {
    id: 'procedure',
    label: 'Procedure',
    matches: (fileNames) => fileNames.has('Procedure.md')
  },
  {
    id: 'dependencies',
    label: 'Dependencies',
    matches: (fileNames) => fileNames.has('_DEPENDENCIES.md') || fileNames.has('Dependencies.csv')
  },
  {
    id: 'references',
    label: 'References',
    matches: (fileNames) => fileNames.has('_REFERENCES.md')
  },
  {
    id: 'context',
    label: 'Context',
    matches: (fileNames) => fileNames.has('_CONTEXT.md')
  },
  {
    id: 'status',
    label: 'Status',
    matches: (fileNames) => fileNames.has('_STATUS.md')
  },
  {
    id: 'semantic',
    label: 'Semantic',
    matches: (fileNames) => fileNames.has('_SEMANTIC.md') || fileNames.has('_SEMANTIC_LENSING.md')
  },
  {
    id: 'memory',
    label: 'Memory',
    matches: (fileNames) => fileNames.has('MEMORY.md')
  }
];

function compareDirectoryEntries(a: { name: string; isDirectory(): boolean }, b: { name: string; isDirectory(): boolean }): number {
  if (a.isDirectory() && !b.isDirectory()) {
    return -1;
  }

  if (!a.isDirectory() && b.isDirectory()) {
    return 1;
  }

  return a.name.localeCompare(b.name);
}

function ensureAbsolutePath(input: string): string {
  const trimmed = input.trim();
  if (!trimmed) {
    throw new WorkspaceValidationError(
      'INVALID_PROJECT_ROOT',
      400,
      "Missing or invalid 'projectRoot'"
    );
  }

  if (!path.isAbsolute(trimmed)) {
    throw new WorkspaceValidationError(
      'INVALID_PROJECT_ROOT',
      400,
      'projectRoot must be an absolute filesystem path'
    );
  }

  return path.resolve(trimmed);
}

export async function normalizeProjectRoot(projectRootInput: string): Promise<string> {
  const normalized = ensureAbsolutePath(projectRootInput);

  let rootStat;
  try {
    rootStat = await stat(normalized);
  } catch {
    throw new WorkspaceValidationError(
      'WORKING_ROOT_INACCESSIBLE',
      404,
      'projectRoot is not accessible'
    );
  }

  if (!rootStat.isDirectory()) {
    throw new WorkspaceValidationError(
      'WORKING_ROOT_INACCESSIBLE',
      404,
      'projectRoot must point to a directory'
    );
  }

  return normalized;
}

async function buildTree(currentPath: string, remainingDepth: number): Promise<TreeNode> {
  const baseName = path.basename(currentPath) || currentPath;
  const node: TreeNode = {
    name: baseName,
    path: currentPath,
    kind: 'directory'
  };

  if (remainingDepth <= 0) {
    return node;
  }

  let entries;
  try {
    entries = await readdir(currentPath, { withFileTypes: true });
  } catch {
    return {
      ...node,
      truncated: true
    };
  }

  const filtered = entries
    .filter((entry) => !SKIP_DIRECTORY_NAMES.has(entry.name))
    .sort(compareDirectoryEntries);
  const limited = filtered.slice(0, MAX_TREE_ENTRIES_PER_DIRECTORY);
  const children: TreeNode[] = [];

  for (const entry of limited) {
    const childPath = path.join(currentPath, entry.name);

    if (entry.isSymbolicLink()) {
      children.push({
        name: entry.name,
        path: childPath,
        kind: 'symlink'
      });
      continue;
    }

    if (entry.isDirectory()) {
      children.push(await buildTree(childPath, remainingDepth - 1));
      continue;
    }

    children.push({
      name: entry.name,
      path: childPath,
      kind: 'file'
    });
  }

  if (children.length > 0) {
    node.children = children;
  }

  if (filtered.length > MAX_TREE_ENTRIES_PER_DIRECTORY) {
    node.truncated = true;
  }

  return node;
}

export async function readProjectRootTree(projectRoot: string, depth: number): Promise<TreeNode> {
  const boundedDepth = Number.isFinite(depth) ? Math.max(1, Math.min(6, Math.floor(depth))) : 3;
  return buildTree(projectRoot, boundedDepth);
}

function splitStableId(folderName: string): { id: string; label: string } {
  const separator = folderName.indexOf('_');
  if (separator < 0) {
    return { id: folderName, label: folderName };
  }

  const id = folderName.slice(0, separator);
  const label = folderName.slice(separator + 1).replace(/_/g, ' ');
  return { id, label };
}

function isDeliverableDirectory(name: string): boolean {
  return /^DEL-\d{2,3}-\d{2}(?:$|_)/.test(name);
}

function isKnowledgeTypeDirectory(name: string): boolean {
  return /^KTY-[A-Za-z0-9]{2}-[A-Za-z0-9]{2}(?:$|_)/.test(name);
}

export function buildDeliverableCompositeKey(pkg: string, deliverableId: string): string {
  return `${pkg}::${deliverableId}`;
}

function getPackageFolderForDeliverable(projectRoot: string, deliverablePath: string): string {
  const relativePath = path.relative(projectRoot, deliverablePath);
  if (!relativePath || relativePath.startsWith('..')) {
    return 'UNKNOWN_PACKAGE';
  }

  const segments = relativePath.split(path.sep).filter(Boolean);
  const packageSegment = segments.find((segment) => /^PKG-\d{2,3}(?:$|_)/.test(segment));
  return packageSegment ?? 'UNKNOWN_PACKAGE';
}

async function parseDeliverableStatus(deliverablePath: string): Promise<string> {
  const statusPath = path.join(deliverablePath, '_STATUS.md');
  try {
    const content = await readFile(statusPath, 'utf8');
    return parseStatusDocument(content).currentState.toLowerCase();
  } catch {
    return 'unknown';
  }
}

async function readDirectoryFileSet(directoryPath: string): Promise<Set<string>> {
  const fileNames = new Set<string>();
  try {
    const entries = await readdir(directoryPath, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isFile()) {
        fileNames.add(entry.name);
      }
    }
  } catch {
    return fileNames;
  }
  return fileNames;
}

function buildKnowledgeTypeOptions(
  rows: Array<{ key: string; fileNames: Set<string> }>
): KnowledgeTypeOption[] {
  const byBucket = new Map<string, { label: string; keys: Set<string> }>();

  for (const bucket of KNOWLEDGE_TYPE_BUCKETS) {
    byBucket.set(bucket.id, {
      label: bucket.label,
      keys: new Set<string>()
    });
  }

  for (const row of rows) {
    for (const bucket of KNOWLEDGE_TYPE_BUCKETS) {
      if (bucket.matches(row.fileNames)) {
        byBucket.get(bucket.id)?.keys.add(row.key);
      }
    }
  }

  return KNOWLEDGE_TYPE_BUCKETS.map((bucket) => {
    const entry = byBucket.get(bucket.id);
    return {
      id: bucket.id,
      label: bucket.label,
      matchingDeliverableKeys: [...(entry?.keys ?? new Set<string>())].sort((a, b) =>
        a.localeCompare(b)
      )
    };
  }).filter((entry) => entry.matchingDeliverableKeys.length > 0);
}

async function detectKnowledgeMarkerFile(projectRoot: string): Promise<string | null> {
  const decompositionDirectory = path.join(projectRoot, '_Decomposition');

  try {
    const entries = await readdir(decompositionDirectory, { withFileTypes: true });
    const sortedFiles = entries
      .filter((entry) => entry.isFile() && /\.md$/i.test(entry.name))
      .map((entry) => entry.name)
      .sort((a, b) => a.localeCompare(b));

    for (const fileName of sortedFiles) {
      const filePath = path.join(decompositionDirectory, fileName);
      try {
        const content = await readFile(filePath, 'utf8');
        if (
          KNOWLEDGE_MARKER_PATTERNS.some((pattern) => pattern.test(content)) ||
          /domain/i.test(fileName)
        ) {
          return filePath;
        }
      } catch {
        continue;
      }
    }

    return null;
  } catch {
    return null;
  }
}

export async function scanProjectScopes(projectRoot: string): Promise<ScopeScanResult> {
  const deliverables: ScopeItem[] = [];
  const knowledgeTypes: ScopeItem[] = [];
  const visited = new Set<string>();
  let scannedCount = 0;
  let truncated = false;

  async function walk(currentPath: string, depth: number): Promise<void> {
    if (truncated || depth > 8) {
      return;
    }

    if (visited.has(currentPath)) {
      return;
    }
    visited.add(currentPath);

    scannedCount += 1;
    if (scannedCount > MAX_SCOPE_SCAN_DIRECTORIES) {
      truncated = true;
      return;
    }

    let entries;
    try {
      entries = await readdir(currentPath, { withFileTypes: true });
    } catch {
      return;
    }

    const hasStatusFile = entries.some((entry) => entry.isFile() && entry.name === '_STATUS.md');
    const folderName = path.basename(currentPath);

    if (hasStatusFile && isDeliverableDirectory(folderName)) {
      const { id, label } = splitStableId(folderName);
      deliverables.push({ id, label, path: currentPath });
    }

    if (hasStatusFile && isKnowledgeTypeDirectory(folderName)) {
      const { id, label } = splitStableId(folderName);
      knowledgeTypes.push({ id, label, path: currentPath });
    }

    if (depth >= 8) {
      return;
    }

    const childDirectories = entries
      .filter((entry) => entry.isDirectory())
      .filter((entry) => !SKIP_DIRECTORY_NAMES.has(entry.name))
      .sort(compareDirectoryEntries);

    for (const entry of childDirectories) {
      await walk(path.join(currentPath, entry.name), depth + 1);
      if (truncated) {
        return;
      }
    }
  }

  await walk(projectRoot, 0);

  const sortById = (a: ScopeItem, b: ScopeItem): number => a.id.localeCompare(b.id);
  deliverables.sort(sortById);
  knowledgeTypes.sort(sortById);

  return {
    deliverables,
    knowledgeTypes,
    hasKnowledgeDecomposition: (await detectKnowledgeMarkerFile(projectRoot)) !== null,
    truncated
  };
}

export async function scanProjectDeliverables(
  projectRoot: string
): Promise<ProjectDeliverablesScanResult> {
  const deliverables: ProjectDeliverable[] = [];
  const visited = new Set<string>();
  let scannedCount = 0;
  let truncated = false;

  async function walk(currentPath: string, depth: number): Promise<void> {
    if (truncated || depth > 8) {
      return;
    }
    if (visited.has(currentPath)) {
      return;
    }
    visited.add(currentPath);

    scannedCount += 1;
    if (scannedCount > MAX_SCOPE_SCAN_DIRECTORIES) {
      truncated = true;
      return;
    }

    let entries;
    try {
      entries = await readdir(currentPath, { withFileTypes: true });
    } catch {
      return;
    }

    const hasStatusFile = entries.some((entry) => entry.isFile() && entry.name === '_STATUS.md');
    const folderName = path.basename(currentPath);

    if (hasStatusFile && isDeliverableDirectory(folderName)) {
      const { id, label } = splitStableId(folderName);
      const pkg = getPackageFolderForDeliverable(projectRoot, currentPath);
      const status = await parseDeliverableStatus(currentPath);
      deliverables.push({
        id,
        name: label,
        pkg,
        status,
        path: currentPath
      });
    }

    if (depth >= 8) {
      return;
    }

    const childDirectories = entries
      .filter((entry) => entry.isDirectory())
      .filter((entry) => !SKIP_DIRECTORY_NAMES.has(entry.name))
      .sort(compareDirectoryEntries);

    for (const entry of childDirectories) {
      await walk(path.join(currentPath, entry.name), depth + 1);
      if (truncated) {
        return;
      }
    }
  }

  await walk(projectRoot, 0);

  deliverables.sort((a, b) => {
    const pkgCompare = a.pkg.localeCompare(b.pkg);
    if (pkgCompare !== 0) {
      return pkgCompare;
    }
    return a.id.localeCompare(b.id);
  });

  const knowledgeRows = await Promise.all(
    deliverables.map(async (deliverable) => ({
      key: buildDeliverableCompositeKey(deliverable.pkg, deliverable.id),
      fileNames: await readDirectoryFileSet(deliverable.path)
    }))
  );
  const knowledgeMarkerFile = await detectKnowledgeMarkerFile(projectRoot);

  return {
    deliverables,
    knowledgeDecomposition: {
      enabled: knowledgeMarkerFile !== null,
      markerFile: knowledgeMarkerFile
    },
    knowledgeTypes: buildKnowledgeTypeOptions(knowledgeRows),
    truncated
  };
}

export function workspaceErrorPayload(error: unknown): {
  status: number;
  body: { error: { type: string; message: string; details?: unknown } };
} {
  if (error instanceof WorkspaceValidationError) {
    return {
      status: error.status,
      body: {
        error: {
          type: error.code,
          message: error.message
        }
      }
    };
  }

  if (error instanceof WorkspaceOperationError) {
    return {
      status: error.status,
      body: {
        error: {
          type: error.code,
          message: error.message,
          details: error.details
        }
      }
    };
  }

  const fallbackMessage = error instanceof Error ? error.message : 'Unexpected workspace failure';
  return {
    status: 500,
    body: {
      error: {
        type: 'WORKSPACE_FAILURE',
        message: fallbackMessage
      }
    }
  };
}
