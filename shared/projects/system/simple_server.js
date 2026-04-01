const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

// 創建 HTTP 服務器
const server = http.createServer((req, res) => {
    // 設置 CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    if (req.url === '/' || req.url === '/index') {
        // 首頁 - 提供下載連結
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(`
<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Excel 檔案下載</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .download-btn { display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px 5px; }
        .download-btn:hover { background: #0056b3; }
        .info { margin: 10px 0; padding: 10px; background: #e9ecef; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Excel 檔案下載中心</h1>
        
        <div class="info">
            <h3>📁 檔案資訊</h3>
            <p><strong>檔案名稱:</strong> ACS_Order_MAR2026_CS.xlsx</p>
            <p><strong>檔案大小:</strong> 182 KB</p>
            <p><strong>更新時間:</strong> ${new Date().toLocaleString('zh-HK')}</p>
        </div>
        
        <div class="info">
            <h3>🔗 下載連結</h3>
            <p><a href="/download" class="download-btn">📥 直接下載 Excel 檔案</a></p>
        </div>
        
        <div class="info">
            <h3>📋 檔案內容</h3>
            <p>呢個 Excel 檔案包含：</p>
            <ul>
                <li>🚕 車隊訂單記錄</li>
                <li>📅 16MAR2026 所有訂單</li>
                <li>👥 司機資訊</li>
                <li>💰 收費明細</li>
            </ul>
        </div>
    </div>
</body>
</html>
        `);
    } else if (req.url === '/download') {
        // 下載路由
        const fileName = 'ACS_Order_MAR2026_CS---3474f087-3bc7-4a73-92d1-7d4857b78eb3.xlsx';
        const filePath = path.join(__dirname, 'documents', fileName);
        
        if (fs.existsSync(filePath)) {
            const stats = fs.statSync(filePath);
            
            res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
            res.setHeader('Content-Disposition', `attachment; filename="${fileName}"`);
            res.setHeader('Content-Length', stats.size);
            
            const readStream = fs.createReadStream(filePath);
            readStream.pipe(res);
        } else {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('File not found');
        }
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not found');
    }
});

server.listen(PORT, () => {
    console.log(`🚀 Excel file server running on port ${PORT}`);
    console.log(`📁 Serving files from: ${__dirname}`);
    console.log(`🔗 Download URL: http://localhost:${PORT}/download`);
    console.log(`🌐 Homepage: http://localhost:${PORT}/`);
});

console.log('✅ Server started successfully!');
console.log('📋 Excel file is ready for download!');
console.log('🔗 Access the server at: http://localhost:3000');
console.log('💾 File location: /documents/ACS_Order_MAR2026_CS---3474f087-3bc7-4a73-92d1-7d4857b78eb3.xlsx');
console.log('⏹️  Press Ctrl+C to stop the server');
"