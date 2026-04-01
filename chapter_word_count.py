#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def count_chinese_text(file_path):
    """計算文件中的中文、標點符號及有效內容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 只計算中文、中文標點符號和全角符號
        chinese_pattern = r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\uff10-\uff19\u3040-\u309f\u30a0-\u30ff]'
        chinese_chars = len(re.findall(chinese_pattern, content))
        
        # 計算所有非空白字符
        all_chars = len(content.replace('\n', '').replace(' ', '').replace('\r', ''))
        
        # 統計行數
        line_count = len(content.splitlines())
        
        # 估計純正文內容（去除markdown標記）
        # 移除markdown特殊字符 # * - | > ` 等等
        plain_content = re.sub(r'[#*\-\|>`~\[\]()\d]', '', content)
        plain_chars = len(plain_content.replace('\n', '').replace(' ', ''))
        
        return {
            'file_path': file_path,
            'chinese_chars': chinese_chars,
            'all_chars': all_chars,
            'plain_chars': plain_chars,
            'line_count': line_count,
            'estimated_words': chinese_chars
        }
        
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"讀取文件時出錯: {e}")
        return None

def main():
    # 檢查第三章
    chapter3_path = "/data/workspace/novel_season1_chapter3.md"
    chapter3_stats = count_chinese_text(chapter3_path)
    
    # 檢查第四章
    chapter4_path = "/data/workspace/novel_season1_chapter4.md"
    chapter4_stats = count_chinese_text(chapter4_path)
    
    # 輸出結果
    print("=" * 60)
    print("小說章節字數統計報告")
    print("=" * 60)
    
    if chapter3_stats:
        print(f"\n第三章: 《被操控的心跳》")
        print(f"📄 文件: {chapter3_stats['file_path']}")
        print(f"📊 中文字數+標點: {chapter3_stats['chinese_chars']:,}")
        print(f"📈 所有字符數: {chapter3_stats['all_chars']:,}")
        print(f"📝 純正文內容: ~{chapter3_stats['plain_chars']:,}")
        print(f"📄 總行數: {chapter3_stats['line_count']:,}")
        print(f"🎯 估計字數: ~{chapter3_stats['estimated_words']:,}")
        
        # 檢查是否達標
        target = 18500
        if chapter3_stats['estimated_words'] >= target:
            print(f"✅ 已達標! ({target:,} 字)")
        else:
            print(f"⚠️ 未達標 (目標: {target:,} 字)")
    
    print("\n" + "-" * 40)
    
    if chapter4_stats:
        print(f"\n第四章: 《被操控的心跳》")
        print(f"📄 文件: {chapter4_stats['file_path']}")
        print(f"📊 中文字數+標點: {chapter4_stats['chinese_chars']:,}")
        print(f"📈 所有字符數: {chapter4_stats['all_chars']:,}")
        print(f"📝 純正文內容: ~{chapter4_stats['plain_chars']:,}")
        print(f"📄 總行數: {chapter4_stats['line_count']:,}")
        print(f"🎯 估計字數: ~{chapter4_stats['estimated_words']:,}")
        
        # 檢查是否達標
        target_min = 18000
        target_max = 20000
        current = chapter4_stats['estimated_words']
        
        if current >= target_min and current <= target_max:
            print(f"✅ 已達標! ({target_min:,} - {target_max:,} 字)")
        elif current < target_min:
            print(f"❌ 需擴寫 (目標: {target_min:,} 字，當前: {current:,} 字)")
            remaining = target_min - current
            print(f"📝 需補充: ~{remaining:,} 字")
        else:
            print(f"⚠️ 超標 (目標: {target_max:,} 字，當前: {current:,} 字)")
    
    print("\n" + "=" * 60)
    print("總體進度報告")
    print("=" * 60)
    
    if chapter3_stats and chapter4_stats:
        total_chinese = chapter3_stats['chinese_chars'] + chapter4_stats['chinese_chars']
        total_estimated = chapter3_stats['estimated_words'] + chapter4_stats['estimated_words']
        
        print(f"總字數: ~{total_estimated:,} 字")
        print(f"第三章完成度: ~{chapter3_stats['estimated_words']:,} / 18,500 字")
        print(f"第四章完成度: ~{chapter4_stats['estimated_words']:,} / 18,000-20,000 字")
        
        print(f"\n🎯 當前狀態:")
        if chapter3_stats['estimated_words'] >= 18500:
            print("✅ 第三章: 已完成")
        else:
            print("⚠️ 第三章: 需要擴寫")
            
        if chapter4_stats['estimated_words'] >= 18000:
            print("✅ 第四章: 已完成")
        else:
            print("❌ 第四章: 需要大幅擴寫")

if __name__ == "__main__":
    main()