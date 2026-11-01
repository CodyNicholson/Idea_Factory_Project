"""Read-only HTTP API and dashboard for Idea Factory (`http://127.0.0.1:8020`).

Generation runs only in the agent. No route here can trigger it, so no web request can spend tokens.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from . import config
from .postgres import PostgresError, get_postgres_status, run_migrations
from .signals import gather_signals
from .storage import load_agent_state, load_ideas
from .workspace_intel import inspect_live_workspace


class IdeaFactoryHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:
        return  # Keep console clean

    def _send_json(self, data: Any, status: int = 200) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        try:
            self._route_get()
        except (OSError, PostgresError) as exc:
            self._send_json({"error": f"PostgreSQL unavailable: {exc}"}, 503)

    def _route_get(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            raw = (config.WEB_DIR / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.end_headers()
            self.wfile.write(raw)
            return

        if path == "/api/health":
            self._send_json({"status": "ok", "service": "idea-factory"})
            return

        if path == "/api/status":
            state = load_agent_state()
            state["postgres"] = get_postgres_status()
            self._send_json(state)
            return

        if path == "/api/db":
            self._send_json(get_postgres_status())
            return

        if path == "/api/workspace":
            self._send_json(
                {
                    "workspace": inspect_live_workspace(),
                    "signals": [s.to_dict() for s in gather_signals(include_live=False)],
                }
            )
            return

        if path == "/api/ideas":
            cat = qs.get("category", ["ALL"])[0]
            q = qs.get("q", [""])[0].lower().strip()
            filtered = [
                i.to_dict()
                for i in load_ideas()
                if (cat == "ALL" or i.category == cat)
                and (not q or q in i.title.lower() or q in i.summary.lower() or q in i.naics_code.lower())
            ]
            self._send_json({"count": len(filtered), "ideas": filtered})
            return

        self._send_json({"error": "Not found"}, 404)


def run_server(host: str = "127.0.0.1", port: int = config.PORT) -> None:
    run_migrations()
    httpd = ThreadingHTTPServer((host, port), IdeaFactoryHandler)
    print(f"Idea Factory Dashboard & API listening on http://{host}:{port}")
    httpd.serve_forever()
