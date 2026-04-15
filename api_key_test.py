#!/usr/bin/env python3
"""
簡單API Key測試
"""

import os
import urllib.request
import json

def test_api_key():
    # 測試不同嘅API Key配置
    test_keys = [
        '764229241579d0bcf83c9d749d07948979131dbd',
        os.getenv('OPENROUTER_API_KEY', '')
    ]
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    messages = [{"role": "user", "content": "測試"}]
    
    for i, api_key in enumerate(test_keys):
        if not api_key:
            print(f"⚠️ 測試 {i+1}: API Key為空")
            continue
            
        print(f"\n=== 測試 {i+1} ===")
        print(f"API Key: {api_key[:20]}...")
        
        data = {
            "model": "glm-4-flash:free",
            "messages": messages,
            "timeout": 10
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://localhost:3000",
                "X-Title": "API Key Test"
            },
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    result = json.loads(response.read().decode('utf-8'))
                    print(f"✅ 測試 {i+1} 成功！")
                    print(f"模型: {result.get('model', 'N/A')}")
                    return True
                else:
                    error_text = response.read().decode('utf-8')
                    print(f"❌ 測試 {i+1} 失敗: HTTP {response.status}")
                    print(f"錯誤: {error_text}")
        except Exception as e:
            print(f"❌ 測試 {i+1} 連接失敗: {e}")
    
    return False

if __name__ == "__main__":
    print("測試OpenRouter API Key...")
    success = test_api_key()
    
    if success:
        print("\n🎉 有API Key可以正常工作！")
    else:
        print("\n❌ 所有API Key都測試失敗")
        print("按照你嘅建議，需要:")
        print("1. 申請新嘅OpenRouter API Key")
        print("2. 確保Key有圖像生成權限")
        print("3. 實施fallback機制")
