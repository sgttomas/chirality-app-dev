import { afterEach, describe, expect, it } from 'vitest';
import { AnthropicAgentSdkManager } from '../../lib/harness/anthropic-agent-sdk-manager';
import {
  getHarnessRuntime,
  resetHarnessRuntimeForTests,
  resolveHarnessProviderMode
} from '../../lib/harness/runtime';
import { StubAgentSdkManager } from '../../lib/harness/agent-sdk-manager';

afterEach(() => {
  delete process.env.CHIRALITY_HARNESS_PROVIDER;
  resetHarnessRuntimeForTests();
});

describe('harness runtime provider mode', () => {
  it('defaults to stub provider mode when env is unset', () => {
    expect(resolveHarnessProviderMode()).toBe('stub');
    const runtime = getHarnessRuntime();
    expect(runtime.agentSdkManager).toBeInstanceOf(StubAgentSdkManager);
  });

  it('selects anthropic provider mode when explicitly configured', () => {
    process.env.CHIRALITY_HARNESS_PROVIDER = 'anthropic';

    expect(resolveHarnessProviderMode()).toBe('anthropic');
    const runtime = getHarnessRuntime();
    expect(runtime.agentSdkManager).toBeInstanceOf(AnthropicAgentSdkManager);
  });
});
