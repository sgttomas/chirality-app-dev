/**
 * API Key Storage Adapter — DEL-02-06
 *
 * Encrypts and persists an Anthropic API key using Electron safeStorage.
 * The encrypted blob is stored in the app's userData directory (outside projectRoot).
 * Key material MUST NOT appear in logs, config files, or git-tracked locations.
 *
 * On store/remove, the adapter also sets/clears a process-global variable
 * so the Next.js server (same process in packaged builds) can read the key
 * without IPC round-trips.
 */

import { app, safeStorage } from 'electron';
import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';

const STORAGE_FILENAME = 'api-key.enc';
const GLOBAL_KEY = '__CHIRALITY_UI_API_KEY__';

type ApiKeyGlobal = typeof globalThis & {
  [GLOBAL_KEY]?: string;
};

const apiKeyGlobal = globalThis as ApiKeyGlobal;

function getStoragePath(): string {
  return path.join(app.getPath('userData'), 'credentials', STORAGE_FILENAME);
}

async function ensureStorageDir(): Promise<void> {
  const dir = path.dirname(getStoragePath());
  await mkdir(dir, { recursive: true });
}

/**
 * Store an API key: encrypt with safeStorage, write to disk, set global.
 * Throws if safeStorage is unavailable or encryption fails.
 */
export async function storeApiKey(key: string): Promise<void> {
  if (!safeStorage.isEncryptionAvailable()) {
    throw new Error('Secure storage is not available on this platform');
  }

  const encrypted = safeStorage.encryptString(key);
  await ensureStorageDir();
  await writeFile(getStoragePath(), encrypted);
  apiKeyGlobal[GLOBAL_KEY] = key;
}

/**
 * Retrieve the decrypted API key from disk + safeStorage.
 * Returns null if no key is stored or decryption fails.
 * On decryption failure, the corrupted blob is NOT deleted (operator may investigate).
 */
export async function retrieveApiKey(): Promise<string | null> {
  if (!safeStorage.isEncryptionAvailable()) {
    return null;
  }

  let encrypted: Buffer;
  try {
    encrypted = await readFile(getStoragePath());
  } catch {
    return null;
  }

  try {
    return safeStorage.decryptString(encrypted);
  } catch {
    // Corrupted blob — return null, do NOT auto-delete (per Procedure Step 4b.2).
    return null;
  }
}

/**
 * Remove the stored API key from disk and clear the global.
 */
export async function removeApiKey(): Promise<void> {
  apiKeyGlobal[GLOBAL_KEY] = undefined;
  try {
    await rm(getStoragePath());
  } catch {
    // File may not exist — that's fine.
  }
}

/**
 * Check whether a UI-provided API key is stored (without retrieving the value).
 */
export async function hasStoredApiKey(): Promise<boolean> {
  if (apiKeyGlobal[GLOBAL_KEY]) {
    return true;
  }

  try {
    await readFile(getStoragePath());
    return true;
  } catch {
    return false;
  }
}

/**
 * Check whether safeStorage encryption is available on this platform.
 */
export function isEncryptionAvailable(): boolean {
  return safeStorage.isEncryptionAvailable();
}

/**
 * Load the stored key into the process global on startup.
 * Called once from electron/main.ts after app.whenReady().
 */
export async function loadStoredKeyIntoGlobal(): Promise<void> {
  const key = await retrieveApiKey();
  if (key) {
    apiKeyGlobal[GLOBAL_KEY] = key;
  }
}

/**
 * Read the UI-provided API key from the process global.
 * Used by server-side code (anthropic-agent-sdk-manager.ts) to implement
 * ENV+UI precedence without IPC.
 */
export function getUiApiKey(): string | undefined {
  return apiKeyGlobal[GLOBAL_KEY];
}
