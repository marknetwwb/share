#!/bin/bash

# Railway VNC 安全密碼設定腳本
# 使用預設安全密碼

# 安全密碼設定
SECURE_PASSWORD="railway2024!"

# 創建 VNC 目錄
mkdir -p ~/.vnc

# 設定 VNC 密碼
echo "$SECURE_PASSWORD" | vncpasswd -f > ~/.vnc/passwd

# 設定檔案權限
chmod 600 ~/.vnc/passwd

# 啟動 VNC 服務
echo "啟動 VNC 服務..."
vncserver :1 -geometry 1280x720 -depth 24

# 顯示連接資訊
echo ""
echo "✅ VNC 服務已成功啟動！"
echo ""
echo "🔐 連接資訊："
echo "   密碼: railway2024!"
echo "   端口: 5901"
echo "   顯示: :1"
echo ""
echo "🌐 Railway 連接："
echo "   網址: {your-project}.railway.app:5901"
echo ""
echo "💡 提示："
echo "   - 使用 VNC 客戶端連接"
echo "   - 密碼係: railway2024!"
echo "   - 建議喺安全環境使用"