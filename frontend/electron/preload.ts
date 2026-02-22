import { contextBridge, ipcRenderer } from 'electron';

const SELECT_DIRECTORY_CHANNEL = 'chirality:select-directory';

contextBridge.exposeInMainWorld('chirality', {
  platform: process.platform,
  versions: {
    chrome: process.versions.chrome,
    electron: process.versions.electron,
    node: process.versions.node
  },
  selectDirectory: () => ipcRenderer.invoke(SELECT_DIRECTORY_CHANNEL)
});
