#!/bin/bash

# 系統防護守護進程
# 長期監控並自動處理系統問題

SERVICE_NAME="system_protection"
SERVICE_PID="/tmp/${SERVICE_NAME}.pid"
LOG_DIR="/var/log/${SERVICE_NAME}"
CRON_LOG="${LOG_DIR}/cron.log"
MONITOR_LOG="${LOG_DIR}/monitor.log"

# 創建日誌目錄
mkdir -p $LOG_DIR

echo "啟動系統防護守護進程 - $(date)" >> $CRON_LOG

# 檢查是否已經在運行
if [ -f $SERVICE_PID ]; then
    old_pid=$(cat $SERVICE_PID)
    if ps -p $old_pid > /dev/null 2>&1; then
        echo "服務已在運行 (PID: $old_pid)" >> $CRON_LOG
        exit 1
    else
        rm -f $SERVICE_PID
    fi
fi

echo $$ > $SERVICE_PID

# 設定定時任務
echo "設定系統監控定時任務..." >> $CRON_LOG

# 每分鐘檢查一次系統健康
echo "* * * * * /data/workspace/system_health_monitor.sh >> $MONITOR_LOG 2>&1" | crontab -

# 每5分鐘清理一次僵屍進程
echo "*/5 * * * * /data/workspace/cleanup_zombies.sh >> $MONITOR_LOG 2>&1" | crontab -

# 每小時生成系統報告
echo "0 * * * * echo \"=== 小時報告 $(date) ===\" >> $MONITOR_LOG && echo \"負載: $(uptime | awk -F'load average:' '{print $2}')\" >> $MONITOR_LOG && echo \"內存: $(free -h | grep Mem | awk '{print $3\"/\"$2}')\" >> $MONITOR_LOG" | crontab -

# 每天重啟一次OpenClaw服務（避免內存泄漏）
echo "0 2 * * * echo \"=== 重啟OpenClaw服務 $(date) ===\" >> $MONITOR_LOG && pkill -f openclaw-gateway && sleep 3 && /usr/local/bin/openclaw gateway start 2>/dev/null || true" | crontab -

echo "防護機制已啟動" >> $CRON_LOG

# 守護循環
while true; do
    sleep 60
    
    # 檢查系統狀態
    current_load=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    
    # 如果負載過高，立即執行深度清理
    if (( $(echo "$current_load > 20.0" | bc -l) )); then
        echo "高負載警告: $current_load，執行緊急清理" >> $MONITOR_LOG
        
        # 強制清理系統資源
        sync
        echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true
        
        # 清理所有非關鍵進程
        pkill -f "chrome" 2>/dev/null || true
        pkill -f "firefox" 2>/dev/null || true
        pkill -f "slack" 2>/dev/null || true
        
        # 重啟Gateway服務
        pkill -f "openclaw-gateway"
        sleep 2
        /usr/local/bin/openclaw gateway start 2>/dev/null || true
        
        echo "緊急清理完成" >> $MONITOR_LOG
    fi
    
    # 檢查日誌文件大小
    for log_file in $MONITOR_LOG $CRON_LOG; do
        if [ -f $log_file ]; then
            file_size=$(du -k $log_file | cut -f1)
            if [ $file_size -gt 10240 ]; then  # 超過10MB
                echo "日誌文件過大，進行壓縮: $log_file" >> $MONITOR_LOG
                gzip -f $log_file
                mv ${log_file}.gz ${log_file}.gz.$(date +%Y%m%d_%H%M%S)
            fi
        fi
    done
done