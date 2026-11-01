"""Continuous idea loop: generate with Gemini 4 Argon at High effort, store in PostgreSQL.

The loop runs until told to stop. When the tokens run out it records the wait in PostgreSQL, sleeps
until they refresh, and resumes. It never falls back to another model or a template engine.
"""
from __future__ import annotations

import logging
import random
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, TypeVar

from . import config
from .gemini import FatalGeminiError, GeminiCall, TokensExhaustedError, TransientGeminiError
from .generator import InvalidIdeaError, generate_next_idea
from .models import ProductIdea
from .postgres import (
    PostgresError,
    acquire_agent_lock,
    count_ideas,
    is_transient_db_error,
    record_gemini_call,
    run_migrations,
    upsert_agent_state_postgres,
    upsert_ideas_postgres,
)

logger = logging.getLogger(__name__)
T = TypeVar("T")

BACKOFF_BASE_SECONDS = 30.0
MAX_WAIT_SECONDS = 3600.0  # Also the polling interval when the reset time is unknown.
RESET_MARGIN_SECONDS = 60.0


class AgentAlreadyRunningError(RuntimeError):
    """Another agent holds the lock. Two agents would spend tokens on duplicate work."""


def backoff_seconds(attempt: int) -> float:
    """Exponential backoff with jitter, capped at one hour."""
    delay = BACKOFF_BASE_SECONDS * (2 ** min(attempt, 10))
    return min(MAX_WAIT_SECONDS, delay * random.uniform(0.9, 1.1))


def refresh_wait_seconds(exc: TokensExhaustedError, attempt: int, now: datetime | None = None) -> float:
    """How long to wait for tokens: the known reset time, the API's hint, or a capped poll."""
    if exc.resume_at is not None:
        remaining = (exc.resume_at - (now or datetime.now(timezone.utc))).total_seconds()
        return max(RESET_MARGIN_SECONDS, remaining + RESET_MARGIN_SECONDS)
    if exc.kind == "billing":
        return MAX_WAIT_SECONDS  # Refreshes on the 1st of the month, or whenever credits are added.
    return max(exc.retry_after or 0.0, min(backoff_seconds(attempt), MAX_WAIT_SECONDS))


def run_agent_loop(
    *,
    interval_seconds: float = config.AGENT_LOOP_INTERVAL_SECONDS,
    max_iterations: int | None = None,
    on_idea_added: Callable[[ProductIdea, dict[str, Any]], None] | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    """Run until interrupted, or until `max_iterations` ideas have been stored."""
    run_id = f"run-{uuid.uuid4().hex[:8]}"
    started_at = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic()
    state: dict[str, Any] = {
        "run_id": run_id,
        "status": "RUNNING",
        "model": config.GEMINI_MODEL,
        "thinking_level": config.GEMINI_THINKING_LEVEL,
        "started_at": started_at,
        "iterations": 0,
        "new_ideas_added_this_run": 0,
        "ideas_rejected_this_run": 0,
        "ideas_count": 0,
        "api_calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "thought_tokens": 0,
        "refresh_waits": 0,
        "resume_at": None,
        "last_idea_id": None,
        "stop_reason": "",
    }

    def save_state() -> dict[str, Any]:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        state["elapsed_seconds"] = round(time.monotonic() - t0, 2)
        try:
            upsert_agent_state_postgres(state)
        except (OSError, PostgresError) as exc:
            logger.warning("Could not save agent state: %s", exc)
        return dict(state)

    def wait(status: str, seconds: float, reason: str) -> None:
        state["status"] = status
        state["stop_reason"] = reason
        state["resume_at"] = datetime.fromtimestamp(time.time() + seconds, timezone.utc).isoformat()
        save_state()
        logger.warning("%s for %.0fs: %s", status, seconds, reason)
        sleep(seconds)
        state["status"] = "RUNNING"
        state["stop_reason"] = ""
        state["resume_at"] = None
        save_state()

    def persist(write: Callable[[], T]) -> T:
        """Retry a database write until it lands. The tokens behind this data are already paid for."""
        attempt = 0
        while True:
            try:
                return write()
            except (OSError, PostgresError) as exc:
                if not is_transient_db_error(exc):
                    raise
                wait("WAITING_FOR_DATABASE", backoff_seconds(attempt), f"PostgreSQL unavailable: {exc}")
                attempt += 1

    def record_usage(call: GeminiCall) -> None:
        state["api_calls"] += 1
        state["input_tokens"] += call.input_tokens
        state["output_tokens"] += call.output_tokens
        state["thought_tokens"] += call.thought_tokens

    def reject(call: GeminiCall, outcome: str, error: str) -> None:
        record_usage(call)
        state["ideas_rejected_this_run"] += 1
        persist(lambda: record_gemini_call(run_id, call, outcome=outcome, error=error))

    lock = None
    exhausted_attempts = 0
    transient_attempts = 0
    rejected_attempts = 0
    try:
        persist(run_migrations)
        lock = persist(acquire_agent_lock)
        if lock is None:
            raise AgentAlreadyRunningError("Another Idea Factory agent is already running against this database.")
        state["ideas_count"] = persist(count_ideas)
        save_state()

        while max_iterations is None or state["iterations"] < max_iterations:
            try:
                idea, call = generate_next_idea(iteration=state["iterations"])
            except TokensExhaustedError as exc:
                state["refresh_waits"] += 1
                wait("WAITING_FOR_TOKEN_REFRESH", refresh_wait_seconds(exc, exhausted_attempts), str(exc))
                exhausted_attempts += 1
                continue
            except InvalidIdeaError as exc:
                reject(exc.call, "invalid_output", str(exc))
                wait("WAITING_AFTER_INVALID_OUTPUT", backoff_seconds(rejected_attempts), str(exc))
                rejected_attempts += 1
                continue
            except TransientGeminiError as exc:
                wait("WAITING_AFTER_TRANSIENT_ERROR", backoff_seconds(transient_attempts), str(exc))
                transient_attempts += 1
                continue
            except (OSError, PostgresError) as exc:
                if not is_transient_db_error(exc):
                    raise
                wait("WAITING_FOR_DATABASE", backoff_seconds(transient_attempts), f"PostgreSQL unavailable: {exc}")
                transient_attempts += 1
                continue

            exhausted_attempts = transient_attempts = 0
            try:
                persist(lambda: upsert_ideas_postgres([idea]))
            except PostgresError as exc:
                # A constraint rejected the data itself, for example a slug that already exists.
                outcome = "duplicate" if exc.sqlstate == "23505" else "invalid_output"
                reject(call, outcome, str(exc))
                wait("WAITING_AFTER_INVALID_OUTPUT", backoff_seconds(rejected_attempts), str(exc))
                rejected_attempts += 1
                continue

            rejected_attempts = 0
            record_usage(call)
            persist(lambda: record_gemini_call(run_id, call, outcome="stored", idea_id=idea.id))
            state["iterations"] += 1
            state["new_ideas_added_this_run"] += 1
            state["last_idea_id"] = idea.id
            state["ideas_count"] = persist(count_ideas)
            snapshot = save_state()
            if on_idea_added:
                on_idea_added(idea, snapshot)
            if interval_seconds > 0 and (max_iterations is None or state["iterations"] < max_iterations):
                sleep(interval_seconds)

        state["status"] = "COMPLETED_MAX_ITERATIONS"
        state["stop_reason"] = f"Stored the requested {max_iterations} ideas."
    except KeyboardInterrupt:
        state["status"] = "STOPPED_BY_USER"
        state["stop_reason"] = "Stopped by signal."
    except AgentAlreadyRunningError:
        raise
    except FatalGeminiError as exc:
        state["status"] = "FAILED"
        state["stop_reason"] = str(exc)
        save_state()
        raise
    finally:
        if lock is not None:
            lock.close()
    return save_state()
