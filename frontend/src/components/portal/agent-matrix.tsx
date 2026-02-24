'use client';

import { useEffect, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import { useDeliverables } from '../workspace/deliverables-provider';
import { createNavigationIntentScheduler } from '../../lib/workspace/navigation-intent';

type MatrixCell = {
  row: 'NORMATIVE' | 'OPERATIVE' | 'EVALUATIVE';
  column: 'GUIDING' | 'APPLYING' | 'JUDGING' | 'REVIEWING';
  label: string;
  target: string;
};

const MATRIX_ROWS: Array<{
  rowLabel: MatrixCell['row'];
  cells: MatrixCell[];
}> = [
  {
    rowLabel: 'NORMATIVE',
    cells: [
      {
        row: 'NORMATIVE',
        column: 'GUIDING',
        label: 'HELP',
        target: '/workbench?agent=HELP&row=NORMATIVE&column=GUIDING'
      },
      {
        row: 'NORMATIVE',
        column: 'APPLYING',
        label: 'ORCHESTRATE',
        target: '/workbench?agent=ORCHESTRATE&row=NORMATIVE&column=APPLYING'
      },
      {
        row: 'NORMATIVE',
        column: 'JUDGING',
        label: 'WORKING_ITEMS',
        target: '/workbench?agent=WORKING_ITEMS&row=NORMATIVE&column=JUDGING'
      },
      {
        row: 'NORMATIVE',
        column: 'REVIEWING',
        label: 'AGGREGATE',
        target: '/workbench?agent=AGGREGATE&row=NORMATIVE&column=REVIEWING'
      }
    ]
  },
  {
    rowLabel: 'OPERATIVE',
    cells: [
      {
        row: 'OPERATIVE',
        column: 'GUIDING',
        label: 'DECOMP*',
        target: '/pipeline?category=DECOMP'
      },
      {
        row: 'OPERATIVE',
        column: 'APPLYING',
        label: 'PREP*',
        target: '/pipeline?category=PREP'
      },
      {
        row: 'OPERATIVE',
        column: 'JUDGING',
        label: 'TASK*',
        target: '/pipeline?category=TASK'
      },
      {
        row: 'OPERATIVE',
        column: 'REVIEWING',
        label: 'AUDIT*',
        target: '/pipeline?category=AUDIT'
      }
    ]
  },
  {
    rowLabel: 'EVALUATIVE',
    cells: [
      {
        row: 'EVALUATIVE',
        column: 'GUIDING',
        label: 'AGENTS',
        target: '/workbench?agent=AGENTS&row=EVALUATIVE&column=GUIDING'
      },
      {
        row: 'EVALUATIVE',
        column: 'APPLYING',
        label: 'DEPENDENCIES',
        target: '/workbench?agent=DEPENDENCIES&row=EVALUATIVE&column=APPLYING'
      },
      {
        row: 'EVALUATIVE',
        column: 'JUDGING',
        label: 'CHANGE',
        target: '/workbench?agent=CHANGE&row=EVALUATIVE&column=JUDGING'
      },
      {
        row: 'EVALUATIVE',
        column: 'REVIEWING',
        label: 'RECONCILING',
        target: '/workbench?agent=RECONCILING&row=EVALUATIVE&column=REVIEWING'
      }
    ]
  }
];

export function AgentMatrix(): JSX.Element {
  const router = useRouter();
  const { loading, error, scan } = useDeliverables();
  const navigationScheduler = useMemo(
    () =>
      createNavigationIntentScheduler({
        onNavigate: (target) => {
          router.push(target);
        }
      }),
    [router]
  );

  useEffect(() => {
    return () => {
      navigationScheduler.cancel();
    };
  }, [navigationScheduler]);

  return (
    <section className="portal-matrix">
      <header>
        <h3>Agent Matrix</h3>
        <p>
          Select any cell to open its execution surface. NORMATIVE and EVALUATIVE cells route to
          WORKBENCH. OPERATIVE cells route to PIPELINE categories.
        </p>
      </header>

      <div className="matrix-grid" role="grid" aria-label="Chirality Agent Matrix">
        <div className="matrix-header-cell" />
        <div className="matrix-header-cell">GUIDING</div>
        <div className="matrix-header-cell">APPLYING</div>
        <div className="matrix-header-cell">JUDGING</div>
        <div className="matrix-header-cell">REVIEWING</div>

        {MATRIX_ROWS.map((row) => (
          <div key={row.rowLabel} className="matrix-row-group">
            <div className="matrix-row-label">{row.rowLabel}</div>
            {row.cells.map((cell) => (
              <button
                key={`${cell.row}-${cell.column}`}
                type="button"
                className="matrix-cell"
                onClick={() => {
                  navigationScheduler.schedule(cell.target);
                }}
              >
                <span>{cell.label}</span>
              </button>
            ))}
          </div>
        ))}
      </div>

      <section className="portal-deliverables">
        <header>
          <h4>OPERATIVE Deliverable Rows</h4>
          <p>Select a deliverable row to open PIPELINE `TASK*` with that `pkg::id` pre-selected.</p>
        </header>

        {loading ? (
          <p className="pipeline-note">Loading deliverables from `/api/project/deliverables`...</p>
        ) : error ? (
          <p className="panel-error">{error}</p>
        ) : !scan || scan.deliverables.length === 0 ? (
          <p className="panel-empty">No deliverables found for the selected Working Root.</p>
        ) : (
          <div className="portal-deliverable-grid">
            {scan.deliverables.map((deliverable) => {
              const deliverableKey = deliverable.key;
              return (
                <button
                  key={deliverable.path}
                  type="button"
                  className="portal-deliverable-row"
                  title={deliverable.path}
                  onClick={() => {
                    const params = new URLSearchParams({
                      category: 'TASK',
                      taskScopeMode: 'DELIVERABLES',
                      scopeKey: deliverableKey
                    });
                    navigationScheduler.schedule(`/pipeline?${params.toString()}`);
                  }}
                >
                  <span className="portal-deliverable-key">{deliverableKey}</span>
                  <span className="portal-deliverable-name">{deliverable.name}</span>
                </button>
              );
            })}
          </div>
        )}
      </section>
    </section>
  );
}
