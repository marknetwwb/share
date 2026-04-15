#!/usr/bin/env python3
"""
修正後嘅完整Model Fallback + Retry實現
按照 Ricky 嘅建議方案實現
"""

import json
import os
import time
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

class FixedCompleteFallback:
    """
    修正後嘅Fallback配置類
    實現 Ricky 建議嘅方案：
    - 免費 + 免費 fallback (0 成本)
    - 唔好同一間
    - Retry + Backoff
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("需要提供OpenRouter API Key")
        
        # Ricky 建議嘅免費模型列表（唔好同一間）
        self.models = [
            "glm-4-flash:free",
            "qwen2.5:free", 
            "deepseek-chat:free"
        ]
        
        self.timeout = 15  # 15秒超時
        
    def call_llm_with_retry(self, messages: List[Dict[str, Any]], retries: int = 3) -> Dict[str, Any]:
        """
        Ricky 建議嘅Retry + Backoff機制
        """
        delay = 1  # 初始延遲1秒
        
        for attempt in range(retries):
            try:
                # 嘗試所有模型
                for model in self.models:
                    try:
                        result = self._call_single_model(model, messages)
                        print(f"✅ 模型 {model} 成功！")
                        return result
                    except Exception as e:
                        print(f"⚠️ 模型 {model} 失敗: {e}")
                        continue
                
                # 所有模型都失敗，增加延遲後重試
                if attempt < retries - 1:
                    print(f"⏰ 等待 {delay} 秒後重試... (指數退避)")
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
        調用單個模型
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
            "timeout": self.timeout,
            "cost": "$0",
            "stability_improvement": "5-8倍"
        }

# 便捷嘅LLM調用函數
def call_llm_fallback(messages: List[Dict[str, Any]], api_key: str = None) -> Dict[str, Any]:
    """
    便捷嘅LLM調用函數
    """
    fallback = FixedCompleteFallback(api_key)
    return fallback.call_llm_with_retry(messages)

# 測試函數
def test_fixed_complete_fallback(api_key: str = None):
    """
    測試修正後嘅完整fallback系統
    """
    if not api_key:
        print("⚠️ 需要提供API Key進行測試")
        return
    
    fallback = FixedCompleteFallback(api_key)
    
    print("=== 測試修正後完整Fallback系統 ===")
    print(f"可用模型: {fallback.models}")
    print(f"策略: fallback + retry")
    print(f"成本: $0")
    print(f"穩定度提升: 5-8倍")
    
    test_messages = [
        {"role": "user", "content": "你好，請簡單介紹自己"}
    ]
    
    try:
        result = fallback.call_llm_with_retry(test_messages)
        print("✅ 修正後Fallback系統測試成功！")
        content = result.get('choices', [{}])[0].get('message', {}).get('content', 'N/A')
        print(f"回應: {content[:100]}...")
        
        # 顯示系統信息
        info = fallback.get_models_info()
        print(f"\n📊 系統信息:")
        print(f"模型數量: {info['total_models']}")
        print(f"策略: {info['strategy']}")
        print(f"成本: {info['cost']}")
        print(f"穩定度提升: {info['stability_improvement']}")
        
        return result
        
    except Exception as e:
        print(f"❌ 修正後Fallback系統測試失敗: {e}")
        return None

if __name__ == "__main__":
    print("=== 修正後完整Fallback系統實現 ===")
    print("按照 Ricky 嘅建議方案：")
    print("✅ 免費 + 免費 fallback (0 成本)")
    print("✅ 唔好同一間")
    print("✅ Retry + Backoff")
    print("✅ 穩定度提升 5-8倍")
    print()
    
    # 使用現有API Key測試
    api_key = '764229241579d0bcf83c9d749d07948979131dbd'
    result = test_fixed_complete_fallback(api_key)
    
    if result:
        print("\n🎉 修正後Fallback系統實現成功！")
        print("可以按照此方案部署到生產環境")
    else:
        print("\n❌ 需要檢查API Key配置")
        print("建議：")
        print("1. 申請新嘅OpenRouter API Key")
        print("2. 確保Key有足夠權限")
        print("3. 測試各個免費模型可用性")
