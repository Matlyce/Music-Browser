const { contextBridge, ipcRenderer } = require('electron');

// Expose custom API to the renderer process
contextBridge.exposeInMainWorld('api', {
    openUrl: (url) => {
        ipcRenderer.send('open-url', url);
    },
    saveSettings: (hiddenMenus) => {
        ipcRenderer.send('save-settings', hiddenMenus);
    },


    retrieveSettings: () => {
        ipcRenderer.send('retrieve-settings');
    },
    onRetrieveSettingsReply: (callback) => {
        ipcRenderer.on('retrieve-settings-reply', (event, hiddenMenus) => {
            callback(hiddenMenus);
        });
    }

});