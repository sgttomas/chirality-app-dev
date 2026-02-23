import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

const PACKAGE_JSON_PATH = path.resolve(process.cwd(), 'package.json');

type BuildTarget = string | { target?: string; arch?: string[] };

type ExtraResource = {
  from?: string;
  to?: string;
  filter?: string[];
};

type FrontendPackageJson = {
  scripts?: Record<string, string>;
  build?: {
    mac?: {
      minimumSystemVersion?: string;
      target?: BuildTarget[];
    };
    extraResources?: ExtraResource[];
  };
};

async function readPackageJson(): Promise<FrontendPackageJson> {
  const raw = await readFile(PACKAGE_JSON_PATH, 'utf8');
  return JSON.parse(raw) as FrontendPackageJson;
}

function parseMajor(version: string): number {
  const [majorToken] = version.split('.');
  return Number.parseInt(majorToken, 10);
}

describe('dmg packaging policy', () => {
  it('forces unsigned packaging in desktop build scripts', async () => {
    const pkg = await readPackageJson();
    const pack = pkg.scripts?.['desktop:pack'] ?? '';
    const dist = pkg.scripts?.['desktop:dist'] ?? '';

    expect(pack).toContain('CSC_IDENTITY_AUTO_DISCOVERY=false');
    expect(dist).toContain('CSC_IDENTITY_AUTO_DISCOVERY=false');
  });

  it('pins macOS minimum version and arm64 dmg target', async () => {
    const pkg = await readPackageJson();
    const minimumSystemVersion = pkg.build?.mac?.minimumSystemVersion ?? '';
    const targetEntries = pkg.build?.mac?.target ?? [];

    expect(minimumSystemVersion).not.toBe('');
    expect(parseMajor(minimumSystemVersion)).toBeGreaterThanOrEqual(15);

    const hasArm64DmgTarget = targetEntries.some((entry) => {
      if (typeof entry === 'string') {
        return entry === 'dmg';
      }

      if (entry.target !== 'dmg') {
        return false;
      }

      return (entry.arch ?? []).includes('arm64');
    });

    expect(hasArm64DmgTarget).toBe(true);
  });

  it('bundles instruction-root resources into packaged artifacts', async () => {
    const pkg = await readPackageJson();
    const resources = pkg.build?.extraResources ?? [];

    expect(resources).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          from: '../agents',
          to: 'agents'
        }),
        expect.objectContaining({
          from: '../docs',
          to: 'docs'
        })
      ])
    );
  });
});
