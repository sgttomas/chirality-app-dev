'use client';

import { FormEvent, useState } from 'react';

type ChatMessage = {
  id: string;
  role: 'operator' | 'assistant';
  text: string;
};

export function ChatPanel(): JSX.Element {
  const [draft, setDraft] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'seed-1',
      role: 'assistant',
      text: 'WORKBENCH chat shell is ready. Session transport wiring is layered in DEL-03-01/03-02.'
    }
  ]);

  function submitDraft(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    const text = draft.trim();
    if (!text) {
      return;
    }

    setMessages((existing) => [
      ...existing,
      {
        id: `operator-${existing.length + 1}`,
        role: 'operator',
        text
      },
      {
        id: `assistant-${existing.length + 2}`,
        role: 'assistant',
        text: 'Message captured in shell baseline. Live turn execution wiring is downstream scope.'
      }
    ]);
    setDraft('');
  }

  return (
    <aside className="panel panel--chat">
      <header className="panel-header">
        <h2>Chat Panel</h2>
      </header>

      <div className="panel-body chat-transcript">
        {messages.map((message) => (
          <article key={message.id} className={`chat-bubble chat-bubble--${message.role}`}>
            <p>{message.text}</p>
          </article>
        ))}
      </div>

      <form className="chat-input-row" onSubmit={submitDraft}>
        <input
          aria-label="Chat input"
          value={draft}
          onChange={(event) => {
            setDraft(event.target.value);
          }}
          placeholder="Type a WORKBENCH prompt..."
        />
        <button type="submit">Send</button>
      </form>
    </aside>
  );
}
