import { describe, expect, it, vi } from 'vitest';
import {
  CHAT_DRAFT_STORAGE_WARNING_CORRUPT,
  CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE,
  buildChatDraftStorageKey,
  persistChatDraftSnapshotToStorage,
  readChatDraftSnapshotFromStorage,
  sanitizeChatDraftSnapshot
} from '../../lib/harness/chat-draft';

describe('chat draft helpers', () => {
  it('builds a scoped local-storage key', () => {
    expect(
      buildChatDraftStorageKey('/tmp/project', 'WORKING_ITEMS', 'WORKBENCH')
    ).toBe('chirality.chatDraft.v1:/tmp/project:WORKING_ITEMS:WORKBENCH');
  });

  it('sanitizes persisted draft state and attachment records', () => {
    const snapshot = sanitizeChatDraftSnapshot({
      draft: 'continue this turn',
      attachments: [
        {
          path: '/tmp/example/data.csv',
          displayName: 'data.csv',
          mimeType: 'text/csv',
          clientType: 'csv'
        },
        {
          displayName: 'missing-path'
        }
      ]
    });

    expect(snapshot).toEqual({
      draft: 'continue this turn',
      attachments: [
        {
          path: '/tmp/example/data.csv',
          displayName: 'data.csv',
          mimeType: 'text/csv',
          clientType: 'csv'
        }
      ]
    });
  });

  it('reads a valid draft snapshot from local storage', () => {
    const storage = {
      getItem: vi.fn().mockReturnValue(
        JSON.stringify({
          draft: 'resume this turn',
          attachments: [
            {
              path: '/tmp/example/notes.md',
              displayName: 'notes.md',
              mimeType: 'text/markdown',
              clientType: 'markdown'
            }
          ]
        })
      ),
      removeItem: vi.fn()
    };

    const result = readChatDraftSnapshotFromStorage(storage, 'draft-key');

    expect(result).toEqual({
      snapshot: {
        draft: 'resume this turn',
        attachments: [
          {
            path: '/tmp/example/notes.md',
            displayName: 'notes.md',
            mimeType: 'text/markdown',
            clientType: 'markdown'
          }
        ]
      },
      writable: true,
      warning: null
    });
  });

  it('resets corrupt draft storage payloads and warns once', () => {
    const storage = {
      getItem: vi.fn().mockReturnValue('{not-json'),
      removeItem: vi.fn()
    };

    const result = readChatDraftSnapshotFromStorage(storage, 'draft-key');

    expect(result).toEqual({
      snapshot: {
        draft: '',
        attachments: []
      },
      writable: true,
      warning: CHAT_DRAFT_STORAGE_WARNING_CORRUPT
    });
    expect(storage.removeItem).toHaveBeenCalledWith('draft-key');
  });

  it('marks storage unavailable when reads throw', () => {
    const storage = {
      getItem: vi.fn(() => {
        throw new Error('localStorage unavailable');
      }),
      removeItem: vi.fn()
    };

    const result = readChatDraftSnapshotFromStorage(storage, 'draft-key');

    expect(result).toEqual({
      snapshot: {
        draft: '',
        attachments: []
      },
      writable: false,
      warning: CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE
    });
  });

  it('marks storage unavailable when corrupt payload reset fails', () => {
    const storage = {
      getItem: vi.fn().mockReturnValue('{not-json'),
      removeItem: vi.fn(() => {
        throw new Error('localStorage unavailable');
      })
    };

    const result = readChatDraftSnapshotFromStorage(storage, 'draft-key');

    expect(result).toEqual({
      snapshot: {
        draft: '',
        attachments: []
      },
      writable: false,
      warning: CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE
    });
  });

  it('writes non-empty snapshots to local storage', () => {
    const storage = {
      setItem: vi.fn(),
      removeItem: vi.fn()
    };

    const result = persistChatDraftSnapshotToStorage(storage, 'draft-key', {
      draft: 'continue',
      attachments: [
        {
          path: '/tmp/example/data.csv',
          displayName: 'data.csv',
          mimeType: 'text/csv',
          clientType: 'csv'
        }
      ]
    });

    expect(result).toEqual({
      writable: true,
      warning: null
    });
    expect(storage.setItem).toHaveBeenCalledWith(
      'draft-key',
      JSON.stringify({
        draft: 'continue',
        attachments: [
          {
            path: '/tmp/example/data.csv',
            displayName: 'data.csv',
            mimeType: 'text/csv',
            clientType: 'csv'
          }
        ]
      })
    );
    expect(storage.removeItem).not.toHaveBeenCalled();
  });

  it('removes empty snapshots from local storage', () => {
    const storage = {
      setItem: vi.fn(),
      removeItem: vi.fn()
    };

    const result = persistChatDraftSnapshotToStorage(storage, 'draft-key', {
      draft: '',
      attachments: []
    });

    expect(result).toEqual({
      writable: true,
      warning: null
    });
    expect(storage.removeItem).toHaveBeenCalledWith('draft-key');
    expect(storage.setItem).not.toHaveBeenCalled();
  });

  it('marks storage unavailable when write operations fail', () => {
    const storage = {
      setItem: vi.fn(() => {
        throw new Error('quota exceeded');
      }),
      removeItem: vi.fn()
    };

    const result = persistChatDraftSnapshotToStorage(storage, 'draft-key', {
      draft: 'continue',
      attachments: []
    });

    expect(result).toEqual({
      writable: false,
      warning: CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE
    });
  });
});
