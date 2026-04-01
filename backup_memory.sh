#!/bin/bash
# backup_memory.sh - 記憶檔案備份腳本

# 備份日期
BACKUP_DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="/data/workspace/backups/memory_$BACKUP_DATE"

# 創建備份目錄
mkdir -p "$BACKUP_DIR"

echo "開始備份記憶檔案..."
echo "備份時間: $BACKUP_DATE"
echo "備份目錄: $BACKUP_DIR"

# 備份記憶檔案
if [ -d "/data/workspace/memory" ]; then
    cp -r /data/workspace/memory "$BACKUP_DIR/"
    echo "✅ 每日記憶已備份"
else
    echo "⚠️ 每日記憶目錄不存在"
fi

# 備份長期記憶
if [ -f "/data/workspace/MEMORY.md" ]; then
    cp /data/workspace/MEMORY.md "$BACKUP_DIR/"
    echo "✅ 長期記憶已備份"
else
    echo "⚠️ 長期記憶檔案不存在"
fi

# 壓縮備份
cd /data/workspace/backups
tar -czf "memory_backup_$BACKUP_DATE.tar.gz" "memory_$BACKUP_DATE/"
rm -rf "memory_$BACKUP_DATE/"

echo "🎉 記憶備份完成: memory_backup_$BACKUP_DATE.tar.gz"
echo "備份位置: /data/workspace/backups/memory_backup_$BACKUP_DATE.tar.gz"