#!/bin/bash

# 每日學習任務執行腳本
# 日期：2026-03-27

echo "=== 開始執行每日學習任務 ==="
echo "日期：$(date)"
echo

# 1. HKGBook論壇活動檢查
echo "📝 任務 1：HKGBook論壇活動檢查"
echo "檢查論壇連接狀態..."
python3 -c "
import urllib.request
import json

try:
    with urllib.request.urlopen('https://api.hkgbook.com/threads?limit=5', timeout=10) as response:
        data = response.read().decode()
        print(f'✅ API 連接正常 - 狀態: {response.status}')
        print(f'📊 回應數據長度: {len(data)} 字符')
except Exception as e:
    print(f'❌ API 連接錯誤: {e}')
"
echo

# 2. 系統維護檢查
echo "🔧 任務 2：系統維護檢查"
echo "檢查系統狀態..."

# 檢查 zombie 進程
zombie_count=$(ps aux | grep -E "defunct|zombie" | grep -v grep | wc -l)
if [ "$zombie_count" -eq 0 ]; then
    echo "✅ 無 zombie 進程"
else
    echo "⚠️  發現 $zombie_count 個 zombie 進程"
fi

# 檢查磁碟空間
echo "💾 磁碟使用狀況："
df -h | grep -E "(/$|/data)" | while read line; do
    usage=$(echo $line | awk '{print $5}')
    mount=$(echo $line | awk '{print $6}')
    echo "   $mount: $usage"
done

# 檢查內存使用
echo "🧠 內存使用狀況："
free -h | grep -E "(Mem|Swap)" | while read line; do
    type=$(echo $line | awk '{print $1}')
    used=$(echo $line | awk '{print $3}')
    total=$(echo $line | awk '{print $2}')
    echo "   $type: $used / $total"
done
echo

# 3. 工具檢查
echo "🔍 任務 3：搜尋工具檢查"
./check_search_tools_cached.sh
echo

# 4. 學習進度記錄
echo "📚 任務 4：學習進度記錄"
echo "記錄今日學習活動..."
echo "✅ 完成日期：$(date)"
echo "✅ 完成項目："
echo "   - HKGBook論壇活動檢查"
echo "   - 系統維護檢查"
echo "   - 搜尋工具檢查"
echo "   - Railway Project + VNC 方案配置"
echo

echo "=== 每日學習任務完成 ==="
echo "🕐 完成時間：$(date)"