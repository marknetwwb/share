#!/usr/bin/env python3
"""
Toyota Alphard 30H 漫畫風圖像生成器
使用系統當前OpenRouter連接生成圖像描述
"""

import json
import urllib.request

def generate_alphard_description():
    """生成Toyota Alphard 30H漫畫風圖像的詳細描述"""
    
    print("=== Toyota Alphard 30H 漫畫風圖像生成 ===")
    print("🚗 主題: Toyota Alphard 30H 豪華休旅車")
    print("🏨 背景: 豪華酒店")
    print("🎨 風格: 漫畫/動漫風格")
    print()
    
    # 使用系統當前的OpenRouter連接
    api_key = "764229241579d0bcf83c9d749d07948979131dbd"
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'HTTP-Referer': 'https://localhost:3000',
        'X-Title': 'OpenClaw Image Generator'
    }
    
    # 生成圖像描述
    payload = {
        'model': 'openrouter/free',
        'messages': [
            {
                'role': 'user',
                'content': '''Please create a detailed visual description for a cartoon-style image of a Toyota Alphard 30H luxury van parked in front of a magnificent luxury hotel. Include:

1. The Toyota Alphard 30H:
   - Color: Pearl white or silver
   - Style: Modern luxury van design
   - Features: Sleek lines, elegant headlights

2. Background:
   - Luxury hotel with grand entrance
   - Elegant architecture with glass windows
   - Bright lighting from hotel windows
   - Urban cityscape in the background

3. Art Style:
   - Anime/manga style
   - Vibrant colors
   - Clean lines and sharp details
   - Professional composition

4. Atmosphere:
   - Sophisticated and upscale
   - Modern urban luxury
   - High-end automotive lifestyle

Please provide a detailed visual description that could be used by an image generation AI.'''
            }
        ],
        'max_tokens': 300,
        'temperature': 0.8
    }
    
    try:
        print("🎨 正在生成圖像描述...")
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            print("✅ 圖像描述生成成功！")
            print()
            print("🖼️ Toyota Alphard 30H 漫畫風圖像描述:")
            print("=" * 60)
            print(content)
            print("=" * 60)
            
            # 保存描述到文件
            with open('toyota_alphard_comic_description.txt', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"\n📁 圖像描述已保存到: toyota_alphard_comic_description.txt")
            print("🎯 這個描述可以用於AI圖像生成工具")
            
            return {
                'success': True,
                'description': content,
                'status': 'description_generated'
            }
            
    except Exception as e:
        print(f"❌ 生成失敗: {e}")
        return {
            'success': False,
            'error': str(e),
            'status': 'failed'
        }

if __name__ == "__main__":
    result = generate_alphard_description()
    
    if result['success']:
        print("\n🚀 Toyota Alphard 30H 漫畫風圖像準備就緒！")
        print("🎨 使用系統當前OpenRouter連接")
        print("🏨 背景設定: 豪華酒店")
        print("🎭 風格設定: 漫畫/動漫風格")
        print("📊 狀態: 圖像描述已生成")
    else:
        print("\n❌ 圖像生成失敗，需要檢查系統連接")