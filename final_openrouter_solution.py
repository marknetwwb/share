#!/usr/bin/env python3
"""
最終OpenRouter API Key申請和配置方案
"""

import json
import os

def final_solution():
    """最終解決方案"""
    
    print("=== 最終OpenRouter API Key申請方案 ===")
    print()
    print("🎯 問題確認：")
    print("✅ 系統OpenRouter連接正常（能夠回應）")
    print("❌ 當前API Key無法進行圖像生成（401錯誤）")
    print("🎨 需要新的API Key來實現圖像生成")
    print()
    
    print("📋 建議的解決步驟：")
    print("1. 訪問: https://openrouter.ai/keys")
    print("2. 登錄或創建帳戶")
    print("3. 點擊 'Create API Key'")
    print("4. 命名: OpenClaw-Image-Generation")
    print("5. 選擇正確的權限（包括圖像生成）")
    print("6. 申請永不過期的Key")
    print("7. 複製新的API Key")
    print("8. 提供給我進行配置")
    print()
    
    print("⚡ 配置後的預期效果：")
    print("✅ Toyota Alphard 30H漫畫風圖像生成")
    print("✅ 豪華酒店背景")
    print("✅ 使用Seedream 4.5模型")
    print("✅ 完整的圖像生成功能")
    print()
    
    # 更新HEARTBEAT.md
    update_heartbeat_md()
    
    print("📝 HEARTBEAT.md已更新，記錄了API Key問題和解決方案")
    print("🎯 系統已準備好接收新的API Key")

def update_heartbeat_md():
    """更新HEARTBEAT.md記錄API Key問題"""
    
    heartbeat_file = "HEARTBEAT.md"
    
    try:
        # 讀取當前內容
        with open(heartbeat_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加新的問題記錄
        new_entry = f"""

### 🔧 **API Key問題處理**
- **問題**: OpenRouter API Key測試失敗 (401 Unauthorized)
- **影響**: 圖像生成API調用失敗
- **解決方案**: 需要重新申請有效的API Key
- **進度**: 待處理 - 需要提供新的API Key
- **目標**: 實現Toyota Alphard 30H漫畫風圖像生成

### 📅 **2026-03-20 事件記錄**
- **時間**: 凌晨5:43
- **事件**: 嘗試圖像生成失敗
- **原因**: OpenRouter API Key權限問題
- **狀態**: 等待新的API Key
- **負責人**: Airi
"""
        
        # 更新內容
        updated_content = content.replace(
            "## 📅 日期：2026年3月19日（星期四）",
            f"## 📅 日期：2026年3月20日（星期五）{new_entry}"
        )
        
        # 寫回文件
        with open(heartbeat_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ HEARTBEAT.md已更新")
        
    except Exception as e:
        print(f"❌ 更新HEARTBEAT.md失敗: {e}")

if __name__ == "__main__":
    final_solution()