# 郵件過濾系統 - 記憶文件

## 📋 過濾規則記錄

### 第一重過濾規則
- **起始點**: "JOB ID:"
- **結束點**: "请在车上备好矿泉水供客人饮用"
- **描述**: 移除郵件頭尾歡迎語，保留訂單核心信息
- **目標群組**: ACS BOOKING REQUEST (完整內容)

### 第二重過濾規則
- **格式**: 四行格式
- **第一行**: 單号: Job ID (例如: 單号: 544163)
- **第二行**: 日期: 服務日期 (例如: 日期: 2026年03月01日)
- **第三行**: 時間: 服務時間 (去掉 AM/PM，格式: 時間: 0915)
- **第四行**: 地點: 上車地點>目的地 (例如: 地點: HKG>Cordis)
- **目標群組**: 內部派單系統

### 標籤映射規則
- "P1 Limo Lounge" → "HKG"
- "Cordis Hong Kong" → "Cordis"
- "Airport" → "AP"

## 🎯 使用方法

### 1. 配置文件
- `email_filter_config.py`: 基礎配置
- `email_filter_system.py`: 過濾系統
- `email_filter_automation.py`: 自動化任務

### 2. 郵件處理
```python
from email_filter_system import EmailFilterSystem

filter_system = EmailFilterSystem()
result = filter_system.process_email(email_content)
```

### 3. 結果輸出
- 第一重過濾: 完整訂單信息
- 第二重過濾: 四行派單格式

## 📞 技術支持
- 如果規則需要調整，修改 `email_filter_config.py`
- 如果格式需要更改，修改 `email_filter_system.py`
- 如果群組需要更改，修改 `email_filter_automation.py`