import { sanitizeStoredAttachments, type UiAttachment } from './ui-attachments';

export const CHAT_DRAFT_STORAGE_PREFIX = 'chirality.chatDraft.v1';
export const CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE =
  'Chat draft local storage is unavailable. Draft text and attachments will stay in memory for this session only.';
export const CHAT_DRAFT_STORAGE_WARNING_CORRUPT =
  'Chat draft local storage data was invalid and has been reset.';

export type ChatDraftSnapshot = {
  draft: string;
  attachments: UiAttachment[];
};

export type ChatDraftStorageReadResult = {
  snapshot: ChatDraftSnapshot;
  writable: boolean;
  warning: string | null;
};

export type ChatDraftStorageWriteResult = {
  writable: boolean;
  warning: string | null;
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

export function emptyChatDraftSnapshot(): ChatDraftSnapshot {
  return {
    draft: '',
    attachments: []
  };
}

export function sanitizeChatDraftSnapshot(value: unknown): ChatDraftSnapshot {
  if (!value || typeof value !== 'object') {
    return emptyChatDraftSnapshot();
  }

  const record = value as Record<string, unknown>;
  return {
    draft: readString(record.draft),
    attachments: sanitizeStoredAttachments(record.attachments)
  };
}

function isEmptySnapshot(snapshot: ChatDraftSnapshot): boolean {
  return snapshot.draft.length === 0 && snapshot.attachments.length === 0;
}

export function readChatDraftSnapshotFromStorage(
  storage: Pick<Storage, 'getItem' | 'removeItem'>,
  key: string
): ChatDraftStorageReadResult {
  const empty = emptyChatDraftSnapshot();
  let raw: string | null;
  try {
    raw = storage.getItem(key);
  } catch {
    return {
      snapshot: empty,
      writable: false,
      warning: CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE
    };
  }

  if (!raw) {
    return {
      snapshot: empty,
      writable: true,
      warning: null
    };
  }

  try {
    return {
      snapshot: sanitizeChatDraftSnapshot(JSON.parse(raw)),
      writable: true,
      warning: null
    };
  } catch {
    try {
      storage.removeItem(key);
      return {
        snapshot: empty,
        writable: true,
        warning: CHAT_DRAFT_STORAGE_WARNING_CORRUPT
      };
    } catch {
      return {
        snapshot: empty,
        writable: false,
        warning: CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE
      };
    }
  }
}

export function persistChatDraftSnapshotToStorage(
  storage: Pick<Storage, 'setItem' | 'removeItem'>,
  key: string,
  snapshot: ChatDraftSnapshot
): ChatDraftStorageWriteResult {
  try {
    if (isEmptySnapshot(snapshot)) {
      storage.removeItem(key);
    } else {
      storage.setItem(key, JSON.stringify(snapshot));
    }
    return {
      writable: true,
      warning: null
    };
  } catch {
    return {
      writable: false,
      warning: CHAT_DRAFT_STORAGE_WARNING_UNAVAILABLE
    };
  }
}
