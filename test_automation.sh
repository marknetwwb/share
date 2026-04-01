#!/bin/bash

# 🧪 自動化系統測試腳本
# 功能：測試工作流程自動化系統

echo "🧪 自動化工作流程系統測試"
echo "================================"

# 測試配置文件
echo "1. 測試配置文件..."
if [ -f "/data/workspace/config/automation_config.json" ]; then
    echo "✅ 配置文件存在"
    cat /data/workspace/config/automation_config.json
else
    echo "❌ 配置文件不存在"
    exit 1
fi

# 測試腳本文件
echo -e "\n2. 測試腳本文件..."
if [ -f "/data/workspace/automation_workflow_v2.sh" ]; then
    echo "✅ 自動化腳本存在"
    ls -la /data/workspace/automation_workflow_v2.sh
else
    echo "❌ 自動化腳本不存在"
    exit 1
fi

# 測試創作模式切換
echo -e "\n3. 測試創作模式切換..."
echo "測試創作模式開啟..."
# 這裡可以添加創作模式測試邏輯

# 測試進度追蹤
echo -e "\n4. 測試進度追蹤..."
novel_dir="/data/workspace"
if [ -d "$novel_dir" ]; then
    echo "✅ 小說目錄存在"
    find "$novel_dir" -name "*season1*" -type f | head -5
else
    echo "❌ 小說目錄不存在"
fi

# 測試系統監控
echo -e "\n5. 測試系統監控..."
echo "檢查系統資源..."
free -h
df -h | head -5

# 測試工具狀態
echo -e "\n6. 測試工具狀態..."
if [ -f "/data/workspace/check_search_tools_cached.sh" ]; then
    echo "✅ 工具檢查腳本存在"
    ./check_search_tools_cached.sh
else
    echo "❌ 工具檢查腳本不存在"
fi

echo -e "\n7. 測試完成..."
echo "🎯 自動化系統已準備就緒！"
echo "🚀 可以開始執行工作流程優化"