#!/bin/bash
# auto_backup_scheduler_v2.sh - 修正版自動記憶備份排程器

# 配置參數
BACKUP_SCRIPT="/data/workspace/backup_memory.sh"
LOG_FILE="/data/workspace/backups/auto_backup.log"
SLEEP_INTERVAL="86400"  # 24小時 = 86400秒

echo "=== 自動記憶備份排程器 v2.0 ==="
echo "啟動時間: $(date)"
echo "備份腳本: $BACKUP_SCRIPT"
echo "間隔時間: $SLEEP_INTERVAL 秒 (24小時)"
echo "日誌檔案: $LOG_FILE"
echo "================================"
echo ""

# 檢查備份腳本是否存在
if [ ! -f "$BACKUP_SCRIPT" ]; then
    echo "❌ 錯誤：備份腳本不存在: $BACKUP_SCRIPT"
    exit 1
fi

# 給予執行權限
chmod +x "$BACKUP_SCRIPT"

# 創建備份目錄
mkdir -p "/data/workspace/backups"

# 初始化日誌
echo "自動備份排程器 v2.0 啟動 - $(date)" > "$LOG_FILE"

# 執行循環備份
echo "🚀 開始自動備份循環..."
echo ""

while true; do
    CURRENT_TIME=$(date)
    echo "=== 執行備份 - $CURRENT_TIME ===" | tee -a "$LOG_FILE"
    
    # 執行備份
    if "$BACKUP_SCRIPT" >> "$LOG_FILE" 2>&1; then
        echo "✅ 備份成功完成 - $CURRENT_TIME" | tee -a "$LOG_FILE"
    else
        echo "❌ 備份執行失敗 - $CURRENT_TIME" | tee -a "$LOG_FILE"
    fi
    
    echo "" | tee -a "$LOG_FILE"
    
    # 顯示下次執行時間
    NEXT_RUN_TIME=$(date -d "+86400 seconds" "+%Y-%m-%d %H:%M:%S")
    echo "下次備份時間: $NEXT_RUN_TIME" | tee -a "$LOG_FILE"
    echo "等待中... (間隔: 24小時)" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
    
    # 等待指定時間
    sleep "$SLEEP_INTERVAL"
done