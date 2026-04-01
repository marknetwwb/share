#!/bin/bash

# 授權重啟系統腳本
# 需要手動授權才能執行系統重啟

LOG_FILE="/data/workspace/authorized_restart.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "=== 授權重啟請求 $TIMESTAMP ===" >> $LOG_FILE

# 檢查重啟原因
REASON=${1:-"定期維護"}

# 檢查系統狀態
ZOMBIE_COUNT=$(ps aux | grep -E 'Z|defunct' | grep -v grep | wc -l)
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')

echo "重啟原因: $REASON" >> $LOG_FILE
echo "僵屍進程: $ZOMBIE_COUNT" >> $LOG_FILE
echo "內存使用: ${MEMORY_USAGE}%" >> $LOG_FILE

# 創建授權文件
AUTH_FILE="/data/workspace/restart_authorized.flag"
echo "$TIMESTAMP" > "$AUTH_FILE"
echo "Reason: $REASON" >> "$AUTH_FILE"
echo "Zombies: $ZOMBIE_COUNT" >> "$AUTH_FILE"
echo "Memory: ${MEMORY_USAGE}%" >> "$AUTH_FILE"

echo "✅ 授權文件已創建: $AUTH_FILE" >> $LOG_FILE
echo "手動執行: sudo reboot" >> $LOG_FILE

echo "授權重啟請求已記錄，等待手動確認執行 sudo reboot" >> $LOG_FILE
