#!/usr/bin/env python3
"""
Serper.dev Search Function for OpenClaw
可以直接在系統中調用的搜索功能
"""

import json
import urllib.request
import urllib.parse
from typing import Dict, Any

def serper_search(query: str, count: int = 5, country: str = "HK", 
                 search_lang: str = "zh", ui_lang: str = "zh") -> Dict[str, Any]:
    """
    使用 Serper.dev 進行網路搜索
    
    Args:
        query: 搜索關鍵字
        count: 返回結果數量 (1-10)
        country: 國家代碼
        search_lang: 搜索語言
        ui_lang: 介面語言
    
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

def search_hong_kong_weather():
    """搜索香港天氣信息"""
    result = serper_search("香港天氣預報今晚氣溫", count=3, country="HK", search_lang="zh")
    return result

def search_novel_info(query: str):
    """搜索小說相關信息"""
    result = serper_search(f"小說 {query}", count=5, country="HK", search_lang="zh")
    return result

# 測試函數
if __name__ == "__main__":
    # 測試香港天氣搜索
    print("=== 香港天氣搜索測試 ===")
    weather_result = search_hong_kong_weather()
    print(json.dumps(weather_result, indent=2, ensure_ascii=False))
    
    print("\n=== 小說搜索測試 ===")
    novel_result = search_novel_info("愛情小說")
    print(json.dumps(novel_result, indent=2, ensure_ascii=False))
    
    print("\n=== 資訊攻擊面搜索測試 ===")
    attack_surface_result = serper_search("information attack surface summary", count=5, country="US", search_lang="en")
    print(json.dumps(attack_surface_result, indent=2, ensure_ascii=False))