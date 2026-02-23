import { constants as fsConstants } from 'node:fs';
import { access, copyFile, mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { HarnessError } from './errors';
import { sanitizeNonEmptyLabel } from './sanitize';

const PKG_ID_PATTERN = /^PKG-\d{2,3}$/;
const DEL_ID_PATTERN = /^DEL-\d{2,3}-\d{2}$/;

const EXECUTION_ROOT_DIRECTORIES = [
  '_Aggregation',
  '_Aggregation/_Archive',
  '_Aggregation/_Templates',
  '_Change',
  '_Coordination',
  '_Decomposition',
  '_Decomposition/_Archive',
  '_Estimates',
  '_Reconciliation',
  '_Archive',
  '_Scripts',
  '_Sources'
] as const;

const REQUIRED_PACKAGE_SUBDIRECTORIES = [
  '0_References',
  '0_References/_Archive',
  '1_Working',
  '1_Working/_Archive',
  '2_Checking',
  '2_Checking/From',
  '2_Checking/To',
  '3_Issued',
  '3_Issued/_Archive'
] as const;

const COORDINATION_MODES = ['SCHEDULE_FIRST', 'DEPENDENCY_TRACKED', 'HYBRID'] as const;

export type CoordinationMode = (typeof COORDINATION_MODES)[number];

type ParsedDeliverable = {
  id: string;
  name: string;
};

type ParsedPackage = {
  id: string;
  name: string;
  deliverables: ParsedDeliverable[];
};

type ParsedDecomposition = {
  projectName: string;
  packages: ParsedPackage[];
};

type PackagePlan = {
  id: string;
  path: string;
  expectedPaths: string[];
  deliverables: Array<{
    id: string;
    path: string;
  }>;
};

export type LayoutValidationItem = {
  id: string;
  path: string;
  valid: boolean;
  missing: string[];
};

export type LayoutValidationResult = {
  valid: boolean;
  executionRoot: {
    path: string;
    valid: boolean;
    missing: string[];
  };
  packages: LayoutValidationItem[];
  deliverables: LayoutValidationItem[];
};

export type ScaffoldExecutionRootInput = {
  executionRoot: string;
  decompositionPath: string;
  projectName?: string;
  coordinationMode?: CoordinationMode;
  now?: Date;
};

export type ScaffoldExecutionRootResult = {
  executionRoot: string;
  decompositionPath: string;
  copiedDecompositionPath: string;
  projectName: string;
  coordinationMode: CoordinationMode;
  packageCount: number;
  deliverableCount: number;
  created: {
    directories: string[];
    files: string[];
  };
  layoutValidation: LayoutValidationResult;
};

function isErrnoCode(error: unknown, code: string): boolean {
  if (typeof error !== 'object' || error === null) {
    return false;
  }

  const value = (error as NodeJS.ErrnoException).code;
  return value === code;
}

function requireAbsolutePath(input: unknown, field: string): string {
  if (typeof input !== 'string' || input.trim().length === 0) {
    throw new HarnessError('INVALID_REQUEST', 400, `Missing or invalid '${field}'`);
  }

  const trimmed = input.trim();
  if (!path.isAbsolute(trimmed)) {
    throw new HarnessError('INVALID_REQUEST', 400, `${field} must be an absolute filesystem path`);
  }

  return path.resolve(trimmed);
}

function parseMarkdownTableRow(line: string): string[] | null {
  const trimmed = line.trim();
  if (!trimmed.startsWith('|') || !trimmed.endsWith('|')) {
    return null;
  }

  const cells = trimmed
    .slice(1, -1)
    .split('|')
    .map((cell) => cell.trim());

  const isSeparator = cells.every((cell) => /^:?-{3,}:?$/.test(cell));
  if (isSeparator) {
    return null;
  }

  return cells;
}

function extractProjectName(markdown: string): string {
  const titleLine = markdown
    .split(/\r?\n/)
    .map((line) => line.trim())
    .find((line) => line.startsWith('# '));

  if (!titleLine) {
    return 'Chirality Project';
  }

  const heading = titleLine.replace(/^#\s+/, '').trim();
  const splitOnDash = heading.split(/\s+[—-]\s+/);
  if (splitOnDash[0].trim().length > 0) {
    return splitOnDash[0].trim();
  }

  return heading || 'Chirality Project';
}

function parseDecomposition(markdown: string): ParsedDecomposition {
  const lines = markdown.split(/\r?\n/);
  const packageNameById = new Map<string, string>();
  const deliverablesByPackage = new Map<string, Map<string, string>>();

  let currentPackageId: string | undefined;

  for (const line of lines) {
    const packageHeadingMatch = line.match(/^###\s+(PKG-\d{2,3})\s+[—-]\s+(.+?)\s*$/);
    if (packageHeadingMatch) {
      const packageId = packageHeadingMatch[1];
      const packageName = packageHeadingMatch[2].trim();
      currentPackageId = packageId;

      if (!packageNameById.has(packageId)) {
        packageNameById.set(packageId, packageName);
      }
      if (!deliverablesByPackage.has(packageId)) {
        deliverablesByPackage.set(packageId, new Map<string, string>());
      }
      continue;
    }

    const row = parseMarkdownTableRow(line);
    if (!row || row.length < 2) {
      continue;
    }

    const first = row[0];
    const second = row[1];

    if (PKG_ID_PATTERN.test(first)) {
      if (!packageNameById.has(first)) {
        packageNameById.set(first, second);
      }
      if (!deliverablesByPackage.has(first)) {
        deliverablesByPackage.set(first, new Map<string, string>());
      }
      continue;
    }

    if (currentPackageId && DEL_ID_PATTERN.test(first)) {
      const deliverables = deliverablesByPackage.get(currentPackageId);
      if (!deliverables) {
        continue;
      }
      if (!deliverables.has(first)) {
        deliverables.set(first, second);
      }
    }
  }

  const packageIds = new Set([...packageNameById.keys(), ...deliverablesByPackage.keys()]);
  const packages = [...packageIds]
    .sort((a, b) => a.localeCompare(b))
    .map((packageId) => {
      const packageName = packageNameById.get(packageId) ?? packageId;
      const deliverablesMap = deliverablesByPackage.get(packageId) ?? new Map<string, string>();
      const deliverables = [...deliverablesMap.entries()]
        .sort((a, b) => a[0].localeCompare(b[0]))
        .map(([deliverableId, deliverableName]) => ({
          id: deliverableId,
          name: deliverableName
        }));

      return {
        id: packageId,
        name: packageName,
        deliverables
      };
    });

  const deliverableCount = packages.reduce((total, pkg) => total + pkg.deliverables.length, 0);

  if (packages.length === 0 || deliverableCount === 0) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'Decomposition document does not contain parseable package and deliverable tables'
    );
  }

  return {
    projectName: extractProjectName(markdown),
    packages
  };
}

function parseCoordinationMode(input: unknown): CoordinationMode {
  if (input === undefined) {
    return 'DEPENDENCY_TRACKED';
  }

  if (typeof input !== 'string') {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      "coordinationMode must be one of 'SCHEDULE_FIRST', 'DEPENDENCY_TRACKED', 'HYBRID'"
    );
  }

  const normalized = input.trim().toUpperCase() as CoordinationMode;
  if (!COORDINATION_MODES.includes(normalized)) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      "coordinationMode must be one of 'SCHEDULE_FIRST', 'DEPENDENCY_TRACKED', 'HYBRID'",
      { coordinationMode: input }
    );
  }

  return normalized;
}

async function ensureDirectory(targetPath: string, createdDirectories: string[]): Promise<void> {
  try {
    const existing = await stat(targetPath);
    if (!existing.isDirectory()) {
      throw new HarnessError(
        'WORKING_ROOT_INACCESSIBLE',
        409,
        `Expected directory but found file at '${targetPath}'`
      );
    }
    return;
  } catch (error) {
    if (!isErrnoCode(error, 'ENOENT')) {
      if (error instanceof HarnessError) {
        throw error;
      }
      throw new HarnessError(
        'WORKING_ROOT_INACCESSIBLE',
        500,
        `Unable to inspect directory '${targetPath}'`
      );
    }
  }

  await mkdir(targetPath, { recursive: true });
  createdDirectories.push(targetPath);
}

async function ensureFile(
  targetPath: string,
  content: string,
  createdFiles: string[]
): Promise<void> {
  try {
    await access(targetPath, fsConstants.F_OK);
    return;
  } catch (error) {
    if (!isErrnoCode(error, 'ENOENT')) {
      throw new HarnessError('SDK_FAILURE', 500, `Unable to access '${targetPath}'`);
    }
  }

  await writeFile(targetPath, content, 'utf8');
  createdFiles.push(targetPath);
}

async function findMissingPaths(pathsToCheck: string[]): Promise<string[]> {
  const missing: string[] = [];

  for (const candidatePath of pathsToCheck) {
    try {
      await access(candidatePath, fsConstants.F_OK);
    } catch {
      missing.push(candidatePath);
    }
  }

  return missing;
}

function buildInitTemplate(
  projectName: string,
  decompositionReference: string,
  coordinationMode: CoordinationMode,
  now: Date
): string {
  const date = now.toISOString().slice(0, 10);
  return `# Execution Init

**Project Name:** ${projectName}
**Initialized:** ${date}
**Decomposition Reference:** ${decompositionReference}
**Coordination Mode:** ${coordinationMode}

## Session Parameters

- Update this file with project-specific startup constraints as needed.
`;
}

function buildCoordinationTemplate(coordinationMode: CoordinationMode): string {
  return `# Coordination Record

**Representation:** ${coordinationMode}
**Dependency tracking mode:** FULL_GRAPH

## Coordination Representations

- SCHEDULE_FIRST
- DEPENDENCY_TRACKED
- HYBRID

## Selection Notes

- Full dependency graph remains audit truth.
- Blocker subset may be used as execution sequencing truth per project policy.
`;
}

async function validateLayout(
  executionRoot: string,
  copiedDecompositionPath: string,
  packagePlans: PackagePlan[]
): Promise<LayoutValidationResult> {
  const executionExpectedPaths = [
    path.join(executionRoot, 'INIT.md'),
    path.join(executionRoot, '_Coordination', '_COORDINATION.md'),
    copiedDecompositionPath,
    ...EXECUTION_ROOT_DIRECTORIES.map((entry) => path.join(executionRoot, entry))
  ];

  const executionMissing = await findMissingPaths(executionExpectedPaths);
  const packageResults: LayoutValidationItem[] = [];
  const deliverableResults: LayoutValidationItem[] = [];

  for (const pkg of packagePlans) {
    const missing = await findMissingPaths(pkg.expectedPaths);
    packageResults.push({
      id: pkg.id,
      path: pkg.path,
      valid: missing.length === 0,
      missing
    });

    for (const deliverable of pkg.deliverables) {
      const deliverableMissing = await findMissingPaths([deliverable.path]);
      deliverableResults.push({
        id: deliverable.id,
        path: deliverable.path,
        valid: deliverableMissing.length === 0,
        missing: deliverableMissing
      });
    }
  }

  const valid =
    executionMissing.length === 0 &&
    packageResults.every((pkg) => pkg.valid) &&
    deliverableResults.every((deliverable) => deliverable.valid);

  return {
    valid,
    executionRoot: {
      path: executionRoot,
      valid: executionMissing.length === 0,
      missing: executionMissing
    },
    packages: packageResults,
    deliverables: deliverableResults
  };
}

export async function scaffoldExecutionRoot(
  input: ScaffoldExecutionRootInput
): Promise<ScaffoldExecutionRootResult> {
  const executionRoot = requireAbsolutePath(input.executionRoot, 'executionRoot');
  const decompositionPath = requireAbsolutePath(input.decompositionPath, 'decompositionPath');
  const coordinationMode = parseCoordinationMode(input.coordinationMode);
  const now = input.now ?? new Date();

  let decompositionMarkdown: string;
  try {
    decompositionMarkdown = await readFile(decompositionPath, 'utf8');
  } catch {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'decompositionPath must point to a readable markdown file',
      { decompositionPath }
    );
  }

  const parsed = parseDecomposition(decompositionMarkdown);
  const projectName = input.projectName?.trim() || parsed.projectName;

  const createdDirectories: string[] = [];
  const createdFiles: string[] = [];

  await ensureDirectory(executionRoot, createdDirectories);
  for (const relativePath of EXECUTION_ROOT_DIRECTORIES) {
    await ensureDirectory(path.join(executionRoot, relativePath), createdDirectories);
  }

  const copiedDecompositionPath = path.join(executionRoot, '_Decomposition', path.basename(decompositionPath));
  if (path.resolve(copiedDecompositionPath) !== path.resolve(decompositionPath)) {
    try {
      await access(copiedDecompositionPath, fsConstants.F_OK);
    } catch (error) {
      if (!isErrnoCode(error, 'ENOENT')) {
        throw new HarnessError('SDK_FAILURE', 500, `Unable to access '${copiedDecompositionPath}'`);
      }
      await copyFile(decompositionPath, copiedDecompositionPath);
      createdFiles.push(copiedDecompositionPath);
    }
  }

  await ensureFile(
    path.join(executionRoot, 'INIT.md'),
    buildInitTemplate(
      projectName,
      path.relative(executionRoot, copiedDecompositionPath) || path.basename(copiedDecompositionPath),
      coordinationMode,
      now
    ),
    createdFiles
  );
  await ensureFile(
    path.join(executionRoot, '_Coordination', '_COORDINATION.md'),
    buildCoordinationTemplate(coordinationMode),
    createdFiles
  );

  const packagePlans: PackagePlan[] = [];
  for (const pkg of parsed.packages) {
    const packageLabel = sanitizeNonEmptyLabel(pkg.name, `package '${pkg.id}' name`);
    const packageFolder = `${pkg.id}_${packageLabel}`;
    const packagePath = path.join(executionRoot, packageFolder);
    await ensureDirectory(packagePath, createdDirectories);

    const expectedPackagePaths = [packagePath];
    for (const subDirectory of REQUIRED_PACKAGE_SUBDIRECTORIES) {
      const absoluteSubDirectory = path.join(packagePath, subDirectory);
      await ensureDirectory(absoluteSubDirectory, createdDirectories);
      expectedPackagePaths.push(absoluteSubDirectory);
    }

    const deliverables = [];
    for (const deliverable of pkg.deliverables) {
      const deliverableLabel = sanitizeNonEmptyLabel(
        deliverable.name,
        `deliverable '${deliverable.id}' name`
      );
      const deliverableFolder = `${deliverable.id}_${deliverableLabel}`;
      const deliverablePath = path.join(packagePath, '1_Working', deliverableFolder);
      await ensureDirectory(deliverablePath, createdDirectories);
      deliverables.push({
        id: deliverable.id,
        path: deliverablePath
      });
    }

    packagePlans.push({
      id: pkg.id,
      path: packagePath,
      expectedPaths: expectedPackagePaths,
      deliverables
    });
  }

  const deliverableCount = packagePlans.reduce((count, pkg) => count + pkg.deliverables.length, 0);
  const layoutValidation = await validateLayout(executionRoot, copiedDecompositionPath, packagePlans);

  return {
    executionRoot,
    decompositionPath,
    copiedDecompositionPath,
    projectName,
    coordinationMode,
    packageCount: packagePlans.length,
    deliverableCount,
    created: {
      directories: createdDirectories,
      files: createdFiles
    },
    layoutValidation
  };
}
