#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram TTS 整合腳本
實現 TTS 語音生成並發送到 Telegram 的功能
"""

import os
import json
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

class TelegramTTSSender:
    def __init__(self):
        self.telegram_token = "8738273870:AAEUJKVy0Np0ytnUqs6W1cJ85Tn342Arta0"
        self.telegram_api_base = "https://api.telegram.org"
        
    def generate_tts(self, text: str) -> Optional[str]:
        """
        生成 TTS 語音文件
        """
        try:
            print(f"🎤 正在生成語音: {text[:50]}...")
            
            # 記錄當前嘅 TTS 目錄
            existing_dirs = set(os.listdir("/tmp/openclaw"))
            
            # 使用 OpenClaw 嘅 TTS 功能（模擬）
            print("🎤 模擬 TTS 生成過程...")
            # 實際使用時呢個會被真嘅 TTS 調用取代
            time.sleep(3)  # 模擬生成時間
            
            # 等待文件生成
            import time
            time.sleep(2)
            
            # 查找新生成嘅語音文件
            current_dirs = set(os.listdir("/tmp/openclaw"))
            new_dirs = current_dirs - existing_dirs
            
            if new_dirs:
                latest_dir = max(new_dirs)
                audio_files = [f for f in os.listdir(f"/tmp/openclaw/{latest_dir}") 
                             if f.startswith("voice-") and f.endswith(".mp3")]
                if audio_files:
                    audio_path = f"/tmp/openclaw/{latest_dir}/{audio_files[0]}"
                    print(f"✅ 語音文件生成成功: {audio_path}")
                    return audio_path
            
            return None
            
        except subprocess.TimeoutExpired:
            print("❌ TTS 生成超時")
            return None
        except subprocess.CalledProcessError as e:
            print(f"❌ TTS 生成失敗: {e}")
            return None
        except Exception as e:
            print(f"❌ TTS 生成錯誤: {e}")
            return None
    
    def send_audio_to_telegram(self, audio_path: str, chat_id: str) -> bool:
        """
        發送音頻文件到 Telegram
        """
        try:
            print(f"📤 正在發送語音到 Telegram...")
            
            # 使用 curl 發送音頻文件
            url = f"{self.telegram_api_base}/bot{self.telegram_token}/sendAudio"
            
            curl_cmd = [
                'curl', '-X', 'POST',
                '-F', f'chat_id={chat_id}',
                '-F', f'audio=@{audio_path}',
                '-F', f'caption=Airi嘅語音消息 😊',
                url
            ]
            
            # 執行 curl 命令
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ 語音發送成功！")
                return True
            else:
                print(f"❌ 發送失敗: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 發送超時")
            return False
        except Exception as e:
            print(f"❌ 發送錯誤: {e}")
            return False
    
    def cleanup_tts_files(self):
        """
        清理 TTS 臨時文件
        """
        try:
            tts_dirs = [d for d in os.listdir("/tmp/openclaw") if d.startswith("tts-")]
            
            # 只保留最新嘅兩個目錄
            tts_dirs.sort(reverse=True)
            dirs_to_remove = tts_dirs[2:] if len(tts_dirs) > 2 else []
            
            for dir_name in dirs_to_remove:
                dir_path = f"/tmp/openclaw/{dir_name}"
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
                    print(f"🧹 已清理: {dir_path}")
                    
        except Exception as e:
            print(f"清理文件時出错: {e}")
    
    def send_tts_message(self, text: str, chat_id: str) -> bool:
        """
        發送 TTS 語音消息到 Telegram
        """
        print(f"\n🚀 開始發送語音消息...")
        print(f"📝 內容: {text}")
        
        # 生成 TTS
        audio_path = self.generate_tts(text)
        if not audio_path:
            print("❌ TTS 生成失敗，無法發送語音")
            return False
        
        # 發送到 Telegram
        success = self.send_audio_to_telegram(audio_path, chat_id)
        
        # 清理臨時文件
        self.cleanup_tts_files()
        
        return success
    
    def test_system(self) -> bool:
        """
        測試系統功能
        """
        print("🔧 系統功能測試...")
        
        # 測試 Telegram 連接
        try:
            url = f"{self.telegram_api_base}/bot{self.telegram_token}/getMe"
            curl_cmd = ['curl', '-s', url]
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                try:
                    response = json.loads(result.stdout)
                    if response.get('ok', False):
                        bot_info = response['result']
                        print(f"✅ Telegram 連接成功！")
                        print(f"   Bot: {bot_info['first_name']} (@{bot_info['username']})")
                        return True
                except json.JSONDecodeError:
                    print("❌ 回應解析失敗")
                    return False
            else:
                print(f"❌ Telegram 連接失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 連接錯誤: {e}")
            return False

def main():
    """
    主函數：測試 TTS + Telegram 整合功能
    """
    print("🎤 Airi 語音消息發送器")
    print("=" * 40)
    
    tts_sender = TelegramTTSSender()
    
    # 測試系統
    if not tts_sender.test_system():
        print("\n❌ 系統測試失敗，無法繼續")
        return
    
    print("\n🎯 開始測試語音發送...")
    
    # 測試中文消息
    chinese_text = "你好 Ricky！這是一個中文語音測試，TTS 系統整合成功！很高興能夠用聲音和你對話。😄"
    
    chat_id = "8571127921"  # 你的 Telegram ID
    
    # 發送語音消息
    success = tts_sender.send_tts_message(chinese_text, chat_id)
    
    if success:
        print("\n🎉 測試完成！語音消息已成功發送到 Telegram")
    else:
        print("\n❌ 測試失敗，請檢查配置")

if __name__ == "__main__":
    main()