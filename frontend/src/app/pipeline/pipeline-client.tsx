'use client';

import { useSearchParams } from 'next/navigation';
import { useEffect, useMemo, useState } from 'react';
import { AppShell } from '../../components/shell/app-shell';
import { useWorkspace } from '../../components/workspace/workspace-provider';

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
  const [scopeLoading, setScopeLoading] = useState(false);
  const [scopeError, setScopeError] = useState<string | null>(null);
  const [scopeData, setScopeData] = useState<ScopeResponse | null>(null);

  useEffect(() => {
    setSelectedCategory(normalizeCategory(searchParams.get('category')));
  }, [searchParams]);

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
  }, [projectRoot]);

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
      </section>
    </AppShell>
  );
}

export default PipelineClient;
