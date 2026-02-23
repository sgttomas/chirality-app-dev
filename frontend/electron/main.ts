import { app, BrowserWindow, dialog, ipcMain } from 'electron';
import { stat } from 'node:fs/promises';
import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import type { AddressInfo } from 'node:net';
import path from 'node:path';

type RendererServer = {
  close: () => Promise<void>;
  url: string;
};

const SELECT_DIRECTORY_CHANNEL = 'chirality:select-directory';

let rendererServer: RendererServer | undefined;

function resolveInstructionRootForProcess(): string {
  const envOverride = process.env.CHIRALITY_INSTRUCTION_ROOT?.trim();
  if (envOverride) {
    return path.resolve(envOverride);
  }

  if (app.isPackaged) {
    return path.resolve(process.resourcesPath);
  }

  return path.resolve(__dirname, '..', '..');
}

async function registerDirectorySelectionHandler(): Promise<void> {
  ipcMain.removeHandler(SELECT_DIRECTORY_CHANNEL);
  ipcMain.handle(SELECT_DIRECTORY_CHANNEL, async () => {
    const dialogResult = await dialog.showOpenDialog({
      title: 'Select Working Root',
      properties: ['openDirectory']
    });

    if (dialogResult.canceled || dialogResult.filePaths.length === 0) {
      return { cancelled: true };
    }

    const selectedPath = path.resolve(dialogResult.filePaths[0]);

    try {
      const selectedStat = await stat(selectedPath);
      if (!selectedStat.isDirectory()) {
        return {
          cancelled: true,
          error: 'Selected path is not a directory'
        };
      }
    } catch {
      return {
        cancelled: true,
        error: 'Selected path is not accessible'
      };
    }

    return {
      cancelled: false,
      path: selectedPath
    };
  });
}

async function startPackagedRendererServer(): Promise<RendererServer> {
  const rendererRoot = path.join(process.resourcesPath, 'app.asar');
  const nextModule = await import('next');
  const nextFactory = (nextModule.default ?? nextModule) as unknown as (config: {
    dev: boolean;
    dir: string;
  }) => {
    getRequestHandler: () => (
      req: IncomingMessage,
      res: ServerResponse<IncomingMessage>
    ) => Promise<void> | void;
    prepare: () => Promise<void>;
  };

  const nextApp = nextFactory({
    dev: false,
    dir: rendererRoot
  });

  await nextApp.prepare();
  const handle = nextApp.getRequestHandler();
  const server = createServer((req, res) => {
    handle(req, res);
  });

  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      server.off('error', reject);
      resolve();
    });
  });

  const address = server.address() as AddressInfo | null;
  if (!address || typeof address === 'string') {
    throw new Error('Renderer server failed to bind a TCP port');
  }

  return {
    close: async () => {
      await new Promise<void>((resolve, reject) => {
        server.close((error) => {
          if (error) {
            reject(error);
            return;
          }
          resolve();
        });
      });
    },
    url: `http://127.0.0.1:${address.port}`
  };
}

function createMainWindow(rendererUrl: string): BrowserWindow {
  const window = new BrowserWindow({
    width: 1280,
    height: 840,
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    }
  });

  window.once('ready-to-show', () => {
    window.show();
  });

  window.loadURL(rendererUrl);

  return window;
}

app
  .whenReady()
  .then(async () => {
    await registerDirectorySelectionHandler();
    process.env.CHIRALITY_INSTRUCTION_ROOT = resolveInstructionRootForProcess();

    const rendererUrl = app.isPackaged
      ? (rendererServer = await startPackagedRendererServer()).url
      : process.env.ELECTRON_RENDERER_URL ?? 'http://localhost:3000';

    createMainWindow(rendererUrl);

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        createMainWindow(rendererUrl);
      }
    });
  })
  .catch((error) => {
    console.error('Failed to initialize renderer runtime', error);
    app.quit();
  });

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', async () => {
  ipcMain.removeHandler(SELECT_DIRECTORY_CHANNEL);

  if (rendererServer) {
    try {
      await rendererServer.close();
    } catch (error) {
      console.error('Failed closing packaged renderer server', error);
    }
    rendererServer = undefined;
  }
});
