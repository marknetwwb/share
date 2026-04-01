#!/usr/bin/env python3
"""
OpenRouter 圖像生成配置工具
處理API認證和配置管理
"""

import json
import os
from typing import Dict, Any, Optional

class OpenRouterConfig:
    """OpenRouter配置管理器"""
    
    def __init__(self):
        self.config_file = "openrouter_config.json"
        self.api_key = None
        self.load_config()
    
    def load_config(self):
        """載入配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.api_key = config.get('api_key')
                    return True
            return False
        except Exception as e:
            print(f"載入配置文件失敗: {e}")
            return False
    
    def save_config(self, api_key: str):
        """保存配置"""
        try:
            config = {
                'api_key': api_key,
                'created_at': '2026-03-19',
                'model': 'openrouter/free',
                'image_model': 'seedream-4.5'
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.api_key = api_key
            return True
        except Exception as e:
            print(f"保存配置文件失敗: {e}")
            return False
    
    def get_api_key(self) -> Optional[str]:
        """獲取API Key"""
        return self.api_key
    
    def setup_api_key(self):
        """設置API Key"""
        print("=== OpenRouter API 設置 ===")
        print("請提供你的 OpenRouter API Key")
        print("獲取方式:")
        print("1. 訪問 https://openrouter.ai/keys")
        print("2. 登錄或創建帳戶")
        print("3. 獲取 API Key")
        print("4. 在下方輸入你的 API Key")
        
        while True:
            api_key = input("請輸入 OpenRouter API Key: ").strip()
            if api_key:
                if len(api_key) >= 20:  # 基本驗證
                    if self.save_config(api_key):
                        print("✅ API Key 已保存成功！")
                        return True
                    else:
                        print("❌ 保存失敗，請重試")
                else:
                    print("❌ API Key 格式不正確，請重新輸入")
            else:
                print("❌ API Key 不能為空")

def check_openrouter_status():
    """檢查OpenRouter服務狀態"""
    print("=== OpenRouter 服務狀態檢查 ===")
    
    config = OpenRouterConfig()
    api_key = config.get_api_key()
    
    if not api_key:
        print("❌ 未找到 API Key")
        print("請先運行 setup_api_key() 進行設置")
        return False
    
    print(f"✅ API Key 已設置: {api_key[:10]}...")
    print("✅ 配置文件已創建")
    print("✅ 模型配置: openrouter/free (包含 Seedream 4.5)")
    return True

def setup_environment():
    """設置環境變量"""
    config = OpenRouterConfig()
    api_key = config.get_api_key()
    
    if api_key:
        os.environ['OPENROUTER_API_KEY'] = api_key
        print("✅ 環境變量已設置")
        return True
    else:
        print("❌ 請先設置 API Key")
        return False

# 主要配置函數
def configure_openrouter():
    """配置OpenRouter"""
    config = OpenRouterConfig()
    
    # 檢查是否已有配置
    if config.get_api_key():
        print("⚠️  已有現有配置，是否要覆蓋？")
        choice = input("覆蓋現有配置？(y/N): ").strip().lower()
        if choice != 'y':
            print("保留現有配置")
            return True
    
    # 設置新的API Key
    return config.setup_api_key()

# 測試函數
if __name__ == "__main__":
    # 載入配置
    config = OpenRouterConfig()
    
    print("=== OpenRouter 配置工具 ===")
    print("1. 設置 API Key")
    print("2. 檢查配置狀態")
    print("3. 設置環境變量")
    print("4. 退出")
    
    while True:
        choice = input("請選擇操作 (1-4): ").strip()
        
        if choice == '1':
            configure_openrouter()
        elif choice == '2':
            check_openrouter_status()
        elif choice == '3':
            setup_environment()
        elif choice == '4':
            print("退出配置工具")
            break
        else:
            print("無效選擇，請重新輸入")