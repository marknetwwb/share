#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram TTS 發送器 - 簡化版本
直接發送已生成嘅語音文件到 Telegram
"""

import os
import json
import subprocess
import shutil
from pathlib import Path
from typing import Optional

class TelegramAudioSender:
    def __init__(self):
        self.telegram_token = "8738273870:AAEUJKVy0Np0ytnUqs6W1cJ85Tn342Arta0"
        self.telegram_api_base = "https://api.telegram.org"
        
    def find_latest_audio(self) -> Optional[str]:
        """
        查找最新生成嘅語音文件
        """
        try:
            tts_dirs = [d for d in os.listdir("/tmp/openclaw") if d.startswith("tts-")]
            if not tts_dirs:
                return None
                
            # 排序並獲取最新目錄
            tts_dirs.sort(reverse=True)
            latest_dir = tts_dirs[0]
            
            # 查找音頻文件
            audio_files = [f for f in os.listdir(f"/tmp/openclaw/{latest_dir}") 
                         if f.startswith("voice-") and f.endswith(".mp3")]
            
            if audio_files:
                return f"/tmp/openclaw/{latest_dir}/{audio_files[0]}"
            
            return None
            
        except Exception as e:
            print(f"查找音頻文件失敗: {e}")
            return None
    
    def send_audio_to_telegram(self, audio_path: str, chat_id: str) -> bool:
        """
        發送音頻文件到 Telegram
        """
        try:
            print(f"📤 正在發送語音到 Telegram...")
            print(f"📁 文件: {os.path.basename(audio_path)}")
            
            # 使用 curl 發送音頻文件
            url = f"{self.telegram_api_base}/bot{self.telegram_token}/sendAudio"
            
            curl_cmd = [
                'curl', '-X', 'POST',
                '-F', f'chat_id={chat_id}',
                '-F', f'audio=@{audio_path}',
                '-F', f'caption=Airi嘅語音消息 😄\n🎤 中文語音測試成功！',
                url
            ]
            
            print("🔧 執行發送命令...")
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ 語音發送成功！")
                print("🎉 你喺 Telegram 中收到語音消息喇！")
                return True
            else:
                print(f"❌ 發送失敗: {result.stderr}")
                print(f"返回碼: {result.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 發送超時")
            return False
        except Exception as e:
            print(f"❌ 發送錯誤: {e}")
            return False
    
    def cleanup_old_files(self):
        """
        清理舊嘅 TTS 文件
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
    
    def test_connection(self) -> bool:
        """
        測試 Telegram 連接
        """
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
    主函數：發送語音文件到 Telegram
    """
    print("🎤 Airi 語音消息發送器")
    print("=" * 40)
    
    sender = TelegramAudioSender()
    
    # 測試系統
    if not sender.test_connection():
        print("\n❌ 系統測試失敗，無法繼續")
        return
    
    # 查找最新語音文件
    audio_path = sender.find_latest_audio()
    
    if not audio_path:
        print("\n❌ 未找到語音文件")
        print("請先使用 TTS 功能生成語音文件")
        return
    
    print(f"\n🎵 找到語音文件: {audio_path}")
    
    # 顯示文件信息
    file_size = os.path.getsize(audio_path)
    print(f"📊 文件大小: {file_size / 1024 / 1024:.2f} MB")
    
    # 檢查文件是否存在
    if not os.path.exists(audio_path):
        print(f"❌ 文件不存在: {audio_path}")
        return
    
    chat_id = "8571127921"  # 你的 Telegram ID
    
    # 發送語音消息
    success = sender.send_audio_to_telegram(audio_path, chat_id)
    
    # 清理舊文件
    sender.cleanup_old_files()
    
    if success:
        print(f"\n🎉 測試完成！語音消息已成功發送到 Telegram")
        print("📱 請檢查你的 Telegram 收件箱！")
    else:
        print(f"\n❌ 發送失敗，請檢查配置")

if __name__ == "__main__":
    main()