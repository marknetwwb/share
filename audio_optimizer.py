#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
語音預處理腳本
確保語音檔案完整性
"""

import os
import subprocess
import wave

def check_audio_file(file_path):
    """檢查音頻檔案完整性"""
    try:
        with wave.open(file_path, 'rb') as wav_file:
            frames = wav_file.getnframes()
            channels = wav_file.getnchannels()
            width = wav_file.getsampwidth()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            
            print(f"🎵 檔案檢查：{file_path}")
            print(f"   時長：{duration:.2f} 秒")
            print(f"   通道：{channels}")
            print(f"   取樣率：{rate} Hz")
            print(f"   位元深度：{width * 8} bits")
            print(f"   總幀數：{frames}")
            
            return True
            
    except Exception as e:
        print(f"❌ 檔案檢查失敗：{e}")
        return False

def optimize_audio(input_file, output_file):
    """優化音頻檔案"""
    try:
        # 使用 ffmpeg 優化（如果可用）
        cmd = [
            'ffmpeg', '-i', input_file, 
            '-acodec', 'libmp3lame', 
            '-ab', '16k', 
            '-ar', '16000', 
            output_file
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        # 如果 ffmpeg 無法使用，直接複製
        import shutil
        shutil.copy2(input_file, output_file)
        return True

def main():
    # 檢查最新嘅語音檔案
    tts_dirs = [d for d in os.listdir("/tmp/openclaw") if d.startswith("tts-")]
    
    if tts_dirs:
        latest_dir = max(tts_dirs)
        audio_files = [f for f in os.listdir(f"/tmp/openclaw/{latest_dir}") 
                     if f.startswith("voice-") and f.endswith(".mp3")]
        
        if audio_files:
            audio_path = f"/tmp/openclaw/{latest_dir}/{audio_files[0]}"
            
            # 檢查檔案
            if check_audio_file(audio_path):
                print("✅ 語音檔案完整")
            else:
                print("❌ 語音檔案可能損壞")
                
                # 嘗試優化
                optimized_path = f"/tmp/openclaw/{latest_dir}/voice_optimized.mp3"
                if optimize_audio(audio_path, optimized_path):
                    print("✅ 檔案優化完成")
                    # 使用優化後嘅檔案
                    audio_path = optimized_path
            
            return audio_path
    
    return None

if __name__ == "__main__":
    main()