"""Unit and integration tests for Idea Factory scoring, 14-question validation, and 5-hour agent loop."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from idea_factory import config
from idea_factory.agent import run_agent_loop
from idea_factory.generator import CreditExhaustedError, generate_next_idea
from idea_factory.models import validate_idea
from idea_factory.postgres import _idea_to_upsert_sql, pg_literal
from idea_factory.scoring import (
    compute_idea_metrics,
    projected_3yr_irr_pct,
    risk_adjusted_roi,
    roi_score,
    weibull_survival_curve,
)
from idea_factory.seed_ideas import get_seed_ideas
from idea_factory.storage import load_ideas, save_idea


class TestIdeaFactory(unittest.TestCase):
    def test_weibull_and_israelsen_roi_math(self) -> None:
        curve = weibull_survival_curve(0.90, 0.60)
        self.assertAlmostEqual(curve(12), 0.90, places=3)
        self.assertAlmostEqual(curve(60), 0.60, places=3)
        self.assertGreater(curve(12), curve(36))
        self.assertGreater(curve(36), curve(60))

        # Positive numerator divides by sigma; negative numerator multiplies by sigma (Israelsen correction)
        pos_raw = risk_adjusted_roi(0.60, 500_000, 50_000, 0.50, 0.30)
        neg_raw = risk_adjusted_roi(0.10, 5_000, 500_000, 0.90, 1.50)
        self.assertGreater(pos_raw, 0)
        self.assertLess(neg_raw, 0)
        self.assertGreater(roi_score(pos_raw), 50.0)
        self.assertLess(roi_score(neg_raw), 50.0)

        irr_val = projected_3yr_irr_pct(35_000, 500_000, curve, 0.50, "VERTICAL_SAAS")
        self.assertGreater(irr_val, 50.0)

    def test_all_seed_ideas_pass_14_question_validator(self) -> None:
        seed_ideas = get_seed_ideas()
        self.assertGreaterEqual(len(seed_ideas), 20)
        seen_ids = set()
        seen_slugs = set()
        for idea in seed_ideas:
            errors = validate_idea(idea)
            self.assertEqual(errors, [], f"Validation failed for {idea.id}: {errors}")
            self.assertNotIn(idea.id, seen_ids)
            self.assertNotIn(idea.slug, seen_slugs)
            seen_ids.add(idea.id)
            seen_slugs.add(idea.slug)
            md = idea.to_markdown(index=1)
            self.assertIn("### 1. Product & Problem-Solving", md)
            self.assertIn("### 2. Market & Competition", md)
            self.assertIn("### 3. Business Model & Traction", md)
            self.assertIn("### 4. Financials & Runway", md)
            self.assertIn("### 5. Team & Execution", md)

    def test_combinatorial_generator_produces_valid_unique_ideas(self) -> None:
        ideas = list(get_seed_ideas())
        for step in range(5):
            new_idea, provider, cost = generate_next_idea(ideas, iteration=step)
            self.assertEqual(validate_idea(new_idea), [])
            self.assertNotIn(new_idea.id, {i.id for i in ideas})
            ideas.append(new_idea)

    def test_agent_loop_stops_on_credit_exhaustion(self) -> None:
        with patch("idea_factory.agent.generate_next_idea", side_effect=CreditExhaustedError("5-hour limit reached")):
            state = run_agent_loop(max_hours=5.0, interval_seconds=0.0, max_iterations=10)
            self.assertEqual(state["status"], "CREDIT_LIMIT_REACHED")
            self.assertIn("5-hour limit reached", state["stop_reason"])

    def test_agent_loop_waits_for_5hr_refresh_and_resumes(self) -> None:
        seed = get_seed_ideas()[0]
        effects = [
            CreditExhaustedError("5-hour token limit reached"),
            (seed, "synthesis", 0.0),
        ]
        with (
            patch("idea_factory.agent.generate_next_idea", side_effect=effects),
            patch("idea_factory.agent.save_idea"),
        ):
            state = run_agent_loop(
                max_hours=5.0,
                interval_seconds=0.0,
                max_iterations=1,
                auto_resume_on_refresh=True,
                refresh_cooldown_seconds=0.01,
                max_refresh_cycles=2,
            )
            self.assertEqual(state["status"], "COMPLETED_MAX_ITERATIONS")
            self.assertEqual(state["window_cycle"], 2)
            self.assertEqual(state["new_ideas_added_this_run"], 1)

    def test_storage_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            db_p = tmp_path / "test.db"
            json_p = tmp_path / "ideas.json"
            md_p = tmp_path / "IDEAS_CATALOG.md"
            first = get_seed_ideas()[0]
            save_idea(first, db_path=db_p, json_path=json_p, catalog_path=md_p)
            loaded = load_ideas(json_p)
            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0].id, first.id)
            self.assertTrue(md_p.exists())

    def test_postgres_migration_file_and_upsert_sql(self) -> None:
        mig_file_1 = config.MIGRATIONS_DIR / "001_initial_idea_factory_schema.sql"
        mig_file_2 = config.MIGRATIONS_DIR / "002_recalibrated_scoring_v2.sql"
        self.assertTrue(mig_file_1.exists(), "Migration file 001_initial_idea_factory_schema.sql must exist")
        self.assertTrue(mig_file_2.exists(), "Migration file 002_recalibrated_scoring_v2.sql must exist")
        sql_text_1 = mig_file_1.read_text(encoding="utf-8")
        for obj_name in (
            "CREATE TABLE IF NOT EXISTS schema_migrations",
            "CREATE TABLE IF NOT EXISTS product_ideas",
            "CREATE TABLE IF NOT EXISTS idea_metrics",
            "CREATE TABLE IF NOT EXISTS idea_diligence_questions",
            "CREATE TABLE IF NOT EXISTS agent_runs",
            "CREATE OR REPLACE VIEW v_idea_leaderboard",
            "CREATE OR REPLACE VIEW v_portfolio_summary",
            "CREATE OR REPLACE VIEW v_category_analytics",
        ):
            self.assertIn(obj_name, sql_text_1)
        sql_text_2 = mig_file_2.read_text(encoding="utf-8")
        self.assertIn("ALTER TABLE product_ideas", sql_text_2)
        self.assertIn("capital_required_usd", sql_text_2)
        first = get_seed_ideas()[0]
        upsert_sql = _idea_to_upsert_sql(first)
        self.assertIn("INSERT INTO product_ideas", upsert_sql)
        self.assertIn("annual_churn_pct", upsert_sql)
        self.assertIn("capital_required_usd", upsert_sql)
        self.assertIn("INSERT INTO idea_metrics", upsert_sql)
        self.assertIn("INSERT INTO idea_diligence_questions", upsert_sql)
        self.assertEqual(pg_literal(["PAT-01", "PAT-02"]), "ARRAY['PAT-01', 'PAT-02']::text[]")


if __name__ == "__main__":
    unittest.main()

