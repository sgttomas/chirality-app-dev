import { readFile, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { readDependencyRegister } from '../dependencies/register-reader';
import { serializeDependencyRegister } from '../dependencies/register-writer';
import {
  DELIVERABLE_ID_PATTERN,
  DependencyContractError,
  DependencyRegisterRow
} from '../dependencies/schema';
import { StatusParseError, parseStatusDocument } from '../lifecycle/status-parser';
import {
  LifecycleTransitionError,
  LifecycleTransitionOptions,
  transitionStatusFile
} from '../lifecycle/transition';
import {
  WorkspaceOperationError,
  WorkspaceValidationError,
  normalizeProjectRoot
} from './filesystem';

function requireNonEmptyPath(input: string, field: string): string {
  const trimmed = input.trim();
  if (!trimmed) {
    throw new WorkspaceValidationError('INVALID_PROJECT_ROOT', 400, `Missing or invalid '${field}'`);
  }
  if (!path.isAbsolute(trimmed)) {
    throw new WorkspaceValidationError(
      'INVALID_PROJECT_ROOT',
      400,
      `${field} must be an absolute filesystem path`
    );
  }
  return path.resolve(trimmed);
}

function assertWithinProjectRoot(projectRoot: string, candidatePath: string): void {
  const relative = path.relative(projectRoot, candidatePath);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new WorkspaceOperationError(
      'DELIVERABLE_PATH_OUTSIDE_PROJECT_ROOT',
      400,
      'deliverablePath must be inside projectRoot',
      { projectRoot, deliverablePath: candidatePath }
    );
  }
}

async function normalizeDeliverablePath(
  projectRoot: string,
  deliverablePathInput: string
): Promise<string> {
  const deliverablePath = requireNonEmptyPath(deliverablePathInput, 'deliverablePath');
  assertWithinProjectRoot(projectRoot, deliverablePath);

  let deliverableStat;
  try {
    deliverableStat = await stat(deliverablePath);
  } catch {
    throw new WorkspaceOperationError(
      'DELIVERABLE_NOT_FOUND',
      404,
      'deliverablePath is not accessible',
      { deliverablePath }
    );
  }

  if (!deliverableStat.isDirectory()) {
    throw new WorkspaceOperationError(
      'DELIVERABLE_NOT_FOUND',
      404,
      'deliverablePath must point to a directory',
      { deliverablePath }
    );
  }

  return deliverablePath;
}

function getDeliverableIdFromPath(deliverablePath: string): string | undefined {
  const directoryName = path.basename(deliverablePath);
  const match = directoryName.match(/^DEL-\d{2,3}-\d{2}/);
  if (!match) {
    return undefined;
  }

  const candidate = match[0];
  return DELIVERABLE_ID_PATTERN.test(candidate) ? candidate : undefined;
}

function getErrnoCode(error: unknown): string | undefined {
  if (typeof error !== 'object' || error === null) {
    return undefined;
  }

  const code = (error as NodeJS.ErrnoException).code;
  return typeof code === 'string' ? code : undefined;
}

async function readRequiredFile(
  filePath: string,
  notFoundCode: string,
  notFoundMessage: string
): Promise<string> {
  try {
    return await readFile(filePath, 'utf8');
  } catch (error) {
    const errnoCode = getErrnoCode(error);
    if (errnoCode === 'ENOENT') {
      throw new WorkspaceOperationError(notFoundCode, 404, notFoundMessage, { filePath });
    }
    throw new WorkspaceOperationError('WORKSPACE_FILE_READ_FAILED', 500, 'Unable to read file', {
      filePath,
      errnoCode
    });
  }
}

export interface DeliverableStatusSnapshot {
  projectRoot: string;
  deliverablePath: string;
  statusFilePath: string;
  status: ReturnType<typeof parseStatusDocument>;
}

export async function readDeliverableStatus(
  projectRootInput: string,
  deliverablePathInput: string
): Promise<DeliverableStatusSnapshot> {
  const projectRoot = await normalizeProjectRoot(projectRootInput);
  const deliverablePath = await normalizeDeliverablePath(projectRoot, deliverablePathInput);
  const statusFilePath = path.join(deliverablePath, '_STATUS.md');
  const content = await readRequiredFile(
    statusFilePath,
    'STATUS_FILE_NOT_FOUND',
    '_STATUS.md is not accessible in deliverablePath'
  );

  try {
    return {
      projectRoot,
      deliverablePath,
      statusFilePath,
      status: parseStatusDocument(content)
    };
  } catch (error) {
    if (error instanceof StatusParseError) {
      throw new WorkspaceOperationError(error.code, 400, error.message, {
        statusFilePath,
        parseDetails: error.details
      });
    }
    throw error;
  }
}

export interface DeliverableStatusTransitionInput extends LifecycleTransitionOptions {
  projectRoot: string;
  deliverablePath: string;
  targetState: string;
  actor: string;
}

export interface DeliverableStatusTransitionResult extends DeliverableStatusSnapshot {
  transition: {
    from: string;
    to: string;
    actor: string;
  };
}

export async function transitionDeliverableStatus(
  input: DeliverableStatusTransitionInput
): Promise<DeliverableStatusTransitionResult> {
  const projectRoot = await normalizeProjectRoot(input.projectRoot);
  const deliverablePath = await normalizeDeliverablePath(projectRoot, input.deliverablePath);
  const statusFilePath = path.join(deliverablePath, '_STATUS.md');

  try {
    const transition = await transitionStatusFile(
      statusFilePath,
      input.targetState,
      input.actor,
      {
        date: input.date,
        metadata: input.metadata,
        approvalSha: input.approvalSha
      }
    );

    return {
      projectRoot,
      deliverablePath,
      statusFilePath,
      transition: {
        from: transition.from,
        to: transition.to,
        actor: transition.actor
      },
      status: parseStatusDocument(transition.content)
    };
  } catch (error) {
    const errnoCode = getErrnoCode(error);
    if (errnoCode === 'ENOENT') {
      throw new WorkspaceOperationError(
        'STATUS_FILE_NOT_FOUND',
        404,
        '_STATUS.md is not accessible in deliverablePath',
        { statusFilePath }
      );
    }
    if (error instanceof LifecycleTransitionError) {
      throw new WorkspaceOperationError(error.code, 400, error.message, error.details);
    }
    if (error instanceof StatusParseError) {
      throw new WorkspaceOperationError(error.code, 400, error.message, error.details);
    }
    throw error;
  }
}

export interface DeliverableDependenciesSnapshot {
  projectRoot: string;
  deliverablePath: string;
  dependenciesFilePath: string;
  headers: string[];
  rows: DependencyRegisterRow[];
  warnings: string[];
}

export async function readDeliverableDependencies(
  projectRootInput: string,
  deliverablePathInput: string
): Promise<DeliverableDependenciesSnapshot> {
  const projectRoot = await normalizeProjectRoot(projectRootInput);
  const deliverablePath = await normalizeDeliverablePath(projectRoot, deliverablePathInput);
  const dependenciesFilePath = path.join(deliverablePath, 'Dependencies.csv');
  const csv = await readRequiredFile(
    dependenciesFilePath,
    'DEPENDENCY_REGISTER_NOT_FOUND',
    'Dependencies.csv is not accessible in deliverablePath'
  );

  const parsed = readDependencyRegister(csv);
  return {
    projectRoot,
    deliverablePath,
    dependenciesFilePath,
    headers: parsed.headers,
    rows: parsed.rows,
    warnings: parsed.warnings
  };
}

export interface WriteDeliverableDependenciesInput {
  projectRoot: string;
  deliverablePath: string;
  rows: DependencyRegisterRow[];
}

export async function writeDeliverableDependencies(
  input: WriteDeliverableDependenciesInput
): Promise<DeliverableDependenciesSnapshot> {
  const projectRoot = await normalizeProjectRoot(input.projectRoot);
  const deliverablePath = await normalizeDeliverablePath(projectRoot, input.deliverablePath);
  const dependenciesFilePath = path.join(deliverablePath, 'Dependencies.csv');
  const hostDeliverableId = getDeliverableIdFromPath(deliverablePath);

  let previousRows: DependencyRegisterRow[] | undefined;
  let readWarnings: string[] = [];

  try {
    const existingCsv = await readFile(dependenciesFilePath, 'utf8');
    const existing = readDependencyRegister(existingCsv);
    previousRows = existing.rows;
    readWarnings = existing.warnings;
  } catch (error) {
    const errnoCode = getErrnoCode(error);
    if (errnoCode !== 'ENOENT') {
      throw new WorkspaceOperationError(
        'WORKSPACE_FILE_READ_FAILED',
        500,
        'Unable to read existing Dependencies.csv',
        { dependenciesFilePath, errnoCode }
      );
    }
  }

  try {
    const serialized = serializeDependencyRegister(input.rows, {
      hostDeliverableId,
      previousRows
    });
    await writeFile(dependenciesFilePath, serialized.csv, 'utf8');

    const parsed = readDependencyRegister(serialized.csv);
    return {
      projectRoot,
      deliverablePath,
      dependenciesFilePath,
      headers: parsed.headers,
      rows: parsed.rows,
      warnings: [...readWarnings, ...serialized.warnings, ...parsed.warnings]
    };
  } catch (error) {
    if (error instanceof DependencyContractError) {
      throw new WorkspaceOperationError(error.code, 400, error.message, error.details);
    }
    throw error;
  }
}
