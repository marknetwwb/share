#!/bin/bash

# 授權重啟腳本
# 這個腳本會創建授權文件，但不執行重啟

AUTH_REASON=${1:-"定期系統維護"}
AUTH_FILE="/data/workspace/restart_authorization.json"
LOG_FILE="/data/workspace/restart_permission.log"

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "=== 授權請求 $TIMESTAMP ===" >> $LOG_FILE
echo "授權原因: $AUTH_REASON" >> $LOG_FILE

# 檢查當前系統狀態
echo "系統狀態檢查:" >> $LOG_FILE

# 僵屍進程檢查
ZOMBIE_COUNT=$(ps aux | grep -E 'Z|defunct' | grep -v grep | wc -l)
echo "僵屍進程數量: $ZOMBIE_COUNT" >> $LOG_FILE

# 內存使用檢查
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
echo "內存使用率: ${MEMORY_USAGE}%" >> $LOG_FILE

# 創建授權JSON
cat > "$AUTH_FILE" << JSON_EOF
{
  "timestamp": "$TIMESTAMP",
  "reason": "$AUTH_REASON",
  "authorized_by": "Ricky_Lai",
  "system_status": {
    "zombie_count": $ZOMBIE_COUNT,
    "memory_usage": $MEMORY_USAGE,
    "uptime": "$(uptime -p)"
  },
  "expiry": "$(date -d "+24 hours" "+%Y-%m-%d %H:%M:%S")",
  "restart_command": "sudo reboot",
  "authorization_level": "full_system_restart"
}
JSON_EOF

echo "✅ 授權文件已創建: $AUTH_FILE" >> $LOG_FILE
echo "授權內容:" >> $LOG_FILE
cat "$AUTH_FILE" >> $LOG_FILE
echo "" >> $LOG_FILE

echo "🎯 授權完成!"
echo "授權原因: $AUTH_REASON"
echo "僵屍進程: $ZOMBIE_COUNT"
echo "內存使用: ${MEMORY_USAGE}%"
echo ""
echo "📋 下一步:"
echo "1. 手動執行重啟命令: sudo reboot"
echo "2. 或等待系統自動檢查到授權"
echo ""
echo "📝 授權文件位置: $AUTH_FILE"
