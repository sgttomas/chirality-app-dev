import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it } from 'vitest';
import { ChatMarkdown } from '../../components/shell/chat-markdown';

describe('chat markdown rendering', () => {
  it('renders core GFM structures for assistant messages', () => {
    const source = [
      '| Col A | Col B |',
      '| --- | --- |',
      '| 1 | 2 |',
      '',
      '- [x] done',
      '- [ ] todo',
      '',
      '~~deprecated~~',
      '',
      'Visit https://example.com',
      '',
      '```ts',
      'const value = 1;',
      '```'
    ].join('\n');

    const html = renderToStaticMarkup(createElement(ChatMarkdown, { source }));

    expect(html).toContain('<table>');
    expect(html).toContain('type="checkbox"');
    expect(html).toContain('<del>deprecated</del>');
    expect(html).toContain('href="https://example.com"');
    expect(html).toContain('language-ts');
    expect(html).toContain('const value = 1;');
  });

  it('uses ansi fallback rendering for terminal code blocks', () => {
    const source = ['```ansi', '\u001b[31mERR\u001b[0m', '```'].join('\n');
    const html = renderToStaticMarkup(createElement(ChatMarkdown, { source }));

    expect(html).toContain('chat-code-block--ansi');
    expect(html).toContain('ansi-red-fg');
    expect(html).toContain('ERR');
  });
});
