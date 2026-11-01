"""Command-line interface for the Idea Factory 5-Hour Autonomous Agent."""
from __future__ import annotations

import argparse
import json
import sys

from . import config
from .agent import ensure_seeded, run_agent_loop
from .generator import generate_next_idea
from .models import validate_idea
from .postgres import get_postgres_status
from .server import run_server
from .storage import load_agent_state, load_ideas, rescore_all_ideas, save_idea, sync_all_to_postgres


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="idea_factory",
        description="Autonomous 5-Hour Startup & Product Idea Factory grounded in Claude_Skills_Project and Business_Analyzer_Project.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("seed", help="Seed and render all foundational product blueprints into data/ideas.json and IDEAS_CATALOG.md")

    p_run = sub.add_parser("run", help="Run the continuous autonomous agent loop until the 5-hour limit or AI credits are consumed")
    p_run.add_argument("--hours", type=float, default=config.AGENT_MAX_HOURS, help="Max runtime window in hours (default: 5.0)")
    p_run.add_argument("--interval", type=float, default=config.AGENT_LOOP_INTERVAL_SECONDS, help="Seconds between iterations")
    p_run.add_argument("--max-iterations", type=int, default=None, help="Optional cap on iterations for testing")
    p_run.add_argument("--max-credit", type=float, default=config.AGENT_MAX_CREDIT_USD, help="Max credit budget in USD")
    p_run.add_argument(
        "--auto-resume",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Wait for the 5-hour token limit window to refresh and continue generating where left off (default: True for continuous runs)",
    )

    sub.add_parser("generate-one", help="Synthesize and append one new product idea immediately")
    sub.add_parser("status", help="Show current catalog stats and 5-hour loop telemetry")
    sub.add_parser("verify", help="Deterministically validate all persisted product ideas against the 14-question schema")
    sub.add_parser("rescore", help="Recalibrate all catalog ideas to benchmark-calibrated scoring v2 (finite LTV, funded CAC)")
    sub.add_parser("migrate", help="Apply SQL schema migrations (`migrations/*.sql`) and sync all ideas & metrics to Docker PostgreSQL")
    sub.add_parser("db-status", help="Show live Docker PostgreSQL connection, migration, table row counts, and portfolio metrics")

    p_serve = sub.add_parser("serve", help="Start the live web dashboard & API server (default port 8020)")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=config.PORT)

    args = parser.parse_args(argv)

    if args.cmd == "seed":
        ideas = ensure_seeded()
        print(f"Seeded {len(ideas)} product ideas -> {config.CATALOG_MD_PATH} & {config.IDEAS_JSON_PATH}")
        return 0

    if args.cmd == "generate-one":
        ideas = ensure_seeded()
        idea, provider, cost = generate_next_idea(ideas, iteration=len(ideas))
        save_idea(idea)
        print(f"Added {idea.id}: {idea.title} (ROI Score: {idea.roi_score}/100, Provider: {provider}, Cost: ${cost:.4f})")
        return 0

    if args.cmd == "run":
        def _log_progress(idea, snap):
            print(
                f"[{snap['elapsed_seconds']:.1f}s / {snap['max_runtime_seconds']}s] "
                f"Added {idea.id}: {idea.title} (ROI={idea.roi_score}, Total={snap['ideas_count']})"
            )

        auto_resume = args.auto_resume if args.auto_resume is not None else (args.max_iterations is None)
        final = run_agent_loop(
            max_hours=args.hours,
            interval_seconds=args.interval,
            max_iterations=args.max_iterations,
            max_credit_usd=args.max_credit,
            auto_resume_on_refresh=auto_resume,
            on_idea_added=_log_progress,
        )
        print(json.dumps(final, indent=2))
        return 0

    if args.cmd == "status":
        ideas = ensure_seeded()
        state = load_agent_state()
        state["ideas_count"] = len(ideas)
        print(json.dumps(state, indent=2))
        return 0

    if args.cmd == "verify":
        ideas = ensure_seeded()
        all_errors: list[str] = []
        for idea in ideas:
            all_errors.extend(validate_idea(idea))
        if all_errors:
            for err in all_errors:
                print(f"ERROR: {err}", file=sys.stderr)
            print(f"RESULT: FAIL ({len(all_errors)} errors across {len(ideas)} ideas)")
            return 1
        print(f"RESULT: PASS ({len(ideas)} product ideas verified; all 14 diligence questions and actuarial checks passed)")
        return 0

    if args.cmd == "serve":
        run_server(host=args.host, port=args.port)
        return 0

    if args.cmd == "rescore":
        rescored = rescore_all_ideas()
        print(f"Rescored {len(rescored)} product ideas to scoring v2 (benchmark-calibrated).")
        return 0

    if args.cmd == "migrate":
        ensure_seeded()
        result = sync_all_to_postgres()
        print(json.dumps(result, indent=2))
        return 0

    if args.cmd == "db-status":
        status = get_postgres_status()
        print(json.dumps(status, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

