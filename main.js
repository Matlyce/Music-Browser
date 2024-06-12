const { app, BrowserWindow, Menu, shell } = require('electron');
const path = require('path');
const fs = require('fs');
const { ipcMain } = require('electron');


function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 1280,
        height: 720,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: true,
            webviewTag: true,
            preload: path.join(__dirname, 'preload.js'),
            contentSecurityPolicy: {
                directives: {
                    defaultSrc: ["'self'"],
                    scriptSrc: ["'self'"]
                }
            }
        },
    });

    // set background color
    mainWindow.setBackgroundColor('#000000');

    // load the icon.png file
    mainWindow.setIcon(path.join(__dirname, 'public', 'assets', 'icon.png'));
    mainWindow.loadFile('public/index.html');

    // hide the menu
    mainWindow.setMenuBarVisibility(false);
    // mainWindow.webContents.openDevTools();

    ipcMain.on('open-url', (event, url) => {
        console.log('open-url event received');
        shell.openExternal(url);
    });

    ipcMain.on('save-settings', (event, hiddenMenus) => {
        console.log('save-settings event received');
        const appData = process.env.APPDATA || (process.platform == 'darwin' ? process.env.HOME + '/Library/Preferences' : '/var/local');
        const filePath = path.join(appData, 'hiddenMenus.json');

        fs.writeFileSync(
            filePath,
            JSON.stringify(hiddenMenus),
            'utf-8'
        );

        console.log('settings saved at: ' + filePath);
    });

    ipcMain.on('retrieve-settings', (event) => {
        console.log('retrieve-settings event received');
        const appData = process.env.APPDATA || (process.platform == 'darwin' ? process.env.HOME + '/Library/Preferences' : '/var/local');
        const filePath = path.join(appData, 'hiddenMenus.json');

        if (fs.existsSync(filePath)) {
            const hiddenMenus = fs.readFileSync(filePath, 'utf-8');
            event.reply('retrieve-settings-reply', hiddenMenus);
        } else {
            event.reply('retrieve-settings-reply', null);
        }
    });

}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
