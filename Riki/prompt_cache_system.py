#!/usr/bin/env python3
"""
智能 Prompt 緩存系統
用於減少重複任務嘅 token 消耗同提升效率
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
import os

class PromptCache:
    """智能 Prompt 緩存系統"""
    
    def __init__(self, cache_file="/data/workspace/Riki/prompt_cache.json"):
        self.cache_file = cache_file
        self.cache_data = {}
        self.max_cache_size = 100  # 最大緩存項目數
        self.default_ttl = 3600  # 默認1小時TTL
        
        # 確保緩存檔案存在
        self._load_cache()
    
    def _load_cache(self):
        """載入緩存數據"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache_data = json.load(f)
                print("✅ Prompt 緩存已載入")
            else:
                self.cache_data = {}
                print("🆕 創建新嘅 Prompt 緩存")
        except Exception as e:
            print(f"⚠️ 載入緩存失敗: {e}")
            self.cache_data = {}
    
    def _save_cache(self):
        """保存緩存數據"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, ensure_ascii=False, indent=2)
            print("✅ Prompt 緩存已保存")
        except Exception as e:
            print(f"⚠️ 保存緩存失敗: {e}")
    
    def _generate_key(self, prompt, template_name=None):
        """生成緩存鍵"""
        # 包含模板名稱同prompt嘅hash
        content = f"{template_name or 'default'}:{prompt}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def _is_expired(self, cache_entry):
        """檢查緩存是否過期"""
        if 'expires_at' not in cache_entry:
            return True
        
        return datetime.now() > datetime.fromisoformat(cache_entry['expires_at'])
    
    def _cleanup_expired(self):
        """清理過期緩存"""
        expired_keys = []
        for key, entry in self.cache_data.items():
            if self._is_expired(entry):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache_data[key]
            print(f"🗑️ 清理過期緩存: {key}")
        
        if expired_keys:
            self._save_cache()
    
    def _enforce_size_limit(self):
        """強制執行大小限制"""
        if len(self.cache_data) > self.max_cache_size:
            # 按時間戳排序，刪除最舊嘅項目
            sorted_items = sorted(
                self.cache_data.items(),
                key=lambda x: x[1].get('created_at', '1970-01-01T00:00:00')
            )
            
            items_to_remove = len(self.cache_data) - self.max_cache_size
            for i in range(items_to_remove):
                key, _ = sorted_items[i]
                del self.cache_data[key]
                print(f"🗑️ 清理舊緩存: {key}")
            
            self._save_cache()
    
    def get(self, prompt, template_name=None):
        """獲取緩存結果"""
        key = self._generate_key(prompt, template_name)
        
        if key in self.cache_data:
            entry = self.cache_data[key]
            if not self._is_expired(entry):
                print(f"🎯 命中緩存: {template_name or 'default'}")
                return entry['result']
            else:
                print(f"⏰ 緩存已過期: {template_name or 'default'}")
                del self.cache_data[key]
        
        return None
    
    def set(self, prompt, result, template_name=None, ttl=None):
        """設置緩存結果"""
        key = self._generate_key(prompt, template_name)
        
        # 設置TTL
        expires_at = datetime.now() + timedelta(seconds=ttl or self.default_ttl)
        
        # 創建緩存項目
        cache_entry = {
            'result': result,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat(),
            'template': template_name,
            'prompt_preview': prompt[:100] + '...' if len(prompt) > 100 else prompt
        }
        
        self.cache_data[key] = cache_entry
        
        # 執行清理
        self._cleanup_expired()
        self._enforce_size_limit()
        
        # 保存到檔案
        self._save_cache()
        
        print(f"💾 緩存已保存: {template_name or 'default'}")
    
    def get_stats(self):
        """獲取緩存統計"""
        total_entries = len(self.cache_data)
        expired_entries = sum(1 for entry in self.cache_data.values() if self._is_expired(entry))
        
        return {
            'total_entries': total_entries,
            'expired_entries': expired_entries,
            'active_entries': total_entries - expired_entries,
            'cache_file': self.cache_file
        }
    
    def clear_all(self):
        """清空所有緩存"""
        self.cache_data = {}
        self._save_cache()
        print("🧹 所有緩存已清空")

# 全局緩存實例
prompt_cache = PromptCache()

def get_cached_result(prompt, template_name=None, ttl=3600):
    """獲取緩存結果嘅便捷函數"""
    return prompt_cache.get(prompt, template_name)

def cache_result(prompt, result, template_name=None, ttl=3600):
    """緩存結果嘅便捷函數"""
    prompt_cache.set(prompt, result, template_name, ttl)

def get_cache_stats():
    """獲取緩存統計嘅便捷函數"""
    return prompt_cache.get_stats()

# 示例使用
if __name__ == "__main__":
    # 測試緩存功能
    test_prompt = "請處理發票圖片"
    test_result = "發票處理完成"
    
    # 設置緩存
    cache_result(test_prompt, test_result, "invoice_processing", 60)
    
    # 獲取緩存
    cached_result = get_cached_result(test_prompt, "invoice_processing")
    print(f"緩存結果: {cached_result}")
    
    # 獲取統計
    stats = get_cache_stats()
    print(f"緩存統計: {stats}")