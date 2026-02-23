import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { AnthropicAgentSdkManager } from '../../lib/harness/anthropic-agent-sdk-manager';
import { UIEvent } from '../../lib/harness/types';

function createSseResponse(frames: string[]): Response {
  const encoder = new TextEncoder();
  let index = 0;
  const stream = new ReadableStream<Uint8Array>({
    pull(controller) {
      if (index >= frames.length) {
        controller.close();
        return;
      }
      controller.enqueue(encoder.encode(frames[index]));
      index += 1;
    }
  });

  return new Response(stream, {
    status: 200,
    headers: {
      'Content-Type': 'text/event-stream'
    }
  });
}

async function collectEvents(iterable: AsyncIterable<UIEvent>): Promise<UIEvent[]> {
  const events: UIEvent[] = [];
  for await (const event of iterable) {
    events.push(event);
  }
  return events;
}

const session = {
  sessionId: 'sess_provider',
  projectRoot: '/tmp/project',
  persona: 'WORKING_ITEMS',
  mode: 'chat',
  createdAt: '2026-02-23T00:00:00.000Z',
  updatedAt: '2026-02-23T00:00:00.000Z'
};

const opts = {
  model: 'claude-sonnet-test',
  tools: ['read'],
  maxTurns: 4,
  persona: 'WORKING_ITEMS',
  mode: 'chat'
};

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn());
});

afterEach(() => {
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_URL;
  delete process.env.CHIRALITY_ANTHROPIC_MAX_TOKENS;
  delete process.env.CHIRALITY_ANTHROPIC_STREAM_TIMEOUT_MS;
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe('AnthropicAgentSdkManager', () => {
  it('returns successful bootstrap exit without network calls when API key is present', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const manager = new AnthropicAgentSdkManager();

    const events = await collectEvents(manager.startTurn(session, 'bootstrap', opts));

    expect(events.map((event) => event.type)).toEqual(['session:init', 'process:exit']);
    expect(events[1]).toMatchObject({
      type: 'process:exit',
      data: {
        exitCode: 0
      }
    });
    expect(fetch).not.toHaveBeenCalled();
  });

  it('fails with typed SDK_FAILURE when API key is missing', async () => {
    const manager = new AnthropicAgentSdkManager();
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual(['session:init']);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 503
    });
  });

  it('maps Anthropic stream deltas into harness SSE events', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      createSseResponse([
        'event: content_block_delta\ndata: {"delta":{"text":"Hello"}}\n\n',
        'event: content_block_delta\ndata: {"delta":{"text":" world"}}\n\n',
        'event: message_stop\ndata: {"type":"message_stop"}\n\n'
      ])
    );

    const manager = new AnthropicAgentSdkManager();
    const events = await collectEvents(
      manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])
    );

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'chat:delta',
      'chat:delta',
      'chat:complete',
      'session:complete',
      'process:exit'
    ]);
    expect(events[3]).toMatchObject({
      type: 'chat:complete',
      data: {
        text: 'Hello world'
      }
    });
    expect(fetchMock).toHaveBeenCalledWith(
      'https://api.anthropic.com/v1/messages',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'x-api-key': 'test-key'
        })
      })
    );
  });
});
