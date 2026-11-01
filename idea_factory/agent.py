"""5-Hour Continuous Autonomous Idea Factory Agent Loop."""
from __future__ import annotations

import importlib
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Callable

from . import config
from . import generator as _generator_mod
from .generator import CreditExhaustedError, active_provider, generate_next_idea
from .models import ProductIdea
from .seed_ideas import get_seed_ideas
from .storage import (
    init_db,
    load_ideas,
    save_agent_state,
    save_idea,
    save_ideas_batch,
)

logger = logging.getLogger(__name__)


def ensure_seeded() -> list[ProductIdea]:
    """Ensure the foundational workspace product blueprints are loaded into the catalog."""
    init_db()
    existing = load_ideas()
    seed = get_seed_ideas()
    existing_ids = {i.id for i in existing}
    missing = [s for s in seed if s.id not in existing_ids]
    if missing:
        save_ideas_batch(existing + missing)
        existing = load_ideas()
    return existing


def run_agent_loop(
    *,
    max_hours: float = config.AGENT_MAX_HOURS,
    interval_seconds: float = config.AGENT_LOOP_INTERVAL_SECONDS,
    max_iterations: int | None = None,
    max_credit_usd: float = config.AGENT_MAX_CREDIT_USD,
    auto_resume_on_refresh: bool = False,
    refresh_cooldown_seconds: float | None = None,
    max_refresh_cycles: int | None = None,
    on_idea_added: Callable[[ProductIdea, dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Run the Idea Factory Agent in a continuous loop until the 5-hour window or AI credit limit is reached.

    When `auto_resume_on_refresh=True`, reaching the 5-hour token/credit limit transitions the agent into
    `WAITING_FOR_5HR_TOKEN_REFRESH`, waits until the 5-hour window refreshes, and resumes generating ideas
    right where it left off.
    """
    ideas = ensure_seeded()
    run_id = f"run-{uuid.uuid4().hex[:8]}"
    started_at = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic()
    max_runtime_seconds = int(max_hours * 3600)
    provider = active_provider()

    iterations = 0
    new_ideas_added = 0
    api_calls = 0
    estimated_cost_usd = 0.0
    window_cycle = 1
    status = "RUNNING"
    stop_reason = ""
    last_idea_id = max((i.id for i in ideas), default="")

    def _snapshot(extra: dict[str, Any] | None = None) -> dict[str, Any]:
        elapsed = round(time.monotonic() - t0, 2)
        remaining = max(0.0, round(max_runtime_seconds - elapsed, 1))
        snap = {
            "run_id": run_id,
            "status": status,
            "provider": provider,
            "started_at": started_at,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "window_cycle": window_cycle,
            "auto_resume_on_refresh": auto_resume_on_refresh,
            "elapsed_seconds": elapsed,
            "remaining_seconds": remaining,
            "max_runtime_seconds": max_runtime_seconds,
            "max_hours": max_hours,
            "iterations": iterations,
            "new_ideas_added_this_run": new_ideas_added,
            "ideas_count": len(ideas),
            "api_calls": api_calls,
            "estimated_cost_usd": round(estimated_cost_usd, 4),
            "max_credit_usd": max_credit_usd,
            "last_idea_id": last_idea_id,
            "stop_reason": stop_reason,
        }
        if extra:
            snap.update(extra)
        return snap

    def _wait_for_5hr_refresh(reason: str) -> bool:
        nonlocal t0, estimated_cost_usd, window_cycle, status, stop_reason
        if not auto_resume_on_refresh:
            return False
        if max_refresh_cycles is not None and window_cycle >= max_refresh_cycles:
            return False
        elapsed_in_window = time.monotonic() - t0
        wait_sec = (
            refresh_cooldown_seconds
            if refresh_cooldown_seconds is not None
            else max(60.0, float(max_runtime_seconds) - elapsed_in_window)
        )
        status = "WAITING_FOR_5HR_TOKEN_REFRESH"
        stop_reason = f"{reason} Waiting {wait_sec:.0f}s for 5-hour token window refresh (cycle {window_cycle})..."
        save_agent_state(_snapshot({"refresh_wait_seconds": round(wait_sec, 1)}))
        if wait_sec > 0:
            time.sleep(wait_sec)
        window_cycle += 1
        t0 = time.monotonic()
        estimated_cost_usd = 0.0
        status = "RUNNING"
        stop_reason = ""
        save_agent_state(_snapshot())
        return True

    save_agent_state(_snapshot())

    try:
        while True:
            elapsed = time.monotonic() - t0
            if elapsed >= max_runtime_seconds:
                if _wait_for_5hr_refresh(f"Reached {max_hours:.2f}-hour window limit ({max_runtime_seconds}s)."):
                    continue
                status = "COMPLETED_5HR_WINDOW"
                stop_reason = f"Reached {max_hours:.2f}-hour time limit ({max_runtime_seconds}s)."
                break
            if max_iterations is not None and iterations >= max_iterations:
                status = "COMPLETED_MAX_ITERATIONS"
                stop_reason = f"Completed requested {max_iterations} loop iterations."
                break
            if estimated_cost_usd >= max_credit_usd:
                if _wait_for_5hr_refresh(f"Consumed 5-hour credit budget (${estimated_cost_usd:.2f} / ${max_credit_usd:.2f})."):
                    continue
                status = "CREDIT_LIMIT_REACHED"
                stop_reason = f"Consumed allocated credit budget (${estimated_cost_usd:.2f} / ${max_credit_usd:.2f})."
                break

            try:
                ideas = load_ideas()
                idea, used_provider, call_cost = generate_next_idea(ideas, iteration=iterations)
                provider = used_provider
                api_calls += 1
                estimated_cost_usd += call_cost
                save_idea(idea)
                ideas = load_ideas()
                iterations += 1
                new_ideas_added += 1
                last_idea_id = idea.id
                snap = _snapshot()
                save_agent_state(snap)
                if on_idea_added:
                    on_idea_added(idea, snap)
            except CreditExhaustedError as exc:
                if _wait_for_5hr_refresh(str(exc)):
                    continue
                status = "CREDIT_LIMIT_REACHED"
                stop_reason = str(exc)
                break
            except Exception as exc:
                logger.warning("Iteration error (continuing loop): %s", exc)
                if config.AGENT_STOP_ON_RATE_LIMIT and "429" in str(exc):
                    if _wait_for_5hr_refresh(f"Rate/token limit reached: {exc}"):
                        continue
                    status = "CREDIT_LIMIT_REACHED"
                    stop_reason = f"Rate/credit limit reached: {exc}"
                    break

            # Check if sleeping would exceed the 5-hour window or max_iterations
            if max_iterations is not None and iterations >= max_iterations:
                status = "COMPLETED_MAX_ITERATIONS"
                stop_reason = f"Completed requested {max_iterations} loop iterations."
                break
            if (time.monotonic() - t0) + interval_seconds >= max_runtime_seconds:
                if _wait_for_5hr_refresh(f"Reached {max_hours:.2f}-hour window limit."):
                    continue
                status = "COMPLETED_5HR_WINDOW"
                stop_reason = f"Reached {max_hours:.2f}-hour time limit."
                break
            if interval_seconds > 0:
                time.sleep(interval_seconds)
    except KeyboardInterrupt:
        status = "STOPPED_BY_USER"
        stop_reason = "Interrupted by user (SIGINT)."

    final_state = _snapshot()
    save_agent_state(final_state)
    return final_state

