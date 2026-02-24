import { NextResponse } from 'next/server';
import { asHarnessError, HarnessError } from '../../../../lib/harness/errors';
import {
  errorResponse,
  formatSseEvent,
  readJsonBody,
  requireNonEmptyString,
  requireStringArray
} from '../../../../lib/harness/http';
import { resolveRuntimeOptions } from '../../../../lib/harness/options';
import { getHarnessRuntime } from '../../../../lib/harness/runtime';
import { evaluateSubagentGovernance } from '../../../../lib/harness/subagent-governance';
import { AttachmentError, ContentBlock, TurnRequest } from '../../../../lib/harness/types';

const MAX_ATTACHMENT_WARNING_DETAILS = 3;
const activeSessionTurns = new Set<string>();

function buildAttachmentWarningText(errors: AttachmentError[]): string | undefined {
  if (errors.length === 0) {
    return undefined;
  }

  const lines = errors
    .slice(0, MAX_ATTACHMENT_WARNING_DETAILS)
    .map((error) => `- ${error.path}: ${error.reason}`);
  const remaining = errors.length - lines.length;
  if (remaining > 0) {
    lines.push(`- ... ${remaining} additional attachment error(s) omitted`);
  }

  return [
    'Attachment warning: one or more attachments could not be processed. Continue with available content.',
    ...lines
  ].join('\n');
}

export async function POST(request: Request): Promise<Response> {
  let lockedSessionId: string | undefined;
  let turnLockHeld = false;

  try {
    const body = await readJsonBody<TurnRequest>(request);
    const sessionId = requireNonEmptyString(body.sessionId, 'sessionId');
    lockedSessionId = sessionId;

    if (typeof body.message !== 'string') {
      throw new HarnessError('INVALID_REQUEST', 400, "Missing or invalid 'message'");
    }

    const attachments =
      body.attachments === undefined ? [] : requireStringArray(body.attachments, 'attachments');

    const runtime = getHarnessRuntime();
    const session = await runtime.sessionManager.resume(sessionId);
    if (activeSessionTurns.has(sessionId)) {
      throw new HarnessError(
        'INVALID_REQUEST',
        409,
        'A turn is already in progress for this session',
        { sessionId }
      );
    }
    activeSessionTurns.add(sessionId);
    turnLockHeld = true;

    const resolvedOpts = await resolveRuntimeOptions(session, body.opts);

    const attachmentResolution = await runtime.attachmentResolver.resolveAttachmentsToContentBlocks(
      body.message,
      attachments
    );

    const warningText = buildAttachmentWarningText(attachmentResolution.errors);
    const contentBlocks: ContentBlock[] = warningText
      ? [{ type: 'text', text: warningText }, ...attachmentResolution.contentBlocks]
      : attachmentResolution.contentBlocks;
    const text = body.message.trim();
    const hasExecutableAttachment = contentBlocks.some((block) => block.type === 'file');

    if (!text && !hasExecutableAttachment) {
      throw new HarnessError(
        'ATTACHMENT_FAILURE',
        400,
        'Turn requires text content or at least one valid attachment',
        { attachmentErrors: attachmentResolution.errors }
      );
    }

    await runtime.personaManager.buildSystemPrompt(
      session.projectRoot,
      resolvedOpts.persona,
      resolvedOpts.mode
    );

    const governanceDecision = await evaluateSubagentGovernance(
      resolvedOpts.persona,
      resolvedOpts.subagentGovernance
    );
    const effectiveOpts = governanceDecision.allowed
      ? {
          ...resolvedOpts,
          delegatedSubagents: governanceDecision.delegatedSubagents
        }
      : {
          ...resolvedOpts,
          delegatedSubagents: []
        };

    const encoder = new TextEncoder();
    let released = false;
    const releaseTurnLock = (): void => {
      if (released) {
        return;
      }
      released = true;
      activeSessionTurns.delete(sessionId);
    };

    const stream = new ReadableStream<Uint8Array>({
      async start(controller): Promise<void> {
        try {
          for await (const event of runtime.agentSdkManager.startTurn(
            session,
            body.message,
            effectiveOpts,
            contentBlocks
          )) {
            if (event.type === 'session:init') {
              await runtime.sessionManager.save(sessionId, {
                claudeSessionId: event.data.claudeSessionId,
                model: event.data.model
              });
            }

            controller.enqueue(encoder.encode(formatSseEvent(event.type, event.data)));
          }
        } catch (error) {
          const harnessError = asHarnessError(error);
          controller.enqueue(
            encoder.encode(
              formatSseEvent('process:exit', {
                exitCode: 1,
                interrupted: false,
                error: harnessError.message,
                errorType: harnessError.type,
                status: harnessError.status,
                errorDetails: harnessError.details
              })
            )
          );
        } finally {
          releaseTurnLock();
          try {
            controller.close();
          } catch {
            // Stream may already be closed/cancelled.
          }
        }
      },
      async cancel(): Promise<void> {
        try {
          await runtime.agentSdkManager.interrupt(sessionId);
        } catch {
          // Best-effort cleanup only.
        } finally {
          releaseTurnLock();
        }
      }
    });
    turnLockHeld = false;

    return new Response(stream, {
      status: 200,
      headers: {
        'Content-Type': 'text/event-stream; charset=utf-8',
        'Cache-Control': 'no-cache, no-transform',
        Connection: 'keep-alive'
      }
    });
  } catch (error) {
    if (turnLockHeld && lockedSessionId) {
      activeSessionTurns.delete(lockedSessionId);
    }
    return errorResponse(error);
  }
}
