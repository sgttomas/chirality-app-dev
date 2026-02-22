import type { Metadata } from 'next';
import './globals.css';
import { WorkspaceProvider } from '../components/workspace/workspace-provider';

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
        <WorkspaceProvider>{children}</WorkspaceProvider>
      </body>
    </html>
  );
}
