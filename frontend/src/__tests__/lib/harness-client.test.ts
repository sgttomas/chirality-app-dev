import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  HarnessApiClientError,
  bootHarnessSession,
  createHarnessSession,
  scaffoldHarnessExecutionRoot,
  streamHarnessTurn
} from '../../lib/harness/client';

function jsonResponse(payload: unknown, status = 200): Response {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      'Content-Type': 'application/json'
    }
  });
}

function sseResponse(chunks: string[]): Response {
  const encoder = new TextEncoder();
  let index = 0;

  const stream = new ReadableStream<Uint8Array>({
    pull(controller) {
      if (index >= chunks.length) {
        controller.close();
        return;
      }

      controller.enqueue(encoder.encode(chunks[index]));
      index += 1;
    }
  });

  return new Response(stream, {
    status: 200,
    headers: {
      'Content-Type': 'text/event-stream; charset=utf-8'
    }
  });
}

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn());
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe('harness client helpers', () => {
  it('creates sessions through create route', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      jsonResponse({
        session: {
          sessionId: 'sess_1',
          projectRoot: '/tmp/project',
          persona: 'WORKING_ITEMS',
          mode: 'WORKBENCH',
          createdAt: '2026-02-23T00:00:00.000Z',
          updatedAt: '2026-02-23T00:00:00.000Z'
        }
      })
    );

    const session = await createHarnessSession({
      projectRoot: '/tmp/project',
      persona: 'WORKING_ITEMS',
      mode: 'WORKBENCH'
    });

    expect(session.sessionId).toBe('sess_1');
    const [input, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(input).toBe('/api/harness/session/create');
    expect(init.method).toBe('POST');
  });

  it('surfaces typed boot errors for non-2xx responses', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      jsonResponse(
        {
          error: {
            type: 'PERSONA_NOT_FOUND',
            message: 'Persona not found'
          }
        },
        404
      )
    );

    await expect(bootHarnessSession({ sessionId: 'sess_1' })).rejects.toEqual(
      expect.objectContaining({
        name: 'HarnessApiClientError',
        status: 404,
        code: 'PERSONA_NOT_FOUND'
      }) satisfies Partial<HarnessApiClientError>
    );
  });

  it('parses SSE frames for streaming turns', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      sseResponse([
        'event: chat:delta\ndata: {"text":"Hel"}\n\n',
        'event: chat:delta\ndata: {"text":"lo"}\n\n',
        'event: chat:complete\ndata: {"text":"Hello"}\n\n',
        'event: process:exit\ndata: {"exitCode":0}\n\n'
      ])
    );

    const events: Array<{ event: string; data: unknown }> = [];

    await streamHarnessTurn(
      {
        sessionId: 'sess_1',
        message: 'hello'
      },
      (event) => {
        events.push(event);
      }
    );

    expect(events.map((entry) => entry.event)).toEqual([
      'chat:delta',
      'chat:delta',
      'chat:complete',
      'process:exit'
    ]);
    expect(fetchMock).toHaveBeenCalledWith(
      '/api/harness/turn',
      expect.objectContaining({
        method: 'POST'
      })
    );
  });

  it('scaffolds execution roots through scaffold route', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      jsonResponse({
        executionRoot: '/tmp/execution',
        decompositionPath: '/tmp/decomposition.md',
        copiedDecompositionPath: '/tmp/execution/_Decomposition/decomposition.md',
        projectName: 'Example',
        coordinationMode: 'DEPENDENCY_TRACKED',
        packageCount: 1,
        deliverableCount: 1,
        created: {
          directories: ['/tmp/execution/_Coordination'],
          files: ['/tmp/execution/INIT.md']
        },
        layoutValidation: {
          valid: true,
          executionRoot: {
            path: '/tmp/execution',
            valid: true,
            missing: []
          },
          packages: [],
          deliverables: []
        },
        preparationCompatibility: {
          ready: true,
          deliverablesChecked: 1,
          issueCount: 0,
          deliverables: []
        }
      })
    );

    const result = await scaffoldHarnessExecutionRoot({
      executionRoot: '/tmp/execution',
      decompositionPath: '/tmp/decomposition.md'
    });

    expect(result.layoutValidation.valid).toBe(true);
    expect(result.preparationCompatibility.ready).toBe(true);
    const [input, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(input).toBe('/api/harness/scaffold');
    expect(init.method).toBe('POST');
  });
});
