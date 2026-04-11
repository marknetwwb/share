import pandas as pd
import os
from datetime import datetime

# 根據用戶提供嘅行程數據建立訂單輸入規則
def create_order_format():
    # 建立標準化嘅訂單格式
    order_columns = [
        'Order_ID',           # 訂單編號
        'Date',              # 日期
        'Time',              # 時間
        'Route',             # 路線
        'Passenger',         # 乘客
        'Cars_Required',     # 需要車輛數量
        'Drivers',          # 司機資料
        'License_Plates',    # 車牌號碼
        'Mobile_Numbers',    # 手機號碼
        'Pickup_Time',       # 上車時間
        'Dropoff_Time',      # 下車時間
        'Duration',          # 行程時間
        'Overtime_Fee',      # 超時費
        'Parking_Fee',       # 停車費
        'Total_Fee',         # 總費用
        'Customer_Info',     # 客戶資料
        'Notes'             # 備註
    ]
    
    # 創建數據框架
    df = pd.DataFrame(columns=order_columns)
    
    # 添加第一個訂單 (11月3日)
    order1_data = {
        'Order_ID': '546271',
        'Date': '2026-11-03',
        'Time': '12:06 - 16:52',
        'Route': '機場 → 旺角 → K11 → 長沙灣 → 迪士尼',
        'Passenger': 'Keith',
        'Cars_Required': 1,
        'Drivers': 'N/A',
        'License_Plates': 'N/A',
        'Mobile_Numbers': 'N/A',
        'Pickup_Time': '12:06',
        'Dropoff_Time': '16:52',
        'Duration': '5小時',
        'Overtime_Fee': 0,
        'Parking_Fee': 16,
        'Total_Fee': 1598,
        'Customer_Info': 'N/A',
        'Notes': '大嶼山附加費2X200=$400\n隧道費$16\n停車場$16'
    }
    
    # 添加第二個訂單 (4月4日)
    order2_data = {
        'Order_ID': '549906',
        'Date': '2026-04-04',
        'Time': '1:15',
        'Route': 'MB300 → 尖沙咀',
        'Passenger': '⁨U/阿恒 RN377 30 黑 Vellfire⁩',
        'Cars_Required': 2,
        'Drivers': 'Eva, Soo',
        'License_Plates': 'TZ9800, FN655',
        'Mobile_Numbers': '97062468, 6097 7620',
        'Pickup_Time': '1:58',
        'Dropoff_Time': '2:28',
        'Duration': '30分鐘',
        'Overtime_Fee': 60,
        'Parking_Fee': 35,
        'Total_Fee': 495,
        'Customer_Info': '⁨U/阿恒 RN377 30 黑 Vellfire⁩',
        'Notes': 'Driver: Eva\nPlate：TZ9800\nMobile：97062468\n\nDriver: Soo\nMobile: 6097 7620\nPlate: FN655'
    }
    
    # 將數據添加到DataFrame
    df.loc[0] = order1_data
    df.loc[1] = order2_data
    
    return df

# 建立司機價格表格式
def create_driver_price_format():
    price_columns = [
        'Location',          # 地點
        '九龙',              # 九龍價格
        '港岛',              # 港島價格
        '機場/東涌',         # 機場/東涌價格
        '大埔/上水',        # 大埔/上水價格
        '西貢',              # 西貢價格
        '元朗市/落馬洲',    # 元朗市/落馬洲價格
        '將軍澳',            # 將軍澳價格
        '沙田',              # 沙田價格
        '郵碼'              # 郵碼價格
    ]
    
    # 創建價格表數據框架
    price_df = pd.DataFrame(columns=price_columns)
    
    # 手動添加價格數據，確保列數匹配
    price_data = [
        ['司機價表', '', '九龙', 250, 300, 400, 360, 360, 410, 310],
        ['', '', '港岛', 300, 280, 400, 360, 290, 360, 310],
        ['', '', '機場/東涌', 400, 400, 400, 360, 290, 440, 310],
        ['', '', '大埔/上水', 360, 360, 400, 360, 290, 440, 310],
        ['', '', '西貢', 360, 360, 400, 360, 290, 360, 310],
        ['', '', '元朗市/落馬洲', 410, 410, 400, 410, 440, 440, 410],
        ['', '', '將軍澳', 310, 300, 400, 360, 250, 360, 250],
        ['', '', '沙田', 310, 300, 400, 290, 250, 410, 250],
        ['', '', '郵碼', 250, 250, 400, 450, 300, 450, 300],
        ['', '迪士尼 > AP', '迪士尼 > AP', 350, 350, 350, 350, 350, 350, 350],
        ['', 'AP > 迪士尼', 'AP > 迪士尼', 400, 400, 400, 400, 400, 400, 400],
        ['', '東涌　＞ＡＰ', '東涌　＞ＡＰ', 250, 250, 250, 250, 250, 250, 250],
        ['', 'ＡＰ＞　東涌', 'ＡＰ＞　東涌', 300, 300, 300, 300, 300, 300, 300]
    ]
    
    for i, row in enumerate(price_data):
        price_df.loc[i] = row
    
    return price_df

# 保存文件
def save_order_files():
    # 創建訂單文件
    order_df = create_order_format()
    order_df.to_excel('ACS_Orders_Input_Format.xlsx', index=False)
    
    # 創建司機價格表文件
    price_df = create_driver_price_format()
    price_df.to_excel('ACS_Driver_Price_Table.xlsx', index=False)
    
    print("訂單格式文件已創建:")
    print("1. ACS_Orders_Input_Format.xlsx - 訂單輸入格式")
    print("2. ACS_Driver_Price_Table.xlsx - 司機價格表")
    
    return order_df, price_df

# 主程序
if __name__ == "__main__":
    order_df, price_df = save_order_files()
    
    print("\n=== 訂單格式預覽 ===")
    print(order_df)
    
    print("\n=== 司機價格表預覽 ===")
    print(price_df)