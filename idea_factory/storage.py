"""Atomic persistence layer: SQLite (`data/idea_factory.db`), JSON (`data/ideas.json`), and Markdown (`IDEAS_CATALOG.md`)."""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import config
from .models import ProductIdea, validate_idea
from .postgres import (
    get_postgres_status,
    load_ideas_postgres,
    run_migrations,
    upsert_agent_state_postgres,
    upsert_ideas_postgres,
)


def _warn_postgres(operation: str, exc: Exception) -> None:
    """Report (never silently swallow) a failed PostgreSQL write; local JSON/SQLite copies remain intact."""
    print(
        f"WARNING [{operation}]: PostgreSQL write failed ({type(exc).__name__}: {exc}). "
        "Idea saved to local JSON/SQLite; run `python3 -m idea_factory migrate` to backfill Postgres.",
        file=sys.stderr,
    )


def _atomic_write_text(path: Path, content: str) -> None:
    """Atomically write text to `path` via a PID-scoped temp file and `os.replace`."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    tmp_path.write_text(content, encoding="utf-8")
    os.replace(tmp_path, path)


def init_db(db_path: Path = config.SQLITE_DB_PATH) -> None:
    """Ensure SQLite tables exist for ideas and 5-hour agent loop telemetry."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS product_ideas (
                id TEXT PRIMARY KEY,
                slug TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                naics_code TEXT NOT NULL,
                target_metro TEXT NOT NULL,
                roi_score REAL NOT NULL,
                survival_5yr REAL NOT NULL,
                projected_3yr_irr_pct REAL NOT NULL,
                ltv_cac_ratio REAL NOT NULL,
                founder_fit_score REAL NOT NULL,
                generation_source TEXT NOT NULL,
                created_at TEXT NOT NULL,
                payload_json TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS agent_runs (
                run_id TEXT PRIMARY KEY,
                started_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                status TEXT NOT NULL,
                provider TEXT NOT NULL,
                elapsed_seconds REAL NOT NULL,
                max_runtime_seconds INTEGER NOT NULL,
                ideas_generated INTEGER NOT NULL,
                api_calls INTEGER NOT NULL,
                estimated_cost_usd REAL NOT NULL,
                stop_reason TEXT
            )
            """
        )
        conn.commit()


def load_ideas(json_path: Path = config.IDEAS_JSON_PATH) -> list[ProductIdea]:
    """Load all persisted product ideas ordered by Risk-Adjusted ROI score descending (PostgreSQL primary, JSON/SQLite fallback)."""
    if json_path == config.IDEAS_JSON_PATH:
        try:
            pg_ideas = load_ideas_postgres()
            if pg_ideas:
                return pg_ideas
        except Exception:
            pass
    if json_path.exists():
        try:
            text = json_path.read_text(encoding="utf-8")
            if text.strip():
                raw = json.loads(text)
                return [ProductIdea.from_dict(item) for item in raw]
        except Exception:
            pass
    if json_path == config.IDEAS_JSON_PATH and config.SQLITE_DB_PATH.exists():
        with sqlite3.connect(config.SQLITE_DB_PATH, timeout=30.0) as conn:
            rows = conn.execute(
                "SELECT payload_json FROM product_ideas ORDER BY roi_score DESC, id ASC"
            ).fetchall()
        return [ProductIdea.from_dict(json.loads(r[0])) for r in rows]
    return []


def save_idea(
    idea: ProductIdea,
    *,
    db_path: Path = config.SQLITE_DB_PATH,
    json_path: Path = config.IDEAS_JSON_PATH,
    catalog_path: Path = config.CATALOG_MD_PATH,
) -> bool:
    """Validate and atomically persist a new ProductIdea across SQLite, JSON, and IDEAS_CATALOG.md.

    Returns True if inserted or updated, False if validation failed.
    """
    if not idea.created_at:
        idea.created_at = datetime.now(timezone.utc).isoformat()
    errors = validate_idea(idea)
    if errors:
        raise ValueError("Invalid ProductIdea: " + "; ".join(errors))

    init_db(db_path)
    payload_str = json.dumps(idea.to_dict(), ensure_ascii=False)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO product_ideas (
                id, slug, title, category, naics_code, target_metro,
                roi_score, survival_5yr, projected_3yr_irr_pct, ltv_cac_ratio,
                founder_fit_score, generation_source, created_at, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                slug=excluded.slug,
                title=excluded.title,
                category=excluded.category,
                naics_code=excluded.naics_code,
                target_metro=excluded.target_metro,
                roi_score=excluded.roi_score,
                survival_5yr=excluded.survival_5yr,
                projected_3yr_irr_pct=excluded.projected_3yr_irr_pct,
                ltv_cac_ratio=excluded.ltv_cac_ratio,
                founder_fit_score=excluded.founder_fit_score,
                generation_source=excluded.generation_source,
                payload_json=excluded.payload_json
            """,
            (
                idea.id,
                idea.slug,
                idea.title,
                idea.category,
                idea.naics_code,
                idea.target_metro,
                idea.roi_score,
                idea.survival_5yr,
                idea.projected_3yr_irr_pct,
                idea.ltv_cac_ratio,
                idea.founder_fit_score,
                idea.generation_source,
                idea.created_at,
                payload_str,
            ),
        )
        conn.commit()
        rows = conn.execute(
            "SELECT payload_json FROM product_ideas ORDER BY roi_score DESC, id ASC"
        ).fetchall()

    all_ideas = [ProductIdea.from_dict(json.loads(r[0])) for r in rows]
    if db_path == config.SQLITE_DB_PATH:
        try:
            upsert_ideas_postgres([idea])
        except Exception as exc:
            _warn_postgres("save_idea", exc)
    _atomic_write_text(
        json_path,
        json.dumps([i.to_dict() for i in all_ideas], indent=2, ensure_ascii=False),
    )
    render_catalog_markdown(all_ideas, catalog_path=catalog_path)
    if json_path == config.IDEAS_JSON_PATH:
        write_web_bundle(ideas=all_ideas)
    return True


def save_ideas_batch(
    ideas: list[ProductIdea],
    *,
    db_path: Path = config.SQLITE_DB_PATH,
    json_path: Path = config.IDEAS_JSON_PATH,
    catalog_path: Path = config.CATALOG_MD_PATH,
) -> int:
    """Validate and save a batch of ProductIdeas efficiently."""
    init_db(db_path)
    now = datetime.now(timezone.utc).isoformat()
    for idea in ideas:
        if not idea.created_at:
            idea.created_at = now
        errors = validate_idea(idea)
        if errors:
            raise ValueError("; ".join(errors))

    with sqlite3.connect(db_path) as conn:
        for idea in ideas:
            conn.execute(
                """
                INSERT INTO product_ideas (
                    id, slug, title, category, naics_code, target_metro,
                    roi_score, survival_5yr, projected_3yr_irr_pct, ltv_cac_ratio,
                    founder_fit_score, generation_source, created_at, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    slug=excluded.slug,
                    title=excluded.title,
                    category=excluded.category,
                    naics_code=excluded.naics_code,
                    target_metro=excluded.target_metro,
                    roi_score=excluded.roi_score,
                    survival_5yr=excluded.survival_5yr,
                    projected_3yr_irr_pct=excluded.projected_3yr_irr_pct,
                    ltv_cac_ratio=excluded.ltv_cac_ratio,
                    founder_fit_score=excluded.founder_fit_score,
                    generation_source=excluded.generation_source,
                    payload_json=excluded.payload_json
                """,
                (
                    idea.id,
                    idea.slug,
                    idea.title,
                    idea.category,
                    idea.naics_code,
                    idea.target_metro,
                    idea.roi_score,
                    idea.survival_5yr,
                    idea.projected_3yr_irr_pct,
                    idea.ltv_cac_ratio,
                    idea.founder_fit_score,
                    idea.generation_source,
                    idea.created_at,
                    json.dumps(idea.to_dict(), ensure_ascii=False),
                ),
            )
        conn.commit()
        rows = conn.execute(
            "SELECT payload_json FROM product_ideas ORDER BY roi_score DESC, id ASC"
        ).fetchall()

    all_ideas = [ProductIdea.from_dict(json.loads(r[0])) for r in rows]
    if db_path == config.SQLITE_DB_PATH:
        try:
            upsert_ideas_postgres(ideas)
        except Exception as exc:
            _warn_postgres("save_ideas_batch", exc)
    _atomic_write_text(
        json_path,
        json.dumps([i.to_dict() for i in all_ideas], indent=2, ensure_ascii=False),
    )
    render_catalog_markdown(all_ideas, catalog_path=catalog_path)
    if json_path == config.IDEAS_JSON_PATH:
        write_web_bundle(ideas=all_ideas)
    return len(all_ideas)


def render_catalog_markdown(
    ideas: list[ProductIdea],
    *,
    catalog_path: Path = config.CATALOG_MD_PATH,
) -> None:
    """Write the complete `IDEAS_CATALOG.md` with leaderboard summary and 14-point diligence per idea."""
    avg_roi = sum(i.roi_score for i in ideas) / len(ideas) if ideas else 0.0
    avg_s5 = sum(i.survival_5yr for i in ideas) / len(ideas) * 100 if ideas else 0.0
    avg_ltv_cac = sum(i.ltv_cac_ratio for i in ideas) / len(ideas) if ideas else 0.0

    table_rows = []
    for idx, i in enumerate(ideas, start=1):
        table_rows.append(
            f"| {idx} | `{i.id}` | **{i.title}** | `{i.category}` | `{i.naics_code}` | {i.target_metro} | **{i.roi_score:.1f}** | {i.survival_5yr * 100:.1f}% | {i.projected_3yr_irr_pct:.1f}% | {i.ltv_cac_ratio:.1f}x | {i.payback_months:.1f}m | {i.founder_fit_score:.0f}/100 |"
        )
    leaderboard = "\n".join(table_rows)
    sections = "\n\n---\n\n".join(i.to_markdown(index=idx) for idx, i in enumerate(ideas, start=1))

    doc = f"""# Idea Factory — Master Product Ideas Catalog & 14-Point Investor Diligence

> **Autonomous 5-Hour Idea Factory Engine** · Grounded in [`Claude_Skills_Project`](file:///Users/codynicholson/workspace/Claude_Skills_Project/README.md) & [`Business_Analyzer_Project`](file:///Users/codynicholson/workspace/Business_Analyzer_Project/README.md)
> See also: [What Successful Startups Are Doing Right Now & 8 Repeatable Patterns (`docs/STARTUP_PATTERNS_AND_PLAYBOOK.md`)](file:///Users/codynicholson/workspace/Idea_Factory_Project/docs/STARTUP_PATTERNS_AND_PLAYBOOK.md)

## Portfolio Summary & Actuarial Leaderboard

* **Total Product Ideas Evaluated:** **{len(ideas)}**
* **Mean Israelsen Risk-Adjusted ROI Score:** **{avg_roi:.1f} / 100**
* **Mean 5-Year Survival Probability $S(60)$:** **{avg_s5:.1f}%** (vs. 26.8% coastal startup baseline)
* **Mean LTV : CAC Ratio:** **{avg_ltv_cac:.1f}x**

| Rank | ID | Product Title | Category | NAICS | Target Launch Metro | ROI Score | 5-Yr Survival | 3-Yr IRR | LTV:CAC | Payback | Founder Fit |
| :---: | :---: | :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
{leaderboard}

---

{sections}
"""
    _atomic_write_text(catalog_path, doc)


def write_web_bundle(
    ideas: list[ProductIdea] | None = None,
    state: dict[str, Any] | None = None,
) -> None:
    """Write `web/ideas_data.js` so `web/index.html` live-updates even when opened via `file://` or static server."""
    if ideas is None:
        ideas = load_ideas()
    if state is None:
        state = load_agent_state()
    state = dict(state)
    state["ideas_count"] = len(ideas)
    bundle = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "state": state,
        "ideas": [i.to_dict() for i in ideas],
    }
    js_path = config.WEB_DIR / "ideas_data.js"
    _atomic_write_text(
        js_path,
        "window.__IDEA_FACTORY_BUNDLE__ = " + json.dumps(bundle, ensure_ascii=False) + ";\n",
    )


def save_agent_state(state: dict[str, Any], path: Path = config.AGENT_STATE_PATH) -> None:
    """Persist the live 5-hour loop agent telemetry without clobbering an active 5-hr daemon from a one-shot run."""
    path.parent.mkdir(parents=True, exist_ok=True)
    merged = dict(state)
    if path.exists():
        try:
            prev = json.loads(path.read_text(encoding="utf-8"))
            if (
                prev.get("status") == "RUNNING"
                and prev.get("run_id") != state.get("run_id")
                and state.get("elapsed_seconds", 0) < 30
            ):
                merged["run_id"] = prev["run_id"]
                merged["status"] = "RUNNING"
                merged["started_at"] = prev["started_at"]
                merged["elapsed_seconds"] = prev.get("elapsed_seconds", 0.0)
                merged["remaining_seconds"] = prev.get("remaining_seconds", 18000.0)
                merged["iterations"] = max(prev.get("iterations", 0), state.get("iterations", 0))
                merged["stop_reason"] = ""
        except Exception:
            pass
    _atomic_write_text(path, json.dumps(merged, indent=2, ensure_ascii=False))
    if path == config.AGENT_STATE_PATH:
        try:
            upsert_agent_state_postgres(merged)
        except Exception as exc:
            _warn_postgres("save_agent_state", exc)
        write_web_bundle(state=merged)


def sync_all_to_postgres() -> dict[str, Any]:
    """Run PostgreSQL schema migrations and sync all ProductIdeas, metrics, 14 questions, and agent state to Docker Postgres."""
    applied_migrations = run_migrations()
    local_ideas: list[ProductIdea] = []
    if config.IDEAS_JSON_PATH.exists():
        raw = json.loads(config.IDEAS_JSON_PATH.read_text(encoding="utf-8"))
        local_ideas = [ProductIdea.from_dict(item) for item in raw]
    elif config.SQLITE_DB_PATH.exists():
        with sqlite3.connect(config.SQLITE_DB_PATH, timeout=30.0) as conn:
            rows = conn.execute(
                "SELECT payload_json FROM product_ideas ORDER BY roi_score DESC, id ASC"
            ).fetchall()
        local_ideas = [ProductIdea.from_dict(json.loads(r[0])) for r in rows]

    upserted = upsert_ideas_postgres(local_ideas)
    state = load_agent_state()
    state["ideas_count"] = len(local_ideas)
    upsert_agent_state_postgres(state)
    status = get_postgres_status()
    status["upserted_ideas"] = upserted
    status["migrations_just_verified"] = applied_migrations
    return status


def rescore_idea(idea: ProductIdea) -> ProductIdea:
    """Recalibrate an existing ProductIdea with benchmark-calibrated scoring v2."""
    from .scoring import compute_idea_metrics
    from .seed_ideas import unit_economics_narratives
    from .workspace_intel import BUSINESS_ANALYZER_INDUSTRIES

    bench = BUSINESS_ANALYZER_INDUSTRIES.get(idea.naics_code)
    lgd = bench.lgd_pct if bench else 0.50
    sigma = bench.volatility if bench else 0.32

    inputs = idea.scoring_inputs or {}
    s12 = inputs.get("s12", idea.survival_1yr)
    s60 = inputs.get("s60", idea.survival_5yr)
    cac = inputs.get("cac_usd", idea.cac_usd)
    gm = inputs.get("gross_margin_pct", idea.gross_margin_pct)
    churn = inputs.get(
        "annual_churn_pct",
        100.0 * idea.annual_contract_value_usd * min(max(gm / 100.0, 0.2), 0.96) / max(idea.ltv_usd, 1.0),
    )

    calc = compute_idea_metrics(
        s12=s12,
        s60=s60,
        initial_capex_usd=idea.initial_capex_usd,
        steady_state_ebitda_usd=idea.steady_state_ebitda_usd,
        lgd=lgd,
        sigma=sigma,
        archetype=idea.business_archetype,
        cac_usd=cac,
        annual_contract_value_usd=idea.annual_contract_value_usd,
        gross_margin_pct=gm,
        annual_churn_pct=churn,
    )

    narr = unit_economics_narratives(
        calc,
        acv=idea.annual_contract_value_usd,
        capex=idea.initial_capex_usd,
        ebitda=idea.steady_state_ebitda_usd,
        cac_estimate=cac,
        original_cac_text=idea.business_model_and_traction.cac_ltv_and_payback,
        original_retention_text=idea.product_and_problem_solving.usage_and_retention_metrics,
    )

    idea.roi_score = calc["roi_score"]
    idea.survival_1yr = calc["survival_1yr"]
    idea.survival_5yr = calc["survival_5yr"]
    idea.projected_3yr_irr_pct = calc["projected_3yr_irr_pct"]
    idea.cac_usd = calc["cac_usd"]
    idea.ltv_usd = calc["ltv_usd"]
    idea.ltv_cac_ratio = calc["ltv_cac_ratio"]
    idea.payback_months = calc["payback_months"]
    idea.gross_margin_pct = calc["gross_margin_pct"]
    idea.monthly_burn_usd = calc["monthly_burn_usd"]
    idea.runway_months = calc["runway_months"]
    idea.annual_churn_pct = calc["annual_churn_pct"]
    idea.capital_required_usd = calc["capital_required_usd"]
    idea.customers_to_steady_state = calc["customers_to_steady_state"]
    idea.customer_segment = calc["customer_segment"]
    idea.scoring_version = calc["scoring_version"]
    idea.scoring_inputs = {
        "s12": s12,
        "s60": s60,
        "cac_usd": cac,
        "gross_margin_pct": gm,
        "annual_churn_pct": churn,
        "lgd": lgd,
        "sigma": sigma,
    }
    idea.product_and_problem_solving.usage_and_retention_metrics = narr["usage_and_retention_metrics"]
    idea.business_model_and_traction.cac_ltv_and_payback = narr["cac_ltv_and_payback"]
    idea.financials_and_runway.burn_rate_and_runway = narr["burn_rate_and_runway"]
    return idea


def rescore_all_ideas() -> list[ProductIdea]:
    """Rescore all persisted ideas in data/ideas.json to scoring v2 and save across JSON, SQLite, catalog, and web bundle."""
    raw_ideas = load_ideas()
    rescored = [rescore_idea(idea) for idea in raw_ideas]
    save_ideas_batch(rescored)
    return rescored


def load_agent_state(path: Path = config.AGENT_STATE_PATH) -> dict[str, Any]:
    if path.exists():
        try:
            text = path.read_text(encoding="utf-8")
            if text.strip():
                return json.loads(text)
        except Exception:
            pass
    return {
        "status": "IDLE",
        "elapsed_seconds": 0.0,
        "max_runtime_seconds": config.AGENT_MAX_RUNTIME_SECONDS,
        "ideas_count": len(load_ideas()),
        "iterations": 0,
        "provider": "synthesis",
    }

