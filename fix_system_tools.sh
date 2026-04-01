#!/bin/bash
# 系統工具修復腳本 - Riki Subagent 優化

echo "🔧 開始修復 Riki Subagent 系統工具..."

# 創建必要嘅符號鏈接
echo "📝 創建系統工具符號鏈接..."

# 檢查並創建 ping 符號鏈接
if [ ! -f "/bin/ping" ]; then
    echo "🔍 檢查 ping 命令..."
    PING_PATH=$(which ping || which ping6 || echo "")
    if [ -n "$PING_PATH" ]; then
        ln -sf "$PING_PATH" /bin/ping
        echo "✅ 已創建 ping 符號鏈接: $PING_PATH"
    else
        echo "⚠️ 未找到 ping 命令，跳過創建"
    fi
fi

# 檢查並創建 pip 符號鏈接
if [ ! -f "/bin/pip" ]; then
    echo "🔍 檢查 pip 命令..."
    PIP_PATH=$(which pip3 || which pip || echo "")
    if [ -n "$PIP_PATH" ]; then
        ln -sf "$PIP_PATH" /bin/pip
        echo "✅ 已創建 pip 符號鏈接: $PIP_PATH"
    else
        echo "⚠️ 未找到 pip 命令，跳過創建"
    fi
fi

# 檢查並創建 tts 符號鏈接
if [ ! -f "/bin/tts" ]; then
    echo "🔍 檢查 tts 命令..."
    # tts 係 OpenClaw 內建功能，唔需要系統級別嘅符號鏈接
    echo "ℹ️ tts 係 OpenClaw 內建功能，唔需要符號鏈接"
fi

echo "🔧 系統工具修復完成！"

# 測�试基本命令
echo "🧪 測試基本命令..."
echo "✅ Python3 位置: $(which python3)"
echo "✅ Python3 版本: $(python3 --version 2>/dev/null || echo '未知')"

if [ -f "/bin/ping" ]; then
    echo "✅ Ping 命令可用"
else
    echo "⚠️ Ping 命令仍然不可用"
fi

if [ -f "/bin/pip" ]; then
    echo "✅ Pip 命令可用"
else
    echo "⚠️ Pip 命令仍然不可用"
fi

echo "🎯 下一步建議：重啟 OpenClaw 服務以應用新配置"