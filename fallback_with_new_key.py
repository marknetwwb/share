#!/usr/bin/env python3
"""
使用新API Key嘅完整Fallback實現
"""

import json
import urllib.request
import time

# 新嘅API Key
NEW_API_KEY = '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'

class FallbackWithNewKey:
    def __init__(self):
        self.api_key = NEW_API_KEY
        self.models = [
            "glm-4-flash:free",
            "qwen2.5:free", 
            "deepseek-chat:free"
        ]
        self.timeout = 15
        
    def call_llm_with_retry(self, messages, retries=3):
        delay = 1
        
        for attempt in range(retries):
            try:
                for model in self.models:
                    try:
                        result = self._call_single_model(model, messages)
                        print(f"✅ 模型 {model} 成功！")
                        return result
                    except Exception as e:
                        print(f"⚠️ 模型 {model} 失敗: {e}")
                        continue
                
                if attempt < retries - 1:
                    print(f"⏰ 等待 {delay} 秒後重試...")
                    time.sleep(delay)
                    delay *= 2
                    
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(delay)
                delay *= 2
                
        raise Exception(f"所有模型嘅 {retries} 次嘗試都失敗了")
    
    def _call_single_model(self, model, messages):
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        data = {
            "model": model,
            "messages": messages,
            "timeout": self.timeout
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://localhost:3000",
                "X-Title": "New API Fallback"
            },
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                if response.status == 200:
                    result = json.loads(response.read().decode('utf-8'))
                    return result
                else:
                    error_text = response.read().decode('utf-8')
                    raise Exception(f"HTTP {response.status}: {error_text}")
        except urllib.error.HTTPError as e:
            error_text = e.read().decode('utf-8')
            raise Exception(f"HTTP {e.code}: {error_text}")
        except Exception as e:
            raise Exception(f"連接失敗: {e}")

def test_new_key_fallback():
    fallback = FallbackWithNewKey()
    
    print("=== 測試新API Key嘅Fallback系統 ===")
    print(f"API Key: {NEW_API_KEY[:30]}...")
    print(f"可用模型: {fallback.models}")
    
    test_messages = [{"role": "user", "content": "你好"}]
    
    try:
        result = fallback.call_llm_with_retry(test_messages)
        print("✅ 新API Key Fallback系統測試成功！")
        content = result.get('choices', [{}])[0].get('message', {}).get('content', 'N/A')
        print(f"回應: {content[:100]}...")
        return True
    except Exception as e:
        print(f"❌ 新API Key Fallback系統測試失敗: {e}")
        return False

if __name__ == "__main__":
    print("=== 使用新API Key嘅Fallback系統 ===")
    success = test_new_key_fallback()
    
    if success:
        print("\n🎉 新API Key完全正常工作！")
    else:
        print("\n❌ 新API Key仍然有問題")
        print("建議：")
        print("1. 檢查API Key是否正確")
        print("2. 確認Key有足夠權限")
        print("3. 可能需要等待Key生效")
