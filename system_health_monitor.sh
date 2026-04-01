#!/bin/bash

# 系統健康監控腳本
# 定期檢查系統狀態並自動處理問題

LOG_FILE="/var/log/system_health.log"
ALERT_THRESHOLD_LOAD=10.0
ALERT_THRESHOLD_MEM=80
ALERT_THRESHOLD_DISK=85

echo "=== 系統健康檢查 $(date) ===" >> $LOG_FILE

# 1. 檢查系統負載
load_avg=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
echo "系統負載: $load_avg" >> $LOG_FILE

if (( $(echo "$load_avg > $ALERT_THRESHOLD_LOAD" | bc -l) )); then
    echo "⚠️ 負載警告: $load_avg > $ALERT_THRESHOLD_LOAD" >> $LOG_FILE
    
    # 檢查高CPU進程
    echo "高CPU進程:" >> $LOG_FILE
    ps aux --sort=-%cpu | head -5 >> $LOG_FILE
    
    # 清理系統緩存
    sync
    echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true
    echo "已清理系統緩存" >> $LOG_FILE
fi

# 2. 檢查內存使用
mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
echo "內存使用: ${mem_usage}%" >> $LOG_FILE

if [ $mem_usage -gt $ALERT_THRESHOLD_MEM ]; then
    echo "⚠️ 內存警告: ${mem_usage}% > ${ALERT_THRESHOLD_MEM}%" >> $LOG_FILE
    
    # 清理不必要的進程
    echo "清理緩存進程..." >> $LOG_FILE
    pkill -f "chrome" 2>/dev/null || true
    pkill -f "firefox" 2>/dev/null || true
fi

# 3. 檢查磁碟空間
disk_usage=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
echo "磁碟使用: ${disk_usage}%" >> $LOG_FILE

if [ $disk_usage -gt $ALERT_THRESHOLD_DISK ]; then
    echo "⚠️ 磁碟警告: ${disk_usage}% > ${ALERT_THRESHOLD_DISK}%" >> $LOG_FILE
    
    # 清理日誌文件
    echo "清理舊日�..." >> $LOG_FILE
    find /var/log -name "*.log.*" -mtime +7 -delete 2>/dev/null || true
    find /tmp -type f -mtime +1 -delete 2>/dev/null || true
fi

# 4. 檢查僵屍進程
zombie_count=$(ps aux | grep -E 'Z|<defunct>' | grep -v grep | wc -l)
echo "僵屍進程: $zombie_count" >> $LOG_FILE

if [ $zombie_count -gt 0 ]; then
    echo "清理僵屍進程..." >> $LOG_FILE
    /data/workspace/cleanup_zombies.sh
fi

# 5. 檢查網絡連接
echo "檢查網絡狀態..." >> $LOG_FILE
ping -c 1 8.8.8.8 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ 網絡連接正常" >> $LOG_FILE
else
    echo "❌ 網絡連接異常" >> $LOG_FILE
fi

echo "=== 系統健康檢查完成 ===" >> $LOG_FILE
echo "" >> $LOG_FILE