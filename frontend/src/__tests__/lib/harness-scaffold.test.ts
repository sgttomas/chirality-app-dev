import { mkdtemp, readFile, rm, stat, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { scaffoldExecutionRoot } from '../../lib/harness/scaffold';

const DECOMPOSITION_FIXTURE = `# Example System - Software Decomposition

## Packages (work-domain partitions)

| PackageID | Package Name | Description |
|---|---|---|
| PKG-01 | Build & Packaging | Build outputs |
| PKG-02 | UI : Shell | UI workflow |

## Deliverables

### PKG-01 - Build & Packaging

| DeliverableID | Name | Type |
|---|---|---|
| DEL-01-01 | DMG Build: Baseline | CI_CD_CHANGE |
| DEL-01-02 | Bundle / Integrity | CI_CD_CHANGE |

### PKG-02 - UI : Shell

| DeliverableID | Name | Type |
|---|---|---|
| DEL-02-01 | Portal   Layout | UX_UI_SLICE |
`;

let tmpDir = '';

afterEach(async () => {
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('scaffoldExecutionRoot', () => {
  it('creates execution-root layout, package folders, and deliverable folders from decomposition', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-test-'));
    const executionRoot = path.join(tmpDir, 'execution');
    const decompositionPath = path.join(tmpDir, 'decomposition.md');
    await writeFile(decompositionPath, DECOMPOSITION_FIXTURE, 'utf8');

    const result = await scaffoldExecutionRoot({
      executionRoot,
      decompositionPath,
      coordinationMode: 'HYBRID'
    });

    expect(result.projectName).toBe('Example System');
    expect(result.packageCount).toBe(2);
    expect(result.deliverableCount).toBe(3);
    expect(result.layoutValidation.valid).toBe(true);
    expect(result.layoutValidation.executionRoot.valid).toBe(true);

    await expect(stat(path.join(executionRoot, '_Aggregation', '_Templates'))).resolves.toBeDefined();
    await expect(stat(path.join(executionRoot, '_Decomposition', path.basename(decompositionPath)))).resolves.toBeDefined();
    await expect(stat(path.join(executionRoot, '_Coordination', '_COORDINATION.md'))).resolves.toBeDefined();

    await expect(
      stat(path.join(executionRoot, 'PKG-01_Build & Packaging', '1_Working', 'DEL-01-01_DMG Build- Baseline'))
    ).resolves.toBeDefined();
    await expect(
      stat(path.join(executionRoot, 'PKG-01_Build & Packaging', '1_Working', 'DEL-01-02_Bundle - Integrity'))
    ).resolves.toBeDefined();
    await expect(
      stat(path.join(executionRoot, 'PKG-02_UI - Shell', '1_Working', 'DEL-02-01_Portal Layout'))
    ).resolves.toBeDefined();

    const coordination = await readFile(path.join(executionRoot, '_Coordination', '_COORDINATION.md'), 'utf8');
    expect(coordination).toContain('**Representation:** HYBRID');
  });

  it('is idempotent and does not overwrite existing files on rerun', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-idempotent-'));
    const executionRoot = path.join(tmpDir, 'execution');
    const decompositionPath = path.join(tmpDir, 'decomposition.md');
    await writeFile(decompositionPath, DECOMPOSITION_FIXTURE, 'utf8');

    await scaffoldExecutionRoot({
      executionRoot,
      decompositionPath
    });

    const initPath = path.join(executionRoot, 'INIT.md');
    const customFile = path.join(
      executionRoot,
      'PKG-01_Build & Packaging',
      '1_Working',
      'DEL-01-01_DMG Build- Baseline',
      'custom.txt'
    );

    await writeFile(initPath, '# custom-init\n', 'utf8');
    await writeFile(customFile, 'custom-content\n', 'utf8');

    const rerun = await scaffoldExecutionRoot({
      executionRoot,
      decompositionPath
    });

    expect(rerun.created.files).toHaveLength(0);
    expect(rerun.created.directories).toHaveLength(0);

    const initContent = await readFile(initPath, 'utf8');
    const customContent = await readFile(customFile, 'utf8');
    expect(initContent).toBe('# custom-init\n');
    expect(customContent).toBe('custom-content\n');
    expect(rerun.layoutValidation.valid).toBe(true);
  });

  it('rejects malformed decomposition input without deliverable rows', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-malformed-'));
    const executionRoot = path.join(tmpDir, 'execution');
    const decompositionPath = path.join(tmpDir, 'bad-decomposition.md');
    await writeFile(
      decompositionPath,
      `# Bad Decomposition

| PackageID | Package Name |
|---|---|
| PKG-01 | Build |
`,
      'utf8'
    );

    await expect(
      scaffoldExecutionRoot({
        executionRoot,
        decompositionPath
      })
    ).rejects.toMatchObject({
      type: 'INVALID_REQUEST'
    });
  });
});
