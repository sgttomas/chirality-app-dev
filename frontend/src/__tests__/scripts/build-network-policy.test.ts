import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

const PACKAGE_JSON_PATH = path.resolve(process.cwd(), 'package.json');
const ELECTRON_MAIN_PATH = path.resolve(process.cwd(), 'electron', 'main.ts');

type FrontendPackageJson = {
  scripts?: Record<string, string>;
};

async function readPackageJson(): Promise<FrontendPackageJson> {
  const raw = await readFile(PACKAGE_JSON_PATH, 'utf8');
  return JSON.parse(raw) as FrontendPackageJson;
}

describe('build network policy hardening', () => {
  it('disables Next telemetry in development and build scripts', async () => {
    const pkg = await readPackageJson();
    const devNext = pkg.scripts?.['dev:next'] ?? '';
    const build = pkg.scripts?.build ?? '';

    expect(devNext).toContain('NEXT_TELEMETRY_DISABLED=1');
    expect(build).toContain('NEXT_TELEMETRY_DISABLED=1');
  });

  it('does not include Electron auto-updater or GitHub release checks in main process', async () => {
    const mainSource = await readFile(ELECTRON_MAIN_PATH, 'utf8');

    expect(mainSource).not.toMatch(/\bautoUpdater\b/);
    expect(mainSource).not.toContain('releases/latest');
    expect(mainSource).not.toContain('api.github.com/repos');
  });

  it('enforces renderer egress allowlist interception with fail-closed diagnostics', async () => {
    const mainSource = await readFile(ELECTRON_MAIN_PATH, 'utf8');

    expect(mainSource).toContain('session.webRequest.onBeforeRequest');
    expect(mainSource).toContain("RUNTIME_NETWORK_POLICY_ID = 'REQ-NET-001'");
    expect(mainSource).toContain("'NETWORK_POLICY_VIOLATION'");
    expect(mainSource).toContain("'INVALID_URL'");
    expect(mainSource).toContain("['http://*/*', 'https://*/*', 'ws://*/*', 'wss://*/*']");
    expect(mainSource).toContain("'api.anthropic.com'");
    expect(mainSource).toContain("'localhost'");
    expect(mainSource).toContain("'127.0.0.1'");
    expect(mainSource).toContain("'[::1]'");
    expect(mainSource).toContain('Blocked renderer outbound request by network policy');
  });
});
