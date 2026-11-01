"""Zero-dependency HTTP API & Live Dashboard Server for Idea Factory (`http://127.0.0.1:8020`)."""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from . import config
from .agent import ensure_seeded, run_agent_loop
from .generator import generate_next_idea
from .postgres import get_postgres_status
from .signals import gather_signals
from .storage import load_agent_state, load_ideas, save_idea, sync_all_to_postgres
from .workspace_intel import inspect_live_workspace

_bg_thread: threading.Thread | None = None
_bg_lock = threading.Lock()


class IdeaFactoryHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:
        return  # Keep console clean

    def _send_json(self, data: Any, status: int = 200) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            html_file = config.WEB_DIR / "index.html"
            if html_file.exists():
                raw = html_file.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(raw)))
                self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
                self.end_headers()
                self.wfile.write(raw)
                return
            self._send_json({"error": "Dashboard HTML not found"}, 404)
            return

        if path == "/ideas_data.js":
            js_file = config.WEB_DIR / "ideas_data.js"
            if js_file.exists():
                raw = js_file.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "application/javascript; charset=utf-8")
                self.send_header("Content-Length", str(len(raw)))
                self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(raw)
                return

        if path == "/api/health":
            self._send_json({"status": "ok", "service": "idea-factory"})
            return

        if path == "/api/status":
            ideas = load_ideas()
            state = load_agent_state()
            state["ideas_count"] = len(ideas)
            try:
                state["postgres"] = get_postgres_status()
            except Exception as exc:
                state["postgres"] = {"connected": False, "error": str(exc)}
            self._send_json(state)
            return

        if path == "/api/db":
            try:
                self._send_json(get_postgres_status())
            except Exception as exc:
                self._send_json({"connected": False, "error": str(exc)}, 503)
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
            ideas = load_ideas() or ensure_seeded()
            cat = qs.get("category", ["ALL"])[0]
            q = qs.get("q", [""])[0].lower().strip()
            filtered = [
                i.to_dict()
                for i in ideas
                if (cat == "ALL" or i.category == cat)
                and (not q or q in i.title.lower() or q in i.summary.lower() or q in i.naics_code.lower())
            ]
            self._send_json({"count": len(filtered), "ideas": filtered})
            return

        self._send_json({"error": "Not found"}, 404)

    def do_POST(self) -> None:
        global _bg_thread
        parsed = urlparse(self.path)
        if parsed.path == "/api/generate-one":
            ideas = ensure_seeded()
            idea, provider, cost = generate_next_idea(ideas, iteration=len(ideas))
            save_idea(idea)
            self._send_json(
                {"status": "generated", "provider": provider, "cost_usd": cost, "idea": idea.to_dict()},
                201,
            )
            return

        if parsed.path == "/api/start-loop":
            with _bg_lock:
                if _bg_thread and _bg_thread.is_alive():
                    self._send_json({"status": "already_running", "state": load_agent_state()})
                    return
                _bg_thread = threading.Thread(
                    target=run_agent_loop,
                    kwargs={"max_hours": config.AGENT_MAX_HOURS, "interval_seconds": config.AGENT_LOOP_INTERVAL_SECONDS},
                    daemon=True,
                )
                _bg_thread.start()
            self._send_json({"status": "started", "max_hours": config.AGENT_MAX_HOURS})
            return

        self._send_json({"error": "Not found"}, 404)


def run_server(host: str = "127.0.0.1", port: int = config.PORT) -> None:
    ensure_seeded()
    httpd = ThreadingHTTPServer((host, port), IdeaFactoryHandler)
    print(f"Idea Factory Dashboard & API listening on http://{host}:{port}")
    httpd.serve_forever()

