'use client';

import { useRouter } from 'next/navigation';

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
                  router.push(cell.target);
                }}
              >
                <span>{cell.label}</span>
              </button>
            ))}
          </div>
        ))}
      </div>
    </section>
  );
}
