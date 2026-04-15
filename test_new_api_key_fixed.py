#!/usr/bin/env python3
"""
測試新嘅OpenRouter API Key
"""

import json
import urllib.request

# 新嘅API Key
new_api_key = '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'

print('=== 測試新API Key ===')
print(f'API Key: {new_api_key[:30]}...')

url = 'https://openrouter.ai/api/v1/chat/completions'
messages = [{'role': 'user', 'content': '你好'}]

# 測試基本請求
data = {
    'model': 'glm-4-flash:free',
    'messages': messages,
    'timeout': 15
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers={
        'Authorization': f'Bearer {new_api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://localhost:3000',
        'X-Title': 'New API Key Test'
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=15) as response:
        if response.status == 200:
            result = json.loads(response.read().decode('utf-8'))
            print('✅ 新API Key測試成功！')
            model_used = result.get('model', 'N/A')
            print(f'模型: {model_used}')
            content = result.get('choices', [{}])[0].get('message', {}).get('content', 'N/A')
            print(f'回應: {content[:100]}...')
        else:
            error_text = response.read().decode('utf-8')
            print(f'❌ 新API Key測試失敗: HTTP {response.status}')
            print(f'錯誤: {error_text}')
except Exception as e:
    print(f'❌ 新API Key連接失敗: {e}')
