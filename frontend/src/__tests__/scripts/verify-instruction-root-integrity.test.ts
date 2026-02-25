import { execFile } from 'node:child_process';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { promisify } from 'node:util';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

const execFileAsync = promisify(execFile);
const SCRIPT_PATH = path.resolve(process.cwd(), 'scripts', 'verify-instruction-root-integrity.mjs');

const BASE_FIXTURE_FILES: Record<string, string> = {
  'AGENTS.md': '# agents index\n',
  'README.md': '# readme\n',
  'WHAT-IS-AN-AGENT.md': '# what is an agent\n',
  'PROFESSIONAL_ENGINEERING.md': '# professional engineering\n',
  'docs/DIRECTIVE.md': '# directive\n',
  'docs/CONTRACT.md': '# contract\n',
  'docs/SPEC.md': '# spec\n',
  'docs/TYPES.md': '# types\n',
  'docs/PLAN.md': '# plan\n',
  'agents/AGENT_WORKING_ITEMS.md': '# working items persona\n',
  'agents/AGENT_TASK.md': '# task persona\n'
};

type ScriptResult = {
  code: number;
  stdout: string;
  stderr: string;
};

let tmpRoot = '';

async function writeFixture(root: string, overrides?: Record<string, string>): Promise<void> {
  const files = {
    ...BASE_FIXTURE_FILES,
    ...(overrides ?? {})
  };

  for (const [relativePath, content] of Object.entries(files)) {
    const absolutePath = path.join(root, relativePath);
    await mkdir(path.dirname(absolutePath), { recursive: true });
    await writeFile(absolutePath, content, 'utf8');
  }
}

async function runIntegrityScript(args: string[]): Promise<ScriptResult> {
  try {
    const result = await execFileAsync('node', [SCRIPT_PATH, ...args], {
      cwd: process.cwd()
    });
    return {
      code: 0,
      stdout: result.stdout,
      stderr: result.stderr
    };
  } catch (error) {
    const failure = error as {
      code?: number;
      stdout?: string;
      stderr?: string;
    };
    return {
      code: typeof failure.code === 'number' ? failure.code : 1,
      stdout: failure.stdout ?? '',
      stderr: failure.stderr ?? ''
    };
  }
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-integrity-script-'));
});

afterEach(async () => {
  if (tmpRoot) {
    await rm(tmpRoot, { recursive: true, force: true });
  }
  tmpRoot = '';
});

describe('verify-instruction-root-integrity script', () => {
  it('passes when bundled files match source hashes', async () => {
    const sourceRoot = path.join(tmpRoot, 'source-root');
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');

    await writeFixture(sourceRoot);
    await writeFixture(bundleRoot);

    const result = await runIntegrityScript([
      '--source-root',
      sourceRoot,
      '--bundle-root',
      bundleRoot,
      '--output-root',
      outputRoot
    ]);

    expect(result.code).toBe(0);
    expect(result.stdout).toContain('instruction-root integrity status: pass');

    const summaryRaw = await readFile(path.join(outputRoot, 'summary.json'), 'utf8');
    const summary = JSON.parse(summaryRaw) as {
      status: string;
      checkedFileCount: number;
      missingInBundle: string[];
      mismatchedFiles: Array<{ path: string }>;
      unexpectedBundleAgentFiles: string[];
    };

    expect(summary.status).toBe('pass');
    expect(summary.checkedFileCount).toBe(11);
    expect(summary.missingInBundle).toHaveLength(0);
    expect(summary.mismatchedFiles).toHaveLength(0);
    expect(summary.unexpectedBundleAgentFiles).toHaveLength(0);
  });

  it('fails when bundled content diverges from source', async () => {
    const sourceRoot = path.join(tmpRoot, 'source-root');
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');

    await writeFixture(sourceRoot);
    await writeFixture(bundleRoot, {
      'agents/AGENT_TASK.md': '# task persona (modified)\n'
    });

    const result = await runIntegrityScript([
      '--source-root',
      sourceRoot,
      '--bundle-root',
      bundleRoot,
      '--output-root',
      outputRoot
    ]);

    expect(result.code).toBe(1);
    expect(result.stdout).toContain('instruction-root integrity status: fail');

    const summaryRaw = await readFile(path.join(outputRoot, 'summary.json'), 'utf8');
    const summary = JSON.parse(summaryRaw) as {
      status: string;
      mismatchedFiles: Array<{ path: string }>;
    };

    expect(summary.status).toBe('fail');
    expect(summary.mismatchedFiles).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          path: 'agents/AGENT_TASK.md'
        })
      ])
    );
  });
});
