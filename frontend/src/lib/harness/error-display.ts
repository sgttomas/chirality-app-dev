import { HarnessApiClientError, harnessApiErrorMessage } from './client';
import type { HarnessErrorType } from './types';

export type HarnessUiError = {
  title: string;
  message: string;
  nextStep: string;
  code?: string;
};

const ERROR_COPY: Partial<Record<HarnessErrorType, Omit<HarnessUiError, 'code'>>> = {
  WORKING_ROOT_INACCESSIBLE: {
    title: 'Working Root Unavailable',
    message: 'The selected projectRoot is missing or inaccessible.',
    nextStep: 'Re-select a valid Working Root, then retry.'
  },
  WORKING_ROOT_CONFLICT: {
    title: 'Working Root Conflicts With Instruction Root',
    message: 'The selected projectRoot overlaps the bundled instruction root.',
    nextStep: 'Choose a separate execution directory outside instruction-root paths.'
  },
  INSTRUCTION_ROOT_INVALID: {
    title: 'Instruction Root Invalid',
    message: 'Required instruction files are missing or unreadable.',
    nextStep: 'Reinstall or rebuild the app bundle and verify instruction resources.'
  },
  PERSONA_NOT_FOUND: {
    title: 'Persona Not Found',
    message: 'The selected agent persona could not be resolved from instruction root.',
    nextStep: 'Choose a valid WORKBENCH agent or verify instruction-root agent files.'
  },
  SDK_FAILURE: {
    title: 'Runtime Bootstrap Failed',
    message: 'The harness runtime failed while booting or running the turn.',
    nextStep: 'Retry once. If it persists, inspect runtime logs and boot configuration.'
  },
  SESSION_NOT_FOUND: {
    title: 'Session Not Found',
    message: 'The active harness session no longer exists.',
    nextStep: 'Start a new session and send the prompt again.'
  },
  ATTACHMENT_FAILURE: {
    title: 'Attachment Validation Failed',
    message: 'No executable attachment content was available for this turn.',
    nextStep: 'Attach readable files or include non-empty text content.'
  },
  INVALID_REQUEST: {
    title: 'Invalid Request',
    message: 'The request payload failed server-side validation.',
    nextStep: 'Check required fields and retry.'
  }
};

export function toHarnessUiError(error: unknown): HarnessUiError {
  if (error instanceof HarnessApiClientError) {
    const copy = ERROR_COPY[error.code as HarnessErrorType];
    if (copy) {
      return {
        ...copy,
        code: error.code
      };
    }

    return {
      title: 'Harness Request Failed',
      message: `${error.code}: ${error.message}`,
      nextStep: 'Review the request context and retry.',
      code: error.code
    };
  }

  return {
    title: 'Unexpected Harness Failure',
    message: harnessApiErrorMessage(error),
    nextStep: 'Retry once and inspect frontend console/runtime logs if the issue persists.'
  };
}
