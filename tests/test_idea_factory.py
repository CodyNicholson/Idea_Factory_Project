"""Tests for scoring, validation, the Gemini client, and the agent loop.

Tests marked as integration run against a throwaway database on the local PostgreSQL server and a
fake Gemini HTTP server. They never touch the real `idea_factory` database or call Google.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import unittest
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from unittest.mock import patch

from idea_factory import agent, config, gemini
from idea_factory.agent import AgentAlreadyRunningError, run_agent_loop
from idea_factory.gemini import (
    FatalGeminiError,
    TokensExhaustedError,
    TransientGeminiError,
    classify_http_error,
    next_quota_reset,
)
from idea_factory.generator import IDEA_SCHEMA
from idea_factory.idea_builder import make_idea
from idea_factory.models import validate_idea
from idea_factory.postgres import (
    PostgresError,
    PostgresWireClient,
    acquire_agent_lock,
    is_transient_db_error,
    load_ideas_postgres,
    pg_literal,
    run_migrations,
)
from idea_factory.scoring import risk_adjusted_roi, roi_score, weibull_survival_curve
from idea_factory.signals import CURATED_SIGNALS

TEST_DB = "idea_factory_test"


def idea_fields(slug: str = "dock-audit-ai") -> dict[str, Any]:
    """A complete, valid answer of the kind Gemini is asked to return."""
    answer = "A specific diligence answer with enough quantitative detail to pass the validator's length check."
    fields: dict[str, Any] = {key: answer for key in IDEA_SCHEMA["properties"]}
    fields.update(
        slug=slug,
        title=f"Title for {slug}",
        tagline="A tagline",
        summary="A summary that is comfortably longer than eighty characters so that it passes validation here.",
        category="Vertical AI",
        naics_code="561790",
        business_archetype="VERTICAL_SAAS",
        target_metro="Dallas-Fort Worth-Arlington MSA",
        pattern_ids=["PAT-01"],
        referenced_skills=["visual-lab"],
        referenced_projects=["Business_Analyzer_Project"],
        causal_drivers=["recurring_revenue"],
        mitigated_failure_modes=["key_person_risk"],
        signal_inspiration="",
        s12=0.9,
        s60=0.6,
        initial_capex_usd=25_000,
        steady_state_ebitda_usd=600_000,
        annual_contract_value_usd=30_000,
        cac_usd=3_000,
        gross_margin_pct=80,
        annual_churn_pct=10,
        monthly_burn_usd=10_000,
        runway_months=24,
        founder_fit_score=85,
    )
    return fields


class TestScoringAndValidation(unittest.TestCase):
    def test_weibull_and_israelsen_roi_math(self) -> None:
        curve = weibull_survival_curve(0.90, 0.60)
        self.assertAlmostEqual(curve(12), 0.90, places=3)
        self.assertAlmostEqual(curve(60), 0.60, places=3)
        self.assertGreater(roi_score(risk_adjusted_roi(0.60, 500_000, 50_000, 0.50, 0.30)), 50.0)
        self.assertLess(roi_score(risk_adjusted_roi(0.10, 5_000, 500_000, 0.90, 1.50)), 50.0)

    def test_valid_answer_builds_a_valid_idea(self) -> None:
        idea = make_idea(id="IDEA-001", **idea_fields())
        self.assertEqual(validate_idea(idea), [])
        self.assertIn("### 5. Team & Execution", idea.to_markdown(index=1))

    def test_pg_literal_handles_hostile_values(self) -> None:
        self.assertEqual(pg_literal(["PAT-01", "PAT-02"]), "ARRAY['PAT-01', 'PAT-02']::text[]")
        self.assertEqual(pg_literal("it's"), "'it''s'")
        self.assertEqual(pg_literal("a\x00b"), "'ab'")
        self.assertEqual(pg_literal(float("nan")), "NULL")


class TestModelLock(unittest.TestCase):
    def test_environment_cannot_change_model_or_effort(self) -> None:
        env = {**os.environ, "GEMINI_MODEL": "gemini-2.5-pro", "GEMINI_THINKING_LEVEL": "low"}
        out = subprocess.run(
            [sys.executable, "-c", "from idea_factory import config as c; print(c.GEMINI_MODEL, c.GEMINI_THINKING_LEVEL)"],
            env=env, capture_output=True, text=True, check=True, cwd=config.ROOT_DIR,
        )
        self.assertEqual(out.stdout.strip(), "gemini-4-argon high")

    def test_no_other_provider_in_the_code(self) -> None:
        banned = ("api.anthropic.com", "api.openai.com", "openrouter.ai", '"claude"', "ANTHROPIC_API_KEY", "OPENAI_API_KEY")
        for path in (config.ROOT_DIR / "idea_factory").glob("*.py"):
            source = path.read_text(encoding="utf-8")
            for term in banned:
                self.assertNotIn(term, source, f"{term} found in {path.name}")


class TestErrorClassification(unittest.TestCase):
    NOW = datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc)

    def test_daily_quota_waits_until_midnight_pacific(self) -> None:
        exc = classify_http_error(429, json.dumps({"error": {"code": "quota_exceeded", "message": "Daily quota"}}), now=self.NOW)
        self.assertIsInstance(exc, TokensExhaustedError)
        self.assertEqual(exc.kind, "daily_quota")
        self.assertEqual(exc.resume_at, datetime(2026, 11, 3, 8, 0, tzinfo=timezone.utc))  # PST is UTC-8

    def test_midnight_pacific_follows_daylight_saving(self) -> None:
        self.assertEqual(
            next_quota_reset(datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)),
            datetime(2026, 7, 2, 7, 0, tzinfo=timezone.utc),  # PDT is UTC-7
        )

    def test_rate_limit_uses_server_hint(self) -> None:
        body = json.dumps({"error": {"code": 429, "status": "RESOURCE_EXHAUSTED", "details": [{"retryDelay": "34s"}]}})
        exc = classify_http_error(429, body)
        self.assertEqual((exc.kind, exc.retry_after), ("rate_limit", 34.0))
        self.assertEqual(classify_http_error(429, "{}", {"Retry-After": "12"}).retry_after, 12.0)

    def test_billing_exhaustion_is_a_wait_not_a_failure(self) -> None:
        for status, message in ((402, "Payment required"), (400, "Prepay credits depleted"), (429, "Spend cap reached")):
            exc = classify_http_error(status, json.dumps({"error": {"message": message}}))
            self.assertIsInstance(exc, TokensExhaustedError, message)
            self.assertEqual(exc.kind, "billing")

    def test_server_errors_are_transient_and_bad_requests_are_fatal(self) -> None:
        for status in (408, 500, 503, 504):
            self.assertIsInstance(classify_http_error(status, "{}"), TransientGeminiError)
        for status in (400, 401, 403, 404):
            self.assertIsInstance(classify_http_error(status, '{"error":{"message":"bad"}}'), FatalGeminiError)

    def test_real_google_error_shape_is_understood(self) -> None:
        # Shape captured from the real endpoint: a one-item array holding the error object.
        body = json.dumps([{"error": {"code": 400, "message": "API key not valid. Please pass a valid API key.",
                                      "status": "INVALID_ARGUMENT", "details": [{"reason": "API_KEY_INVALID"}]}}])
        exc = classify_http_error(400, body)
        self.assertIsInstance(exc, FatalGeminiError)
        self.assertEqual(str(exc), "HTTP 400: API key not valid. Please pass a valid API key.")

    def test_per_minute_limit_mentioning_billing_is_a_short_wait(self) -> None:
        body = json.dumps([{"error": {
            "code": 429, "status": "RESOURCE_EXHAUSTED",
            "message": "You exceeded your current quota, please check your plan and billing details.",
            "details": [{"violations": [{"quotaId": "InputTokensPerModelPerMinute"}]}, {"retryDelay": "21s"}],
        }}])
        exc = classify_http_error(429, body)
        self.assertEqual((exc.kind, exc.retry_after), ("rate_limit", 21.0))

    def test_per_day_quota_id_waits_for_the_reset_even_with_a_retry_hint(self) -> None:
        body = json.dumps([{"error": {
            "code": 429, "message": "You exceeded your current quota, please check your plan and billing details.",
            "details": [{"violations": [{"quotaId": "GenerateRequestsPerDayPerProjectPerModel"}]}, {"retryDelay": "21s"}],
        }}])
        self.assertEqual(classify_http_error(429, body, now=self.NOW).kind, "daily_quota")

    def test_zero_quota_means_wrong_tier_and_never_waits_forever(self) -> None:
        body = json.dumps({"error": {"code": 429, "message": "Quota exceeded for metric: free_tier_requests, limit: 0"}})
        exc = classify_http_error(429, body)
        self.assertIsInstance(exc, FatalGeminiError)
        self.assertIn("paid-tier", str(exc))

    def test_wait_time_uses_reset_time_then_hint_and_is_capped(self) -> None:
        daily = TokensExhaustedError("x", kind="daily_quota", resume_at=self.NOW + timedelta(hours=3))
        self.assertEqual(agent.refresh_wait_seconds(daily, 0, now=self.NOW), 3 * 3600 + agent.RESET_MARGIN_SECONDS)
        self.assertEqual(agent.refresh_wait_seconds(TokensExhaustedError("x", kind="billing"), 0), agent.MAX_WAIT_SECONDS)
        hinted = TokensExhaustedError("x", kind="rate_limit", retry_after=500.0)
        self.assertGreaterEqual(agent.refresh_wait_seconds(hinted, 0), 500.0)
        self.assertLessEqual(agent.refresh_wait_seconds(TokensExhaustedError("x", kind="rate_limit"), 50), agent.MAX_WAIT_SECONDS)

    def test_database_errors_are_sorted(self) -> None:
        self.assertTrue(is_transient_db_error(ConnectionRefusedError()))
        self.assertTrue(is_transient_db_error(PostgresError("starting up", sqlstate="57P03")))
        self.assertFalse(is_transient_db_error(PostgresError("duplicate", sqlstate="23505")))


class FakeGemini(BaseHTTPRequestHandler):
    """Replays queued (status, body, headers) responses and records every request."""

    responses: list[tuple[int, dict[str, Any], dict[str, str]]] = []
    requests: list[dict[str, Any]] = []

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def do_POST(self) -> None:
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        FakeGemini.requests.append({"path": self.path, "headers": {k.lower(): v for k, v in self.headers.items()}, "body": body})
        status, payload, headers = FakeGemini.responses.pop(0)
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def completed(fields: dict[str, Any], model: str = "gemini-4-argon") -> tuple[int, dict[str, Any], dict[str, str]]:
    return 200, {
        "id": "interaction-1",
        "status": "completed",
        "model": model,
        "steps": [
            {"type": "thought", "content": [{"type": "text", "text": "thinking, must be ignored"}]},
            {"type": "model_output", "content": [{"type": "text", "text": json.dumps(fields)}]},
        ],
        "usage": {"total_input_tokens": 100, "total_output_tokens": 200, "total_thought_tokens": 300, "total_tokens": 600},
    }, {}


class TestAgentLoopIntegration(unittest.TestCase):
    """Runs the real loop, real HTTP client and real PostgreSQL. Only Google is replaced."""

    @classmethod
    def setUpClass(cls) -> None:
        try:
            with PostgresWireClient(database="postgres", timeout=2.0) as admin:
                admin.execute(f"DROP DATABASE IF EXISTS {TEST_DB} WITH (FORCE);")
                admin.execute(f"CREATE DATABASE {TEST_DB};")
        except (OSError, PostgresError) as exc:
            raise unittest.SkipTest(f"PostgreSQL unavailable, start it with ./run_agent.sh --db-only: {exc}")
        cls.db_patch = patch.object(config, "POSTGRES_DB", TEST_DB)
        cls.db_patch.start()
        cls.server = HTTPServer(("127.0.0.1", 0), FakeGemini)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.patches = [
            patch.object(gemini, "API_URL", f"http://127.0.0.1:{cls.server.server_port}/v1beta/interactions"),
            patch.object(config, "GEMINI_API_KEY", "test-key"),
            patch("idea_factory.generator.gather_signals", return_value=CURATED_SIGNALS),
        ]
        for item in cls.patches:
            item.start()
        run_migrations()

    @classmethod
    def tearDownClass(cls) -> None:
        for item in cls.patches:
            item.stop()
        cls.db_patch.stop()
        cls.server.shutdown()
        with PostgresWireClient(database="postgres") as admin:
            admin.execute(f"DROP DATABASE IF EXISTS {TEST_DB} WITH (FORCE);")

    def setUp(self) -> None:
        FakeGemini.responses = []
        FakeGemini.requests = []
        self.sleeps: list[float] = []
        self.statuses_during_sleep: list[tuple[str, str | None]] = []
        self.sql("TRUNCATE product_ideas, agent_runs, gemini_calls CASCADE;")

    def sql(self, query: str) -> list[dict[str, Any]]:
        with PostgresWireClient() as client:
            return client.execute(query)

    def fake_sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        rows = self.sql("SELECT status, resume_at::text AS resume_at FROM agent_runs ORDER BY updated_at DESC LIMIT 1;")
        self.statuses_during_sleep.append((rows[0]["status"], rows[0]["resume_at"]))

    def run_loop(self, iterations: int = 1) -> dict[str, Any]:
        return run_agent_loop(interval_seconds=0, max_iterations=iterations, sleep=self.fake_sleep)

    def test_stores_idea_with_only_argon_high_and_key_in_header(self) -> None:
        FakeGemini.responses = [completed(idea_fields())]
        final = self.run_loop()

        request = FakeGemini.requests[0]
        self.assertEqual(request["path"], "/v1beta/interactions")
        self.assertEqual(request["body"]["model"], "gemini-4-argon")
        self.assertEqual(request["body"]["generation_config"]["thinking_level"], "high")
        self.assertEqual(request["headers"]["x-goog-api-key"], "test-key")

        ideas = load_ideas_postgres()
        self.assertEqual([i.generation_source for i in ideas], ["GEMINI_4_ARGON_HIGH"])
        self.assertEqual(ideas[0].id, "IDEA-001")
        self.assertEqual(self.sql("SELECT COUNT(*) AS n FROM idea_diligence_questions;")[0]["n"], "14")
        call = self.sql("SELECT * FROM gemini_calls;")[0]
        self.assertEqual((call["model"], call["thinking_level"], call["outcome"], call["idea_id"]), ("gemini-4-argon", "high", "stored", "IDEA-001"))
        self.assertEqual(call["total_tokens"], "600")
        self.assertEqual(final["status"], "COMPLETED_MAX_ITERATIONS")
        self.assertEqual((final["input_tokens"], final["output_tokens"], final["thought_tokens"]), (100, 200, 300))

    def test_waits_for_token_refresh_then_resumes(self) -> None:
        FakeGemini.responses = [
            (429, {"error": {"code": "quota_exceeded", "message": "Daily quota exceeded"}}, {}),
            (402, {"error": {"code": "payment_required", "message": "Credits depleted"}}, {}),
            (429, {"error": {"code": "rate_limit_exceeded", "message": "slow down"}}, {"Retry-After": "7"}),
            completed(idea_fields()),
        ]
        final = self.run_loop()

        self.assertEqual([status for status, _ in self.statuses_during_sleep], ["WAITING_FOR_TOKEN_REFRESH"] * 3)
        self.assertTrue(all(resume_at for _, resume_at in self.statuses_during_sleep), "resume_at must be stored")
        self.assertGreater(self.sleeps[0], agent.RESET_MARGIN_SECONDS)  # until midnight Pacific
        self.assertEqual(self.sleeps[1], agent.MAX_WAIT_SECONDS)  # billing polls hourly
        self.assertGreaterEqual(self.sleeps[2], 7)
        self.assertEqual(final["refresh_waits"], 3)
        self.assertEqual(final["new_ideas_added_this_run"], 1)
        self.assertIsNone(final["resume_at"])
        self.assertEqual(self.sql("SELECT COUNT(*) AS n FROM gemini_calls;")[0]["n"], "1", "failed calls were not billed")

    def test_exhaustion_never_falls_back_to_another_model(self) -> None:
        FakeGemini.responses = [(429, {"error": {"message": "slow"}}, {}), completed(idea_fields())]
        self.run_loop()
        self.assertEqual({r["body"]["model"] for r in FakeGemini.requests}, {"gemini-4-argon"})

    def test_invalid_answers_are_kept_but_not_stored_as_ideas(self) -> None:
        missing_field = idea_fields("incomplete")
        del missing_field["summary"]
        impossible = idea_fields("impossible")
        impossible["steady_state_ebitda_usd"] = 50_000_000
        impossible["initial_capex_usd"] = 1_000
        impossible["cac_usd"] = 50
        impossible["summary"] = "too short"
        FakeGemini.responses = [
            (200, {"id": "x", "status": "completed", "model": "gemini-4-argon", "steps": [{"type": "model_output", "content": [{"type": "text", "text": "not json"}]}], "usage": {}}, {}),
            (200, {"id": "y", "status": "incomplete", "model": "gemini-4-argon", "steps": [], "usage": {}}, {}),
            completed(missing_field),
            completed(impossible),
            completed(idea_fields()),
        ]
        final = self.run_loop()
        self.assertEqual(final["ideas_rejected_this_run"], 4)
        self.assertEqual([i.slug for i in load_ideas_postgres()], ["dock-audit-ai"])
        rows = self.sql("SELECT outcome, raw_text FROM gemini_calls ORDER BY id;")
        self.assertEqual([r["outcome"] for r in rows], ["invalid_output"] * 4 + ["stored"])
        self.assertEqual(rows[0]["raw_text"], "not json")
        self.assertIn("incomplete", rows[1]["raw_text"], "a call with no answer must keep its raw body")

    def test_duplicate_slug_is_recorded_and_the_loop_continues(self) -> None:
        FakeGemini.responses = [completed(idea_fields("same")), completed(idea_fields("same")), completed(idea_fields("other"))]
        final = self.run_loop(iterations=2)
        self.assertEqual(sorted(i.slug for i in load_ideas_postgres()), ["other", "same"])
        self.assertEqual([r["outcome"] for r in self.sql("SELECT outcome FROM gemini_calls ORDER BY id;")], ["stored", "duplicate", "stored"])
        self.assertEqual(final["ideas_count"], 2)

    def test_transient_errors_retry(self) -> None:
        FakeGemini.responses = [(503, {"error": {"code": "service_unavailable"}}, {}), completed(idea_fields())]
        self.assertEqual(self.run_loop()["new_ideas_added_this_run"], 1)
        self.assertEqual(self.statuses_during_sleep[0][0], "WAITING_AFTER_TRANSIENT_ERROR")

    def test_paid_idea_survives_a_database_outage(self) -> None:
        FakeGemini.responses = [completed(idea_fields())]
        real_upsert = agent.upsert_ideas_postgres
        outcomes = [ConnectionRefusedError("down"), PostgresError("terminating", sqlstate="57P01")]

        def flaky(ideas: list[Any]) -> int:
            if outcomes:
                raise outcomes.pop(0)
            return real_upsert(ideas)

        with patch.object(agent, "upsert_ideas_postgres", side_effect=flaky):
            self.run_loop()
        self.assertEqual(len(FakeGemini.requests), 1, "must not pay for the idea twice")
        self.assertEqual(len(load_ideas_postgres()), 1)
        self.assertEqual(self.statuses_during_sleep[0][0], "WAITING_FOR_DATABASE")

    def test_bad_key_stops_with_a_clear_failure(self) -> None:
        FakeGemini.responses = [(401, {"error": {"code": "authentication", "message": "API key invalid"}}, {})]
        with self.assertRaises(FatalGeminiError):
            self.run_loop()
        row = self.sql("SELECT status, stop_reason FROM agent_runs;")[0]
        self.assertEqual(row["status"], "FAILED")
        self.assertIn("API key invalid", row["stop_reason"])

    def test_substituted_model_is_refused_and_not_stored(self) -> None:
        FakeGemini.responses = [completed(idea_fields(), model="gemini-2.5-flash")]
        with self.assertRaises(FatalGeminiError):
            self.run_loop()
        self.assertEqual(load_ideas_postgres(), [])

    def test_missing_key_is_fatal_without_any_request(self) -> None:
        with patch.object(config, "GEMINI_API_KEY", ""), self.assertRaises(FatalGeminiError):
            self.run_loop()
        self.assertEqual(FakeGemini.requests, [])

    def test_only_one_agent_can_run(self) -> None:
        lock = acquire_agent_lock()
        self.assertIsNotNone(lock)
        try:
            with self.assertRaises(AgentAlreadyRunningError):
                self.run_loop()
            self.assertEqual(FakeGemini.requests, [])
        finally:
            lock.close()

    def test_stop_signal_ends_cleanly(self) -> None:
        def interrupted_sleep(_seconds: float) -> None:
            raise KeyboardInterrupt

        FakeGemini.responses = [(429, {"error": {"message": "slow"}}, {})]
        final = run_agent_loop(interval_seconds=0, sleep=interrupted_sleep)
        self.assertEqual(final["status"], "STOPPED_BY_USER")
        self.assertEqual(self.sql("SELECT status FROM agent_runs;")[0]["status"], "STOPPED_BY_USER")

    def test_database_refuses_any_other_model(self) -> None:
        with self.assertRaises(PostgresError) as caught:
            self.sql("INSERT INTO gemini_calls (run_id, model, thinking_level, outcome) VALUES ('r', 'claude-opus', 'high', 'stored');")
        self.assertEqual(caught.exception.sqlstate, "23514")
        with self.assertRaises(PostgresError):
            self.sql("INSERT INTO gemini_calls (run_id, model, thinking_level, outcome) VALUES ('r', 'gemini-4-argon', 'low', 'stored');")


if __name__ == "__main__":
    unittest.main()
