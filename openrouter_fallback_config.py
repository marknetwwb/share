#!/usr/bin/env python3
"""
OpenRouter Model Fallback 配置
按照建議方案實現免費模型fallback + retry機制
"""

import json
import os
import time
import asyncio
from typing import List, Dict, Any, Optional

class OpenRouterFallback:
    """OpenRouter Fallback 配置類"""
    
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
        
        self.timeout = 15000  # 15秒超時
        
    async def call_llm_with_retry(self, messages: List[Dict[str, Any]], retries: int = 3) -> Dict[str, Any]:
        """
        帶有retry機制嘅LLM調用
        """
        delay = 1000  # 初始延遲1秒
        
        for attempt in range(retries):
            try:
                # 嘗試所有模型
                for model in self.models:
                    try:
                        result = await self._call_single_model(model, messages)
                        return result
                    except Exception as e:
                        print(f"模型 {model} 失敗: {e.message}")
                        continue
                
                # 所有模型都失敗，增加延遲後重試
                if attempt < retries - 1:
                    await asyncio.sleep(delay / 1000)  # 轉換為秒
                    delay *= 2  # 指數退避
                    
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                await asyncio.sleep(delay / 1000)
                delay *= 2
                
        raise Exception(f"所有模型嘅 {retries} 次嘗試都失敗了")
    
    async def _call_single_model(self, model: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        調用單個模型
        """
        import aiohttp
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://localhost:3000",
                    "X-Title": "OpenRouter Fallback"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "timeout": self.timeout
                },
                timeout=aiohttp.ClientTimeout(total=self.timeout/1000)
            ) as response:
                
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")
    
    def get_models_info(self) -> Dict[str, Any]:
        """獲取模型信息"""
        return {
            "models": self.models,
            "total_models": len(self.models),
            "strategy": "fallback + retry",
            "timeout": self.timeout
        }

# 實用函數
async def call_llm_fallback(messages: List[Dict[str, Any]], api_key: str = None) -> Dict[str, Any]:
    """
    便捷嘅LLM調用函數
    """
    fallback = OpenRouterFallback(api_key)
    return await fallback.call_llm_with_retry(messages)

# 測試函數
async def test_fallback_system(api_key: str = None):
    """
    測試fallback系統
    """
    if not api_key:
        print("⚠️ 需要提供API Key進行測試")
        return
    
    fallback = OpenRouterFallback(api_key)
    
    print("=== 測試Fallback系統 ===")
    print(f"可用模型: {fallback.models}")
    
    test_messages = [
        {"role": "user", "content": "你好，請簡單介紹自己"}
    ]
    
    try:
        result = await fallback.call_llm_with_retry(test_messages)
        print("✅ Fallback系統測試成功")
        print(f"回應: {result.get('choices', [{}])[0].get('message', {}).get('content', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Fallback系統測試失敗: {e}")

if __name__ == "__main__":
    # 如果直接運行，進行測試
    import os
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if api_key:
        asyncio.run(test_fallback_system(api_key))
    else:
        print("請設置OPENROUTER_API_KEY環境變量")
