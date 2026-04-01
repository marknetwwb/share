#!/usr/bin/env python3

# 自動檢查重啟需求腳本
# 每5分鐘檢查一次系統狀態

import os
import json
import subprocess
import time
from datetime import datetime, timedelta

def check_system_status():
    """檢查系統狀態"""
    try:
        # 僵屍進程
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        zombie_count = len([line for line in result.stdout.split('\n') if 'defunct' in line])
        
        # 內存使用
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
        
        # 系統運行時間
        uptime = subprocess.run(['uptime'], capture_output=True, text=True).stdout.strip()
        
        return {
            'zombie_count': zombie_count,
            'memory_usage': memory_usage,
            'uptime': uptime,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {'error': str(e)}

def check_authorization():
    """檢查授權"""
    auth_file = "/data/workspace/restart_authorization.json"
    
    if not os.path.exists(auth_file):
        return False, "沒有授權文件"
    
    try:
        with open(auth_file, 'r') as f:
            auth_data = json.load(f)
        
        # 檢查授權是否過期
        expiry_time = datetime.fromisoformat(auth_data['expiry'])
        if datetime.now() > expiry_time:
            return False, "授權已過期"
        
        return True, auth_data
    except Exception as e:
        return False, f"授權文件錯誤: {e}"

def main():
    """主函數"""
    status = check_system_status()
    
    if 'error' in status:
        print(f"❌ 系統狀態檢查失敗: {status['error']}")
        return
    
    # 檢查是否需要重啟
    need_restart = (status['zombie_count'] > 10 or status['memory_usage'] > 80)
    
    print(f"📊 系統狀態檢查 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    print(f"僵屍進程: {status['zombie_count']}")
    print(f"內存使用: {status['memory_usage']:.1f}%")
    print(f"系統時間: {status['uptime']}")
    
    # 檢查授權
    authorized, auth_info = check_authorization()
    
    if need_restart:
        print("⚠️ 系統需要重啟")
        
        if authorized:
            print("✅ 授權已確認")
            print("🚀 可以執行重啟命令: sudo reboot")
            
            # 記錄日誌
            with open("/data/workspace/auto_restart.log", 'a') as f:
                f.write(f"[{datetime.now().isoformat()}] 自動檢測到需要重啟，授權已確認\n")
                f.write(f"系統狀態: {status}\n")
                f.write(f"授權信息: {auth_info}\n")
                f.write("-" * 50 + "\n")
        else:
            print("❌ 沒有有效授權")
            print("🔧 執行授權: ./grant_restart_permission.sh [原因]")
            
            # 記錄日誌
            with open("/data/workspace/auto_restart.log", 'a') as f:
                f.write(f"[{datetime.now().isoformat()}] 檢測到需要重啟，但無授權\n")
                f.write(f"系統狀態: {status}\n")
                f.write("-" * 50 + "\n")
    else:
        print("✅ 系統狀態正常")
        
        # 檢查授權狀態
        if authorized:
            print("✅ 授權有效 (等待需要時使用)")
        else:
            print("ℹ️ 無授權 (需要時執行授權腳本)")

if __name__ == "__main__":
    main()
