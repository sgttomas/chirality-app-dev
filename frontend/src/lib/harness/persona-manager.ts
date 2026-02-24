import { createHash } from 'node:crypto';
import { readAgentInstruction } from './agent-instruction';
import { IPersonaManager } from './types';

async function ensurePersonaExists(persona: string): Promise<void> {
  await readAgentInstruction(persona);
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
