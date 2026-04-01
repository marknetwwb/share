# Telegram 配置備份

## 📋 當前配置狀態

### **原始配置**
```json
{
  "telegram": {
    "enabled": true,
    "dmPolicy": "pairing",
    "botToken": "__OPENCLAW_REDACTED__",
    "groupPolicy": "allowlist",
    "streaming": "partial"
  }
}
```

### **配置路徑**
- **配置路徑**: `channels.telegram`
- **狀態**: 已有基本配置
- **Token**: 已被隱藏 (__OPENCLAW_REDACTED__)

---

## 🔄 配置修改計劃

### **目標**
添加第二個 Telegram 帳戶配置，專門用於 Riki sub-agent。

### **修改策略**
1. **擴展現有配置**：喺 `channels.telegram` 下添加多個帳戶
2. **添加 Riki 專用配置**：為 Riki 創建獨立嘅帳戶設置
3. **維持現有功能**：確保原有配置唔會受影響

---

## 🛠️ 配置修改方案

### **方案 A: 多帳戶配置**
```json
{
  "channels": {
    "telegram": {
      "accounts": {
        "main": {
          "enabled": true,
          "dmPolicy": "pairing",
          "botToken": "MAIN_TOKEN",
          "groupPolicy": "allowlist",
          "streaming": "partial"
        },
        "riki": {
          "enabled": true,
          "dmPolicy": "pairing",
          "botToken": "8738273870:AAEUJKVy0Np0ytnUqs6W1cJ85Tn342Arta0",
          "groupPolicy": "allowlist",
          "streaming": "partial",
          "subagent": {
            "sessionKey": "agent:main:subagent:745e8a32-af19-4d79-9a4a-2fad87b5317b",
            "enabled": true
          }
        }
      }
    }
  }
}
```

### **方案 B: 平行配置**
```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "pairing",
      "botToken": "MAIN_TOKEN",
      "groupPolicy": "allowlist",
      "streaming": "partial"
    },
    "telegram_riki": {
      "enabled": true,
      "dmPolicy": "pairing",
      "botToken": "8738273870:AAEUJKVy0Np0ytnUqs6W1cJ85Tn342Arta0",
      "groupPolicy": "allowlist",
      "streaming": "partial"
    }
  }
}
```

---

## ⚠️ 風險提醒

### **修改前備份**
- [x ] 已備份當前配置
- [ ] 測試修改後功能
- [ ] 確保無法回退時嘅恢復方案

### **潛在風險**
1. **配置錯誤**：可能導致 Telegram 連接失敗
2. **功能影響**：可能影響現有嘅 Telegram 功能
3. **權限問題**：可能需要重新配置權限

---

## 📝 修改記錄

### **修改時間**
- **開始時間**: 2026-02-28 12:50 UTC
- **修改人**: Airi
- **修改原因**: 為 Riki sub-agent 添加獨立嘅 Telegram 連接

### **修改內容**
- 添加第二個 Telegram 帳戶配置
- 綁定 Riki sub-agent 到新配置
- 確保兩個帳戶可以獨立運作

### **預期效果**
- ✅ Riki 可以獨立接收同發送消息
- ✅ Ricky 可以直接同 Riki 通信
- ✅ 保持現有 Telegram 功能唔受影響

---
**備份完成**: 2026-02-28 12:50 UTC
**狀態**: 等待執行配置修改