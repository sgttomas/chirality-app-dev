import { HarnessOpts, ResolvedOpts, SessionRecord } from './types';

const DEFAULT_MODEL = 'claude-sonnet-4-20250514';
const DEFAULT_TOOLS = ['read', 'write', 'bash'];
const DEFAULT_MAX_TURNS = 12;

export function resolveRuntimeOptions(session: SessionRecord, opts?: HarnessOpts): ResolvedOpts {
  return {
    model: opts?.model ?? session.model ?? DEFAULT_MODEL,
    tools: opts?.tools ?? DEFAULT_TOOLS,
    maxTurns: opts?.maxTurns ?? DEFAULT_MAX_TURNS,
    persona: opts?.persona ?? session.persona,
    mode: opts?.mode ?? session.mode
  };
}
