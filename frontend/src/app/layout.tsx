import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Chirality Frontend Bootstrap',
  description: 'Bootstrap workspace for the Chirality desktop harness'
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
