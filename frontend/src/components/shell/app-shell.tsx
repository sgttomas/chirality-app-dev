'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useMemo, useState, type ReactNode } from 'react';
import { useWorkspace } from '../workspace/workspace-provider';
import { ChatPanel } from './chat-panel';
import { FileTreePanel } from './file-tree-panel';

type ShellSection = 'PORTAL' | 'PIPELINE' | 'WORKBENCH';

type AppShellProps = {
  section: ShellSection;
  title: string;
  subtitle: string;
  children: ReactNode;
};

type NavigationItem = {
  href: string;
  label: ShellSection;
};

const NAVIGATION_ITEMS: NavigationItem[] = [
  { href: '/', label: 'PORTAL' },
  { href: '/pipeline', label: 'PIPELINE' },
  { href: '/workbench', label: 'WORKBENCH' }
];

export function AppShell({ section, title, subtitle, children }: AppShellProps): JSX.Element {
  const pathname = usePathname();
  const {
    projectRoot,
    hasElectronDirectoryPicker,
    errorMessage,
    clearError,
    applyProjectRoot,
    chooseProjectRoot,
    clearProjectRoot
  } = useWorkspace();
  const [draftPath, setDraftPath] = useState(projectRoot ?? '');

  useEffect(() => {
    setDraftPath(projectRoot ?? '');
  }, [projectRoot]);

  const currentRootLabel = useMemo(
    () => projectRoot ?? 'No working root selected',
    [projectRoot]
  );

  async function applyDraftPath(): Promise<void> {
    const nextPath = draftPath.trim();
    if (!nextPath) {
      clearProjectRoot();
      return;
    }

    await applyProjectRoot(nextPath);
  }

  return (
    <main className="shell">
      <header className="shell-header">
        <div className="shell-header-main">
          <p className="shell-kicker">{section}</p>
          <h1>{title}</h1>
          <p className="shell-subtitle">{subtitle}</p>
        </div>

        <nav className="shell-nav" aria-label="Primary navigation">
          {NAVIGATION_ITEMS.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                className={active ? 'shell-nav-link shell-nav-link--active' : 'shell-nav-link'}
                href={item.href}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </header>

      <section className="working-root-bar">
        <div className="working-root-fields">
          <label htmlFor="project-root-input">Working Root (`projectRoot`)</label>
          <div className="working-root-controls">
            <input
              id="project-root-input"
              value={draftPath}
              onChange={(event) => {
                setDraftPath(event.target.value);
                if (errorMessage) {
                  clearError();
                }
              }}
              placeholder="/absolute/path/to/execution/root"
            />
            <button type="button" onClick={() => void applyDraftPath()}>
              Apply Path
            </button>
            <button
              type="button"
              className={hasElectronDirectoryPicker ? '' : 'button-muted'}
              onClick={() => void chooseProjectRoot()}
            >
              Choose Folder
            </button>
            <button type="button" className="button-muted" onClick={clearProjectRoot}>
              Clear
            </button>
          </div>
          <p className="working-root-current" title={currentRootLabel}>
            Active root: {currentRootLabel}
          </p>
          {errorMessage ? <p className="working-root-error">{errorMessage}</p> : null}
        </div>
      </section>

      <section className="shell-grid">
        <FileTreePanel />
        <section className="panel panel--main">
          <header className="panel-header">
            <h2>Execution Surface</h2>
          </header>
          <div className="panel-body">{children}</div>
        </section>
        <ChatPanel />
      </section>
    </main>
  );
}
