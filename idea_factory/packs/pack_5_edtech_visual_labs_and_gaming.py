"""Pack 5: Interactive Visual Labs, Developer PLG Sandboxes, Game Production Tech, and Specialty Care."""
from __future__ import annotations

from ..models import ProductIdea
from ..seed_ideas import make_idea

IDEAS_PACK_5: list[ProductIdea] = [
    make_idea(
        id="IDEA-017",
        slug="visuallab-cloud-interactive-plg-sandboxes",
        title="VisualLab Cloud — Autonomous Interactive Product-Led Growth (PLG) Sandbox & 'Mistakes/Fixes' Lab Builder",
        tagline="Productizes `visual-lab` into a B2B SaaS that turns any developer tool, API, or database repo into a live, animated, real-backend interactive demo & troubleshooting lab.",
        summary=(
            "Directly commercializes `Claude_Skills_Project/visual-lab` (already proven in `Kafka_Visual_Lab_Project` and `Business_Analyzer_Project/lab`): "
            "VisualLab Cloud connects to a DevTools or B2B API vendor's docs and GitHub repo, inventories every core feature and top Stack Overflow / GitHub "
            "issue anti-pattern, scaffolds an isolated Dockerized backend that runs each feature and 'Do It Wrong -> Reproduce Genuine Error -> Run Fix' "
            "scenario for real, and pairs it with an animated React/SSE topology UI."
        ),
        category="Developer PLG & Technical EdTech",
        naics_code="518210",
        business_archetype="VERTICAL_SAAS",
        target_metro="Chicago-Naperville-Elgin MSA (US-IL-16980) & San Francisco MSA (US-CA-41860)",
        pattern_ids=["PAT-04", "PAT-05"],
        referenced_skills=["visual-lab", "claude-skill-factory", "enterprise-fullstack-plugin"],
        referenced_projects=["Claude_Skills_Project", "Kafka_Visual_Lab_Project", "Business_Analyzer_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B"],
        mitigated_failure_modes=["FAIL_UNIT_ECON_CAC", "FAIL_CASH_BURN_RUNWAY"],
        s12=0.92,
        s60=0.64,
        initial_capex_usd=24_000,
        steady_state_ebitda_usd=640_000,
        annual_contract_value_usd=24_000,
        cac_usd=1_800,
        gross_margin_pct=88.0,
        annual_churn_pct=5.5,
        monthly_burn_usd=2_300,
        runway_months=24.0,
        founder_fit_score=100.0,
        acuteness_of_problem=(
            "Severe developer drop-off & documentation bounce rate: DevTools, database, and infrastructure startups spend $50,000+/month on developer marketing, "
            "only to have 92% of visitors bounce from static Markdown docs because spinning up a local cluster takes 45 minutes. Meanwhile, enterprise "
            "engineering bootcamps lack safe, real-backend environments that reproduce genuine production errors (like Kafka poison pills or DB lock timeouts)."
        ),
        ten_x_better_solution=(
            "10x higher developer activation and organic SEO capture: unlike static Swagger UIs or mocked Instruqt slideshows, VisualLab Cloud runs the "
            "real engine in an isolated container, streams live `DemoResult` telemetry (`commands`, `data`, `checks`, `elapsedMs`) over SSE, and includes a "
            "searchable '#pitfalls' catalog that reproduces exact production error strings—ranking #1 on Google/LLMs for high-intent error searches."
        ),
        usage_and_retention_metrics=(
            "Embedded on the customer's public `/lab` or `/playground` subdomain and used in 100% of sales engineering demos and enterprise onboarding cohorts; "
            "94% annual retention because it is the customer's top-converting PLG acquisition funnel."
        ),
        tam_and_growth_tailwinds=(
            "$4.4B TAM across 15,000+ DevTools/API vendors, cloud platforms, and Fortune 1000 internal developer enablement academies (replacing Instruqt, Katacoda, and static docs)."
        ),
        competition_and_defensible_edge=(
            "Instruqt charges $30k–$80k/yr and requires weeks of manual bash scripting with ugly terminal-only UIs; Mintlify/ReadMe only render static "
            "markdown text. VisualLab Cloud's moat is its automated `visual-lab` generator (`scaffold.sh` + `test-isolated.sh` + `security-check.sh`) that "
            "synthesizes animated node-flow topologies and genuine error reproductions automatically."
        ),
        why_customers_switch=(
            "DevRel and Growth leads switch immediately when they see a live VisualLab (`Kafka_Visual_Lab_Project`) convert 4x more developer signups "
            "than static Mintlify pages at a fraction of Instruqt's cost."
        ),
        cac_ltv_and_payback=(
            "CAC is $1,800 because every public VisualLab built for a customer or open-source tool (Kafka, Redis, Flink, Polars, RabbitMQ) carries a "
            "'Powered by VisualLab' badge—creating a viral PLG loop. At $24,000 ACV, 88% gross margin, and 5.5% churn, LTV is $384,000 (LTV:CAC = 213.3x) "
            "with a 1.0-month payback."
        ),
        nature_of_revenue=(
            "Recurring annual SaaS subscription ($2,000/mo per hosted interactive lab + automatic version-upgrade sync)."
        ),
        actual_paying_customers=(
            "VPs of Developer Relations, Heads of Product Marketing, and Engineering Enablement Directors at Series A–D infrastructure/API companies and enterprise tech academies."
        ),
        burn_rate_and_runway=(
            "$2,300/month burn on $24,000 initial capital; `visual-lab` templates, `scaffold.sh`, `test-isolated.sh`, and `security-check.sh` are already 100% built in `Claude_Skills_Project`!"
        ),
        unit_economics_scaling=(
            "88%+ gross margin: each lab runs in lightweight, sleep-on-idle containers with clamped visitor inputs and constant-time `X-Admin-Token` protection."
        ),
        fundraising_and_cap_table=(
            "100% founder-owned and bootstrapped via upfront annual DevTools PLG subscriptions; zero convertible debt or dilutive SAFE overhang."
        ),
        founder_product_fit=(
            "Perfect 100/100 founder fit: Cody Nicholson created `Claude_Skills_Project/visual-lab`, built `Kafka_Visual_Lab_Project` and `Business_Analyzer_Project/lab`, "
            "and has 7+ years as Lead Software Development Instructor at ThriveDX and Data Science Instructor at Northwestern University."
        ),
        pressure_and_pivot_playbook=(
            "Dual monetization: sell both to DevTools vendors as a PLG conversion engine AND to enterprise engineering organizations as an interactive internal onboarding academy."
        ),
        signal_inspiration="Claude_Skills_Project/visual-lab + Kafka_Visual_Lab_Project + ThriveDX/Northwestern Instructor background",
    ),
    make_idea(
        id="IDEA-018",
        slug="tetradforge-game-economy-monte-carlo",
        title="TetradForge — Playcentric Game Economy Monte-Carlo Simulator & Design-Smell Diagnostic Engine",
        tagline="Productizes `design-game` into an automated economy balancer, Beat Chart compiler, and pre-production risk auditor for game studios.",
        summary=(
            "Directly commercializes `Claude_Skills_Project/design-game` (`SKILL.md`, `four-books-framework.md`, `case-study-diagnostics.md`, "
            "`platform-architecture-guides.md`, and `validate_design_spec.py`) plus `Cameo_HoldEm_Project`'s probability simulation engine: "
            "TetradForge audits game design specs against Salen & Zimmerman's Cybernetic Loops, Fullerton's Resource Economy (Sources, Drains, Converters), "
            "Schell's Elemental Tetrad, and Rogers' Master Beat Chart—running 100,000 Monte-Carlo player economy simulations to catch runaway inflation "
            "and `Anthem`/`Diablo III`/`Concord` design smells before a studio writes a line of shader code."
        ),
        category="GameTech & Interactive Media Tools",
        naics_code="513210",
        business_archetype="VERTICAL_SAAS",
        target_metro="Seattle-Tacoma-Bellevue MSA (US-WA-42660) & Austin MSA (US-TX-12420)",
        pattern_ids=["PAT-04", "PAT-05", "PAT-08"],
        referenced_skills=["design-game", "visual-lab", "claude-skill-factory"],
        referenced_projects=["Claude_Skills_Project", "Cameo_HoldEm_Project", "Video_Game_Music_Generator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B"],
        mitigated_failure_modes=["FAIL_NO_MARKET_NEED", "FAIL_UNIT_ECON_CAC"],
        s12=0.90,
        s60=0.59,
        initial_capex_usd=26_000,
        steady_state_ebitda_usd=540_000,
        annual_contract_value_usd=14_400,
        cac_usd=1_400,
        gross_margin_pct=90.0,
        annual_churn_pct=6.5,
        monthly_burn_usd=2_200,
        runway_months=24.0,
        founder_fit_score=96.0,
        acuteness_of_problem=(
            "Existential studio risk: indie and AA/AAA game studios burn $500k to $50M+ building art and levels over 2–4 years, only to launch with "
            "broken progression math (invisible rubber-band scaling like *Anthem*, uncapped resource inflation with no sinks like *Diablo III* launch, "
            "or snowballed multiplayer runaway loops) that causes 'Mostly Negative' Steam reviews in 48 hours."
        ),
        ten_x_better_solution=(
            "10x faster economy balancing and pre-production validation: TetradForge takes a game's JSON economy tables and GDD, runs `validate_design_spec.py`, "
            "executes 100,000 simulated player runs across Rogers' Master Beat Chart, flags missing Negative Feedback Stabilizers or missing Resource Drains, "
            "and exports balanced JSON/CSV curves directly into Godot 4, Unity, or Unreal Engine 5."
        ),
        usage_and_retention_metrics=(
            "Used weekly from pre-production through live-ops seasonal balance patches; 93% retention across multi-year game development cycles."
        ),
        tam_and_growth_tailwinds=(
            "$2.8B TAM across 35,000+ indie/AA studios, mobile F2P publishers, and game design university programs worldwide."
        ),
        competition_and_defensible_edge=(
            "Machinations.io requires complex manual node-graph drawing with no theoretical design-smell diagnostics or platform engineering roadmap; "
            "spreadsheets break on non-linear roguelite/deckbuilder synergies. TetradForge's moat is its Four-Book theoretical diagnostic engine + "
            "automated Godot/Unity/UE5 data-table exporter."
        ),
        why_customers_switch=(
            "Game directors and systems designers switch when Excel economy sheets fail to predict a game-breaking currency exploit during closed playtesting."
        ),
        cac_ltv_and_payback=(
            "CAC is $1,400 via a free 'Steam GDD & Economy Smell Grader' web tool based on `case-study-diagnostics.md`. At $14,400 ACV ($1,200/mo studio tier), "
            "90% gross margin, and 6.5% churn, LTV is $199,384 (LTV:CAC = 142.4x) with a 1.3-month payback."
        ),
        nature_of_revenue=(
            "Recurring monthly/annual SaaS studio license ($300/mo Indie, $1,200/mo AA Studio, $3,500/mo Publisher Underwriting Tier)."
        ),
        actual_paying_customers=(
            "Systems Designers, Game Directors, Live-Ops Economists, and Indie Game Publishers (who use TetradForge to audit pitch decks before funding a studio)."
        ),
        burn_rate_and_runway=(
            "$2,200/month burn on $26,000 initial capital; `design-game` and `validate_design_spec.py` are already built in `Claude_Skills_Project`!"
        ),
        unit_economics_scaling=(
            "90%+ gross margin: Monte-Carlo economy simulations and `validate_design_spec.py` run deterministically in Python/WebAssembly."
        ),
        fundraising_and_cap_table=(
            "100% founder-owned; bootstrapped profitably via studio and game-publisher subscriptions."
        ),
        founder_product_fit=(
            "96/100 fit: Cody authored `Claude_Skills_Project/design-game` (Four-Books synthesis, `validate_design_spec.py`, `case-study-diagnostics.md`) "
            "and built `Cameo_HoldEm_Project`."
        ),
        pressure_and_pivot_playbook=(
            "High-ticket B2B pivot: sell TetradForge as a 'Pre-Funding Technical & Design Due-Diligence Suite' to game venture funds and publishers "
            "(Devolver, Hooded Horse, Kowloon Nights) evaluating 500+ game pitches a year."
        ),
        signal_inspiration="Claude_Skills_Project/design-game + Cameo_HoldEm_Project",
    ),
]

IDEAS_PACK_5.extend([
    make_idea(
        id="IDEA-019",
        slug="assetgate-3d-glb-music-pipeline",
        title="AssetGate 3D & AdaptiveStem — Automated Blender-to-GLB Production Validator & Dynamic Game Audio Compiler",
        tagline="Unites `Airship_Blender_Assets_Project` and `Video_Game_Music_Generator_Project` into an automated CI/CD asset & adaptive audio pipeline for 3D web/mobile games.",
        summary=(
            "Directly commercializes `Airship_Blender_Assets_Project` (`CLAUDE.md` Blender MCP rules, `validate_production.py`, `asset_manifest.json`) "
            "and `Video_Game_Music_Generator_Project` (JSON-driven multi-stem adaptive game soundtrack synthesis): AssetGate 3D acts as an automated "
            "quality gate between generative 3D tools (Hyper3D/Rodin, Meshy, PolyHaven, Blender) and production engines (Three.js, Godot, Unity)—auto-normalizing "
            "pivots, unwrapping UVs, enforcing `SM_`/`SK_` naming conventions, validating polygon/draw-call budgets, and pairing each level beat with "
            "procedurally synthesized, royalty-free adaptive audio stems."
        ),
        category="GameTech & Interactive Media Tools",
        naics_code="513210",
        business_archetype="VERTICAL_SAAS",
        target_metro="Austin-Round Rock MSA (US-TX-12420) & Seattle MSA (US-WA-42660)",
        pattern_ids=["PAT-04", "PAT-08"],
        referenced_skills=["design-game", "claude-skill-factory", "enterprise-fullstack-plugin"],
        referenced_projects=["Airship_Blender_Assets_Project", "Video_Game_Music_Generator_Project", "Claude_Skills_Project"],
        causal_drivers=["SUCC_RECURRING_B2B"],
        mitigated_failure_modes=["FAIL_UNIT_ECON_CAC", "FAIL_CASH_BURN_RUNWAY"],
        s12=0.89,
        s60=0.58,
        initial_capex_usd=28_000,
        steady_state_ebitda_usd=520_000,
        annual_contract_value_usd=18_000,
        cac_usd=1_600,
        gross_margin_pct=88.0,
        annual_churn_pct=6.5,
        monthly_burn_usd=2_300,
        runway_months=24.0,
        founder_fit_score=97.0,
        acuteness_of_problem=(
            "Massive technical-art bottleneck: AI 3D generators (Rodin, Meshy, Tripo) output messy, un-optimized meshes with broken UV maps, off-center "
            "pivots, and 200k+ triangles that crash mobile/web WebGL2 budgets (<5 MB initial load in `design-game/SKILL.md`), forcing technical artists "
            "to spend hours manually cleaning every `.glb` in Blender."
        ),
        ten_x_better_solution=(
            "10x faster asset-to-engine pipeline: AssetGate runs headless Blender + `validate_production.py` automatically on every asset commit or MCP "
            "generation, enforcing `SM_<Category>_<Name>.glb` / `SK_<Name>.glb` schemas, decimating LODs, baking PBR texture atlases, and generating "
            "adaptive loopable music stems (`Video_Game_Music_Generator_Project`) matched to Rogers' Beat Chart intensity curve (1–10)."
        ),
        usage_and_retention_metrics=(
            "Triggered on every 3D asset import and build in CI/CD; 92% annual studio retention because it replaces manual technical-artist QA."
        ),
        tam_and_growth_tailwinds=(
            "$3.1B TAM across 3D web/mobile game studios, e-commerce 3D product configurators, spatial computing/XR teams (DePaul VR Club roots), and digital-twin builders."
        ),
        competition_and_defensible_edge=(
            "Raw 3D AI generators (Meshy, Rodin) stop at mesh generation and fail production engine checks; Simplygon costs $30k+/yr for enterprise-only "
            "decimation without Blender MCP orchestration or adaptive audio synthesis. AssetGate's edge is its deterministic `validate_production.py` + headless Blender MCP pipeline."
        ),
        why_customers_switch=(
            "Studios switch after a single un-optimized 50MB `.glb` asset ships to production and tanks mobile/browser framerates to 12 FPS."
        ),
        cac_ltv_and_payback=(
            "CAC is $1,600 via a free 'GLB Web/Mobile Production Readiness Linter' and Blender MCP plugin. At $18,000 ACV, 88% gross margin, and 6.5% churn, "
            "LTV is $243,692 (LTV:CAC = 152.3x) with a 1.2-month payback."
        ),
        nature_of_revenue=(
            "Recurring B2B SaaS studio subscription ($1,500/mo) + CI/CD runner minutes."
        ),
        actual_paying_customers=(
            "Technical Art Directors, WebGL/Three.js Agencies (`enterprise-fullstack-plugin/skills/data-viz/references/three.md`), and Mobile/Indie Game Studios."
        ),
        burn_rate_and_runway=(
            "$2,300/month burn on $28,000 initial capital; both `Airship_Blender_Assets_Project` and `Video_Game_Music_Generator_Project` already exist in the workspace!"
        ),
        unit_economics_scaling=(
            "Headless Blender mesh optimization and JSON-to-WAV audio synthesis run deterministically on CPU/GPU workers with zero frontier LLM token burn."
        ),
        fundraising_and_cap_table=(
            "100% founder-owned; bootstrapped via self-serve studio plans."
        ),
        founder_product_fit=(
            "97/100 fit: Cody built both `Airship_Blender_Assets_Project` (`tools/validate_production.py`, Blender MCP rules) and `Video_Game_Music_Generator_Project` "
            "(7 multi-stem orchestral/game tracks) and has a background in DePaul's Virtual Reality Club and Three.js (`data-viz`)."
        ),
        pressure_and_pivot_playbook=(
            "If indie game studio budgets tighten, sell the exact same automated `.glb` optimization pipeline to B2B e-commerce furniture/industrial "
            "retailers building Shopify/Three.js 3D product viewers."
        ),
        signal_inspiration="Airship_Blender_Assets_Project + Video_Game_Music_Generator_Project + design-game",
    ),
    make_idea(
        id="IDEA-020",
        slug="careanchor-specialty-eldercare-retention-os",
        title="CareAnchor AI — Private-Pay Specialty Elder Care Caregiver Retention & Instant Shift-Fill OS",
        tagline="Solves the #1 KPI in NAICS `624120` (caregiver retention & open-shift recovery) for private-pay memory and post-acute home care agencies.",
        summary=(
            "Directly executes `Business_Analyzer_Project`'s NAICS `624120` playbook ('Focus on private-pay specialty care (memory, post-acute) where "
            "incumbents are thin; caregiver retention is the core KPI', which has a 58.0% 5-year survival rate and the lowest earnings volatility σ=0.18 "
            "in the entire 21-industry catalog): CareAnchor AI predicts caregiver burnout/churn 30 days in advance from shift-cancellation and commute patterns, "
            "automates SMS/voice instant shift backfilling in under 4 minutes, and generates family daily care-digest reports that justify premium private-pay rates."
        ),
        category="Healthcare FinTech & Ops",
        naics_code="624120",
        business_archetype="VERTICAL_SAAS",
        target_metro="Minneapolis-St. Paul MSA (US-MN-33460) & Chicago MSA (US-IL-16980)",
        pattern_ids=["PAT-01", "PAT-02", "PAT-03"],
        referenced_skills=["software-intake-planner", "enterprise-fullstack-plugin"],
        referenced_projects=["Business_Analyzer_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_RENT_LABOR_SQUEEZE", "FAIL_NO_MARKET_NEED"],
        s12=0.94,
        s60=0.68,
        initial_capex_usd=30_000,
        steady_state_ebitda_usd=610_000,
        annual_contract_value_usd=21_600,
        cac_usd=2_100,
        gross_margin_pct=88.0,
        annual_churn_pct=4.5,
        monthly_burn_usd=2_600,
        runway_months=24.0,
        founder_fit_score=91.0,
        acuteness_of_problem=(
            "Severe caregiver turnover crisis: home care and memory-care agencies suffer 65–80% annual caregiver turnover, costing $2,600 per lost caregiver "
            "in recruiting/onboarding and forcing agencies to turn away high-margin ($40–$55/hr) private-pay dementia/post-acute clients when a 6 a.m. "
            "callout leaves a shift uncovered."
        ),
        ten_x_better_solution=(
            "10x faster callout recovery (3 minutes via ranked SMS/voice matching vs. 2 hours of frantic scheduler phone calls) plus actuarial Cox PH "
            "caregiver survival modeling (adapted directly from `Business_Analyzer_Project/worker/intel/forecasting.py`!) that flags at-risk caregivers "
            "when commute radius or schedule variance spikes."
        ),
        usage_and_retention_metrics=(
            "Used 24/7 by agency schedulers and every shift by caregivers via zero-app SMS/WhatsApp check-in; 96% annual retention because it protects "
            "both caregiver headcount and private-pay family billing."
        ),
        tam_and_growth_tailwinds=(
            "$4.7B TAM across 38,000+ US non-medical and post-acute home care agencies; unstoppable demographic tailwind from the Baby Boomer 'Silver Tsunami' "
            "and hospital-to-home post-acute discharge mandates."
        ),
        competition_and_defensible_edge=(
            "Legacy EVV/scheduling tools (AxisCare, WellSky, ClearCare) are clunky compliance forms that caregivers hate and lack predictive Cox PH "
            "churn modeling or autonomous SMS shift-bidding. CareAnchor sits alongside or replaces legacy schedulers with zero app-install friction."
        ),
        why_customers_switch=(
            "Agency owners switch when they lose a $12,000/month private-pay memory-care family contract because a morning caregiver no-showed and "
            "the scheduler couldn't fill the shift in time."
        ),
        cac_ltv_and_payback=(
            "CAC is $2,100 via a free 'Agency Caregiver Churn Cost & Commute-Radius Audit' tool. At $21,600 ACV ($1,800/mo per agency location), "
            "88% gross margin, and 4.5% churn, LTV is $422,400 (LTV:CAC = 201.1x) with a 1.3-month payback."
        ),
        nature_of_revenue=(
            "Sticky recurring monthly/annual B2B SaaS ($1,800/mo per agency branch)."
        ),
        actual_paying_customers=(
            "Owners and Operations Directors of private-pay home care, memory care, and post-acute staffing agencies in the Midwest, Sunbelt, and Coastal metros."
        ),
        burn_rate_and_runway=(
            "$2,600/month burn on $30,000 initial capital; cash-flow positive with 2 agency customers."
        ),
        unit_economics_scaling=(
            "88%+ gross margin: Cox PH caregiver survival scoring (`lifelines` math from `Business_Analyzer_Project`) and PostGIS commute-distance matching "
            "run deterministically on CPU."
        ),
        fundraising_and_cap_table=(
            "100% founder-owned and bootstrapped to $1M+ ARR via recurring home-care agency subscriptions; clean cap table with zero debt."
        ),
        founder_product_fit=(
            "91/100 fit: directly repurposes `Business_Analyzer_Project`'s Cox proportional-hazards survival engine (`forecasting.py`) and PostGIS "
            "radius math (`geo.py`) to solve caregiver survival and shift matching in NAICS `624120`."
        ),
        pressure_and_pivot_playbook=(
            "Can expand horizontally from private-pay elder care (`624120`) to commercial janitorial route staffing (`561720`) and outpatient clinic nurse staffing (`621498`)."
        ),
        signal_inspiration="Business_Analyzer_Project NAICS 624120 (lowest volatility sigma=0.18, 58% survival) + Cox PH survival transfer",
    ),
])
