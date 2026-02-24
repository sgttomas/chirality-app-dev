import { constants as fsConstants } from 'node:fs';
import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { HarnessError } from './errors';
import { assertInstructionRootReadable } from './instruction-root';

export type ParsedFrontmatter = Record<string, unknown>;
export type AgentClass = 'PERSONA' | 'TASK';

export type AgentInstruction = {
  instructionRoot: string;
  path: string;
  content: string;
};

type ParseFrontmatterOptions = {
  warnPrefix?: string;
};

function normalizeAgentName(agentName: string): string {
  return agentName.trim().replace(/-/g, '_');
}

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

export function parseFrontmatter(
  markdown: string,
  options?: ParseFrontmatterOptions
): ParsedFrontmatter {
  const normalized = markdown.replace(/\r\n/g, '\n');
  if (!normalized.startsWith('---\n')) {
    return {};
  }

  const closingIndex = normalized.indexOf('\n---\n', 4);
  if (closingIndex === -1) {
    if (options?.warnPrefix) {
      console.warn(
        `${options.warnPrefix} Ignoring malformed persona frontmatter: missing closing delimiter.`
      );
    }
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

export function asNonEmptyString(value: unknown): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

export function asStringArray(value: unknown): string[] | undefined {
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

export function parseCommaSeparatedList(value: unknown): string[] {
  if (Array.isArray(value)) {
    return value
      .filter((item): item is string => typeof item === 'string')
      .map((item) => item.trim())
      .filter((item) => item.length > 0);
  }
  if (typeof value !== 'string') {
    return [];
  }
  return value
    .split(',')
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
}

function extractAgentClass(value: string): AgentClass | undefined {
  const normalized = value.trim().toUpperCase();
  if (normalized.startsWith('TASK')) {
    return 'TASK';
  }
  if (normalized.startsWith('PERSONA')) {
    return 'PERSONA';
  }
  return undefined;
}

export function parseAgentType(content: string): number | undefined {
  const bodyHeaderMatch = content.match(/^\s*AGENT_TYPE:\s*(?:TYPE\s*)?([0-2])\b/m);
  if (bodyHeaderMatch?.[1]) {
    return Number.parseInt(bodyHeaderMatch[1], 10);
  }

  const tableMatch = content.match(/^\|\s*\*\*AGENT_TYPE\*\*\s*\|\s*TYPE\s*([0-2])\s*\|/im);
  if (tableMatch?.[1]) {
    return Number.parseInt(tableMatch[1], 10);
  }

  return undefined;
}

export function parseAgentClass(content: string): AgentClass | undefined {
  const bodyHeaderMatch = content.match(/^\s*AGENT_CLASS:\s*([^\n]+)/im);
  if (bodyHeaderMatch?.[1]) {
    return extractAgentClass(bodyHeaderMatch[1]);
  }

  const tableMatch = content.match(/^\|\s*\*\*AGENT_CLASS\*\*\s*\|\s*([^|]+)\|/im);
  if (tableMatch?.[1]) {
    return extractAgentClass(tableMatch[1]);
  }

  return undefined;
}

function getAgentInstructionPath(agentName: string, instructionRoot: string): string {
  return path.join(instructionRoot, 'agents', `AGENT_${normalizeAgentName(agentName)}.md`);
}

async function resolveInstructionRoot(
  instructionRootOverride?: string
): Promise<string> {
  if (instructionRootOverride) {
    return path.resolve(instructionRootOverride);
  }
  return assertInstructionRootReadable();
}

export async function readAgentInstruction(
  agentName: string,
  instructionRootOverride?: string
): Promise<AgentInstruction> {
  const instructionRoot = await resolveInstructionRoot(instructionRootOverride);
  const candidate = getAgentInstructionPath(agentName, instructionRoot);

  try {
    await access(candidate, fsConstants.R_OK);
  } catch {
    throw new HarnessError('PERSONA_NOT_FOUND', 404, `Persona '${agentName}' was not found`, {
      persona: agentName,
      instructionRoot
    });
  }

  const content = await readFile(candidate, 'utf8');
  return {
    instructionRoot,
    path: candidate,
    content
  };
}

export async function tryReadAgentInstruction(
  agentName: string,
  instructionRootOverride?: string
): Promise<AgentInstruction | undefined> {
  try {
    return await readAgentInstruction(agentName, instructionRootOverride);
  } catch (error) {
    if (error instanceof HarnessError && error.type === 'PERSONA_NOT_FOUND') {
      return undefined;
    }
    throw error;
  }
}
