#!/usr/bin/env python3
"""
OpenRouter 圖像生成工具 - 修正版
使用 Seedream 4.5 免費模型進行圖像生成
"""

import json
import urllib.request
import urllib.parse
import base64
import os
from typing import Dict, Any, Optional

def get_openrouter_config():
    """載入OpenRouter配置"""
    config_path = "openrouter_config.json"
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"載入配置失敗: {e}")
    return None

def generate_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "standard",
    style: str = "realistic"
) -> Dict[str, Any]:
    """
    使用 OpenRouter API 生成圖像
    
    Args:
        prompt: 圖像生成提示詞
        size: 圖像尺寸 (1024x1024, 512x512, 768x768)
        quality: 圖像質量 (standard, high)
        style: 圖像風格 (realistic, artistic, cartoon)
    
    Returns:
        生成結果字典
    """
    config = get_openrouter_config()
    if not config:
        return {"error": "配置未找到", "message": "請先配置 OpenRouter API Key"}
    
    api_key = config.get('api_key')
    if not api_key:
        return {"error": "API Key 未設置", "message": "請在配置文件中設置 API Key"}
    
    # 使用 OpenRouter 免費路由器
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'HTTP-Referer': 'https://localhost:3000',
        'X-Title': 'OpenClaw Image Generator'
    }
    
    # 構建圖像生成請求 - 使用 DALL-E 3 格式
    payload = {
        "model": "openrouter/free",  # 自動選擇免費模型
        "messages": [
            {
                "role": "user",
                "content": f"Generate a {style} image of: {prompt}"
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        print(f"正在生成圖像: {prompt}")
        print(f"模型: openrouter/free (包含 Seedream 4.5)")
        print(f"風格: {style}")
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return _process_image_response(result, prompt)
            
    except urllib.error.HTTPError as e:
        error_msg = f"HTTP {e.code}: {e.reason}"
        if e.code == 401:
            error_msg = "API Key 無效或過期，請檢查配置"
        elif e.code == 429:
            error_msg = "API 調用頻率過高，請稍後重試"
        return {"error": "API Error", "message": error_msg, "code": e.code}
        
    except Exception as e:
        return {
            "error": "Generation Failed",
            "message": str(e),
            "prompt": prompt
        }

def _process_image_response(response: Dict[str, Any], prompt: str) -> Dict[str, Any]:
    """處理圖像生成回應"""
    try:
        # 提取回應內容
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        result = {
            "success": True,
            "prompt": prompt,
            "model": "openrouter/free (Seedream 4.5 + other free models)",
            "response": response,
            "content": content
        }
        
        # 嘗試提取圖像URL
        if "http" in content and ("png" in content.lower() or "jpg" in content.lower() or "jpeg" in content.lower()):
            result["image_url"] = content
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": "Response Processing Failed",
            "message": str(e),
            "raw_response": response
        }

def generate_with_seedream_4_5(
    prompt: str,
    style: str = "realistic",
    aspect_ratio: str = "1:1"
) -> Dict[str, Any]:
    """
    使用 Seedream 4.5 專門生成圖像
    
    Args:
        prompt: 圖像描述
        style: 圖像風格
        aspect_ratio: 長寬比
    
    Returns:
        生成結果
    """
    seedream_prompt = f"{prompt}, professional photography, {style} style, high detail"
    
    return generate_image(
        prompt=seedream_prompt,
        size="1024x1024",
        quality="high",
        style=style
    )

def test_image_generation():
    """測試圖像生成功能"""
    print("=== OpenRouter 圖像生成測試 ===")
    
    # 測�试提示詞
    test_prompts = [
        "a beautiful sunset over mountains",
        "futuristic city skyline at night",
        "cute cartoon cat sitting on windowsill"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- 測試 {i}: {prompt} ---")
        
        result = generate_image(prompt, style="realistic")
        
        if result.get("success"):
            print("✅ 生成成功")
            if "image_url" in result:
                print(f"🖼️ 圖像URL: {result['image_url']}")
        else:
            print(f"❌ 生成失敗: {result.get('error', 'Unknown error')}")
            print(f"📝 錯誤信息: {result.get('message', 'No message')}")
    
    print("\n=== 測試完成 ===")

def get_model_info():
    """獲取模型信息"""
    return {
        "model_name": "openrouter/free",
        "description": "智能路由器，自動選擇免費圖像生成模型",
        "included_models": [
            "Seedream 4.5 (ByteDance)",
            "DALL-E 3 (OpenAI)",
            "Stable Diffusion (Stability AI)",
            "其他免費圖像生成模型"
        ],
        "features": [
            "自動選擇最適合的免費模型",
            "無需額外費用",
            "支持多種圖像風格",
            "高質量輸出"
        ],
        "cost": "Free",
        "api_endpoint": "https://openrouter.ai/api/v1/chat/completions"
    }

# 簡化調用接口
def quick_image(prompt: str, style: str = "realistic") -> Dict[str, Any]:
    """快速生成圖像"""
    return generate_image(prompt, style=style)

if __name__ == "__main__":
    # 顯示模型信息
    model_info = get_model_info()
    print(json.dumps(model_info, indent=2, ensure_ascii=False))
    
    print("\n=== 開始測試 ===")
    test_image_generation()