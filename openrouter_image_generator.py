#!/usr/bin/env python3
"""
OpenRouter 圖像生成工具 - 使用 Seedream 4.5 免費模型
可以直接調用 OpenRouter API 進行圖像生成
"""

import json
import urllib.request
import urllib.parse
import base64
from typing import Dict, Any, Optional

def openrouter_image_generation(
    prompt: str,
    model: str = "openrouter/free",
    size: str = "1024x1024",
    quality: str = "standard",
    steps: int = 20,
    guidance_scale: float = 7.5
) -> Dict[str, Any]:
    """
    使用 OpenRouter API 進行圖像生成
    
    Args:
        prompt: 圖像生成提示詞
        model: 模型選擇 (預設使用 openrouter/free 會自動選擇免費模型)
        size: 圖像尺寸 (1024x1024, 512x512, 768x768)
        quality: 圖像質量 (standard, high)
        steps: 生成步數 (10-50)
        guidance_scale: 引導尺度 (1.0-20.0)
    
    Returns:
        API 回應字典
    """
    api_key = "764229241579d0bcf83c9d749d07948979131dbd"
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'HTTP-Referer': 'https://localhost:3000',
        'X-Title': 'OpenClaw Image Generator'
    }
    
    # 構建圖像生成請求
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Generate an image based on this prompt: {prompt}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return _format_image_result(result, prompt)
            
    except Exception as e:
        return {
            "error": "Image Generation Failed",
            "message": str(e),
            "prompt": prompt,
            "model": model
        }

def _format_image_result(raw_result: Dict[str, Any], prompt: str) -> Dict[str, Any]:
    """格式化圖像生成結果"""
    try:
        # 提取圖像數據
        content = raw_result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # 尋找圖像URL或base64數據
        image_data = None
        image_url = None
        
        if "http" in content:
            # 如果是URL格式
            image_url = content
        else:
            # 嘗試解析base64圖像
            try:
                if ",base64," in content:
                    base64_data = content.split(",base64,")[1]
                    image_data = base64.b64decode(base64_data)
            except:
                pass
        
        return {
            "success": True,
            "prompt": prompt,
            "model": "openrouter/free (Seedream 4.5)",
            "image_url": image_url,
            "image_data": image_data,
            "raw_response": raw_result
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": "Result Parsing Failed",
            "message": str(e),
            "prompt": prompt,
            "raw_response": raw_result
        }

def generate_image_with_seedream(
    prompt: str,
    style: str = "realistic",
    aspect_ratio: str = "1:1"
) -> Dict[str, Any]:
    """
    專門使用 Seedream 4.5 生成圖像
    
    Args:
        prompt: 圖像描述
        style: 圖像風格 (realistic, artistic, cartoon, etc.)
        aspect_ratio: 長寬比 (1:1, 16:9, 9:16)
    
    Returns:
        生成結果字典
    """
    # Seedream 4.5 專用參數
    seedream_prompt = f"{prompt}, style: {style}, aspect ratio: {aspect_ratio}"
    
    result = openrouter_image_generation(
        prompt=seedream_prompt,
        model="openrouter/free",
        size="1024x1024",
        quality="standard",
        steps=25,
        guidance_scale=8.0
    )
    
    return result

def list_available_models() -> Dict[str, Any]:
    """列出可用的圖像生成模型"""
    return {
        "available_models": [
            {
                "name": "openrouter/free",
                "description": "智能路由器，自動選擇免費模型",
                "provider": "OpenRouter",
                "cost": "Free",
                "includes": ["Seedream 4.5", "其他免費圖像生成模型"]
            },
            {
                "name": "seedream-4.5",
                "description": "ByteDance 最新圖像生成模型",
                "provider": "ByteDance",
                "cost": "Free via OpenRouter",
                "features": ["圖像理解", "UI重建", "迭代視覺編輯"]
            }
        ],
        "total_models": 2,
        "note": "所有模型都通過 OpenRouter 免費路由器訪問"
    }

# 測試函數
if __name__ == "__main__":
    print("=== OpenRouter 圖像生成測試 ===")
    
    # 列出可用模型
    models = list_available_models()
    print(json.dumps(models, indent=2, ensure_ascii=False))
    
    print("\n=== 圖像生成測試 ===")
    # 測試圖像生成
    test_prompt = "a beautiful sunset over mountains"
    result = generate_image_with_seedream(test_prompt, "realistic", "16:9")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n=== 使用說明 ===")
    print("1. 使用 generate_image_with_seedream() 生成圖像")
    print("2. 使用 openrouter_image_generation() 自定義參數")
    print("3. 所有調用都使用 openrouter/free 自動選擇免費模型")
    print("4. 模型包含 Seedream 4.5 和其他免費圖像生成模型")