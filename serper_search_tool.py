#!/usr/bin/env python3
"""
Serper.dev Search Tool for OpenClaw
使用 Serper.dev API 進行網路搜索
"""

import json
import requests
import os
from typing import Dict, Any, List, Optional

class SerperSearchTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev/search"
    
    def search(self, query: str, count: int = 5, country: str = "HK", 
               search_lang: str = "zh", ui_lang: str = "zh") -> Dict[str, Any]:
        """
        使用 Serper.dev 進行搜索
        
        Args:
            query: 搜索關鍵字
            count: 返回結果數量 (1-10)
            country: 國家代碼
            search_lang: 搜索語言
            ui_lang: 介面語言
        
        Returns:
            搜索結果字典
        """
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        
        payload = {
            "q": query,
            "num": min(count, 10),
            "gl": country,
            "hl": search_lang
        }
        
        try:
            response = requests.post(
                self.base_url, 
                json=payload, 
                headers=headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._format_search_result(result, query)
            else:
                return {
                    "error": f"API Error: {response.status_code}",
                    "message": response.text
                }
                
        except Exception as e:
            return {
                "error": "Request Failed",
                "message": str(e)
            }
    
    def _format_search_result(self, raw_result: Dict[str, Any], query: str) -> Dict[str, Any]:
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

def serper_search(query: str, count: int = 5, country: str = "HK", 
                 search_lang: str = "zh", ui_lang: str = "zh") -> Dict[str, Any]:
    """
    便捷搜索函數
    
    Args:
        query: 搜索關鍵字
        count: 返回結果數量
        country: 國家代碼
        search_lang: 搜索語言
        ui_lang: 介面語言
    
    Returns:
        搜索結果字典
    """
    api_key = "764229241579d0bcf83c9d749d07948979131dbd"
    tool = SerperSearchTool(api_key)
    return tool.search(query, count, country, search_lang, ui_lang)

if __name__ == "__main__":
    # 測�试搜索功能
    result = serper_search("香港天氣預報", count=3)
    print(json.dumps(result, indent=2, ensure_ascii=False))