import { readdir, stat } from 'node:fs/promises';
import path from 'node:path';

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
  kind: 'directory' | 'file';
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

async function detectKnowledgeMarker(projectRoot: string): Promise<boolean> {
  const decompositionDirectory = path.join(projectRoot, '_Decomposition');

  try {
    const entries = await readdir(decompositionDirectory, { withFileTypes: true });
    return entries.some((entry) => entry.isFile() && /domain/i.test(entry.name));
  } catch {
    return false;
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
    hasKnowledgeDecomposition: await detectKnowledgeMarker(projectRoot),
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
