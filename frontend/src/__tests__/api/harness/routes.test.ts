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
  instructionRoot: string;
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
  const instructionRoot = path.join(tmpRoot, 'instruction-root');
  const agentsDir = path.join(instructionRoot, 'agents');
  const docsDir = path.join(instructionRoot, 'docs');

  await mkdir(projectRoot, { recursive: true });
  await mkdir(agentsDir, { recursive: true });
  await mkdir(docsDir, { recursive: true });

  await writeFile(path.join(projectRoot, 'README.md'), '# fixture\n', 'utf8');
  await writeFile(path.join(instructionRoot, 'AGENTS.md'), '# agents index\n', 'utf8');
  await writeFile(path.join(instructionRoot, 'README.md'), '# instruction root\n', 'utf8');
  await writeFile(path.join(agentsDir, 'AGENT_WORKING_ITEMS.md'), '# persona fixture\n', 'utf8');
  await writeFile(path.join(docsDir, 'DIRECTIVE.md'), '# directive\n', 'utf8');
  await writeFile(path.join(docsDir, 'CONTRACT.md'), '# contract\n', 'utf8');
  await writeFile(path.join(docsDir, 'SPEC.md'), '# spec\n', 'utf8');
  await writeFile(path.join(docsDir, 'TYPES.md'), '# types\n', 'utf8');
  await writeFile(path.join(docsDir, 'PLAN.md'), '# plan\n', 'utf8');

  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpRoot, '.chirality', 'sessions');
  process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;
  context = { tmpRoot, projectRoot, instructionRoot };
});

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  delete process.env.CHIRALITY_ENABLE_SUBAGENTS;
  delete process.env.CHIRALITY_HARNESS_PROVIDER;
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
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

  it('rejects projectRoot selections that overlap instruction root', async () => {
    const routes = await importRouteModules();
    const conflictingProjectRoot = path.join(context.instructionRoot, 'execution');
    await mkdir(conflictingProjectRoot, { recursive: true });

    const response = await routes.createRoute.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: conflictingProjectRoot })
      })
    );

    expect(response.status).toBe(409);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'WORKING_ROOT_CONFLICT'
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

  it('passes subagentGovernance through boot opts without consuming it in fallback resolution', async () => {
    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);
    const governance = {
      contextSealed: true,
      pipelineRunApproved: false,
      approvalRef: 'boot-governance-ref'
    };

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          opts: {
            model: 'claude-test',
            subagentGovernance: governance
          }
        })
      })
    );

    expect(bootResponse.status).toBe(200);
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[1]).toBe('bootstrap');
    expect(startTurnSpy.mock.calls[0]?.[2]).toMatchObject({
      subagentGovernance: governance
    });
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

  it('returns SESSION_NOT_FOUND for a well-formed non-existent session id', async () => {
    const routes = await importRouteModules();
    await createSession(routes, context.projectRoot);

    const bootMissingSession = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: 'sess_00000000-0000-0000-0000-000000000000' })
      })
    );

    expect(bootMissingSession.status).toBe(404);
    expect(await bootMissingSession.json()).toMatchObject({
      error: {
        type: 'SESSION_NOT_FOUND',
        message: expect.any(String)
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

  it('returns INSTRUCTION_ROOT_INVALID when required instruction files are missing', async () => {
    const routes = await importRouteModules();
    await rm(path.join(context.instructionRoot, 'docs', 'PLAN.md'));
    const { body } = await createSession(routes, context.projectRoot);

    const bootResponse = await routes.bootRoute.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId })
      })
    );

    expect(bootResponse.status).toBe(500);
    expect(await bootResponse.json()).toMatchObject({
      error: {
        type: 'INSTRUCTION_ROOT_INVALID'
      }
    });
  });

  it('preserves INSTRUCTION_ROOT_INVALID taxonomy across boot route bundle boundaries', async () => {
    vi.resetModules();

    const [createRouteBundleA, runtimeBundleA] = await Promise.all([
      import('../../../app/api/harness/session/create/route'),
      import('../../../lib/harness/runtime')
    ]);
    runtimeBundleA.resetHarnessRuntimeForTests();

    const createResponse = await createRouteBundleA.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: context.projectRoot })
      })
    );
    expect(createResponse.status).toBe(200);
    const createBody = (await createResponse.json()) as { session: SessionRecord };
    const runtimeBeforeBundleSplit = runtimeBundleA.getHarnessRuntime();

    await rm(path.join(context.instructionRoot, 'docs', 'PLAN.md'));

    vi.resetModules();
    const [bootRouteBundleB, runtimeBundleB] = await Promise.all([
      import('../../../app/api/harness/session/boot/route'),
      import('../../../lib/harness/runtime')
    ]);
    expect(runtimeBundleB.getHarnessRuntime()).toBe(runtimeBeforeBundleSplit);

    const bootResponse = await bootRouteBundleB.POST(
      new Request('http://localhost/api/harness/session/boot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: createBody.session.sessionId })
      })
    );

    expect(bootResponse.status).toBe(500);
    expect(await bootResponse.json()).toMatchObject({
      error: {
        type: 'INSTRUCTION_ROOT_INVALID',
        message: expect.any(String)
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

  it('keeps parent turn execution running when governance metadata is invalid', async () => {
    const routes = await importRouteModules();
    process.env.CHIRALITY_ENABLE_SUBAGENTS = 'true';
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_WORKING_ITEMS.md'),
      `---
description: persona fixture
subagents: TASK
---
# persona
AGENT_TYPE: 1
`,
      'utf8'
    );
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_TASK.md'),
      `---
description: task fixture
---
# task
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | TASK |
`,
      'utf8'
    );

    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'governance deny should stay non-fatal',
          opts: {
            subagentGovernance: {
              contextSealed: false,
              pipelineRunApproved: true,
              approvalRef: 'gate-ref-1'
            }
          }
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    const sseBody = await turnResponse.text();
    expectOrdered(sseBody, [
      'event: session:init',
      'event: chat:delta',
      'event: chat:complete',
      'event: session:complete',
      'event: process:exit'
    ]);
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[2]).toMatchObject({
      delegatedSubagents: []
    });
  });

  it('does not allow opts.subagentGovernance to bypass runtime environment gate', async () => {
    const routes = await importRouteModules();
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_WORKING_ITEMS.md'),
      `---
description: persona fixture
subagents: TASK
---
# persona
AGENT_TYPE: 1
`,
      'utf8'
    );
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_TASK.md'),
      `---
description: task fixture
---
# task
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | TASK |
`,
      'utf8'
    );

    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'env gate should block delegation',
          opts: {
            subagentGovernance: {
              contextSealed: true,
              pipelineRunApproved: true,
              approvalRef: 'gate-ref-2'
            }
          }
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[2]).toMatchObject({
      delegatedSubagents: []
    });
  });

  it('passes delegated subagents when governance gates are satisfied', async () => {
    const routes = await importRouteModules();
    process.env.CHIRALITY_ENABLE_SUBAGENTS = 'true';
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_WORKING_ITEMS.md'),
      `---
description: persona fixture
subagents: TASK
---
# persona
AGENT_TYPE: 1
`,
      'utf8'
    );
    await writeFile(
      path.join(context.instructionRoot, 'agents', 'AGENT_TASK.md'),
      `---
description: task fixture
---
# task
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | TASK |
`,
      'utf8'
    );

    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'governance allow path',
          opts: {
            subagentGovernance: {
              contextSealed: true,
              pipelineRunApproved: true,
              approvalRef: 'gate-ref-3',
              approvedBy: 'human-reviewer'
            }
          }
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[2]).toMatchObject({
      delegatedSubagents: ['TASK']
    });
  });

  it('emits typed process-exit metadata when runtime turn execution fails', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'TURN_SDK_FAIL_TEST'
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    const sseBody = await turnResponse.text();
    expect(sseBody).toContain('event: process:exit');
    expect(sseBody).toContain('"exitCode":1');
    expect(sseBody).toContain('"errorType":"SDK_FAILURE"');
    expect(sseBody).toContain('"error":"Turn failed before completion"');
  });

  it('returns pre-stream MISSING_API_KEY when anthropic provider is selected without API key', async () => {
    process.env.CHIRALITY_HARNESS_PROVIDER = 'anthropic';
    delete process.env.ANTHROPIC_API_KEY;
    delete process.env.CHIRALITY_ANTHROPIC_API_KEY;

    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'hello'
        })
      })
    );

    expect(turnResponse.status).toBe(503);
    expect(turnResponse.headers.get('content-type') ?? '').toContain('application/json');
    expect(await turnResponse.json()).toMatchObject({
      error: {
        type: 'MISSING_API_KEY'
      }
    });
    expect(startTurnSpy).not.toHaveBeenCalled();
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

  it('prepends attachment warning context when partial attachment resolution succeeds', async () => {
    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);
    const validAttachmentPath = path.join(context.projectRoot, 'sample.txt');
    await writeFile(validAttachmentPath, 'attachment fixture', 'utf8');

    const response = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'Review attached context',
          attachments: [validAttachmentPath, '/does/not/exist.bin']
        })
      })
    );

    expect(response.status).toBe(200);
    await response.text();

    const contentBlocks = startTurnSpy.mock.calls[0]?.[3] as
      | Array<
          | { type: 'text'; text: string }
          | { type: 'file'; path: string; mimeType: string }
        >
      | undefined;
    expect(contentBlocks).toBeDefined();
    expect(contentBlocks?.[0]).toMatchObject({
      type: 'text'
    });
    if (!contentBlocks || contentBlocks.length === 0 || contentBlocks[0].type !== 'text') {
      throw new Error('Expected a warning text block as the first content block');
    }
    expect(contentBlocks[0].text).toContain('Attachment warning');
    expect(contentBlocks[0].text).toContain('/does/not/exist.bin');
    expect(contentBlocks[1]).toMatchObject({
      type: 'text',
      text: 'Review attached context'
    });
    expect(contentBlocks.some((block) => block.type === 'file' && block.path === validAttachmentPath)).toBe(
      true
    );
  });

  it('uses string prompt mode when no executable attachments are present', async () => {
    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);

    const response = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'text-only turn'
        })
      })
    );

    expect(response.status).toBe(200);
    await response.text();
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[1]).toBe('text-only turn');
    expect(startTurnSpy.mock.calls[0]?.[3]).toBeUndefined();
  });

  it('falls back to string prompt mode with warning text when all attachments fail but text remains', async () => {
    const routes = await importRouteModules();
    const runtime = routes.runtimeModule.getHarnessRuntime();
    const startTurnSpy = vi.spyOn(runtime.agentSdkManager, 'startTurn');
    const { body } = await createSession(routes, context.projectRoot);
    const missingPath = path.join(context.projectRoot, 'missing.txt');

    const response = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'continue without attachments',
          attachments: [missingPath]
        })
      })
    );

    expect(response.status).toBe(200);
    await response.text();
    expect(startTurnSpy).toHaveBeenCalled();
    expect(startTurnSpy.mock.calls[0]?.[3]).toBeUndefined();
    const turnMessage = startTurnSpy.mock.calls[0]?.[1];
    expect(typeof turnMessage).toBe('string');
    expect(turnMessage).toContain('Attachment warning');
    expect(turnMessage).toContain('continue without attachments');
    expect(turnMessage).toContain(missingPath);
  });

  it('rejects overlapping turns for the same session and releases lock after completion', async () => {
    const routes = await importRouteModules();
    const { body } = await createSession(routes, context.projectRoot);

    const firstTurnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'INTERRUPT_SIGINT_TEST keep this turn active briefly'
        })
      })
    );
    expect(firstTurnResponse.status).toBe(200);

    const reader = firstTurnResponse.body?.getReader();
    expect(reader).toBeTruthy();
    const firstChunk = await reader!.read();
    expect(firstChunk.done).toBe(false);

    const overlappingTurnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'this should be rejected while another turn is active'
        })
      })
    );
    expect(overlappingTurnResponse.status).toBe(409);
    expect(await overlappingTurnResponse.json()).toMatchObject({
      error: {
        type: 'TURN_IN_PROGRESS'
      }
    });

    const interruptResponse = await routes.interruptRoute.POST(
      new Request('http://localhost/api/harness/interrupt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: body.session.sessionId })
      })
    );
    expect(interruptResponse.status).toBe(200);

    while (true) {
      const chunk = await reader!.read();
      if (chunk.done) {
        break;
      }
    }

    const recoveryTurnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: body.session.sessionId,
          message: 'turn lock should be released after completion'
        })
      })
    );
    expect(recoveryTurnResponse.status).toBe(200);
    await recoveryTurnResponse.text();
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

  it('keeps turn and interrupt routes coherent across module-bundle boundaries', async () => {
    vi.resetModules();

    const [createRouteBundleA, turnRouteBundleA, runtimeBundleA] = await Promise.all([
      import('../../../app/api/harness/session/create/route'),
      import('../../../app/api/harness/turn/route'),
      import('../../../lib/harness/runtime')
    ]);
    runtimeBundleA.resetHarnessRuntimeForTests();

    const createResponse = await createRouteBundleA.POST(
      new Request('http://localhost/api/harness/session/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: context.projectRoot })
      })
    );
    expect(createResponse.status).toBe(200);
    const createBody = (await createResponse.json()) as { session: SessionRecord };
    const runtimeBeforeBundleSplit = runtimeBundleA.getHarnessRuntime();

    const turnResponse = await turnRouteBundleA.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: createBody.session.sessionId,
          message: 'INTERRUPT_SIGINT_TEST cross-bundle coherence'
        })
      })
    );

    expect(turnResponse.status).toBe(200);
    const reader = turnResponse.body?.getReader();
    expect(reader).toBeTruthy();
    const decoder = new TextDecoder();
    let streamText = '';

    const firstChunk = await reader!.read();
    expect(firstChunk.done).toBe(false);
    if (firstChunk.value) {
      streamText += decoder.decode(firstChunk.value, { stream: true });
    }

    vi.resetModules();
    const [interruptRouteBundleB, runtimeBundleB] = await Promise.all([
      import('../../../app/api/harness/interrupt/route'),
      import('../../../lib/harness/runtime')
    ]);
    expect(runtimeBundleB.getHarnessRuntime()).toBe(runtimeBeforeBundleSplit);

    const interruptResponse = await interruptRouteBundleB.POST(
      new Request('http://localhost/api/harness/interrupt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: createBody.session.sessionId })
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
