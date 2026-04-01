#!/bin/bash
# 每日清理zombie進程腳本

LOG_FILE="/var/log/zombie_cleanup.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] 開始清理zombie進程..." >> $LOG_FILE

# 計數並清理zombie進程
ZOMBIE_COUNT=$(ps aux | grep defunct | grep -v grep | wc -l)
if [ $ZOMBIE_COUNT -gt 0 ]; then
    echo "[$DATE] 發現 $ZOMBIE_COUNT 個zombie進程" >> $LOG_FILE
    ps aux | grep defunct | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null
    echo "[$DATE] 已清理 $ZOMBIE_COUNT 個zombie進程" >> $LOG_FILE
else
    echo "[$DATE] 無zombie進程需要清理" >> $LOG_FILE
fi

# 記錄系統狀態
echo "[$DATE] 系統負載: $(uptime | awk -F'load average:' '{print $2}')" >> $LOG_FILE
echo "[$DATE] 內存使用: $(free -h | grep Mem | awk '{print $3}')" >> $LOG_FILE

echo "[$DATE] 清理完成" >> $LOG_FILE