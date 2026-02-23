import { randomUUID } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { HarnessError } from './errors';
import { ContentBlock, IAgentSdkManager, ResolvedOpts, SessionRecord, UIEvent } from './types';

type ActiveTurnState = {
  interrupted: boolean;
  abortController?: AbortController;
};

type ParsedSseEvent = {
  event: string;
  data: unknown;
};

const ANTHROPIC_MESSAGES_ENDPOINT = 'https://api.anthropic.com/v1/messages';
const DEFAULT_ANTHROPIC_VERSION = '2023-06-01';
const DEFAULT_ANTHROPIC_MAX_TOKENS = 1024;
const DEFAULT_STREAM_TIMEOUT_MS = 90_000;
const MAX_INLINE_IMAGE_BYTES = 5 * 1024 * 1024;
const FALLBACK_MODEL = 'claude-sonnet-4-20250514';

const PERMISSION_DENY_MARKER = 'UNAPPROVED_DENY_TEST';
const PERMISSION_ALLOW_MARKER = 'UNAPPROVED_ALLOW_TEST';
const BOOT_SDK_FAIL_MODEL_MARKER = '__BOOT_SDK_FAIL__';
const TURN_SDK_FAIL_MARKER = 'TURN_SDK_FAIL_TEST';

function asNonEmptyString(value: string | undefined): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

function readAnthropicApiKey(): string {
  const key =
    asNonEmptyString(process.env.ANTHROPIC_API_KEY) ??
    asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_API_KEY);
  if (!key) {
    throw new HarnessError(
      'SDK_FAILURE',
      503,
      'Anthropic API key is not configured. Set ANTHROPIC_API_KEY before running harness turns.',
      {
        provider: 'anthropic',
        category: 'MISSING_API_KEY'
      }
    );
  }
  return key;
}

function getAnthropicEndpoint(): string {
  return (
    asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_API_URL) ?? ANTHROPIC_MESSAGES_ENDPOINT
  );
}

function getAnthropicVersion(): string {
  return asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_VERSION) ?? DEFAULT_ANTHROPIC_VERSION;
}

function getMaxTokens(): number {
  const raw = asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_MAX_TOKENS);
  if (!raw) {
    return DEFAULT_ANTHROPIC_MAX_TOKENS;
  }

  const parsed = Number.parseInt(raw, 10);
  if (!Number.isSafeInteger(parsed) || parsed <= 0) {
    return DEFAULT_ANTHROPIC_MAX_TOKENS;
  }
  return parsed;
}

function getStreamTimeoutMs(): number {
  const raw = asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_STREAM_TIMEOUT_MS);
  if (!raw) {
    return DEFAULT_STREAM_TIMEOUT_MS;
  }

  const parsed = Number.parseInt(raw, 10);
  if (!Number.isSafeInteger(parsed) || parsed <= 0) {
    return DEFAULT_STREAM_TIMEOUT_MS;
  }
  return parsed;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function parseSseFrame(frame: string): ParsedSseEvent | null {
  const lines = frame.split('\n');
  let event = '';
  const dataLines: string[] = [];

  for (const line of lines) {
    if (line.startsWith('event:')) {
      event = line.slice('event:'.length).trim();
      continue;
    }
    if (line.startsWith('data:')) {
      dataLines.push(line.slice('data:'.length).trimStart());
    }
  }

  if (!event || dataLines.length === 0) {
    return null;
  }

  const rawData = dataLines.join('\n');
  if (rawData === '[DONE]') {
    return {
      event,
      data: { type: 'message_stop' }
    };
  }

  try {
    return {
      event,
      data: JSON.parse(rawData) as unknown
    };
  } catch {
    return {
      event,
      data: rawData
    };
  }
}

async function* iterateSseEvents(
  stream: ReadableStream<Uint8Array>
): AsyncIterable<ParsedSseEvent> {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }

    if (value) {
      buffer += decoder.decode(value, { stream: true });
    }

    while (true) {
      const frameBoundary = buffer.indexOf('\n\n');
      if (frameBoundary < 0) {
        break;
      }

      const frame = buffer.slice(0, frameBoundary);
      buffer = buffer.slice(frameBoundary + 2);
      const parsed = parseSseFrame(frame);
      if (parsed) {
        yield parsed;
      }
    }
  }

  buffer += decoder.decode();
  const trailing = buffer.trim();
  if (!trailing) {
    return;
  }

  const parsed = parseSseFrame(trailing);
  if (parsed) {
    yield parsed;
  }
}

function detectMimeType(filePath: string, fallbackMimeType: string): string {
  if (fallbackMimeType && fallbackMimeType !== 'application/octet-stream') {
    return fallbackMimeType;
  }

  const extension = path.extname(filePath).toLowerCase();
  switch (extension) {
    case '.png':
      return 'image/png';
    case '.jpg':
    case '.jpeg':
      return 'image/jpeg';
    case '.gif':
      return 'image/gif';
    case '.webp':
      return 'image/webp';
    default:
      return fallbackMimeType || 'application/octet-stream';
  }
}

async function readImageAsBase64(filePath: string): Promise<string> {
  let bytes: Buffer;
  try {
    bytes = await readFile(filePath);
  } catch {
    throw new HarnessError('ATTACHMENT_FAILURE', 400, `Attachment '${filePath}' is not readable`, {
      path: filePath
    });
  }

  if (bytes.byteLength > MAX_INLINE_IMAGE_BYTES) {
    throw new HarnessError(
      'ATTACHMENT_FAILURE',
      400,
      `Attachment '${filePath}' exceeds ${MAX_INLINE_IMAGE_BYTES} byte inline image limit`,
      {
        path: filePath,
        byteLength: bytes.byteLength,
        limit: MAX_INLINE_IMAGE_BYTES
      }
    );
  }

  return bytes.toString('base64');
}

async function formatContentBlocks(
  message: string,
  contentBlocks: ContentBlock[] | undefined
): Promise<Array<Record<string, unknown>>> {
  const blocks: ContentBlock[] =
    (contentBlocks ?? []).length > 0 ? contentBlocks ?? [] : [{ type: 'text', text: message }];
  const anthropicContent: Array<Record<string, unknown>> = [];

  for (const block of blocks) {
    if (block.type === 'text') {
      anthropicContent.push({
        type: 'text',
        text: block.text
      });
      continue;
    }

    const mimeType = detectMimeType(block.path, block.mimeType);
    if (mimeType.startsWith('image/')) {
      anthropicContent.push({
        type: 'image',
        source: {
          type: 'base64',
          media_type: mimeType,
          data: await readImageAsBase64(block.path)
        }
      });
      continue;
    }

    anthropicContent.push({
      type: 'text',
      text: `Attachment '${path.basename(block.path)}' is available locally but not yet mapped to Anthropic multimodal request types.`
    });
  }

  return anthropicContent;
}

function readMessageStop(event: ParsedSseEvent): boolean {
  if (event.event === 'message_stop') {
    return true;
  }
  if (!isRecord(event.data)) {
    return false;
  }
  return event.data.type === 'message_stop';
}

function readTextDelta(event: ParsedSseEvent): string | undefined {
  if (!isRecord(event.data)) {
    return undefined;
  }

  const delta = event.data.delta;
  if (isRecord(delta) && typeof delta.text === 'string' && delta.text.length > 0) {
    return delta.text;
  }

  const contentBlock = event.data.content_block;
  if (isRecord(contentBlock) && typeof contentBlock.text === 'string' && contentBlock.text.length > 0) {
    return contentBlock.text;
  }

  return undefined;
}

function toAnthropicSseError(data: unknown): HarnessError {
  if (isRecord(data) && isRecord(data.error) && typeof data.error.message === 'string') {
    return new HarnessError('SDK_FAILURE', 502, data.error.message, {
      provider: 'anthropic',
      category: 'API_RESPONSE_ERROR',
      upstreamType: typeof data.error.type === 'string' ? data.error.type : undefined
    });
  }

  return new HarnessError('SDK_FAILURE', 502, 'Anthropic stream returned an error event', {
    provider: 'anthropic',
    category: 'API_RESPONSE_ERROR'
  });
}

function classifyHttpError(
  status: number
): { message: string; category: string } {
  if (status === 401 || status === 403) {
    return {
      message: 'Anthropic authentication failed. Re-provision ANTHROPIC_API_KEY.',
      category: 'INVALID_API_KEY'
    };
  }

  if (status === 429) {
    return {
      message: 'Anthropic rate limit reached. Retry after backoff.',
      category: 'RATE_LIMITED'
    };
  }

  if (status >= 500) {
    return {
      message: 'Anthropic API server error.',
      category: 'API_RESPONSE_ERROR'
    };
  }

  return {
    message: `Anthropic request failed with status ${status}.`,
    category: 'API_RESPONSE_ERROR'
  };
}

async function toAnthropicHttpError(response: Response): Promise<HarnessError> {
  const { message, category } = classifyHttpError(response.status);

  let upstreamMessage: string | undefined;
  let upstreamType: string | undefined;
  try {
    const payload = (await response.json()) as unknown;
    if (isRecord(payload) && isRecord(payload.error)) {
      if (typeof payload.error.message === 'string') {
        upstreamMessage = payload.error.message;
      }
      if (typeof payload.error.type === 'string') {
        upstreamType = payload.error.type;
      }
    }
  } catch {
    // Keep fallback classification message.
  }

  return new HarnessError('SDK_FAILURE', response.status, upstreamMessage ?? message, {
    provider: 'anthropic',
    category,
    upstreamType
  });
}

function toNetworkError(error: unknown): HarnessError | undefined {
  if (!(error instanceof Error)) {
    return undefined;
  }

  if (error.name === 'AbortError') {
    return undefined;
  }

  return new HarnessError('SDK_FAILURE', 503, 'Unable to reach Anthropic API endpoint.', {
    provider: 'anthropic',
    category: 'NETWORK_ERROR',
    cause: error.message
  });
}

export class AnthropicAgentSdkManager implements IAgentSdkManager {
  private readonly activeTurns = new Map<string, ActiveTurnState>();

  async interrupt(sessionId: string): Promise<void> {
    const activeTurn = this.activeTurns.get(sessionId);
    if (!activeTurn) {
      throw new HarnessError('SESSION_NOT_FOUND', 404, `No active turn for session '${sessionId}'`, {
        sessionId
      });
    }

    activeTurn.interrupted = true;
    activeTurn.abortController?.abort();
  }

  async *startTurn(
    session: SessionRecord,
    message: string,
    opts: ResolvedOpts,
    contentBlocks?: ContentBlock[]
  ): AsyncIterable<UIEvent> {
    const turnState: ActiveTurnState = { interrupted: false };
    this.activeTurns.set(session.sessionId, turnState);

    let timeoutHandle: NodeJS.Timeout | undefined;
    let timedOut = false;

    const claudeSessionId = session.claudeSessionId ?? `claude_${randomUUID()}`;
    const trimmedMessage = message.trim();

    try {
      yield {
        type: 'session:init',
        data: {
          claudeSessionId,
          model: opts.model || FALLBACK_MODEL
        }
      };

      if (trimmedMessage === 'bootstrap' && opts.model === BOOT_SDK_FAIL_MODEL_MARKER) {
        yield {
          type: 'process:exit',
          data: {
            exitCode: 1
          }
        };
        return;
      }

      if (trimmedMessage.includes(TURN_SDK_FAIL_MARKER)) {
        throw new HarnessError('SDK_FAILURE', 500, 'Turn failed before completion', {
          marker: TURN_SDK_FAIL_MARKER
        });
      }

      if (opts.mode === 'dontAsk' && trimmedMessage.includes(PERMISSION_DENY_MARKER)) {
        yield {
          type: 'tool:result',
          data: {
            name: 'bash',
            ok: false,
            output: 'permission denied'
          }
        };
        yield {
          type: 'chat:complete',
          data: {
            text: 'Denied: unapproved Bash command under dontAsk.'
          }
        };
        yield {
          type: 'session:complete',
          data: {}
        };
        yield {
          type: 'process:exit',
          data: {
            exitCode: 0
          }
        };
        return;
      }

      if (opts.mode === 'dontAsk' && trimmedMessage.includes(PERMISSION_ALLOW_MARKER)) {
        yield {
          type: 'tool:result',
          data: {
            name: 'bash',
            ok: true,
            output: PERMISSION_ALLOW_MARKER
          }
        };
      }

      const apiKey = readAnthropicApiKey();

      if (trimmedMessage === 'bootstrap') {
        yield {
          type: 'process:exit',
          data: {
            exitCode: 0
          }
        };
        return;
      }

      const resolvedContent = await formatContentBlocks(message, contentBlocks);
      const abortController = new AbortController();
      turnState.abortController = abortController;
      timeoutHandle = setTimeout(() => {
        timedOut = true;
        abortController.abort();
      }, getStreamTimeoutMs());

      const response = await fetch(getAnthropicEndpoint(), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': getAnthropicVersion()
        },
        body: JSON.stringify({
          model: opts.model || FALLBACK_MODEL,
          stream: true,
          max_tokens: getMaxTokens(),
          messages: [
            {
              role: 'user',
              content: resolvedContent
            }
          ]
        }),
        signal: abortController.signal
      });

      if (!response.ok) {
        throw await toAnthropicHttpError(response);
      }

      if (!response.body) {
        throw new HarnessError('SDK_FAILURE', 502, 'Anthropic response did not include a stream', {
          provider: 'anthropic',
          category: 'API_RESPONSE_ERROR'
        });
      }

      let fullText = '';

      for await (const event of iterateSseEvents(response.body)) {
        if (turnState.interrupted) {
          yield {
            type: 'process:exit',
            data: {
              exitCode: 130,
              interrupted: true
            }
          };
          return;
        }

        if (event.event === 'error') {
          throw toAnthropicSseError(event.data);
        }

        const delta = readTextDelta(event);
        if (delta) {
          fullText += delta;
          yield {
            type: 'chat:delta',
            data: {
              text: delta
            }
          };
        }

        if (readMessageStop(event)) {
          break;
        }
      }

      yield {
        type: 'chat:complete',
        data: {
          text: fullText
        }
      };
      yield {
        type: 'session:complete',
        data: {}
      };
      yield {
        type: 'process:exit',
        data: {
          exitCode: 0
        }
      };
    } catch (error) {
      if (turnState.interrupted) {
        yield {
          type: 'process:exit',
          data: {
            exitCode: 130,
            interrupted: true
          }
        };
        return;
      }

      if (timedOut) {
        throw new HarnessError('SDK_FAILURE', 504, 'Anthropic request timed out', {
          provider: 'anthropic',
          category: 'REQUEST_TIMEOUT'
        });
      }

      const networkError = toNetworkError(error);
      if (networkError) {
        throw networkError;
      }

      throw error;
    } finally {
      if (timeoutHandle) {
        clearTimeout(timeoutHandle);
      }
      this.activeTurns.delete(session.sessionId);
    }
  }
}
