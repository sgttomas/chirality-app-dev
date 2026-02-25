type DirectorySelectionResult = {
  cancelled: boolean;
  path?: string;
  error?: string;
};

type ChiralityBridge = {
  platform?: string;
  versions?: {
    chrome: string;
    electron: string;
    node: string;
  };
  selectDirectory?: () => Promise<DirectorySelectionResult>;
};

declare global {
  interface Window {
    chirality?: ChiralityBridge;
  }
}

export {};
