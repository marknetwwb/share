# OpenClaw 配置備份記錄

## 備份檔案
- **檔案名稱**: openclaw_20260301_094317.json
- **備份時間**: 2026年3月1日 09:43:17 UTC
- **原始路徑**: /data/.openclaw/openclaw.json
- **備份路徑**: /data/workspace/backup_config/openclaw_20260301_094317.json

## 備份原因
修復 Riki main subagent 嘅配置問題，包括：
1. 清理過期嘅 session 檔案
2. 修復配置文件格式
3. 優化 subagent 管理配置

## 還原指令
```bash
# 還原到最新嘅備份檔案
cp /data/workspace/backup_config/openclaw_20260301_094317.json /data/.openclaw/openclaw.json

# 或者還原到特定日期嘅備份
cp /data/workspace/backup_config/openclaw_YYYYMMDD_HHMMSS.json /data/.openclaw/openclaw.json
```

## 還原後嘅步驟
1. 重啟 OpenClaw 服務
2. 檢查配置是否正常
3. 驗證 subagent 功能

## 安全提醒
- ✅ 備份已完成
- ✅ 時間戳記錄正確
- ✅ 檔案權限設定正確
- ✅ 備份路徑安全