#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail 訂單監控系統
監控 Gmail 特定標籤，自動提取訂單信息並發送到群組
"""

import re
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import imaplib
import email
from email.header import decode_header
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GmailOrderMonitor:
    def __init__(self):
        self.gmail_config = {
            'imap_server': 'imap.gmail.com',
            'username': 'your_email@gmail.com',
            'password': 'your_app_password',
            'label': '訂單'  # Gmail 標籤
        }
        
        # 群組配置
        self.telegram_config = {
            'bot_token': 'your_telegram_bot_token',
            'chat_id': 'your_group_chat_id',
            'group_name': 'ACS BOOKING REQUEST'
        }
        
        # 訂單提取規則
        self.order_patterns = {
            'job_id': r'JOB ID:\s*(\d+)',
            'passengers': r'Number of Passengers.*?(\d+)',
            'service_date': r'Service Date.*?(\d{4}年\d{1,2}月\d{1,2}日)',
            'service_time': r'Service Time.*?(\d{1,2}:\d{2}\s*[AP]M)',
            'car_type': r'Car Type.*?([^(]+)',
            'pickup_address': r'Pick Up Address.*?([^\n]+)',
            'drop_off': r'Itinerary / drop-off destination.*?([^\n]+)'
        }
    
    def decode_header_str(self, header):
        """解碼郵件標題"""
        decoded = decode_header(header)
        if decoded[0][1]:
            return decoded[0][0].decode(decoded[0][1])
        return decoded[0][0].decode('utf-8')
    
    def extract_order_info(self, email_content: str) -> Dict[str, str]:
        """提取訂單關鍵信息"""
        order_info = {}
        
        for field, pattern in self.order_patterns.items():
            match = re.search(pattern, email_content, re.IGNORECASE)
            if match:
                order_info[field] = match.group(1).strip()
                logger.info(f"提取到 {field}: {order_info[field]}")
        
        # 添加時間戳
        order_info['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return order_info
    
    def format_order_message(self, order_info: Dict[str, str]) -> str:
        """格式化訂單信息為群組消息"""
        message = f"""
📋 新訂單通知

🆔 Job ID: {order_info.get('job_id', 'N/A')}
👥 客人人数: {order_info.get('passengers', 'N/A')}
📅 服務日期: {order_info.get('service_date', 'N/A')}
⏰ 服務時間: {order_info.get('service_time', 'N/A')}
🚗 車型: {order_info.get('car_type', 'N/A')}
📍 上車地點: {order_info.get('pickup_address', 'N/A')}
🎯 目的地: {order_info.get('drop_off', 'N/A')}

⏰ 接收時間: {order_info.get('timestamp', 'N/A')}
📱 群組: {self.telegram_config['group_name']}
"""
        return message.strip()
    
    def send_to_telegram(self, message: str) -> bool:
        """發送消息到 Telegram 群組"""
        import requests
        
        url = f"https://api.telegram.org/bot{self.telegram_config['bot_token']}/sendMessage"
        data = {
            'chat_id': self.telegram_config['chat_id'],
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    logger.info("訂單信息已成功發送到群組")
                    return True
            logger.error(f"Telegram 發送失敗: {response.text}")
            return False
        except Exception as e:
            logger.error(f"發送 Telegram 時發生錯誤: {str(e)}")
            return False
    
    def monitor_gmail(self):
        """監控 Gmail 訂單"""
        try:
            # 連接到 Gmail
            mail = imaplib.IMAP4_SSL(self.gmail_config['imap_server'])
            mail.login(self.gmail_config['username'], self.gmail_config['password'])
            
            # 選擇標籤
            mail.select(f'"{self.gmail_config["label"]}')
            
            # 搜索未讀郵件
            status, messages = mail.search(None, 'UNSEEN')
            
            if status == 'OK':
                email_ids = messages[0].split()
                logger.info(f"找到 {len(email_ids)} 封新訂單郵件")
                
                for email_id in email_ids:
                    # 獲取郵件內容
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    
                    if status == 'OK':
                        raw_email = msg_data[0][1]
                        email_message = email.message_from_bytes(raw_email)
                        
                        # 解碼郵件主題
                        subject = self.decode_header_str(email_message['Subject'])
                        logger.info(f"處理郵件: {subject}")
                        
                        # 獲取郵件正文
                        email_content = ""
                        if email_message.is_multipart():
                            for part in email_message.walk():
                                if part.get_content_type() == "text/plain":
                                    try:
                                        email_content += part.get_payload(decode=True).decode('utf-8')
                                    except:
                                        email_content += part.get_payload(decode=True).decode('gb2312')
                        else:
                            try:
                                email_content = email_message.get_payload(decode=True).decode('utf-8')
                            except:
                                email_content = email_message.get_payload(decode=True).decode('gb2312')
                        
                        # 提取訂單信息
                        order_info = self.extract_order_info(email_content)
                        
                        if order_info:
                            # 格式化消息
                            message = self.format_order_message(order樊�
                        
                            # 發送到 Telegram
                            if self.send_to_telegram(message):
                                logger.info(f"訂單 {order_info.get('job_id')} 已處理完成")
                                
                                # 標記為已讀
                                mail.store(email_id, '+FLAGS', '\\Seen')
                        else:
                            logger.warning("未能提取到訂單信息")
                
                mail.close()
                mail.logout()
                
        except Exception as e:
            logger.error(f監控 Gmail 時發生錯誤: {str(e)}")

if __name__ == "__main__":
    monitor = GmailOrderMonitor()
    monitor.monitor_gmail()