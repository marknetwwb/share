#!/bin/bash
# backup_manager.sh - 備份管理員

BACKUP_ROOT="/data/workspace/backups"
MAX_DAILY=30
MAX_WEEKLY=12
MAX_MONTHLY=24

echo "=== 記憶備份管理員 ==="
echo "執行時間: $(date)"
echo ""

# 檢查備份目錄空間使用情況
echo "📊 備份目錄使用情況:"
du -sh "$BACKUP_ROOT" 2>/dev/null || echo "無法統計備份目錄"
echo ""

# 清理舊備份（保留30天）
echo "🧹 清理超過 $MAX_DAILY 天的每日備份..."
if [ -d "$BACKUP_ROOT" ]; then
    # 找到並刪除舊備份
    find "$BACKUP_ROOT" -name "*.tar.gz" -mtime +$MAX_DAILY -exec rm -f {} \;
    
    # 統計刪除的檔案數量
    DELETED_COUNT=$(find "$BACKUP_ROOT" -name "*.tar.gz" -mtime +$MAX_DAILY | wc -l)
    if [ "$DELETED_COUNT" -gt 0 ]; then
        echo "✅ 已刪除 $DELETED_COUNT 個舊備份檔案"
    else
        echo "ℹ️ 沒有需要清理的舊備份"
    fi
else
    echo "⚠️ 備份目錄不存在"
fi

echo ""
echo "📋 備份檔案列表:"
ls -la "$BACKUP_ROOT/"*.tar.gz 2>/dev/null | wc -l | xargs echo "總計備份檔案數量:"
ls -la "$BACKUP_ROOT/"*.tar.gz 2>/dev/null | tail -5
echo ""

echo "🎉 備份管理完成！"