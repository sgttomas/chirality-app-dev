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
import { ContentBlock, TurnRequest } from '../../../../lib/harness/types';

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<TurnRequest>(request);
    const sessionId = requireNonEmptyString(body.sessionId, 'sessionId');

    if (typeof body.message !== 'string') {
      throw new HarnessError('INVALID_REQUEST', 400, "Missing or invalid 'message'");
    }

    const attachments =
      body.attachments === undefined ? [] : requireStringArray(body.attachments, 'attachments');

    const runtime = getHarnessRuntime();
    const session = await runtime.sessionManager.resume(sessionId);
    const resolvedOpts = await resolveRuntimeOptions(session, body.opts);

    const attachmentResolution = await runtime.attachmentResolver.resolveAttachmentsToContentBlocks(
      body.message,
      attachments
    );

    const contentBlocks: ContentBlock[] = attachmentResolution.contentBlocks;
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

    const encoder = new TextEncoder();

    const stream = new ReadableStream<Uint8Array>({
      async start(controller): Promise<void> {
        try {
          for await (const event of runtime.agentSdkManager.startTurn(
            session,
            body.message,
            resolvedOpts,
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
          controller.close();
        }
      }
    });

    return new Response(stream, {
      status: 200,
      headers: {
        'Content-Type': 'text/event-stream; charset=utf-8',
        'Cache-Control': 'no-cache, no-transform',
        Connection: 'keep-alive'
      }
    });
  } catch (error) {
    return errorResponse(error);
  }
}
