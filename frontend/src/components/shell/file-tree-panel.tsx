'use client';

import { useEffect, useMemo, useState } from 'react';
import { useWorkspace } from '../workspace/workspace-provider';

type TreeNode = {
  name: string;
  path: string;
  kind: 'directory' | 'file';
  children?: TreeNode[];
  truncated?: boolean;
};

type TreeResponse = {
  root: TreeNode;
  depth: number;
  scannedAt: string;
};

function TreeNodeView({ node }: { node: TreeNode }): JSX.Element {
  const icon = node.kind === 'directory' ? 'DIR' : 'FILE';

  return (
    <li>
      <div className={`tree-item tree-item--${node.kind}`}>
        <span className="tree-item-icon">{icon}</span>
        <span className="tree-item-name" title={node.path}>
          {node.name}
        </span>
      </div>
      {node.children && node.children.length > 0 ? (
        <ul className="tree-list">
          {node.children.map((child) => (
            <TreeNodeView key={child.path} node={child} />
          ))}
        </ul>
      ) : null}
      {node.truncated ? (
        <div className="tree-truncated">Directory listing truncated for responsiveness.</div>
      ) : null}
    </li>
  );
}

export function FileTreePanel(): JSX.Element {
  const { projectRoot } = useWorkspace();
  const [tree, setTree] = useState<TreeNode | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadTree(): Promise<void> {
      if (!projectRoot) {
        setTree(null);
        setError(null);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `/api/working-root/tree?projectRoot=${encodeURIComponent(projectRoot)}&depth=3`
        );
        const payload = (await response.json()) as TreeResponse & {
          error?: { message?: string };
        };

        if (!response.ok || !payload.root) {
          throw new Error(payload.error?.message ?? 'Unable to load directory tree');
        }

        if (!cancelled) {
          setTree(payload.root);
        }
      } catch (loadError) {
        if (!cancelled) {
          const message = loadError instanceof Error ? loadError.message : 'Unable to load directory tree';
          setError(message);
          setTree(null);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadTree();

    return () => {
      cancelled = true;
    };
  }, [projectRoot]);

  const panelBody = useMemo(() => {
    if (!projectRoot) {
      return <p className="panel-empty">Select a Working Root to view filesystem contents.</p>;
    }

    if (loading) {
      return <p className="panel-empty">Loading directory tree...</p>;
    }

    if (error) {
      return <p className="panel-error">{error}</p>;
    }

    if (!tree) {
      return <p className="panel-empty">No files available for this root.</p>;
    }

    return (
      <ul className="tree-list">
        <TreeNodeView node={tree} />
      </ul>
    );
  }, [projectRoot, loading, error, tree]);

  return (
    <aside className="panel panel--file-tree">
      <header className="panel-header">
        <h2>File Tree</h2>
      </header>
      <div className="panel-body">{panelBody}</div>
    </aside>
  );
}
