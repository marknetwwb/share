#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 自動化任務
定時監控 Gmail 訂單並發送到群組
"""

import time
import schedule
import logging
from gmail_order_monitor import GmailOrderMonitor
from datetime import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenClawAutomation:
    def __init__(self):
        self.monitor = GmailOrderMonitor()
        self.start_time = datetime.now()
        
    def check_gmail_orders(self):
        """檢查 Gmail 訂單"""
        try:
            logger.info("開始檢查 Gmail 訂單...")
            self.monitor.monitor_gmail()
            logger.info("Gmail 訂單檢查完成")
        except Exception as e:
            logger.error(f"檢查 Gmail 訂單時發生錯誤: {str(e)}")
    
    def run_automation(self):
        """運行自動化任務"""
        logger.info("OpenClaw 自動化任務啟動")
        logger.info(f"開始時間: {self.start_time}")
        
        # 設定定時任務
        # 每 5 分鐘檢查一次
        schedule.every(5).minutes.do(self.check_gmail_orders)
        
        # 每小時執行一次
        schedule.every().hour.do(self.check_gmail_orders)
        
        # 每天早上 9 點執行一次
        schedule.every().day.at("09:00").do(self.check_gmail_orders)
        
        try:
            # 立即執行一次
            self.check_gmail_orders()
            
            # 保持程序運行
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分鐘檢查一次
                
        except KeyboardInterrupt:
            logger.info("自動化任務停止")
        except Exception as e:
            logger.error(f"自動化任務發生錯誤: {str(e)}")

if __name__ == "__main__":
    automation = OpenClawAutomation()
    automation.run_automation()