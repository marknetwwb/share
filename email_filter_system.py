#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
郵件過濾系統
記住兩重過濾格式，自動處理訂單郵件
"""

import re
from email_filter_config import (
    FIRST_FILTER_CONFIG,
    SECOND_FILTER_CONFIG,
    LOCATION_MAPPING,
    TIME_FORMATTING
)

class EmailFilterSystem:
    def __init__(self):
        self.first_filter_config = FIRST_FILTER_CONFIG
        self.second_filter_config = SECOND_FILTER_CONFIG
        self.location_mapping = LOCATION_MAPPING
        self.time_formatting = TIME_FORMATTING
    
    def first_level_filter(self, email_content):
        """第一重過濾：移除頭尾，保留訂單核心信息"""
        start_marker = self.first_filter_config["start_marker"]
        end_marker = self.first_filter_config["end_marker"]
        
        # 找到起始位置
        start_match = re.search(start_marker, email_content)
        if not start_match:
            return "Error: Could not find start marker"
        
        start_pos = start_match.start()
        
        # 找到結束位置
        end_match = re.search(end_marker, email_content)
        if not end_match:
            return "Error: Could not find end marker"
        
        end_pos = end_match.end()
        
        # 提取內容
        filtered_content = email_content[start_pos:end_pos]
        
        return filtered_content.strip()
    
    def extract_job_id(self, content):
        """提取 Job ID"""
        match = re.search(r'JOB ID:\s*(\d+)', content)
        return match.group(1) if match else None
    
    def extract_passengers(self, content):
        """提取客人人数 (1/3 格式)"""
        match = re.search(r'Number of Passengers.*?(\d+)', content)
        if match:
            passengers = match.group(1)
            return f"{passengers}/3"  # 假設最多3人
        return None
    
    def extract_service_time(self, content):
        """提取服務時間 (去掉 AM/PM)"""
        match = re.search(r'Service Time.*?(\d{1,2}:\d{2}\s*[AP]M)', content)
        if match:
            time_str = match.group(1)
            # 去掉 AM/PM，格式化為 HHMM
            time_str = time_str.replace('AM', '').replace('PM', '').strip()
            hours, minutes = time_str.split(':')
            return f"{hours.zfill(2)}{minutes}"
        return None
    
    def extract_service_date(self, content):
        """提取服務日期"""
        match = re.search(r'Service Date.*?(\d{4}年\d{1,2}月\d{1,2}日)', content)
        return match.group(1) if match else None
    
    def extract_location_info(self, content):
        """提取地點信息"""
        # 提取上車地點
        pickup_match = re.search(r'Pick Up Address.*?([^\n]+)', content)
        pickup = pickup_match.group(1).strip() if pickup_match else ""
        
        # 提取目的地
        destination_match = re.search(r'Itinerary / drop-off destination.*?([^\n]+)', content)
        destination = destination_match.group(1).strip() if destination_match else ""
        
        # 地點映射
        pickup_mapped = self.location_mapping.get(pickup, pickup)
        destination_mapped = self.location_mapping.get(destination, destination)
        
        return f"{pickup_mapped}>{destination_mapped}"
    
    def second_level_filter(self, email_content):
        """第二重過濾：四行格式"""
        # 先進行第一重過濾
        first_filtered = self.first_level_filter(email_content)
        
        # 提取各項信息
        job_id = self.extract_job_id(first_filtered)
        passengers = self.extract_passengers(first_filtered)
        service_time = self.extract_service_time(first_filtered)
        service_date = self.extract_service_date(first_filtered)
        location_info = self.extract_location_info(first_filtered)
        
        # 構建四行格式
        result = f"單号: {job_id}\n日期: {service_date}\n時間: {service_time}\n地點: {location_info}"
        
        return result
    
    def process_email(self, email_content):
        """處理郵件，返回兩重過濾結果"""
        first_filtered = self.first_level_filter(email_content)
        second_filtered = self.second_level_filter(email_content)
        
        return {
            "first_filter": first_filtered,
            "second_filter": second_filtered,
            "raw_email": email_content
        }

# 測試
if __name__ == "__main__":
    filter_system = EmailFilterSystem()
    
    # 測試郵件內容
    test_email = """
ACS BOOKING REQUEST
You have received a new booking from Asia Car Service. Please confirm the booking below and provide driver's name and mobile number. Call us at Tel No. +86 755 8213 2434 for any questions. 如有任何疑问，请您拨打 +86 755 8213 2434 与我们联系！ 

Driver Language: English Speaking Preferred drivers for service (首选司机): English speaking, regular drivers for ACS services include (流利英文司机): Simple English speaking, regular drivers for ACS services include (简单英文司机): JOB ID: 544163 Service Date (日期): 2026年03月01日 Service Time (时间): 09:15 AM Passenger Name and Phone # (客人姓名及电话号码): ASL Crew Members Greeting Sign (迎接牌): ASL Crew Members Number of Passengers (客人人数): 1 ( luggage) Car Type (车型): Toyota Alphard (5-6 Pax) (English Speaking Driver) Pick Up Address (上车地点): Crew: Mark Pranzewitsch ------------------------------------ HKG ---flight number tbc P1 Limo Lounge (call driver when you are ready) Itinerary / drop-off destination (具体行程或送达地址): Cordis Hong Kong Custom Quotation: Special Requests (特别要求): 请在车上备好矿泉水供客人饮用。(根据客人人数) 如果乘客直接和司机更改了行程导致费用变更的，请司机立即联系我司客服热线，我司会和乘客确认相关的费用问题。否则服务完之后比较难和乘客收取相关的费用。 Please call ACS at once if the passenger changes the itinerary with the driver, and ACS will confirm any extra cost for changes with the passenger. Otherwise, we may be unable to pay any extra cost for changes. 如接国际航班60分钟后 或 国内航班45分钟后 或 接酒店(工厂)10-15分钟后没有见到客人，请马上联系我司24小时客服 0755 2591 0372. If the driver can't find the pax in 60mins after the plane lands or in 15mins for non-airport pick-up, please call us at once +86 755 2591 0372. Best Regards, Operator: Amanda Chen The Asia Car Service Team Tel: +86 755 8213 2434 Email: bookings@asiacarservice.com Please call us 24 hours a day, 7 days a week. This message and any attachments are solely for the intended recipient and may contain confidential or privileged information. If you not the intended recipient, any disclosure, copying, use, or distribution of the information included in this message and any attachments is prohibited. If you have received this communication in error, please notify us by reply-e-mail and immediately and permanently delete this message and any attachments. Thank you.
"""
    
    # 處理郵件
    result = filter_system.process_email(test_email)
    
    print("📋 郵件過濾系統測試結果：")
    print("=" * 50)
    print("第一重過濾：")
    print(result["first_filter"])
    print("\n第二重過濾：")
    print(result["second_filter"])
    print("=" * 50)