import { createHash } from 'node:crypto';
import { IPersonaManager } from './types';

export class StubPersonaManager implements IPersonaManager {
  async buildSystemPrompt(projectRoot: string, persona: string, mode: string): Promise<string> {
    return `Persona=${persona}; mode=${mode}; projectRoot=${projectRoot}`;
  }

  getBootFingerprint(persona: string, mode: string): string {
    return createHash('sha256').update(`${persona}::${mode}`).digest('hex').slice(0, 32);
  }
}
