import { NextResponse } from 'next/server';
import { asHarnessError, HarnessError } from './errors';
import { HarnessErrorResponse } from './types';

export async function readJsonBody<T>(request: Request): Promise<T> {
  try {
    return (await request.json()) as T;
  } catch {
    throw new HarnessError('INVALID_REQUEST', 400, 'Request body must be valid JSON');
  }
}

export function requireNonEmptyString(value: unknown, field: string): string {
  if (typeof value !== 'string' || value.trim().length === 0) {
    throw new HarnessError('INVALID_REQUEST', 400, `Missing or invalid '${field}'`);
  }

  return value.trim();
}

export function requireStringArray(value: unknown, field: string): string[] {
  if (!Array.isArray(value) || value.some((item) => typeof item !== 'string')) {
    throw new HarnessError('INVALID_REQUEST', 400, `Field '${field}' must be an array of strings`);
  }

  return value;
}

export function errorResponse(error: unknown): NextResponse<HarnessErrorResponse> {
  const harnessError = asHarnessError(error);
  return NextResponse.json(
    {
      error: {
        type: harnessError.type,
        message: harnessError.message,
        details: harnessError.details
      }
    },
    { status: harnessError.status }
  );
}

export function formatSseEvent(event: string, data: unknown): string {
  return `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
}
