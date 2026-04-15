#!/usr/bin/env python3
"""
簡化版Fallback測試 - 使用標準庫實現
"""

import json
import os
import time
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

class SimpleFallback:
    """簡化版Fallback配置類"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("需要提供OpenRouter API Key")
        
        # 建議的免費模型列表（唔好同一間）
        self.models = [
            "glm-4-flash:free",
            "qwen2.5:free", 
            "deepseek-chat:free"
        ]
        
        self.timeout = 15  # 15秒超時
        
    def call_llm_with_retry(self, messages: List[Dict[str, Any]], retries: int = 3) -> Dict[str, Any]:
        """
        帶有retry機制嘅LLM調用（使用urllib）
        """
        delay = 1  # 初始延遲1秒
        
        for attempt in range(retries):
            try:
                # 嘗試所有模型
                for model in self.models:
                    try:
                        result = self._call_single_model(model, messages)
                        return result
                    except Exception as e:
                        print(f"模型 {model} 失敗: {e}")
                        continue
                
                # 所有模型都失敗，增加延遲後重試
                if attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2  # 指數退避
                    
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(delay)
                delay *= 2
                
        raise Exception(f"所有模型嘅 {retries} 次嘗試都失敗了")
    
    def _call_single_model(self, model: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        調用單個模型（使用urllib）
        """
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
                "X-Title": "OpenRouter Fallback"
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
    
    def get_models_info(self) -> Dict[str, Any]:
        """獲取模型信息"""
        return {
            "models": self.models,
            "total_models": len(self.models),
            "strategy": "fallback + retry",
            "timeout": self.timeout
        }

# 實用函數
def call_llm_fallback(messages: List[Dict[str, Any]], api_key: str = None) -> Dict[str, Any]:
    """
    便捷嘅LLM調用函數
    """
    fallback = SimpleFallback(api_key)
    return fallback.call_llm_with_retry(messages)

# 測試函數
def test_fallback_system(api_key: str = None):
    """
    測試fallback系統
    """
    if not api_key:
        print("⚠️ 需要提供API Key進行測試")
        return
    
    fallback = SimpleFallback(api_key)
    
    print("=== 測試Fallback系統 ===")
    print(f"可用模型: {fallback.models}")
    
    test_messages = [
        {"role": "user", "content": "你好，請簡單介紹自己"}
    ]
    
    try:
        result = fallback.call_llm_with_retry(test_messages)
        print("✅ Fallback系統測試成功")
        content = result.get('choices', [{}])[0].get('message', {}).get('content', 'N/A')
        print(f"回應: {content[:100]}...")
        
        return result
        
    except Exception as e:
        print(f"❌ Fallback系統測試失敗: {e}")
        return None

if __name__ == "__main__":
    # 如果直接運行，進行測試
    api_key = os.getenv('OPENROUTER_API_KEY') or '764229241579d0bcf83c9d749d07948979131dbd'
    
    print(f"使用API Key: {api_key[:20]}...")
    result = test_fallback_system(api_key)
    
    if result:
        print("\n🎉 測試成功！Fallback系統可以正常運行")
    else:
        print("\n❌ 測試失敗，需要檢查API Key")
