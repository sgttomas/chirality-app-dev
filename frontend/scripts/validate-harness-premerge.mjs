#!/usr/bin/env node

import { access, copyFile, mkdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { constants as fsConstants } from 'node:fs';

const REQUIRED_TEST_IDS = [
  'setup.server_reachable',
  'regression.session_crud',
  'section8.smoke_stream',
  'section8.session_persistence_resume',
  'section8.permissions_dontask',
  'section8.interrupt_sigint',
  'section8.sdk_native_stream'
];

const LEGACY_REMOVED_TEST_ID = 'regression.api_chat_reachability';

function parseMachineLine(stdout, key) {
  const match = stdout
    .split('\n')
    .map((line) => line.trim())
    .find((line) => line.startsWith(`${key}=`));

  if (!match) {
    throw new Error(`Missing machine-readable output '${key}'`);
  }

  return match.slice(`${key}=`.length);
}

async function ensureReadableFile(filePath) {
  await access(filePath, fsConstants.R_OK);
}

async function runSection8Script(scriptPath) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [scriptPath], {
      cwd: process.cwd(),
      env: process.env,
      stdio: ['ignore', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (chunk) => {
      const text = chunk.toString();
      stdout += text;
      process.stdout.write(text);
    });

    child.stderr.on('data', (chunk) => {
      const text = chunk.toString();
      stderr += text;
      process.stderr.write(text);
    });

    child.on('error', reject);
    child.on('close', (code) => {
      resolve({
        code: code ?? 1,
        stdout,
        stderr
      });
    });
  });
}

async function main() {
  const scriptPath = path.resolve(process.cwd(), 'scripts', 'validate-harness-section8.mjs');
  const stableArtifactPath = path.resolve(
    process.cwd(),
    'artifacts',
    'harness',
    'section8',
    'latest',
    'summary.json'
  );

  try {
    await ensureReadableFile(scriptPath);
  } catch {
    console.error('RUNTIME_SURFACE_MISSING: frontend/scripts/validate-harness-section8.mjs');
    console.log(`HARNESS_PREMERGE_ARTIFACT_PATH=${stableArtifactPath}`);
    console.log('HARNESS_PREMERGE_SOURCE_SUMMARY_PATH=');
    console.log('HARNESS_PREMERGE_STATUS=fail');
    console.log('HARNESS_PREMERGE_TEST_COUNT=0');
    process.exitCode = 1;
    return;
  }

  const section8Result = await runSection8Script(scriptPath);
  if (section8Result.code !== 0) {
    const sourceSummaryPath = (() => {
      try {
        return parseMachineLine(section8Result.stdout, 'HARNESS_VALIDATION_SUMMARY_PATH');
      } catch {
        return '';
      }
    })();
    console.log(`HARNESS_PREMERGE_ARTIFACT_PATH=${stableArtifactPath}`);
    console.log(`HARNESS_PREMERGE_SOURCE_SUMMARY_PATH=${sourceSummaryPath}`);
    console.log('HARNESS_PREMERGE_STATUS=fail');
    console.log('HARNESS_PREMERGE_TEST_COUNT=0');
    process.exitCode = 1;
    return;
  }

  const sourceSummaryPath = parseMachineLine(
    section8Result.stdout,
    'HARNESS_VALIDATION_SUMMARY_PATH'
  );
  const validationStatus = parseMachineLine(section8Result.stdout, 'HARNESS_VALIDATION_STATUS');
  if (validationStatus !== 'pass') {
    throw new Error(`Section8 validation status is '${validationStatus}', expected 'pass'`);
  }

  await ensureReadableFile(sourceSummaryPath);
  const summaryRaw = await readFile(sourceSummaryPath, 'utf8');
  const summary = JSON.parse(summaryRaw);
  const resultRows = Array.isArray(summary.results) ? summary.results : [];
  const seenIds = new Set(resultRows.map((result) => result.id));

  for (const requiredId of REQUIRED_TEST_IDS) {
    if (!seenIds.has(requiredId)) {
      throw new Error(`Summary missing required test id '${requiredId}'`);
    }
  }

  if (seenIds.has(LEGACY_REMOVED_TEST_ID)) {
    throw new Error(`Summary includes legacy test id '${LEGACY_REMOVED_TEST_ID}'`);
  }

  await mkdir(path.dirname(stableArtifactPath), { recursive: true });
  await copyFile(sourceSummaryPath, stableArtifactPath);
  await ensureReadableFile(stableArtifactPath);

  const premergeStatus = resultRows.every((result) => result.status === 'pass') ? 'pass' : 'fail';
  const testCount = resultRows.length;

  console.log(`HARNESS_PREMERGE_ARTIFACT_PATH=${stableArtifactPath}`);
  console.log(`HARNESS_PREMERGE_SOURCE_SUMMARY_PATH=${sourceSummaryPath}`);
  console.log(`HARNESS_PREMERGE_STATUS=${premergeStatus}`);
  console.log(`HARNESS_PREMERGE_TEST_COUNT=${testCount}`);

  process.exitCode = premergeStatus === 'pass' ? 0 : 1;
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`Harness premerge validation failed: ${message}`);
  process.exitCode = 1;
});
