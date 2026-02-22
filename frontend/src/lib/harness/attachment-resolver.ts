import { access, stat } from 'node:fs/promises';
import path from 'node:path';
import { IAttachmentResolver, ResolvedAttachments } from './types';

export class StubAttachmentResolver implements IAttachmentResolver {
  async resolveAttachmentsToContentBlocks(
    message: string,
    attachmentPaths: string[]
  ): Promise<ResolvedAttachments> {
    const contentBlocks: ResolvedAttachments['contentBlocks'] = [];
    const errors: ResolvedAttachments['errors'] = [];

    if (message.trim()) {
      contentBlocks.push({ type: 'text', text: message });
    }

    for (const rawPath of attachmentPaths) {
      if (!path.isAbsolute(rawPath)) {
        errors.push({ path: rawPath, reason: 'Attachment path must be absolute' });
        continue;
      }

      try {
        await access(rawPath);
        const fileStat = await stat(rawPath);
        if (!fileStat.isFile()) {
          errors.push({ path: rawPath, reason: 'Attachment path is not a file' });
          continue;
        }

        contentBlocks.push({
          type: 'file',
          path: rawPath,
          mimeType: 'application/octet-stream'
        });
      } catch {
        errors.push({ path: rawPath, reason: 'Attachment file not accessible' });
      }
    }

    return { contentBlocks, errors };
  }
}
