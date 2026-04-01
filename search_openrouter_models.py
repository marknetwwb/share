#!/usr/bin/env python3
"""
Search for OpenRouter image generation models
"""

import json
import urllib.request
import urllib.parse
from typing import Dict, Any

def serper_search(query: str, count: int = 5, country: str = "US", 
                 search_lang: str = "en", ui_lang: str = "en") -> Dict[str, Any]:
    """
    使用 Serper.dev 進行網路搜索
    
    Args:
        query: 搜索關鍵字
        count: 返回結果數量 (1-10)
        country: 國家代碼
        search_lang: 搜索語言
        ui_lang: 介面語語
    
    Returns:
        搜索結果字典
    """
    api_key = "764229241579d0bcf83c9d749d07948979131dbd"
    url = "https://google.serper.dev/search"
    
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key
    }
    
    payload = {
        'q': query,
        'num': min(count, 10),
        'gl': country,
        'hl': search_lang
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            return _format_search_result(result, query)
            
    except Exception as e:
        return {
            "error": "Search Failed",
            "message": str(e),
            "query": query
        }

def _format_search_result(raw_result: Dict[str, Any], query: str) -> Dict[str, Any]:
    """格式化搜索結果"""
    organic = raw_result.get("organic", [])
    
    formatted_results = []
    for i, item in enumerate(organic[:10]):
        formatted_results.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", ""),
            "position": i + 1
        })
    
    return {
        "query": query,
        "organic": formatted_results,
        "organicResults": len(formatted_results),
        "searchParameters": {
            "q": query,
            "type": "search",
            "num": len(formatted_results),
            "engine": "google"
        }
    }

def search_openrouter_image_models():
    """搜索OpenRouter上支持圖像生成嘅免費模型"""
    query = "OpenRouter free image generation models DALL-E Stable Diffusion 2026"
    result = serper_search(query, count=5, country="US", search_lang="en")
    return result

if __name__ == "__main__":
    print("=== OpenRouter 圖像生成模型搜索 ===")
    result = search_openrouter_image_models()
    print(json.dumps(result, indent=2, ensure_ascii=False))