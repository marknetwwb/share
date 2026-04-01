#!/usr/bin/env python3
"""
OpenClaw系統重啟監控器
每5天檢查一次系統狀態，必要時重啟
"""

import subprocess
import time
import os
from datetime import datetime, timedelta

def check_system_status():
    """檢查系統狀態"""
    try:
        # 檢查僵屍進程
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        zombie_count = len([line for line in result.stdout.split('\n') if 'defunct' in line])
        
        # 檢查內存使用
        result = subprocess.run(['free'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if 'Mem:' in line:
                parts = line.split()
                total_memory = int(parts[1])
                used_memory = int(parts[2])
                memory_usage = (used_memory / total_memory) * 100
                break
        
        # 檢查系統運行時間
        result = subprocess.run(['uptime'], capture_output=True, text=True)
        uptime = result.stdout.strip()
        
        return {
            'zombie_count': zombie_count,
            'memory_usage': memory_usage,
            'uptime': uptime,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {'error': str(e)}

def should_restart(status):
    """判斷是否需要重啟"""
    if 'error' in status:
        return False
    
    # 僵屍進程超過10個或內存使用超過80%
    if status['zombie_count'] > 10 or status['memory_usage'] > 80:
        return True
    
    return False

def log_status(status):
    """記錄狀態到日誌"""
    log_file = "/data/workspace/openclaw_restart.log"
    timestamp = status.get('timestamp', datetime.now().isoformat())
    
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] 系統狀態檢查\n")
        f.write(f"僵屍進程: {status.get('zombie_count', 'N/A')}\n")
        f.write(f"內存使用: {status.get('memory_usage', 'N/A'):.1f}%\n")
        f.write(f"系統時間: {status.get('uptime', 'N/A')}\n")
        
        if should_restart(status):
            f.write("⚠️ 建議重啟系統\n")
        else:
            f.write("✅ 系統狀態正常\n")
        f.write("-" * 50 + "\n")

def main():
    """主循環"""
    last_restart_file = "/data/workspace/last_restart.txt"
    
    # 讀取上次重啟時間
    if os.path.exists(last_restart_file):
        with open(last_restart_file, 'r') as f:
            last_restart = datetime.fromisoformat(f.read().strip())
    else:
        last_restart = datetime.now() - timedelta(days=6)  # 如果沒有記錄，6天前算
    
    # 檢查是否已經5天
    if datetime.now() - last_restart >= timedelta(days=5):
        status = check_system_status()
        log_status(status)
        
        if should_restart(status):
            print(f"需要重啟系統 - 僵屍: {status['zombie_count']}, 內存: {status['memory_usage']:.1f}%")
            # 這裡可以添加重啟邏輯
            # 注意：系統重啟需要root權限
        else:
            print(f"系統狀態良好，更新重啟時間")
            with open(last_restart_file, 'w') as f:
                f.write(datetime.now().isoformat())
    else:
        days_until_restart = 5 - (datetime.now() - last_restart).days
        print(f"距下次重啟還有 {days_until_restart} 天")

if __name__ == "__main__":
    main()
