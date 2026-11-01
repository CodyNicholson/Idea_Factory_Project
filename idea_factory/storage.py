"""Idea persistence. PostgreSQL is the only store; the Markdown catalog is an on-demand export."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from . import config
from .models import ProductIdea
from .postgres import latest_agent_state, load_ideas_postgres, upsert_ideas_postgres


def load_ideas() -> list[ProductIdea]:
    """Load all ideas from PostgreSQL, ordered by risk-adjusted ROI score descending."""
    return load_ideas_postgres()


def load_agent_state() -> dict[str, Any]:
    """Return the telemetry of the most recent agent run."""
    return latest_agent_state() or {"status": "IDLE", "model": config.GEMINI_MODEL, "iterations": 0}


def render_catalog_markdown(
    ideas: list[ProductIdea],
    *,
    catalog_path: Path = config.CATALOG_MD_PATH,
) -> None:
    """Write `IDEAS_CATALOG.md`: a leaderboard summary and the 14-point diligence for each idea."""
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

> Exported from PostgreSQL by `python3 -m idea_factory catalog`.

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
    catalog_path.write_text(doc, encoding="utf-8")


def rescore_idea(idea: ProductIdea) -> ProductIdea:
    """Recalibrate an existing ProductIdea with benchmark-calibrated scoring v2."""
    from .idea_builder import unit_economics_narratives
    from .scoring import compute_idea_metrics
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
    """Rescore every idea in PostgreSQL with scoring v2 and save the results."""
    rescored = [rescore_idea(idea) for idea in load_ideas()]
    upsert_ideas_postgres(rescored)
    return rescored
