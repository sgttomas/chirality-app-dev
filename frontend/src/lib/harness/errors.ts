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

function isHarnessErrorType(value: unknown): value is HarnessErrorType {
  return (
    value === 'INVALID_REQUEST' ||
    value === 'TURN_IN_PROGRESS' ||
    value === 'MISSING_API_KEY' ||
    value === 'PERSONA_NOT_FOUND' ||
    value === 'INSTRUCTION_ROOT_INVALID' ||
    value === 'SDK_FAILURE' ||
    value === 'SESSION_NOT_FOUND' ||
    value === 'WORKING_ROOT_INACCESSIBLE' ||
    value === 'WORKING_ROOT_CONFLICT' ||
    value === 'ATTACHMENT_FAILURE'
  );
}

function isHarnessErrorLike(
  error: unknown
): error is {
  type: HarnessErrorType;
  status: number;
  message: string;
  details?: unknown;
} {
  if (!error || typeof error !== 'object') {
    return false;
  }

  const candidate = error as {
    type?: unknown;
    status?: unknown;
    message?: unknown;
    details?: unknown;
  };

  return (
    isHarnessErrorType(candidate.type) &&
    typeof candidate.status === 'number' &&
    Number.isFinite(candidate.status) &&
    typeof candidate.message === 'string'
  );
}

export function asHarnessError(error: unknown): HarnessError {
  if (error instanceof HarnessError) {
    return error;
  }

  if (isHarnessErrorLike(error)) {
    return new HarnessError(error.type, error.status, error.message, error.details);
  }

  if (error instanceof Error) {
    return new HarnessError('SDK_FAILURE', 500, error.message);
  }

  return new HarnessError('SDK_FAILURE', 500, 'Unexpected harness runtime error');
}
