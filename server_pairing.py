from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# In-memory pairing state (per run; not persisted)
pairings = {}


class Handler(BaseHTTPRequestHandler):
    def _respond(self, body, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length:
            return json.loads(self.rfile.read(length))
        return {}

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("/data/workspace/ui/pair_telegram.html", "rb") as f:
                self.wfile.write(f.read())
            return
        if self.path == "/telegram-pairing-status":
            self._respond({"ok": True, "pairings": pairings})
            return
        self._respond({"error": "not found"}, 404)

    def do_POST(self):
        data = self._read_body()

        if self.path == "/setup-telegram-pairing":
            code = data.get("pairingCode")
            tid = data.get("telegramUserId")
            if not code or not tid:
                self._respond({"ok": False, "error": "missing pairingCode or telegramUserId"}, 400)
                return
            pairings[tid] = code
            self._respond({"ok": True, "pairedUser": tid})
            return

        if self.path == "/telegram-ping":
            tid = data.get("telegramUserId")
            self._respond({"ok": True, "paired": tid in pairings})
            return

        self._respond({"error": "route not found"}, 404)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Pairing server running on http://0.0.0.0:8000")
    server.serve_forever()
