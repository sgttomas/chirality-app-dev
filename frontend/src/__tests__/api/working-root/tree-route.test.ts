import { mkdtemp, mkdir, rename, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

type TreeNode = {
  path: string;
  children?: TreeNode[];
};

let tmpRoot = '';
let projectRoot = '';

function collectPaths(node: TreeNode): Set<string> {
  const paths = new Set<string>([node.path]);
  for (const child of node.children ?? []) {
    for (const childPath of collectPaths(child)) {
      paths.add(childPath);
    }
  }
  return paths;
}

async function importRouteModule(): Promise<typeof import('../../../app/api/working-root/tree/route')> {
  vi.resetModules();
  return import('../../../app/api/working-root/tree/route');
}

async function requestTree(
  route: typeof import('../../../app/api/working-root/tree/route'),
  rootPath: string
): Promise<{ status: number; body: { root?: TreeNode; error?: { type?: string } } }> {
  const response = await route.GET(
    new Request(
      `http://localhost/api/working-root/tree?projectRoot=${encodeURIComponent(rootPath)}&depth=4`
    )
  );
  return {
    status: response.status,
    body: (await response.json()) as { root?: TreeNode; error?: { type?: string } }
  };
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-working-root-tree-route-'));
  projectRoot = path.join(tmpRoot, 'project-root');
  await mkdir(projectRoot, { recursive: true });
});

afterEach(async () => {
  await rm(tmpRoot, { recursive: true, force: true });
  tmpRoot = '';
  projectRoot = '';
});

describe('GET /api/working-root/tree', () => {
  it('reflects external create, rename, and delete changes across refresh calls', async () => {
    const route = await importRouteModule();
    const alpha = path.join(projectRoot, 'alpha.txt');
    const renamed = path.join(projectRoot, 'alpha-renamed.txt');
    const beta = path.join(projectRoot, 'beta.txt');
    const nestedDir = path.join(projectRoot, 'nested');
    const nestedFile = path.join(nestedDir, 'inside.txt');

    await mkdir(nestedDir, { recursive: true });
    await writeFile(alpha, 'alpha', 'utf8');
    await writeFile(nestedFile, 'inside', 'utf8');

    const first = await requestTree(route, projectRoot);
    expect(first.status).toBe(200);
    const firstPaths = collectPaths(first.body.root as TreeNode);
    expect(firstPaths.has(alpha)).toBe(true);
    expect(firstPaths.has(beta)).toBe(false);
    expect(firstPaths.has(nestedFile)).toBe(true);

    await rename(alpha, renamed);
    await writeFile(beta, 'beta', 'utf8');

    const second = await requestTree(route, projectRoot);
    expect(second.status).toBe(200);
    const secondPaths = collectPaths(second.body.root as TreeNode);
    expect(secondPaths.has(alpha)).toBe(false);
    expect(secondPaths.has(renamed)).toBe(true);
    expect(secondPaths.has(beta)).toBe(true);

    await rm(beta);
    const third = await requestTree(route, projectRoot);
    expect(third.status).toBe(200);
    const thirdPaths = collectPaths(third.body.root as TreeNode);
    expect(thirdPaths.has(beta)).toBe(false);
    expect(thirdPaths.has(renamed)).toBe(true);
  });

  it('returns typed accessibility errors for missing roots', async () => {
    const route = await importRouteModule();
    const response = await requestTree(route, path.join(projectRoot, 'missing-root'));

    expect(response.status).toBe(404);
    expect(response.body).toMatchObject({
      error: {
        type: 'WORKING_ROOT_INACCESSIBLE'
      }
    });
  });
});
