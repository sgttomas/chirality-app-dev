import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => {
  const handlers = new Map<string, (...args: unknown[]) => Promise<unknown>>();
  const ipcMain = {
    handle: vi.fn((channel: string, handler: (...args: unknown[]) => Promise<unknown>) => {
      handlers.set(channel, handler);
    }),
    removeHandler: vi.fn((channel: string) => {
      handlers.delete(channel);
    })
  };

  return {
    handlers,
    ipcMain,
    hasStoredApiKey: vi.fn<() => Promise<boolean>>(),
    isEncryptionAvailable: vi.fn<() => boolean>(),
    removeApiKey: vi.fn<() => Promise<void>>(),
    storeApiKey: vi.fn<(key: string) => Promise<void>>()
  };
});

vi.mock('electron', () => ({
  ipcMain: mocks.ipcMain
}));

vi.mock('../../../electron/api-key-storage', () => ({
  hasStoredApiKey: mocks.hasStoredApiKey,
  isEncryptionAvailable: mocks.isEncryptionAvailable,
  removeApiKey: mocks.removeApiKey,
  storeApiKey: mocks.storeApiKey
}));

import {
  API_KEY_REMOVE_CHANNEL,
  API_KEY_STATUS_CHANNEL,
  API_KEY_STORE_CHANNEL,
  registerApiKeyHandlers,
  unregisterApiKeyHandlers
} from '../../../electron/api-key-ipc';

function getHandler(channel: string): (...args: unknown[]) => Promise<unknown> {
  const handler = mocks.handlers.get(channel);
  if (!handler) {
    throw new Error(`Missing handler for ${channel}`);
  }
  return handler;
}

beforeEach(() => {
  mocks.handlers.clear();
  vi.clearAllMocks();
  mocks.hasStoredApiKey.mockResolvedValue(false);
  mocks.isEncryptionAvailable.mockReturnValue(true);
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
});

afterEach(() => {
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
});

describe('electron/api-key-ipc', () => {
  it('registers all API key handlers and unregisters previous handlers first', () => {
    registerApiKeyHandlers();

    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_STORE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_REMOVE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_STATUS_CHANNEL);
    expect(mocks.handlers.has(API_KEY_STORE_CHANNEL)).toBe(true);
    expect(mocks.handlers.has(API_KEY_REMOVE_CHANNEL)).toBe(true);
    expect(mocks.handlers.has(API_KEY_STATUS_CHANNEL)).toBe(true);
  });

  it('trims and stores key material through the store channel', async () => {
    registerApiKeyHandlers();
    const handler = getHandler(API_KEY_STORE_CHANNEL);

    const result = await handler({}, '  sk-ant-test-key  ');

    expect(mocks.storeApiKey).toHaveBeenCalledWith('sk-ant-test-key');
    expect(result).toEqual({ ok: true });
  });

  it('rejects empty values on the store channel', async () => {
    registerApiKeyHandlers();
    const handler = getHandler(API_KEY_STORE_CHANNEL);

    const result = await handler({}, '   ');

    expect(mocks.storeApiKey).not.toHaveBeenCalled();
    expect(result).toEqual({ ok: false, error: 'Key must be a non-empty string' });
  });

  it('returns status source precedence as ui > env > none', async () => {
    registerApiKeyHandlers();
    const handler = getHandler(API_KEY_STATUS_CHANNEL);

    mocks.hasStoredApiKey.mockResolvedValue(true);
    process.env.ANTHROPIC_API_KEY = 'env-key';
    await expect(handler({})).resolves.toEqual({
      hasKey: true,
      encryptionAvailable: true,
      source: 'ui'
    });

    mocks.hasStoredApiKey.mockResolvedValue(false);
    await expect(handler({})).resolves.toEqual({
      hasKey: true,
      encryptionAvailable: true,
      source: 'env'
    });

    delete process.env.ANTHROPIC_API_KEY;
    await expect(handler({})).resolves.toEqual({
      hasKey: false,
      encryptionAvailable: true,
      source: 'none'
    });
  });

  it('handles remove channel failures without throwing', async () => {
    registerApiKeyHandlers();
    const handler = getHandler(API_KEY_REMOVE_CHANNEL);
    mocks.removeApiKey.mockRejectedValue(new Error('remove-failed'));

    await expect(handler({})).resolves.toEqual({ ok: false, error: 'remove-failed' });
  });

  it('unregisters all handlers', () => {
    registerApiKeyHandlers();
    unregisterApiKeyHandlers();

    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_STORE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_REMOVE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_STATUS_CHANNEL);
  });
});
