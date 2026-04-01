#!/bin/bash

# Excel 檔案下載服務器啟動腳本
# 用於啟動 HTTP 服務器提供 Excel 檔案下載

echo "🚀 啟動 Excel 檔案下載服務器..."

# 設定變量
STATIC_DIR="/data/workspace/shared"
PORT=8000
EXCEL_FILE="/data/.openclaw/media/inbound/ACS_Order_MAR2026_CS---3474f087-3bc7-4a73-92d1-7d4857b78eb3.xlsx"

# 檢查檔案是否存在
if [ ! -f "$EXCEL_FILE" ]; then
    echo "❌ Excel 檔案不存在: $EXCEL_FILE"
    exit 1
fi

echo "✅ Excel 檔案找到: $EXCEL_FILE"
echo "📁 服務器目錄: $STATIC_DIR"
echo "🔗 偵聽端口: $PORT"
echo
echo "🔗 下載連結:"
echo "   Excel 檔案: http://localhost:$PORT/documents/ACS_Order_MAR2026_CS---3474f087-3bc7-4a73-92d1-7d4857b78eb3.xlsx"
echo "   直接連結: http://localhost:$PORT/.openclaw/media/inbound/ACS_Order_MAR2026_CS---3474f087-3bc7-4a73-92d1-7d4857b78eb3.xlsx"
echo
echo "⏹️  按 Ctrl+C 停止服務器"
echo "🚀 服務器啟動中..."

# 使用 Python 啟動 HTTP 服務器
python3 -c "
import http.server
import socketserver
import os

class FileHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='/data/workspace/shared', **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def do_GET(self):
        # 如果係下載 Excel 文件，添加適當嘅 content-type
        if self.path.endswith('.xlsx'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            self.send_header('Content-Disposition', f'attachment; filename=\"{os.path.basename(self.path)}\"')
        else:
            super().do_GET()

with socketserver.TCPServer(('', 8000), FileHandler) as httpd:
    print('HTTP server running on port 8000')
    httpd.serve_forever()
"