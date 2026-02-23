'use client';

import { useSearchParams } from 'next/navigation';
import { useEffect, useMemo, useState } from 'react';
import { AppShell } from '../../components/shell/app-shell';
import { useWorkspace } from '../../components/workspace/workspace-provider';
import {
  fetchDeliverableDependencies,
  fetchDeliverableStatus,
  summarizeDependencyRows,
  workspaceApiErrorMessage,
  type DeliverableDependenciesSnapshot,
  type DeliverableStatusSnapshot
} from '../../lib/workspace/deliverable-api';

type ScopeItem = {
  id: string;
  label: string;
  path: string;
};

type ScopeResponse = {
  deliverables: ScopeItem[];
  knowledgeTypes: ScopeItem[];
  hasKnowledgeDecomposition: boolean;
  truncated: boolean;
  scannedAt: string;
};

const BLOCKING_DEPENDENCY_TYPES = new Set(['PREREQUISITE', 'CONSTRAINT']);
const NON_BLOCKING_SATISFACTION = new Set(['SATISFIED', 'WAIVED', 'NOT_APPLICABLE']);

function normalizeAgent(rawValue: string | null): string {
  if (!rawValue) {
    return 'WORKING_ITEMS';
  }

  return rawValue.trim() || 'WORKING_ITEMS';
}

export function WorkbenchClient(): JSX.Element {
  const { projectRoot } = useWorkspace();
  const searchParams = useSearchParams();
  const agent = normalizeAgent(searchParams.get('agent'));
  const row = searchParams.get('row') ?? 'NORMATIVE';
  const column = searchParams.get('column') ?? 'GUIDING';
  const [scopeLoading, setScopeLoading] = useState(false);
  const [scopeError, setScopeError] = useState<string | null>(null);
  const [scopeData, setScopeData] = useState<ScopeResponse | null>(null);
  const [selectedDeliverablePath, setSelectedDeliverablePath] = useState('');
  const [contractsLoading, setContractsLoading] = useState(false);
  const [contractsError, setContractsError] = useState<string | null>(null);
  const [contractsRefreshToken, setContractsRefreshToken] = useState(0);
  const [statusSnapshot, setStatusSnapshot] = useState<DeliverableStatusSnapshot | null>(null);
  const [dependenciesSnapshot, setDependenciesSnapshot] =
    useState<DeliverableDependenciesSnapshot | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadScopeData(): Promise<void> {
      if (!projectRoot) {
        setScopeData(null);
        setScopeError(null);
        setSelectedDeliverablePath('');
        return;
      }

      setScopeLoading(true);
      setScopeError(null);

      try {
        const response = await fetch(
          `/api/working-root/scope?projectRoot=${encodeURIComponent(projectRoot)}`
        );
        const payload = (await response.json()) as ScopeResponse & {
          error?: { message?: string };
        };

        if (!response.ok || !payload) {
          throw new Error(payload.error?.message ?? 'Unable to scan deliverable scopes');
        }

        if (!cancelled) {
          setScopeData(payload);
          setSelectedDeliverablePath(payload.deliverables[0]?.path ?? '');
        }
      } catch (error) {
        if (!cancelled) {
          const message = error instanceof Error ? error.message : 'Unable to scan deliverable scopes';
          setScopeError(message);
          setScopeData(null);
          setSelectedDeliverablePath('');
        }
      } finally {
        if (!cancelled) {
          setScopeLoading(false);
        }
      }
    }

    void loadScopeData();

    return () => {
      cancelled = true;
    };
  }, [projectRoot]);

  useEffect(() => {
    let cancelled = false;

    async function loadContracts(): Promise<void> {
      if (!projectRoot || !selectedDeliverablePath) {
        setContractsError(null);
        setStatusSnapshot(null);
        setDependenciesSnapshot(null);
        return;
      }

      setContractsLoading(true);
      setContractsError(null);

      try {
        const [status, dependencies] = await Promise.all([
          fetchDeliverableStatus(projectRoot, selectedDeliverablePath),
          fetchDeliverableDependencies(projectRoot, selectedDeliverablePath)
        ]);

        if (!cancelled) {
          setStatusSnapshot(status);
          setDependenciesSnapshot(dependencies);
        }
      } catch (error) {
        if (!cancelled) {
          setContractsError(workspaceApiErrorMessage(error));
          setStatusSnapshot(null);
          setDependenciesSnapshot(null);
        }
      } finally {
        if (!cancelled) {
          setContractsLoading(false);
        }
      }
    }

    void loadContracts();

    return () => {
      cancelled = true;
    };
  }, [projectRoot, selectedDeliverablePath, contractsRefreshToken]);

  const scopeSummary = useMemo(() => {
    if (!projectRoot) {
      return 'No Working Root selected.';
    }

    if (scopeLoading) {
      return 'Scanning working root for deliverable scope...';
    }

    if (scopeError) {
      return scopeError;
    }

    if (!scopeData) {
      return 'No scope data available.';
    }

    return `${scopeData.deliverables.length} deliverables available for WORKBENCH contract checks.`;
  }, [projectRoot, scopeLoading, scopeError, scopeData]);

  const selectedDeliverable = useMemo(
    () => scopeData?.deliverables.find((item) => item.path === selectedDeliverablePath) ?? null,
    [scopeData, selectedDeliverablePath]
  );

  const dependencySummary = useMemo(
    () => (dependenciesSnapshot ? summarizeDependencyRows(dependenciesSnapshot.rows) : null),
    [dependenciesSnapshot]
  );

  const blockerCandidateIds = useMemo(() => {
    if (!dependenciesSnapshot) {
      return [] as string[];
    }

    return dependenciesSnapshot.rows
      .filter((row) => {
        const status = (row.Status ?? '').trim().toUpperCase();
        const direction = (row.Direction ?? '').trim().toUpperCase();
        const dependencyType = (row.DependencyType ?? '').trim().toUpperCase();
        const satisfaction = (row.SatisfactionStatus ?? 'TBD').trim().toUpperCase();

        if (status !== 'ACTIVE') {
          return false;
        }
        if (direction !== 'UPSTREAM') {
          return false;
        }
        if (!BLOCKING_DEPENDENCY_TYPES.has(dependencyType)) {
          return false;
        }

        return !NON_BLOCKING_SATISFACTION.has(satisfaction);
      })
      .slice(0, 5)
      .map((row) => row.DependencyID);
  }, [dependenciesSnapshot]);

  return (
    <AppShell
      section="WORKBENCH"
      title="Persona Session Surface"
      subtitle="Interactive manager-agent workspace for scoped briefs, findings, and operator decisions."
    >
      <section className="workbench-layout">
        <section className="workbench-card">
          <header>
            <h3>Active Agent Context</h3>
          </header>
          <dl>
            <div>
              <dt>Agent</dt>
              <dd>{agent}</dd>
            </div>
            <div>
              <dt>Matrix Row</dt>
              <dd>{row}</dd>
            </div>
            <div>
              <dt>Matrix Column</dt>
              <dd>{column}</dd>
            </div>
          </dl>
          <p>{scopeSummary}</p>
          <p>
            WORKBENCH preserves chat-driven orchestration while PIPELINE handles spawned task
            execution. This view now consumes deliverable contract routes for persona-led checks.
          </p>
        </section>

        <article className="pipeline-contracts">
          <header className="pipeline-contracts-header">
            <div>
              <h3>Deliverable Contracts (Read-Only)</h3>
              <p className="pipeline-note">
                Uses lifecycle/dependency contract APIs for dependency and reconciliation reviews.
              </p>
            </div>
            <button
              type="button"
              className="button-muted"
              disabled={!projectRoot || !selectedDeliverablePath || contractsLoading}
              onClick={() => {
                setContractsRefreshToken((value) => value + 1);
              }}
            >
              Refresh
            </button>
          </header>

          <label>
            Deliverable scope
            <select
              value={selectedDeliverablePath}
              onChange={(event) => {
                setSelectedDeliverablePath(event.target.value);
              }}
              disabled={!scopeData || scopeData.deliverables.length === 0}
            >
              {scopeData?.deliverables.length ? null : <option value="">No deliverables found</option>}
              {scopeData?.deliverables.map((item) => (
                <option key={item.path} value={item.path}>
                  {item.id} — {item.label}
                </option>
              ))}
            </select>
          </label>

          {!projectRoot ? (
            <p className="panel-empty">Select a Working Root to load contract snapshots.</p>
          ) : contractsLoading ? (
            <p className="panel-empty">Loading contract snapshots...</p>
          ) : contractsError ? (
            <p className="panel-error">{contractsError}</p>
          ) : !statusSnapshot || !dependenciesSnapshot ? (
            <p className="panel-empty">No contract data available for the selected deliverable.</p>
          ) : (
            <>
              <p className="pipeline-contract-path" title={statusSnapshot.deliverablePath}>
                {statusSnapshot.deliverablePath}
              </p>

              {selectedDeliverable ? (
                <p className="pipeline-note">
                  Selected deliverable: {selectedDeliverable.id} — {selectedDeliverable.label}
                </p>
              ) : null}

              <dl className="pipeline-contract-metrics">
                <div>
                  <dt>Current state</dt>
                  <dd>{statusSnapshot.status.currentState}</dd>
                </div>
                <div>
                  <dt>Last updated</dt>
                  <dd>{statusSnapshot.status.lastUpdated}</dd>
                </div>
                <div>
                  <dt>History entries</dt>
                  <dd>{statusSnapshot.status.history.length}</dd>
                </div>
                <div>
                  <dt>Dependency rows</dt>
                  <dd>{dependencySummary?.totalRows ?? 0}</dd>
                </div>
                <div>
                  <dt>Active rows</dt>
                  <dd>{dependencySummary?.activeRows ?? 0}</dd>
                </div>
                <div>
                  <dt>Active upstream blockers</dt>
                  <dd>{dependencySummary?.activeUpstreamBlockerCandidates ?? 0}</dd>
                </div>
              </dl>

              {blockerCandidateIds.length > 0 ? (
                <div className="pipeline-contract-warnings">
                  <h4>Top blocker candidates</h4>
                  <ul>
                    {blockerCandidateIds.map((dependencyId) => (
                      <li key={dependencyId}>{dependencyId}</li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {dependenciesSnapshot.warnings.length > 0 ? (
                <div className="pipeline-contract-warnings">
                  <h4>Register warnings</h4>
                  <ul>
                    {dependenciesSnapshot.warnings.slice(0, 3).map((warning) => (
                      <li key={warning}>{warning}</li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </>
          )}
        </article>
      </section>
    </AppShell>
  );
}

export default WorkbenchClient;
