import { randomUUID } from 'node:crypto';
import { HarnessError } from './errors';
import { IAgentSdkManager, ResolvedOpts, SessionRecord, UIEvent } from './types';

type ActiveTurnState = {
  interrupted: boolean;
};

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function chunkText(text: string, size = 24): string[] {
  const chunks: string[] = [];
  for (let index = 0; index < text.length; index += size) {
    chunks.push(text.slice(index, index + size));
  }
  return chunks.length > 0 ? chunks : ['ok'];
}

export class StubAgentSdkManager implements IAgentSdkManager {
  private readonly activeTurns = new Map<string, ActiveTurnState>();

  async interrupt(sessionId: string): Promise<void> {
    const activeTurn = this.activeTurns.get(sessionId);
    if (!activeTurn) {
      throw new HarnessError('SESSION_NOT_FOUND', 404, `No active turn for session '${sessionId}'`, {
        sessionId
      });
    }

    activeTurn.interrupted = true;
  }

  async *startTurn(
    session: SessionRecord,
    message: string,
    opts: ResolvedOpts
  ): AsyncIterable<UIEvent> {
    const turnState: ActiveTurnState = { interrupted: false };
    this.activeTurns.set(session.sessionId, turnState);

    const claudeSessionId = session.claudeSessionId ?? `claude_${randomUUID()}`;
    let fullText = message.trim();
    if (!fullText) {
      fullText = 'Turn executed successfully.';
    }

    try {
      yield {
        type: 'session:init',
        data: {
          claudeSessionId,
          model: opts.model
        }
      };

      const chunks = chunkText(fullText);
      let combined = '';

      for (const chunk of chunks) {
        if (turnState.interrupted) {
          yield {
            type: 'process:exit',
            data: {
              exitCode: 130,
              interrupted: true
            }
          };
          return;
        }

        combined += chunk;
        yield {
          type: 'chat:delta',
          data: {
            text: chunk
          }
        };

        await delay(35);
      }

      if (turnState.interrupted) {
        yield {
          type: 'process:exit',
          data: {
            exitCode: 130,
            interrupted: true
          }
        };
        return;
      }

      yield {
        type: 'chat:complete',
        data: {
          text: combined
        }
      };

      yield {
        type: 'session:complete',
        data: {}
      };

      yield {
        type: 'process:exit',
        data: {
          exitCode: 0
        }
      };
    } finally {
      this.activeTurns.delete(session.sessionId);
    }
  }
}
