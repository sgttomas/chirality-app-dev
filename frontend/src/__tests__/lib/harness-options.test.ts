import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { resolveRuntimeOptions } from '../../lib/harness/options';
import type { SessionRecord } from '../../lib/harness/types';

let tmpDir = '';

async function createInstructionRootFixture(options?: {
  agentsIndexContent?: string;
  personaName?: string;
  personaContent?: string;
}): Promise<string> {
  tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-harness-options-'));
  const instructionRoot = path.join(tmpDir, 'instruction-root');
  const agentsDir = path.join(instructionRoot, 'agents');
  const docsDir = path.join(instructionRoot, 'docs');

  await mkdir(agentsDir, { recursive: true });
  await mkdir(docsDir, { recursive: true });

  await writeFile(path.join(instructionRoot, 'README.md'), '# instruction root\n', 'utf8');
  await writeFile(path.join(instructionRoot, 'AGENTS.md'), options?.agentsIndexContent ?? '# index\n', 'utf8');
  await writeFile(path.join(docsDir, 'DIRECTIVE.md'), '# directive\n', 'utf8');
  await writeFile(path.join(docsDir, 'CONTRACT.md'), '# contract\n', 'utf8');
  await writeFile(path.join(docsDir, 'SPEC.md'), '# spec\n', 'utf8');
  await writeFile(path.join(docsDir, 'TYPES.md'), '# types\n', 'utf8');
  await writeFile(path.join(docsDir, 'PLAN.md'), '# plan\n', 'utf8');

  if (options?.personaContent) {
    const personaName = options.personaName ?? 'WORKING_ITEMS';
    await writeFile(path.join(agentsDir, `AGENT_${personaName}.md`), options.personaContent, 'utf8');
  }

  return instructionRoot;
}

function makeSession(overrides?: Partial<SessionRecord>): SessionRecord {
  return {
    sessionId: 'sess_test',
    projectRoot: '/tmp/project',
    persona: 'WORKING_ITEMS',
    mode: 'direct',
    createdAt: '2026-02-23T00:00:00.000Z',
    updatedAt: '2026-02-23T00:00:00.000Z',
    ...overrides
  };
}

afterEach(async () => {
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  delete process.env.CHIRALITY_GLOBAL_MODEL;

  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('resolveRuntimeOptions', () => {
  it('applies persona defaults for tools and maxTurns', async () => {
    const instructionRoot = await createInstructionRootFixture({
      personaContent: `---
description: persona fixture
tools:
  - bash
  - read
max_turns: 5
---
# persona
`
    });
    process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;

    const resolved = await resolveRuntimeOptions(makeSession(), {});

    expect(resolved).toMatchObject({
      model: 'claude-sonnet-4-20250514',
      tools: ['bash', 'read'],
      maxTurns: 5,
      persona: 'WORKING_ITEMS',
      mode: 'direct'
    });
  });

  it('resolves model from instruction-root global setting when configured', async () => {
    const instructionRoot = await createInstructionRootFixture({
      agentsIndexContent: `---
model: claude-global
---
# AGENTS
`,
      personaContent: `---
description: persona fixture
model: claude-persona
---
# persona
`
    });
    process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;

    const resolved = await resolveRuntimeOptions(makeSession(), {});
    expect(resolved.model).toBe('claude-global');
  });

  it('lets opts override persona/global defaults', async () => {
    const instructionRoot = await createInstructionRootFixture({
      agentsIndexContent: `---
model: claude-global
---
# AGENTS
`,
      personaContent: `---
description: persona fixture
tools: [read]
max_turns: 4
---
# persona
`
    });
    process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;

    const resolved = await resolveRuntimeOptions(makeSession(), {
      model: 'claude-override',
      tools: ['write'],
      maxTurns: 9,
      mode: 'dontAsk'
    });

    expect(resolved).toMatchObject({
      model: 'claude-override',
      tools: ['write'],
      maxTurns: 9,
      persona: 'WORKING_ITEMS',
      mode: 'dontAsk'
    });
  });

  it('supports CHIRALITY_GLOBAL_MODEL environment override', async () => {
    const instructionRoot = await createInstructionRootFixture({
      agentsIndexContent: '# AGENTS\n',
      personaContent: '# persona\n'
    });
    process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;
    process.env.CHIRALITY_GLOBAL_MODEL = 'claude-env-global';

    const resolved = await resolveRuntimeOptions(makeSession(), {});
    expect(resolved.model).toBe('claude-env-global');
  });

  it('keeps explicitly provided empty tools array without falling back', async () => {
    const instructionRoot = await createInstructionRootFixture({
      personaContent: `---
description: persona fixture
tools:
  - read
---
# persona
`
    });
    process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;

    const resolved = await resolveRuntimeOptions(makeSession(), {
      tools: []
    });

    expect(resolved.tools).toEqual([]);
  });

  it('falls back to runtime defaults when persona frontmatter is malformed', async () => {
    const instructionRoot = await createInstructionRootFixture({
      personaContent: `---
description: malformed persona
tools:
  - read
max_turns: 7
# missing closing frontmatter delimiter`
    });
    process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;

    const resolved = await resolveRuntimeOptions(makeSession(), {});
    expect(resolved.tools).toEqual(['read', 'write', 'bash']);
    expect(resolved.maxTurns).toBe(12);
  });

  it('throws PERSONA_NOT_FOUND when persona instruction file is missing', async () => {
    const instructionRoot = await createInstructionRootFixture({
      personaContent: '# another persona\n',
      personaName: 'TASK'
    });
    process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;

    await expect(resolveRuntimeOptions(makeSession(), {})).rejects.toMatchObject({
      type: 'PERSONA_NOT_FOUND'
    });
  });
});
