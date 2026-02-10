const { app, BrowserWindow, Menu, Tray, shell } = require('electron');
const path = require('path');
const { spawn, exec } = require('child_process');
const http = require('http');
const fs = require('fs');

// Disable GPU acceleration để tránh lỗi cache
app.disableHardwareAcceleration();
app.commandLine.appendSwitch('disable-gpu');
app.commandLine.appendSwitch('disable-software-rasterizer');

let mainWindow;
let splashWindow;
let tray = null;
let backendProcess = null;

// Đường dẫn
const isDev = !app.isPackaged;
const rootPath = isDev 
  ? path.join(__dirname, '../..')
  : path.join(process.resourcesPath);

// Kiểm tra port đang chạy
function isPortOpen(port) {
  return new Promise((resolve) => {
    const req = http.request({ host: 'localhost', port, method: 'GET', path: '/', timeout: 1000 }, () => {
      resolve(true);
    });
    req.on('error', () => resolve(false));
    req.on('timeout', () => { req.destroy(); resolve(false); });
    req.end();
  });
}

// Khởi động Backend Python (không đợi)
function startBackend() {
  const backendPath = path.join(rootPath, 'backend');
  const venvPython = path.join(backendPath, 'venv', 'Scripts', 'python.exe');
  const pythonPath = fs.existsSync(venvPython) ? venvPython : 'python';
  
  console.log('Starting backend from:', backendPath);
  
  // Kiểm tra xem backend đã chạy chưa
  isPortOpen(8000).then(isOpen => {
    if (isOpen) {
      console.log('Backend already running on port 8000');
      return;
    }
    
    console.log('Starting new backend process...');
    backendProcess = spawn(pythonPath, ['run.py'], {
      cwd: backendPath,
      stdio: 'ignore',
      detached: true,
      shell: false,
      windowsHide: true
    });
    
    backendProcess.unref();
    console.log('Backend process started');
  });
}

// Tắt Backend
function stopBackend() {
  if (backendProcess) {
    console.log('Stopping backend...');
    try {
      process.kill(backendProcess.pid);
    } catch (e) {
      console.log('Backend already stopped');
    }
    backendProcess = null;
  }
  
  // Kill any python processes running on port 8000
  if (process.platform === 'win32') {
    exec('netstat -ano | findstr :8000', (err, stdout) => {
      if (stdout) {
        const lines = stdout.split('\n');
        lines.forEach(line => {
          const parts = line.trim().split(/\s+/);
          const pid = parts[parts.length - 1];
          if (pid && !isNaN(pid)) {
            exec(`taskkill /PID ${pid} /F`, () => {});
          }
        });
      }
    });
  }
}

// Tạo cửa sổ Splash loading
function createSplashWindow() {
  splashWindow = new BrowserWindow({
    width: 400,
    height: 300,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: false,
    skipTaskbar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    }
  });

  const splashHtml = `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {
          margin: 0;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          font-family: 'Segoe UI', sans-serif;
          color: white;
          border-radius: 16px;
        }
        .container { text-align: center; }
        .logo { font-size: 64px; margin-bottom: 16px; }
        h1 { margin: 0; font-size: 28px; font-weight: 600; }
        .loading { margin-top: 24px; font-size: 14px; opacity: 0.9; }
        .spinner {
          margin-top: 16px;
          width: 40px; height: 40px;
          border: 3px solid rgba(255,255,255,0.3);
          border-top-color: white;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-left: auto; margin-right: auto;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="logo">📚</div>
        <h1>GiaoTrinh AI</h1>
        <p class="loading">Đang khởi động...</p>
        <div class="spinner"></div>
      </div>
    </body>
    </html>
  `;

  splashWindow.loadURL('data:text/html;charset=utf-8,' + encodeURIComponent(splashHtml));
}

// Tạo cửa sổ chính
function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 700,
    icon: path.join(__dirname, '../public/icon.ico'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
    show: true,  // Show ngay lập tức
    center: true, // Đặt giữa màn hình
    title: 'GiaoTrinh AI - Hỗ trợ Giáo viên'
  });
  
  // Force show và focus
  mainWindow.show();
  mainWindow.focus();
  mainWindow.moveTop();

  // Load frontend
  const distPath = path.join(__dirname, '../dist/index.html');
  console.log('Loading from:', distPath);
  console.log('File exists:', fs.existsSync(distPath));
  
  if (fs.existsSync(distPath)) {
    mainWindow.loadFile(distPath);
  } else {
    console.log('Dist not found, loading from localhost');
    mainWindow.loadURL('http://localhost:3000');
  }

  // Log when loaded
  mainWindow.webContents.on('did-finish-load', () => {
    console.log('Page loaded successfully!');
    if (splashWindow && !splashWindow.isDestroyed()) {
      splashWindow.close();
    }
    splashWindow = null;
  });

  // Handle load failure
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    console.log('Failed to load:', errorCode, errorDescription);
  });

  // Minimize to tray instead of closing
  mainWindow.on('close', (event) => {
    if (!app.isQuitting) {
      event.preventDefault();
      mainWindow.hide();
    }
  });

  // Open external links in browser
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

// Tạo System Tray
function createTray() {
  const iconPath = path.join(__dirname, '../public/icon.ico');
  
  try {
    tray = new Tray(iconPath);
    
    const contextMenu = Menu.buildFromTemplate([
      { 
        label: 'Mở GiaoTrinh AI', 
        click: () => { mainWindow.show(); mainWindow.focus(); }
      },
      { type: 'separator' },
      { 
        label: 'Thoát', 
        click: () => { app.isQuitting = true; stopBackend(); app.quit(); }
      }
    ]);

    tray.setToolTip('GiaoTrinh AI - Hỗ trợ Giáo viên');
    tray.setContextMenu(contextMenu);
    tray.on('double-click', () => { mainWindow.show(); mainWindow.focus(); });
  } catch (err) {
    console.log('Could not create tray:', err);
  }
}

// Tạo Menu
function createMenu() {
  const template = [
    {
      label: 'GiaoTrinh AI',
      submenu: [
        { label: 'Giới thiệu', role: 'about' },
        { type: 'separator' },
        { label: 'Thoát', accelerator: 'CmdOrCtrl+Q', click: () => { app.isQuitting = true; stopBackend(); app.quit(); } }
      ]
    },
    {
      label: 'Chỉnh sửa',
      submenu: [
        { label: 'Hoàn tác', role: 'undo' },
        { label: 'Làm lại', role: 'redo' },
        { type: 'separator' },
        { label: 'Cắt', role: 'cut' },
        { label: 'Sao chép', role: 'copy' },
        { label: 'Dán', role: 'paste' },
        { label: 'Chọn tất cả', role: 'selectAll' }
      ]
    },
    {
      label: 'Xem',
      submenu: [
        { label: 'Tải lại', role: 'reload' },
        { label: 'Phóng to', role: 'zoomIn' },
        { label: 'Thu nhỏ', role: 'zoomOut' },
        { label: 'Kích thước gốc', role: 'resetZoom' },
        { type: 'separator' },
        { label: 'Toàn màn hình', role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Trợ giúp',
      submenu: [
        { label: 'Hướng dẫn sử dụng', click: () => shell.openExternal('https://giaotrinh.ai/help') },
        { label: 'Liên hệ hỗ trợ', click: () => shell.openExternal('mailto:support@giaotrinh.ai') }
      ]
    }
  ];

  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

// App Events
app.whenReady().then(() => {
  console.log('App is ready!');
  
  // Show splash
  console.log('Creating splash window...');
  createSplashWindow();
  
  // Start backend (non-blocking)
  console.log('Starting backend...');
  startBackend();
  
  // Create UI
  console.log('Creating menu...');
  createMenu();
  
  console.log('Creating main window...');
  createMainWindow();
  
  console.log('Creating tray...');
  createTray();
  
  console.log('All components created!');

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    } else {
      mainWindow.show();
    }
  });
});

app.on('window-all-closed', () => {
  console.log('All windows closed');
  // Không thoát khi đóng cửa sổ - giữ app chạy
  // if (process.platform !== 'darwin') {
  //   stopBackend();
  //   app.quit();
  // }
});

app.on('before-quit', () => {
  app.isQuitting = true;
});

// Single instance
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.show();
      mainWindow.focus();
    }
  });
}
