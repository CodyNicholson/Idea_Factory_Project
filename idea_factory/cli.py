"""Command-line interface for the Idea Factory agent."""
from __future__ import annotations

import argparse
import json
import logging
import signal
import sys
from types import FrameType

from . import config
from .agent import AgentAlreadyRunningError, run_agent_loop
from .gemini import FatalGeminiError
from .models import validate_idea
from .postgres import get_postgres_status, run_migrations
from .server import run_server
from .storage import load_agent_state, load_ideas, render_catalog_markdown, rescore_all_ideas


def _stop_on_sigterm(_signum: int, _frame: FrameType | None) -> None:
    """Let `docker stop` end the loop cleanly, so the final state reaches PostgreSQL."""
    raise KeyboardInterrupt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="idea_factory",
        description="Generates product ideas with Gemini 4 Argon at High effort and stores them in PostgreSQL.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Generate ideas continuously, waiting whenever the tokens run out")
    p_run.add_argument("--interval", type=float, default=config.AGENT_LOOP_INTERVAL_SECONDS, help="Seconds between ideas")
    p_run.add_argument("--max-iterations", type=int, default=None, help="Stop after storing this many ideas")

    sub.add_parser("status", help="Show the telemetry of the latest agent run")
    sub.add_parser("verify", help="Validate all stored ideas against the 14-question schema")
    sub.add_parser("rescore", help="Recalibrate all stored ideas to scoring v2")
    sub.add_parser("migrate", help="Apply pending SQL migrations")
    sub.add_parser("db-status", help="Show PostgreSQL connection, migrations, row counts and portfolio metrics")
    sub.add_parser("catalog", help="Export all stored ideas to IDEAS_CATALOG.md")

    p_serve = sub.add_parser("serve", help="Start the read-only dashboard and API")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=config.PORT)

    args = parser.parse_args(argv)

    if args.cmd == "run":
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
        signal.signal(signal.SIGTERM, _stop_on_sigterm)

        def log_progress(idea, snapshot) -> None:
            print(f"Stored {idea.id}: {idea.title} (ROI={idea.roi_score}, Total={snapshot['ideas_count']})", flush=True)

        try:
            final = run_agent_loop(
                interval_seconds=args.interval,
                max_iterations=args.max_iterations,
                on_idea_added=log_progress,
            )
        except (FatalGeminiError, AgentAlreadyRunningError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr, flush=True)
            return 1
        print(json.dumps(final, indent=2))
        return 0

    if args.cmd == "status":
        print(json.dumps(load_agent_state(), indent=2))
        return 0

    if args.cmd == "verify":
        ideas = load_ideas()
        all_errors = [err for idea in ideas for err in validate_idea(idea)]
        for err in all_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        if all_errors:
            print(f"RESULT: FAIL ({len(all_errors)} errors across {len(ideas)} ideas)")
            return 1
        print(f"RESULT: PASS ({len(ideas)} product ideas verified)")
        return 0

    if args.cmd == "serve":
        run_server(host=args.host, port=args.port)
        return 0

    if args.cmd == "rescore":
        print(f"Rescored {len(rescore_all_ideas())} product ideas to scoring v2.")
        return 0

    if args.cmd == "migrate":
        print(json.dumps({"applied": run_migrations()}, indent=2))
        return 0

    if args.cmd == "db-status":
        print(json.dumps(get_postgres_status(), indent=2))
        return 0

    if args.cmd == "catalog":
        ideas = load_ideas()
        render_catalog_markdown(ideas)
        print(f"Wrote {len(ideas)} ideas to {config.CATALOG_MD_PATH}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
