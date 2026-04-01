import re

def count_chinese_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', content))
    all_chars = len(content.replace('\n', '').replace(' ', '').replace('\r', ''))
    return {'chinese': chinese_chars, 'all': all_chars}

ch3 = count_chinese_words('/data/workspace/novel_season1_chapter3.md')
ch4 = count_chinese_words('/data/workspace/novel_season1_chapter4.md')

print('=== 章節字數統計 ===')
print()
print('第三章:')
print('  純中文字+標點: {:,}'.format(ch3['chinese']))
print('  所有非空白字符: {:,}'.format(ch3['all']))
print('  估計正文: ~{:,} 字'.format(ch3['chinese']))
print()
print('第四章:')
print('  純中文字+標點: {:,}'.format(ch4['chinese']))
print('  所有非空白字符: {:,}'.format(ch4['all']))
print('  估計正文: ~{:,} 字'.format(ch4['chinese']))
print()
print('=== 目標對比 ===')
print('第三章目標: 18,000-20,000字 -> 實際: ~{:,} 字 {}'.format(
    ch3['chinese'], '✅ 達標' if ch3['chinese'] >= 18000 else '❌ 未達標'))
print('第四章目標: 18,000-20,000字 -> 實際: ~{:,} 字 {}'.format(
    ch4['chinese'], '✅ 達標' if ch4['chinese'] >= 18000 else '❌ 未達標'))
print()
print('第四章還需擴寫: ~{:,} 字'.format(max(0, 18000 - ch4['chinese'])))
