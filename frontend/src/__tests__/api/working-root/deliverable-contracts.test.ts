import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { serializeDependencyRegister } from '../../../lib/dependencies/register-writer';
import { DependencyRegisterRow } from '../../../lib/dependencies/schema';

type RouteModules = {
  statusRoute: typeof import('../../../app/api/working-root/deliverable/status/route');
  transitionRoute: typeof import('../../../app/api/working-root/deliverable/status/transition/route');
  dependenciesRoute: typeof import('../../../app/api/working-root/deliverable/dependencies/route');
};

type FixtureContext = {
  tmpRoot: string;
  projectRoot: string;
  deliverablePath: string;
  statusFilePath: string;
  dependenciesFilePath: string;
};

const INITIAL_STATUS = `# Status: DEL-05-03 Lifecycle State Handling

**Current State:** INITIALIZED
**Last Updated:** 2026-02-22

## History
- 2026-02-21 - State set to OPEN (PREPARATION)
- 2026-02-22 - State set to INITIALIZED (4_DOCUMENTS)
`;

let fixture: FixtureContext;

function makeDependencyRow(
  overrides: Partial<DependencyRegisterRow> = {}
): DependencyRegisterRow {
  return {
    RegisterSchemaVersion: 'v3.1',
    DependencyID: 'DEP-05-03-001',
    FromPackageID: 'PKG-05',
    FromDeliverableID: 'DEL-05-03',
    FromDeliverableName: 'Lifecycle State Handling',
    DependencyClass: 'EXECUTION',
    AnchorType: 'NOT_APPLICABLE',
    Direction: 'UPSTREAM',
    DependencyType: 'PREREQUISITE',
    TargetType: 'DELIVERABLE',
    TargetPackageID: 'PKG-05',
    TargetDeliverableID: 'DEL-05-02',
    TargetRefID: '',
    TargetName: 'Execution Root Scaffolding',
    TargetLocation: '',
    Statement: 'Requires scaffolding baseline before lifecycle transitions',
    EvidenceFile: 'Specification.md',
    SourceRef:
      'execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-03_Lifecycle_State_Handling/Specification.md#REQ-01',
    EvidenceQuote: 'Ensure lifecycle is represented by _STATUS.md.',
    Explicitness: 'EXPLICIT',
    RequiredMaturity: 'IN_PROGRESS',
    ProposedMaturity: 'IN_PROGRESS',
    SatisfactionStatus: 'PENDING',
    Confidence: 'HIGH',
    Origin: 'EXTRACTED',
    FirstSeen: '2026-02-22',
    LastSeen: '2026-02-22',
    Status: 'ACTIVE',
    Notes: '',
    ...overrides
  };
}

async function importRouteModules(): Promise<RouteModules> {
  vi.resetModules();
  const [statusRoute, transitionRoute, dependenciesRoute] = await Promise.all([
    import('../../../app/api/working-root/deliverable/status/route'),
    import('../../../app/api/working-root/deliverable/status/transition/route'),
    import('../../../app/api/working-root/deliverable/dependencies/route')
  ]);
  return { statusRoute, transitionRoute, dependenciesRoute };
}

beforeEach(async () => {
  const tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-working-root-contracts-'));
  const projectRoot = path.join(tmpRoot, 'project-root');
  const deliverablePath = path.join(
    projectRoot,
    'PKG-05_Filesystem_Execution_Model',
    '1_Working',
    'DEL-05-03_Lifecycle_State_Handling'
  );
  const statusFilePath = path.join(deliverablePath, '_STATUS.md');
  const dependenciesFilePath = path.join(deliverablePath, 'Dependencies.csv');

  await mkdir(deliverablePath, { recursive: true });
  await writeFile(statusFilePath, INITIAL_STATUS, 'utf8');

  const initialRegister = serializeDependencyRegister([makeDependencyRow()], {
    hostDeliverableId: 'DEL-05-03'
  });
  await writeFile(dependenciesFilePath, initialRegister.csv, 'utf8');

  fixture = {
    tmpRoot,
    projectRoot,
    deliverablePath,
    statusFilePath,
    dependenciesFilePath
  };
});

afterEach(async () => {
  await rm(fixture.tmpRoot, { recursive: true, force: true });
});

describe('working-root deliverable contract routes', () => {
  it('reads parsed lifecycle state from _STATUS.md', async () => {
    const routes = await importRouteModules();
    const response = await routes.statusRoute.GET(
      new Request(
        `http://localhost/api/working-root/deliverable/status?projectRoot=${encodeURIComponent(fixture.projectRoot)}&deliverablePath=${encodeURIComponent(fixture.deliverablePath)}`
      )
    );

    expect(response.status).toBe(200);
    const body = (await response.json()) as {
      status: { currentState: string };
    };

    expect(body.status.currentState).toBe('INITIALIZED');
  });

  it('applies authorized lifecycle transitions and persists status changes', async () => {
    const routes = await importRouteModules();
    const response = await routes.transitionRoute.POST(
      new Request('http://localhost/api/working-root/deliverable/status/transition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          targetState: 'IN_PROGRESS',
          actor: 'WORKING_ITEMS',
          date: '2026-02-24'
        })
      })
    );

    expect(response.status).toBe(200);
    const body = (await response.json()) as {
      transition: { to: string };
      status: { currentState: string };
    };
    expect(body.transition.to).toBe('IN_PROGRESS');
    expect(body.status.currentState).toBe('IN_PROGRESS');

    const statusFile = await readFile(fixture.statusFilePath, 'utf8');
    expect(statusFile).toContain('**Current State:** IN_PROGRESS');
    expect(statusFile).toContain('- 2026-02-24 - State set to IN_PROGRESS (WORKING_ITEMS)');
  });

  it('rejects unauthorized actor transitions with explicit error typing', async () => {
    const routes = await importRouteModules();
    await routes.transitionRoute.POST(
      new Request('http://localhost/api/working-root/deliverable/status/transition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          targetState: 'IN_PROGRESS',
          actor: 'WORKING_ITEMS',
          date: '2026-02-24'
        })
      })
    );

    const unauthorized = await routes.transitionRoute.POST(
      new Request('http://localhost/api/working-root/deliverable/status/transition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          targetState: 'CHECKING',
          actor: 'WORKING_ITEMS',
          date: '2026-02-25'
        })
      })
    );

    expect(unauthorized.status).toBe(400);
    expect(await unauthorized.json()).toMatchObject({
      error: {
        type: 'UNAUTHORIZED_ACTOR'
      }
    });
  });

  it('requires approvalSha evidence for CHECKING and ISSUED transitions', async () => {
    const routes = await importRouteModules();

    await routes.transitionRoute.POST(
      new Request('http://localhost/api/working-root/deliverable/status/transition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          targetState: 'IN_PROGRESS',
          actor: 'WORKING_ITEMS',
          date: '2026-02-24'
        })
      })
    );

    const missingForChecking = await routes.transitionRoute.POST(
      new Request('http://localhost/api/working-root/deliverable/status/transition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          targetState: 'CHECKING',
          actor: 'HUMAN',
          date: '2026-02-25'
        })
      })
    );

    expect(missingForChecking.status).toBe(400);
    expect(await missingForChecking.json()).toMatchObject({
      error: {
        type: 'APPROVAL_SHA_REQUIRED'
      }
    });

    const toChecking = await routes.transitionRoute.POST(
      new Request('http://localhost/api/working-root/deliverable/status/transition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          targetState: 'CHECKING',
          actor: 'HUMAN',
          date: '2026-02-25',
          approvalSha: 'abc1234'
        })
      })
    );

    expect(toChecking.status).toBe(200);

    const missingForIssued = await routes.transitionRoute.POST(
      new Request('http://localhost/api/working-root/deliverable/status/transition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          targetState: 'ISSUED',
          actor: 'HUMAN',
          date: '2026-02-26'
        })
      })
    );

    expect(missingForIssued.status).toBe(400);
    expect(await missingForIssued.json()).toMatchObject({
      error: {
        type: 'APPROVAL_SHA_REQUIRED'
      }
    });
  });

  it('rejects malformed approvalSha values for human-gated transitions', async () => {
    const routes = await importRouteModules();

    await routes.transitionRoute.POST(
      new Request('http://localhost/api/working-root/deliverable/status/transition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          targetState: 'IN_PROGRESS',
          actor: 'WORKING_ITEMS',
          date: '2026-02-24'
        })
      })
    );

    const malformed = await routes.transitionRoute.POST(
      new Request('http://localhost/api/working-root/deliverable/status/transition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          targetState: 'CHECKING',
          actor: 'HUMAN',
          date: '2026-02-25',
          approvalSha: 'not-a-sha'
        })
      })
    );

    expect(malformed.status).toBe(400);
    expect(await malformed.json()).toMatchObject({
      error: {
        type: 'INVALID_APPROVAL_SHA'
      }
    });
  });

  it('reads dependency register data from Dependencies.csv', async () => {
    const routes = await importRouteModules();
    const response = await routes.dependenciesRoute.GET(
      new Request(
        `http://localhost/api/working-root/deliverable/dependencies?projectRoot=${encodeURIComponent(fixture.projectRoot)}&deliverablePath=${encodeURIComponent(fixture.deliverablePath)}`
      )
    );

    expect(response.status).toBe(200);
    const body = (await response.json()) as {
      rows: DependencyRegisterRow[];
      headers: string[];
    };

    expect(body.rows).toHaveLength(1);
    expect(body.rows[0].DependencyID).toBe('DEP-05-03-001');
    expect(body.headers).toContain('RegisterSchemaVersion');
  });

  it('rejects dependency writes when FromDeliverableID mismatches the host deliverable', async () => {
    const routes = await importRouteModules();
    const response = await routes.dependenciesRoute.PUT(
      new Request('http://localhost/api/working-root/deliverable/dependencies', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          rows: [makeDependencyRow({ FromDeliverableID: 'DEL-99-99' })]
        })
      })
    );

    expect(response.status).toBe(400);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'INVALID_IDENTITY'
      }
    });
  });

  it('rejects invalid SatisfactionStatus jumps against prior register rows', async () => {
    const routes = await importRouteModules();
    const response = await routes.dependenciesRoute.PUT(
      new Request('http://localhost/api/working-root/deliverable/dependencies', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          rows: [makeDependencyRow({ SatisfactionStatus: 'SATISFIED' })]
        })
      })
    );

    expect(response.status).toBe(400);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'INVALID_SATISFACTION_TRANSITION'
      }
    });
  });

  it('writes dependency register rows when transitions are valid', async () => {
    const routes = await importRouteModules();
    const response = await routes.dependenciesRoute.PUT(
      new Request('http://localhost/api/working-root/deliverable/dependencies', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectRoot: fixture.projectRoot,
          deliverablePath: fixture.deliverablePath,
          rows: [makeDependencyRow({ SatisfactionStatus: 'IN_PROGRESS' })]
        })
      })
    );

    expect(response.status).toBe(200);
    const body = (await response.json()) as { rows: DependencyRegisterRow[] };
    expect(body.rows[0].SatisfactionStatus).toBe('IN_PROGRESS');

    const csv = await readFile(fixture.dependenciesFilePath, 'utf8');
    expect(csv).toContain('IN_PROGRESS');
  });
});
