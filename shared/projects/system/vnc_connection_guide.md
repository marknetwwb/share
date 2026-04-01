# Railway VNC 安全密碼設定指南

## 🔐 已設定嘅安全密碼

### 推薦密碼
```
railway2024!
```

## 📋 Railway 配置資訊

### 環境變數設定
```bash
VNC_PASSWORD=railway2024!
VNC_RESOLUTION=1280x720
VNC_DEPTH=24
```

### Startup 命令設定
```bash
./setup_secure_vnc.sh
```

或者直接使用一條指令：
```bash
mkdir -p ~/.vnc && echo "railway2024!" | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd && vncserver :1 -geometry 1280x720 -depth 24
```

## 🌐 連接資訊

### VNC 連接資料
- **密碼**: `railway2024!`
- **端口**: `5901`
- **顯示**: `:1`
- **分辨率**: `1280x720`
- **色彩深度**: `24位`

### Railway 網址
- **主網址**: `{your-project}.railway.app`
- **VNC 連接**: `{your-project}.railway.app:5901`

## 🔧 使用方法

### Railway UI 設定步驟：

1. **打開 Railway project**
2. **去到 Settings → Variables**
3. **添加環境變數**：
   ```
   VNC_PASSWORD=railway2024!
   VNC_RESOLUTION=1280x720
   VNC_DEPTH=24
   ```
4. **去到 Settings → Deployments**
5. **設定 Startup command**：
   ```bash
   ./setup_secure_vnc.sh
   ```
   或者直接使用：
   ```bash
   mkdir -p ~/.vnc && echo "railway2024!" | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd && vncserver :1 -geometry 1280x720 -depth 24
   ```
6. **Deploy/重新部署**

## 📱 VNC 客戶端連接

### 推薦嘅 VNC 客戶端
- **Windows**: RealVNC Viewer, TightVNC
- **macOS**: Screen Sharing, Chicken of the VNC
- **Linux**: Remmina, Vinagre
- **Mobile**: VNC Viewer App

### 連接步驟
1. 打開 VNC 客戶端
2. 輸入 Railway 網址: `{your-project}.railway.app:5901`
3. 輸入密碼: `railway2024!`
4. 連接成功後就可以看到桌面環境

## ⚠️ 安全提醒

### 密碼安全
- 此密碼係測試用，生產環境建議使用更複雜嘅密碼
- 建議定期更換密碼
- 不要喺公開場合分享密碼

### 使用注意
- 確保 Railway project 係安全嘅
- 避免喺不安全嘅網絡環境使用
- 定期檢查服務狀態

---

設定日期：2026-03-28
密碼：railway2024!
狀態：✅ 已完成設定