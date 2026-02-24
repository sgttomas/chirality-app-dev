import type { Metadata } from 'next';
import './globals.css';
import { WorkspaceProvider } from '../components/workspace/workspace-provider';
import { ToolkitProvider } from '../components/workspace/toolkit-provider';

export const metadata: Metadata = {
  title: 'Chirality Workflow Shell',
  description: 'PORTAL, PIPELINE, and WORKBENCH shell for local agent execution'
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <WorkspaceProvider>
          <ToolkitProvider>{children}</ToolkitProvider>
        </WorkspaceProvider>
      </body>
    </html>
  );
}
