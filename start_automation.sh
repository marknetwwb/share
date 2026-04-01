#!/bin/bash

# 🚀 自動化工作流程啟動器
# 功能：啟動優化後的工作流程自動化系統

echo "🚀 啟動自動化工作流程系統..."
echo "================================"

# 設置日誌目錄
LOG_DIR="/data/workspace/logs"
mkdir -p "$LOG_DIR"

# 啟動自動化系統
echo "1. 啟動自動化工作流程..."
chmod +x /data/workspace/automation_workflow_v2.sh

# 創建後台進程
echo "2. 創建後台執行進程..."
nohup /data/workspace/automation_workflow_v2.sh > "$LOG_DIR/automation.log" 2>&1 &

# 獲取進程ID
PROCESS_PID=$!
echo "3. 自動化系統進程ID: $PROCESS_PID"

# 保存進程ID
echo "$PROCESS_PID" > "$LOG_DIR/automation.pid"

# 驗證啟動
echo "4. 驗證系統啟動狀態..."
sleep 2

if ps -p $PROCESS_PID > /dev/null; then
    echo "✅ 自動化系統啟動成功！"
    echo "📋 進程ID: $PROCESS_PID"
    echo "📄 日誌文件: $LOG_DIR/automation.log"
    echo "⏰ 系統將在後台持續運行"
    echo ""
    echo "🎯 任務執行頻率："
    echo "   🔴 高優先級: 每30分鐘"
    echo "   🟡 中優先級: 每2小時"
    echo "   🟢 低優先級: 每6小時"
    echo ""
    echo "💡 創作模式可以通過配置文件切換"
    echo "🔧 系統監控已啟動，自動檢查工具狀態"
else
    echo "❌ 自動化系統啟動失敗"
    exit 1
fi

echo ""
echo "🎉 工作流程優化系統已成功啟動！"
echo "📊 您可以通過以下方式監控系統："
echo "   - 查看日誌: tail -f $LOG_DIR/automation.log"
echo "   - 檢查進程: ps aux | grep automation_workflow_v2.sh"
echo "   - 停止系統: kill $(cat $LOG_DIR/automation.pid)"