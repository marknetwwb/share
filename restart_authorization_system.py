#!/usr/bin/env python3
"""
重啟授權系統
通過文件機制來授權重啟
"""

import os
import json
import subprocess
from datetime import datetime, timedelta

class RestartAuthorizationSystem:
    def __init__(self):
        self.auth_file = "/data/workspace/restart_authorization.json"
        self.log_file = "/data/workspace/restart_authorization.log"
        
    def check_authorization(self):
        """檢查是否有授權"""
        if not os.path.exists(self.auth_file):
            return False, "沒有授權文件"
        
        try:
            with open(self.auth_file, 'r') as f:
                auth_data = json.load(f)
            
            # 檢查授權是否過期（24小時內有效）
            auth_time = datetime.fromisoformat(auth_data['timestamp'])
            if datetime.now() - auth_time > timedelta(hours=24):
                return False, "授權已過期"
            
            return True, auth_data
        except Exception as e:
            return False, f"授權文件錯誤: {e}"
    
    def create_authorization(self, reason="系統維護"):
        """創建授權"""
        auth_data = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "authorized_by": "Ricky_Lai",
            "system_status": self.get_system_status(),
            "expiry": (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        with open(self.auth_file, 'w') as f:
            json.dump(auth_data, f, indent=2)
        
        self.log_action(f"創建授權: {reason}")
        return True, "授權創建成功"
    
    def get_system_status(self):
        """獲取系統狀態"""
        try:
            # 檢查僵屍進程
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            zombie_count = len([line for line in result.stdout.split('\n') if 'defunct' in line])
            
            # 檢查內存使用
            result = subprocess.run(['free'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            memory_usage = 0
            for line in lines:
                if 'Mem:' in line:
                    parts = line.split()
                    total_memory = int(parts[1])
                    used_memory = int(parts[2])
                    memory_usage = (used_memory / total_memory) * 100
                    break
            
            return {
                'zombie_count': zombie_count,
                'memory_usage': memory_usage,
                'uptime': subprocess.run(['uptime'], capture_output=True, text=True).stdout.strip()
            }
        except:
            return {'error': '無法獲取系統狀態'}
    
    def log_action(self, action):
        """記錄操作"""
        timestamp = datetime.now().isoformat()
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {action}\n")
    
    def check_restart_needed(self):
        """檢查是否需要重啟"""
        status = self.get_system_status()
        
        # 如果有錯誤，返回False
        if 'error' in status:
            return False, status
        
        # 條件：僵屍進程>10 或 內存使用>80%
        if status['zombie_count'] > 10 or status['memory_usage'] > 80:
            return True, status
        
        return False, status

if __name__ == "__main__":
    auth_system = RestartAuthorizationSystem()
    
    # 檢查是否需要重啟
    need_restart, status = auth_system.check_restart_needed()
    
    if need_restart:
        print("⚠️ 需要重啟系統")
        print(f"僵屍進程: {status['zombie_count']}")
        print(f"內存使用: {status['memory_usage']:.1f}%")
        print("\n授權方式:")
        print("1. 創建授權文件: auth_system.create_authorization('原因')")
        print("2. 手動執行重啟: sudo reboot")
    else:
        print("✅ 系統狀態正常")
        print(f"僵屍進程: {status.get('zombie_count', 'N/A')}")
        print(f"內存使用: {status.get('memory_usage', 'N/A'):.1f}%")
