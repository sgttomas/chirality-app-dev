import { describe, expect, it } from 'vitest';
import { HarnessApiClientError } from '../../lib/harness/client';
import { toHarnessUiError } from '../../lib/harness/error-display';

describe('harness ui error mapping', () => {
  it('maps known typed errors to actionable copy', () => {
    const input = new HarnessApiClientError(
      404,
      'WORKING_ROOT_INACCESSIBLE',
      'projectRoot is not accessible'
    );

    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('Working Root Unavailable');
    expect(mapped.code).toBe('WORKING_ROOT_INACCESSIBLE');
    expect(mapped.nextStep).toContain('Re-select');
  });

  it('falls back to generic copy for unknown codes', () => {
    const input = new HarnessApiClientError(500, 'SOMETHING_NEW', 'Unexpected backend path');
    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('Harness Request Failed');
    expect(mapped.message).toContain('SOMETHING_NEW');
  });

  it('returns unexpected copy for non-client errors', () => {
    const mapped = toHarnessUiError(new Error('boom'));
    expect(mapped.title).toBe('Unexpected Harness Failure');
    expect(mapped.message).toContain('boom');
  });
});
