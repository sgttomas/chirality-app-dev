import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const electronMock = vi.hoisted(() => ({
  app: {
    getPath: vi.fn<(name: string) => string>()
  },
  safeStorage: {
    isEncryptionAvailable: vi.fn<() => boolean>(),
    encryptString: vi.fn<(value: string) => Buffer>(),
    decryptString: vi.fn<(value: Buffer) => string>()
  }
}));

vi.mock('electron', () => ({
  app: electronMock.app,
  safeStorage: electronMock.safeStorage
}));

import {
  getUiApiKey,
  hasStoredApiKey,
  loadStoredKeyIntoGlobal,
  removeApiKey,
  retrieveApiKey,
  storeApiKey
} from '../../../electron/api-key-storage';

const GLOBAL_KEY = '__CHIRALITY_UI_API_KEY__';
const globalState = globalThis as unknown as Record<string, string | undefined>;

function getStoragePath(tmpDir: string): string {
  return path.join(tmpDir, 'credentials', 'api-key.enc');
}

let tmpDir = '';

beforeEach(async () => {
  tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-api-key-storage-'));
  electronMock.app.getPath.mockReturnValue(tmpDir);
  electronMock.safeStorage.isEncryptionAvailable.mockReturnValue(true);
  electronMock.safeStorage.encryptString.mockImplementation((value: string) =>
    Buffer.from(`enc:${value}`, 'utf8')
  );
  electronMock.safeStorage.decryptString.mockImplementation((value: Buffer) => {
    const raw = value.toString('utf8');
    if (!raw.startsWith('enc:')) {
      throw new Error('corrupted');
    }
    return raw.slice(4);
  });
});

afterEach(async () => {
  delete globalState[GLOBAL_KEY];
  vi.clearAllMocks();
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('electron/api-key-storage', () => {
  it('stores encrypted key material outside projectRoot and updates process global', async () => {
    await storeApiKey('ui-key-123');

    const stored = await readFile(getStoragePath(tmpDir), 'utf8');
    expect(stored).toBe('enc:ui-key-123');
    expect(getUiApiKey()).toBe('ui-key-123');
    await expect(hasStoredApiKey()).resolves.toBe(true);
  });

  it('loads stored key into process global during startup', async () => {
    const storagePath = getStoragePath(tmpDir);
    await mkdir(path.dirname(storagePath), { recursive: true });
    await writeFile(storagePath, Buffer.from('enc:boot-key', 'utf8'));

    await loadStoredKeyIntoGlobal();

    expect(getUiApiKey()).toBe('boot-key');
    await expect(retrieveApiKey()).resolves.toBe('boot-key');
  });

  it('returns null when decrypt fails and does not throw', async () => {
    const storagePath = getStoragePath(tmpDir);
    await mkdir(path.dirname(storagePath), { recursive: true });
    await writeFile(storagePath, Buffer.from('invalid', 'utf8'));
    electronMock.safeStorage.decryptString.mockImplementation(() => {
      throw new Error('decrypt-failed');
    });

    await expect(retrieveApiKey()).resolves.toBeNull();
    await expect(hasStoredApiKey()).resolves.toBe(true);
  });

  it('removes stored key and clears process global', async () => {
    await storeApiKey('ui-key-123');
    expect(getUiApiKey()).toBe('ui-key-123');

    await removeApiKey();

    expect(getUiApiKey()).toBeUndefined();
    await expect(hasStoredApiKey()).resolves.toBe(false);
  });

  it('fails closed when secure storage is unavailable', async () => {
    electronMock.safeStorage.isEncryptionAvailable.mockReturnValue(false);

    await expect(storeApiKey('ui-key-123')).rejects.toThrow(
      'Secure storage is not available on this platform'
    );
  });
});
