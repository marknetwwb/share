#!/usr/bin/env python3
"""
航班資訊查詢工具
使用 Serper.dev 查詢 CX782 航班資訊
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

def search_cx782_flight():
    """查詢 CX782 航班資訊"""
    query = "CX782 Cathay Pacific flight status today arrival time Hong Kong"
    result = serper_search(query, count=5, country="HK", search_lang="zh")
    return result

def search_hkgbook_forum():
    """查詢 HKGBook 論壇最新帖子"""
    query = "HKGBook forum latest posts today 2026"
    result = serper_search(query, count=5, country="HK", search_lang="zh")
    return result

if __name__ == "__main__":
    print("=== CX782 航班資訊查詢 ===")
    flight_result = search_cx782_flight()
    print(json.dumps(flight_result, indent=2, ensure_ascii=False))
    
    print("\n=== HKGBook 論壇最新帖子查詢 ===")
    forum_result = search_hkgbook_forum()
    print(json.dumps(forum_result, indent=2, ensure_ascii=False))