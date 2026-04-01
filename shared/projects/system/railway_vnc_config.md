# Railway 配置文件說明
# 使用 Railway template 嘅 VNC 配置

## 📋 Railway 配置步驟

### 1. 環境變數設定
在 Railway project 嘅 Environment variables 設定：

```
VNC_PASSWORD=your_secure_password
VNC_RESOLUTION=1280x720
VNC_DEPTH=24
```

### 2. Startup 命令設定
在 Railway 嘅 Startup command 設定：

```bash
mkdir -p ~/.vnc
echo "$VNC_PASSWORD" | vncpasswd -f > ~/.vnc/passwd
chmod 600 ~/.vnc/passwd
vncserver :1 -geometry $VNC_RESOLUTION -depth $VNC_DEPTH
```

### 3. Build 命令設定（如果需要）
```bash
apt-get update && apt-get install -y xvfb vnc4server firefox
```

## 🔐 密碼選項推薦

### 安全密碼範例
- `railway2024!`
- `vnc_secure_01`
- `project_access_2026`

### 弱密碼（測試用）
- `password`
- `123456`
- `railway`

## 🚀 完整配置指南

### Railway UI 步驟：
1. 打開你嘅 Railway project
2. 去到 Settings → Variables
3. 添加以下環境變數：
   - `VNC_PASSWORD` (你的密碼)
   - `VNC_RESOLUTION` (1280x720)
   - `VNC_DEPTH` (24)
4. 去到 Settings → Deployments
5. 設定 Startup command：
   ```bash
   mkdir -p ~/.vnc && echo "$VNC_PASSWORD" | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd && vncserver :1 -geometry $VNC_RESOLUTION -depth $VNC_DEPTH
   ```

## 🌐 連接信息

### 連接資訊
- **端口**: 5901
- **顯示**: :1
- **密碼**: 設定嘅 VNC_PASSWORD

### Railway 網址
- **主網址**: {your-railway-project}.railway.app
- **VNC 連接**: {your-railway-project}.railway.app:5901

## 💡 注意事项

1. **密碼安全**: 建議使用強密碼
2. **防火牆**: Railway 通常會自動開放端口
3. **服務穩定性**: 定期檢查服務狀態
4. **成本考量**: Railway 免費版有資源限制

---

配置日期：2026-03-28
適用於：Railway template VNC 服務