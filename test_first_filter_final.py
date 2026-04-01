#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
調整後第一重過濾測試：到備好飲用水為止
"""

import re

def first_level_filter_final(email_content):
    """最終第一重過濾：到飲用水相關內容為止"""
    
    # 找到 JOB ID 的位置
    job_id_pattern = r'JOB ID:'
    job_id_match = re.search(job_id_pattern, email_content)
    
    if not job_id_match:
        return "未能找到 JOB ID 標記"
    
    # 從 JOB ID 開始
    start_pos = job_id_match.start()
    
    # 找到結束位置：到飲用水相關內容
    # 嘗試多種匹配模式
    end_patterns = [
        r'请在车上备好矿泉水供客人饮用',
        r'提供客人飲用水',
        r'备好矿泉水',
        r'根据客人人数',
        r'备好矿泉水供客人饮用'
    ]
    
    end_pos = None
    for pattern in end_patterns:
        end_match = re.search(pattern, email_content)
        if end_match:
            end_pos = end_match.end()
            break
    
    if not end_pos:
        return "未能找到飲用水相關標記"
    
    # 提取內容
    filtered_content = email_content[start_pos:end_pos]
    
    return filtered_content.strip()

# 測試郵件內容
test_email_content = """
ACS BOOKING REQUEST
You have received a new booking from Asia Car Service. Please confirm the booking below and provide driver's name and mobile number. Call us at Tel No. +86 755 8213 2434 for any questions. 如有任何疑问，请您拨打 +86 755 8213 2434 与我们联系！ 

Driver Language: None
Preferred drivers for service (首选司机):
JOB ID:     544167
Service Date (日期):     2026年03月01日
Service Time (时间):     18:00 PM
Passenger Name and Phone # (客人姓名及电话号码):     ASL Crew Members
Greeting Sign (迎接牌):     ASL Crew Members
Number of Passengers (客人人数):     1 ( luggage)
Car Type (车型):     Toyota Alphard (5-6 Pax)
Pick Up Address (上车地点):     Crew: 

Sergej Ulzaev


------------------------------------
Cordis Hong Kong
Itinerary / drop-off destination (具体行程或送达地址):     HKG
Custom Quotation:   
Special Requests (特别要求):   
请在车上备好矿泉水供客人饮用。(根据客人人数)
如果乘客直接和司机更改了行程导致费用变更的，请司机立即联系我司客服热线，我司会和乘客确认相关的费用问题。否则服务完之后比较难和乘客收取相关的费用。 Please call ACS at once if the passenger changes the itinerary with the driver, and ACS will confirm any extra cost for changes with the passenger. Otherwise, we may be unable to pay any extra cost for changes.
如接国际航班60分钟后 或 国内航班45分钟后 或 接酒店(工厂)10-15分钟后没有见到客人，请马上联系我司24小时客服 0755 2591 0372. If the driver can't find the pax in 60mins after the plane lands or in 15mins for non-airport pick-up, please call us at once +86 755 2591 0372.
Best Regards,
Operator: Amanda Chen
The Asia Car Service Team
Tel: +86 755 8213 2434
Email: bookings@asiacarservice.com
Please call us 24 hours a day, 7 days a week.

This message and any attachments are solely for the intended recipient and may contain confidential or privileged information. If you are not the intended recipient, any disclosure, copying, use, or distribution of the information included in this message and any attachments is prohibited. If you have received this communication in error, please notify us by reply-e-mail and immediately and permanently delete this message and any attachments. Thank you.
"""

# 執行最終第一重過濾
result = first_level_filter_final(test_email_content)

print("📋 最終第一重過濾測試結果：")
print("=" * 60)
print(result)
print("=" * 60)