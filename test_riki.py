#!/usr/bin/env python3
"""
Riki 測試腳本
測試 Riki 嘅基本功能
"""

import sys
import os

# 添加虛擬環境路徑
sys.path.insert(0, '/data/workspace/aigis_env/lib/python3.11/site-packages')

def test_riki_connection():
    """測試 Riki 連接狀態"""
    try:
        from aigis import Guard
        
        print("🛡️  Riki 安全測試開始...")
        print("=" * 50)
        
        # 創建安全守衛
        guard = Guard(policy="strict")
        
        # 測試 Riki 可以處理嘅正常對話
        test_messages = [
            "你好 Riki，我想了解 HKGBook 論壇嘅發帖策略",
            "幫我分析下論壇入面嘅熱門話題",
            "我想要喺 creative 板塊發一篇小說"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📝 測試消息 {i}: {message}")
            
            # 安全檢查
            result = guard.check_input(message)
            
            print(f"風險評分: {result.risk_score}")
            print(f"風險等級: {result.risk_level}")
            print(f"是否封鎖: {result.blocked}")
            
            if result.blocked:
                print("❌ 消息被安全系統封鎖")
            else:
                print("✅ 消息安全，可以處理")
        
        print("\n" + "=" * 50)
        print("✅ Riki 安全測試完成！")
        print("🎯 現在可以喺 Telegram 中同 @Riki_SuperBot 談話")
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    test_riki_connection()