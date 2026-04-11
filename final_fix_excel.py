import pandas as pd
from datetime import datetime, timedelta

file_path = 'ACS_Order_MAR2026_CS_1---d01fac1d-684c-4db4-89ba-3d9fcb2dba19.xlsx'

# 訂單數據
orders_data = {
    '25MAR2026': [
        {'order_no': 546543, 'time': '02:30:00', 'trip': 'MB300 > TST', 'driver': 'Eva TZ9800 97062468', 'ot': 60, 'p': 35, 'bb': 80},
        {'order_no': 546544, 'time': '03:45:00', 'trip': 'TST > CWB', 'driver': 'Stanley LJ9800 98286100', 'ot': 45, 'p': 35, 'bb': 0},
        {'order_no': 546545, 'time': '05:15:00', 'trip': 'CWB > NT', 'driver': 'Patrick WW8421 93182082', 'ot': 90, 'p': 35, 'bb': 80},
    ],
    '26MAR2026': [
        {'order_no': 546546, 'time': '01:30:00', 'trip': 'NT > YTM', 'driver': 'Tommy CL9800 97062468', 'ot': 30, 'p': 35, 'bb': 0},
        {'order_no': 546547, 'time': '04:20:00', 'trip': 'YTM > KLN', 'driver': 'Jacky WW8800 98286100', 'ot': 60, 'p': 35, 'bb': 80},
        {'order_no': 546548, 'time': '06:45:00', 'trip': 'KLN > HKG', 'driver': 'Kelvin WW8421 93182082', 'ot': 120, 'p': 35, 'bb': 0},
    ],
    '31MAR2026': [
        {'order_no': 546549, 'time': '02:00:00', 'trip': 'HKG > TST', 'driver': 'Vivian WW9800 97062468', 'ot': 75, 'p': 35, 'bb': 80},
        {'order_no': 546550, 'time': '03:30:00', 'trip': 'TST > CWB', 'driver': 'Michael WW8800 98286100', 'ot': 45, 'p': 35, 'bb': 0},
        {'order_no': 546551, 'time': '05:45:00', 'trip': 'CWB > NT', 'driver': 'David WW8421 93182082', 'ot': 90, 'p': 35, 'bb': 80},
    ]
}

print("重新修正Excel檔案，保持原有格式...")
print("=" * 60)

for date, orders in orders_data.items():
    print(f"\\n處理 {date}:")
    
    # 創建數據行，完全按照原有格式
    data_rows = []
    
    for order in orders:
        # 計算時間
        start_time = datetime.strptime(order['time'], '%H:%M:%S')
        pickup_time = start_time  # 上車時間 = 預約時間
        drop_time = start_time + timedelta(minutes=30)  # 下車時間 = 上車時間+30分鐘
        
        # 計算費用
        additional_fees = order['ot'] + order['p'] + order['bb']
        total_cost = 400 + additional_fees  # 基本價$400 + 附加費
        
        # 根據原有格式創建行
        # 格式：[訂單號, 時間, 路線, 司機, 狀態, 上車時間, 下車時間, 空, 空, 附加費說明, OT費用, 基本價, 空, 獎金, 總費用, 空]
        row_data = [
            order['order_no'],                    # 訂單號
            order['time'],                        # 時間
            order['trip'],                        # 路線  
            order['driver'],                      # 司機 (Column D)
            'Done',                               # 狀態
            pickup_time.time(),                   # 上車時間
            drop_time.time(),                     # 下車時間
            None,                                 # 空
            None,                                 # 空
            f'OT${order["ot"]}, P${order["p"]}, BB seat${order["bb"]}' if additional_fees > 0 else None,  # 附加費說明 (Column J)
            order['ot'],                          # OT費用
            400,                                  # 基本價
            None,                                 # 空
            30,                                   # 獎金
            total_cost,                           # 總費用 (Column M)
            None                                  # 空
        ]
        data_rows.append(row_data)
    
    # 讀取原有sheet，保留所有現有內容
    existing_df = pd.read_excel(file_path, sheet_name=date)
    
    # 將新數據添加到現有數據嘅前面
    # 我們要保留所有原有行，只喺開頭添加新訂單
    if len(existing_df) > 0:
        # 如果第一行係header，我哋保留header，將新數據加喺header後面
        new_df = pd.concat([existing_df.iloc[0:1], pd.DataFrame(data_rows)], ignore_index=True)
        
        # 如果有原有數據行，保留佢哋
        if len(existing_df) > 1:
            new_df = pd.concat([new_df, existing_df.iloc[1:]], ignore_index=True)
    else:
        # 如果冇原有數據，直接創建新嘅DataFrame
        new_df = pd.DataFrame(data_rows)
    
    # 保存修正後嘅檔案
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        new_df.to_excel(writer, sheet_name=date, index=False)
    
    print(f"✅ {date} 已修正")
    
    # 驗證結果
    verify_df = pd.read_excel(file_path, sheet_name=date)
    print(f"修正後總行數: {len(verify_df)}")
    
    # 顯示前3行做驗證
    if len(verify_df) > 0:
        print("前3行樣本:")
        for i in range(min(3, len(verify_df))):
            row = verify_df.iloc[i]
            non_empty_vals = [(j, val) for j, val in enumerate(row) if pd.notna(val) and str(val).strip() != '']
            print(f"行{i+1}: {[f'Col{j}: {val}' for j, val in non_empty_vals[:5]]}")

print("\\n" + "=" * 60)
print("✅ 所有日期已重新修正，保持原有格式！")