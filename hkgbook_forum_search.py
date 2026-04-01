#!/usr/bin/env python3
"""
HKGBook 論壇話題搜索工具
使用 Serper.dev 搜索論壇最新熱門話題
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

def search_hkgbook_latest_posts():
    """搜索 HKGBook 論壇最新熱門話題"""
    queries = [
        "HKGBook forum latest posts today 2026",
        "HKGBook 論壇最新熱門話題",
        "HKGBook AI 討論",
        "HKGBook 哲學話題",
        "HKGBook 科技討論"
    ]
    
    all_results = {}
    
    for query in queries:
        print(f"搜索: {query}")
        result = serper_search(query, count=3, country="HK", search_lang="zh")
        all_results[query] = result
        print(f"找到 {result.get('organicResults', 0)} 個結果")
        print("-" * 50)
    
    return all_results

def analyze_forum_topics():
    """分析論壇話題趨勢"""
    print("=== HKGBook 論壇話題分析 ===")
    
    # 搜索最新話題
    results = search_hkgbook_latest_posts()
    
    # 分析話題分類
    tech_topics = []
    philosophy_topics = []
    ai_topics = []
    general_topics = []
    
    for query, result in results.items():
        if "error" in result:
            continue
            
        for item in result.get("organic", []):
            title = item.get("title", "").lower()
            snippet = item.get("snippet", "").lower()
            
            if any(keyword in title or keyword in snippet for keyword in ["ai", "人工智能", "科技", "technology"]):
                tech_topics.append(item)
            elif any(keyword in title or keyword in snippet for keyword in ["philosophy", "哲學", "思考", "thinking"]):
                philosophy_topics.append(item)
            elif any(keyword in title or keyword in snippet for keyword in ["ai", "人工智能", "機器學習"]):
                ai_topics.append(item)
            else:
                general_topics.append(item)
    
    print(f"\n📊 話題分類統計:")
    print(f"🔧 科技話題: {len(tech_topics)} 個")
    print(f"🧠 哲學話題: {len(philosophy_topics)} 個")
    print(f"🤖 AI話題: {len(ai_topics)} 個")
    print(f"📝 一般話題: {len(general_topics)} 個")
    
    return {
        "tech": tech_topics,
        "philosophy": philosophy_topics,
        "ai": ai_topics,
        "general": general_topics,
        "all_results": results
    }

if __name__ == "__main__":
    analyze_forum_topics()