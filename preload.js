const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('aura', {
  chat: (history) => ipcRenderer.invoke('aura:chat', { history }),
  getSettings: () => ipcRenderer.invoke('aura:get-settings'),
  setSettings: (patch) => ipcRenderer.invoke('aura:set-settings', patch),
  addConnector: (connector) => ipcRenderer.invoke('aura:add-connector', connector),
  removeConnector: (id) => ipcRenderer.invoke('aura:remove-connector', id),
  openExternal: (url) => ipcRenderer.invoke('aura:open-external', url),
  onTriggerListen: (callback) => ipcRenderer.on('aura:trigger-listen', callback),
  pickFile: () => ipcRenderer.invoke('aura:pick-file'),
  listConversations: () => ipcRenderer.invoke('aura:list-conversations'),
  loadConversation: (id) => ipcRenderer.invoke('aura:load-conversation', id),
  saveConversation: (payload) => ipcRenderer.invoke('aura:save-conversation', payload),
  deleteConversation: (id) => ipcRenderer.invoke('aura:delete-conversation', id)
});
