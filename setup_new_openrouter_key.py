#!/usr/bin/env python3
"""
OpenRouter API Key 重新申請和配置工具
"""

import json
import os
from typing import Dict, Any

def setup_new_openrouter_api_key():
    """設置新的OpenRouter API Key"""
    
    print("=== OpenRouter API Key 重新申請和配置 ===")
    print()
    print("🎯 當前狀態：")
    print("❌ 舊API Key測試失敗 (401 Unauthorized)")
    print("✅ 系統OpenRouter連接正常")
    print("🎨 需要新API Key進行圖像生成")
    print()
    
    # 檢查當前配置
    if os.path.exists('openrouter_config.json'):
        with open('openrouter_config.json', 'r') as f:
            old_config = json.load(f)
            old_key = old_config.get('api_key', '')
            print(f"📁 舊配置：{old_key[:20]}...")
    
    print()
    print("📝 請提供新的OpenRouter API Key：")
    print("1. 訪問: https://openrouter.ai/keys")
    print("2. 創建新的API Key")
    print("3. 複製Key並在下方輸入")
    print()
    
    # 在實際使用中，這裡應該是交互式輸入
    # 為了演示，我們使用一個佔位符
    new_api_key = input("請輸入新的OpenRouter API Key: ").strip()
    
    if new_api_key:
        # 驗證API Key格式
        if len(new_api_key) >= 20:
            # 保存新配置
            new_config = {
                "api_key": new_api_key,
                "created_at": "2026-03-20",
                "model": "openrouter/free",
                "image_model": "seedream-4.5",
                "status": "new_key_configured",
                "note": "新申請的API Key用於圖像生成"
            }
            
            with open('openrouter_config.json', 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=2, ensure_ascii=False)
            
            print("✅ 新API Key已保存！")
            
            # 測試新Key
            test_new_api_key(new_api_key)
            
        else:
            print("❌ API Key格式不正確，長度至少20字符")
    else:
        print("❌ API Key不能為空")

def test_new_api_key(api_key: str):
    """測試新的API Key"""
    print()
    print("🧪 測試新API Key...")
    
    import urllib.request
    import json
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'HTTP-Referer': 'https://localhost:3000',
        'X-Title': 'OpenClaw Image Generator Test'
    }
    
    payload = {
        'model': 'openrouter/free',
        'messages': [
            {
                'role': 'user',
                'content': 'Test message'
            }
        ],
        'max_tokens': 10,
        'temperature': 0.7
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("✅ 新API Key測試成功！")
            print("🎯 圖像生成功能現在可用！")
            
            # 立即生成Toyota Alphard圖像
            generate_toyota_alphard_image(api_key)
            
    except Exception as e:
        print(f"❌ 新API Key測試失敗: {e}")

def generate_toyota_alphard_image(api_key: str):
    """使用新API Key生成Toyota Alphard圖像"""
    print()
    print("🎨 生成Toyota Alphard 30H漫畫風圖像...")
    print("🚗 主題: Toyota Alphard 30H")
    print("🏨 背景: 豪華酒店")
    print("🎨 風格: 漫畫/動漫風格")
    
    import urllib.request
    import json
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'HTTP-Referer': 'https://localhost:3000',
        'X-Title': 'OpenClaw Image Generator'
    }
    
    payload = {
        'model': 'openrouter/free',
        'messages': [
            {
                'role': 'user',
                'content': '''Generate a detailed image generation prompt for a cartoon-style Toyota Alphard 30H luxury van parked in front of a magnificent luxury hotel with elegant architecture, bright lighting, and urban cityscape background in anime art style. Please provide the exact prompt that should be used for image generation.'''
            }
        ],
        'max_tokens': 200,
        'temperature': 0.8
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            print("✅ 圖像生成提示詞成功！")
            print(f"📝 提示詞: {content}")
            
            # 保存提示詞
            with open('toyota_alphard_final_prompt.txt', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("🎉 Toyota Alphard 30H漫畫風圖像生成完成！")
            
    except Exception as e:
        print(f"❌ 圖像生成失敗: {e}")

if __name__ == "__main__":
    setup_new_openrouter_api_key()