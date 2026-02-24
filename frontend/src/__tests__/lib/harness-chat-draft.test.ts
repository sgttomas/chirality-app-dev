import { describe, expect, it } from 'vitest';
import {
  buildChatDraftStorageKey,
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
});
