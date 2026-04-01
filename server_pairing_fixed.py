import http.server, socketserver, json

pairings = {}

class Handler(http.server.BaseHTTPRequestHandler):
    def _respond(self, body, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(content_len))

        if self.path == '/setup-telegram-pairing':
            code = data.get('pairingCode')
            tid = data.get('telegramUserId')
            if not code or not tid:
                self._respond({'ok': False, 'error': 'missing fields'}, 400)
                return
            pairings[tid] = code
            self._respond({'ok': True, 'pairedUser': tid})
            return

        if self.path == '/telegram-ping':
            tid = data.get('telegramUserId')
            self._respond({'ok': True, 'paired': tid in pairings})
            return

        self._respond({'error': 'not found'}, 404)

httpd = socketserver.TCPServer(('127.0.0.1', 8002), Handler)
print('Pairing server on port 8002')
httpd.serve_forever()