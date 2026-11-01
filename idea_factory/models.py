"""Data models and deterministic validation for Product Ideas and the 14 Diligence Questions."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ProductProblemSolving:
    """Section 1: Product & Problem-Solving."""
    acuteness_of_problem: str
    ten_x_better_solution: str
    usage_and_retention_metrics: str


@dataclass
class MarketCompetition:
    """Section 2: Market & Competition."""
    tam_and_growth_tailwinds: str
    competition_and_defensible_edge: str
    why_customers_switch: str


@dataclass
class BusinessModelTraction:
    """Section 3: Business Model & Traction."""
    cac_ltv_and_payback: str
    nature_of_revenue: str
    actual_paying_customers: str


@dataclass
class FinancialsRunway:
    """Section 4: Financials & Runway."""
    burn_rate_and_runway: str
    unit_economics_scaling: str
    fundraising_and_cap_table: str


@dataclass
class TeamExecution:
    """Section 5: Team & Execution."""
    founder_product_fit: str
    pressure_and_pivot_playbook: str


@dataclass
class ProductIdea:
    """A complete, quantitatively scored product blueprint answering all 5 sections (14 questions)."""
    id: str
    slug: str
    title: str
    tagline: str
    summary: str
    category: str
    naics_code: str
    industry_name: str
    business_archetype: str
    target_metro: str
    pattern_ids: list[str]
    referenced_skills: list[str]
    referenced_projects: list[str]
    causal_drivers: list[str]
    mitigated_failure_modes: list[str]

    # Quantitative metrics (Business_Analyzer_Project actuarial + unit economics)
    roi_score: float
    survival_1yr: float
    survival_5yr: float
    projected_3yr_irr_pct: float
    initial_capex_usd: float
    steady_state_ebitda_usd: float
    annual_contract_value_usd: float
    cac_usd: float
    ltv_usd: float
    ltv_cac_ratio: float
    payback_months: float
    gross_margin_pct: float
    monthly_burn_usd: float
    runway_months: float
    founder_fit_score: float

    # The 5 Required Sections (14 Questions)
    product_and_problem_solving: ProductProblemSolving
    market_and_competition: MarketCompetition
    business_model_and_traction: BusinessModelTraction
    financials_and_runway: FinancialsRunway
    team_and_execution: TeamExecution

    created_at: str = ""
    generation_source: str = "SEED_SYNTHESIS"
    signal_inspiration: str = ""

    # Scoring v2 (benchmark-calibrated) outputs and the raw founder estimates they were derived from
    annual_churn_pct: float = 0.0
    capital_required_usd: float = 0.0
    customers_to_steady_state: float = 0.0
    customer_segment: str = ""
    scoring_version: str = "v1-face-value"
    scoring_inputs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ProductIdea:
        data = dict(d)
        data["product_and_problem_solving"] = ProductProblemSolving(**data["product_and_problem_solving"])
        data["market_and_competition"] = MarketCompetition(**data["market_and_competition"])
        data["business_model_and_traction"] = BusinessModelTraction(**data["business_model_and_traction"])
        data["financials_and_runway"] = FinancialsRunway(**data["financials_and_runway"])
        data["team_and_execution"] = TeamExecution(**data["team_and_execution"])
        return cls(**data)

    def to_markdown(self, index: int | None = None) -> str:
        """Render the complete product idea and all 14 diligence answers as formatted Markdown."""
        prefix = f"#{index:02d} — " if index is not None else ""
        skills_str = ", ".join(f"`{s}`" for s in self.referenced_skills)
        projs_str = ", ".join(f"`{p}`" for p in self.referenced_projects)
        patterns_str = ", ".join(f"`{p}`" for p in self.pattern_ids)
        drivers_str = ", ".join(f"`{c}`" for c in self.causal_drivers)
        mitigated_str = ", ".join(f"`{m}`" for m in self.mitigated_failure_modes)

        return f"""## {prefix}{self.title} (`{self.id}`)

> **{self.tagline}**

* **Category / Archetype:** `{self.category}` · `{self.business_archetype}`
* **NAICS Sector & Target Launch Metro:** `{self.naics_code}` ({self.industry_name}) · **{self.target_metro}**
* **Referenced Skills (`Claude_Skills_Project`):** {skills_str}
* **Referenced Workspace Projects:** {projs_str}
* **Applied Startup Patterns:** {patterns_str}
* **SHAP Success Drivers:** {drivers_str} | **Inoculated Failure Risks:** {mitigated_str}
* **Source / Signal Provenance:** `{self.generation_source}`{f" ({self.signal_inspiration})" if self.signal_inspiration else ""}

| Risk-Adjusted ROI Score | 5-Yr Survival $S(60)$ | 1-Yr Survival $S(12)$ | 3-Yr Projected IRR | Initial CapEx | Year-3 Target EBITDA / ARR | LTV : CAC Ratio | CAC Payback | Gross Margin | Founder Fit |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **{self.roi_score:.1f} / 100** | **{self.survival_5yr * 100:.1f}%** | {self.survival_1yr * 100:.1f}% | **{self.projected_3yr_irr_pct:.1f}%** | \\${self.initial_capex_usd:,.0f} | \\${self.steady_state_ebitda_usd:,.0f}/yr | **{self.ltv_cac_ratio:.1f}x** (\\${self.ltv_usd:,.0f} / \\${self.cac_usd:,.0f}) | **{self.payback_months:.1f} mos** | **{self.gross_margin_pct:.0f}%** | **{self.founder_fit_score:.0f}/100** |

* **Capital Required to Steady State:** \\\\${self.capital_required_usd:,.0f} (~{self.customers_to_steady_state:,.0f} customers, {self.customer_segment or "n/a"} segment) · **Annual Churn:** {self.annual_churn_pct:.1f}% · **Scoring:** `{self.scoring_version}`

### Executive Summary
{self.summary}

### 1. Product & Problem-Solving
* **How acute is the problem?** {self.product_and_problem_solving.acuteness_of_problem}
* **Is the solution 10x better?** {self.product_and_problem_solving.ten_x_better_solution}
* **What are the usage and retention metrics?** {self.product_and_problem_solving.usage_and_retention_metrics}

### 2. Market & Competition
* **How big is the market and is it growing?** {self.market_and_competition.tam_and_growth_tailwinds}
* **Who is the competition and what is the "edge"?** {self.market_and_competition.competition_and_defensible_edge}
* **Why do customers switch?** {self.market_and_competition.why_customers_switch}

### 3. Business Model & Traction
* **What does customer acquisition look like?** {self.business_model_and_traction.cac_ltv_and_payback}
* **What is the nature of the revenue?** {self.business_model_and_traction.nature_of_revenue}
* **Who are the actual paying customers?** {self.business_model_and_traction.actual_paying_customers}

### 4. Financials & Runway
* **What is the burn rate and runway?** {self.financials_and_runway.burn_rate_and_runway}
* **Are unit economics improving?** {self.financials_and_runway.unit_economics_scaling}
* **What are the fundraising and cap table realities?** {self.financials_and_runway.fundraising_and_cap_table}

### 5. Team & Execution
* **Do they have founder-product fit?** {self.team_and_execution.founder_product_fit}
* **How do they handle pressure and pivot?** {self.team_and_execution.pressure_and_pivot_playbook}
"""


def validate_idea(idea: ProductIdea) -> list[str]:
    """Deterministic validator ensuring all 14 questions and actuarial invariants pass."""
    errors: list[str] = []
    if not idea.id or not idea.title or not idea.slug:
        errors.append("Missing id, slug, or title.")
    if len(idea.summary.strip()) < 80:
        errors.append(f"Idea {idea.id}: summary is too short (< 80 chars).")

    checks = [
        ("1.1 acuteness_of_problem", idea.product_and_problem_solving.acuteness_of_problem),
        ("1.2 ten_x_better_solution", idea.product_and_problem_solving.ten_x_better_solution),
        ("1.3 usage_and_retention_metrics", idea.product_and_problem_solving.usage_and_retention_metrics),
        ("2.1 tam_and_growth_tailwinds", idea.market_and_competition.tam_and_growth_tailwinds),
        ("2.2 competition_and_defensible_edge", idea.market_and_competition.competition_and_defensible_edge),
        ("2.3 why_customers_switch", idea.market_and_competition.why_customers_switch),
        ("3.1 cac_ltv_and_payback", idea.business_model_and_traction.cac_ltv_and_payback),
        ("3.2 nature_of_revenue", idea.business_model_and_traction.nature_of_revenue),
        ("3.3 actual_paying_customers", idea.business_model_and_traction.actual_paying_customers),
        ("4.1 burn_rate_and_runway", idea.financials_and_runway.burn_rate_and_runway),
        ("4.2 unit_economics_scaling", idea.financials_and_runway.unit_economics_scaling),
        ("4.3 fundraising_and_cap_table", idea.financials_and_runway.fundraising_and_cap_table),
        ("5.1 founder_product_fit", idea.team_and_execution.founder_product_fit),
        ("5.2 pressure_and_pivot_playbook", idea.team_and_execution.pressure_and_pivot_playbook),
    ]
    for label, text in checks:
        if not text or len(text.strip()) < 60:
            errors.append(f"Idea {idea.id}: Question '{label}' is missing or under-detailed (< 60 chars).")

    if not (1.0 <= idea.roi_score <= 99.9):
        errors.append(f"Idea {idea.id}: roi_score {idea.roi_score} outside [1.0, 99.9].")
    if not (0.0 < idea.survival_5yr <= idea.survival_1yr <= 1.0):
        errors.append(
            f"Idea {idea.id}: invalid survival probabilities S(5y)={idea.survival_5yr}, S(1y)={idea.survival_1yr}."
        )
    if idea.ltv_usd <= idea.cac_usd:
        errors.append(f"Idea {idea.id}: LTV ({idea.ltv_usd}) must exceed CAC ({idea.cac_usd}).")
    if not idea.referenced_skills:
        errors.append(f"Idea {idea.id}: must reference at least one skill from Claude_Skills_Project.")
    if not idea.referenced_projects:
        errors.append(f"Idea {idea.id}: must reference at least one workspace project.")
    if idea.scoring_version.startswith("v2"):
        # Plausibility guards: catch regressions back to v1-style impossible unit economics
        if not (1.0 <= idea.ltv_cac_ratio <= 15.0):
            errors.append(f"Idea {idea.id}: LTV:CAC {idea.ltv_cac_ratio}x outside plausible range [1, 15].")
        if not (3.0 <= idea.payback_months <= 48.0):
            errors.append(f"Idea {idea.id}: CAC payback {idea.payback_months} months outside plausible range [3, 48].")
        if idea.projected_3yr_irr_pct >= 300.0:
            errors.append(f"Idea {idea.id}: 3-yr IRR is pinned at the 300% cap; inputs are not credible.")
        if idea.capital_required_usd <= idea.initial_capex_usd:
            errors.append(f"Idea {idea.id}: capital required must include customer acquisition spend.")
    return errors

