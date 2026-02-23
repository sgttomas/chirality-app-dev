import { afterEach, describe, expect, it, vi } from 'vitest';
import { AnthropicAgentSdkManager } from '../../lib/harness/anthropic-agent-sdk-manager';
import { UIEvent } from '../../lib/harness/types';

async function* createStream(events: unknown[]): AsyncIterable<unknown> {
  for (const event of events) {
    yield event;
  }
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

afterEach(() => {
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_URL;
  delete process.env.CHIRALITY_ANTHROPIC_MAX_TOKENS;
  delete process.env.CHIRALITY_ANTHROPIC_STREAM_TIMEOUT_MS;
  delete process.env.CHIRALITY_ANTHROPIC_VERSION;
});

describe('AnthropicAgentSdkManager', () => {
  it('returns successful bootstrap exit without SDK calls when API key is present', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn();
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    const events = await collectEvents(manager.startTurn(session, 'bootstrap', opts));

    expect(events.map((event) => event.type)).toEqual(['session:init', 'process:exit']);
    expect(events[1]).toMatchObject({
      type: 'process:exit',
      data: {
        exitCode: 0
      }
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails with typed SDK_FAILURE when API key is missing', async () => {
    const createMock = vi.fn();
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
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
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('maps Anthropic stream deltas into harness SSE events using SDK stream', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/messages';
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        { type: 'content_block_delta', delta: { text: 'Hello' } },
        { type: 'content_block_delta', delta: { text: ' world' } },
        { type: 'message_stop' }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));

    const manager = new AnthropicAgentSdkManager(clientFactory as never);
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
    expect(clientFactory).toHaveBeenCalledWith({
      apiKey: 'test-key',
      baseURL: 'https://api.anthropic.com',
      anthropicVersion: '2023-06-01'
    });
    expect(createMock).toHaveBeenCalledWith(
      expect.objectContaining({
        model: 'claude-sonnet-test',
        stream: true,
        max_tokens: 1024
      }),
      expect.objectContaining({
        signal: expect.any(AbortSignal)
      })
    );
  });

  it('maps SDK auth errors to typed invalid-key failures', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: 'invalid x-api-key'
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
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
      status: 401,
      details: expect.objectContaining({
        category: 'INVALID_API_KEY'
      })
    });
  });
});
