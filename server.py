from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from knowledge_api import create_knowledge_item, get_status, init_db, list_knowledge, search_knowledge

ROOT = Path(__file__).resolve().parent


def load_env_file(env_path: Path | None = None) -> None:
    path = env_path or ROOT / "database.env"
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


load_env_file(ROOT / "database.env")
HOST = os.getenv("PETPAL_HOST", "0.0.0.0")
PORT = int(os.getenv("PETPAL_PORT", "8080"))
DB_PATH = os.getenv("PETPAL_DB_PATH", str(ROOT / "petpal.db"))
API_KEY = os.getenv("PETPAL_API_KEY")

init_db(DB_PATH)


def check_api_key(expected_key: str | None, provided_key: str | None) -> bool:
    if not expected_key:
        return True
    return bool(provided_key and provided_key == expected_key)


class PetpalHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path

        if self._requires_auth(path) and not self._authorized():
            self._send_json(401, {"error": "Unauthorized"})
            return
        query = parse_qs(parsed.query)

        if path == "/api/health":
            self._send_json(200, get_status(DB_PATH))
            return

        if path == "/api/knowledge":
            search = (query.get("query", [""])[0] or "").strip()
            limit = int(query.get("limit", [10])[0])
            items = search_knowledge(search, limit=limit, db_path=DB_PATH) if search else list_knowledge(limit=limit, db_path=DB_PATH)
            self._send_json(200, {"items": items, "count": len(items)})
            return

        self._serve_static(path)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if self._requires_auth(parsed.path) and not self._authorized():
            self._send_json(401, {"error": "Unauthorized"})
            return
        if parsed.path != "/api/knowledge":
            self._send_json(404, {"error": "Not found"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        title = payload.get("title", "").strip()
        content = payload.get("content", "").strip()
        if not title or not content:
            self._send_json(400, {"error": "title and content are required"})
            return

        created = create_knowledge_item(
            title=title,
            content=content,
            tags=payload.get("tags"),
            source=payload.get("source"),
            db_path=DB_PATH,
        )
        self._send_json(201, {"success": True, "item": created})

    def _requires_auth(self, path: str) -> bool:
        return path.startswith("/api/")

    def _authorized(self) -> bool:
        return check_api_key(API_KEY, self.headers.get("X-API-Key"))

    def _serve_static(self, path: str) -> None:
        if path in {"/", "/index.html"}:
            target = ROOT / "index.html"
            if target.exists():
                content = target.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
        self._send_json(404, {"error": "Not found"})

    def _send_json(self, status: int, payload: object) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        return


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), PetpalHandler)
    print(f"Petpal knowledge API running on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
