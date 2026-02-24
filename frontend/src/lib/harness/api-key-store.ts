/**
 * Server-side API key store accessor — DEL-02-06
 *
 * Reads the UI-provided API key from the process-global variable set by the
 * Electron main process storage adapter. In packaged builds, the Electron
 * main process and the Next.js server share the same Node.js process, so
 * this global is directly available.
 *
 * Key material MUST NOT be logged by any function in this module.
 */

const GLOBAL_KEY = '__CHIRALITY_UI_API_KEY__';

type ApiKeyGlobal = typeof globalThis & {
  [key: string]: string | undefined;
};

const apiKeyGlobal = globalThis as ApiKeyGlobal;

/**
 * Get the UI-provided API key (set by Electron main process via safeStorage).
 * Returns undefined if no UI key is stored or if running outside Electron.
 */
export function getUiApiKey(): string | undefined {
  const value = apiKeyGlobal[GLOBAL_KEY];
  return typeof value === 'string' && value.trim().length > 0 ? value : undefined;
}

/**
 * Check whether a UI-provided API key is available in the process global.
 */
export function hasUiApiKey(): boolean {
  return getUiApiKey() !== undefined;
}
