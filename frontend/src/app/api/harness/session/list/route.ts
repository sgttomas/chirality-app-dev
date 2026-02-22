import { NextResponse } from 'next/server';
import {
  errorResponse,
  requireNonEmptyString
} from '../../../../../lib/harness/http';
import { getHarnessRuntime } from '../../../../../lib/harness/runtime';

export async function GET(request: Request): Promise<Response> {
  try {
    const url = new URL(request.url);
    const projectRoot = requireNonEmptyString(url.searchParams.get('projectRoot'), 'projectRoot');

    const runtime = getHarnessRuntime();
    const sessions = await runtime.sessionManager.list(projectRoot);

    return NextResponse.json({ sessions }, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
