import { sanitizeStoredAttachments, type UiAttachment } from './ui-attachments';

export const CHAT_DRAFT_STORAGE_PREFIX = 'chirality.chatDraft.v1';

export type ChatDraftSnapshot = {
  draft: string;
  attachments: UiAttachment[];
};

function readString(value: unknown): string {
  if (typeof value !== 'string') {
    return '';
  }
  return value;
}

export function buildChatDraftStorageKey(
  projectRoot: string,
  persona: string,
  mode: string
): string {
  return `${CHAT_DRAFT_STORAGE_PREFIX}:${projectRoot}:${persona}:${mode}`;
}

export function sanitizeChatDraftSnapshot(value: unknown): ChatDraftSnapshot {
  if (!value || typeof value !== 'object') {
    return {
      draft: '',
      attachments: []
    };
  }

  const record = value as Record<string, unknown>;
  return {
    draft: readString(record.draft),
    attachments: sanitizeStoredAttachments(record.attachments)
  };
}
