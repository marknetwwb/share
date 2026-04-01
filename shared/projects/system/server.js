const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// 中間件
app.use(cors());
app.use(express.static('.'));

// Excel 檔案下載路由
app.get('/download', (req, res) => {
    const fileName = 'ACS_Order_MAR2026_CS---3474f087-3bc7-4a73-92d1-7d4857b78eb3.xlsx';
    const filePath = path.join(__dirname, 'documents', fileName);
    
    if (fs.existsSync(filePath)) {
        res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
        res.setHeader('Content-Disposition', `attachment; filename="${fileName}"`);
        res.sendFile(filePath);
    } else {
        res.status(404).json({ error: 'File not found' });
    }
});

// 主頁路由 - 提供下載連結
app.get('/', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Excel 檔案下載</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .download-section {
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .download-btn {
            display: inline-block;
            padding: 12px 24px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px 5px;
            transition: background 0.3s;
        }
        .download-btn:hover {
            background: #0056b3;
        }
        .info {
            margin: 10px 0;
            padding: 10px;
            background: #e9ecef;
            border-left: 4px solid #007bff;
        }
        .file-info {
            margin: 15px 0;
            padding: 15px;
            background: #d4edda;
            border-radius: 5px;
            border-left: 4px solid #28a745;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Excel 檔案下載中心</h1>
        
        <div class="file-info">
            <h3>📁 檔案資訊</h3>
            <p><strong>檔案名稱:</strong> ACS_Order_MAR2026_CS.xlsx</p>
            <p><strong>檔案大小:</strong> 182 KB</p>
            <p><strong>更新時間:</strong> ${new Date().toLocaleString('zh-HK')}</p>
            <p><strong>檔案類型:</strong> Excel 工作簿 (.xlsx)</p>
        </div>
        
        <div class="download-section">
            <h3>🔗 下載連結</h3>
            <p>點擊以下連結直接下載 Excel 檔案：</p>
            
            <a href="/download" class="download-btn">
                📥 直接下載 Excel 檔案
            </a>
            
            <div class="info">
                <p><strong>說明:</strong> 點擊連結後，檔案會自動下載到你的設備。</p>
                <p><strong>注意:</strong> 確保你的設備有安裝 Excel 或相容嘅軟件。</p>
            </div>
        </div>
        
        <div class="download-section">
            <h3>📋 檔案內容</h3>
            <p>呢個 Excel 檔案包含：</p>
            <ul>
                <li>🚕 車隊訂單記錄</li>
                <li>📅 每月訂單數據</li>
                <li>👥 司機資訊</li>
                <li>💰 收費明細</li>
            </ul>
        </div>
        
        <div class="info">
            <p><strong>技術支援:</strong> 如果下載遇到問題，請檢查網絡連接或重新嘗試。</p>
        </div>
    </div>
</body>
</html>
    `);
});

// 健康檢查路由
app.get('/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        timestamp: new Date().toISOString(),
        service: 'Excel file download server'
    });
});

// 錯誤處理中間件
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal server error' });
});

// 404 處理
app.use((req, res) => {
    res.status(404).json({ error: 'Not found' });
});

// 啟動服務器
app.listen(PORT, () => {
    console.log(`🚀 Excel file server running on port ${PORT}`);
    console.log(`📁 Serving files from: ${__dirname}`);
    console.log(`🔗 Download URL: https://your-railway-app.railway.app/download`);
    console.log(`🌐 Homepage: https://your-railway-app.railway.app/`);
});