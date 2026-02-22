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

export function getHarnessRuntime(): HarnessRuntime {
  if (!runtimeSingleton) {
    runtimeSingleton = {
      sessionManager: new FileSessionManager(),
      personaManager: new StubPersonaManager(),
      attachmentResolver: new StubAttachmentResolver(),
      agentSdkManager: new StubAgentSdkManager()
    };
  }

  return runtimeSingleton;
}

export function resetHarnessRuntimeForTests(): void {
  runtimeSingleton = undefined;
}
