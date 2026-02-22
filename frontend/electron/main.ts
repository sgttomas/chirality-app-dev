import { app, BrowserWindow } from 'electron';
import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import type { AddressInfo } from 'node:net';
import path from 'node:path';

type RendererServer = {
  close: () => Promise<void>;
  url: string;
};

let rendererServer: RendererServer | undefined;

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
  if (rendererServer) {
    try {
      await rendererServer.close();
    } catch (error) {
      console.error('Failed closing packaged renderer server', error);
    }
    rendererServer = undefined;
  }
});
