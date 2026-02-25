import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

type RouteModule = typeof import('../../../app/api/project/deliverables/route');

type RouteBody = {
  projectRoot?: string;
  deliverables?: Array<{
    id: string;
    name: string;
    pkg: string;
    status: string;
    path: string;
  }>;
  knowledgeDecomposition?: {
    enabled: boolean;
    markerFile: string | null;
  };
  knowledgeTypes?: Array<{
    id: string;
    label: string;
    matchingDeliverableKeys: string[];
  }>;
  error?: {
    type?: string;
    message?: string;
  };
};

let tmpRoot = '';
let projectRoot = '';

function statusDocument(state: string): string {
  return `# Status — Example

**Current State:** ${state}
**Last Updated:** 2026-02-24

## History
- 2026-02-24 - State set to ${state} (WORKING_ITEMS)
`;
}

async function createDeliverable(
  pkgFolder: string,
  deliverableFolder: string,
  state: string,
  files: string[]
): Promise<string> {
  const deliverablePath = path.join(projectRoot, pkgFolder, '1_Working', deliverableFolder);
  await mkdir(deliverablePath, { recursive: true });
  await writeFile(path.join(deliverablePath, '_STATUS.md'), statusDocument(state), 'utf8');

  for (const fileName of files) {
    await writeFile(path.join(deliverablePath, fileName), `${fileName} content`, 'utf8');
  }

  return deliverablePath;
}

async function importRouteModule(): Promise<RouteModule> {
  vi.resetModules();
  return import('../../../app/api/project/deliverables/route');
}

async function requestDeliverables(rootPath: string): Promise<{ status: number; body: RouteBody }> {
  const route = await importRouteModule();
  const response = await route.GET(
    new Request(
      `http://localhost/api/project/deliverables?projectRoot=${encodeURIComponent(rootPath)}`
    )
  );

  return {
    status: response.status,
    body: (await response.json()) as RouteBody
  };
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-project-deliverables-route-'));
  projectRoot = path.join(tmpRoot, 'project-root');
  await mkdir(projectRoot, { recursive: true });
});

afterEach(async () => {
  await rm(tmpRoot, { recursive: true, force: true });
  tmpRoot = '';
  projectRoot = '';
});

describe('GET /api/project/deliverables', () => {
  it('returns deliverables, knowledge marker metadata, and knowledge type mappings', async () => {
    const deliverablePath = await createDeliverable(
      'PKG-02_Desktop_UI_Workflow',
      'DEL-02-02_Portal_Pipeline_Navigation',
      'IN_PROGRESS',
      ['Datasheet.md', 'Specification.md', 'MEMORY.md']
    );

    const decompositionPath = path.join(projectRoot, '_Decomposition');
    await mkdir(decompositionPath, { recursive: true });
    await writeFile(
      path.join(decompositionPath, 'Domain_Handbook.md'),
      '# Knowledge Types\n\nKnowledge Categories and Knowledge Types are defined here.',
      'utf8'
    );

    const response = await requestDeliverables(projectRoot);

    expect(response.status).toBe(200);
    expect(response.body.projectRoot).toBe(projectRoot);
    expect(response.body.deliverables).toEqual([
      {
        id: 'DEL-02-02',
        name: 'Portal Pipeline Navigation',
        pkg: 'PKG-02_Desktop_UI_Workflow',
        status: 'in_progress',
        path: deliverablePath
      }
    ]);
    expect(response.body.knowledgeDecomposition).toEqual({
      enabled: true,
      markerFile: path.join(projectRoot, '_Decomposition', 'Domain_Handbook.md')
    });
    expect(response.body.knowledgeTypes).toEqual(
      expect.arrayContaining([
        {
          id: 'datasheet',
          label: 'Datasheet',
          matchingDeliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02']
        },
        {
          id: 'specification',
          label: 'Specification',
          matchingDeliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02']
        },
        {
          id: 'memory',
          label: 'Memory',
          matchingDeliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02']
        }
      ])
    );
  });

  it('returns marker disabled when no decomposition marker is present', async () => {
    await createDeliverable(
      'PKG-06_Agent_Suite_Governance',
      'DEL-06-03_Cross_Deliverable_Workflows',
      'SEMANTIC_READY',
      ['Guidance.md']
    );

    const decompositionPath = path.join(projectRoot, '_Decomposition');
    await mkdir(decompositionPath, { recursive: true });
    await writeFile(
      path.join(decompositionPath, 'ChiralityApp_SoftwareDecomposition.md'),
      '# Software Decomposition\n\nNo domain marker text.',
      'utf8'
    );

    const response = await requestDeliverables(projectRoot);
    expect(response.status).toBe(200);
    expect(response.body.knowledgeDecomposition).toEqual({
      enabled: false,
      markerFile: null
    });
  });

  it('returns typed accessibility failures for missing project roots', async () => {
    const response = await requestDeliverables(path.join(projectRoot, 'missing-root'));
    expect(response.status).toBe(404);
    expect(response.body).toMatchObject({
      error: {
        type: 'WORKING_ROOT_INACCESSIBLE'
      }
    });
  });
});
