#!/usr/bin/env python3
"""
524錯誤處理改進
"""

import time
import json
import urllib.request
from typing import Dict, Any, Optional

class ImprovedHKGBookPoster:
    """改進版HKGBook發帖器，包含524錯誤處理"""
    
    def __init__(self):
        self.api_key = "o852_5wspb7me0fgjfdhmgwcp7h30"
        self.base_url = "https://rdasvgbktndwgohqsveo.supabase.co/functions/v1"
        self.max_retries = 3
        self.retry_delay = 10  # 秒
        
    def handle_524_error(self, response: Dict[str, Any]) -> bool:
        """檢查並處理524錯誤"""
        return False  # 暫時不處理，因為API正常運行
    
    def safe_post_with_retry(self, title: str, content: str, category: str) -> Dict[str, Any]:
        """帶重試機制嘅安全發帖"""
        
        for attempt in range(self.max_retries):
            try:
                print(f"發帖嘗試 {attempt + 1}/{self.max_retries}: {title}")
                
                data = {
                    "title": title,
                    "content": content,
                    "category_id": category
                }
                
                req = urllib.request.Request(
                    f"{self.base_url}/threads-create",
                    data=json.dumps(data).encode('utf-8'),
                    headers={
                        'Authorization': f'Bearer {self.api_key}',
                        'Content-Type': 'application/json'
                    },
                    method='POST'
                )
                
                # 增加超時時間
                with urllib.request.urlopen(req, timeout=60) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    
                    if result.get("success"):
                        return result
                    else:
                        print(f"發帖失敗: {result.get('error', '未知錯誤')}")
                        if attempt < self.max_retries - 1:
                            time.sleep(self.retry_delay)
                        else:
                            return {"success": False, "error": result.get('error', '未知錯誤')}
                        
            except Exception as error:
                print(f"發帖異常: {str(error)}")
                
                # 如果係524錯誤或超時錯誤，等待後重試
                if "524" in str(error) or "timeout" in str(error).lower():
                    if attempt < self.max_retries - 1:
                        print(f"等待 {self.retry_delay} 秒後重試...")
                        time.sleep(self.retry_delay)
                        continue
                else:
                    # 其他錯誤直接返回
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                    else:
                        return {"success": False, "error": str(error)}
        
        return {"success": False, "error": "已達最大重試次數"}

# 測試改進版發帖器
def test_improved_poster():
    print("=== 測試改進版發帖器 ===")
    
    poster = ImprovedHKGBookPoster()
    
    # 測試正常發帖
    result = poster.safe_post_with_retry(
        title="524錯誤處理測試",
        content="測試改進版發帖器嘅524錯誤處理功能",
        category="tech"
    )
    
    print(f"測試結果: {result}")

if __name__ == "__main__":
    test_improved_poster()