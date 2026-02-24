'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Suspense,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type KeyboardEvent,
  type PointerEvent,
  type ReactNode
} from 'react';
import {
  DEFAULT_PANE_WIDTH_PX,
  MIN_PANE_WIDTH_PX,
  clampPaneWidthForLayout,
  createDefaultLayoutState,
  readLayoutStateFromStorage,
  resolvePaneWidth,
  writeLayoutStateToStorage,
  type LayoutStorageState,
  type ResizablePaneKey
} from '../../lib/shell/layout-state';
import { useToolkit } from '../workspace/toolkit-provider';
import { useWorkspace } from '../workspace/workspace-provider';
import { ChatPanel } from './chat-panel';
import { FileTreePanel } from './file-tree-panel';
import { OperatorToolkitPanel } from './operator-toolkit-panel';

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

const PANE_TITLE: Record<ResizablePaneKey, string> = {
  fileTree: 'File Tree',
  toolkit: 'Tool Kit',
  chat: 'Chat Panel'
};

const DRAG_DIRECTION: Record<ResizablePaneKey, 1 | -1> = {
  fileTree: 1,
  toolkit: -1,
  chat: -1
};

export function AppShell({ section, title, subtitle, children }: AppShellProps): JSX.Element {
  const pathname = usePathname();
  const { isToolkitVisible, setToolkitVisible } = useToolkit();
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
  const [updateNotice] = useState<string | null>(null);
  const [layoutState, setLayoutState] = useState<LayoutStorageState>(() =>
    createDefaultLayoutState()
  );
  const [layoutWidth, setLayoutWidth] = useState(0);
  const [resizingPane, setResizingPane] = useState<ResizablePaneKey | null>(null);
  const layoutRef = useRef<HTMLElement | null>(null);
  const dragStateRef = useRef<{
    pane: ResizablePaneKey;
    startX: number;
    startWidth: number;
  } | null>(null);

  useEffect(() => {
    setDraftPath(projectRoot ?? '');
  }, [projectRoot]);

  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }
    setLayoutState(readLayoutStateFromStorage(window.localStorage));
  }, []);

  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }
    writeLayoutStateToStorage(window.localStorage, layoutState);
  }, [layoutState]);

  useEffect(() => {
    const element = layoutRef.current;
    if (!element) {
      return;
    }

    const updateWidth = (): void => {
      setLayoutWidth(element.clientWidth);
    };

    updateWidth();

    const observer = new ResizeObserver(updateWidth);
    observer.observe(element);

    return () => {
      observer.disconnect();
    };
  }, [isToolkitVisible]);

  const currentRootLabel = useMemo(
    () => projectRoot ?? 'No working root selected',
    [projectRoot]
  );

  const gridStyle = useMemo(
    () =>
      ({
        '--pane-file-tree-width': `${resolvePaneWidth(layoutState, 'fileTree', isToolkitVisible)}px`,
        '--pane-toolkit-width': `${resolvePaneWidth(layoutState, 'toolkit', isToolkitVisible)}px`,
        '--pane-chat-width': `${resolvePaneWidth(layoutState, 'chat', isToolkitVisible)}px`
      }) as CSSProperties,
    [isToolkitVisible, layoutState]
  );

  const resizePaneByDelta = useCallback(
    (pane: ResizablePaneKey, delta: number): void => {
      setLayoutState((current) => {
        const requestedWidth = current.widths[pane] + delta;
        const nextWidth = clampPaneWidthForLayout({
          pane,
          requestedWidth,
          state: current,
          layoutWidth,
          toolkitVisible: isToolkitVisible
        });

        return {
          ...current,
          collapsed: {
            ...current.collapsed,
            [pane]: false
          },
          widths: {
            ...current.widths,
            [pane]: nextWidth
          }
        };
      });
    },
    [isToolkitVisible, layoutWidth]
  );

  const togglePaneCollapse = useCallback((pane: ResizablePaneKey): void => {
    setLayoutState((current) => ({
      ...current,
      collapsed: {
        ...current.collapsed,
        [pane]: !current.collapsed[pane]
      }
    }));
  }, []);

  const handleResizePointerDown = useCallback(
    (event: PointerEvent<HTMLDivElement>, pane: ResizablePaneKey): void => {
      if (event.button !== 0) {
        return;
      }

      event.preventDefault();
      dragStateRef.current = {
        pane,
        startX: event.clientX,
        startWidth: layoutState.widths[pane]
      };
      setResizingPane(pane);
    },
    [layoutState.widths]
  );

  useEffect(() => {
    if (!resizingPane) {
      return;
    }

    const handlePointerMove = (event: globalThis.PointerEvent): void => {
      const dragState = dragStateRef.current;
      if (!dragState) {
        return;
      }

      const delta = (event.clientX - dragState.startX) * DRAG_DIRECTION[dragState.pane];
      const requestedWidth = dragState.startWidth + delta;

      setLayoutState((current) => {
        const nextWidth = clampPaneWidthForLayout({
          pane: dragState.pane,
          requestedWidth,
          state: current,
          layoutWidth,
          toolkitVisible: isToolkitVisible
        });

        return {
          ...current,
          collapsed: {
            ...current.collapsed,
            [dragState.pane]: false
          },
          widths: {
            ...current.widths,
            [dragState.pane]: nextWidth
          }
        };
      });
    };

    const stopResizing = (): void => {
      dragStateRef.current = null;
      setResizingPane(null);
    };

    window.addEventListener('pointermove', handlePointerMove);
    window.addEventListener('pointerup', stopResizing);
    window.addEventListener('pointercancel', stopResizing);

    return () => {
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('pointerup', stopResizing);
      window.removeEventListener('pointercancel', stopResizing);
    };
  }, [isToolkitVisible, layoutWidth, resizingPane]);

  function handleResizeKeyDown(event: KeyboardEvent<HTMLDivElement>, pane: ResizablePaneKey): void {
    const step = event.shiftKey ? 40 : 16;

    if (event.key === 'ArrowRight') {
      event.preventDefault();
      resizePaneByDelta(pane, step);
      return;
    }

    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      resizePaneByDelta(pane, -step);
      return;
    }

    if (event.key === 'Home') {
      event.preventDefault();
      setLayoutState((current) => ({
        ...current,
        collapsed: {
          ...current.collapsed,
          [pane]: true
        }
      }));
      return;
    }

    if (event.key === 'End') {
      event.preventDefault();
      setLayoutState((current) => {
        const requestedWidth = current.widths[pane] || DEFAULT_PANE_WIDTH_PX[pane];
        const nextWidth = clampPaneWidthForLayout({
          pane,
          requestedWidth,
          state: current,
          layoutWidth,
          toolkitVisible: isToolkitVisible
        });

        return {
          ...current,
          collapsed: {
            ...current.collapsed,
            [pane]: false
          },
          widths: {
            ...current.widths,
            [pane]: nextWidth
          }
        };
      });
    }
  }

  function renderResizeHandle(pane: ResizablePaneKey): JSX.Element {
    const widthNow = resolvePaneWidth(layoutState, pane, isToolkitVisible);
    const isActive = resizingPane === pane;

    return (
      <div
        key={`handle-${pane}`}
        className={isActive ? 'shell-resize-handle shell-resize-handle--active' : 'shell-resize-handle'}
        role="separator"
        aria-label={`Resize ${PANE_TITLE[pane]}`}
        aria-orientation="vertical"
        aria-valuemin={MIN_PANE_WIDTH_PX[pane]}
        aria-valuenow={widthNow}
        tabIndex={0}
        onPointerDown={(event) => {
          handleResizePointerDown(event, pane);
        }}
        onKeyDown={(event) => {
          handleResizeKeyDown(event, pane);
        }}
      />
    );
  }

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
          <div className="shell-brand-row">
            <img
              src="/chirality-app-icon.svg"
              alt="Chirality app icon"
              className="shell-brand-tile"
              width={48}
              height={48}
            />
            <div className="shell-brand-meta">
              <p className="shell-kicker">{section}</p>
              <h1>{title}</h1>
            </div>
          </div>
          <p className="shell-subtitle">{subtitle}</p>
          {updateNotice ? (
            <p className="shell-update-banner" role="status" aria-live="polite">
              {updateNotice}
            </p>
          ) : null}
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
          <label className="toolkit-checkbox">
            <input
              type="checkbox"
              checked={isToolkitVisible}
              onChange={(event) => {
                setToolkitVisible(event.target.checked);
              }}
            />
            Show Tool Kit sidebar
          </label>
          {errorMessage ? <p className="working-root-error">{errorMessage}</p> : null}
        </div>
      </section>

      <section
        ref={layoutRef}
        className={isToolkitVisible ? 'shell-grid shell-grid--resizable shell-grid--with-toolkit' : 'shell-grid shell-grid--resizable'}
        style={gridStyle}
      >
        <div
          className={
            layoutState.collapsed.fileTree ? 'shell-pane shell-pane--file-tree shell-pane--collapsed' : 'shell-pane shell-pane--file-tree'
          }
        >
          <button
            type="button"
            className="shell-pane-toggle button-muted"
            onClick={() => {
              togglePaneCollapse('fileTree');
            }}
          >
            {layoutState.collapsed.fileTree ? 'Expand' : 'Collapse'}
          </button>
          {layoutState.collapsed.fileTree ? (
            <span className="shell-pane-collapsed-label">File Tree</span>
          ) : null}
          <FileTreePanel />
        </div>

        {renderResizeHandle('fileTree')}

        <section className="panel panel--main">
          <header className="panel-header">
            <h2>Execution Surface</h2>
          </header>
          <div className="panel-body">{children}</div>
        </section>

        {isToolkitVisible ? (
          <>
            {renderResizeHandle('toolkit')}
            <div
              className={
                layoutState.collapsed.toolkit ? 'shell-pane shell-pane--toolkit shell-pane--collapsed' : 'shell-pane shell-pane--toolkit'
              }
            >
              <button
                type="button"
                className="shell-pane-toggle button-muted"
                onClick={() => {
                  togglePaneCollapse('toolkit');
                }}
              >
                {layoutState.collapsed.toolkit ? 'Expand' : 'Collapse'}
              </button>
              {layoutState.collapsed.toolkit ? (
                <span className="shell-pane-collapsed-label">Tool Kit</span>
              ) : null}
              <OperatorToolkitPanel />
            </div>
          </>
        ) : null}

        {renderResizeHandle('chat')}

        <div
          className={layoutState.collapsed.chat ? 'shell-pane shell-pane--chat shell-pane--collapsed' : 'shell-pane shell-pane--chat'}
        >
          <button
            type="button"
            className="shell-pane-toggle button-muted"
            onClick={() => {
              togglePaneCollapse('chat');
            }}
          >
            {layoutState.collapsed.chat ? 'Expand' : 'Collapse'}
          </button>
          {layoutState.collapsed.chat ? <span className="shell-pane-collapsed-label">Chat</span> : null}
          <Suspense
            fallback={
              <aside className="panel panel--chat">
                <header className="panel-header">
                  <h2>Chat Panel</h2>
                </header>
                <div className="panel-body chat-transcript">
                  <p className="panel-empty">Loading chat panel...</p>
                </div>
              </aside>
            }
          >
            <ChatPanel />
          </Suspense>
        </div>
      </section>
    </main>
  );
}
