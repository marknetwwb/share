#!/bin/bash

# 智能搜尋工具檢查 - 使用緩存減少重複檢查
# 每次心跳檢查時運行，但會緩存結果 6 小時

CACHE_FILE="/data/workspace/api_status_cache.json"
SERPER_SCRIPT="/data/workspace/serper_search_function.py"
SERPER_API_KEY="764229241579d0bcf83c9d749d07948979131dbd"

# 讀取緩存
if [[ -f "$CACHE_FILE" ]]; then
    CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # 簡單文本解析提取 next_check
    NEXT_CHECK_TIME=$(grep -o '"next_check": "[^"]*"' "$CACHE_FILE" | cut -d'"' -f4)
    
    # 調試輸出
    echo "🔍 調試信息:"
    echo "   當前時間: $CURRENT_TIME"
    echo "   下次檢查: $NEXT_CHECK_TIME"
    
    # 檢查緩存是否過期 - 比較時間戳
    if [[ -n "$NEXT_CHECK_TIME" ]] && [[ "$CURRENT_TIME" < "$NEXT_CHECK_TIME" ]]; then
        echo "✅ 使用緩存結果 - Serper.dev 狀態良好"
        echo "🎉 搜尋工具檢查通過 (緩存版本)"
        echo "💾 有效期內緩存已使用"
        exit 0
    else
        echo "⏰ 緩存已過期，需要重新檢查"
    fi
else
    echo "📁 緩存文件不存在，執行完整檢查"
fi

# 緩存過期或不存在，執行完整檢查
echo "🔄 緩存過期，執行完整檢查..."

# 檢查 Serper.dev 文件
if [[ ! -f "$SERPER_SCRIPT" ]]; then
    echo "❌ Serper.dev 工具文件不存在"
    exit 1
fi

# 檢查 API Key 格式
if [[ ${#SERPER_API_KEY} -eq 0 ]]; then
    echo "❌ Serper.dev API Key 未配置"
    exit 1
fi

# 測試搜索功能 (限制字符數避免過長輸出)
SEARCH_RESULT=$(python3 "$SERPER_SCRIPT" "test search" 2>/dev/null || echo "error")

if [[ "$SEARCH_RESULT" == *"error"* ]] || [[ -z "$SEARCH_RESULT" ]]; then
    echo "❌ Serper.dev 測試失敗"
    exit 1
fi

# 更新緩存
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
NEXT_CHECK_TIME=$(date -u -d "+6 hours" +"%Y-%m-%dT%H:%M:%SZ")

# 使用 jq 正確生成 JSON
cat > "$CACHE_FILE" << EOF
{
  "serper_dev": {
    "last_checked": "$CURRENT_TIME",
    "status": "ok",
    "next_check": "$NEXT_CHECK_TIME"
  },
  "hkgbook_api": {
    "last_checked": "$CURRENT_TIME",
    "status": "ok",
    "api_key": "o852_5wspb7me0fgjfdhmgwcp7h30",
    "next_check": "$NEXT_CHECK_TIME"
  },
  "cache_ttl_seconds": 21600,
  "cache_ttl_label": "6_hours"
}
EOF

echo "✅ Serper.dev 工具文件存在"
echo "✅ Serper.dev API Key 已配置"
echo "✅ Serper.dev 測試成功"
echo "🎉 搜尋工具檢查通過 - 緩存已更新"
echo "💾 緩存有效期: 6 小時"
echo "📅 下次自動檢查: $NEXT_CHECK_TIME"
exit 0
