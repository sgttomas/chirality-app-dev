import { randomUUID } from 'node:crypto';
import { mkdir, readdir, readFile, rm, stat, writeFile, access } from 'node:fs/promises';
import { constants as fsConstants } from 'node:fs';
import path from 'node:path';
import { HarnessError } from './errors';
import { ISessionManager, SessionCreateRequest, SessionRecord } from './types';

const DEFAULT_PERSONA = 'WORKING_ITEMS';
const DEFAULT_MODE = 'direct';

function getSessionStoreDirectory(): string {
  return process.env.CHIRALITY_SESSION_ROOT ?? path.join(process.cwd(), '.chirality', 'sessions');
}

async function ensureDirectoryExists(dirPath: string): Promise<void> {
  await mkdir(dirPath, { recursive: true });
}

export async function assertProjectRootAccessible(projectRoot: string): Promise<string> {
  if (!path.isAbsolute(projectRoot)) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'projectRoot must be an absolute filesystem path',
      { projectRoot }
    );
  }

  try {
    const directoryStat = await stat(projectRoot);
    if (!directoryStat.isDirectory()) {
      throw new HarnessError(
        'WORKING_ROOT_INACCESSIBLE',
        404,
        'projectRoot must point to an existing directory',
        { projectRoot }
      );
    }
    await access(projectRoot, fsConstants.R_OK | fsConstants.W_OK);
  } catch (error) {
    if (error instanceof HarnessError) {
      throw error;
    }
    throw new HarnessError('WORKING_ROOT_INACCESSIBLE', 404, 'projectRoot is not accessible', {
      projectRoot
    });
  }

  return path.resolve(projectRoot);
}

function getSessionFilePath(sessionId: string): string {
  return path.join(getSessionStoreDirectory(), `${sessionId}.json`);
}

async function readSessionFromDisk(sessionId: string): Promise<SessionRecord> {
  const filePath = getSessionFilePath(sessionId);

  try {
    const raw = await readFile(filePath, 'utf8');
    return JSON.parse(raw) as SessionRecord;
  } catch {
    throw new HarnessError('SESSION_NOT_FOUND', 404, `Session '${sessionId}' does not exist`, {
      sessionId
    });
  }
}

export class FileSessionManager implements ISessionManager {
  async create(input: SessionCreateRequest): Promise<SessionRecord> {
    const projectRoot = await assertProjectRootAccessible(input.projectRoot);
    await ensureDirectoryExists(getSessionStoreDirectory());

    const now = new Date().toISOString();
    const session: SessionRecord = {
      sessionId: `sess_${randomUUID()}`,
      projectRoot,
      persona: input.persona?.trim() || DEFAULT_PERSONA,
      mode: input.mode?.trim() || DEFAULT_MODE,
      createdAt: now,
      updatedAt: now
    };

    await writeFile(getSessionFilePath(session.sessionId), `${JSON.stringify(session, null, 2)}\n`, 'utf8');
    return session;
  }

  async resume(sessionId: string): Promise<SessionRecord> {
    return this.getById(sessionId);
  }

  async getById(sessionId: string): Promise<SessionRecord> {
    await ensureDirectoryExists(getSessionStoreDirectory());
    return readSessionFromDisk(sessionId);
  }

  async save(sessionId: string, updates: Partial<SessionRecord>): Promise<SessionRecord> {
    await ensureDirectoryExists(getSessionStoreDirectory());
    const existing = await readSessionFromDisk(sessionId);
    const updated: SessionRecord = {
      ...existing,
      ...updates,
      sessionId: existing.sessionId,
      createdAt: existing.createdAt,
      updatedAt: new Date().toISOString()
    };

    await writeFile(getSessionFilePath(sessionId), `${JSON.stringify(updated, null, 2)}\n`, 'utf8');
    return updated;
  }

  async list(projectRoot: string): Promise<SessionRecord[]> {
    const normalizedProjectRoot = await assertProjectRootAccessible(projectRoot);
    await ensureDirectoryExists(getSessionStoreDirectory());

    const entries = await readdir(getSessionStoreDirectory());
    const sessions: SessionRecord[] = [];

    for (const entry of entries) {
      if (!entry.endsWith('.json')) {
        continue;
      }

      const sessionId = entry.replace(/\.json$/, '');
      try {
        const session = await readSessionFromDisk(sessionId);
        if (path.resolve(session.projectRoot) === normalizedProjectRoot) {
          sessions.push(session);
        }
      } catch {
        // Ignore malformed or orphaned records during list traversal.
      }
    }

    sessions.sort((a, b) => a.createdAt.localeCompare(b.createdAt));
    return sessions;
  }

  async delete(sessionId: string): Promise<void> {
    await ensureDirectoryExists(getSessionStoreDirectory());

    try {
      await rm(getSessionFilePath(sessionId));
    } catch {
      throw new HarnessError('SESSION_NOT_FOUND', 404, `Session '${sessionId}' does not exist`, {
        sessionId
      });
    }
  }
}
