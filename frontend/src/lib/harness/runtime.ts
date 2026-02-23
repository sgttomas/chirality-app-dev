import { AnthropicAgentSdkManager } from './anthropic-agent-sdk-manager';
import { StubAgentSdkManager } from './agent-sdk-manager';
import { StubAttachmentResolver } from './attachment-resolver';
import { StubPersonaManager } from './persona-manager';
import { FileSessionManager } from './session-manager';
import { IAgentSdkManager, IAttachmentResolver, IPersonaManager, ISessionManager } from './types';

type HarnessRuntime = {
  sessionManager: ISessionManager;
  personaManager: IPersonaManager;
  attachmentResolver: IAttachmentResolver;
  agentSdkManager: IAgentSdkManager;
};

let runtimeSingleton: HarnessRuntime | undefined;

export type HarnessProviderMode = 'stub' | 'anthropic';

function asNonEmptyString(value: string | undefined): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

export function resolveHarnessProviderMode(env: NodeJS.ProcessEnv = process.env): HarnessProviderMode {
  const raw = asNonEmptyString(env.CHIRALITY_HARNESS_PROVIDER)?.toLowerCase();
  return raw === 'anthropic' ? 'anthropic' : 'stub';
}

function buildAgentSdkManager(mode: HarnessProviderMode): IAgentSdkManager {
  if (mode === 'anthropic') {
    return new AnthropicAgentSdkManager();
  }
  return new StubAgentSdkManager();
}

export function getHarnessRuntime(): HarnessRuntime {
  if (!runtimeSingleton) {
    const providerMode = resolveHarnessProviderMode();
    runtimeSingleton = {
      sessionManager: new FileSessionManager(),
      personaManager: new StubPersonaManager(),
      attachmentResolver: new StubAttachmentResolver(),
      agentSdkManager: buildAgentSdkManager(providerMode)
    };
  }

  return runtimeSingleton;
}

export function resetHarnessRuntimeForTests(): void {
  runtimeSingleton = undefined;
}
