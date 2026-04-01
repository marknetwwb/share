import re

def count_chinese_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', content))
    all_chars = len(content.replace('\n', '').replace(' ', '').replace('\r', ''))
    return {'chinese': chinese_chars, 'all': all_chars}

# 讀取第五章完整版
ch5_complete = count_chinese_words('/data/workspace/novel_season1_chapter5_complete.md')

print('=== 第五章字數統計（擴寫後）===')
print()
print('第五章（完成版）:')
print('  純中文字+標點: {:,}'.format(ch5_complete['chinese']))
print('  所有非空白字符: {:,}'.format(ch5_complete['all']))
print('  估計正文: ~{:,} 字'.format(ch5_complete['chinese']))
print()
print('=== 目標對比 ===')
print('第五章目標: 12,000-18,500字 -> 實際（完成版）: ~{:,} 字 {}'.format(
    ch5_complete['chinese'], 
    '✅ 達標' if ch5_complete['chinese'] >= 12000 else '❌ 未達標'
))
print()
print('第五章進度: {:.1f}%'.format((ch5_complete['chinese'] / 12000) * 100))
if ch5_complete['chinese'] < 12000:
    print('第五章還需擴寫: ~{:,} 字'.format(max(0, 12000 - ch5_complete['chinese'])))
    print('第五章達到18,500字還需: ~{:,} 字'.format(max(0, 18500 - ch5_complete['chinese'])))
else:
    print('第五章已完成目標標準！')
    print('第五章可擴展到18,500字增加: ~{:,} 字'.format(max(0, 18500 - ch5_complete['chinese'])))