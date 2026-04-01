#!/bin/bash
# 搜尋工具檢查腳本
# 確保使用正確嘅搜尋工具

echo "=== 搜尋工具檢查 ==="
echo "檢查日期: $(date)"
echo "檢查目標: 確保使用 Serper.dev，唔係 Brave Search"
echo ""

# 檢查 Serper.dev 工具文件是否存在
if [ -f "serper_search_function.py" ]; then
    echo "✅ Serper.dev 工具文件存在"
else
    echo "❌ Serper.dev 工具文件不存在"
    exit 1
fi

# 檢查 API Key 是否存在
if grep -q "764229241579d0bcf83c9d749d07948979131dbd" serper_search_function.py; then
    echo "✅ Serper.dev API Key 已配置"
else
    echo "❌ Serper.dev API Key 未配置"
    exit 1
fi

# 測試搜索功能
echo "測試搜索功能..."
python3 serper_search_function.py > /tmp/search_test.log 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Serper.dev 測試成功"
else
    echo "❌ Serper.dev 測試失敗"
    cat /tmp/search_test.log
    exit 1
fi

echo ""
echo "🎉 搜尋工具檢查通過，可以安全使用 Serper.dev"
echo "📝 記住：唔可以使用 web_search 工具（Brave Search）"
echo "💡 核心：Serper.dev，唔係 Brave Search！"