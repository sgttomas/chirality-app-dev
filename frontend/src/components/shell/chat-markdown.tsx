'use client';

import React from 'react';
import ReactMarkdown, { type Components } from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { hasAnsiEscapeCodes, renderAnsiToHtml } from '../../lib/shell/ansi';

function extractLanguage(className: string | undefined): string {
  if (!className) {
    return '';
  }

  if (!className.startsWith('language-')) {
    return '';
  }

  return className.replace('language-', '').trim().toLowerCase();
}

function trimTrailingFenceNewline(value: string): string {
  return value.endsWith('\n') ? value.slice(0, -1) : value;
}

const MARKDOWN_COMPONENTS: Components = {
  a: ({ href, children }) => (
    <a href={href} target="_blank" rel="noreferrer noopener">
      {children}
    </a>
  ),
  code: (props) => {
    const inline = 'inline' in props ? Boolean((props as { inline?: boolean }).inline) : false;
    const className = 'className' in props ? (props.className as string | undefined) : undefined;
    const rawText = trimTrailingFenceNewline(String(props.children ?? ''));
    const language = extractLanguage(className);
    const shouldUseAnsiFallback = language === 'ansi' || hasAnsiEscapeCodes(rawText);

    if (inline) {
      return <code className={className}>{rawText}</code>;
    }

    if (shouldUseAnsiFallback) {
      return (
        <pre className="chat-code-block chat-code-block--ansi">
          <code
            className="chat-ansi"
            dangerouslySetInnerHTML={{
              __html: renderAnsiToHtml(rawText)
            }}
          />
        </pre>
      );
    }

    return (
      <pre className="chat-code-block">
        <code className={className}>{rawText}</code>
      </pre>
    );
  }
};

type ChatMarkdownProps = {
  source: string;
};

export function ChatMarkdown({ source }: ChatMarkdownProps): JSX.Element {
  return (
    <div className="chat-markdown">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={MARKDOWN_COMPONENTS}>
        {source}
      </ReactMarkdown>
    </div>
  );
}
