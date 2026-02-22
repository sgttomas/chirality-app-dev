export type HarnessErrorType =
  | 'INVALID_REQUEST'
  | 'SESSION_NOT_FOUND'
  | 'PERSONA_NOT_FOUND'
  | 'SDK_FAILURE'
  | 'WORKING_ROOT_INACCESSIBLE'
  | 'ATTACHMENT_FAILURE';

export interface HarnessErrorResponse {
  error: {
    type: HarnessErrorType;
    message: string;
    details?: unknown;
  };
}

export interface SessionRecord {
  sessionId: string;
  projectRoot: string;
  persona: string;
  mode: string;
  createdAt: string;
  updatedAt: string;
  claudeSessionId?: string;
  bootFingerprint?: string;
  bootedAt?: string;
  model?: string;
}

export interface SessionCreateRequest {
  projectRoot: string;
  persona?: string;
  mode?: string;
}

export interface SessionBootRequest {
  sessionId: string;
  opts?: HarnessOpts;
}

export interface SessionListResponse {
  sessions: SessionRecord[];
}

export interface BootMetadata {
  claudeSessionId: string;
  bootFingerprint: string;
  bootedAt: string;
}

export interface SessionBootResponse {
  session: SessionRecord;
  boot: BootMetadata;
}

export interface TurnRequest {
  sessionId: string;
  message: string;
  opts?: HarnessOpts;
  attachments?: string[];
}

export interface InterruptRequest {
  sessionId: string;
}

export interface HarnessOpts {
  model?: string;
  tools?: string[];
  maxTurns?: number;
  persona?: string;
  mode?: string;
}

export interface ResolvedOpts {
  model: string;
  tools: string[];
  maxTurns: number;
  persona: string;
  mode: string;
}

export type ContentBlock =
  | {
      type: 'text';
      text: string;
    }
  | {
      type: 'file';
      path: string;
      mimeType: string;
    };

export interface AttachmentError {
  path: string;
  reason: string;
}

export interface ResolvedAttachments {
  contentBlocks: ContentBlock[];
  errors: AttachmentError[];
}

export type UIEvent =
  | {
      type: 'session:init';
      data: {
        claudeSessionId: string;
        model: string;
      };
    }
  | {
      type: 'chat:delta';
      data: {
        text: string;
      };
    }
  | {
      type: 'chat:complete';
      data: {
        text: string;
      };
    }
  | {
      type: 'tool:result';
      data: {
        name: string;
        ok: boolean;
        output?: string;
      };
    }
  | {
      type: 'session:complete';
      data: Record<string, never>;
    }
  | {
      type: 'process:exit';
      data: {
        exitCode: number;
        interrupted?: boolean;
      };
    };

export interface ISessionManager {
  create(input: SessionCreateRequest): Promise<SessionRecord>;
  resume(sessionId: string): Promise<SessionRecord>;
  getById(sessionId: string): Promise<SessionRecord>;
  save(sessionId: string, updates: Partial<SessionRecord>): Promise<SessionRecord>;
  list(projectRoot: string): Promise<SessionRecord[]>;
  delete(sessionId: string): Promise<void>;
}

export interface IPersonaManager {
  buildSystemPrompt(projectRoot: string, persona: string, mode: string): Promise<string>;
  getBootFingerprint(persona: string, mode: string): string;
}

export interface IAttachmentResolver {
  resolveAttachmentsToContentBlocks(
    message: string,
    attachmentPaths: string[]
  ): Promise<ResolvedAttachments>;
}

export interface IAgentSdkManager {
  startTurn(
    session: SessionRecord,
    message: string,
    opts: ResolvedOpts,
    contentBlocks?: ContentBlock[]
  ): AsyncIterable<UIEvent>;
  interrupt(sessionId: string): Promise<void>;
}
