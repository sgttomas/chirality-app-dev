#!/usr/bin/env node

import { spawn } from 'node:child_process';
import { createWriteStream } from 'node:fs';
import { appendFile, cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const FRONTEND_ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const REPO_ROOT = path.resolve(FRONTEND_ROOT, '..');
const DELIVERABLE_ROOT = path.resolve(
  REPO_ROOT,
  'execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails'
);

const LOOPBACK_HOSTS = new Set(['localhost', '127.0.0.1', '::1', '[::1]']);
const ALLOWLIST_HOSTS = new Set(['api.anthropic.com']);

const DEFAULT_RUN_COUNT = 3;
const DEFAULT_IDLE_SECONDS = 600;
const DEFAULT_IDLE_SAMPLE_SECONDS = 60;
const DEFAULT_HTTP_TIMEOUT_MS = 120_000;
const DEFAULT_STARTUP_WAIT_MS = 4000;

function timestampForPath(date = new Date()) {
  return date.toISOString().replace(/[:]/g, '').replace(/\..+$/, '').replace('T', '_');
}

function parseIntegerArg(value, fallback) {
  if (value === undefined) {
    return fallback;
  }

  const parsed = Number.parseInt(value, 10);
  if (!Number.isSafeInteger(parsed) || parsed <= 0) {
    return fallback;
  }

  return parsed;
}

function parseArgs(argv) {
  const args = {
    runs: DEFAULT_RUN_COUNT,
    idleSeconds: DEFAULT_IDLE_SECONDS,
    idleSampleSeconds: DEFAULT_IDLE_SAMPLE_SECONDS,
    outputDir: path.resolve(
      DELIVERABLE_ROOT,
      'Evidence',
      `OI-002_PROOF_${timestampForPath()}`
    )
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    if (token === '--runs' && argv[index + 1]) {
      args.runs = parseIntegerArg(argv[index + 1], args.runs);
      index += 1;
      continue;
    }

    if (token === '--idle-seconds' && argv[index + 1]) {
      args.idleSeconds = parseIntegerArg(argv[index + 1], args.idleSeconds);
      index += 1;
      continue;
    }

    if (token === '--idle-sample-seconds' && argv[index + 1]) {
      args.idleSampleSeconds = parseIntegerArg(argv[index + 1], args.idleSampleSeconds);
      index += 1;
      continue;
    }

    if (token === '--output-dir' && argv[index + 1]) {
      args.outputDir = path.resolve(argv[index + 1]);
      index += 1;
    }
  }

  return args;
}

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function toIsoNow() {
  return new Date().toISOString();
}

function parseRemoteHost(remote) {
  if (!remote) {
    return '';
  }

  if (remote.startsWith('[')) {
    const close = remote.indexOf(']');
    if (close > 1) {
      return remote.slice(1, close);
    }
  }

  const lastColon = remote.lastIndexOf(':');
  if (lastColon > 0) {
    return remote.slice(0, lastColon);
  }

  return remote;
}

function classifyRemoteHost(host) {
  const normalized = host.trim().toLowerCase();
  if (!normalized) {
    return 'unknown';
  }

  if (LOOPBACK_HOSTS.has(normalized)) {
    return 'loopback';
  }

  if (ALLOWLIST_HOSTS.has(normalized)) {
    return 'allowlisted';
  }

  if (normalized.endsWith('.anthropic.com')) {
    return 'anthropic_non_allowlisted';
  }

  return 'external_non_allowlisted';
}

function parseLsofTcp(output) {
  const lines = output.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const remoteEndpoints = [];
  for (const line of lines) {
    if (!line.includes('->')) {
      continue;
    }

    const arrowIndex = line.indexOf('->');
    const remoteField = line.slice(arrowIndex + 2).split(' ')[0];
    const remoteHost = parseRemoteHost(remoteField);
    remoteEndpoints.push({
      endpoint: remoteField,
      host: remoteHost,
      class: classifyRemoteHost(remoteHost)
    });
  }

  return {
    rawLineCount: lines.length,
    remoteEndpoints
  };
}

async function runCommand(command, args, options = {}) {
  return new Promise((resolve) => {
    const child = spawn(command, args, {
      cwd: options.cwd,
      env: options.env,
      stdio: ['ignore', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (chunk) => {
      stdout += chunk.toString();
    });

    child.stderr.on('data', (chunk) => {
      stderr += chunk.toString();
    });

    child.on('close', (code) => {
      resolve({ code: code ?? 1, stdout, stderr });
    });
  });
}

function startLoggedProcess({ label, command, args, cwd, env, logPath }) {
  const child = spawn(command, args, {
    cwd,
    env,
    stdio: ['ignore', 'pipe', 'pipe']
  });

  const stream = createWriteStream(logPath, { flags: 'a' });
  stream.write(`[${toIsoNow()}] START ${label}: ${command} ${args.join(' ')}\n`);

  child.stdout.on('data', (chunk) => {
    stream.write(chunk);
  });

  child.stderr.on('data', (chunk) => {
    stream.write(chunk);
  });

  child.on('close', (code, signal) => {
    stream.write(`[${toIsoNow()}] EXIT ${label}: code=${code ?? 'null'} signal=${signal ?? 'null'}\n`);
  });

  return { child, stream };
}

async function stopProcess(child, label, timeoutMs = 10_000) {
  if (!child || child.exitCode !== null) {
    return;
  }

  child.kill('SIGTERM');
  const start = Date.now();

  while (child.exitCode === null && Date.now() - start < timeoutMs) {
    await sleep(100);
  }

  if (child.exitCode === null) {
    child.kill('SIGKILL');
    const hardStart = Date.now();
    while (child.exitCode === null && Date.now() - hardStart < 2000) {
      await sleep(50);
    }
  }

  if (child.exitCode === null) {
    throw new Error(`Failed to stop ${label} process`);
  }
}

async function waitForHttpReady(url, timeoutMs, processToWatch) {
  const started = Date.now();

  while (Date.now() - started < timeoutMs) {
    if (processToWatch && processToWatch.exitCode !== null) {
      throw new Error(`Observed process exit before HTTP readiness at ${url}`);
    }

    try {
      const response = await fetch(url, { method: 'GET' });
      if (response.ok || response.status === 404) {
        return;
      }
    } catch {
      // keep waiting until timeout
    }

    await sleep(500);
  }

  throw new Error(`Timed out waiting for HTTP readiness at ${url}`);
}

async function postJson(url, payload) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  const text = await response.text();
  let parsed = null;
  try {
    parsed = JSON.parse(text);
  } catch {
    // no-op: preserve raw text
  }

  return {
    status: response.status,
    ok: response.ok,
    raw: text,
    parsed
  };
}

async function postTurnSse(url, payload) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  const text = await response.text();
  const events = [];

  let currentEvent = null;
  let currentData = [];

  for (const line of text.split(/\r?\n/)) {
    if (line.startsWith('event:')) {
      currentEvent = line.slice('event:'.length).trim();
      continue;
    }

    if (line.startsWith('data:')) {
      currentData.push(line.slice('data:'.length).trim());
      continue;
    }

    if (line.trim().length === 0 && currentEvent) {
      const dataString = currentData.join('\n');
      let parsed = null;
      try {
        parsed = JSON.parse(dataString);
      } catch {
        parsed = null;
      }

      events.push({
        event: currentEvent,
        rawData: dataString,
        data: parsed
      });

      currentEvent = null;
      currentData = [];
    }
  }

  return {
    status: response.status,
    ok: response.ok,
    raw: text,
    events
  };
}

async function captureTcpSnapshot({ runDir, label, processLabel, pid }) {
  const capture = {
    timestamp: toIsoNow(),
    label,
    processLabel,
    pid,
    lsofExitCode: 0,
    raw: '',
    parsed: {
      rawLineCount: 0,
      remoteEndpoints: []
    }
  };

  if (!Number.isSafeInteger(pid) || pid <= 0) {
    capture.lsofExitCode = 1;
    return capture;
  }

  const result = await runCommand('lsof', [
    '-P',
    '-a',
    `-p${pid}`,
    '-iTCP',
    '-sTCP:LISTEN,ESTABLISHED,SYN_SENT,CLOSE_WAIT'
  ]);

  capture.lsofExitCode = result.code;
  capture.raw = `${result.stdout}${result.stderr}`.trim();

  if (result.code === 0 && result.stdout.trim().length > 0) {
    capture.parsed = parseLsofTcp(result.stdout);
  }

  await appendFile(
    path.resolve(runDir, 'tcp_snapshots.ndjson'),
    `${JSON.stringify(capture)}\n`,
    'utf8'
  );

  return capture;
}

function summarizeSnapshotEndpoints(snapshots) {
  const unique = new Map();

  for (const snapshot of snapshots) {
    for (const endpoint of snapshot.parsed.remoteEndpoints) {
      const key = `${endpoint.host}|${endpoint.endpoint}|${endpoint.class}`;
      if (!unique.has(key)) {
        unique.set(key, {
          host: endpoint.host,
          endpoint: endpoint.endpoint,
          class: endpoint.class,
          firstSeen: snapshot.timestamp,
          label: snapshot.label,
          processLabel: snapshot.processLabel
        });
      }
    }
  }

  return Array.from(unique.values());
}

function extractProbePayloads(logText) {
  const payloads = [];
  const lines = logText.split(/\r?\n/);

  for (const line of lines) {
    const markerIndex = line.indexOf('[network-policy-probe]');
    if (markerIndex === -1) {
      continue;
    }

    const jsonPart = line.slice(markerIndex + '[network-policy-probe]'.length).trim();
    if (!jsonPart) {
      continue;
    }

    try {
      payloads.push(JSON.parse(jsonPart));
    } catch {
      payloads.push({ parseError: true, raw: jsonPart });
    }
  }

  return payloads;
}

async function runProofCycle({ runIndex, args, outputDir }) {
  const runId = `run-${String(runIndex).padStart(2, '0')}`;
  const runDir = path.resolve(outputDir, runId);
  await mkdir(runDir, { recursive: true });
  const workingRootSource = path.resolve(REPO_ROOT, 'examples/example-project');
  const workingRootPath = path.resolve('/tmp', `chirality-proof-${runId}-${timestampForPath()}`);
  const sessionRootPath = path.resolve('/tmp', `chirality-proof-sessions-${runId}-${timestampForPath()}`);
  await cp(workingRootSource, workingRootPath, { recursive: true });
  await mkdir(sessionRootPath, { recursive: true });

  const baseEnv = {
    ...process.env,
    NEXT_TELEMETRY_DISABLED: '1',
    ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY || 'sk-ant-proof-placeholder',
    CHIRALITY_ANTHROPIC_STREAM_TIMEOUT_MS: process.env.CHIRALITY_ANTHROPIC_STREAM_TIMEOUT_MS || '15000',
    CHIRALITY_SESSION_ROOT: sessionRootPath
  };

  const nextLogPath = path.resolve(runDir, 'next.log');
  const electronLogPath = path.resolve(runDir, 'electron.log');

  const nextProcess = startLoggedProcess({
    label: `${runId}:next`,
    command: path.resolve(FRONTEND_ROOT, 'node_modules/.bin/next'),
    args: ['dev', '--port', '3000', '--hostname', '127.0.0.1'],
    cwd: FRONTEND_ROOT,
    env: baseEnv,
    logPath: nextLogPath
  });

  let electronProcess;
  const snapshots = [];
  const timeline = [];

  try {
    timeline.push({ at: toIsoNow(), step: 'next_start' });
    await waitForHttpReady('http://127.0.0.1:3000', DEFAULT_HTTP_TIMEOUT_MS, nextProcess.child);
    timeline.push({ at: toIsoNow(), step: 'next_ready' });

    const probeUrls = [
      'https://example.com/chirality-network-policy-blocked-check',
      'https://api.anthropic.com/v1/messages',
      'http://127.0.0.1:3000/'
    ].join(',');

    electronProcess = startLoggedProcess({
      label: `${runId}:electron`,
      command: path.resolve(FRONTEND_ROOT, 'node_modules/.bin/electron'),
      args: ['dist-electron/main.js'],
      cwd: FRONTEND_ROOT,
      env: {
        ...baseEnv,
        ELECTRON_RENDERER_URL: 'http://127.0.0.1:3000',
        CHIRALITY_NETWORK_POLICY_PROBE_URLS: probeUrls,
        CHIRALITY_NETWORK_POLICY_PROBE_DELAY_MS: '2500',
        CHIRALITY_NETWORK_POLICY_PROBE_TIMEOUT_MS: '8000'
      },
      logPath: electronLogPath
    });

    timeline.push({ at: toIsoNow(), step: 'electron_start' });
    await sleep(DEFAULT_STARTUP_WAIT_MS);

    snapshots.push(
      await captureTcpSnapshot({
        runDir,
        label: 'startup_next',
        processLabel: 'next',
        pid: nextProcess.child.pid
      })
    );

    snapshots.push(
      await captureTcpSnapshot({
        runDir,
        label: 'startup_electron',
        processLabel: 'electron',
        pid: electronProcess.child.pid
      })
    );

    const createResponse = await postJson('http://127.0.0.1:3000/api/harness/session/create', {
      projectRoot: workingRootPath,
      persona: 'CHANGE',
      mode: 'ask'
    });

    await writeFile(path.resolve(runDir, 'session_create.json'), JSON.stringify(createResponse, null, 2));

    if (!createResponse.ok || !createResponse.parsed?.session?.sessionId) {
      throw new Error(`Session create failed for ${runId}`);
    }

    const sessionId = createResponse.parsed.session.sessionId;

    const bootResponse = await postJson('http://127.0.0.1:3000/api/harness/session/boot', {
      sessionId,
      opts: {
        persona: 'CHANGE',
        mode: 'ask'
      }
    });

    await writeFile(path.resolve(runDir, 'session_boot.json'), JSON.stringify(bootResponse, null, 2));

    snapshots.push(
      await captureTcpSnapshot({
        runDir,
        label: 'post_boot_next',
        processLabel: 'next',
        pid: nextProcess.child.pid
      })
    );

    snapshots.push(
      await captureTcpSnapshot({
        runDir,
        label: 'post_boot_electron',
        processLabel: 'electron',
        pid: electronProcess.child.pid
      })
    );

    const turnResponse = await postTurnSse('http://127.0.0.1:3000/api/harness/turn', {
      sessionId,
      message: `DEL-03-06 OI-002 proof run ${runId}`,
      opts: {
        persona: 'CHANGE',
        mode: 'ask'
      },
      attachments: []
    });

    await writeFile(path.resolve(runDir, 'turn_sse.txt'), turnResponse.raw, 'utf8');
    await writeFile(path.resolve(runDir, 'turn_events.json'), JSON.stringify(turnResponse, null, 2), 'utf8');

    snapshots.push(
      await captureTcpSnapshot({
        runDir,
        label: 'post_turn_next',
        processLabel: 'next',
        pid: nextProcess.child.pid
      })
    );

    snapshots.push(
      await captureTcpSnapshot({
        runDir,
        label: 'post_turn_electron',
        processLabel: 'electron',
        pid: electronProcess.child.pid
      })
    );

    for (
      let elapsed = args.idleSampleSeconds;
      elapsed <= args.idleSeconds;
      elapsed += args.idleSampleSeconds
    ) {
      await sleep(args.idleSampleSeconds * 1000);

      snapshots.push(
        await captureTcpSnapshot({
          runDir,
          label: `idle_${elapsed}s_next`,
          processLabel: 'next',
          pid: nextProcess.child.pid
        })
      );

      snapshots.push(
        await captureTcpSnapshot({
          runDir,
          label: `idle_${elapsed}s_electron`,
          processLabel: 'electron',
          pid: electronProcess.child.pid
        })
      );
    }

    timeline.push({ at: toIsoNow(), step: 'idle_window_complete' });

    const uniqueEndpoints = summarizeSnapshotEndpoints(snapshots);

    const nextLog = await readFile(nextLogPath, 'utf8').catch(() => '');
    const electronLog = await readFile(electronLogPath, 'utf8').catch(() => '');

    const blockedDiagnostics = (electronLog.match(/Blocked renderer outbound request by network policy/g) || [])
      .length;

    const probePayloads = extractProbePayloads(electronLog);

    const nonAllowlistedEndpoints = uniqueEndpoints.filter(
      (endpoint) => endpoint.class === 'external_non_allowlisted'
    );

    const anthropicAllowlistedEndpoints = uniqueEndpoints.filter(
      (endpoint) => endpoint.class === 'allowlisted'
    );

    const processExitEvents = turnResponse.events.filter((event) => event.event === 'process:exit');

    const summary = {
      runId,
      generatedAt: toIsoNow(),
      timeline,
      scenario: {
        startup: true,
        workingRootPath,
        sessionRootPath,
        sessionCreate: createResponse.ok,
        sessionBoot: bootResponse.ok,
        turnRequestStatus: turnResponse.status,
        processExitEvents,
        idleSeconds: args.idleSeconds,
        shutdown: true
      },
      diagnostics: {
        blockedRendererDiagnosticsCount: blockedDiagnostics,
        networkProbePayloadCount: probePayloads.length,
        networkProbePayloads: probePayloads
      },
      endpointSummary: {
        totalUniqueEndpoints: uniqueEndpoints.length,
        allowlistedAnthropicEndpoints: anthropicAllowlistedEndpoints,
        nonAllowlistedEndpoints,
        uniqueEndpoints
      },
      verdict: {
        noNonAllowlistedOutboundTcp: nonAllowlistedEndpoints.length === 0,
        blockedRendererDiagnosticsObserved: blockedDiagnostics > 0,
        networkProbePayloadObserved: probePayloads.length > 0,
        scenarioCompleted:
          createResponse.ok &&
          bootResponse.ok &&
          turnResponse.ok &&
          processExitEvents.length > 0
      },
      artifacts: {
        nextLogPath,
        electronLogPath,
        tcpSnapshotsPath: path.resolve(runDir, 'tcp_snapshots.ndjson'),
        sessionCreatePath: path.resolve(runDir, 'session_create.json'),
        sessionBootPath: path.resolve(runDir, 'session_boot.json'),
        turnEventsPath: path.resolve(runDir, 'turn_events.json')
      },
      notes: {
        unresolvedConf002:
          'CONF-002 (OCSP/CRL infrastructure carve-out) remains unresolved; TCP-level summary flags only explicit non-allowlisted external endpoints.'
      }
    };

    await writeFile(path.resolve(runDir, 'summary.json'), JSON.stringify(summary, null, 2), 'utf8');

    return summary;
  } finally {
    if (electronProcess?.child) {
      await stopProcess(electronProcess.child, `${runId}:electron`);
      electronProcess.stream.end();
    }

    await stopProcess(nextProcess.child, `${runId}:next`);
    nextProcess.stream.end();
    await rm(workingRootPath, { recursive: true, force: true });
    await rm(sessionRootPath, { recursive: true, force: true });
  }
}

function aggregateRunVerdicts(runs) {
  const failedRuns = runs.filter((run) => {
    const verdict = run.verdict;
    return !(
      verdict.noNonAllowlistedOutboundTcp &&
      verdict.blockedRendererDiagnosticsObserved &&
      verdict.networkProbePayloadObserved &&
      verdict.scenarioCompleted
    );
  });

  return {
    runCount: runs.length,
    failedRunCount: failedRuns.length,
    passed: failedRuns.length === 0,
    failedRuns: failedRuns.map((run) => run.runId)
  };
}

function renderMarkdownSummary(args, outputDir, runSummaries, aggregate) {
  const lines = [];

  lines.push('# OI-002 Option B Proof Run Summary');
  lines.push('');
  lines.push(`- Generated: ${toIsoNow()}`);
  lines.push(`- Output directory: ${outputDir}`);
  lines.push(`- Run count: ${args.runs}`);
  lines.push(`- Idle window per run: ${args.idleSeconds} seconds`);
  lines.push('');
  lines.push('## Aggregate Verdict');
  lines.push('');
  lines.push(`- Overall: ${aggregate.passed ? 'PASS' : 'FAIL'}`);
  lines.push(`- Failed runs: ${aggregate.failedRunCount}`);
  lines.push('');
  lines.push('## Per-Run Results');
  lines.push('');
  lines.push('| Run | Scenario Completed | Blocked Diagnostics | Probe Payloads | Non-Allowlisted Endpoints | Verdict |');
  lines.push('|---|---|---|---|---|---|');

  for (const run of runSummaries) {
    const verdict =
      run.verdict.noNonAllowlistedOutboundTcp &&
      run.verdict.blockedRendererDiagnosticsObserved &&
      run.verdict.networkProbePayloadObserved &&
      run.verdict.scenarioCompleted
        ? 'PASS'
        : 'FAIL';

    lines.push(
      `| ${run.runId} | ${run.verdict.scenarioCompleted ? 'yes' : 'no'} | ${run.diagnostics.blockedRendererDiagnosticsCount} | ${run.diagnostics.networkProbePayloadCount} | ${run.endpointSummary.nonAllowlistedEndpoints.length} | ${verdict} |`
    );
  }

  lines.push('');
  lines.push('## Notes');
  lines.push('');
  lines.push(
    '- CONF-002 (OCSP/CRL carve-out wording) remains unresolved; this summary reports explicit non-allowlisted TCP endpoints and renderer policy diagnostics only.'
  );

  return `${lines.join('\n')}\n`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  await mkdir(args.outputDir, { recursive: true });

  const buildResult = await runCommand('npm', ['run', 'build:electron'], {
    cwd: FRONTEND_ROOT,
    env: {
      ...process.env,
      NEXT_TELEMETRY_DISABLED: '1'
    }
  });

  await writeFile(
    path.resolve(args.outputDir, 'build_electron.log'),
    `${buildResult.stdout}${buildResult.stderr}`,
    'utf8'
  );

  if (buildResult.code !== 0) {
    throw new Error('Failed to build Electron main process before proof runs');
  }

  const runSummaries = [];

  for (let index = 1; index <= args.runs; index += 1) {
    // Keep each run independent by restarting runtime processes per cycle.
    // This matches the proof standard requirement for independent runs.
    console.log(`[proof] starting run ${index}/${args.runs}`);
    const summary = await runProofCycle({ runIndex: index, args, outputDir: args.outputDir });
    runSummaries.push(summary);
    console.log(`[proof] completed run ${index}/${args.runs}`);
  }

  const aggregate = aggregateRunVerdicts(runSummaries);

  await writeFile(
    path.resolve(args.outputDir, 'summary.json'),
    JSON.stringify(
      {
        generatedAt: toIsoNow(),
        args,
        aggregate,
        runs: runSummaries
      },
      null,
      2
    ),
    'utf8'
  );

  await writeFile(
    path.resolve(args.outputDir, 'SUMMARY.md'),
    renderMarkdownSummary(args, args.outputDir, runSummaries, aggregate),
    'utf8'
  );

  console.log(`[proof] output: ${args.outputDir}`);
  console.log(`[proof] verdict: ${aggregate.passed ? 'PASS' : 'FAIL'}`);

  if (!aggregate.passed) {
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error('[proof] fatal:', error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
