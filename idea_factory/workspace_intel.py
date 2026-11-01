"""Structured intelligence extracted from Claude_Skills_Project, Business_Analyzer_Project, and sibling workspace repos."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from . import config


@dataclass(frozen=True)
class SkillAsset:
    name: str
    repo_path: str
    core_capability: str
    productization_angle: str


@dataclass(frozen=True)
class IndustryBenchmark:
    naics: str
    sector: str
    subsector: str
    archetype: str
    capex_usd: float
    ebitda_to_capex: float
    volatility: float
    lgd_pct: float
    base_survival_5yr: float
    recurring_b2b: bool
    playbook: str


CLAUDE_SKILLS_CATALOG: list[SkillAsset] = [
    SkillAsset(
        name="software-intake-planner",
        repo_path="Claude_Skills_Project/software-intake-planner/SKILL.md",
        core_capability="3-round Socratic discovery, repo reconnaissance, hard business invariant (INV-n) & NFR extraction, Unknowns register ([UNKNOWN: UNK-n]), and deterministic spec-to-plan traceability via validate_intake.py.",
        productization_angle="Automated Pre-Sales Scoping, Legacy Modernization Blueprinting, and SOC2/Architectural Spec Governance.",
    ),
    SkillAsset(
        name="visual-lab",
        repo_path="Claude_Skills_Project/visual-lab/SKILL.md",
        core_capability="Dockerized real-backend feature runners paired with animated React request-flow topologies, live SSE telemetry, and real reproduction of 'Mistakes, Errors & Fixes' anti-patterns.",
        productization_angle="Interactive Customer Onboarding Sandboxes, PLG Developer Docs-as-Labs, and Enterprise Cloud/Distributed Systems Training.",
    ),
    SkillAsset(
        name="design-game",
        repo_path="Claude_Skills_Project/design-game/SKILL.md",
        core_capability="Four-Pillar playcentric game architecture (Salen & Zimmerman, Fullerton, Schell, Rogers), Cybernetic Negative Feedback Stabilizers, Master Beat Charts, and Case-Study Design Smell Diagnostics.",
        productization_angle="Automated Game Economy & Live-Ops Balancing Auditor, Playtest Telemetry Analyzer, and Gamified B2B Training Simulators.",
    ),
    SkillAsset(
        name="claude-skill-factory",
        repo_path="Claude_Skills_Project/claude-skill-factory/SKILL.md",
        core_capability="Primitive routing gate (CLAUDE.md vs. Hook vs. Subagent vs. Skill), 3-tier progressive token disclosure, least-privilege tool scoping, and deterministic self-verification loops (validate_skill.py).",
        productization_angle="Enterprise AI Agent Governance, MCP & Skill Security Firewalls, and Token-Cost FinOps Routers.",
    ),
    SkillAsset(
        name="enterprise-fullstack-plugin",
        repo_path="Claude_Skills_Project/enterprise-fullstack-plugin/README.md",
        core_capability="7 specialized role agents (architect, backend-engineer, frontend-engineer, data-engineer, platform-engineer, test-engineer, code-reviewer) + 13 domain skills (event-streaming, db-migrations, etl-pipeline, search-indexing, cloud-deploy, workflow-automation, etc.) + Flyway protection hooks.",
        productization_angle="Autonomous Legacy Monolith-to-Microservice Modernization, Self-Healing Kafka/DLT AIOps, and Automated Contract Testing.",
    ),
]

BUSINESS_ANALYZER_INDUSTRIES: dict[str, IndustryBenchmark] = {
    "238220": IndustryBenchmark(
        "238220", "Plumbing, Heating & Air-Conditioning Contractors", "Commercial HVAC & Refrigeration Service",
        "SMB_MAIN_STREET", 185_000, 0.62, 0.22, 0.45, 0.56, True,
        "Sell multi-year preventive-maintenance contracts to commercial and industrial sites; keep install work as upsell.",
    ),
    "493120": IndustryBenchmark(
        "493120", "Refrigerated Warehousing & Storage", "Cold-Chain Logistics & Micro-Fulfillment",
        "SMB_MAIN_STREET", 240_000, 0.45, 0.25, 0.40, 0.54, True,
        "Anchor on contracted food or pharma shippers; automate temperature compliance and multi-facility inventory.",
    ),
    "561720": IndustryBenchmark(
        "561720", "Janitorial Services", "Automated B2B Facility Services",
        "SMB_MAIN_STREET", 60_000, 0.90, 0.20, 0.60, 0.50, True,
        "Target multi-site commercial accounts with route density; automate scheduling and QA to protect labor margins.",
    ),
    "238210": IndustryBenchmark(
        "238210", "Electrical Contractors", "Electrical & Smart-Grid Installation",
        "SMB_MAIN_STREET", 140_000, 0.68, 0.24, 0.48, 0.55, True,
        "Specialize in EV-charger, battery and commercial panel-upgrade work; automate utility rebate and permit packets.",
    ),
    "562910": IndustryBenchmark(
        "562910", "Remediation Services", "Water & Mold Mitigation",
        "SMB_MAIN_STREET", 120_000, 0.70, 0.28, 0.50, 0.52, True,
        "Get on insurer and property-manager preferred-vendor lists; automate Xactimate scope documentation to accelerate 60-90 day insurer payouts.",
    ),
    "621498": IndustryBenchmark(
        "621498", "All Other Outpatient Care Centers", "Ambulatory Surgical & Specialty Clinic Support",
        "SMB_MAIN_STREET", 260_000, 0.42, 0.20, 0.42, 0.60, True,
        "Partner with physician groups; automate prior-authorization appeals, payer credentialing, and surgical coding.",
    ),
    "541611": IndustryBenchmark(
        "541611", "Management Consulting Services", "Productized Fractional B2B Advisory",
        "SMB_MAIN_STREET", 45_000, 1.60, 0.30, 0.70, 0.50, True,
        "Productize a narrow compliance, actuarial, or finance offering on monthly retainers; avoid one-off projects.",
    ),
    "541512": IndustryBenchmark(
        "541512", "Computer Systems Design Services", "Cybersecurity Auditing & Continuous Compliance",
        "SMB_MAIN_STREET", 70_000, 1.15, 0.28, 0.65, 0.53, True,
        "Sell SOC 2 / ISO 27001 / AI governance readiness plus continuous monitoring retainers to mid-market firms.",
    ),
    "624120": IndustryBenchmark(
        "624120", "Services for the Elderly & Persons with Disabilities", "Specialty Elder Care Operations",
        "SMB_MAIN_STREET", 90_000, 0.55, 0.18, 0.55, 0.58, True,
        "Focus on private-pay specialty care and caregiver retention/shift-fill automation.",
    ),
    "513210": IndustryBenchmark(
        "513210", "Software Publishers", "Vertical B2B SaaS & AI Agents",
        "HIGH_GROWTH_STARTUP", 75_000, 1.45, 0.42, 0.55, 0.44, True,
        "Sell into one regulated vertical (supply chain, legal, healthcare, trades) with measurable ROI; reach $1M ARR with a micro-team before scaling GTM.",
    ),
    "518210": IndustryBenchmark(
        "518210", "Computing Infrastructure & Data Processing", "Developer & Agent Infrastructure",
        "HIGH_GROWTH_STARTUP", 85_000, 1.35, 0.45, 0.58, 0.42, True,
        "Lead with open-source or interactive visual-lab adoption and convert usage to enterprise contracts; keep cloud COGS under 20%.",
    ),
    "522320": IndustryBenchmark(
        "522320", "Financial Transactions Processing", "Embedded Finance & B2B Payments FinTech",
        "HIGH_GROWTH_STARTUP", 95_000, 1.30, 0.46, 0.60, 0.40, True,
        "Offer working-capital, ledger reconciliation, or draw payments inside an existing vertical workflow.",
    ),
    "541715": IndustryBenchmark(
        "541715", "R&D in Physical & Engineering Sciences", "Industrial & ClimateTech Telemetry Software",
        "HIGH_GROWTH_STARTUP", 110_000, 1.15, 0.48, 0.62, 0.39, True,
        "Pair industrial/cold-chain sensors with recurring compliance and energy-arbitrage software.",
    ),
    "531390": IndustryBenchmark(
        "531390", "Other Real Estate Activities", "PropTech & Construction FinTech",
        "HIGH_GROWTH_STARTUP", 65_000, 1.40, 0.40, 0.55, 0.45, True,
        "Automate painful builder, lender, or property-manager workflows (draw management, lien waivers, permitting, CAM audits).",
    ),
    "488510": IndustryBenchmark(
        "488510", "Freight Transportation Arrangement", "Supply-Chain & Cross-Border Freight Automation",
        "HIGH_GROWTH_STARTUP", 70_000, 1.48, 0.40, 0.52, 0.46, True,
        "Automate freight exception recovery, detention billing, and cross-border US-Mexico-Canada customs brokerage.",
    ),
}

CAUSAL_FACTORS: dict[str, str] = {
    "SUCC_RECURRING_B2B": "Multi-year or sticky monthly B2B contracts with low churn and predictable cash conversion",
    "SUCC_LOCAL_OLIGOPOLY": "Undersupplied vertical or regional niche with fragmented, legacy incumbents",
    "FAIL_NO_MARKET_NEED": "Insufficient acute buyer pain; mitigated by requiring <60-day hard-dollar ROI payback",
    "FAIL_CASH_BURN_RUNWAY": "Excessive burn before PMF; mitigated by micro-team agentic execution & <$5k/mo initial burn",
    "FAIL_UNIT_ECON_CAC": "CAC or LLM token COGS exceeding LTV; mitigated by PLG visual labs & deterministic model routing",
    "FAIL_PREMATURE_SCALING": "Hiring GTM/ops before repeatable unit economics; mitigated by staying lean until $1M ARR",
    "FAIL_RENT_LABOR_SQUEEZE": "Margin compression from occupancy or manual service labor; mitigated by 100% autonomous workflows",
}

WORKSPACE_PROJECTS: dict[str, str] = {
    "Business_Analyzer_Project": "Actuarial SMB & Startup Survival Intelligence Engine (Cox PH, LightGBM quantiles, Israelsen ROI, PostGIS, TimescaleDB, pgvector, SEC Form D / BLS QCEW / Census BDS / CourtListener / HN ETL).",
    "Claude_Skills_Project": "Modular Claude Code Skills & Enterprise Full-Stack Multi-Agent Plugin (software-intake-planner, visual-lab, design-game, claude-skill-factory, enterprise-fullstack-plugin).",
    "Kafka_Visual_Lab_Project": "Spring Boot 3.3 + Apache Kafka 3.8 (KRaft) + React/SSE interactive topology demonstrating keyed ordering, non-blocking retry topics, Dead Letter Topics (DLT), and offset replay.",
    "Rixus_RE_Project": "Go 1.22 + PostgreSQL (pgx/v5) + React 19 + Three-Tier Docker Network real estate intelligence platform.",
    "Accounting_Backend_API_Project": "Java/Spring Boot/Gradle enterprise accounting ledger backend with Karate contract tests and Jacoco coverage.",
    "Resume_Creator_Project": "TypeScript + pdf-lib + fontkit + sharp deterministic document/PDF layout compiler.",
    "Airship_Blender_Assets_Project": "Automated 3D asset production pipeline with Blender MCP, UV/pivot normalization, and validate_production.py.",
    "Video_Game_Music_Generator_Project": "Programmatic JSON-driven multi-track adaptive game music synthesis engine.",
    "Cameo_HoldEm_Project": "Interactive React/TypeScript probability & state-machine card game engine.",
}

FOUNDER_EDGE_SUMMARY = (
    "Cody Nicholson is a Chicago-based Lead Software Engineer (Ahold Delhaize USA; previously Senior Software "
    "Engineer at Peapod Digital Labs for 4+ years and Data Engineer at Arity/Allstate) and Lead Software/Data "
    "Science Instructor (ThriveDX, Northwestern University). He architected high-throughput Java/Spring Boot/Kafka/"
    "Postgres/Redis/Azure order-processing ETL pipelines fulfilling 3,000,000+ ecommerce orders annually across "
    "25 facilities, built self-service on-call tooling that reduced production incident volume by 73%, and created "
    "both the actuarial `Business_Analyzer_Project` and the multi-agent `Claude_Skills_Project`."
)


def inspect_live_workspace() -> dict[str, Any]:
    """Inspect sibling workspace directories on disk when accessible."""
    skills_found = [s.name for s in CLAUDE_SKILLS_CATALOG]
    if config.CLAUDE_SKILLS_DIR.exists():
        try:
            skills_found = sorted(
                p.name for p in config.CLAUDE_SKILLS_DIR.iterdir()
                if p.is_dir() and not p.name.startswith(".")
            )
        except OSError:
            pass
    return {
        "claude_skills_dir": str(config.CLAUDE_SKILLS_DIR),
        "business_analyzer_dir": str(config.BUSINESS_ANALYZER_DIR),
        "skills_count": len(skills_found),
        "skills": skills_found,
        "industries_tracked": len(BUSINESS_ANALYZER_INDUSTRIES),
        "workspace_projects": list(WORKSPACE_PROJECTS.keys()),
    }

