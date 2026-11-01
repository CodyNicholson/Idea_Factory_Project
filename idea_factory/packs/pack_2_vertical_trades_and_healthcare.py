"""Pack 2: High-Survival Commercial Trades, Field Services, and Outpatient Healthcare AI."""
from __future__ import annotations

from ..models import ProductIdea
from ..seed_ideas import make_idea

IDEAS_PACK_2: list[ProductIdea] = [
    make_idea(
        id="IDEA-005",
        slug="hvac-pact-commercial-pm-os",
        title="HVAC Pact AI — Commercial HVAC & Refrigeration Preventative-Maintenance Contract & Dispatch OS",
        tagline="Turns one-off commercial HVAC/refrigeration repair shops into high-margin recurring preventative-maintenance machines.",
        summary=(
            "Directly implements `Business_Analyzer_Project`'s highest-scoring Midwest B2B playbook for NAICS `238220` (56% baseline 5-year survival, "
            "61.4% in US_MIDWEST, 4.2% low SBA charge-off rate): HVAC Pact AI ingests equipment nameplate photos from technician phones, auto-generates "
            "multi-year ASHRAE-compliant Preventative Maintenance (PM) service agreements, automates seasonal route density scheduling, and flags "
            "end-of-life rooftop units for high-margin replacement upsells."
        ),
        category="Vertical B2B SaaS (Trades)",
        naics_code="238220",
        business_archetype="VERTICAL_SAAS",
        target_metro="Minneapolis-St. Paul MSA (US-MN-33460) & Chicago MSA (US-IL-16980)",
        pattern_ids=["PAT-01", "PAT-02", "PAT-03"],
        referenced_skills=["software-intake-planner", "enterprise-fullstack-plugin"],
        referenced_projects=["Business_Analyzer_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_NO_MARKET_NEED", "FAIL_RENT_LABOR_SQUEEZE"],
        s12=0.93,
        s60=0.68,
        initial_capex_usd=32_000,
        steady_state_ebitda_usd=610_000,
        annual_contract_value_usd=18_000,
        cac_usd=1_900,
        gross_margin_pct=87.0,
        annual_churn_pct=5.0,
        monthly_burn_usd=2_900,
        runway_months=22.0,
        founder_fit_score=93.0,
        acuteness_of_problem=(
            "Severe revenue feast-or-famine: commercial HVAC and refrigeration contractors rely heavily on emergency summer/winter breakdowns, "
            "leaving technicians idle in shoulder months (spring/fall) while losing 4–6x valuation multiples because they lack contracted recurring "
            "PM revenue (`SUCC_RECURRING_B2B`). Estimating a multi-building commercial PM contract manually takes 6+ hours of spreadsheet math per bid."
        ),
        ten_x_better_solution=(
            "10x faster PM proposal generation (5 minutes on-site vs. 6 hours back at the office): a tech snaps photos of rooftop unit (RTU) and "
            "walk-in cooler serial plates; HVAC Pact AI decodes tonnage/age/refrigerant type (R-410A phaseout compliance), calculates exact filter/belt/"
            "coil labor hours, and renders a branded multi-year PDF contract (`Resume_Creator_Project` PDF engine) with instant ACH auto-billing."
        ),
        usage_and_retention_metrics=(
            "Used daily by field techs and service managers; 95% annual retention because all multi-year customer PM schedules, asset registries, "
            "and recurring ACH billing live inside the system."
        ),
        tam_and_growth_tailwinds=(
            "$4.1B TAM across 115,000+ US HVAC/R contractors; massive tailwinds from EPA AIM Act refrigerant transitions, commercial heat-pump mandates, "
            "and private-equity roll-ups paying 8–12x EBITDA for contractors with >40% recurring maintenance share."
        ),
        competition_and_defensible_edge=(
            "ServiceTitan costs $300–$500+/tech/month with 6-month implementation bloat geared toward residential plumbing/HVAC. HVAC Pact AI is a "
            "lightweight, commercial-first PM & asset lifecycle engine that deploys in 48 hours and owns a proprietary RTU/refrigeration nameplate database."
        ),
        why_customers_switch=(
            "Commercial contractors switch because ServiceTitan is built for residential 'sell-a-new-furnace' call centers rather than multi-site B2B "
            "preventative maintenance contracts and EPA refrigerant logbooks."
        ),
        cac_ltv_and_payback=(
            "CAC is $1,900 via commercial HVAC distributor partnerships (Johnstone, Ferguson) and a free 'RTU Nameplate Decoder & PM Pricing Calculator'. "
            "At $18,000 ACV, 87% gross margin, and 5% churn, LTV is $313,200 (LTV:CAC = 164.8x) with a 1.5-month payback."
        ),
        nature_of_revenue=(
            "Sticky annual SaaS subscription ($1,500/mo per contractor) plus 0.5% embedded payment processing take-rate on recurring commercial PM invoices."
        ),
        actual_paying_customers=(
            "Owners and Service Managers of 10-to-75 truck commercial HVAC and refrigeration contractors in Chicago, Minneapolis, Columbus, and Indianapolis."
        ),
        burn_rate_and_runway=(
            "$2,900/month burn on $32,000 initial capital; reaches profitability with just 2 paying commercial HVAC contractors."
        ),
        unit_economics_scaling=(
            "Every nameplate scanned is cached by model prefix in PostgreSQL, dropping vision/LLM inference calls to near zero after the first 5,000 units."
        ),
        fundraising_and_cap_table=(
            "100% bootstrapped; zero VC dilution required due to rapid 45-day SMB sales cycles and upfront annual billing."
        ),
        founder_product_fit=(
            "93/100 fit: combines `Business_Analyzer_Project`'s NAICS `238220` actuarial forecasting, `Resume_Creator_Project`'s deterministic PDF contract "
            "renderer, and `enterprise-fullstack-plugin`'s Postgres/React/Spring architecture."
        ),
        pressure_and_pivot_playbook=(
            "If standalone SaaS adoption slows, partner with PE commercial HVAC roll-up platforms as their standardized post-acquisition PM conversion engine."
        ),
        signal_inspiration="Business_Analyzer_Project NAICS 238220 top Midwest survival pick",
    ),
    make_idea(
        id="IDEA-006",
        slug="gridrebate-electrical-permit-compiler",
        title="GridRebate AI — Commercial EV-Charger, Battery & Panel-Upgrade Permit + Utility Rebate Compiler",
        tagline="Automates NEC load calculations, municipal permit packets, and utility make-ready rebate filings for electrical contractors.",
        summary=(
            "Built directly on `Business_Analyzer_Project`'s NAICS `238210` playbook ('Specialize in EV-charger, battery and panel-upgrade work for builders', "
            "which has a 1.14x regional fit in Sunbelt/Midwest metros): GridRebate AI turns site photos and single-line panel schedules into stamped-ready "
            "NEC Article 220 load calculations, municipal permit PDFs, and ComEd/Oncor/PG&E commercial EV & battery rebate applications."
        ),
        category="Vertical B2B SaaS (Trades)",
        naics_code="238210",
        business_archetype="VERTICAL_SAAS",
        target_metro="Austin-Round Rock MSA (US-TX-12420) & Chicago MSA (US-IL-16980)",
        pattern_ids=["PAT-01", "PAT-02", "PAT-04"],
        referenced_skills=["software-intake-planner", "enterprise-fullstack-plugin"],
        referenced_projects=["Business_Analyzer_Project", "Resume_Creator_Project", "Rixus_RE_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_NO_MARKET_NEED", "FAIL_UNIT_ECON_CAC"],
        s12=0.91,
        s60=0.63,
        initial_capex_usd=35_000,
        steady_state_ebitda_usd=580_000,
        annual_contract_value_usd=21_600,
        cac_usd=2_200,
        gross_margin_pct=86.0,
        annual_churn_pct=5.5,
        monthly_burn_usd=3_000,
        runway_months=22.0,
        founder_fit_score=92.0,
        acuteness_of_problem=(
            "Acute administrative bottleneck: electrical contractors win lucrative commercial EV fleet, battery storage, and 400A–2000A panel upgrade jobs, "
            "but projects stall for 6–14 weeks in municipal permitting and utility interconnection queues because estimators spend 12+ hours per project "
            "filling out inconsistent city PDF forms and utility rebate worksheets."
        ),
        ten_x_better_solution=(
            "10x faster permit and rebate approval: GridRebate AI uses deterministic NEC Article 220 calculation rules (`validate_intake.py` invariant pattern) "
            "plus municipal jurisdiction templates (`PostGIS` parcel lookup from `Business_Analyzer_Project`) to generate a complete permit + utility rebate "
            "submission packet in 15 minutes—unlocking $10k–$100k in utility subsidies that close the sale for the contractor."
        ),
        usage_and_retention_metrics=(
            "Used on every commercial bid and installation; 94% annual retention because contractors embed the live 'Utility Rebate Estimate' widget "
            "directly on their customer quotes to win bids at higher margins."
        ),
        tam_and_growth_tailwinds=(
            "$3.8B TAM across 75,000+ US electrical contractors and commercial solar/EV installers; propelled by $7.5B+ in federal/utility electrification "
            "rebates, data-center power constraints, and fleet electrification."
        ),
        competition_and_defensible_edge=(
            "Solar-only tools (Aurora Solar) ignore commercial electrical panel upgrades and utility fleet make-ready rebates. GridRebate's edge is its "
            "continuously updated PostGIS map of utility feeder capacity, local AHJ (Authority Having Jurisdiction) code amendments, and live rebate balances."
        ),
        why_customers_switch=(
            "Contractors switch the moment they lose a $150,000 commercial EV/panel bid to a competitor who quoted the project at half the net price "
            "by bundling an pre-approved utility make-ready rebate."
        ),
        cac_ltv_and_payback=(
            "CAC is $2,200 via a free 'ZIP-Code Utility Rebate & NEC 220 Load Calculator' web tool. At $21,600 ACV, 86% gross margin, and 5.5% churn, "
            "LTV is $337,745 (LTV:CAC = 153.5x) with a 1.4-month payback."
        ),
        nature_of_revenue=(
            "Recurring SaaS subscription ($1,800/mo) or $1,000/mo base + $199 per approved permit/rebate packet."
        ),
        actual_paying_customers=(
            "Commercial electrical contractors, EV charging EPCs, and multifamily property electrical retrofittters in Texas, Illinois, California, and North Carolina."
        ),
        burn_rate_and_runway=(
            "$3,000/month burn rate on $35,000 initial capital; reaches cash-flow positivity with 2 customers."
        ),
        unit_economics_scaling=(
            "86%+ gross margins: NEC load math and PDF packet rendering (`pdf-lib` / Python vector drawing) are 100% deterministic CPU operations."
        ),
        fundraising_and_cap_table=(
            "Bootstrapped to $1M ARR; zero debt or complex cap table instruments."
        ),
        founder_product_fit=(
            "92/100 fit: combines `Business_Analyzer_Project`'s PostGIS geospatial intelligence, `Resume_Creator_Project`'s pixel-accurate PDF compiler, "
            "and `software-intake-planner`'s deterministic validation engine."
        ),
        pressure_and_pivot_playbook=(
            "If federal EV incentives fluctuate, pivot emphasis to commercial backup generator, microgrid battery, and industrial panel upgrade permitting, "
            "which are driven by grid reliability rather than federal policy."
        ),
        signal_inspiration="Business_Analyzer_Project NAICS 238210 Sunbelt/Midwest electrical playbook",
    ),
]

IDEAS_PACK_2.extend([
    make_idea(
        id="IDEA-007",
        slug="claimscope-remediation-insurer-packet",
        title="ClaimScope AI — Water & Mold Mitigation Xactimate Scope & Insurer Receivables Accelerator",
        tagline="Turns technician moisture-meter logs and jobsite photos into IICRC S500/S520-compliant insurer claim packets that cut carrier payout times from 75 days to 14 days.",
        summary=(
            "Directly addresses `Business_Analyzer_Project`'s NAICS `562910` (Remediation Services) playbook ('Get on insurer and property-manager preferred-vendor "
            "lists; insurance receivables need a 60-90 day working-capital buffer'): ClaimScope AI ingests daily psychrometric readings, thermal images, and "
            "voice notes from mitigation crews and compiles line-by-line Xactimate/Symbility justification narratives cited to IICRC S500/S520 standards—eliminating "
            "desk-adjuster pushback and cutting Days Sales Outstanding (DSO) by 60%+."
        ),
        category="Vertical B2B SaaS (Trades)",
        naics_code="562910",
        business_archetype="AI_NATIVE_SERVICE",
        target_metro="Atlanta-Sandy Springs MSA (US-GA-12060) & Chicago MSA (US-IL-16980)",
        pattern_ids=["PAT-01", "PAT-03", "PAT-04"],
        referenced_skills=["software-intake-planner", "enterprise-fullstack-plugin"],
        referenced_projects=["Business_Analyzer_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_CASH_BURN_RUNWAY", "FAIL_NO_MARKET_NEED"],
        s12=0.90,
        s60=0.60,
        initial_capex_usd=34_000,
        steady_state_ebitda_usd=570_000,
        annual_contract_value_usd=24_000,
        cac_usd=2_400,
        gross_margin_pct=86.0,
        annual_churn_pct=5.5,
        monthly_burn_usd=2_900,
        runway_months=22.0,
        founder_fit_score=91.0,
        acuteness_of_problem=(
            "Existential working-capital crunch (`FAIL_CASH_BURN_RUNWAY`): water and mold mitigation contractors pay crew wages and equipment fuel weekly, "
            "but insurance desk adjusters routinely reject or slash 25–40% of line items (dehumidifier days, HEPA air scrubbers, PPE) for 'insufficient drying "
            "log justification,' trapping contractors in a 60–90 day receivable lag."
        ),
        ten_x_better_solution=(
            "10x faster claim approval and 22% higher approved invoice value: ClaimScope AI validates daily moisture/grain-depression readings in real time "
            "(alerting the crew before leaving the site if a required photo or reading is missing, using `software-intake-planner`'s `[UNKNOWN: UNK-n]` check) "
            "and outputs an ironclad, IICRC-cited supplement packet that desk adjusters approve on first review."
        ),
        usage_and_retention_metrics=(
            "Used on every single water/mold loss job from Day 1 to dry-out completion; 94%+ annual retention because it directly accelerates cash collection."
        ),
        tam_and_growth_tailwinds=(
            "$3.2B TAM across 32,000+ US restoration and remediation firms; strong climate and extreme-weather tailwinds driving commercial and residential "
            "water-intrusion claims."
        ),
        competition_and_defensible_edge=(
            "Encircle and CompanyCam capture photos but leave the estimator to manually write Xactimate line-item justifications; outsourced supplement writers "
            "charge 10–15% of the claim and take 5 days. ClaimScope's moat is its deterministic IICRC S500 psychrometric math engine + carrier-specific approval rules."
        ),
        why_customers_switch=(
            "Restoration owners switch after a carrier denies $8,000 of air-mover/dehumidifier charges on a single commercial flood job due to a missing psychrometric log entry."
        ),
        cac_ltv_and_payback=(
            "CAC is $2,400 via a free 'Denied Line-Item Rebuttal Generator' for Xactimate codes WTR-DHM and WTR-NAFAN. At $24,000 ACV, 86% gross margin, "
            "and 5.5% churn, LTV is $375,272 (LTV:CAC = 156.4x) with a 1.4-month payback."
        ),
        nature_of_revenue=(
            "Recurring monthly SaaS subscription ($2,000/mo for unlimited crews) plus optional 1.5% embedded invoice-factoring referral fee."
        ),
        actual_paying_customers=(
            "Independent and franchised (Servpro, ServiceMaster, PuroClean, independent B2B) water/mold remediation owners and estimators."
        ),
        burn_rate_and_runway=(
            "$2,900/month burn on $34,000 initial capital; cash-flow positive with 2 restoration company customers."
        ),
        unit_economics_scaling=(
            "Psychrometric grain-depression calculations and IICRC rule checks run deterministically; LLM calls are restricted to summarizing unstructured field notes."
        ),
        fundraising_and_cap_table=(
            "100% founder-bootstrapped to $1M ARR via upfront annual contractor subscriptions; zero venture debt, zero participating preferred stock, and no messy uncapped SAFEs."
        ),
        founder_product_fit=(
            "91/100 fit: combines Cody's insurance/telematics data engineering experience at Arity (Allstate spinout) with `Business_Analyzer_Project`'s "
            "NAICS `562910` working-capital model and `Resume_Creator_Project`'s PDF packet generator."
        ),
        pressure_and_pivot_playbook=(
            "If insurers tighten Xactimate API access, export standard ESX/XML and PDF evidence packets that upload into any estimating suite with zero integration lockouts."
        ),
        signal_inspiration="Business_Analyzer_Project NAICS 562910 + Arity insurance data engineering background",
    ),
    make_idea(
        id="IDEA-008",
        slug="surgauth-asc-prior-auth-credentialing",
        title="SurgAuth AI — Autonomous Prior-Authorization Appeal & Payer Credentialing Engine for Outpatient Surgical Centers",
        tagline="Eliminates the 9-12 month payer credentialing bottleneck and recovers denied surgical prior authorizations for independent Ambulatory Surgical Centers (ASCs).",
        summary=(
            "Built on `Business_Analyzer_Project`'s NAICS `621498` (All Other Outpatient Care Centers), which boasts the highest 5-year survival rate in "
            "the catalog (60.0% baseline, 3.6% lowest SBA default rate): SurgAuth AI automates CAQH/PECOS multi-payer physician credentialing packets and "
            "generates clinical peer-to-peer prior-authorization appeal dossiers cited directly to payer LCD/NCD medical policies."
        ),
        category="Healthcare FinTech & Ops",
        naics_code="621498",
        business_archetype="AI_NATIVE_SERVICE",
        target_metro="Nashville-Davidson MSA (US-TN-34980) & Chicago MSA (US-IL-16980)",
        pattern_ids=["PAT-01", "PAT-02", "PAT-04"],
        referenced_skills=["software-intake-planner", "claude-skill-factory", "enterprise-fullstack-plugin"],
        referenced_projects=["Business_Analyzer_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_NO_MARKET_NEED", "FAIL_CASH_BURN_RUNWAY"],
        s12=0.94,
        s60=0.69,
        initial_capex_usd=42_000,
        steady_state_ebitda_usd=740_000,
        annual_contract_value_usd=48_000,
        cac_usd=4_800,
        gross_margin_pct=85.0,
        annual_churn_pct=4.5,
        monthly_burn_usd=3_600,
        runway_months=24.0,
        founder_fit_score=92.0,
        acuteness_of_problem=(
            "Severe revenue blockage: as noted in `Business_Analyzer_Project/worker/intel/reference_data.py` (line 172), independent Ambulatory Surgical Centers "
            "(ASCs) must budget 9–12 months for licensing and payer credentialing before a new surgeon can bill in-network, losing $50,000+/month per uncredentialed "
            "surgeon, while losing another 12–18% of scheduled orthopedic/GI/ophthalmology procedures to last-minute prior-authorization denials."
        ),
        ten_x_better_solution=(
            "10x faster appeal & credentialing assembly: SurgAuth AI continuously audits payer medical necessity checklists (Aetna, UHC, BCBS, Medicare LCDs) "
            "against the patient's chart notes *before* submission (catching missing conservative-therapy dates via `software-intake-planner`'s `[UNKNOWN]` "
            "checklist pattern) and auto-maintains primary-source credentialing expirables across 40+ payers."
        ),
        usage_and_retention_metrics=(
            "Used daily by ASC billing/scheduling staff for every surgical booking; 96% annual retention and <4.5% churn because it holds the center's "
            "live payer credentialing calendar and medical-necessity rulebook."
        ),
        tam_and_growth_tailwinds=(
            "$6.4B TAM across 6,200+ Medicare-certified ASCs and 45,000+ specialty outpatient clinics; massive secular tailwind as CMS and commercial payers "
            "shift orthopedic, spine, and cardiology procedures from hospitals to lower-cost ASCs."
        ),
        competition_and_defensible_edge=(
            "Legacy EHR modules (HST Pathways, SIS) track schedules but do not cross-examine clinical notes against payer-specific LCD denial criteria; "
            "outsourced RCM agencies charge 5–7% of net collections. SurgAuth's moat is its payer-by-CPT deterministic medical-necessity rule graph."
        ),
        why_customers_switch=(
            "ASC administrators switch immediately after a single $18,000 total-joint or spine procedure is canceled 24 hours before surgery or denied "
            "post-op due to a missing physical-therapy documentation checkbox."
        ),
        cac_ltv_and_payback=(
            "CAC is $4,800 via free 'ASC Payer Credentialing Gap & CPT Prior-Auth Denial Audit' workshops with state ASC associations. At $48,000 ACV, "
            "85% gross margin, and 4.5% churn, LTV is $906,667 (LTV:CAC = 188.9x) with a 1.4-month payback."
        ),
        nature_of_revenue=(
            "High-margin annual B2B subscription ($4,000/mo per surgical center) with multi-year contract terms."
        ),
        actual_paying_customers=(
            "ASC Administrators, Medical Directors, and Physician-Owners at independent orthopedic, GI, pain-management, and ophthalmology surgical centers."
        ),
        burn_rate_and_runway=(
            "$3,600/month burn on $42,000 initial capital; reaches profitability with a single paying ASC customer."
        ),
        unit_economics_scaling=(
            "Payer LCD/NCD policy updates are parsed once centrally and shared across all customer ASCs, driving marginal gross margins above 90%."
        ),
        fundraising_and_cap_table=(
            "100% founder-controlled; physician-owners of pilot ASCs frequently offer non-dilutive customer prepayments or strategic angel checks."
        ),
        founder_product_fit=(
            "92/100 fit: applies `software-intake-planner`'s deterministic gap/unknown verification engine (`validate_intake.py`) and `Business_Analyzer_Project`'s "
            "pgvector policy search directly to the highest-survival NAICS sector (`621498`) in the database."
        ),
        pressure_and_pivot_playbook=(
            "Zero-PHI starting wedge: launch first with Physician Payer Credentialing & Payer Policy Search (which requires zero patient HIPAA PHI), "
            "signing BAA agreements only when upselling the Prior-Auth Appeal module."
        ),
        signal_inspiration="Business_Analyzer_Project NAICS 621498 (60% 5-yr survival leader) + software-intake-planner checklist engine",
    ),
])
