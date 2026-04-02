# 車隊記憶 - Excel 輸入格式規則

## 📅 **格式對比總結**

### **三月份格式 (MAR2026)**
```
列標題: ['Ord No.', 'Time', 'Trip', 'Driver', 'Status', 'Pick', 'Drop', 'Decp', 'Ptime', 'Driver.Details', 'Dvr.OT', 'Dvr.C', 'Driver.C+OT', 'Bouns']
```

**特點：**
1. **Time格式**: 包含秒數 (HH:MM:SS)
   - 例: "03:30:00", "08:10:00"

2. **Trip格式**: 使用 "-" 或 ">" 連接
   - 例: "TST-AP", "3V951 > Cordis"

3. **Driver格式**: 包含完整信息
   - 例: "Stanley LJ9800 9828 6100"
   - 例: "Ricky ZJ6071 5108 9715"
   - 例: "(Ricky 已付） Donny DC8685 62258245"

4. **Decp欄位**: 通常為空

5. **Driver.Details**: 包含備註信息
   - 例: "OT $60" (加班費)
   - 例: "P$35" (車位費)
   - 例: "4 hour on hire, 機場$200隧道$42"

6. **Dvr.OT**: 數值格式 (加班費)
   - 例: "60", "35"

7. **Dvr.C**: 數值格式 (車位費/基本費)
   - 例: "400"

### **四月份格式 (APR2026)**
```
列標題: ['Ord No.', 'Time', 'Trip', 'Driver', 'Status', 'Pick', 'Drop', 'Decp', 'Ptime', 'Driver.Details', 'Dvr.OT', 'Dvr.C', 'Driver.C+OT', 'Bouns']
```

**特點：**
1. **Time格式**: 不包含秒數 (HH:MM 或 HH:MM AM/PM)
   - 例: "3:00", "4:30", "10:25 AM", "09:00 AM"

2. **Trip格式**: 使用 ">" 連接
   - 例: "TST > AP"
   - 例: "CX983 > 迪士尼荷里活酒店"
   - 例: "Cordis > AP"

3. **Driver格式**: 只有司機姓名
   - 例: "Eva"
   - 例: "Jacky"
   - 例: "Keith 陳"

4. **Decp欄位**: 包含備註信息
   - 例: "OT$60"
   - 例: "2 booster"
   - 例: "P$35"

5. **Driver.Details**: 包含完整信息
   - 例: "Eva TZ9800 97062468"
   - 例: "Jacky CT8022 69986953"
   - 例: "Keith 陳 CK9898 98880261"

6. **Dvr.OT**: 數值格式 (加班費)
   - 例: "60"

7. **Dvr.C**: 數值格式 (車位費)
   - 例: "35"

## 🔧 **輸入規則總結**

### **通用規則：**
1. **工作表命名**: [日期][月份縮寫][年份]
   - 例: "1MAR2026", "1APR2026"

2. **列順序**: 必須按照標準順序
   - Ord No. → Time → Trip → Driver → Status → Pick → Drop → Decp → Ptime → Driver.Details → Dvr.OT → Dvr.C → Driver.C+OT → Bouns

3. **雙車輛處理**: 同一訂單多台車分兩行輸入
   - 保持相同 Ord No.
   - 第二行包含第二台車的司機信息

### **數據格式要求：**
1. **Ord No.**: 訂單編號，數字格式
2. **Time**: 
   - 三月: HH:MM:SS
   - 四月: HH:MM 或 HH:MM AM/PM
3. **Trip**: 路線信息，使用標準符號
4. **Driver**: 三月=完整信息，四月=姓名
5. **Status**: 通常為空或 "Done"
6. **Pick/Drop**: 時間格式與 Time 一致
7. **Decp**: 備註信息
8. **Ptime**: 實際上車時間
9. **Driver.Details**: 三月=備註，四月=完整信息
10. **Dvr.OT**: 數值，加班費
11. **Dvr.C**: 數值，車位費/基本費
12. **Driver.C+OT**: 公式 =SUM(K:L)
13. **Bouns**: 通常為 "30"

### **特別注意：**
- 三月份：Driver 欄位包含完整信息，Driver.Details 為備註
- 四月份：Driver 欄位只有姓名，Decp 欄位包含備註
- 雙車輛訂單必須分兩行輸入
- 數值欄位必須為數字格式
- 時間格式必須與工作表月份一致

---
**記錄時間**: 2026-04-02
**來源**: 三月份和四月份 Excel 樣本分析
**用途**: 指導未來車隊訂單輸入工作