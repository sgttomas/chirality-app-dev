import { contextBridge, ipcRenderer } from 'electron';

const SELECT_DIRECTORY_CHANNEL = 'chirality:select-directory';
const API_KEY_STORE_CHANNEL = 'chirality:api-key-store';
const API_KEY_REMOVE_CHANNEL = 'chirality:api-key-remove';
const API_KEY_STATUS_CHANNEL = 'chirality:api-key-status';

contextBridge.exposeInMainWorld('chirality', {
  platform: process.platform,
  versions: {
    chrome: process.versions.chrome,
    electron: process.versions.electron,
    node: process.versions.node
  },
  selectDirectory: () => ipcRenderer.invoke(SELECT_DIRECTORY_CHANNEL),
  apiKey: {
    store: (key: string) => ipcRenderer.invoke(API_KEY_STORE_CHANNEL, key),
    remove: () => ipcRenderer.invoke(API_KEY_REMOVE_CHANNEL),
    status: () => ipcRenderer.invoke(API_KEY_STATUS_CHANNEL)
  }
});
