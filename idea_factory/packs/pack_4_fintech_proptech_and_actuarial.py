"""Pack 4: Construction PropTech, Actuarial Lending Intelligence, and B2B FinTech."""
from __future__ import annotations

from ..models import ProductIdea
from ..seed_ideas import make_idea

IDEAS_PACK_4: list[ProductIdea] = [
    make_idea(
        id="IDEA-013",
        slug="drawshield-construction-draw-lien-waiver",
        title="DrawShield — Automated Construction Draw Request, AIA G702/G703 & Lien-Waiver Verification Engine",
        tagline="Cuts commercial construction loan draw approvals from 14 days to 24 hours with deterministic schedule-of-values math and conditional lien-waiver tracking.",
        summary=(
            "Directly implements `Business_Analyzer_Project`'s NAICS `531390` (PropTech & Construction FinTech) playbook ('Automate a painful builder or "
            "property-manager workflow (draw management, permitting) with per-project pricing', which carries a 1.15x Sunbelt fit): DrawShield ingests "
            "subcontractor invoices, AIA G702/G703 PDFs, geotagged site photos, and conditional/unconditional lien waivers, verifies arithmetic and retainage "
            "invariants (`INV-n`), and triggers instant title-company/lender wire release."
        ),
        category="PropTech & Construction FinTech",
        naics_code="531390",
        business_archetype="VERTICAL_SAAS",
        target_metro="Dallas-Fort Worth MSA (US-TX-19100) & Phoenix MSA (US-AZ-38060)",
        pattern_ids=["PAT-01", "PAT-02", "PAT-04"],
        referenced_skills=["software-intake-planner", "enterprise-fullstack-plugin"],
        referenced_projects=["Business_Analyzer_Project", "Rixus_RE_Project", "Accounting_Backend_API_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_NO_MARKET_NEED", "FAIL_CASH_BURN_RUNWAY"],
        s12=0.91,
        s60=0.61,
        initial_capex_usd=38_000,
        steady_state_ebitda_usd=660_000,
        annual_contract_value_usd=36_000,
        cac_usd=3_500,
        gross_margin_pct=87.0,
        annual_churn_pct=5.5,
        monthly_burn_usd=3_100,
        runway_months=22.0,
        founder_fit_score=94.0,
        acuteness_of_problem=(
            "Monthly hair-on-fire pain for every general contractor (GC) and real estate developer: every month, a GC must collect 25–60 subcontractor "
            "pay applications (AIA G702/G703), verify 10% retainage math, match state-specific statutory lien waivers, and submit a 200-page draw packet "
            "to the construction lender. One arithmetic mismatch or missing notarized lien waiver freezes a $500,000+ draw for 2 weeks."
        ),
        ten_x_better_solution=(
            "10x faster draw cycle: DrawShield parses subcontractor PDFs, cross-checks line-item completion percentages against previous draws and "
            "change orders using deterministic ledger invariants (`Accounting_Backend_API_Project`), auto-generates statutory state lien waivers "
            "(`Resume_Creator_Project` PDF compiler), and gives the lender a verified one-click approval package."
        ),
        usage_and_retention_metrics=(
            "100% monthly stickiness for the entire 12–36 month life of every construction project; once a GC or construction lender standardizes on "
            "DrawShield for 1 project, they mandate it across all active projects (135%+ NRR)."
        ),
        tam_and_growth_tailwinds=(
            "$5.1B TAM across 85,000+ US commercial/multifamily general contractors, real estate developers, and private construction lenders."
        ),
        competition_and_defensible_edge=(
            "Procore costs $30,000–$100,000+/yr and still requires manual lender draw packet formatting; Built Technologies sells top-down to mega-banks "
            "with slow 9-month onboarding. DrawShield wins mid-market GCs and debt funds immediately via instant per-project onboarding and network effects "
            "(every GC brings 30 subcontractors onto the platform)."
        ),
        why_customers_switch=(
            "Developers and GCs switch when a delayed bank draw causes a subcontractor to walk off the jobsite or file a mechanic's lien."
        ),
        cac_ltv_and_payback=(
            "CAC is $3,500 via a free 'AIA G702/G703 & State Statutory Lien Waiver Generator' web tool (`Resume_Creator_Project` PDF engine) and viral "
            "subcontractor invites. At $36,000 ACV ($500/mo per active project, average 6 projects/builder), 87% gross margin, and 5.5% churn, "
            "LTV is $569,454 (LTV:CAC = 162.7x) with a 1.3-month payback."
        ),
        nature_of_revenue=(
            "Per-project recurring monthly SaaS ($500/project/mo) plus optional instant-ACH subcontractor disbursement fee."
        ),
        actual_paying_customers=(
            "Mid-market multifamily/commercial developers, General Contractors, and private real estate bridge/construction lenders in Dallas, Phoenix, Austin, and Chicago."
        ),
        burn_rate_and_runway=(
            "$3,100/month burn on $38,000 initial capital; reaches break-even with just 2 mid-market developers (7 active projects)."
        ),
        unit_economics_scaling=(
            "Schedule-of-values ledger arithmetic and state lien-waiver PDF generation are 100% deterministic CPU tasks, keeping gross margins at 87%+."
        ),
        fundraising_and_cap_table=(
            "100% founder-bootstrapped via per-project upfront draw fees; clean single-class common stock cap table with zero convertible debt or messy SAFEs."
        ),
        founder_product_fit=(
            "94/100 fit: combines `Rixus_RE_Project` (real estate platform in Go/Postgres/React), `Accounting_Backend_API_Project` (ledger invariants), "
            "`Business_Analyzer_Project` (NAICS `531390` playbook), and `Resume_Creator_Project` (PDF vector rendering)."
        ),
        pressure_and_pivot_playbook=(
            "If GCs resist paying out of pocket, bill the DrawShield fee as an eligible project-level construction loan closing/inspection line item paid by the borrower's draw."
        ),
        signal_inspiration="Business_Analyzer_Project NAICS 531390 + Rixus_RE_Project + Accounting_Backend_API_Project",
    ),
    make_idea(
        id="IDEA-014",
        slug="sba-actuarial-underwrite-intelligence",
        title="SurvivalQuant — Actuarial SBA 7(a)/504 Underwriting & Portfolio Early-Warning API for Community Banks",
        tagline="Commercializes `Business_Analyzer_Project` into a B2B credit-intelligence API for SBA lenders, CDFIs, and commercial credit committees.",
        summary=(
            "Directly productizes `/Users/codynicholson/workspace/Business_Analyzer_Project`: SurvivalQuant packages the Cox Proportional-Hazards survival "
            "model, LightGBM quantile EBITDA/CapEx regressors, SBA FOIA charge-off predictor, Israelsen Risk-Adjusted ROI score, and live CourtListener / "
            "SEC Form D / BLS QCEW feeds into a white-label Loan Committee Memo Generator and Portfolio Surveillance SaaS for the 1,800+ active US SBA 7(a) and 504 lenders."
        ),
        category="Actuarial FinTech & Intelligence",
        naics_code="522320",
        business_archetype="VERTICAL_SAAS",
        target_metro="Chicago-Naperville-Elgin MSA (US-IL-16980) & Charlotte/Raleigh (US-NC-39580)",
        pattern_ids=["PAT-01", "PAT-02", "PAT-07"],
        referenced_skills=["visual-lab", "software-intake-planner", "enterprise-fullstack-plugin"],
        referenced_projects=["Business_Analyzer_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_NO_MARKET_NEED", "FAIL_CASH_BURN_RUNWAY", "FAIL_UNIT_ECON_CAC"],
        s12=0.94,
        s60=0.68,
        initial_capex_usd=20_000,
        steady_state_ebitda_usd=780_000,
        annual_contract_value_usd=45_000,
        cac_usd=3_900,
        gross_margin_pct=91.0,
        annual_churn_pct=4.5,
        monthly_burn_usd=2_200,
        runway_months=24.0,
        founder_fit_score=100.0,
        acuteness_of_problem=(
            "Acute credit-committee pain: SBA 7(a) and 504 underwriters at community banks and credit unions must underwrite SMB acquisition and startup loans "
            "across dozens of NAICS codes and metros. Today they copy-paste static, national IBISWorld PDFs that ignore local metro saturation (BLS QCEW location "
            "quotient), regional commercial rent-to-income pressure, and historical metro×NAICS SBA charge-off rates—leading to costly loan defaults."
        ),
        ten_x_better_solution=(
            "10x faster and actuarially rigorous: an underwriter enters the borrower's 6-digit NAICS code, CBSA metro, requested loan amount, and projected "
            "DSCR; SurvivalQuant instantly queries the TimescaleDB/PostGIS engine (`Business_Analyzer_Project`), returns the 1-yr and 5-yr survival curve, "
            "predicted SBA default probability, SHAP risk drivers, and 5 comparable post-mortem failure autopsies (`pgvector` cosine search) in a ready-to-attach Credit Committee PDF."
        ),
        usage_and_retention_metrics=(
            "Used on every commercial/SBA loan application screened by the bank's credit team; 96% annual retention because it becomes part of the bank's "
            "documented OCC/SBA credit-policy compliance file."
        ),
        tam_and_growth_tailwinds=(
            "$3.9B TAM across 1,800+ SBA lenders, 4,500+ community banks, 1,400+ CDFIs, and 3,000+ lower-middle-market business brokers and search-fund investors."
        ),
        competition_and_defensible_edge=(
            "IBISWorld ($15k+/yr) provides static national text essays with zero metro-level survival math or SBA charge-off models; VerticalIQ lacks "
            "actuarial Cox PH / LightGBM forecasting and CourtListener post-mortem evidence. SurvivalQuant's engine is already built in `Business_Analyzer_Project`."
        ),
        why_customers_switch=(
            "Chief Credit Officers switch when rising interest rates spike their SBA 7(a) charge-offs and examiners demand localized, data-driven industry risk benchmarking."
        ),
        cac_ltv_and_payback=(
            "CAC is $3,900 by deploying the already-built `Business_Analyzer_Project/lab` Findings Lab publicly as an interactive lead magnet for SBA underwriters "
            "and search-fund buyers. At $45,000 ACV, 91% gross margin, and 4.5% churn, LTV is $910,000 (LTV:CAC = 233.3x) with a 1.1-month payback."
        ),
        nature_of_revenue=(
            "Multi-year annual B2B institutional subscription ($3,750/mo per bank/lender)."
        ),
        actual_paying_customers=(
            "Heads of SBA Lending, Chief Credit Officers at community/regional banks, CDFI directors, and self-funded ETA (Entrepreneurship Through Acquisition) searchers."
        ),
        burn_rate_and_runway=(
            "$2,200/month burn on $20,000 initial capital—because 90% of the product (`api/`, `worker/`, `db/`, `web/`, `lab/`) is already built and tested in `Business_Analyzer_Project`!"
        ),
        unit_economics_scaling=(
            "91%+ gross margin: public data sources (BLS QCEW, Census BDS/BFS, FRED, World Bank, SEC EDGAR, SBA FOIA) are 100% free government feeds."
        ),
        fundraising_and_cap_table=(
            "100% founder-owned; near-zero additional R&D required to close the first 5 bank/search-fund customers."
        ),
        founder_product_fit=(
            "Perfect 100/100 founder-product fit: Cody Nicholson built the entire `Business_Analyzer_Project` (FastAPI, TimescaleDB, PostGIS, pgvector, "
            "Cox PH, LightGBM, Israelsen ROI, and the Visual Findings Lab)."
        ),
        pressure_and_pivot_playbook=(
            "While bank procurement cycles run (60–90 days), sell a $299/month self-serve tier immediately to SMB acquisition searchers (ETA/Searchfunder community) "
            "evaluating Main Street businesses on BizBuySell."
        ),
        signal_inspiration="Business_Analyzer_Project (direct commercialization of existing workspace engine)",
    ),
]

IDEAS_PACK_4.extend([
    make_idea(
        id="IDEA-015",
        slug="camaudit-commercial-lease-escalation-recovery",
        title="CAM-Audit AI — Commercial NNN Lease, CAM Reconciliation & Property-Tax Pass-Through Recovery Engine",
        tagline="Audits landlord Common Area Maintenance (CAM) reconciliations against commercial lease clauses to recover 8-15% in illegal landlord overcharges.",
        summary=(
            "Directly inspired by `Business_Analyzer_Project/worker/intel/seed.py`'s primary Midwest/Coastal failure driver `FAIL_RENT_LABOR_SQUEEZE` "
            "('A lease escalation and rising local wages squeezed operating margin... Property-tax pass-throughs on the retail lease added to occupancy costs'): "
            "CAM-Audit AI ingests a multi-unit tenant's 80-page commercial NNN lease PDF alongside the landlord's year-end CAM reconciliation statement, "
            "checks every expense against lease caps, pro-rata share formulas, and excluded capital expenditures, and generates a formal legal/accounting audit demand."
        ),
        category="PropTech & Construction FinTech",
        naics_code="531390",
        business_archetype="AI_NATIVE_SERVICE",
        target_metro="Chicago-Naperville-Elgin MSA (US-IL-16980) & New York MSA (US-NY-35620)",
        pattern_ids=["PAT-01", "PAT-03", "PAT-04"],
        referenced_skills=["software-intake-planner", "enterprise-fullstack-plugin"],
        referenced_projects=["Business_Analyzer_Project", "Rixus_RE_Project", "Accounting_Backend_API_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_RENT_LABOR_SQUEEZE", "FAIL_NO_MARKET_NEED"],
        s12=0.92,
        s60=0.63,
        initial_capex_usd=28_000,
        steady_state_ebitda_usd=640_000,
        annual_contract_value_usd=30_000,
        cac_usd=2_800,
        gross_margin_pct=88.0,
        annual_churn_pct=5.0,
        monthly_burn_usd=2_600,
        runway_months=24.0,
        founder_fit_score=94.0,
        acuteness_of_problem=(
            "Massive silent profit leak: industry studies show 70%+ of commercial Triple-Net (NNN) landlord year-end CAM reconciliation bills contain errors "
            "favoring the landlord (charging tenants for roof replacements, landlord management overhead above the 5% cap, or vacant-anchor pro-rata manipulation). "
            "Multi-location dental groups, urgent cares, franchises (`722513`), and regional retailers lose $5,000–$25,000 per location per year because "
            "human lease auditors charge $3,500 upfront per lease."
        ),
        ten_x_better_solution=(
            "10x faster and feasible for every store location: CAM-Audit AI extracts the exact CAM cap, base-year, gross-up, and capital-exclusion clauses "
            "from the lease PDF, reconciles them deterministically against the landlord's general-ledger invoice dump (`Accounting_Backend_API_Project`), "
            "and produces a clause-cited audit dispute letter in 5 minutes."
        ),
        usage_and_retention_metrics=(
            "Recurring annual reconciliation audit + monthly NNN escrow tracking across all tenant locations; 95% annual retention because landlords "
            "issue new CAM reconciliations every spring."
        ),
        tam_and_growth_tailwinds=(
            "$3.4B TAM across 120,000+ multi-unit retail, restaurant franchise, outpatient clinic (`621498`), and industrial warehouse tenants in North America."
        ),
        competition_and_defensible_edge=(
            "Lease administration software (VisualLease, CoStar Real Estate Manager) tracks renewal dates but does not audit line-item landlord GL expenses "
            "against custom lease exclusions; boutique CPA lease-audit firms only take Fortune 500 clients. CAM-Audit's moat is its landlord-GL classification database."
        ),
        why_customers_switch=(
            "Multi-unit operators switch immediately when a free 1-location historical CAM audit uncovers a $12,000 landlord overbilling credit."
        ),
        cac_ltv_and_payback=(
            "CAC is $2,800 via a 'Free 1-Lease CAM Overcharge Scan' offer to multi-unit franchise and clinic CFOs. At $30,000 ACV ($150/location/mo for "
            "a 15-unit operator + 15% of recovered credits), 88% gross margin, and 5% churn, LTV is $528,000 (LTV:CAC = 188.6x) with a 1.3-month payback."
        ),
        nature_of_revenue=(
            "Base per-location annual SaaS subscription plus contingency share on historical CAM refunds recovered."
        ),
        actual_paying_customers=(
            "CFOs and Directors of Real Estate at 5-to-200 unit franchise groups (`722513`), outpatient medical/dental groups (`621498`), and regional retailers."
        ),
        burn_rate_and_runway=(
            "$2,600/month burn on $28,000 initial capital; profitable from the second multi-unit customer."
        ),
        unit_economics_scaling=(
            "Once a tenant's lease PDF is parsed into structured invariant rules in Year 1, Year 2–10 annual CAM audits run deterministically at 94% gross margin."
        ),
        fundraising_and_cap_table=(
            "100% founder-bootstrapped from first-month contingency recoveries and annual tenant retainers; zero institutional dilution or debt instruments."
        ),
        founder_product_fit=(
            "94/100 fit: combines `Rixus_RE_Project` (real estate platform), `Accounting_Backend_API_Project` (accounting ledger validation), and "
            "`Business_Analyzer_Project`'s Cook County/Midwest commercial property-tax pass-through insights."
        ),
        pressure_and_pivot_playbook=(
            "Expand seamlessly from tenant-side CAM defense to commercial property-tax assessment appeal packet generation in high-tax counties like Cook County, IL."
        ),
        signal_inspiration="Business_Analyzer_Project seed.py FAIL_RENT_LABOR_SQUEEZE + Rixus_RE_Project",
    ),
    make_idea(
        id="IDEA-016",
        slug="ledgerrecon-idempotent-subledger-close",
        title="LedgerRecon AI — Autonomous Order-to-Cash & Sub-Ledger Invariant Reconciliation Engine",
        tagline="Continuously reconciles Kafka/Stripe/Shopify/WMS order events against ERP General Ledgers with zero-cent discrepancy guarantees.",
        summary=(
            "Built directly on `Accounting_Backend_API_Project` (Java/Spring Boot/Gradle + Karate contract tests) and `software-intake-planner`'s "
            "`core-intake-checklist.md` financial invariant triggers ('Money, balances, credits, inventory... require an idempotency-key strategy'): "
            "LedgerRecon AI ingests high-volume ecommerce/marketplace order streams, payment processor settlements, refund webhooks, and 3PL fulfillment events, "
            "detects penny-level drift before month-end close, and posts verified, idempotent adjusting journal entries to NetSuite/QuickBooks/SAP."
        ),
        category="Actuarial FinTech & Intelligence",
        naics_code="522320",
        business_archetype="VERTICAL_SAAS",
        target_metro="Chicago-Naperville-Elgin MSA (US-IL-16980)",
        pattern_ids=["PAT-04", "PAT-06"],
        referenced_skills=["enterprise-fullstack-plugin", "software-intake-planner"],
        referenced_projects=["Accounting_Backend_API_Project", "Kafka_Visual_Lab_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B"],
        mitigated_failure_modes=["FAIL_UNIT_ECON_CAC", "FAIL_CASH_BURN_RUNWAY"],
        s12=0.92,
        s60=0.63,
        initial_capex_usd=32_000,
        steady_state_ebitda_usd=650_000,
        annual_contract_value_usd=36_000,
        cac_usd=3_400,
        gross_margin_pct=89.0,
        annual_churn_pct=4.5,
        monthly_burn_usd=2_800,
        runway_months=24.0,
        founder_fit_score=98.0,
        acuteness_of_problem=(
            "Brutal month-end close bottleneck: Controllers and FinOps teams at ecommerce, marketplace, and multi-facility retail companies spend 10–15 days "
            "every month downloading gigabyte CSVs from Stripe, Adyen, Shopify, Kafka order logs, and WMS shipments to figure out why recognized revenue "
            "differs from cash settled by $40,000+ (partial shipments, split captures, duplicate webhook retries, FX rounding)."
        ),
        ten_x_better_solution=(
            "Continuous T+0 stream reconciliation instead of T+30 spreadsheet archaeology: LedgerRecon AI consumes the live order/payment event stream "
            "(`Kafka_Visual_Lab_Project` keyed-partition architecture) and applies double-entry accounting invariants (`Accounting_Backend_API_Project`) "
            "on every transaction lifecycle transition—shrinking month-end close from 12 days to 1 day."
        ),
        usage_and_retention_metrics=(
            "Runs 24/7 on every transaction and is reviewed daily by the Controller and Revenue Accounting team; 96% annual retention because it becomes "
            "the company's SOX / external audit trail."
        ),
        tam_and_growth_tailwinds=(
            "$5.8B TAM in continuous accounting close and order-to-cash reconciliation (Numeric, FloQast, BlackLine challengers; YC 2025–2026 FinTech thesis)."
        ),
        competition_and_defensible_edge=(
            "BlackLine is legacy enterprise bloatware costing $150k+/yr; lightweight AI close checklists don't handle high-throughput multi-facility "
            "order splitting and webhook idempotency bugs. LedgerRecon's edge is its streaming Java/Spring/Postgres matching engine."
        ),
        why_customers_switch=(
            "CFOs and Controllers switch when an external financial audit flags material weaknesses in order-to-cash revenue cutoff or un-reconciled suspense accounts."
        ),
        cac_ltv_and_payback=(
            "CAC is $3,400 via a free '30-Day Stripe/Order-Log Discrepancy Detector' tool. At $36,000 ACV, 89% gross margin, and 4.5% churn, "
            "LTV is $712,000 (LTV:CAC = 209.4x) with a 1.3-month payback."
        ),
        nature_of_revenue=(
            "Annual B2B SaaS subscription ($3,000/mo) tiered by monthly reconciled transaction volume."
        ),
        actual_paying_customers=(
            "Controllers, VPs of Finance, and FinOps Engineering Leads at omnichannel retailers, marketplaces, and B2B ecommerce companies."
        ),
        burn_rate_and_runway=(
            "$2,800/month burn on $32,000 initial capital; `Accounting_Backend_API_Project` already provides the core Spring Boot + Gradle + Karate foundation."
        ),
        unit_economics_scaling=(
            "89%+ gross margin: 99.8% of transaction matching is deterministic SQL/keyed-stream joins; LLM reasoning is invoked only to classify novel fee codes."
        ),
        fundraising_and_cap_table=(
            "100% founder-bootstrapped with upfront annual enterprise contracts; clean cap table free of stacked post-money SAFEs or venture debt."
        ),
        founder_product_fit=(
            "98/100 fit: directly unites Cody's 3M+ order/yr ecommerce fulfillment pipeline experience at Peapod Digital Labs with his "
            "`Accounting_Backend_API_Project` and `ExpenseReportingApp` / `finance-system-example` repositories."
        ),
        pressure_and_pivot_playbook=(
            "Can be sold either directly to mid-market Controllers or as a white-label diagnostic engine for outsourced fractional CFO and audit firms (`541611`)."
        ),
        signal_inspiration="Accounting_Backend_API_Project + Peapod 3M-order ETL + software-intake-planner financial invariants",
    ),
])
