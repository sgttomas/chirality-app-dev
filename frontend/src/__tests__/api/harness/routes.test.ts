import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

type SessionRecord = {
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
};

type RouteModules = {
  createRoute: typeof import('../../../app/api/harness/session/create/route');
  listRoute: typeof import('../../../app/api/harness/session/list/route');
  idRoute: typeof import('../../../app/api/harness/session/[id]/route');
  bootRoute: typeof import('../../../app/api/harness/session/boot/route');
  turnRoute: typeof import('../../../app/api/harness/turn/route');
  interruptRoute: typeof import('../../../app/api/harness/interrupt/route');
  runtimeModule: typeof import('../../../lib/harness/runtime');
};

type TestContext = {
  tmpRoot: string;
  projectRoot: string;
};

let context: TestContext;

async function importRouteModules(): Promise<RouteModules> {
  vi.resetModules();

  const [createRoute, listRoute, idRoute, bootRoute, turnRoute, interruptRoute, runtimeModule] =
    await Promise.all([
      import('../../../app/api/harness/session/create/route'),
      import('../../../app/api/harness/session/list/route'),
      import('../../../app/api/harness/session/[id]/route'),
      import('../../../app/api/harness/session/boot/route'),
      import('../../../app/api/harness/turn/route'),
      import('../../../app/api/harness/interrupt/route'),
      import('../../../lib/harness/runtime')
    ]);

  runtimeModule.resetHarnessRuntimeForTests();

  return {
    createRoute,
    listRoute,
    idRoute,
    bootRoute,
    turnRoute,
    interruptRoute,
    runtimeModule
  };
}

async function createSession(
  routes: RouteModules,
  projectRoot: string,
  overrides?: {
    persona?: string;
    mode?: string;
  }
): Promise<{ response: Response; body: { session: SessionRecord } }> {
  const response = await routes.createRoute.POST(
    new Request('http://localhost/api/harness/session/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        projectRoot,
        persona: overrides?.persona,
        mode: overrides?.mode
      })
    })
  );

  const body = (await response.json()) as { session: SessionRecord };
  return { response, body };
}

function expectOrdered(text: string, fragments: string[]): void {
  let current = -1;
  for (const fragment of fragments) {
    const index = text.indexOf(fragment);
    expect(index).toBeGreaterThan(current);
    current = index;
  }
}

beforeEach(async () => {
  const tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-harness-routes-'));
  const projectRoot = path.join(tmpRoot, 'project-root');
  await mkdir(projectRoot, { recursive: true });
  await writeFile(path.join(projectRoot, 'README.md'), '# fixture\n', 'utf8');

  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpRoot, '.chirality', 'sessions');
  context = { tmpRoot, projectRoot };
});

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  await rm(context.tmpRoot, { recursive: true, force: true });
});

describe('Harness API baseline routes', () => {
  it('supports session create/list/get/delete happy path', async () => {
    const routes = await importRouteModules();

    const { response: createResponse, body: createBody } = await createSession(
      routes,
      context.projectRoot
    );
    expect(createResponse.status).toBe(200);
    expect(createBody.session.projectRoot).toBe(context.projectRoot);

    const listResponse = await routes.listRoute.GET(
      new Request(
        `http://localhost/api/harness/session/list?projectRoot=${encodeURIComponent(context.projectRoot)}`
      )
    );
    expect(listResponse.status).toBe(200);
    const listBody = (await listResponse.json()) as { sessions: SessionRecord[] };
    expect(listBody.sessions.map((item) => item.sessionId)).toContain(createBody.session.sessionId);

    const getResponse = await routes.idRoute.GET(new Request('http://localhost'), {
      params: { id: createBody.session.sessionId }
    });
    expect(getResponse.status).toBe(200);

    const deleteResponse = await routes.idRoute.DELETE(new Request('http://localhost'), {
      params: { id: createBody.session.sessionId }
    });
    expect(deleteResponse.status).toBe(200);
    expect(await deleteResponse.json()).toEqual({ ok: true });

    const getAfterDelete = await routes.idRoute.GET(new Request('http://localhost'), {
      params: { id: createBody.session.sessionId }
    });
    expect(getAfterDelete.status).toBe(404);
    expect(await getAfterDelete.json()).toMatchObject({
      error: { type: 'SESSION_NOT_FOUND' }
    });
  });

  it('returns typed validation failure for missing projectRoot', async () => {
    const routes = await importRouteModules();

    const response = await routes.createRoute.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      })
    );

    expect(response.status).toBe(400);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'INVALID_REQUEST'
      }
    });
  });

  it('returns typed failure when projectRoot is inaccessible at create time', async () => {
    const routes = await importRouteModules();
    const missingProjectRoot = path.join(context.tmpRoot, 'missing-project-root');

    const response = await routes.createRoute.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: missingProjectRoot })
      })
    );

    expect(response.status).toBe(404);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'WORKING_ROOT_INACCESSIBLE'
      }
    });
  });

  it('boots sessions and persists boot metadata', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId, opts: { model: 'claude-test' } })
      })
    );

    expect(bootResponse.status).toBe(200);
    const bootBody = (await bootResponse.json()) as {
      session: SessionRecord;
      boot: { claudeSessionId: string; bootFingerprint: string; bootedAt: string };
    };

    expect(typeof bootBody.boot.claudeSessionId).toBe('string');
    expect(typeof bootBody.boot.bootFingerprint).toBe('string');
    expect(typeof bootBody.boot.bootedAt).toBe('string');
    expect(bootBody.session.bootFingerprint).toBe(bootBody.boot.bootFingerprint);
  });

  it('returns SESSION_NOT_FOUND when booting without prior create', async () => {
    const routes = await importRouteModules();

    const bootMissingSession = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: 'sess_missing' })
      })
    );

    expect(bootMissingSession.status).toBe(404);
    expect(await bootMissingSession.json()).toMatchObject({
      error: {
        type: 'SESSION_NOT_FOUND'
      }
    });
  });

  it('returns WORKING_ROOT_INACCESSIBLE when booting a session with missing projectRoot', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);
    await rm(context.projectRoot, { recursive: true, force: true });

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId })
      })
    );

    expect(bootResponse.status).toBe(404);
    expect(await bootResponse.json()).toMatchObject({
      error: {
        type: 'WORKING_ROOT_INACCESSIBLE'
      }
    });
  });

  it('returns PERSONA_NOT_FOUND when boot references unknown persona', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot, {
      persona: 'NON_EXISTENT_PERSONA'
    });

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId })
      })
    );

    expect(bootResponse.status).toBe(404);
    expect(await bootResponse.json()).toMatchObject({
      error: {
        type: 'PERSONA_NOT_FOUND'
      }
    });
  });

  it('returns SDK_FAILURE when bootstrap turn exits non-zero', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          opts: { model: '__BOOT_SDK_FAIL__' }
        })
      })
    );

    expect(bootResponse.status).toBe(500);
    expect(await bootResponse.json()).toMatchObject({
      error: {
        type: 'SDK_FAILURE'
      }
    });
  });

  it('streams ordered SSE events for turn execution', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'Hello from route tests',
          opts: { model: 'claude-test' }
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    expect(turnResponse.headers.get('content-type')).toContain('text/event-stream');

    const sseBody = await turnResponse.text();
    expectOrdered(sseBody, [
      'event: session:init',
      'event: chat:delta',
      'event: chat:complete',
      'event: session:complete',
      'event: process:exit'
    ]);
  });

  it('rejects attachment-only turns when all attachments fail and no text remains', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const response = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: '   ',
          attachments: ['/does/not/exist.bin']
        })
      })
    );

    expect(response.status).toBe(400);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'ATTACHMENT_FAILURE'
      }
    });
  });

  it('interrupt endpoint returns ok and marks active turn as interrupted', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'This turn should be interrupted while streaming.'
        })
      })
    );

    const reader = turnResponse.body?.getReader();
    expect(reader).toBeTruthy();

    const decoder = new TextDecoder();
    let streamText = '';

    const firstChunk = await reader!.read();
    if (firstChunk.value) {
      streamText += decoder.decode(firstChunk.value, { stream: true });
    }

    const interruptResponse = await routes.interruptRoute.POST(
      new Request('http://localhost/api/harness/interrupt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId })
      })
    );

    expect(interruptResponse.status).toBe(200);
    expect(await interruptResponse.json()).toEqual({ ok: true });

    while (true) {
      const chunk = await reader!.read();
      if (chunk.done) {
        break;
      }
      if (chunk.value) {
        streamText += decoder.decode(chunk.value, { stream: true });
      }
    }

    expect(streamText).toContain('event: process:exit');
    expect(streamText).toContain('"interrupted":true');
  });

  it('returns typed failure for interrupt on unknown session', async () => {
    const routes = await importRouteModules();

    const interruptResponse = await routes.interruptRoute.POST(
      new Request('http://localhost/api/harness/interrupt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: 'sess_unknown' })
      })
    );

    expect(interruptResponse.status).toBe(404);
    expect(await interruptResponse.json()).toMatchObject({
      error: {
        type: 'SESSION_NOT_FOUND'
      }
    });
  });
});
