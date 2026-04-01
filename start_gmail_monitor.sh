#!/bin/bash
# Gmail 訂單監控啟動腳本
# 用於 OpenClaw 自動化系統

# 設置環境變量
export $(cat /data/workspace/gmail_monitor_config.env | xargs)

# 啟動監控程序
echo "啟動 Gmail 訂單監控..."
cd /data/workspace

# 使用 nohup 在後台運行
nohup python3 openclaw_automation.py >> /data/workspace/gmail_monitor.log 2>&1 &

# 保存 PID
echo $! > /data/workspace/gmail_monitor.pid

echo "Gmail 訂單監控已啟動，PID: $!"
echo "日誌文件: /data/workspace/gmail_monitor.log"
echo "配置文件: /data/workspace/gmail_monitor_config.env"