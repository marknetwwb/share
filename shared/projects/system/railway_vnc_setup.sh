#!/bin/bash

# Railway VNC 密碼設定腳本
# 透過環境變數設定 VNC 密碼

# 設定 VNC 密碼（從環境變數讀取）
VNC_PASSWORD=${VNC_PASSWORD:-"password"}

# 創建 VNC 密碼檔案
mkdir -p ~/.vnc
echo "$VNC_PASSWORD" | vncpasswd -f > ~/.vnc/passwd
chmod 600 ~/.vnc/passwd

# 啟動 VNC 服務
echo "啟動 VNC 服務..."
vncserver :1 -geometry 1280x720 -depth 24

echo "VNC 服務已啟動"
echo "密碼: $VNC_PASSWORD"
echo "端口: 5901"
echo "顯示: :1"