import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { assertInstructionRootReadable } from './instruction-root';
import { HarnessError } from './errors';
import { HarnessOpts, ResolvedOpts, SessionRecord } from './types';

const DEFAULT_MODEL = 'claude-sonnet-4-20250514';
const DEFAULT_TOOLS = ['read', 'write', 'bash'];
const DEFAULT_MAX_TURNS = 12;
const GLOBAL_MODEL_ENV_VAR = 'CHIRALITY_GLOBAL_MODEL';

type ParsedFrontmatter = Record<string, unknown>;

type PersonaDefaults = {
  tools?: string[];
  maxTurns?: number;
};

function parseYamlScalar(raw: string): unknown {
  const value = raw.trim();
  if (!value) {
    return '';
  }
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }
  if (value === 'true') {
    return true;
  }
  if (value === 'false') {
    return false;
  }
  if (/^-?\d+$/.test(value)) {
    const parsed = Number.parseInt(value, 10);
    if (Number.isSafeInteger(parsed)) {
      return parsed;
    }
  }
  return value;
}

function parseYamlInlineList(raw: string): string[] {
  const inner = raw.slice(1, -1).trim();
  if (!inner) {
    return [];
  }
  return inner
    .split(',')
    .map((item) => {
      const parsed = parseYamlScalar(item);
      return typeof parsed === 'string' ? parsed.trim() : '';
    })
    .filter((item) => item.length > 0);
}

function parseFrontmatter(markdown: string): ParsedFrontmatter {
  const normalized = markdown.replace(/\r\n/g, '\n');
  if (!normalized.startsWith('---\n')) {
    return {};
  }

  const closingIndex = normalized.indexOf('\n---\n', 4);
  if (closingIndex === -1) {
    return {};
  }

  const block = normalized.slice(4, closingIndex);
  const result: ParsedFrontmatter = {};
  let activeListKey: string | undefined;

  for (const rawLine of block.split('\n')) {
    const trimmed = rawLine.trim();
    if (!trimmed || trimmed.startsWith('#')) {
      continue;
    }

    const keyMatch = trimmed.match(/^([a-zA-Z0-9_]+):(.*)$/);
    if (keyMatch) {
      const key = keyMatch[1];
      const trailing = keyMatch[2].trim();
      if (!trailing) {
        result[key] = [];
        activeListKey = key;
      } else if (trailing.startsWith('[') && trailing.endsWith(']')) {
        result[key] = parseYamlInlineList(trailing);
        activeListKey = undefined;
      } else {
        result[key] = parseYamlScalar(trailing);
        activeListKey = undefined;
      }
      continue;
    }

    if (activeListKey && trimmed.startsWith('-')) {
      const list = Array.isArray(result[activeListKey]) ? result[activeListKey] : [];
      const nextValue = parseYamlScalar(trimmed.slice(1).trim());
      if (typeof nextValue === 'string' && nextValue.trim().length > 0) {
        (list as unknown[]).push(nextValue.trim());
      }
      result[activeListKey] = list;
      continue;
    }

    activeListKey = undefined;
  }

  return result;
}

function asNonEmptyString(value: unknown): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

function asStringArray(value: unknown): string[] | undefined {
  if (!Array.isArray(value)) {
    return undefined;
  }

  const normalized: string[] = [];
  for (const item of value) {
    if (typeof item !== 'string') {
      return undefined;
    }
    const trimmed = item.trim();
    if (trimmed.length > 0) {
      normalized.push(trimmed);
    }
  }

  return normalized;
}

function asPositiveInteger(value: unknown): number | undefined {
  if (typeof value !== 'number' || !Number.isInteger(value) || value <= 0) {
    return undefined;
  }
  return value;
}

function getPersonaCandidates(persona: string, instructionRoot: string): string[] {
  const normalizedPersona = persona.trim().replace(/-/g, '_');
  return [path.join(instructionRoot, 'agents', `AGENT_${normalizedPersona}.md`)];
}

async function readPersonaFrontmatter(persona: string): Promise<ParsedFrontmatter> {
  const instructionRoot = await assertInstructionRootReadable();

  for (const candidate of getPersonaCandidates(persona, instructionRoot)) {
    try {
      const content = await readFile(candidate, 'utf8');
      return parseFrontmatter(content);
    } catch {
      // Continue to next candidate.
    }
  }

  throw new HarnessError('PERSONA_NOT_FOUND', 404, `Persona '${persona}' was not found`, {
    persona,
    instructionRoot
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

export async function resolveRuntimeOptions(
  session: SessionRecord,
  opts?: HarnessOpts
): Promise<ResolvedOpts> {
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
