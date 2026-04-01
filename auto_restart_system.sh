#!/bin/bash

# 自動重啟系統腳本
# 每5天執行一次系統重啟

LOG_FILE="/data/workspace/auto_restart.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "=== $TIMESTAMP ===" >> $LOG_FILE

# 檢查僵屍進程數量
ZOMBIE_COUNT=$(ps aux | grep -E 'Z|defunct' | grep -v grep | wc -l)
echo "僵屍進程數量: $ZOMBIE_COUNT" >> $LOG_FILE

# 檢查內存使用
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
echo "內存使用率: ${MEMORY_USAGE}%" >> $LOG_FILE

# 檢查系統運行時間
UPTIME=$(uptime -p)
echo "系統運行時間: $UPTIME" >> $LOG_FILE

# 如果僵屍進程超過10個或內存使用超過80%，立即重啟
if [ $ZOMBIE_COUNT -gt 10 ] || [ $(echo "$MEMORY_USAGE > 80" | bc) -eq 1 ]; then
    echo "觸發條件重啟: 僵屍進程($ZOMBIE_COUNT)或內存使用(${MEMORY_USAGE}%)" >> $LOG_FILE
    # 這裡需要root權限才能執行系統重啟
    echo "需要root權限執行: sudo reboot" >> $LOG_FILE
else
    echo "系統狀態正常，無需重啟" >> $LOG_FILE
fi

echo "" >> $LOG_FILE
