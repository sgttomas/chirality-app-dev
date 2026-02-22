'use client';

import { useSearchParams } from 'next/navigation';
import { AppShell } from '../../components/shell/app-shell';

function normalizeAgent(rawValue: string | null): string {
  if (!rawValue) {
    return 'WORKING_ITEMS';
  }

  return rawValue.trim() || 'WORKING_ITEMS';
}

export function WorkbenchClient(): JSX.Element {
  const searchParams = useSearchParams();
  const agent = normalizeAgent(searchParams.get('agent'));
  const row = searchParams.get('row') ?? 'NORMATIVE';
  const column = searchParams.get('column') ?? 'GUIDING';

  return (
    <AppShell
      section="WORKBENCH"
      title="Persona Session Surface"
      subtitle="Interactive manager-agent workspace for scoped briefs, findings, and operator decisions."
    >
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
        <p>
          WORKBENCH preserves chat-driven orchestration while PIPELINE handles spawned task
          execution. The shell keeps file-tree and chat panels visible for quick cross-checking.
        </p>
      </section>
    </AppShell>
  );
}

export default WorkbenchClient;
