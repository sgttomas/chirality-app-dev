import { HarnessErrorType } from './types';

export class HarnessError extends Error {
  readonly type: HarnessErrorType;
  readonly status: number;
  readonly details?: unknown;

  constructor(type: HarnessErrorType, status: number, message: string, details?: unknown) {
    super(message);
    this.name = 'HarnessError';
    this.type = type;
    this.status = status;
    this.details = details;
  }
}

export function asHarnessError(error: unknown): HarnessError {
  if (error instanceof HarnessError) {
    return error;
  }

  if (error instanceof Error) {
    return new HarnessError('SDK_FAILURE', 500, error.message);
  }

  return new HarnessError('SDK_FAILURE', 500, 'Unexpected harness runtime error');
}
