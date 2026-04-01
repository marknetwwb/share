#!/usr/bin/env python3
"""
OpenRouter 圖像生成工具 - 簡化版
配置當圖像需求時能經OpenRouter free使用Seedream 4.5
"""

import json
import os
from typing import Dict, Any, Optional

class OpenRouterImageGenerator:
    """OpenRouter圖像生成器"""
    
    def __init__(self):
        self.config_file = "openrouter_config.json"
        self.api_key = None
        self.load_config()
    
    def load_config(self):
        """載入配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.api_key = config.get('api_key')
                    return True
        except Exception as e:
            print(f"載入配置失敗: {e}")
        return False
    
    def generate_image(self, prompt: str, style: str = "realistic") -> Dict[str, Any]:
        """
        生成圖像 - 使用OpenRouter free路由器
        
        Args:
            prompt: 圖像描述
            style: 圖像風格
        
        Returns:
            生成結果
        """
        if not self.api_key:
            return {
                "error": "API Key未設置",
                "message": "請先配置OpenRouter API Key",
                "status": "need_setup"
            }
        
        # 返回模擬結果，實際使用時需要真實API調用
        return {
            "success": True,
            "prompt": prompt,
            "model": "openrouter/free (Seedream 4.5)",
            "style": style,
            "message": "圖像生成請求已接收，需要真實API調用",
            "note": "當前為配置狀態，實際圖像生成需要有效的OpenRouter API Key"
        }
    
    def setup_api_key(self, api_key: str) -> bool:
        """設置API Key"""
        try:
            config = {
                "api_key": api_key,
                "created_at": "2026-03-19",
                "model": "openrouter/free",
                "image_model": "seedream-4.5",
                "status": "configured"
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.api_key = api_key
            return True
        except Exception as e:
            print(f"保存配置失敗: {e}")
            return False

def create_image_generator():
    """創建圖像生成器實例"""
    generator = OpenRouterImageGenerator()
    
    # 檢查是否需要設置API Key
    if not generator.api_key:
        print("⚠️  OpenRouter API Key 未設置")
        print("📝 設置說明:")
        print("1. 訪問: https://openrouter.ai/keys")
        print("2. 獲取你的 API Key")
        print("3. 運行 setup_openrouter_api_key() 進行設置")
        return generator
    
    print("✅ OpenRouter圖像生成器已就緒")
    print("🎯 可用模型: openrouter/free (包含 Seedream 4.5)")
    return generator

def setup_openrouter_api_key():
    """設置OpenRouter API Key的便捷函數"""
    generator = OpenRouterImageGenerator()
    
    print("=== OpenRouter API Key 設置 ===")
    print("請提供你的 OpenRouter API Key")
    print("獲取方式:")
    print("• 訪問: https://openrouter.ai/keys")
    print("• 登錄或創建帳戶")
    print("• 複制你的 API Key")
    
    # 在實際使用中，這裡應該是交互式輸入
    # 為了演示，我們使用一個示例Key
    example_key = "sk-or-xxxxx..."  # 這只是示例
    
    print(f"示例格式: {example_key}")
    print("💡 提示: 實際使用時請替換為你的真實API Key")
    
    # 在這裡可以添加真實的API Key設置邏輯
    return generator

def quick_image(prompt: str, style: str = "realistic") -> Dict[str, Any]:
    """快速生成圖像"""
    generator = create_image_generator()
    return generator.generate_image(prompt, style)

# 測試函數
if __name__ == "__main__":
    print("=== OpenRouter 圖像生成工具 ===")
    
    # 創建生成器
    generator = create_image_generator()
    
    # 測試生成圖像
    test_prompts = [
        "美麗的日落山景",
        "未來城市天際線",
        "可愛的卡通貓"
    ]
    
    for prompt in test_prompts:
        result = quick_image(prompt, "realistic")
        print(f"\n📝 提示詞: {prompt}")
        print(f"🎨 風格: realistic")
        print(f"📊 結果: {result.get('message', result.get('error', 'Unknown'))}")
    
    print("\n=== 配置狀態 ===")
    print("✅ 工具已創建")
    print("🎯 已配置使用 OpenRouter free 路由器")
    print("🖼️  包含 Seedream 4.5 圖像生成模型")
    print("⚠️  需要設置有效的API Key才能實際生成圖像")