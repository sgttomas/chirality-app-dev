'use client';

import { useSearchParams } from 'next/navigation';
import { useEffect, useMemo, useState, type FormEvent } from 'react';
import { AppShell } from '../../components/shell/app-shell';
import { useWorkspace } from '../../components/workspace/workspace-provider';
import { harnessApiErrorMessage, scaffoldHarnessExecutionRoot } from '../../lib/harness/client';
import type { CoordinationMode, ScaffoldExecutionRootResponse } from '../../lib/harness/types';
import {
  currentIsoDate,
  fetchDeliverableDependencies,
  fetchDeliverableStatus,
  nextLifecycleTargets,
  summarizeDependencyRows,
  transitionDeliverableStatus,
  workspaceApiErrorMessage,
  type DeliverableDependenciesSnapshot,
  type DeliverableStatusSnapshot
} from '../../lib/workspace/deliverable-api';

type OperativeCategory = 'DECOMP' | 'PREP' | 'TASK' | 'AUDIT';

type Option = {
  value: string;
  label: string;
  enabled: boolean;
};

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

const CATEGORY_ORDER: OperativeCategory[] = ['DECOMP', 'PREP', 'TASK', 'AUDIT'];
const SATISFACTION_DISPLAY_ORDER = [
  'TBD',
  'PENDING',
  'IN_PROGRESS',
  'SATISFIED',
  'WAIVED',
  'NOT_APPLICABLE'
];

const TRANSITION_ACTOR_OPTIONS: Option[] = [
  { value: 'WORKING_ITEMS', label: 'WORKING_ITEMS', enabled: true },
  { value: 'HUMAN', label: 'HUMAN', enabled: true },
  { value: 'CHIRALITY_FRAMEWORK', label: 'CHIRALITY_FRAMEWORK', enabled: true },
  { value: '4_DOCUMENTS', label: '4_DOCUMENTS', enabled: true }
];

const DECOMP_OPTIONS: Option[] = [
  { value: 'SOFTWARE', label: 'SOFTWARE', enabled: true },
  { value: 'PROJECT', label: 'PROJECT', enabled: true },
  { value: 'DOMAIN', label: 'DOMAIN', enabled: true },
  { value: 'BASE', label: 'BASE (create new)', enabled: false }
];

const PREP_OPTIONS: Option[] = [
  { value: 'PREPARATION', label: 'PREPARATION', enabled: true },
  { value: '4_DOCUMENTS', label: '4_DOCUMENTS', enabled: true },
  { value: 'CHIRALITY_FRAMEWORK', label: 'CHIRALITY_FRAMEWORK', enabled: true },
  { value: 'CHIRALITY_LENS', label: 'CHIRALITY_LENS', enabled: true }
];

const TASK_AGENT_OPTIONS: Option[] = [
  { value: 'SCOPE_CHANGE', label: 'SCOPE_CHANGE', enabled: true },
  { value: 'SCOPE_PREP', label: 'SCOPE_PREP', enabled: true },
  { value: 'ESTIMATE_PREP', label: 'ESTIMATE_PREP', enabled: true },
  { value: 'AUDIT_PREP', label: 'AUDIT_PREP', enabled: true },
  { value: 'SCHEDULE_PREP', label: 'SCHEDULE_PREP', enabled: true },
  { value: 'ESTIMATING', label: 'ESTIMATING', enabled: false },
  { value: 'SCHEDULING', label: 'SCHEDULING', enabled: false }
];

const AUDIT_OPTIONS: Option[] = [
  { value: 'AGENTS', label: 'AGENTS', enabled: true },
  { value: 'DEPENDENCIES', label: 'DEPENDENCIES', enabled: true },
  { value: 'ESTIMATES', label: 'ESTIMATES', enabled: false },
  { value: 'REFERENCES', label: 'REFERENCES', enabled: true },
  { value: 'SCHEDULES', label: 'SCHEDULES', enabled: false },
  { value: 'SCOPE', label: 'SCOPE', enabled: true }
];

const COORDINATION_MODE_OPTIONS: CoordinationMode[] = [
  'DEPENDENCY_TRACKED',
  'SCHEDULE_FIRST',
  'HYBRID'
];

function normalizeCategory(rawValue: string | null): OperativeCategory {
  const fallback: OperativeCategory = 'DECOMP';
  if (!rawValue) {
    return fallback;
  }

  if (CATEGORY_ORDER.includes(rawValue as OperativeCategory)) {
    return rawValue as OperativeCategory;
  }

  return fallback;
}

function renderOptionLabel(option: Option): string {
  return option.enabled ? option.label : `${option.label} (coming soon)`;
}

export function PipelineClient(): JSX.Element {
  const { projectRoot } = useWorkspace();
  const searchParams = useSearchParams();

  const [selectedCategory, setSelectedCategory] = useState<OperativeCategory>('DECOMP');
  const [selectedDecomp, setSelectedDecomp] = useState('SOFTWARE');
  const [selectedPrep, setSelectedPrep] = useState('PREPARATION');
  const [selectedAudit, setSelectedAudit] = useState('AGENTS');
  const [selectedTaskAgent, setSelectedTaskAgent] = useState('SCOPE_CHANGE');
  const [selectedDeliverableScope, setSelectedDeliverableScope] = useState('');
  const [selectedKnowledgeScope, setSelectedKnowledgeScope] = useState('');

  const [scopeRefreshToken, setScopeRefreshToken] = useState(0);
  const [scopeLoading, setScopeLoading] = useState(false);
  const [scopeError, setScopeError] = useState<string | null>(null);
  const [scopeData, setScopeData] = useState<ScopeResponse | null>(null);

  const [contractsRefreshToken, setContractsRefreshToken] = useState(0);
  const [contractsLoading, setContractsLoading] = useState(false);
  const [contractsError, setContractsError] = useState<string | null>(null);
  const [statusSnapshot, setStatusSnapshot] = useState<DeliverableStatusSnapshot | null>(null);
  const [dependenciesSnapshot, setDependenciesSnapshot] =
    useState<DeliverableDependenciesSnapshot | null>(null);

  const [transitionTarget, setTransitionTarget] = useState('');
  const [transitionActor, setTransitionActor] = useState('WORKING_ITEMS');
  const [transitionDate, setTransitionDate] = useState(currentIsoDate);
  const [transitionApprovalSha, setTransitionApprovalSha] = useState('');
  const [transitionError, setTransitionError] = useState<string | null>(null);
  const [transitionSubmitting, setTransitionSubmitting] = useState(false);

  const [scaffoldDecompositionPath, setScaffoldDecompositionPath] = useState('');
  const [scaffoldProjectName, setScaffoldProjectName] = useState('');
  const [scaffoldCoordinationMode, setScaffoldCoordinationMode] =
    useState<CoordinationMode>('DEPENDENCY_TRACKED');
  const [scaffoldSubmitting, setScaffoldSubmitting] = useState(false);
  const [scaffoldError, setScaffoldError] = useState<string | null>(null);
  const [scaffoldResult, setScaffoldResult] = useState<ScaffoldExecutionRootResponse | null>(null);

  useEffect(() => {
    setSelectedCategory(normalizeCategory(searchParams.get('category')));
  }, [searchParams]);

  useEffect(() => {
    setScaffoldResult(null);
    setScaffoldError(null);
    setScaffoldProjectName('');
    setScaffoldCoordinationMode('DEPENDENCY_TRACKED');
  }, [projectRoot]);

  useEffect(() => {
    let cancelled = false;

    async function loadScopeData(): Promise<void> {
      if (!projectRoot) {
        setScopeData(null);
        setScopeError(null);
        setSelectedDeliverableScope('');
        setSelectedKnowledgeScope('');
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
          setSelectedDeliverableScope(payload.deliverables[0]?.path ?? '');
          setSelectedKnowledgeScope(payload.knowledgeTypes[0]?.path ?? '');
        }
      } catch (error) {
        if (!cancelled) {
          const message = error instanceof Error ? error.message : 'Unable to scan deliverable scopes';
          setScopeError(message);
          setScopeData(null);
          setSelectedDeliverableScope('');
          setSelectedKnowledgeScope('');
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
  }, [projectRoot, scopeRefreshToken]);

  useEffect(() => {
    let cancelled = false;

    async function loadDeliverableContracts(): Promise<void> {
      if (!projectRoot || !selectedDeliverableScope) {
        setStatusSnapshot(null);
        setDependenciesSnapshot(null);
        setContractsError(null);
        return;
      }

      setContractsLoading(true);
      setContractsError(null);

      try {
        const [status, dependencies] = await Promise.all([
          fetchDeliverableStatus(projectRoot, selectedDeliverableScope),
          fetchDeliverableDependencies(projectRoot, selectedDeliverableScope)
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

    void loadDeliverableContracts();

    return () => {
      cancelled = true;
    };
  }, [projectRoot, selectedDeliverableScope, contractsRefreshToken]);

  const currentLifecycleState = statusSnapshot?.status.currentState;

  useEffect(() => {
    if (!currentLifecycleState) {
      setTransitionTarget('');
      return;
    }

    const allowedTargets = nextLifecycleTargets(currentLifecycleState);
    setTransitionTarget(allowedTargets[0] ?? '');
    setTransitionError(null);
  }, [currentLifecycleState]);

  const scopeSummary = useMemo(() => {
    if (!projectRoot) {
      return 'No Working Root selected.';
    }

    if (scopeLoading) {
      return 'Scanning working root for deliverables and knowledge types...';
    }

    if (scopeError) {
      return scopeError;
    }

    if (!scopeData) {
      return 'No scope data available.';
    }

    const baseSummary = `${scopeData.deliverables.length} deliverables, ${scopeData.knowledgeTypes.length} knowledge types`;
    if (!scopeData.truncated) {
      return baseSummary;
    }

    return `${baseSummary}. Scan truncated at directory cap for responsiveness.`;
  }, [projectRoot, scopeLoading, scopeError, scopeData]);

  const selectedDeliverable = useMemo(
    () => scopeData?.deliverables.find((item) => item.path === selectedDeliverableScope) ?? null,
    [scopeData, selectedDeliverableScope]
  );

  const dependencySummary = useMemo(
    () => (dependenciesSnapshot ? summarizeDependencyRows(dependenciesSnapshot.rows) : null),
    [dependenciesSnapshot]
  );

  const satisfactionSummary = useMemo(() => {
    if (!dependencySummary) {
      return [] as Array<{ key: string; count: number }>;
    }

    const seen = new Set<string>();
    const ordered: Array<{ key: string; count: number }> = [];

    for (const key of SATISFACTION_DISPLAY_ORDER) {
      const count = dependencySummary.bySatisfaction[key];
      if (count) {
        seen.add(key);
        ordered.push({ key, count });
      }
    }

    for (const [key, count] of Object.entries(dependencySummary.bySatisfaction)) {
      if (!seen.has(key)) {
        ordered.push({ key, count });
      }
    }

    return ordered;
  }, [dependencySummary]);

  const availableTransitionTargets = useMemo(
    () => (currentLifecycleState ? nextLifecycleTargets(currentLifecycleState) : []),
    [currentLifecycleState]
  );

  const scaffoldIssuePreview = useMemo(() => {
    if (!scaffoldResult || scaffoldResult.preparationCompatibility.ready) {
      return [] as Array<{ deliverableId: string; message: string }>;
    }

    const preview: Array<{ deliverableId: string; message: string }> = [];
    for (const item of scaffoldResult.preparationCompatibility.deliverables) {
      for (const issue of item.issues) {
        preview.push({
          deliverableId: item.id,
          message: issue
        });
        if (preview.length >= 5) {
          return preview;
        }
      }
    }

    return preview;
  }, [scaffoldResult]);

  const canSubmitTransition =
    Boolean(projectRoot) &&
    Boolean(selectedDeliverableScope) &&
    Boolean(transitionTarget) &&
    !transitionSubmitting &&
    !contractsLoading;

  async function submitTransition(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();

    if (!projectRoot || !selectedDeliverableScope || !transitionTarget) {
      return;
    }

    setTransitionSubmitting(true);
    setTransitionError(null);

    try {
      const result = await transitionDeliverableStatus({
        projectRoot,
        deliverablePath: selectedDeliverableScope,
        targetState: transitionTarget,
        actor: transitionActor,
        date: transitionDate.trim() || undefined,
        approvalSha: transitionApprovalSha.trim() || undefined
      });

      setStatusSnapshot(result);
    } catch (error) {
      setTransitionError(workspaceApiErrorMessage(error));
    } finally {
      setTransitionSubmitting(false);
    }
  }

  async function submitScaffold(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();

    if (!projectRoot) {
      setScaffoldError('Select a Working Root before running scaffold.');
      return;
    }

    const decompositionPath = scaffoldDecompositionPath.trim();
    if (!decompositionPath) {
      setScaffoldError('Decomposition path is required.');
      return;
    }

    setScaffoldSubmitting(true);
    setScaffoldError(null);

    try {
      const result = await scaffoldHarnessExecutionRoot({
        executionRoot: projectRoot,
        decompositionPath,
        projectName: scaffoldProjectName.trim() || undefined,
        coordinationMode: scaffoldCoordinationMode
      });

      setScaffoldResult(result);
      setScopeRefreshToken((value) => value + 1);
      setContractsRefreshToken((value) => value + 1);
    } catch (error) {
      setScaffoldResult(null);
      setScaffoldError(harnessApiErrorMessage(error));
    } finally {
      setScaffoldSubmitting(false);
    }
  }

  function requestContractsRefresh(): void {
    setTransitionError(null);
    setContractsRefreshToken((value) => value + 1);
  }

  return (
    <AppShell
      section="PIPELINE"
      title="Operative Pipeline"
      subtitle="Configure DECOMP, PREP, TASK, and AUDIT execution intents from one shell surface."
    >
      <section className="pipeline-layout">
        <section className="pipeline-grid">
          <article className={`pipeline-card ${selectedCategory === 'DECOMP' ? 'pipeline-card--active' : ''}`}>
            <header>
              <h3>DECOMP*</h3>
              <p>SOFTWARE, PROJECT, DOMAIN, and BASE create-new variant routing.</p>
            </header>
            <label>
              Decomposition lane
              <select
                value={selectedDecomp}
                onChange={(event) => {
                  setSelectedCategory('DECOMP');
                  setSelectedDecomp(event.target.value);
                }}
              >
                {DECOMP_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value} disabled={!option.enabled}>
                    {renderOptionLabel(option)}
                  </option>
                ))}
              </select>
            </label>
          </article>

          <article className={`pipeline-card ${selectedCategory === 'PREP' ? 'pipeline-card--active' : ''}`}>
            <header>
              <h3>PREP*</h3>
              <p>Preparation and semantic framing pipelines.</p>
            </header>
            <label>
              Preparation lane
              <select
                value={selectedPrep}
                onChange={(event) => {
                  setSelectedCategory('PREP');
                  setSelectedPrep(event.target.value);
                }}
              >
                {PREP_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value} disabled={!option.enabled}>
                    {renderOptionLabel(option)}
                  </option>
                ))}
              </select>
            </label>
          </article>

          <article className={`pipeline-card ${selectedCategory === 'TASK' ? 'pipeline-card--active' : ''}`}>
            <header>
              <h3>TASK*</h3>
              <p>Split selectors: static task agent + dynamic scope from Working Root.</p>
            </header>

            <label>
              Task agent
              <select
                value={selectedTaskAgent}
                onChange={(event) => {
                  setSelectedCategory('TASK');
                  setSelectedTaskAgent(event.target.value);
                }}
              >
                {TASK_AGENT_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value} disabled={!option.enabled}>
                    {renderOptionLabel(option)}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Deliverable scope (dynamic)
              <select
                value={selectedDeliverableScope}
                onChange={(event) => {
                  setSelectedCategory('TASK');
                  setSelectedDeliverableScope(event.target.value);
                }}
                disabled={!scopeData || scopeData.deliverables.length === 0}
              >
                {scopeData?.deliverables.length ? null : (
                  <option value="">No deliverables found</option>
                )}
                {scopeData?.deliverables.map((item) => (
                  <option key={item.path} value={item.path}>
                    {item.id} — {item.label}
                  </option>
                ))}
              </select>
            </label>

            {scopeData?.hasKnowledgeDecomposition ? (
              <label>
                Knowledge-type scope (dynamic)
                <select
                  value={selectedKnowledgeScope}
                  onChange={(event) => {
                    setSelectedCategory('TASK');
                    setSelectedKnowledgeScope(event.target.value);
                  }}
                  disabled={scopeData.knowledgeTypes.length === 0}
                >
                  {scopeData.knowledgeTypes.length ? null : (
                    <option value="">No knowledge types found</option>
                  )}
                  {scopeData.knowledgeTypes.map((item) => (
                    <option key={item.path} value={item.path}>
                      {item.id} — {item.label}
                    </option>
                  ))}
                </select>
              </label>
            ) : (
              <p className="pipeline-note">
                Knowledge-type selector hidden: no DOMAIN decomposition marker detected in
                `_Decomposition`.
              </p>
            )}
          </article>

          <article className={`pipeline-card ${selectedCategory === 'AUDIT' ? 'pipeline-card--active' : ''}`}>
            <header>
              <h3>AUDIT*</h3>
              <p>Evaluation lanes with selective "coming soon" support.</p>
            </header>
            <label>
              Audit lane
              <select
                value={selectedAudit}
                onChange={(event) => {
                  setSelectedCategory('AUDIT');
                  setSelectedAudit(event.target.value);
                }}
              >
                {AUDIT_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value} disabled={!option.enabled}>
                    {renderOptionLabel(option)}
                  </option>
                ))}
              </select>
            </label>
          </article>
        </section>

        <article className="pipeline-summary">
          <h3>Dynamic Scope Scan</h3>
          <p>{scopeSummary}</p>
          <p>
            Selected category: <strong>{selectedCategory}</strong>
          </p>
        </article>

        <article className="pipeline-contracts">
          <header className="pipeline-contracts-header">
            <div>
              <h3>Execution Root Scaffold</h3>
              <p className="pipeline-note">
                Runs `POST /api/harness/scaffold` and validates PREPARATION handoff compatibility.
              </p>
            </div>
          </header>

          {!projectRoot ? (
            <p className="panel-empty">Select a Working Root before running scaffold.</p>
          ) : (
            <form
              className="pipeline-transition-form"
              onSubmit={(event) => {
                void submitScaffold(event);
              }}
            >
              <div className="pipeline-transition-grid">
                <label>
                  Decomposition markdown path
                  <input
                    value={scaffoldDecompositionPath}
                    onChange={(event) => {
                      setScaffoldDecompositionPath(event.target.value);
                      if (scaffoldError) {
                        setScaffoldError(null);
                      }
                    }}
                    placeholder="/absolute/path/to/decomposition.md"
                  />
                </label>

                <label>
                  Coordination mode
                  <select
                    value={scaffoldCoordinationMode}
                    onChange={(event) => {
                      setScaffoldCoordinationMode(event.target.value as CoordinationMode);
                    }}
                  >
                    {COORDINATION_MODE_OPTIONS.map((mode) => (
                      <option key={mode} value={mode}>
                        {mode}
                      </option>
                    ))}
                  </select>
                </label>

                <label>
                  Project name (optional)
                  <input
                    value={scaffoldProjectName}
                    onChange={(event) => {
                      setScaffoldProjectName(event.target.value);
                    }}
                    placeholder="Overrides decomposition title"
                  />
                </label>
              </div>

              {scaffoldError ? <p className="panel-error">{scaffoldError}</p> : null}

              <div className="pipeline-transition-actions">
                <button
                  type="submit"
                  disabled={scaffoldSubmitting || !scaffoldDecompositionPath.trim()}
                >
                  {scaffoldSubmitting ? 'Scaffolding...' : 'Scaffold Execution Root'}
                </button>
              </div>
            </form>
          )}

          {scaffoldResult ? (
            <>
              <p className="pipeline-contract-path" title={scaffoldResult.executionRoot}>
                {scaffoldResult.executionRoot}
              </p>
              <p className="pipeline-note" title={scaffoldResult.decompositionPath}>
                Decomposition: {scaffoldResult.decompositionPath}
              </p>
              <dl className="pipeline-contract-metrics">
                <div>
                  <dt>Packages</dt>
                  <dd>{scaffoldResult.packageCount}</dd>
                </div>
                <div>
                  <dt>Deliverables</dt>
                  <dd>{scaffoldResult.deliverableCount}</dd>
                </div>
                <div>
                  <dt>Created directories</dt>
                  <dd>{scaffoldResult.created.directories.length}</dd>
                </div>
                <div>
                  <dt>Created files</dt>
                  <dd>{scaffoldResult.created.files.length}</dd>
                </div>
                <div>
                  <dt>Layout valid</dt>
                  <dd>{scaffoldResult.layoutValidation.valid ? 'YES' : 'NO'}</dd>
                </div>
                <div>
                  <dt>PREPARATION ready</dt>
                  <dd>{scaffoldResult.preparationCompatibility.ready ? 'YES' : 'NO'}</dd>
                </div>
              </dl>

              {!scaffoldResult.preparationCompatibility.ready ? (
                <div className="pipeline-contract-warnings">
                  <h4>PREPARATION Compatibility Issues</h4>
                  <ul>
                    {scaffoldIssuePreview.map((issue) => (
                      <li key={`${issue.deliverableId}:${issue.message}`}>
                        {issue.deliverableId}: {issue.message}
                      </li>
                    ))}
                  </ul>
                  {scaffoldResult.preparationCompatibility.issueCount > scaffoldIssuePreview.length ? (
                    <p className="pipeline-note">
                      +{scaffoldResult.preparationCompatibility.issueCount - scaffoldIssuePreview.length} additional
                      issue(s)
                    </p>
                  ) : null}
                </div>
              ) : null}
            </>
          ) : null}
        </article>

        <article className="pipeline-contracts">
          <header className="pipeline-contracts-header">
            <div>
              <h3>Deliverable Contracts</h3>
              <p className="pipeline-note">
                Consumes lifecycle and dependency contract routes for the selected deliverable.
              </p>
            </div>
            <button
              type="button"
              className="button-muted"
              onClick={requestContractsRefresh}
              disabled={!projectRoot || !selectedDeliverableScope || contractsLoading}
            >
              Refresh
            </button>
          </header>

          {!projectRoot ? (
            <p className="panel-empty">Select a Working Root to inspect deliverable contracts.</p>
          ) : !selectedDeliverableScope ? (
            <p className="panel-empty">Select a deliverable in the TASK lane to load contracts.</p>
          ) : contractsLoading ? (
            <p className="panel-empty">Loading deliverable contract snapshots...</p>
          ) : contractsError ? (
            <p className="panel-error">{contractsError}</p>
          ) : !statusSnapshot || !dependenciesSnapshot ? (
            <p className="panel-empty">No deliverable contract snapshot is currently available.</p>
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
                  <dt>Blocker-subset rows</dt>
                  <dd>{dependencySummary?.activeUpstreamBlockerCandidates ?? 0}</dd>
                </div>
              </dl>

              {satisfactionSummary.length > 0 ? (
                <div className="pipeline-contract-satisfaction">
                  <h4>Satisfaction Snapshot</h4>
                  <div className="pipeline-contract-tags">
                    {satisfactionSummary.map((entry) => (
                      <span key={entry.key} className="pipeline-contract-tag">
                        {entry.key}: {entry.count}
                      </span>
                    ))}
                  </div>
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

              <form
                className="pipeline-transition-form"
                onSubmit={(event) => {
                  void submitTransition(event);
                }}
              >
                <h4>Lifecycle Transition</h4>
                <div className="pipeline-transition-grid">
                  <label>
                    Target state
                    <select
                      value={transitionTarget}
                      onChange={(event) => {
                        setTransitionTarget(event.target.value);
                        if (transitionError) {
                          setTransitionError(null);
                        }
                      }}
                      disabled={availableTransitionTargets.length === 0}
                    >
                      {availableTransitionTargets.length === 0 ? (
                        <option value="">No forward transition available</option>
                      ) : null}
                      {availableTransitionTargets.map((state) => (
                        <option key={state} value={state}>
                          {state}
                        </option>
                      ))}
                    </select>
                  </label>

                  <label>
                    Actor
                    <select
                      value={transitionActor}
                      onChange={(event) => {
                        setTransitionActor(event.target.value);
                        if (transitionError) {
                          setTransitionError(null);
                        }
                      }}
                    >
                      {TRANSITION_ACTOR_OPTIONS.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </label>

                  <label>
                    Transition date
                    <input
                      type="date"
                      value={transitionDate}
                      onChange={(event) => {
                        setTransitionDate(event.target.value);
                        if (transitionError) {
                          setTransitionError(null);
                        }
                      }}
                    />
                  </label>

                  <label>
                    Approval SHA (optional)
                    <input
                      value={transitionApprovalSha}
                      onChange={(event) => {
                        setTransitionApprovalSha(event.target.value);
                        if (transitionError) {
                          setTransitionError(null);
                        }
                      }}
                      placeholder="commit SHA for issuance approvals"
                    />
                  </label>
                </div>

                {transitionError ? <p className="panel-error">{transitionError}</p> : null}

                <div className="pipeline-transition-actions">
                  <button type="submit" disabled={!canSubmitTransition}>
                    {transitionSubmitting ? 'Applying...' : 'Apply Transition'}
                  </button>
                </div>
              </form>
            </>
          )}
        </article>
      </section>
    </AppShell>
  );
}

export default PipelineClient;
