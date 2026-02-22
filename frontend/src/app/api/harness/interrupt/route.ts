import { NextResponse } from 'next/server';
import {
  errorResponse,
  readJsonBody,
  requireNonEmptyString
} from '../../../../lib/harness/http';
import { getHarnessRuntime } from '../../../../lib/harness/runtime';
import { InterruptRequest } from '../../../../lib/harness/types';

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<InterruptRequest>(request);
    const sessionId = requireNonEmptyString(body.sessionId, 'sessionId');

    const runtime = getHarnessRuntime();
    await runtime.agentSdkManager.interrupt(sessionId);

    return NextResponse.json({ ok: true }, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
