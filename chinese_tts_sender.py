#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版 Telegram TTS 發送器
"""

import os
import subprocess
import time

def send_chinese_voice_to_telegram():
    """
    發送中文語音消息到 Telegram
    """
    print("🎤 開始發送中文語音消息...")
    
    # 測試文本
    chinese_text = "你好 Ricky！我是 Airi，TTS 系統整合成功！很高興能夠用聲音和你對話。😄"
    
    print(f"📝 語音內容：{chinese_text}")
    
    # 步驟 1：生成 TTS 語音
    print("🔄 正在生成中文語音...")
    
    try:
        # 使用系統 TTS 功能
        result = subprocess.run(['tts', chinese_text], 
                              capture_output=True, 
                              text=True, 
                              timeout=30)
        
        if result.returncode == 0:
            print("✅ TTS 生成指令執行成功")
            
            # 等待文件生成
            time.sleep(3)
            
            # 查找最新嘅語音文件
            tts_dirs = [d for d in os.listdir("/tmp/openclaw") if d.startswith("tts-")]
            
            if tts_dirs:
                latest_dir = max(tts_dirs)
                audio_files = [f for f in os.listdir(f"/tmp/openclaw/{latest_dir}") 
                             if f.startswith("voice-") and f.endswith(".mp3")]
                
                if audio_files:
                    audio_path = f"/tmp/openclaw/{latest_dir}/{audio_files[0]}"
                    print(f"✅ 語音文件生成成功：{audio_path}")
                    
                    # 步驟 2：發送到 Telegram
                    print("📤 正在發送到 Telegram...")
                    
                    # 使用 curl 發送音頻文件
                    telegram_token = "8738273870:AAEUJKVy0Np0ytnUqs6W1cJ85Tn342Arta0"
                    chat_id = "8571127921"
                    
                    url = f"https://api.telegram.org/bot{telegram_token}/sendAudio"
                    
                    curl_cmd = [
                        'curl', '-X', 'POST',
                        '-F', f'chat_id={chat_id}',
                        '-F', f'audio=@{audio_path}',
                        '-F', f'caption=Airi嘅中文語音消息 😄',
                        url
                    ]
                    
                    # 執行 curl 命令
                    result = subprocess.run(curl_cmd, 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=60)
                    
                    if result.returncode == 0:
                        print("✅ 中文語音消息發送成功！")
                        return True
                    else:
                        print(f"❌ 發送失敗：{result.stderr}")
                        return False
                else:
                    print("❌ 喺 TTS 目錄中冇找到語音文件")
                    return False
            else:
                print("❌ 無法找到 TTS 目錄")
                return False
        else:
            print(f"❌ TTS 生成失敗：{result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ TTS 生成超時")
        return False
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
        return False

def test_chinese_tts():
    """
    測試中文 TTS 功能
    """
    print("🧪 測試中文 TTS 功能...")
    
    # 生成簡單嘅中文測試
    test_text = "你好，這是一個中文語音測試。"
    
    try:
        print(f"🎤 正在測試：{test_text}")
        
        # 使用 TTS
        result = subprocess.run(['tts', test_text], 
                              capture_output=True, 
                              text=True, 
                              timeout=30)
        
        if result.returncode == 0:
            print("✅ 中文 TTS 測試成功！")
            
            # 等待文件生成
            time.sleep(3)
            
            # 檢查文件是否存在
            tts_dirs = [d for d in os.listdir("/tmp/openclaw") if d.startswith("tts-")]
            
            if tts_dirs:
                latest_dir = max(tts_dirs)
                audio_files = [f for f in os.listdir(f"/tmp/openclaw/{latest_dir}") 
                             if f.startswith("voice-") and f.endswith(".mp3")]
                
                if audio_files:
                    audio_path = f"/tmp/openclaw/{latest_dir}/{audio_files[0]}"
                    file_size = os.path.getsize(audio_path)
                    print(f"✅ 語音文件生成成功：{audio_path}")
                    print(f"📊 文件大小：{file_size} 字節")
                    return True
                else:
                    print("❌ 無法找到語音文件")
                    return False
            else:
                print("❌ 無法找到 TTS 目錄")
                return False
        else:
            print(f"❌ TTS 測試失敗：{result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗：{e}")
        return False

def main():
    """
    主函數
    """
    print("🎤 Airi 中文語音發送器")
    print("=" * 40)
    
    # 測試 TTS 功能
    if test_chinese_tts():
        print("\n🎯 TTS 測試通過，開始發送語音消息...")
        
        # 發送完整嘅中文語音消息
        success = send_chinese_voice_to_telegram()
        
        if success:
            print("\n🎉 中文語音消息發送完成！")
        else:
            print("\n❌ 語音消息發送失敗")
    else:
        print("\n❌ TTS 測試失敗，無法繼續")

if __name__ == "__main__":
    main()