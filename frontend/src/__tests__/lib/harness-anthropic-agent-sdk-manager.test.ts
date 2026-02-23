import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
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

function toLowercasePercentEncoding(value: string): string {
  return value.replace(/%[0-9A-F]{2}/g, (match) => match.toLowerCase());
}

function toDoubleUrlEncoding(value: string): string {
  return encodeURIComponent(encodeURIComponent(value));
}

function toDoubleQueryStyleEncoding(value: string): string {
  return encodeURIComponent(encodeURIComponent(value).replace(/%20/g, '+'));
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

let tmpDir = '';

async function writeFixtureFile(name: string, content: string | Buffer): Promise<string> {
  if (!tmpDir) {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'anthropic-sdk-manager-test-'));
  }
  const filePath = path.join(tmpDir, name);
  await writeFile(filePath, content);
  return filePath;
}

async function getFixturePath(name: string): Promise<string> {
  if (!tmpDir) {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'anthropic-sdk-manager-test-'));
  }
  return path.join(tmpDir, name);
}

afterEach(() => {
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_URL;
  delete process.env.CHIRALITY_ANTHROPIC_MAX_TOKENS;
  delete process.env.CHIRALITY_ANTHROPIC_STREAM_TIMEOUT_MS;
  delete process.env.CHIRALITY_ANTHROPIC_VERSION;
});

afterEach(async () => {
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
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

  it('fails closed when CHIRALITY_ANTHROPIC_API_URL host is outside Anthropic allowlist', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'https://example.com/v1/messages';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
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
      status: 400,
      details: expect.objectContaining({
        category: 'NETWORK_POLICY_VIOLATION',
        host: 'example.com',
        policy: 'REQ-NET-001'
      })
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails closed when CHIRALITY_ANTHROPIC_API_URL does not use https', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'http://api.anthropic.com/v1/messages';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
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
      status: 400,
      details: expect.objectContaining({
        category: 'NETWORK_POLICY_VIOLATION',
        policy: 'REQ-NET-001',
        protocol: 'http:'
      })
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails with typed SDK_FAILURE when CHIRALITY_ANTHROPIC_API_URL is malformed', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'not-a-url';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
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
      status: 400,
      details: expect.objectContaining({
        category: 'INVALID_BASE_URL'
      })
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails closed when CHIRALITY_ANTHROPIC_API_URL includes credentials', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'https://user:pass@api.anthropic.com/v1/messages';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
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
      status: 400,
      details: expect.objectContaining({
        category: 'NETWORK_POLICY_VIOLATION',
        policy: 'REQ-NET-001'
      })
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails closed when CHIRALITY_ANTHROPIC_API_URL uses non-default https port', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'https://api.anthropic.com:444/v1/messages';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
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
      status: 400,
      details: expect.objectContaining({
        category: 'NETWORK_POLICY_VIOLATION',
        policy: 'REQ-NET-001',
        port: '444'
      })
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('accepts CHIRALITY_ANTHROPIC_API_URL when explicit default https port is used', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'https://api.anthropic.com:443/v1/messages';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));

    expect(clientFactory).toHaveBeenCalledWith({
      apiKey: 'test-key',
      baseURL: 'https://api.anthropic.com',
      anthropicVersion: '2023-06-01'
    });
    expect(createMock).toHaveBeenCalledTimes(1);
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

  it('redacts configured API key material from SDK error messages', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: 'provided key test-key is invalid'
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain('test-key');
  });

  it('redacts URL-encoded configured API key material from SDK error messages', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const encodedKey = encodeURIComponent(process.env.ANTHROPIC_API_KEY);
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: `provided key ${encodedKey} is invalid`
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(encodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts lowercase URL-encoded configured API key material from SDK error messages', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const lowercaseEncodedKey = toLowercasePercentEncoding(
      encodeURIComponent(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: `provided key ${lowercaseEncodedKey} is invalid`
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(lowercaseEncodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts double URL-encoded configured API key material from SDK error messages', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const doubleEncodedKey = toLowercasePercentEncoding(
      toDoubleUrlEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: `provided key ${doubleEncodedKey} is invalid`
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(doubleEncodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts double URL-encoded query-style configured API key material from SDK error messages', async () => {
    process.env.ANTHROPIC_API_KEY = 'test key/with space';
    const doubleQueryEncodedKey = toLowercasePercentEncoding(
      toDoubleQueryStyleEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: `provided key ${doubleQueryEncodedKey} is invalid`
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(doubleQueryEncodedKey);
    expect((thrown as Error).message).not.toContain('test key/with space');
  });

  it('redacts overlapping canonical and alias key material without leaking suffixes', async () => {
    process.env.ANTHROPIC_API_KEY = 'KEY';
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'KEY_LONG';
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: 'canonical=KEY alias=KEY_LONG failed'
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toBe(
      'canonical=[REDACTED_API_KEY] alias=[REDACTED_API_KEY] failed'
    );
    expect((thrown as Error).message).not.toContain('KEY_LONG');
    expect((thrown as Error).message).not.toContain('_LONG');
  });

  it('redacts configured API key material from stream error events', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        {
          type: 'error',
          error: {
            status: 502,
            type: 'api_error',
            message: 'upstream rejected key test-key'
          }
        }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain('test-key');
  });

  it('redacts URL-encoded configured API key material from stream error events', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const encodedKey = encodeURIComponent(process.env.ANTHROPIC_API_KEY);
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        {
          type: 'error',
          error: {
            status: 502,
            type: 'api_error',
            message: `upstream rejected key ${encodedKey}`
          }
        }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(encodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts lowercase URL-encoded configured API key material from stream error events', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const lowercaseEncodedKey = toLowercasePercentEncoding(
      encodeURIComponent(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        {
          type: 'error',
          error: {
            status: 502,
            type: 'api_error',
            message: `upstream rejected key ${lowercaseEncodedKey}`
          }
        }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(lowercaseEncodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts double URL-encoded configured API key material from stream error events', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const doubleEncodedKey = toLowercasePercentEncoding(
      toDoubleUrlEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        {
          type: 'error',
          error: {
            status: 502,
            type: 'api_error',
            message: `upstream rejected key ${doubleEncodedKey}`
          }
        }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(doubleEncodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts double URL-encoded query-style configured API key material from stream error events', async () => {
    process.env.ANTHROPIC_API_KEY = 'test key/with space';
    const doubleQueryEncodedKey = toLowercasePercentEncoding(
      toDoubleQueryStyleEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        {
          type: 'error',
          error: {
            status: 502,
            type: 'api_error',
            message: `upstream rejected key ${doubleQueryEncodedKey}`
          }
        }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(doubleQueryEncodedKey);
    expect((thrown as Error).message).not.toContain('test key/with space');
  });

  it('redacts configured API key material from network error details', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockRejectedValue(new Error('socket rejected key test-key'));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.stringContaining('[REDACTED_API_KEY]')
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining('test-key')
      })
    });
  });

  it('redacts URL-encoded configured API key material from network error details', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const encodedKey = encodeURIComponent(process.env.ANTHROPIC_API_KEY);
    const createMock = vi.fn().mockRejectedValue(new Error(`socket rejected key ${encodedKey}`));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.stringContaining('[REDACTED_API_KEY]')
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining(encodedKey)
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining('test:key/with?chars=1')
      })
    });
  });

  it('redacts lowercase URL-encoded configured API key material from network error details', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const lowercaseEncodedKey = toLowercasePercentEncoding(
      encodeURIComponent(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockRejectedValue(new Error(`socket rejected key ${lowercaseEncodedKey}`));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.stringContaining('[REDACTED_API_KEY]')
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining(lowercaseEncodedKey)
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining('test:key/with?chars=1')
      })
    });
  });

  it('redacts double URL-encoded configured API key material from network error details', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const doubleEncodedKey = toLowercasePercentEncoding(
      toDoubleUrlEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockRejectedValue(new Error(`socket rejected key ${doubleEncodedKey}`));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.stringContaining('[REDACTED_API_KEY]')
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining(doubleEncodedKey)
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining('test:key/with?chars=1')
      })
    });
  });

  it('redacts double URL-encoded query-style configured API key material from network error details', async () => {
    process.env.ANTHROPIC_API_KEY = 'test key/with space';
    const doubleQueryEncodedKey = toLowercasePercentEncoding(
      toDoubleQueryStyleEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi
      .fn()
      .mockRejectedValue(new Error(`socket rejected key ${doubleQueryEncodedKey}`));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.stringContaining('[REDACTED_API_KEY]')
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining(doubleQueryEncodedKey)
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining('test key/with space')
      })
    });
  });

  it('uses compatibility alias key when canonical key is unset', async () => {
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'alias-key';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));

    expect(clientFactory).toHaveBeenCalledWith(
      expect.objectContaining({
        apiKey: 'alias-key'
      })
    );
  });

  it('prefers canonical API key when both canonical and alias keys are set', async () => {
    process.env.ANTHROPIC_API_KEY = 'canonical-key';
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'alias-key';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));

    expect(clientFactory).toHaveBeenCalledWith(
      expect.objectContaining({
        apiKey: 'canonical-key'
      })
    );
  });

  it('formats image attachments as Anthropic image content blocks', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('fake-image-data');
    const imagePath = await writeFixtureFile('fixture.png', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: 'application/octet-stream' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('fails with typed ATTACHMENT_FAILURE when image attachment is unreadable', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const missingImagePath = await getFixturePath('missing-fixture.png');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(
        manager.startTurn(session, 'hello', opts, [
          { type: 'text', text: 'hello' },
          { type: 'file', path: missingImagePath, mimeType: 'image/png' }
        ])
      );
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      type: 'ATTACHMENT_FAILURE',
      status: 400,
      details: {
        path: missingImagePath
      }
    });
    expect((thrown as Error).message).toContain(`Attachment '${missingImagePath}' is not readable`);
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails with typed ATTACHMENT_FAILURE when image attachment exceeds inline byte limit', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const oversizedImagePath = await writeFixtureFile(
      'oversized-image.png',
      Buffer.alloc((5 * 1024 * 1024) + 1, 1)
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(
        manager.startTurn(session, 'hello', opts, [
          { type: 'text', text: 'hello' },
          { type: 'file', path: oversizedImagePath, mimeType: 'image/png' }
        ])
      );
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      type: 'ATTACHMENT_FAILURE',
      status: 400,
      details: {
        path: oversizedImagePath,
        byteLength: (5 * 1024 * 1024) + 1,
        limit: 5 * 1024 * 1024
      }
    });
    expect((thrown as Error).message).toContain('exceeds 5242880 byte inline image limit');
    expect(createMock).not.toHaveBeenCalled();
  });

  it('accepts image attachment when byte size is exactly at inline limit', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const maxInlineBytes = 5 * 1024 * 1024;
    const atLimitImageBytes = Buffer.alloc(maxInlineBytes, 1);
    const atLimitImagePath = await writeFixtureFile('at-limit-image.png', atLimitImageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: atLimitImagePath, mimeType: 'image/png' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: atLimitImageBytes.toString('base64')
        }
      }
    ]);
  });

  it('normalizes resolver-provided image mime metadata before classification', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-classified-image-data');
    const imagePath = await writeFixtureFile('resolver-output.bin', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' Image/PNG ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('normalizes resolver-provided image mime metadata with parameters', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-classified-image-data-with-params');
    const imagePath = await writeFixtureFile('resolver-output-with-params.bin', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' Image/PNG; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('treats uppercase octet-stream mime as extension-fallback input', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-octet-stream-image-data');
    const imagePath = await writeFixtureFile('resolver-output.PNG', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' APPLICATION/OCTET-STREAM ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('treats parameterized octet-stream mime as extension-fallback input', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-octet-stream-image-data-with-params');
    const imagePath = await writeFixtureFile('resolver-output-with-params.PNG', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' APPLICATION/OCTET-STREAM; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has no media-type token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-missing-token-image-data');
    const imagePath = await writeFixtureFile('resolver-output-with-empty-token.JpEg', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/jpeg',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to extension and normalizes webp when resolver mime metadata has no media-type token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-missing-token-webp-image-data');
    const imagePath = await writeFixtureFile('resolver-output-with-empty-token.WeBp', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has malformed image token without subtype', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-malformed-token-image-data');
    const imagePath = await writeFixtureFile('resolver-output-with-malformed-token.GiF', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/ ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/gif',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has malformed image token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('resolver-output-with-malformed-token.bin', 'placeholder');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/ ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-malformed-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has wildcard subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-wildcard-subtype-image-data');
    const imagePath = await writeFixtureFile('resolver-output-with-wildcard-token.PnG', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/* ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has wildcard subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('resolver-output-with-wildcard-token.bin', 'placeholder');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/* ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-wildcard-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-image-subtype-data');
    const imagePath = await writeFixtureFile('resolver-output-with-unsupported-image-token.JpEg', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/bmp ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/jpeg',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('resolver-output-with-unsupported-image-token.bin', 'placeholder');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/bmp ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-image-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported image alias subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-image-alias-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-image-alias-token.JpEg',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/jpg ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/jpeg',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported image alias subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-image-alias-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/jpg ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-image-alias-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported vendor-tree image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-vendor-tree-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-vendor-tree-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/x-png ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported vendor-tree image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-vendor-tree-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/x-png ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-vendor-tree-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported dotted vendor-tree image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-dotted-vendor-tree-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-dotted-vendor-tree-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/vnd.microsoft.icon ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported dotted vendor-tree image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-dotted-vendor-tree-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/vnd.microsoft.icon ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-dotted-vendor-tree-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported personal-tree image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-personal-tree-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-personal-tree-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/prs.btif ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported personal-tree image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-personal-tree-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/prs.btif ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-personal-tree-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported structured-suffix image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-structured-suffix-image-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-structured-suffix-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/svg+xml ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported structured-suffix image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-structured-suffix-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/svg+xml ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-structured-suffix-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has no media-type token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('resolver-output-with-empty-token.bin', 'placeholder');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-empty-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('trusts resolver-provided image mime type even when extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-classified-image-data');
    const imagePath = await writeFixtureFile('resolver-output.bin', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: 'image/png' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('keeps resolver-provided non-image mime authoritative even when extension is image-like', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('resolver-classified.png', '%PDF-1.7 test');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: 'application/pdf' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-classified.png' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('keeps parameterized resolver-provided non-image mime authoritative even when extension is image-like', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('resolver-classified-with-params.png', '%PDF-1.7 test');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' application/pdf; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-classified-with-params.png' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('formats non-image attachments into explicit text fallback blocks', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('notes.txt', 'hello');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: filePath, mimeType: 'application/octet-stream' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'text',
        text: "Attachment 'notes.txt' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('preserves resolver warning text blocks and keeps document blocks in explicit fallback text', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('spec.pdf', '%PDF-1.7 test');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review the attachment', opts, [
        {
          type: 'text',
          text: "Attachment warning: 'legacy.bmp' rejected (unsupported extension)."
        },
        { type: 'text', text: 'review the attachment' },
        { type: 'file', path: filePath, mimeType: 'application/pdf' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      {
        type: 'text',
        text: "Attachment warning: 'legacy.bmp' rejected (unsupported extension)."
      },
      { type: 'text', text: 'review the attachment' },
      {
        type: 'text',
        text: "Attachment 'spec.pdf' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });
});
