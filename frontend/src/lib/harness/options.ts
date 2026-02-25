import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { assertInstructionRootReadable } from './instruction-root';
import {
  asNonEmptyString,
  asStringArray,
  parseFrontmatter,
  type ParsedFrontmatter,
  readAgentInstruction
} from './agent-instruction';
import { HarnessOpts, ResolvedOpts, SessionRecord } from './types';

const DEFAULT_MODEL = 'claude-sonnet-4-20250514';
const DEFAULT_TOOLS = ['read', 'write', 'bash'];
const DEFAULT_MAX_TURNS = 12;
const GLOBAL_MODEL_ENV_VAR = 'CHIRALITY_GLOBAL_MODEL';
const SUPPORTED_OPT_KEYS = new Set([
  'model',
  'tools',
  'maxTurns',
  'persona',
  'mode',
  'subagentGovernance'
]);

type PersonaDefaults = {
  tools?: string[];
  maxTurns?: number;
};

function asPositiveInteger(value: unknown): number | undefined {
  if (typeof value !== 'number' || !Number.isInteger(value) || value <= 0) {
    return undefined;
  }
  return value;
}

async function readPersonaFrontmatter(persona: string): Promise<ParsedFrontmatter> {
  const { content } = await readAgentInstruction(persona);
  return parseFrontmatter(content, {
    warnPrefix: '[harness/options]'
  });
}

async function readPersonaDefaults(persona: string): Promise<PersonaDefaults> {
  const frontmatter = await readPersonaFrontmatter(persona);
  return {
    tools: asStringArray(frontmatter.tools),
    maxTurns: asPositiveInteger(frontmatter.max_turns)
  };
}

async function readGlobalModelFromInstructionRoot(): Promise<string | undefined> {
  const fromEnv = asNonEmptyString(process.env[GLOBAL_MODEL_ENV_VAR]);
  if (fromEnv) {
    return fromEnv;
  }

  const instructionRoot = await assertInstructionRootReadable();
  const agentsIndexPath = path.join(instructionRoot, 'AGENTS.md');

  try {
    const content = await readFile(agentsIndexPath, 'utf8');
    const frontmatter = parseFrontmatter(content);
    return asNonEmptyString(frontmatter.model);
  } catch {
    return undefined;
  }
}

function warnOnUnknownOpts(opts: HarnessOpts | undefined): void {
  if (!opts || typeof opts !== 'object') {
    return;
  }

  const unknownKeys = Object.keys(opts as Record<string, unknown>).filter(
    (key) => !SUPPORTED_OPT_KEYS.has(key)
  );
  if (unknownKeys.length === 0) {
    return;
  }

  const sortedUnknownKeys = unknownKeys.sort((left, right) => left.localeCompare(right));
  console.warn(`[harness/options] Ignoring unknown opts field(s): ${sortedUnknownKeys.join(', ')}`);
}

export async function resolveRuntimeOptions(
  session: SessionRecord,
  opts?: HarnessOpts
): Promise<ResolvedOpts> {
  warnOnUnknownOpts(opts);

  const persona = asNonEmptyString(opts?.persona) ?? session.persona;
  const mode = asNonEmptyString(opts?.mode) ?? session.mode;
  const [personaDefaults, globalModel] = await Promise.all([
    readPersonaDefaults(persona),
    readGlobalModelFromInstructionRoot()
  ]);

  return {
    model: asNonEmptyString(opts?.model) ?? globalModel ?? DEFAULT_MODEL,
    tools: asStringArray(opts?.tools) ?? personaDefaults.tools ?? DEFAULT_TOOLS,
    maxTurns: asPositiveInteger(opts?.maxTurns) ?? personaDefaults.maxTurns ?? DEFAULT_MAX_TURNS,
    persona,
    mode,
    subagentGovernance: opts?.subagentGovernance
  };
}
