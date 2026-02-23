#!/usr/bin/env node

import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

const HARNESS_BASE_URL = process.env.HARNESS_BASE_URL ?? 'http://127.0.0.1:3000';
const TMP_ROOT = path.join(
  process.env.TMPDIR ?? os.tmpdir(),
  'chirality-harness-validation',
  'latest'
);
const OUTPUT_DIRS = {
  api: path.join(TMP_ROOT, 'api'),
  sse: path.join(TMP_ROOT, 'sse'),
  logs: path.join(TMP_ROOT, 'logs'),
  cleanup: path.join(TMP_ROOT, 'cleanup')
};

const REQUIRED_CHECK_ORDER = [
  'setup.server_reachable',
  'regression.session_crud',
  'section8.boot_error_taxonomy',
  'section8.smoke_stream',
  'section8.session_persistence_resume',
  'section8.permissions_dontask',
  'section8.interrupt_sigint',
  'section8.sdk_native_stream'
];

const encoder = new TextEncoder();
const decoder = new TextDecoder();

function nowIso() {
  return new Date().toISOString();
}

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function urlFor(pathname, params = {}) {
  const url = new URL(pathname, HARNESS_BASE_URL);
  for (const [key, value] of Object.entries(params)) {
    url.searchParams.set(key, value);
  }
  return url.toString();
}

function resolveProjectRoot() {
  if (process.env.HARNESS_PROJECT_ROOT) {
    return path.resolve(process.env.HARNESS_PROJECT_ROOT);
  }

  const inferredRepoRoot = path.resolve(process.cwd(), '..');
  return inferredRepoRoot;
}

function parseSse(raw) {
  const events = [];
  const segments = raw.split('\n\n');

  for (const segment of segments) {
    const lines = segment.trim().split('\n').filter(Boolean);
    if (lines.length === 0) {
      continue;
    }

    let eventType = null;
    const dataLines = [];

    for (const line of lines) {
      if (line.startsWith('event:')) {
        eventType = line.slice('event:'.length).trim();
      } else if (line.startsWith('data:')) {
        dataLines.push(line.slice('data:'.length).trim());
      }
    }

    if (!eventType) {
      continue;
    }

    let data = null;
    if (dataLines.length) {
      try {
        data = JSON.parse(dataLines.join('\n'));
      } catch {
        data = dataLines.join('\n');
      }
    }

    events.push({ type: eventType, data });
  }

  return events;
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function assertOrderedEvents(events, expectedOrder) {
  let previousIndex = -1;
  for (const type of expectedOrder) {
    const index = events.findIndex((event, idx) => idx > previousIndex && event.type === type);
    if (index < 0) {
      throw new Error(`Missing ordered SSE event '${type}'`);
    }
    previousIndex = index;
  }
}

function testResultToLog(result) {
  const output = {
    id: result.id,
    status: result.status,
    startedAt: result.startedAt,
    endedAt: result.endedAt,
    durationMs: result.durationMs
  };
  if (result.details !== undefined) {
    output.details = result.details;
  }
  if (result.error !== undefined) {
    output.error = result.error;
  }
  return output;
}

async function ensureOutputLayout() {
  await rm(TMP_ROOT, { recursive: true, force: true });
  await mkdir(OUTPUT_DIRS.api, { recursive: true });
  await mkdir(OUTPUT_DIRS.sse, { recursive: true });
  await mkdir(OUTPUT_DIRS.logs, { recursive: true });
  await mkdir(OUTPUT_DIRS.cleanup, { recursive: true });
}

async function writeJson(filePath, payload) {
  await writeFile(filePath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

async function writeText(filePath, text) {
  await writeFile(filePath, text, 'utf8');
}

async function requestJson(pathname, { method = 'GET', body, query } = {}) {
  const response = await fetch(urlFor(pathname, query), {
    method,
    headers: {
      'Content-Type': 'application/json'
    },
    body: body ? JSON.stringify(body) : undefined
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  return { response, payload };
}

async function requestSse(pathname, body) {
  const response = await fetch(urlFor(pathname), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });
  const raw = await response.text();
  const events = parseSse(raw);
  return { response, raw, events };
}

async function requestSseWithInterrupt(pathname, body, sessionId) {
  const response = await fetch(urlFor(pathname), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });

  assert(response.ok, `Turn request failed with HTTP ${response.status}`);
  assert(response.body, 'Expected readable SSE body');

  let raw = '';
  let interruptPayload = null;
  let interruptStatus = null;
  let interruptSent = false;

  const interruptPromise = (async () => {
    await sleep(50);
    interruptSent = true;
    const startedAt = Date.now();
    const retryWindowMs = 2000;
    const retryDelayMs = 50;

    while (Date.now() - startedAt <= retryWindowMs) {
      const interrupt = await requestJson('/api/harness/interrupt', {
        method: 'POST',
        body: { sessionId }
      });
      interruptStatus = interrupt.response.status;
      interruptPayload = interrupt.payload;

      if (interruptStatus !== 404) {
        return;
      }

      await sleep(retryDelayMs);
    }
  })();

  const reader = response.body.getReader();

  while (true) {
    const chunk = await reader.read();
    if (chunk.done) {
      break;
    }

    raw += decoder.decode(chunk.value, { stream: true });
  }

  await interruptPromise;
  raw += decoder.decode(encoder.encode(''), { stream: false });
  const events = parseSse(raw);
  return { response, raw, events, interruptStatus, interruptPayload, interruptSent };
}

async function main() {
  await ensureOutputLayout();

  const projectRoot = resolveProjectRoot();
  const createdSessions = new Set();
  const cleanedSessions = [];
  const cleanupFailures = [];
  const results = [];

  async function createSession(options) {
    let body;
    if (typeof options === 'string') {
      body = {
        projectRoot,
        mode: options
      };
    } else {
      body = {
        projectRoot: options?.projectRoot ?? projectRoot
      };
      if (options?.mode) {
        body.mode = options.mode;
      }
      if (options?.persona) {
        body.persona = options.persona;
      }
    }

    const sessionResponse = await requestJson('/api/harness/session/create', {
      method: 'POST',
      body
    });

    assert(
      sessionResponse.response.status === 200 && sessionResponse.payload?.session?.sessionId,
      `Session creation failed: HTTP ${sessionResponse.response.status}`
    );

    const sessionId = sessionResponse.payload.session.sessionId;
    createdSessions.add(sessionId);
    return sessionId;
  }

  async function deleteSession(sessionId) {
    const deleted = await requestJson(`/api/harness/session/${sessionId}`, { method: 'DELETE' });
    if (deleted.response.status === 200) {
      cleanedSessions.push(sessionId);
      createdSessions.delete(sessionId);
      return;
    }

    cleanupFailures.push({
      sessionId,
      status: deleted.response.status,
      payload: deleted.payload
    });
  }

  async function runCheck(id, run) {
    const startedAt = nowIso();
    const startMs = Date.now();
    try {
      const details = await run();
      const endedAt = nowIso();
      const result = {
        id,
        status: 'pass',
        startedAt,
        endedAt,
        durationMs: Date.now() - startMs,
        details
      };
      results.push(result);
      await writeJson(path.join(OUTPUT_DIRS.logs, `${id}.json`), testResultToLog(result));
    } catch (error) {
      const endedAt = nowIso();
      const message = error instanceof Error ? error.message : String(error);
      const result = {
        id,
        status: 'fail',
        startedAt,
        endedAt,
        durationMs: Date.now() - startMs,
        error: message
      };
      results.push(result);
      await writeJson(path.join(OUTPUT_DIRS.logs, `${id}.json`), testResultToLog(result));
    }
  }

  await runCheck('setup.server_reachable', async () => {
    const check = await requestJson('/api/harness/session/list', {
      query: { projectRoot }
    });
    assert(check.response.status === 200, `Expected 200; received ${check.response.status}`);
    await writeJson(path.join(OUTPUT_DIRS.api, 'setup.server_reachable.json'), {
      status: check.response.status,
      payload: check.payload
    });
    return { httpStatus: check.response.status };
  });

  await runCheck('regression.session_crud', async () => {
    const sessionId = await createSession();

    const list = await requestJson('/api/harness/session/list', {
      query: { projectRoot }
    });
    assert(list.response.status === 200, 'Session list failed');
    const listedSessionIds = (list.payload?.sessions ?? []).map((item) => item.sessionId);
    assert(
      listedSessionIds.includes(sessionId),
      `Session list does not include created session '${sessionId}'`
    );

    const get = await requestJson(`/api/harness/session/${sessionId}`);
    assert(get.response.status === 200, 'Session get failed');

    await deleteSession(sessionId);

    const getAfterDelete = await requestJson(`/api/harness/session/${sessionId}`);
    assert(getAfterDelete.response.status === 404, 'Deleted session should return 404');

    await writeJson(path.join(OUTPUT_DIRS.api, 'regression.session_crud.json'), {
      listedSessionIds,
      getStatus: get.response.status,
      getAfterDeleteStatus: getAfterDelete.response.status
    });

    return {
      sessionId,
      listedCount: listedSessionIds.length
    };
  });

  await runCheck('section8.boot_error_taxonomy', async () => {
    const missingSessionId = `missing-${Date.now()}`;
    const missingSessionBoot = await requestJson('/api/harness/session/boot', {
      method: 'POST',
      body: { sessionId: missingSessionId }
    });
    assert(missingSessionBoot.response.status === 404, 'Missing-session boot should return 404');
    assert(
      missingSessionBoot.payload?.error?.type === 'SESSION_NOT_FOUND',
      'Missing-session boot should return SESSION_NOT_FOUND'
    );

    const personaSessionId = await createSession({ persona: 'PERSONA_DOES_NOT_EXIST' });
    const personaBoot = await requestJson('/api/harness/session/boot', {
      method: 'POST',
      body: { sessionId: personaSessionId }
    });
    assert(personaBoot.response.status === 404, 'Unknown-persona boot should return 404');
    assert(
      personaBoot.payload?.error?.type === 'PERSONA_NOT_FOUND',
      'Unknown-persona boot should return PERSONA_NOT_FOUND'
    );
    await deleteSession(personaSessionId);

    const sdkFailureSessionId = await createSession();
    const sdkFailureBoot = await requestJson('/api/harness/session/boot', {
      method: 'POST',
      body: {
        sessionId: sdkFailureSessionId,
        opts: {
          model: '__BOOT_SDK_FAIL__'
        }
      }
    });
    assert(sdkFailureBoot.response.status === 500, 'SDK-failure boot should return 500');
    assert(
      sdkFailureBoot.payload?.error?.type === 'SDK_FAILURE',
      'SDK-failure boot should return SDK_FAILURE'
    );
    await deleteSession(sdkFailureSessionId);

    const inaccessibleRoot = path.join(TMP_ROOT, 'workroots', `missing-${Date.now()}`);
    await mkdir(inaccessibleRoot, { recursive: true });
    const inaccessibleSessionId = await createSession({ projectRoot: inaccessibleRoot });
    await rm(inaccessibleRoot, { recursive: true, force: true });
    const inaccessibleBoot = await requestJson('/api/harness/session/boot', {
      method: 'POST',
      body: { sessionId: inaccessibleSessionId }
    });
    assert(
      inaccessibleBoot.response.status === 404,
      'Inaccessible-root boot should return 404'
    );
    assert(
      inaccessibleBoot.payload?.error?.type === 'WORKING_ROOT_INACCESSIBLE',
      'Inaccessible-root boot should return WORKING_ROOT_INACCESSIBLE'
    );
    await deleteSession(inaccessibleSessionId);

    await writeJson(path.join(OUTPUT_DIRS.api, 'section8.boot_error_taxonomy.json'), {
      missingSession: {
        status: missingSessionBoot.response.status,
        type: missingSessionBoot.payload?.error?.type
      },
      unknownPersona: {
        status: personaBoot.response.status,
        type: personaBoot.payload?.error?.type
      },
      sdkFailure: {
        status: sdkFailureBoot.response.status,
        type: sdkFailureBoot.payload?.error?.type
      },
      inaccessibleRoot: {
        status: inaccessibleBoot.response.status,
        type: inaccessibleBoot.payload?.error?.type
      }
    });

    return {
      checkedCodes: [
        missingSessionBoot.payload?.error?.type,
        personaBoot.payload?.error?.type,
        sdkFailureBoot.payload?.error?.type,
        inaccessibleBoot.payload?.error?.type
      ]
    };
  });

  await runCheck('section8.smoke_stream', async () => {
    const sessionId = await createSession();
    const turn = await requestSse('/api/harness/turn', {
      sessionId,
      message: 'Smoke stream ordering validation'
    });

    assert(turn.response.status === 200, `Turn failed with HTTP ${turn.response.status}`);
    assertOrderedEvents(turn.events, [
      'session:init',
      'chat:delta',
      'chat:complete',
      'session:complete',
      'process:exit'
    ]);

    await writeText(path.join(OUTPUT_DIRS.sse, 'section8.smoke_stream.sse'), turn.raw);
    await writeJson(path.join(OUTPUT_DIRS.api, 'section8.smoke_stream.json'), {
      eventTypes: turn.events.map((event) => event.type)
    });

    await deleteSession(sessionId);
    return { eventCount: turn.events.length };
  });

  await runCheck('section8.session_persistence_resume', async () => {
    const sessionId = await createSession();

    const firstTurn = await requestSse('/api/harness/turn', {
      sessionId,
      message: 'First turn to initialize claudeSessionId'
    });
    const firstSessionInit = firstTurn.events.find((event) => event.type === 'session:init');
    assert(firstSessionInit?.data?.claudeSessionId, 'First turn missing session:init claudeSessionId');

    const sessionAfterFirst = await requestJson(`/api/harness/session/${sessionId}`);
    assert(sessionAfterFirst.response.status === 200, 'Unable to read session after first turn');
    const persistedAfterFirst = sessionAfterFirst.payload?.session?.claudeSessionId;
    assert(
      persistedAfterFirst === firstSessionInit.data.claudeSessionId,
      'Persisted claudeSessionId mismatch after first turn'
    );

    const secondTurn = await requestSse('/api/harness/turn', {
      sessionId,
      message: 'Second turn should resume existing session'
    });
    const secondSessionInit = secondTurn.events.find((event) => event.type === 'session:init');
    assert(secondSessionInit?.data?.claudeSessionId, 'Second turn missing session:init claudeSessionId');

    const sessionAfterSecond = await requestJson(`/api/harness/session/${sessionId}`);
    assert(sessionAfterSecond.response.status === 200, 'Unable to read session after second turn');
    const persistedAfterSecond = sessionAfterSecond.payload?.session?.claudeSessionId;

    assert(
      persistedAfterSecond === secondSessionInit.data.claudeSessionId,
      'Persisted claudeSessionId mismatch after second turn'
    );
    assert(
      secondSessionInit.data.claudeSessionId === firstSessionInit.data.claudeSessionId,
      'Resume continuity failed: claudeSessionId changed between turns'
    );

    await writeJson(path.join(OUTPUT_DIRS.api, 'section8.session_persistence_resume.json'), {
      firstClaudesessionId: firstSessionInit.data.claudeSessionId,
      secondClaudesessionId: secondSessionInit.data.claudeSessionId,
      persistedAfterFirst,
      persistedAfterSecond
    });

    await deleteSession(sessionId);
    return {
      claudeSessionId: firstSessionInit.data.claudeSessionId
    };
  });

  await runCheck('section8.permissions_dontask', async () => {
    const sessionId = await createSession('dontAsk');

    const denyTurn = await requestSse('/api/harness/turn', {
      sessionId,
      message: 'UNAPPROVED_DENY_TEST run dangerous command'
    });
    assert(denyTurn.response.status === 200, 'Deny turn failed');
    const denyToolResult = denyTurn.events.find((event) => event.type === 'tool:result');
    assert(denyToolResult, 'Deny case missing tool:result event');
    assert(denyToolResult.data?.ok === false, 'Deny tool result should report ok=false');
    assert(
      !denyTurn.raw.includes('UNAPPROVED_ALLOW_TEST'),
      'Deny case unexpectedly contains allow token output'
    );

    const allowTurn = await requestSse('/api/harness/turn', {
      sessionId,
      message: 'UNAPPROVED_ALLOW_TEST run allow-list command'
    });
    assert(allowTurn.response.status === 200, 'Allow turn failed');
    const allowToolResult = allowTurn.events.find((event) => event.type === 'tool:result');
    assert(allowToolResult, 'Allow case missing tool:result event');
    assert(allowToolResult.data?.ok === true, 'Allow tool result should report ok=true');
    assert(
      String(allowToolResult.data?.output ?? '').includes('UNAPPROVED_ALLOW_TEST'),
      'Allow tool result missing UNAPPROVED_ALLOW_TEST marker'
    );

    await writeText(path.join(OUTPUT_DIRS.sse, 'section8.permissions_dontask.deny.sse'), denyTurn.raw);
    await writeText(path.join(OUTPUT_DIRS.sse, 'section8.permissions_dontask.allow.sse'), allowTurn.raw);
    await writeJson(path.join(OUTPUT_DIRS.api, 'section8.permissions_dontask.json'), {
      denyEventTypes: denyTurn.events.map((event) => event.type),
      allowEventTypes: allowTurn.events.map((event) => event.type)
    });

    await deleteSession(sessionId);
    return {
      denyEvents: denyTurn.events.length,
      allowEvents: allowTurn.events.length
    };
  });

  await runCheck('section8.interrupt_sigint', async () => {
    const sessionId = await createSession();
    const longMessage = 'INTERRUPT_SIGINT_TEST '.repeat(40);

    const interruptedTurn = await requestSseWithInterrupt(
      '/api/harness/turn',
      { sessionId, message: longMessage },
      sessionId
    );

    assert(interruptedTurn.interruptSent, 'Interrupt call was not dispatched');
    assert(
      interruptedTurn.interruptStatus === 200,
      `Interrupt endpoint returned ${interruptedTurn.interruptStatus}`
    );
    assert(
      interruptedTurn.interruptPayload?.ok === true,
      'Interrupt endpoint payload did not return { ok: true }'
    );

    const exitEvent = interruptedTurn.events.find((event) => event.type === 'process:exit');
    assert(exitEvent, 'Interrupted stream missing process:exit');
    assert(exitEvent.data?.interrupted === true, 'process:exit missing interrupted=true');
    assert(exitEvent.data?.exitCode === 130, 'process:exit missing exitCode 130');

    await writeText(path.join(OUTPUT_DIRS.sse, 'section8.interrupt_sigint.sse'), interruptedTurn.raw);
    await writeJson(path.join(OUTPUT_DIRS.api, 'section8.interrupt_sigint.json'), {
      interruptStatus: interruptedTurn.interruptStatus,
      interruptPayload: interruptedTurn.interruptPayload,
      eventTypes: interruptedTurn.events.map((event) => event.type)
    });

    await deleteSession(sessionId);
    return { interruptStatus: interruptedTurn.interruptStatus };
  });

  await runCheck('section8.sdk_native_stream', async () => {
    const sessionId = await createSession();
    const turn = await requestSse('/api/harness/turn', {
      sessionId,
      message: 'sdk-native-stream validation baseline'
    });

    assert(turn.response.status === 200, `Turn failed with HTTP ${turn.response.status}`);
    assert(
      turn.events.some((event) => event.type === 'chat:complete'),
      'SDK native stream missing chat:complete'
    );
    assert(
      turn.events.some((event) => event.type === 'process:exit'),
      'SDK native stream missing process:exit'
    );
    assert(
      !turn.events.some((event) => event.type === 'parse:error'),
      'SDK native stream unexpectedly emitted parse:error'
    );

    await writeText(path.join(OUTPUT_DIRS.sse, 'section8.sdk_native_stream.sse'), turn.raw);
    await writeJson(path.join(OUTPUT_DIRS.api, 'section8.sdk_native_stream.json'), {
      eventTypes: turn.events.map((event) => event.type)
    });

    await deleteSession(sessionId);
    return { eventCount: turn.events.length };
  });

  for (const sessionId of [...createdSessions]) {
    await deleteSession(sessionId);
  }

  await writeJson(path.join(OUTPUT_DIRS.cleanup, 'sessions.json'), {
    cleanedSessions,
    cleanupFailures
  });

  const normalizedResults = REQUIRED_CHECK_ORDER.map((id) => {
    const found = results.find((result) => result.id === id);
    if (found) {
      return found;
    }

    return {
      id,
      status: 'fail',
      startedAt: nowIso(),
      endedAt: nowIso(),
      durationMs: 0,
      error: 'Check did not execute'
    };
  });

  const status = normalizedResults.every((result) => result.status === 'pass') ? 'pass' : 'fail';
  const summary = {
    generatedAt: nowIso(),
    harnessBaseUrl: HARNESS_BASE_URL,
    projectRoot,
    status,
    testCount: normalizedResults.length,
    results: normalizedResults.map((result) => {
      const output = {
        id: result.id,
        status: result.status,
        durationMs: result.durationMs
      };
      if (result.details !== undefined) {
        output.details = result.details;
      }
      if (result.error !== undefined) {
        output.error = result.error;
      }
      return output;
    })
  };

  const summaryPath = path.join(TMP_ROOT, 'summary.json');
  await writeJson(summaryPath, summary);

  // Warm read to ensure summary is parseable JSON and file permissions are stable.
  await readFile(summaryPath, 'utf8');

  console.log(`HARNESS_VALIDATION_SUMMARY_PATH=${summaryPath}`);
  console.log(`HARNESS_VALIDATION_STATUS=${status}`);

  process.exitCode = status === 'pass' ? 0 : 1;
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error('Harness validation crashed:', message);
  process.exitCode = 1;
});
