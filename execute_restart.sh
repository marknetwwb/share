#!/bin/bash

# 手動執行重啟腳本
# 檢查授權並執行重啟

AUTH_FILE="/data/workspace/restart_authorization.json"
LOG_FILE="/data/workspace/execute_restart.log"
FLAG_FILE="/data/workspace/restart_pending.flag"

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "=== 重啟執行請求 $TIMESTAMP ===" >> "$LOG_FILE"

# 檢查授權文件
if [ ! -f "$AUTH_FILE" ]; then
    echo "❌ 錯誤: 沒有授權文件" >> "$LOG_FILE"
    echo "請先執行: ./grant_restart_permission.sh [原因]"
    exit 1
fi

# 讀取授權信息
echo "📋 讀取授權信息..." >> "$LOG_FILE"
cat "$AUTH_FILE" >> "$LOG_FILE"

# 檢查授權是否過期
EXPIRY=$(grep -o '"expiry": "[^"]*"' "$AUTH_FILE" | cut -d'"' -f4)
if [ -n "$EXPIRY" ]; then
    EXPIRY_TS=$(date -d "$EXPIRY" +%s)
    CURRENT_TS=$(date +%s)
    
    if [ $CURRENT_TS -gt $EXPIRY_TS ]; then
        echo "❌ 授權已過期" >> "$LOG_FILE"
        exit 1
    else
        echo "✅ 授權有效" >> "$LOG_FILE"
    fi
fi

echo "⚠️ 即將執行系統重啟" >> "$LOG_FILE"
echo "執行時間: $TIMESTAMP" >> "$LOG_FILE"
echo "授權原因: $(grep -o '"reason": "[^"]*"' "$AUTH_FILE" | cut -d'"' -f4)" >> "$LOG_FILE"

# 創建執行標誌
cat > "$FLAG_FILE" << JSON_EOF
{
  "timestamp": "$TIMESTAMP",
  "command": "sudo reboot",
  "status": "pending",
  "auth_file": "$AUTH_FILE"
}
JSON_EOF

echo "🎯 重啟標誌已創建" >> "$LOG_FILE"
echo "請手動執行: sudo reboot" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "📝 重啟準備完成!"
echo "授權信息:"
cat "$AUTH_FILE"
echo ""
echo "🚀 下一步:"
echo "手動執行: sudo reboot"
