import { NextResponse } from 'next/server';
import {
  errorResponse,
  requireNonEmptyString
} from '../../../../../lib/harness/http';
import { getHarnessRuntime } from '../../../../../lib/harness/runtime';

type RouteContext = {
  params: {
    id: string;
  };
};

export async function GET(_request: Request, context: RouteContext): Promise<Response> {
  try {
    const sessionId = requireNonEmptyString(context.params.id, 'id');
    const runtime = getHarnessRuntime();
    const session = await runtime.sessionManager.getById(sessionId);
    return NextResponse.json({ session }, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}

export async function DELETE(_request: Request, context: RouteContext): Promise<Response> {
  try {
    const sessionId = requireNonEmptyString(context.params.id, 'id');
    const runtime = getHarnessRuntime();
    await runtime.sessionManager.delete(sessionId);
    return NextResponse.json({ ok: true }, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
