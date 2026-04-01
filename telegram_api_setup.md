# Telegram API Setup Guide

## 📱 為 Riki 配置 Telegram API

### **配置步驟**

#### 1. **Token 驗證**
```
Token: 8738273870:AAEUJKVy0Np0ytnUqs6W1cJ85Tn342Arta0
```
- ✅ Token 格式正確 (bot token 格式)
- ✅ 準備用於 Riki 嘅獨立連接

#### 2. **API 端點配置**
```bash
# 基本端點
BASE_URL=https://api.telegram.org/bot8738273870:AAEUJKVy0Np0ytnUqs6W1cJ85Tn342Arta0

# 測試連接
curl "$BASE_URL/getMe"
```

#### 3. **Webhook 設置** (如果需要)
```bash
# 設置 webhook
curl -X POST "$BASE_URL/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "YOUR_WEBHOOK_URL"}'
```

### **OpenClaw 配置建議**

#### **配置文件修改**
需要喺 OpenClaw 配置中添加新嘅 Telegram 連接：

```yaml
telegram:
  accounts:
    main:
      token: "MAIN_BOT_TOKEN"
      account_id: "default"
    riki:
      token: "8738273870:AAEUJKVy0Np0ytnUqs6W1cJ85Tn342Arta0"
      account_id: "riki"
      session_type: "subagent"
```

#### **會話映射**
```
主會話 (Airi)  → Telegram API 1
副會話 (Riki)  → Telegram API 2 (新配置)
```

### **測試驗證**

#### **1. 基本連接測試**
```bash
# 獲取 bot 信息
curl "https://api.telegram.org/bot8738273870:AAEUJKVy0Np0ytnUqs6W1cJ85Tn342Arta0/getMe"
```

#### **2. 發送測試消息**
```bash
# 發送測試消息
curl -X POST "https://api.telegram.org/bot8738273870:AAEUJKVy0Np0ytnUqs6W1cJ85Tn342Arta0/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "YOUR_CHAT_ID",
    "text": "Riki 測試消息！"
  }'
```

#### **3. Riki 功能測試**
- [x] Riki 基本功能正常
- [ ] Riki 獨立通信測試
- [ ] 任務分配功能驗證
- [ ] 回報機制測試

### **技術支持聯繫**

#### **需要 OpenClaw 支援嘅內容**
1. 多 Telegram API 配置支持
2. Sub-agent 獨立會話映射
3. 自動路由規則設置
4. 錯誤處理同重連機制

#### **聯繫資訊**
- 問題描述：需要為 Riki sub-agent 配置獨立嘅 Telegram API 連接
- Token：8738273870:AAEUJKVy0Np0ytnUqs6W1cJ85Tn342Arta0
- 期望功能：Riki 可以獨立接收 Telegram 消息並執行任務

### **注意事項**

#### **安全提醒**
- 🔒 妥善保存 Token，唔可以外泄
- 🔒 定期更換 Token 以確保安全
- 🔒 監控 API 使用情況

#### **使用限制**
- ⚠️ 每天 50 條消息限制（免費版本）
- ⚠️ 需要 Chat ID 先可以發送消息
- ⚠️ Webhook 需要可訪問嘅伺服器端點

#### **成本考慮**
- 💰 Telegram API 免費版本有使用限制
- 💰 如需更高頻率使用，考慮升級到付費版本
- 💰 需要伺服器支持 Webhook 功能

### **下一步行動**

1. **立即執行**：
   - [ ] 測試 Token 有效性
   - [ ] 驗證 API 連接
   - [ ] 準備 OpenClaw 配置文件

2. **技術支援**：
   - [ ] 聯繫 OpenClay 支援團隊
   - [ ] 提交多 API 配置請求
   - [ ] 確認配置可行性

3. **功能驗證**：
   - [ ] 測試 Riki 獨立通信
   - [ ] 驗證任務分配機制
   - [ ] 監控執行效果

---
**創建時間**: 2026-02-28 12:46 UTC
**狀態**: 配置文件已準備，等待技術支援
**負責人**: Airi