import { NextResponse } from 'next/server';
import {
  normalizeProjectRoot,
  workspaceErrorPayload
} from '../../../../lib/workspace/filesystem';

type ValidateRequest = {
  projectRoot: string;
};

export async function POST(request: Request): Promise<Response> {
  try {
    const body = (await request.json()) as ValidateRequest;
    const projectRoot = await normalizeProjectRoot(body.projectRoot);
    return NextResponse.json({ ok: true, projectRoot }, { status: 200 });
  } catch (error) {
    const payload = workspaceErrorPayload(error);
    return NextResponse.json(payload.body, { status: payload.status });
  }
}
