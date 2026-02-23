import { NextResponse } from 'next/server';
import { errorResponse, readJsonBody, requireNonEmptyString } from '../../../../lib/harness/http';
import { CoordinationMode, scaffoldExecutionRoot } from '../../../../lib/harness/scaffold';

type ScaffoldRequest = {
  executionRoot: string;
  decompositionPath: string;
  projectName?: string;
  coordinationMode?: CoordinationMode;
};

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<ScaffoldRequest>(request);
    const result = await scaffoldExecutionRoot({
      executionRoot: requireNonEmptyString(body.executionRoot, 'executionRoot'),
      decompositionPath: requireNonEmptyString(body.decompositionPath, 'decompositionPath'),
      projectName: body.projectName?.trim(),
      coordinationMode: body.coordinationMode
    });

    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
