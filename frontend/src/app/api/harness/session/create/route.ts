import { NextResponse } from 'next/server';
import {
  errorResponse,
  readJsonBody,
  requireNonEmptyString
} from '../../../../../lib/harness/http';
import { getHarnessRuntime } from '../../../../../lib/harness/runtime';
import { SessionCreateRequest } from '../../../../../lib/harness/types';

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<SessionCreateRequest>(request);
    const projectRoot = requireNonEmptyString(body.projectRoot, 'projectRoot');

    const runtime = getHarnessRuntime();
    const session = await runtime.sessionManager.create({
      projectRoot,
      persona: body.persona,
      mode: body.mode
    });

    return NextResponse.json({ session }, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
