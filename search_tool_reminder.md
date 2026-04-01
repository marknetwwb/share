# 搜尋工具配置提醒

## 🔍 **主要搜尋工具**

### ✅ **主要使用：Serper.dev**
- **API Key**: 764229241579d0bcf83c9d749d07948979131dbd
- **工具文件**: serper_search_function.py
- **使用場景**: 所有網路搜索需求
- **優勢**: 已配置成功，測試通過

### ❌ **禁用工具：Brave Search**
- **問題**: API認證錯誤，無法使用
- **狀態**: 暫停使用
- **替代方案**: 完全使用 Serper.dev

## 📋 **使用規則**

1. **任何搜索需求**：首先使用 Serper.dev
2. **檢查工具文件**：serper_search_function.py
3. **驗證API狀態**：確認配置正常
4. **記錄使用結果**：在memory文件中記錄

## ⚠️ **錯誤預防**

### 常見錯誤：
- 錯誤使用 `web_search` 工具（Brave Search）
- 忘記檢查工具文件狀態
- 未驗證API可用性

### 預防措施：
- 每次搜索前確認工具選擇
- 使用 `exec` 執行 serper_search_function.py
- 在任務清單中標記工具使用狀態

## 🎯 **執行檢查清單**

### 搜索任務執行步驟：
1. [ ] 確認使用 Serper.dev，唔係 Brave Search
2. [ ] 檢查 serper_search_function.py 文件存在
3. [ ] 執行 python3 serper_search_function.py
4. [ ] 記錄搜索結果喺 memory 文件
5. [ ] 更新 HEARTBEAT.md 工具狀態

## 🔍 **工具使用範例**

### 正確用法：
```bash
python3 serper_search_function.py
# 或者在代碼中直接調用 serper_search() 函數
```

### 錯誤用法：
```bash
web_search  # 會使用 Brave Search，應該避免
```

## 💡 **記憶提醒**

**核心口令**: "Serper.dev，唔係 Brave Search！"

**每日檢查**: 每次開始工作前，確認搜尋工具配置

**文件證據**: 係 memory/2026-02-25.md 中記錄工具使用狀態