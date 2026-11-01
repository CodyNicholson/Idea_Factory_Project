"""Actuarial survival, Israelsen risk-adjusted ROI, and unit-economics math (scoring v2, benchmark-calibrated).

Adapted from `/Users/codynicholson/workspace/Business_Analyzer_Project/worker/intel/finance.py`
and `worker/intel/reference_data.py` so every product idea is evaluated on the same actuarial scale.

Scoring v2 recalibration
------------------------
v1 took every idea's own inputs at face value, which produced impossible results across the whole catalog
(3-yr IRR pinned at the 300% cap for 100% of ideas, LTV:CAC ~185x, 1.2-month CAC payback). v2 fixes this by:

1. **Credibility-weighting founder estimates toward industry benchmarks.** Each idea's CAC, churn, gross
   margin, and survival inputs are treated as *estimates*. The calibrated value is a blend that gives the
   estimate weight ``CREDIBILITY_Z`` and the benchmark weight ``1 - CREDIBILITY_Z`` (geometric blend for
   CAC and churn, which are ratio-scaled; arithmetic for margins and survival probabilities). Optimistic
   estimates still rank ahead of pessimistic ones, but cannot escape gravity.
2. **Funding customer acquisition.** Reaching steady-state EBITDA requires acquiring enough customers to
   generate it. That acquisition spend is now part of the capital required, and it is deducted from the
   3-year cash flows that feed IRR and the risk-adjusted ROI yield.
3. **Finite, discounted LTV** over a 5-year horizon instead of the unbounded ``ACV * GM / churn``.

Benchmark constants are deliberately round, publicly-reported B2B SaaS medians (e.g. KeyBanc/Sapphire
SaaS surveys, SaaS Capital retention reports, BLS Business Employment Dynamics survival rates). They are
heuristics for *ranking* ideas consistently, not forecasts; tune them here as better data arrives.
"""
from __future__ import annotations

import math
from typing import Callable

SCORING_VERSION = "v2-benchmark-calibrated"

# Terminal value multiple of steady-state annual EBITDA at end of the 3-year horizon
EXIT_MULTIPLE: dict[str, float] = {
    "SMB_MAIN_STREET": 2.5,
    "FRANCHISE": 3.0,
    "SOLOPRENEUR": 1.5,
    "HIGH_GROWTH_STARTUP": 6.0,
    "AI_NATIVE_SERVICE": 5.0,
    "VERTICAL_SAAS": 5.5,
}
SALVAGE_SHARE_OF_RECOVERY = 0.5

# 5-year survival benchmarks per macro archetype (SMB, venture startup) from Business_Analyzer_Project
ARCHETYPE_SURVIVAL_5YR: dict[str, tuple[float, float]] = {
    "US_MIDWEST": (0.614, 0.340),
    "US_SUNBELT": (0.578, 0.315),
    "US_COASTAL": (0.521, 0.268),
    "EU_WEST_NORTH": (0.592, 0.294),
    "APAC_LATAM": (0.485, 0.220),
}
SMB_SURVIVAL_BASELINE = 0.556
STARTUP_SURVIVAL_BASELINE = 0.290

# ---------------------------------------------------------------------------
# v2 calibration benchmarks
# ---------------------------------------------------------------------------
# Weight given to an idea's own estimate (0 = ignore estimates, 1 = v1 face-value behaviour)
CREDIBILITY_Z = 0.30

# New-establishment survival (approx. BLS Business Employment Dynamics): ~80% reach year 1, ~50% year 5
BENCHMARK_S12 = 0.80
BENCHMARK_S60 = 0.50

# Customer segment by ACV: (max ACV exclusive, annual gross logo churn, median CAC payback months)
SEGMENT_BENCHMARKS: list[tuple[str, float, float, float]] = [
    ("SMB", 15_000.0, 0.30, 12.0),
    ("MID_MARKET", 100_000.0, 0.15, 18.0),
    ("ENTERPRISE", math.inf, 0.08, 24.0),
]

# Gross-margin benchmark by archetype (AI-native services carry inference + human-in-the-loop COGS)
BENCHMARK_GROSS_MARGIN: dict[str, float] = {
    "VERTICAL_SAAS": 0.78,
    "AI_NATIVE_SERVICE": 0.62,
    "HIGH_GROWTH_STARTUP": 0.72,
    "SOLOPRENEUR": 0.70,
    "SMB_MAIN_STREET": 0.50,
    "FRANCHISE": 0.45,
}

# Mature EBITDA margin by archetype: converts a steady-state EBITDA target into required revenue
STEADY_STATE_EBITDA_MARGIN: dict[str, float] = {
    "VERTICAL_SAAS": 0.25,
    "AI_NATIVE_SERVICE": 0.20,
    "HIGH_GROWTH_STARTUP": 0.20,
    "SOLOPRENEUR": 0.30,
    "SMB_MAIN_STREET": 0.15,
    "FRANCHISE": 0.15,
}

LTV_HORIZON_YEARS = 5
LTV_DISCOUNT_RATE = 0.10
# Phasing of acquisition spend across the ramp: year 0, year 1, year 2 (year 3 = steady state)
ACQUISITION_PHASING = (0.4, 0.4, 0.2)
# Logistic slope mapping the Israelsen ratio to 0-100 (tuned so the v2 catalog spans roughly 38-85, median ~47)
ROI_SCORE_SLOPE = 8.0


def segment_for_acv(acv: float) -> tuple[str, float, float]:
    """Return (segment name, benchmark annual churn, benchmark CAC payback months) for an ACV."""
    for name, upper, churn, payback in SEGMENT_BENCHMARKS:
        if acv < upper:
            return name, churn, payback
    name, _, churn, payback = SEGMENT_BENCHMARKS[-1]
    return name, churn, payback


def credibility_blend(estimate: float, benchmark: float, z: float = CREDIBILITY_Z, geometric: bool = False) -> float:
    """Blend an estimate toward a benchmark: Z * estimate + (1 - Z) * benchmark (optionally in log space)."""
    if geometric:
        estimate = max(estimate, 1e-9)
        benchmark = max(benchmark, 1e-9)
        return math.exp(z * math.log(estimate) + (1.0 - z) * math.log(benchmark))
    return z * estimate + (1.0 - z) * benchmark


def weibull_survival_curve(s12: float, s60: float) -> Callable[[float], float]:
    """Fit S(t) = exp(-(t/lam)^k) through S(12) and S(60) and return S as a function of months."""
    s12 = min(max(s12, 0.01), 0.999)
    s60 = min(max(s60, 0.005), s12 - 1e-4)
    k = (math.log(-math.log(s60)) - math.log(-math.log(s12))) / math.log(60.0 / 12.0)
    k = max(k, 0.05)
    lam = 12.0 / (-math.log(s12)) ** (1.0 / k)
    return lambda t: math.exp(-((t / lam) ** k))


def risk_adjusted_roi(s60: float, ebitda: float, capex: float, lgd: float, sigma: float) -> float:
    """(S60 * Yield - (1 - S60) * LGD) / sigma_sector, where Yield = steady-state EBITDA / capital invested.

    Uses Israelsen's correction: for a negative numerator the ratio is multiplied by sigma
    instead of divided, preventing high-variance money-losers from outranking steadier ones.
    In v2, ``capex`` should be the *total capital required* (build cost + customer acquisition),
    so no artificial yield dampening is needed.
    """
    capex = max(capex, 1.0)
    yield_ = ebitda / capex
    numerator = s60 * yield_ - (1.0 - s60) * lgd
    sigma = max(sigma, 1e-3)
    return numerator / sigma if numerator >= 0 else numerator * sigma


def roi_score(raw: float, slope: float | None = None) -> float:
    """Map the unbounded Israelsen ratio to a 1-99.9 ranking score (50 = break-even risk-adjusted)."""
    slope = ROI_SCORE_SLOPE if slope is None else slope
    return round(min(99.9, max(1.0, 100.0 / (1.0 + math.exp(-slope * raw)))), 2)


def irr(cashflows: list[float], lo: float = -0.99, hi: float = 100.0) -> float | None:
    """Annual internal rate of return by bisection; None when there is no sign change."""

    def npv(rate: float) -> float:
        return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))

    f_lo, f_hi = npv(lo), npv(hi)
    if f_lo * f_hi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2.0
        f_mid = npv(mid)
        if abs(f_mid) < 1e-6:
            break
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


def projected_3yr_irr_pct(
    capex: float,
    ebitda: float,
    survival: Callable[[float], float],
    lgd: float,
    archetype: str,
    acquisition_spend: float = 0.0,
) -> float:
    """IRR of survival-weighted cash flows over a 3-year horizon.

    Year 0: -(CapEx + phased acquisition spend). Year 1: EBITDA ~0 while ramping, minus acquisition spend.
    Year 2: half of steady-state EBITDA (survival-weighted) minus remaining acquisition spend.
    Year 3: full survival-weighted EBITDA plus exit value (or salvage if the venture failed).
    With ``acquisition_spend=0`` this reduces to a pure build-cost model (v1-compatible shape).
    """
    s12, s24, s36 = survival(12), survival(24), survival(36)
    p0, p1, p2 = ACQUISITION_PHASING
    mult = EXIT_MULTIPLE.get(archetype, 3.5)
    terminal = s36 * mult * ebitda + (1.0 - s36) * (1.0 - lgd) * capex * SALVAGE_SHARE_OF_RECOVERY
    if acquisition_spend > 0:
        flows = [
            -(capex + p0 * acquisition_spend),
            -p1 * acquisition_spend,
            0.5 * ebitda * s24 - p2 * acquisition_spend,
            ebitda * s36 + terminal,
        ]
    else:
        flows = [-capex, ebitda * s12, ebitda * s24, ebitda * s36 + terminal]
    rate = irr(flows)
    if rate is None:
        return -99.0
    return round(min(300.0, max(-99.0, rate * 100.0)), 2)


def discounted_ltv(acv: float, gross_margin: float, annual_churn: float) -> float:
    """Gross-profit LTV over LTV_HORIZON_YEARS, decayed by churn and discounted at LTV_DISCOUNT_RATE."""
    retention_discount = (1.0 - annual_churn) / (1.0 + LTV_DISCOUNT_RATE)
    annual_gp = acv * gross_margin
    return sum(annual_gp * retention_discount**t for t in range(LTV_HORIZON_YEARS))


def compute_idea_metrics(
    *,
    s12: float,
    s60: float,
    initial_capex_usd: float,
    steady_state_ebitda_usd: float,
    lgd: float,
    sigma: float,
    archetype: str,
    cac_usd: float,
    annual_contract_value_usd: float,
    gross_margin_pct: float,
    annual_churn_pct: float,
) -> dict[str, float | str]:
    """Compute benchmark-calibrated actuarial and unit-economics metrics for a product idea.

    All arguments are the idea's own *estimates*; returned values are calibrated (see module docstring).
    """
    acv = max(annual_contract_value_usd, 1.0)
    segment, bench_churn, bench_payback = segment_for_acv(acv)

    # 1. Calibrate survival, gross margin, churn, and CAC toward benchmarks
    s12_cal = round(min(max(credibility_blend(s12, BENCHMARK_S12), 0.40), 0.98), 4)
    s60_cal = round(min(max(credibility_blend(s60, BENCHMARK_S60), 0.15), s12_cal - 0.02), 4)
    gm_est = min(max(gross_margin_pct / 100.0, 0.20), 0.96)
    gm_cal = credibility_blend(gm_est, BENCHMARK_GROSS_MARGIN.get(archetype, 0.70))
    churn_est = min(max(annual_churn_pct / 100.0, 0.01), 0.90)
    churn_cal = credibility_blend(churn_est, bench_churn, geometric=True)
    bench_cac = bench_payback * (acv / 12.0) * gm_cal
    cac_cal = credibility_blend(max(cac_usd, 50.0), bench_cac, geometric=True)

    # 2. Unit economics: finite discounted LTV, LTV:CAC, CAC payback on gross profit
    ltv = discounted_ltv(acv, gm_cal, churn_cal)
    payback = cac_cal / max((acv / 12.0) * gm_cal, 1.0)

    # 3. Capital required: build cost + acquiring enough customers to reach steady-state EBITDA
    ebitda_margin = STEADY_STATE_EBITDA_MARGIN.get(archetype, 0.20)
    customers_needed = (steady_state_ebitda_usd / ebitda_margin) / acv
    acquisition_spend = customers_needed * cac_cal * (1.0 + churn_cal)  # replace ~1 year of churn during ramp
    capital_required = initial_capex_usd + acquisition_spend
    ramp_burn_months = 24.0
    monthly_burn = (initial_capex_usd + sum(ACQUISITION_PHASING[:2]) * acquisition_spend) / ramp_burn_months

    # 4. Risk-adjusted ROI and 3-year IRR on total capital, survival-weighted
    curve = weibull_survival_curve(s12_cal, s60_cal)
    raw = risk_adjusted_roi(s60_cal, steady_state_ebitda_usd, capital_required, lgd, sigma)
    irr_3yr = projected_3yr_irr_pct(
        initial_capex_usd, steady_state_ebitda_usd, curve, lgd, archetype, acquisition_spend=acquisition_spend
    )

    return {
        "scoring_version": SCORING_VERSION,
        "customer_segment": segment,
        "survival_1yr": s12_cal,
        "survival_5yr": s60_cal,
        "risk_adjusted_roi_raw": round(raw, 4),
        "roi_score": roi_score(raw),
        "projected_3yr_irr_pct": irr_3yr,
        "gross_margin_pct": round(gm_cal * 100.0, 1),
        "annual_churn_pct": round(churn_cal * 100.0, 1),
        "cac_usd": round(cac_cal, 0),
        "ltv_usd": round(ltv, 0),
        "ltv_cac_ratio": round(ltv / cac_cal, 2),
        "payback_months": round(payback, 1),
        "customers_to_steady_state": round(customers_needed, 0),
        "capital_required_usd": round(capital_required, 0),
        "monthly_burn_usd": round(monthly_burn, 0),
        "runway_months": ramp_burn_months,
    }
