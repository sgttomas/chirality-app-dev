import { app, BrowserWindow } from 'electron';
import path from 'node:path';

function createMainWindow(): BrowserWindow {
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

  if (app.isPackaged) {
    const indexHtml = path.join(__dirname, '..', 'out', 'index.html');
    window.loadFile(indexHtml);
  } else {
    const rendererUrl = process.env.ELECTRON_RENDERER_URL ?? 'http://localhost:3000';
    window.loadURL(rendererUrl);
  }

  return window;
}

app.whenReady().then(() => {
  createMainWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
