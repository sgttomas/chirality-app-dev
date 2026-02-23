import { createHash } from 'node:crypto';
import { access } from 'node:fs/promises';
import path from 'node:path';
import { constants as fsConstants } from 'node:fs';
import { HarnessError } from './errors';
import { assertInstructionRootReadable } from './instruction-root';
import { IPersonaManager } from './types';

function getPersonaCandidates(persona: string, instructionRoot: string): string[] {
  const normalizedPersona = persona.trim().replace(/-/g, '_');
  return [path.join(instructionRoot, 'agents', `AGENT_${normalizedPersona}.md`)];
}

async function ensurePersonaExists(persona: string): Promise<void> {
  const instructionRoot = await assertInstructionRootReadable();

  for (const candidate of getPersonaCandidates(persona, instructionRoot)) {
    try {
      await access(candidate, fsConstants.R_OK);
      return;
    } catch {
      // Continue to the next candidate.
    }
  }

  throw new HarnessError('PERSONA_NOT_FOUND', 404, `Persona '${persona}' was not found`, {
    persona,
    instructionRoot
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
