import pandas as pd
from datetime import datetime
import random
import string

class ACSOrderManager:
    def __init__(self):
        self.order_columns = [
            'Order_ID', 'Date', 'Time', 'Route', 'Passenger', 'Cars_Required',
            'Drivers', 'License_Plates', 'Mobile_Numbers', 'Pickup_Time',
            'Dropoff_Time', 'Duration', 'Overtime_Fee', 'Parking_Fee',
            'Total_Fee', 'Customer_Info', 'Notes'
        ]
        
        # 司機資料庫
        self.drivers_db = [
            {'name': 'Eva', 'plate': 'TZ9800', 'mobile': '97062468'},
            {'name': 'Soo', 'plate': 'FN655', 'mobile': '6097 7620'},
            {'name': 'John', 'plate': 'AB123', 'mobile': '9123 4567'},
            {'name': 'Mary', 'plate': 'CD456', 'mobile': '9234 5678'},
            {'name': 'Peter', 'plate': 'EF789', 'mobile': '9345 6789'},
            {'name': 'Amy', 'plate': 'GH012', 'mobile': '9456 7890'},
            {'name': 'David', 'plate': 'IJ345', 'mobile': '9567 8901'},
            {'name': 'Lisa', 'plate': 'KL678', 'mobile': '9678 9012'}
        ]
        
        # 路線價格表
        self.route_prices = {
            '九龙': 250, '港岛': 300, '機場/東涌': 400, '大埔/上水': 360,
            '西貢': 360, '元朗市/落馬洲': 410, '將軍澳': 310, '沙田': 310, '郵碼': 250
        }
        
    def generate_order_id(self):
        """生成訂單編號"""
        return ''.join(random.choices(string.digits, k=6))
    
    def calculate_base_fee(self, route, cars_required=1):
        """計算基礎費用"""
        # 提取起點和終點
        if '→' in route:
            start, end = route.split('→', 1)
        elif '＞' in route:
            start, end = route.split('＞', 1)
        else:
            # 如果只有一個地點，使用該地點價格
            start = route.strip()
            end = route.strip()
        
        # 獲取價格
        start_price = self.route_prices.get(start.strip(), 300)
        end_price = self.route_prices.get(end.strip(), 300)
        
        # 計算費用（取較高價格）
        base_fee = max(start_price, end_price) * cars_required
        return base_fee
    
    def get_available_drivers(self, cars_required):
        """獲取可用司機"""
        available_drivers = []
        driver_names = []
        plates = []
        mobiles = []
        
        for i in range(cars_required):
            if i < len(self.drivers_db):
                driver = self.drivers_db[i]
                available_drivers.append(driver)
                driver_names.append(driver['name'])
                plates.append(driver['plate'])
                mobiles.append(driver['mobile'])
            else:
                # 如果司機不足，生成隨機數據
                driver_names.append(f'Driver_{i+1}')
                plates.append(f'XXX{i+1:03d}')
                mobiles.append(f'9{random.randint(1000, 9999)} {random.randint(1000, 9999)}')
        
        return {
            'drivers': ', '.join(driver_names),
            'plates': ', '.join(plates),
            'mobiles': ', '.join(mobiles),
            'driver_details': available_drivers
        }
    
    def create_order(self, date, time, route, passenger, cars_required=1, 
                    customer_info='', overtime_fee=0, parking_fee=0):
        """創建新訂單"""
        
        # 生成訂單ID
        order_id = self.generate_order_id()
        
        # 計算基礎費用
        base_fee = self.calculate_base_fee(route, cars_required)
        
        # 獲取司機資料
        driver_info = self.get_available_drivers(cars_required)
        
        # 計算總費用
        total_fee = base_fee + overtime_fee + parking_fee
        
        # 設置時間點
        if time.count(':') == 1:  # 格式：1:15
            hour, minute = map(int, time.split(':'))
            pickup_time = f"{hour:02d}:{minute:02d}"
            dropoff_time = f"{(hour + 1):02d}:{minute:02d}"
            duration = "1小時"
        else:  # 格式：12:06 - 16:52
            pickup_time = time.split(' - ')[0]
            dropoff_time = time.split(' - ')[1]
            start_h, start_m = map(int, pickup_time.split(':'))
            end_h, end_m = map(int, dropoff_time.split(':'))
            duration_hours = end_h - start_h
            duration_minutes = end_m - start_m
            duration = f"{duration_hours}小時{duration_minutes}分鐘" if duration_minutes > 0 else f"{duration_hours}小時"
        
        # 創建訂單數據
        order_data = {
            'Order_ID': order_id,
            'Date': date,
            'Time': time,
            'Route': route,
            'Passenger': passenger,
            'Cars_Required': cars_required,
            'Drivers': driver_info['drivers'],
            'License_Plates': driver_info['plates'],
            'Mobile_Numbers': driver_info['mobiles'],
            'Pickup_Time': pickup_time,
            'Dropoff_Time': dropoff_time,
            'Duration': duration,
            'Overtime_Fee': overtime_fee,
            'Parking_Fee': parking_fee,
            'Total_Fee': total_fee,
            'Customer_Info': customer_info,
            'Notes': f'基礎費用：${base_fee}\n超時費：${overtime_fee}\n停車費：${parking_fee}\n總費用：${total_fee}'
        }
        
        return order_data, driver_info['driver_details']
    
    def load_existing_orders(self, file_path):
        """載入現有訂單"""
        if os.path.exists(file_path):
            return pd.read_excel(file_path)
        return pd.DataFrame(columns=self.order_columns)
    
    def save_orders(self, orders_df, file_path):
        """保存訂單到文件"""
        orders_df.to_excel(file_path, index=False)
        print(f"訂單已保存到 {file_path}")
    
    def add_order_to_file(self, file_path, order_data):
        """將訂單添加到文件"""
        # 載入現有訂單
        existing_orders = self.load_existing_orders(file_path)
        
        # 創建新訂單DataFrame
        new_order_df = pd.DataFrame([order_data])
        
        # 合併訂單
        updated_orders = pd.concat([existing_orders, new_order_df], ignore_index=True)
        
        # 保存文件
        self.save_orders(updated_orders, file_path)
        
        return updated_orders
    
    def display_orders(self, orders_df, limit=10):
        """顯示訂單"""
        if len(orders_df) == 0:
            print("無訂單數據")
            return
        
        print(f"\n=== 訂單列表 (共{len(orders_df)}筆) ===")
        print(orders_df.head(limit).to_string())
        
        if len(orders_df) > limit:
            print(f"... 還有 {len(orders_df) - limit} 筆訂單")
    
    def create_sample_orders(self):
        """創建樣本訂單"""
        sample_orders = [
            {
                'date': '2026-04-10',
                'time': '14:30',
                'route': '中環 → 尖沙咀',
                'passenger': '陳先生',
                'cars_required': 1,
                'customer_info': 'VIP客戶',
                'overtime_fee': 0,
                'parking_fee': 20
            },
            {
                'date': '2026-04-11',
                'time': '09:15 - 11:45',
                'route': '機場 → 銅鑼灣',
                'passenger': '李小姐',
                'cars_required': 2,
                'customer_info': '商務團隊',
                'overtime_fee': 80,
                'parking_fee': 50
            },
            {
                'date': '2026-04-12',
                'time': '16:00',
                'route': '旺角 → 迪士尼',
                'passenger': '張一家',
                'cars_required': 1,
                'customer_info': '家庭旅遊',
                'overtime_fee': 0,
                'parking_fee': 35
            }
        ]
        
        orders = []
        for sample in sample_orders:
            order_data, driver_details = self.create_order(
                sample['date'], sample['time'], sample['route'], 
                sample['passenger'], sample['cars_required'], 
                sample['customer_info'], sample['overtime_fee'], sample['parking_fee']
            )
            orders.append(order_data)
        
        return orders

# 創建訂單管理器並添加樣本訂單
if __name__ == "__main__":
    import os
    
    manager = ACSOrderManager()
    
    # 設定文件路徑
    order_file = 'ACS_Orders_Input_Format.xlsx'
    
    print("=== ACS 訂單管理系統 ===")
    print("正在創建樣本訂單...")
    
    # 創建並添加樣本訂單
    sample_orders = manager.create_sample_orders()
    
    for i, order_data in enumerate(sample_orders):
        manager.add_order_to_file(order_file, order_data)
        print(f"樣本訂單 {i+1} 已添加！")
        print(f"訂單ID: {order_data['Order_ID']}")
        print(f"路線: {order_data['Route']}")
        print(f"總費用: ${order_data['Total_Fee']}")
        print()
    
    # 顯示所有訂單
    orders_df = manager.load_existing_orders(order_file)
    manager.display_orders(orders_df)
    
    print(f"\n=== 訂單管理完成 ===")
    print(f"總共添加了 {len(sample_orders)} 筆新訂單")
    print(f"最新訂單文件: {order_file}")