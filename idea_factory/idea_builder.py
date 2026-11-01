"""Builds a scored ProductIdea from founder estimates and the 14 diligence answers."""
from __future__ import annotations

import re
from datetime import datetime, timezone

from .models import (
    BusinessModelTraction,
    FinancialsRunway,
    MarketCompetition,
    ProductIdea,
    ProductProblemSolving,
    TeamExecution,
)
from .scoring import compute_idea_metrics
from .workspace_intel import BUSINESS_ANALYZER_INDUSTRIES


def make_idea(
    *,
    id: str,
    slug: str,
    title: str,
    tagline: str,
    summary: str,
    category: str,
    naics_code: str,
    business_archetype: str,
    target_metro: str,
    pattern_ids: list[str],
    referenced_skills: list[str],
    referenced_projects: list[str],
    causal_drivers: list[str],
    mitigated_failure_modes: list[str],
    s12: float,
    s60: float,
    initial_capex_usd: float,
    steady_state_ebitda_usd: float,
    annual_contract_value_usd: float,
    cac_usd: float,
    gross_margin_pct: float,
    annual_churn_pct: float,
    monthly_burn_usd: float,
    runway_months: float,
    founder_fit_score: float,
    acuteness_of_problem: str,
    ten_x_better_solution: str,
    usage_and_retention_metrics: str,
    tam_and_growth_tailwinds: str,
    competition_and_defensible_edge: str,
    why_customers_switch: str,
    cac_ltv_and_payback: str,
    nature_of_revenue: str,
    actual_paying_customers: str,
    burn_rate_and_runway: str,
    unit_economics_scaling: str,
    fundraising_and_cap_table: str,
    founder_product_fit: str,
    pressure_and_pivot_playbook: str,
    generation_source: str = "WORKSPACE_SYNTHESIS",
    signal_inspiration: str = "",
) -> ProductIdea:
    """Construct a ProductIdea and compute its actuarial & unit-economics scores."""
    bench = BUSINESS_ANALYZER_INDUSTRIES.get(naics_code)
    industry_name = bench.subsector if bench else "Vertical B2B Software"
    lgd = bench.lgd_pct if bench else 0.50
    sigma = bench.volatility if bench else 0.32

    calc = compute_idea_metrics(
        s12=s12,
        s60=s60,
        initial_capex_usd=initial_capex_usd,
        steady_state_ebitda_usd=steady_state_ebitda_usd,
        lgd=lgd,
        sigma=sigma,
        archetype=business_archetype,
        cac_usd=cac_usd,
        annual_contract_value_usd=annual_contract_value_usd,
        gross_margin_pct=gross_margin_pct,
        annual_churn_pct=annual_churn_pct,
    )
    scoring_inputs = {
        "s12": s12,
        "s60": s60,
        "cac_usd": cac_usd,
        "gross_margin_pct": gross_margin_pct,
        "annual_churn_pct": annual_churn_pct,
        "monthly_burn_usd": monthly_burn_usd,
        "runway_months": runway_months,
        "lgd": lgd,
        "sigma": sigma,
    }
    narr = unit_economics_narratives(
        calc,
        acv=annual_contract_value_usd,
        capex=initial_capex_usd,
        ebitda=steady_state_ebitda_usd,
        cac_estimate=cac_usd,
        original_cac_text=cac_ltv_and_payback,
        original_retention_text=usage_and_retention_metrics,
    )

    return ProductIdea(
        id=id,
        slug=slug,
        title=title,
        tagline=tagline,
        summary=summary,
        category=category,
        naics_code=naics_code,
        industry_name=industry_name,
        business_archetype=business_archetype,
        target_metro=target_metro,
        pattern_ids=pattern_ids,
        referenced_skills=referenced_skills,
        referenced_projects=referenced_projects,
        causal_drivers=causal_drivers,
        mitigated_failure_modes=mitigated_failure_modes,
        roi_score=calc["roi_score"],
        survival_1yr=calc["survival_1yr"],
        survival_5yr=calc["survival_5yr"],
        projected_3yr_irr_pct=calc["projected_3yr_irr_pct"],
        initial_capex_usd=initial_capex_usd,
        steady_state_ebitda_usd=steady_state_ebitda_usd,
        annual_contract_value_usd=annual_contract_value_usd,
        cac_usd=calc["cac_usd"],
        ltv_usd=calc["ltv_usd"],
        ltv_cac_ratio=calc["ltv_cac_ratio"],
        payback_months=calc["payback_months"],
        gross_margin_pct=calc["gross_margin_pct"],
        monthly_burn_usd=calc["monthly_burn_usd"],
        runway_months=calc["runway_months"],
        founder_fit_score=founder_fit_score,
        product_and_problem_solving=ProductProblemSolving(
            acuteness_of_problem=acuteness_of_problem,
            ten_x_better_solution=ten_x_better_solution,
            usage_and_retention_metrics=narr["usage_and_retention_metrics"],
        ),
        market_and_competition=MarketCompetition(
            tam_and_growth_tailwinds=tam_and_growth_tailwinds,
            competition_and_defensible_edge=competition_and_defensible_edge,
            why_customers_switch=why_customers_switch,
        ),
        business_model_and_traction=BusinessModelTraction(
            cac_ltv_and_payback=narr["cac_ltv_and_payback"],
            nature_of_revenue=nature_of_revenue,
            actual_paying_customers=actual_paying_customers,
        ),
        financials_and_runway=FinancialsRunway(
            burn_rate_and_runway=narr["burn_rate_and_runway"],
            unit_economics_scaling=unit_economics_scaling,
            fundraising_and_cap_table=fundraising_and_cap_table,
        ),
        team_and_execution=TeamExecution(
            founder_product_fit=founder_product_fit,
            pressure_and_pivot_playbook=pressure_and_pivot_playbook,
        ),
        created_at=datetime.now(timezone.utc).isoformat(),
        generation_source=generation_source,
        signal_inspiration=signal_inspiration,
        annual_churn_pct=calc["annual_churn_pct"],
        capital_required_usd=calc["capital_required_usd"],
        customers_to_steady_state=calc["customers_to_steady_state"],
        customer_segment=calc["customer_segment"],
        scoring_version=calc["scoring_version"],
        scoring_inputs=scoring_inputs,
    )


_CHANNEL_RE = re.compile(r"\bvia (.+?)(?:\.\s|\.$)", re.DOTALL)
_RETENTION_RE = re.compile(r"\d+(?:\.\d+)?% (Gross Revenue Retention \(GRR\)|annual retention)")
_PRIOR_CALIBRATION_RE = re.compile(r"^Founder estimate: \$[\d,]+ CAC via ")


def unit_economics_narratives(
    calc: dict,
    *,
    acv: float,
    capex: float,
    ebitda: float,
    cac_estimate: float,
    original_cac_text: str,
    original_retention_text: str,
) -> dict[str, str]:
    """Rewrite the number-bearing diligence answers (3.1, 4.1, and the retention figure in 1.3) from calibrated metrics.

    Keeps the idea's go-to-market channel and qualitative retention story; replaces every hardcoded figure so the
    prose can never disagree with the stored metrics.
    """
    source = _PRIOR_CALIBRATION_RE.sub("CAC via ", original_cac_text)
    m = _CHANNEL_RE.search(source)
    channel = m.group(1).strip() if m else "founder-led outbound and industry-association partnerships"
    grr = 100.0 - float(calc["annual_churn_pct"])
    acquisition = float(calc["capital_required_usd"]) - capex

    cac_text = (
        f"Founder estimate: ${cac_estimate:,.0f} CAC via {channel}. Benchmark-calibrated "
        f"({calc['customer_segment']} segment, {calc['scoring_version']}): CAC ≈ ${calc['cac_usd']:,.0f}, "
        f"{calc['annual_churn_pct']:.1f}% annual churn, and {calc['gross_margin_pct']:.0f}% gross margin on ${acv:,.0f} ACV "
        f"give a 5-year discounted LTV of ${calc['ltv_usd']:,.0f} (LTV:CAC {calc['ltv_cac_ratio']:.1f}x) "
        f"and a {calc['payback_months']:.1f}-month CAC payback."
    )
    burn_text = (
        f"Reaching ${ebitda:,.0f} steady-state EBITDA requires ≈{calc['customers_to_steady_state']:,.0f} customers at "
        f"${acv:,.0f} ACV, i.e. ≈${calc['capital_required_usd']:,.0f} total capital (${capex:,.0f} build + "
        f"≈${acquisition:,.0f} customer acquisition). Expect ≈${calc['monthly_burn_usd']:,.0f}/month net burn through a "
        f"{calc['runway_months']:.0f}-month ramp, funded by early annual prepayments, revenue-based financing, or a seed round."
    )
    if _RETENTION_RE.search(original_retention_text):
        retention_text = _RETENTION_RE.sub(lambda mm: f"{grr:.1f}% {mm.group(1)}", original_retention_text, count=1)
    else:
        retention_text = f"{original_retention_text.rstrip()} Calibrated gross logo retention: {grr:.1f}%/yr."
    return {
        "cac_ltv_and_payback": cac_text,
        "burn_rate_and_runway": burn_text,
        "usage_and_retention_metrics": retention_text,
    }
