import { NextResponse } from 'next/server';
import {
  errorResponse,
  readJsonBody,
  requireNonEmptyString
} from '../../../../../lib/harness/http';
import { resolveRuntimeOptions } from '../../../../../lib/harness/options';
import { getHarnessRuntime } from '../../../../../lib/harness/runtime';
import { SessionBootRequest } from '../../../../../lib/harness/types';

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<SessionBootRequest>(request);
    const sessionId = requireNonEmptyString(body.sessionId, 'sessionId');

    const runtime = getHarnessRuntime();
    const session = await runtime.sessionManager.resume(sessionId);
    const resolvedOpts = resolveRuntimeOptions(session, body.opts);

    const bootFingerprint = runtime.personaManager.getBootFingerprint(
      resolvedOpts.persona,
      resolvedOpts.mode
    );

    let claudeSessionId = session.claudeSessionId;

    for await (const event of runtime.agentSdkManager.startTurn(
      session,
      'bootstrap',
      resolvedOpts
    )) {
      if (event.type === 'session:init') {
        claudeSessionId = event.data.claudeSessionId;
      }
      if (event.type === 'process:exit' && event.data.exitCode !== 0) {
        throw new Error('Boot turn failed before completion');
      }
    }

    const bootedAt = new Date().toISOString();
    const updatedSession = await runtime.sessionManager.save(sessionId, {
      claudeSessionId,
      bootFingerprint,
      bootedAt,
      model: resolvedOpts.model
    });

    return NextResponse.json(
      {
        session: updatedSession,
        boot: {
          claudeSessionId,
          bootFingerprint,
          bootedAt
        }
      },
      { status: 200 }
    );
  } catch (error) {
    return errorResponse(error);
  }
}
