#!/bin/bash

# 系統維護重啟腳本
# 包含完整的授權和執行流程

echo "🔧 系統維護重啟流程"
echo "===================="

# 檢查系統狀態
echo "📊 檢查系統狀態..."
ZOMBIE_COUNT=$(ps aux | grep -E 'Z|defunct' | grep -v grep | wc -l)
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')

echo "僵屍進程: $ZOMBIE_COUNT"
echo "內存使用: ${MEMORY_USAGE}%"

# 創建授權
echo ""
echo "🔐 創建授權..."
./grant_restart_permission.sh "系統維護 - 清理僵屍進程和釋放內存"

# 檢查授權是否創建成功
if [ -f "/data/workspace/restart_authorization.json" ]; then
    echo ""
    echo "✅ 授權創建成功!"
    echo ""
    echo "🚀 執行重啟:"
    echo "手動執行: sudo reboot"
    echo ""
    echo "📝 或者使用執行腳本:"
    echo "./execute_restart.sh"
else
    echo "❌ 授權創建失敗"
    exit 1
fi

# 記錄維護日誌
echo ""
echo "📋 維護記錄:"
MAINTENANCE_LOG="/data/workspace/maintenance_log.txt"
echo "[$(date "+%Y-%m-%d %H:%M:%S")] 系統維護重啟流程" >> "$MAINTENANCE_LOG"
echo "僵屍進程: $ZOMBIE_COUNT" >> "$MAINTENANCE_LOG"
echo "內存使用: ${MEMORY_USAGE}%" >> "$MAINTENANCE_LOG"
echo "授權狀態: 已創建" >> "$MAINTENANCE_LOG"
echo "狀態: 等待手動執行重啟" >> "$MAINTENANCE_LOG"
echo "----------------------------------------" >> "$MAINTENANCE_LOG"
