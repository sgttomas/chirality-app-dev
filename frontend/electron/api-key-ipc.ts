import { ipcMain } from 'electron';
import {
  hasStoredApiKey,
  isEncryptionAvailable,
  removeApiKey,
  storeApiKey
} from './api-key-storage';

export const API_KEY_STORE_CHANNEL = 'chirality:api-key-store';
export const API_KEY_REMOVE_CHANNEL = 'chirality:api-key-remove';
export const API_KEY_STATUS_CHANNEL = 'chirality:api-key-status';

export type ApiKeyStatusResult = {
  hasKey: boolean;
  encryptionAvailable: boolean;
  source: 'ui' | 'env' | 'none';
};

export type ApiKeyStoreResult = {
  ok: boolean;
  error?: string;
};

export function registerApiKeyHandlers(): void {
  unregisterApiKeyHandlers();

  ipcMain.handle(API_KEY_STORE_CHANNEL, async (_event, key: unknown): Promise<ApiKeyStoreResult> => {
    if (typeof key !== 'string' || key.trim().length === 0) {
      return { ok: false, error: 'Key must be a non-empty string' };
    }

    try {
      await storeApiKey(key.trim());
      return { ok: true };
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to store key';
      return { ok: false, error: message };
    }
  });

  ipcMain.handle(API_KEY_REMOVE_CHANNEL, async (): Promise<ApiKeyStoreResult> => {
    try {
      await removeApiKey();
      return { ok: true };
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to remove key';
      return { ok: false, error: message };
    }
  });

  ipcMain.handle(API_KEY_STATUS_CHANNEL, async (): Promise<ApiKeyStatusResult> => {
    const uiKeyStored = await hasStoredApiKey();
    const envKey = Boolean(
      process.env.ANTHROPIC_API_KEY?.trim() || process.env.CHIRALITY_ANTHROPIC_API_KEY?.trim()
    );

    let source: 'ui' | 'env' | 'none' = 'none';
    if (uiKeyStored) {
      source = 'ui';
    } else if (envKey) {
      source = 'env';
    }

    return {
      hasKey: uiKeyStored || envKey,
      encryptionAvailable: isEncryptionAvailable(),
      source
    };
  });
}

export function unregisterApiKeyHandlers(): void {
  ipcMain.removeHandler(API_KEY_STORE_CHANNEL);
  ipcMain.removeHandler(API_KEY_REMOVE_CHANNEL);
  ipcMain.removeHandler(API_KEY_STATUS_CHANNEL);
}
