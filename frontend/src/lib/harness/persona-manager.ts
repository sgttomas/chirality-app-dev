import { createHash } from 'node:crypto';
import { access } from 'node:fs/promises';
import path from 'node:path';
import { constants as fsConstants } from 'node:fs';
import { HarnessError } from './errors';
import { IPersonaManager } from './types';

function getInstructionRoot(): string {
  return process.env.CHIRALITY_INSTRUCTION_ROOT ?? path.resolve(process.cwd(), '..');
}

function getPersonaCandidates(persona: string): string[] {
  const normalizedPersona = persona.trim().replace(/-/g, '_');
  const instructionRoot = getInstructionRoot();
  return [path.join(instructionRoot, 'agents', `AGENT_${normalizedPersona}.md`)];
}

async function ensurePersonaExists(persona: string): Promise<void> {
  for (const candidate of getPersonaCandidates(persona)) {
    try {
      await access(candidate, fsConstants.R_OK);
      return;
    } catch {
      // Continue to the next candidate.
    }
  }

  throw new HarnessError('PERSONA_NOT_FOUND', 404, `Persona '${persona}' was not found`, {
    persona,
    instructionRoot: getInstructionRoot()
  });
}

export class StubPersonaManager implements IPersonaManager {
  async buildSystemPrompt(projectRoot: string, persona: string, mode: string): Promise<string> {
    await ensurePersonaExists(persona);
    return `Persona=${persona}; mode=${mode}; projectRoot=${projectRoot}`;
  }

  getBootFingerprint(persona: string, mode: string): string {
    return createHash('sha256').update(`${persona}::${mode}`).digest('hex').slice(0, 32);
  }
}
