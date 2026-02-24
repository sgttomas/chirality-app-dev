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

  it('maps TURN_IN_PROGRESS to retry guidance', () => {
    const input = new HarnessApiClientError(409, 'TURN_IN_PROGRESS', 'A turn is already active');
    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('Turn Already In Progress');
    expect(mapped.code).toBe('TURN_IN_PROGRESS');
    expect(mapped.nextStep).toContain('Wait for the current turn');
  });

  it('maps MISSING_API_KEY to provisioning guidance', () => {
    const input = new HarnessApiClientError(
      503,
      'MISSING_API_KEY',
      'Anthropic API key is not configured'
    );
    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('API Key Not Configured');
    expect(mapped.code).toBe('MISSING_API_KEY');
    expect(mapped.nextStep).toContain('ANTHROPIC_API_KEY');
  });

  it('falls back to generic copy for unknown codes', () => {
    const input = new HarnessApiClientError(500, 'SOMETHING_NEW', 'Unexpected backend path');
    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('Harness Request Failed');
    expect(mapped.message).toContain('SOMETHING_NEW');
  });

  it('maps instruction-root failures to recovery guidance', () => {
    const input = new HarnessApiClientError(
      500,
      'INSTRUCTION_ROOT_INVALID',
      'Instruction root is missing required resources'
    );

    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('Instruction Root Invalid');
    expect(mapped.code).toBe('INSTRUCTION_ROOT_INVALID');
    expect(mapped.nextStep).toContain('Reinstall');
  });

  it('returns unexpected copy for non-client errors', () => {
    const mapped = toHarnessUiError(new Error('boom'));
    expect(mapped.title).toBe('Unexpected Harness Failure');
    expect(mapped.message).toContain('boom');
  });
});
