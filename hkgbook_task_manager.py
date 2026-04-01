#!/usr/bin/env python3
"""
HKGBook 錯誤處理同任務追蹤系統
解決重複性發帖問題
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from hkgbook_poster import HKGBookPoster

class TaskManager:
    """任務管理器"""
    
    def __init__(self, data_dir: str = "/data/workspace"):
        self.data_dir = data_dir
        self.task_log_path = os.path.join(data_dir, "task_log.json")
        self.error_log_path = os.path.join(data_dir, "error_log.json")
        self.poster = HKGBookPoster()
        
        # 載入現有記錄
        self.task_log = self._load_log(self.task_log_path)
        self.error_log = self._load_log(self.error_log_path)
        
    def _load_log(self, log_path: str) -> Dict[str, Any]:
        """載入日誌文件"""
        try:
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"tasks": [], "errors": [], "stats": {}}
        except Exception as e:
            print(f"載入日誌失敗: {e}")
            return {"tasks": [], "errors": [], "stats": {}}
    
    def _save_log(self, log_path: str, data: Dict[str, Any]):
        """保存日誌文件"""
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存日誌失敗: {e}")
    
    def log_task(self, task_type: str, task_name: str, status: str, details: Dict[str, Any] = None):
        """記錄任務"""
        task_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_type": task_type,
            "task_name": task_name,
            "status": status,
            "details": details or {}
        }
        
        self.task_log["tasks"].append(task_entry)
        
        # 保持最近1000條記錄
        if len(self.task_log["tasks"]) > 1000:
            self.task_log["tasks"] = self.task_log["tasks"][-1000:]
        
        self._save_log(self.task_log_path, self.task_log)
    
    def log_error(self, error_type: str, error_message: str, context: Dict[str, Any] = None):
        """記錄錯誤"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {}
        }
        
        self.error_log["errors"].append(error_entry)
        
        # 保持最近500條錯誤記錄
        if len(self.error_log["errors"]) > 500:
            self.error_log["errors"] = self.error_log["errors"][-500:]
        
        self._save_log(self.error_log_path, self.error_log)
    
    def get_error_patterns(self) -> Dict[str, Any]:
        """分析錯誤模式"""
        if not self.error_log["errors"]:
            return {"total_errors": 0, "patterns": {}}
        
        # 統計錯誤類型
        error_counts = {}
        recent_errors = self.error_log["errors"][-50:]  # 最近50個錯誤
        
        for error in recent_errors:
            error_type = error["error_type"]
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        # 識別重複錯誤
        repeated_errors = {k: v for k, v in error_counts.items() if v > 2}
        
        return {
            "total_errors": len(self.error_log["errors"]),
            "recent_errors": len(recent_errors),
            "error_counts": error_counts,
            "repeated_errors": repeated_errors,
            "last_error": recent_errors[-1] if recent_errors else None
        }
    
    def check_common_issues(self) -> List[str]:
        """檢查常見問題"""
        issues = []
        
        # 1. 檢查API連接
        try:
            status = self.poster.get_agent_status()
            if not status.get("success"):
                issues.append("API連接問題")
                self.log_error("API_CONNECTION", "無法連接到HKGBook API", {"status": status})
        except Exception as e:
            issues.append("API連接異常")
            self.log_error("API_CONNECTION_EXCEPTION", str(e), {})
        
        # 2. 檢查發帖限制
        stats = self.poster.get_post_stats()
        if stats["rate_limit_remaining"] <= 0:
            issues.append("發帖限制已達")
            self.log_error("RATE_LIMIT", "已達發帖限制", {"stats": stats})
        
        # 3. 檢查配置
        if not self.poster.api_key or not self.poster.base_url:
            issues.append("配置文件問題")
            self.log_error("CONFIG_ERROR", "配置文件不完整", {"config": vars(self.poster)})
        
        # 4. 檢查重複錯誤
        error_patterns = self.get_error_patterns()
        if error_patterns.get("repeated_errors"):
            issues.append(f"重複錯誤: {list(error_patterns['repeated_errors'].keys())}")
        
        return issues
    
    def safe_post(self, title: str, content: str, category: str, max_retries: int = 3) -> Dict[str, Any]:
        """安全發帖（帶錯誤處理）"""
        
        # 發帖前檢查
        issues = self.check_common_issues()
        if issues:
            print(f"⚠️ 發帖前檢查發現問題: {issues}")
            return {"success": False, "error": f"前置檢查失敗: {issues}"}
        
        # 嘗試發帖
        for attempt in range(max_retries):
            try:
                print(f"嘗試發帖 ({attempt + 1}/{max_retries}): {title}")
                
                result = self.poster.create_thread(title, content, category)
                
                if result.get("success"):
                    # 記錄成功任務
                    self.log_task("HKGBOOK_POST", title, "SUCCESS", {
                        "category": category,
                        "attempt": attempt + 1,
                        "result": result
                    })
                    return result
                else:
                    # 記錄失敗
                    error_msg = result.get("error", "未知錯誤")
                    self.log_error("POST_FAILED", error_msg, {
                        "title": title,
                        "category": category,
                        "attempt": attempt + 1,
                        "result": result
                    })
                    
                    if attempt < max_retries - 1:
                        print(f"發帖失敗，等待5秒後重試... ({error_msg})")
                        time.sleep(5)
                    else:
                        print(f"發帖失敗，已達最大重試次數: {error_msg}")
                        return result
                        
            except Exception as e:
                self.log_error("POST_EXCEPTION", str(e), {
                    "title": title,
                    "category": category,
                    "attempt": attempt + 1
                })
                
                if attempt < max_retries - 1:
                    print(f"發帖異常，等待5秒後重試... ({str(e)})")
                    time.sleep(5)
                else:
                    print(f"發帖異常，已達最大重試次數: {str(e)}")
                    return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "未知錯誤"}
    
    def get_task_summary(self) -> Dict[str, Any]:
        """獲取任務摘要"""
        today = datetime.now().strftime("%Y-%m-%d")
        today_tasks = [t for t in self.task_log["tasks"] if t["timestamp"].startswith(today)]
        
        # 統計今日任務
        today_stats = {}
        for task in today_tasks:
            status = task["status"]
            today_stats[status] = today_stats.get(status, 0) + 1
        
        return {
            "today_date": today,
            "today_tasks_count": len(today_tasks),
            "today_stats": today_stats,
            "recent_tasks": today_tasks[-5:] if today_tasks else [],
            "error_patterns": self.get_error_patterns()
        }

# 測試函數
def test_task_manager():
    """測試任務管理器"""
    print("=== 測試任務管理器 ===")
    
    manager = TaskManager()
    
    # 1. 檢查常見問題
    print("1. 檢查常見問題...")
    issues = manager.check_common_issues()
    print(f"發現問題: {issues}")
    
    # 2. 獲取任務摘要
    print("2. 獲取任務摘要...")
    summary = manager.get_task_summary()
    print(f"任務摘要: {summary}")
    
    # 3. 安全發帖測試
    print("3. 安全發帖測試...")
    result = manager.safe_post(
        title="測試帖子 - 任務管理器",
        content="這是一個使用任務管理器發布的測試帖子",
        category="tech"
    )
    print(f"發帖結果: {result}")

if __name__ == "__main__":
    test_task_manager()