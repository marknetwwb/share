#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Airi TTS 系統整合
整合 OpenClaw TTS 功能，讓 Airi 可以對你說話
"""

import time
import random
from airi_voice_module import AiriVoiceModule
from typing import Dict, List, Optional

class AiriTTS:
    """Airi 語音系統"""
    
    def __init__(self):
        self.voice_module = AiriVoiceModule()
        self.is_enabled = True
        
    def speak_to_user(self, text: str, emotion: str = 'friendly', use_tts: bool = True) -> None:
        """
        對用戶說話
        text: 要說的話
        emotion: 情感類型
        use_tts: 是否使用實際 TTS
        """
        if not self.is_enabled:
            print(f"[靜音模式] {text}")
            return
        
        # 生成語音消息
        voice_message = self.voice_module.speak(text, emotion)
        
        if use_tts:
            try:
                # 調用 OpenClaw TTS 功能
                import tts
                tts.tts(text, channel='telegram')
                print(f"[TTS 已發送] {voice_message}")
            except Exception as e:
                print(f"[TTS 錯誤] {e}")
                print(f"[文字顯示] {voice_message}")
        else:
            print(f"[文字顯示] {voice_message}")
    
    def greet_user(self, use_tts: bool = True) -> None:
        """向用戶問候"""
        greeting = self.voice_module.greet()
        self.speak_to_user(greeting, 'friendly', use_tts)
    
    def farewell_user(self, use_tts: bool = True) -> None:
        """向用戶道別"""
        farewell = self.voice_module.farewell()
        self.speak_to_user(farewell, 'friendly', use_tts)
    
    def encourage_user(self, use_tts: bool = True) -> None:
        """鼓勵用戶"""
        encouragement = self.voice_module.encourage()
        self.speak_to_user(encouragement, 'happy', use_tts)
    
    def announce_novel_progress(self, chapter: str, progress: str, use_tts: bool = True) -> None:
        """宣布小說進度"""
        progress_msg = self.voice_module.speak_novel_update(chapter, progress)
        self.speak_to_user(progress_msg, 'excited', use_tts)
    
    def remind_task(self, task: str, use_tts: bool = True) -> None:
        """提醒任務"""
        reminder = self.voice_module.speak_task_reminder(task)
        self.speak_to_user(reminder, 'serious', use_tts)
    
    def conclude_topic(self, topic: str, use_tts: bool = True) -> None:
        """總結話題"""
        conclusion = self.voice_module.speak_conclusion(topic)
        self.speak_to_user(conclusion, 'calm', use_tts)
    
    def respond_to_user(self, user_message: str, context: str = '', use_tts: bool = True) -> None:
        """
        回應用戶消息
        user_message: 用戶消息
        context: 回應上下文
        use_tts: 是否使用 TTS
        """
        # 根據上下文選擇適當的回應
        if '你好' in user_message or 'hi' in user_message.lower():
            self.greet_user(use_tts)
        elif '再見' in user_message or 'bye' in user_message.lower():
            self.farewell_user(use_tts)
        elif '謝謝' in user_message or 'thanks' in user_message.lower():
            self.encourage_user(use_tts)
        elif '小說' in user_message or 'chapter' in user_message.lower():
            self.announce_novel_progress('相關章節', '正在更新中...', use_tts)
        elif '任務' in user_message or 'task' in user_message.lower():
            self.remind_task('查看 HEARTBEAT.md', use_tts)
        else:
            # 一般回應
            responses = [
                "我明白你的意思！",
                "好的，我會處理！",
                "讓我想想...",
                "這個想法不錯！"
            ]
            response = random.choice(responses)
            self.speak_to_user(response, 'friendly', use_tts)
    
    def toggle_tts(self, enabled: bool) -> None:
        """開關 TTS 功能"""
        self.is_enabled = enabled
        status = "開啟" if enabled else "關閉"
        self.speak_to_user(f"TTS功能已{status}", 'friendly', False)

# 測試 Airi TTS 系統
if __name__ == "__main__":
    airi_tts = AiriTTS()
    
    print("🎤 Airi TTS 系統測試")
    print("=" * 40)
    
    # 測試各種功能
    airi_tts.greet_user(use_tts=False)  # 關閉 TTS，只顯示文字
    
    time.sleep(1)
    
    airi_tts.announce_novel_progress("第四章", "已完成50%", use_tts=False)
    
    time.sleep(1)
    
    airi_tts.respond_to_user("你好，我想知道小說進度", use_tts=False)
    
    time.sleep(1)
    
    airi_tts.conclude_topic("語音模塊", use_tts=False)
    
    print("=" * 40)
    print("測試完成！語音模塊已準備好使用。")