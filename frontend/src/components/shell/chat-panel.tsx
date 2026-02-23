'use client';

import { usePathname, useSearchParams } from 'next/navigation';
import { FormEvent, useEffect, useMemo, useState } from 'react';
import {
  bootHarnessSession,
  createHarnessSession,
  interruptHarnessSession,
  streamHarnessTurn
} from '../../lib/harness/client';
import { toHarnessUiError, type HarnessUiError } from '../../lib/harness/error-display';
import { useWorkspace } from '../workspace/workspace-provider';

type ChatMessage = {
  id: string;
  role: 'operator' | 'assistant';
  text: string;
};

type ActiveSession = {
  sessionId: string;
  projectRoot: string;
  persona: string;
  mode: string;
};

const PERSONA_ALIASES: Record<string, string> = {
  HELP: 'HELP_HUMAN',
  ORCHESTRATE: 'ORCHESTRATOR',
  AGGREGATE: 'AGGREGATION',
  RECONCILING: 'RECONCILIATION',
  AGENTS: 'HELPS_HUMANS'
};

function readTextField(data: unknown): string | undefined {
  if (!data || typeof data !== 'object') {
    return undefined;
  }

  const text = (data as Record<string, unknown>).text;
  return typeof text === 'string' ? text : undefined;
}

function resolvePersona(pathname: string, rawAgent: string | null): string {
  if (pathname.startsWith('/workbench')) {
    const candidate = rawAgent?.trim();
    if (!candidate) {
      return 'WORKING_ITEMS';
    }

    const normalized = candidate.toUpperCase();
    return PERSONA_ALIASES[normalized] ?? normalized;
  }

  return 'WORKING_ITEMS';
}

function resolveMode(pathname: string): string {
  if (pathname.startsWith('/workbench')) {
    return 'WORKBENCH';
  }

  if (pathname.startsWith('/pipeline')) {
    return 'PIPELINE';
  }

  return 'PORTAL';
}

export function ChatPanel(): JSX.Element {
  const { projectRoot } = useWorkspace();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [draft, setDraft] = useState('');
  const [activeSession, setActiveSession] = useState<ActiveSession | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [runtimeStatus, setRuntimeStatus] = useState<string | null>(null);
  const [runtimeError, setRuntimeError] = useState<HarnessUiError | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'seed-1',
      role: 'assistant',
      text: 'Harness chat wiring is active. Select a Working Root and send a prompt.'
    }
  ]);

  const activePersona = useMemo(
    () => resolvePersona(pathname, searchParams.get('agent')),
    [pathname, searchParams]
  );
  const activeMode = useMemo(() => resolveMode(pathname), [pathname]);

  useEffect(() => {
    setActiveSession((existing) => {
      if (
        existing &&
        existing.projectRoot === projectRoot &&
        existing.persona === activePersona &&
        existing.mode === activeMode
      ) {
        return existing;
      }
      return null;
    });
  }, [projectRoot, activePersona, activeMode]);

  async function ensureSessionBooted(): Promise<ActiveSession> {
    if (!projectRoot) {
      throw new Error('Select a Working Root before sending a prompt.');
    }

    if (
      activeSession &&
      activeSession.projectRoot === projectRoot &&
      activeSession.persona === activePersona &&
      activeSession.mode === activeMode
    ) {
      return activeSession;
    }

    setRuntimeStatus('Creating session...');
    const session = await createHarnessSession({
      projectRoot,
      persona: activePersona,
      mode: activeMode
    });

    setRuntimeStatus('Booting session...');
    const boot = await bootHarnessSession({
      sessionId: session.sessionId
    });

    const nextSession: ActiveSession = {
      sessionId: boot.session.sessionId,
      projectRoot,
      persona: activePersona,
      mode: activeMode
    };
    setActiveSession(nextSession);
    return nextSession;
  }

  async function interruptTurn(): Promise<void> {
    if (!activeSession || !isRunning) {
      return;
    }

    try {
      setRuntimeStatus('Interrupt requested...');
      setRuntimeError(null);
      await interruptHarnessSession({ sessionId: activeSession.sessionId });
    } catch (error) {
      setRuntimeError(toHarnessUiError(error));
      setRuntimeStatus(null);
    }
  }

  async function submitDraft(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    const text = draft.trim();
    if (!text) {
      return;
    }

    setRuntimeError(null);
    setRuntimeStatus('Preparing turn...');
    setDraft('');
    setIsRunning(true);

    const operatorMessage: ChatMessage = {
      id: `operator-${Date.now()}`,
      role: 'operator',
      text
    };
    const assistantId = `assistant-${Date.now() + 1}`;
    const assistantMessage: ChatMessage = {
      id: assistantId,
      role: 'assistant',
      text: ''
    };

    setMessages((existing) => [
      ...existing,
      operatorMessage,
      assistantMessage
    ]);

    try {
      const session = await ensureSessionBooted();

      let assistantText = '';
      let processExitError: string | null = null;

      setRuntimeStatus('Running turn...');

      await streamHarnessTurn(
        {
          sessionId: session.sessionId,
          message: text
        },
        (streamEvent) => {
          if (streamEvent.event === 'chat:delta') {
            const chunk = readTextField(streamEvent.data);
            if (chunk) {
              assistantText += chunk;
              setMessages((existing) =>
                existing.map((item) =>
                  item.id === assistantId
                    ? {
                        ...item,
                        text: assistantText
                      }
                    : item
                )
              );
            }
            return;
          }

          if (streamEvent.event === 'chat:complete') {
            const completed = readTextField(streamEvent.data);
            if (completed) {
              assistantText = completed;
              setMessages((existing) =>
                existing.map((item) =>
                  item.id === assistantId
                    ? {
                        ...item,
                        text: assistantText
                      }
                    : item
                )
              );
            }
            return;
          }

          if (
            streamEvent.event === 'process:exit' &&
            streamEvent.data &&
            typeof streamEvent.data === 'object'
          ) {
            const payload = streamEvent.data as Record<string, unknown>;
            const exitCode = typeof payload.exitCode === 'number' ? payload.exitCode : 0;
            const interrupted = payload.interrupted === true;

            if (interrupted && !assistantText) {
              assistantText = 'Turn interrupted by operator.';
              setMessages((existing) =>
                existing.map((item) =>
                  item.id === assistantId
                    ? {
                        ...item,
                        text: assistantText
                      }
                    : item
                )
              );
            }

            if (exitCode !== 0) {
              processExitError =
                typeof payload.error === 'string'
                  ? payload.error
                  : `Turn failed with exit code ${exitCode}.`;
            }
          }
        }
      );

      if (processExitError) {
        throw new Error(processExitError);
      }

      if (!assistantText.trim()) {
        setMessages((existing) =>
          existing.map((item) =>
            item.id === assistantId
              ? {
                  ...item,
                  text: 'No assistant text was returned for this turn.'
                }
              : item
          )
        );
      }

      setRuntimeStatus(null);
    } catch (error) {
      const uiError = toHarnessUiError(error);
      setRuntimeError(uiError);
      setRuntimeStatus(null);
      setMessages((existing) =>
        existing.map((item) =>
          item.id === assistantId
            ? {
                ...item,
                text: `${uiError.title}: ${uiError.message}`
              }
            : item
        )
      );
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <aside className="panel panel--chat">
      <header className="panel-header">
        <h2>Chat Panel</h2>
        <p className="chat-meta">
          Persona: {activePersona} | Mode: {activeMode}
        </p>
      </header>

      <div className="panel-body chat-transcript">
        {!projectRoot ? (
          <p className="panel-empty">Select a Working Root before starting a harness turn.</p>
        ) : null}
        {messages.map((message) => (
          <article key={message.id} className={`chat-bubble chat-bubble--${message.role}`}>
            <p>{message.text}</p>
          </article>
        ))}
      </div>

      {runtimeStatus ? <p className="chat-runtime-status">{runtimeStatus}</p> : null}

      {runtimeError ? (
        <div className="chat-runtime-error">
          <p className="chat-runtime-error-title">
            {runtimeError.title}
            {runtimeError.code ? ` (${runtimeError.code})` : ''}
          </p>
          <p>{runtimeError.message}</p>
          <p>{runtimeError.nextStep}</p>
        </div>
      ) : null}

      <form
        className="chat-input-row"
        onSubmit={(event) => {
          void submitDraft(event);
        }}
      >
        <input
          aria-label="Chat input"
          value={draft}
          disabled={!projectRoot || isRunning}
          onChange={(event) => {
            setDraft(event.target.value);
            if (runtimeError) {
              setRuntimeError(null);
            }
          }}
          placeholder={
            projectRoot ? `Send prompt as ${activePersona}...` : 'Select a Working Root first...'
          }
        />
        <button type="submit" disabled={!projectRoot || isRunning || !draft.trim()}>
          {isRunning ? 'Running...' : 'Send'}
        </button>
        <button
          type="button"
          className="button-muted"
          onClick={() => {
            void interruptTurn();
          }}
          disabled={!isRunning || !activeSession}
        >
          Interrupt
        </button>
      </form>
    </aside>
  );
}
