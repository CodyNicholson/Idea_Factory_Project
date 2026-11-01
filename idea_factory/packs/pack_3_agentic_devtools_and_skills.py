"""Pack 3: Agentic Developer Tools, Enterprise Skill Governance, and Legacy Modernization."""
from __future__ import annotations

from ..models import ProductIdea
from ..seed_ideas import make_idea

IDEAS_PACK_3: list[ProductIdea] = [
    make_idea(
        id="IDEA-009",
        slug="intakespec-deterministic-architecture-compiler",
        title="IntakeSpec AI — Deterministic Requirements, Business Invariant & Migration Parity Compiler",
        tagline="Productizes `software-intake-planner` into a SaaS governance gate that turns messy PRDs and legacy repos into verified specs, vertical-slice plans, and concurrency tests.",
        summary=(
            "Directly commercializes `Claude_Skills_Project/software-intake-planner`: IntakeSpec AI connects to a team's GitHub/GitLab repository, Jira, "
            "and Notion, executes automated Track A (Greenfield), Track B (Brownfield), or Track C (Legacy Migration) codebase reconnaissance, conducts "
            "a structured 3-round Socratic discovery interview, logs unresolved decisions in an explicit `[UNKNOWN: UNK-n]` register, and runs deterministic "
            "traceability validation (`validate_intake.py`) so no AI agent or engineer writes code before hard business invariants (`INV-n`) are locked."
        ),
        category="Agentic DevTools & Governance",
        naics_code="513210",
        business_archetype="VERTICAL_SAAS",
        target_metro="Chicago-Naperville-Elgin MSA (US-IL-16980) & San Francisco MSA (US-CA-41860)",
        pattern_ids=["PAT-04", "PAT-05"],
        referenced_skills=["software-intake-planner", "claude-skill-factory", "enterprise-fullstack-plugin"],
        referenced_projects=["Claude_Skills_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B"],
        mitigated_failure_modes=["FAIL_UNIT_ECON_CAC", "FAIL_CASH_BURN_RUNWAY", "FAIL_PREMATURE_SCALING"],
        s12=0.92,
        s60=0.63,
        initial_capex_usd=25_000,
        steady_state_ebitda_usd=650_000,
        annual_contract_value_usd=24_000,
        cac_usd=2_100,
        gross_margin_pct=89.0,
        annual_churn_pct=5.5,
        monthly_burn_usd=2_400,
        runway_months=24.0,
        founder_fit_score=99.0,
        acuteness_of_problem=(
            "The #1 failure mode of AI-assisted software engineering in 2025–2026: coding agents (Claude Code, Cursor, Copilot) generate thousands of lines "
            "of plausible code from vague prompts, silently inventing fake NFRs ('500 req/s'), omitting idempotency keys on payment/inventory mutations, "
            "and breaking legacy migration parity—causing millions in production rework and broken client fixed-bid contracts."
        ),
        ten_x_better_solution=(
            "10x reduction in architectural rework: unlike generic PRD chat templates, IntakeSpec AI scans the actual repo first (`package.json`, `pom.xml`, "
            "`docker-compose.yml`, Flyway migrations), forces explicit non-goals, enumerates hard invariants (`INV-n` with required concurrency tests), "
            "rejects vague `TBD`/`TODO` placeholders via deterministic AST/regex checks (`validate_intake.py`), and blocks milestones whose `UNK-n` dependencies are open."
        ),
        usage_and_retention_metrics=(
            "Embedded directly as a mandatory GitHub Actions / GitLab CI pre-implementation gate for every epic and client statement of work (SOW). "
            "94% annual retention with strong seat expansion across Product, Architecture, and Engineering."
        ),
        tam_and_growth_tailwinds=(
            "$7.5B TAM across 60,000+ software consultancies, system integrators, and enterprise engineering teams adopting AI coding agents who desperately "
            "need spec-driven development (SDD) guardrails."
        ),
        competition_and_defensible_edge=(
            "Linear, Jira, and Notion AI summarize text but have zero deterministic traceability validation between `US-n`/`INV-n`/`NFR-n` requirements and "
            "vertical-slice milestones (`M0..Mn`). IntakeSpec's moat is its deterministic validator engine + Track A/B/C industry probe libraries."
        ),
        why_customers_switch=(
            "Engineering leaders and software agency partners switch after a single under-scoped project or hallucinated AI migration blows their margin "
            "or causes a double-charge/tenant-leak outage in production."
        ),
        cac_ltv_and_payback=(
            "CAC is $2,100 via open-sourcing the CLI checker (`validate_intake.py`) and offering a free 'PRD & Repo Risk Audit' GitHub App. "
            "At $24,000 ACV, 89% gross margin, and 5.5% churn, LTV is $388,363 (LTV:CAC = 184.9x) with a 1.2-month payback."
        ),
        nature_of_revenue=(
            "Sticky recurring B2B SaaS subscription ($2,000/month per engineering organization or consultancy practice)."
        ),
        actual_paying_customers=(
            "CTOs, VPs of Engineering, Principal Architects, and Managing Partners at custom software agencies and enterprise modernization teams."
        ),
        burn_rate_and_runway=(
            "$2,400/month burn on $25,000 initial capital; core skill, templates, and `validate_intake.py` are already 100% built in `Claude_Skills_Project`!"
        ),
        unit_economics_scaling=(
            "89%+ gross margin: deterministic validation (`validate_intake.py`) and repo tree scanning cost $0.00 in tokens; LLM calls are bounded to 3 structured rounds per feature."
        ),
        fundraising_and_cap_table=(
            "100% bootstrapped; near-zero CapEx because the core product already exists in `/Users/codynicholson/workspace/Claude_Skills_Project/software-intake-planner`."
        ),
        founder_product_fit=(
            "99/100 founder fit: Cody Nicholson designed and built `software-intake-planner` (`SKILL.md`, `core-intake-checklist.md`, Tracks A/B/C, "
            "`validate_intake.py`) and leads enterprise architecture strategy at Ahold Delhaize USA."
        ),
        pressure_and_pivot_playbook=(
            "If self-serve SaaS teams want IDE-native execution, package IntakeSpec as a paid Claude Code / Cursor MCP Server + GitHub Action bundle."
        ),
        signal_inspiration="Claude_Skills_Project/software-intake-planner (already built and validated in workspace)",
    ),
    make_idea(
        id="IDEA-010",
        slug="skillshield-mcp-governance-finops",
        title="SkillShield — Enterprise Claude Skill, Subagent & MCP Security Firewall + Token FinOps Optimizer",
        tagline="Audits, hardens, and token-optimizes `.claude/skills/`, hooks, and MCP servers across enterprise engineering teams.",
        summary=(
            "Directly productizes `Claude_Skills_Project/claude-skill-factory`: SkillShield provides CISOs and Platform Engineering teams with an automated "
            "registry, CI/CD security scanner (`validate_skill.py`), deterministic `PreToolUse` hook synthesizer, and 3-Tier Progressive Disclosure "
            "refactoring engine that cuts enterprise Claude/Cursor context token burn by 55% while blocking unbounded `Bash` or secret-exfiltration risks."
        ),
        category="Agentic DevTools & Governance",
        naics_code="541512",
        business_archetype="VERTICAL_SAAS",
        target_metro="Chicago-Naperville-Elgin MSA (US-IL-16980)",
        pattern_ids=["PAT-02", "PAT-04", "PAT-05"],
        referenced_skills=["claude-skill-factory", "enterprise-fullstack-plugin"],
        referenced_projects=["Claude_Skills_Project", "Business_Analyzer_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_UNIT_ECON_CAC", "FAIL_CASH_BURN_RUNWAY"],
        s12=0.92,
        s60=0.64,
        initial_capex_usd=28_000,
        steady_state_ebitda_usd=660_000,
        annual_contract_value_usd=30_000,
        cac_usd=2_600,
        gross_margin_pct=91.0,
        annual_churn_pct=5.0,
        monthly_burn_usd=2_500,
        runway_months=24.0,
        founder_fit_score=99.0,
        acuteness_of_problem=(
            "Urgent CISO & FinOps crisis: enterprises adopting Claude Code, Cursor, and MCP servers have hundreds of developers checking bloated "
            "2,000-line `CLAUDE.md` files and unvetted skills with `allowed-tools: Bash` (unrestricted shell execution) into repos. This causes two "
            "acute pains: (1) probabilistic prompt-injection / destructive migration edits, and (2) $20,000+/month in wasted context-window token burn."
        ),
        ten_x_better_solution=(
            "10x safer and 55% cheaper agent operations: SkillShield automatically runs `claude-skill-factory`'s Primitive Routing Gate—splitting bloated "
            "`CLAUDE.md` files into 3-tier progressive disclosure skills (`SKILL.md` <500 lines + 1-hop `references/`), scoping `allowed-tools` to least privilege, "
            "adding `disable-model-invocation: true` on deploy/reset skills, and generating deterministic exit-code-2 `PreToolUse` hooks (`protect-migrations.sh`) for zero-exception rules."
        ),
        usage_and_retention_metrics=(
            "Runs on every PR touching `.claude/`, `.cursor/`, `CLAUDE.md`, or `mcp.json`; 96% annual retention because it is both a security compliance "
            "control and a FinOps cost-reducer that pays for itself in saved Anthropic/OpenAI API bills."
        ),
        tam_and_growth_tailwinds=(
            "$4.6B TAM in AI Agent Security, Governance, and Token FinOps (NAICS `541512`); explosive 40%+ YoY growth as enterprises standardize on "
            "Claude Code, Antigravity, and Model Context Protocol (MCP)."
        ),
        competition_and_defensible_edge=(
            "Traditional SAST tools (Snyk,Checkmarx) scan Python/JS ASTs but are blind to probabilistic evasion in `SKILL.md`, nested reference chains, "
            "and MCP tool-permission escalation. SkillShield's moat is `claude-skill-factory`'s deterministic rubric (`patterns-and-rubric.md` + `validate_skill.py`)."
        ),
        why_customers_switch=(
            "CISOs and VPs of Platform switch immediately when an autonomous coding agent accidentally modifies a committed Flyway migration, leaks a `.env` secret, "
            "or blows through the team's monthly Anthropic enterprise token budget in 10 days."
        ),
        cac_ltv_and_payback=(
            "CAC is $2,600 via a free 'CLAUDE.md & Skill Security/Token Grader' web tool and GitHub Action. At $30,000 ACV, 91% gross margin, and 5% churn, "
            "LTV is $546,000 (LTV:CAC = 210.0x) with a 1.1-month payback."
        ),
        nature_of_revenue=(
            "Annual B2B subscription ($2,500/mo per enterprise organization) + optional continuous compliance certification badge."
        ),
        actual_paying_customers=(
            "CISOs, Heads of AI Platform, DevSecOps Directors, and Staff Engineers at mid-market and Fortune 1000 companies deploying Claude Code and MCP."
        ),
        burn_rate_and_runway=(
            "$2,500/month burn on $28,000 initial capital; `validate_skill.py` and `patterns-and-rubric.md` are already built in `Claude_Skills_Project`."
        ),
        unit_economics_scaling=(
            "91% gross margin: static frontmatter/permission/hook validation is 100% deterministic Python with zero per-scan LLM cost."
        ),
        fundraising_and_cap_table=(
            "Bootstrapped to $1M+ ARR with 100% founder equity; zero debt."
        ),
        founder_product_fit=(
            "99/100 fit: Cody authored `claude-skill-factory` and `enterprise-fullstack-plugin` (including `protect-migrations.sh` and `format-file.sh` hooks)."
        ),
        pressure_and_pivot_playbook=(
            "As new agent standards emerge (Antigravity skills, Cursor rules, OpenAI agents), SkillShield's AST/frontmatter transpiler cross-compiles "
            "one canonical skill package across all agent runtimes."
        ),
        signal_inspiration="Claude_Skills_Project/claude-skill-factory + enterprise-fullstack-plugin hooks",
    ),
]

IDEAS_PACK_3.extend([
    make_idea(
        id="IDEA-011",
        slug="stranglerfig-ai-legacy-spring-modernizer",
        title="StranglerFig AI — Multi-Agent Legacy Java/Monolith Decoupling & Karate Contract-Test Engine",
        tagline="Extracts bounded microservices from legacy Java/Spring/DB monoliths with automated Karate contract parity and Flyway expand-migrate-contract safety.",
        summary=(
            "Synthesizes Cody's Lead Software Engineer role at Ahold Delhaize USA ('Spearheaded core software modernization by decoupling legacy systems'), "
            "`Claude_Skills_Project/enterprise-fullstack-plugin` (7 role agents), `software-intake-planner/references/track-c-migration.md`, and "
            "`Karate_SpringBoot_Demo_Project` / `Accounting_Backend_API_Project`: StranglerFig AI maps legacy monolith call graphs, generates Karate "
            "black-box API parity tests first, scaffolds the target Spring Boot 3 / Postgres / Kafka outbox microservice, and enforces zero-downtime "
            "cutover with automated shadow-traffic diffing."
        ),
        category="Agentic DevTools & Governance",
        naics_code="541512",
        business_archetype="AI_NATIVE_SERVICE",
        target_metro="Chicago-Naperville-Elgin MSA (US-IL-16980)",
        pattern_ids=["PAT-02", "PAT-04", "PAT-06"],
        referenced_skills=["enterprise-fullstack-plugin", "software-intake-planner", "claude-skill-factory"],
        referenced_projects=["Claude_Skills_Project", "Accounting_Backend_API_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_NO_MARKET_NEED", "FAIL_PREMATURE_SCALING"],
        s12=0.91,
        s60=0.62,
        initial_capex_usd=38_000,
        steady_state_ebitda_usd=720_000,
        annual_contract_value_usd=60_000,
        cac_usd=5_200,
        gross_margin_pct=85.0,
        annual_churn_pct=5.0,
        monthly_burn_usd=3_400,
        runway_months=22.0,
        founder_fit_score=99.0,
        acuteness_of_problem=(
            "Multi-million-dollar enterprise pain: Fortune 1000 retailers, banks, and insurers spend $2M–$10M+ paying Big-4 system integrators to "
            "decouple 10-year-old Java/Spring/Oracle monoliths, and 65% of those rewrites stall or break production because engineers rewrite code "
            "without an automated black-box contract parity suite or safe Flyway database migration plan."
        ),
        ten_x_better_solution=(
            "10x faster and 80% cheaper than offshore system integrators: StranglerFig AI orchestrates the exact 7-agent pipeline in `enterprise-fullstack-plugin` "
            "(`architect` -> `test-engineer` writing Karate DSL contract tests against the legacy endpoint -> `backend-engineer` + `db-migrations` building "
            "the expand-migrate-contract schema -> `code-reviewer` verifying 100% response parity)."
        ),
        usage_and_retention_metrics=(
            "Multi-quarter enterprise engagement: teams extract 1 bounded domain per month across 12–36 month modernization roadmaps, driving 95%+ retention "
            "and 140% NRR."
        ),
        tam_and_growth_tailwinds=(
            "$12B+ TAM in enterprise application modernization and legacy technical-debt elimination (YC 2026 'SaaS & Legacy Challengers' thesis)."
        ),
        competition_and_defensible_edge=(
            "Generic coding assistants (Copilot, Devin) fail on 500k-line enterprise Java repos because they lack a disciplined Track-C Migration Parity Matrix "
            "and Karate/Testcontainers verification harness. StranglerFig's edge is its deterministic Karate parity-first loop."
        ),
        why_customers_switch=(
            "VPs of Engineering switch after a manual microservice extraction causes a production regression or slips 6 months behind schedule."
        ),
        cac_ltv_and_payback=(
            "CAC is $5,200 via a '1-Endpoint Free Karate Parity & Strangler Spec Assessment' for enterprise Java shops. At $60,000 ACV, 85% gross margin, "
            "and 5% churn, LTV is $1,020,000 (LTV:CAC = 196.2x) with a 1.2-month payback."
        ),
        nature_of_revenue=(
            "High-ACV annual enterprise license ($5,000/mo) or AI-Native Service fixed-price domain extraction retainers."
        ),
        actual_paying_customers=(
            "CTOs, VPs of Enterprise Architecture, and Engineering Directors at mid-to-large retail, grocery, banking, and insurance enterprises."
        ),
        burn_rate_and_runway=(
            "$3,400/month burn on $38,000 initial capital; profitable from the very first enterprise customer."
        ),
        unit_economics_scaling=(
            "Karate test execution, Jacoco coverage checks, and OpenAPI schema diffs run locally in Docker/Testcontainers at zero LLM cost."
        ),
        fundraising_and_cap_table=(
            "Bootstrapped via upfront enterprise pilot retainers; 100% founder equity."
        ),
        founder_product_fit=(
            "99/100 fit: Cody literally spearheads legacy system decoupling at Ahold Delhaize USA and built both `enterprise-fullstack-plugin` and "
            "the Java/Spring/Karate repositories (`Accounting_Backend_API_Project`, `Karate_SpringBoot_Demo_Project`)."
        ),
        pressure_and_pivot_playbook=(
            "If an enterprise won't allow cloud LLM calls on proprietary Java source code, deploy StranglerFig against their self-hosted AWS Bedrock / "
            "Azure OpenAI endpoint inside their VPC."
        ),
        signal_inspiration="Ahold Delhaize legacy modernization role + enterprise-fullstack-plugin + Karate_SpringBoot_Demo_Project",
    ),
    make_idea(
        id="IDEA-012",
        slug="auditguard-continuous-soc2-ai-compliance",
        title="AuditGuard Retainer — Continuous SOC 2, ISO 27001 & AI-Governance Evidence Engine for Mid-Market B2B",
        tagline="Replaces $50k manual security consultants with an automated evidence collector, vendor questionnaire responder, and continuous compliance retainer.",
        summary=(
            "Directly executes `Business_Analyzer_Project`'s NAICS `541512` playbook ('Sell SOC 2 / ISO 27001 readiness plus continuous monitoring retainers "
            "to mid-market firms facing customer audits', which carries a 1.14x Coastal and 1.08x EU fit and 1.15 EBITDA/CapEx ratio) and `541611` "
            "(Fractional B2B Advisory at 1.60 EBITDA/CapEx): AuditGuard connects to AWS/Azure, GitHub, Okta, and Docker Compose configs to auto-collect "
            "audit evidence, enforce security-header/secret-scan hooks (`visual-lab/scripts/security-check.sh`), and answer 300-question enterprise security questionnaires."
        ),
        category="Cybersecurity & Compliance AI",
        naics_code="541512",
        business_archetype="AI_NATIVE_SERVICE",
        target_metro="Boston-Cambridge MSA (US-MA-14460) & Chicago MSA (US-IL-16980)",
        pattern_ids=["PAT-01", "PAT-02", "PAT-04"],
        referenced_skills=["visual-lab", "claude-skill-factory", "software-intake-planner"],
        referenced_projects=["Business_Analyzer_Project", "Claude_Skills_Project", "Rixus_RE_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_NO_MARKET_NEED", "FAIL_UNIT_ECON_CAC"],
        s12=0.92,
        s60=0.65,
        initial_capex_usd=30_000,
        steady_state_ebitda_usd=670_000,
        annual_contract_value_usd=27_000,
        cac_usd=2_700,
        gross_margin_pct=88.0,
        annual_churn_pct=5.0,
        monthly_burn_usd=2_700,
        runway_months=24.0,
        founder_fit_score=95.0,
        acuteness_of_problem=(
            "Deal-blocking urgency: B2B SaaS and mid-market service companies cannot close $100k+ enterprise contracts until they pass SOC 2 Type II, "
            "ISO 27001, and new 2025–2026 ISO 42001 (AI Management System) vendor security questionnaires. Vanta/Drata still leave 40+ hours of engineering "
            "remediation (nginx security headers, Docker network isolation, migration audit trails) to the customer."
        ),
        ten_x_better_solution=(
            "Unlike compliance dashboards that only show red checkboxes, AuditGuard acts as an AI-Native Compliance Engineer: it runs deterministic infrastructure "
            "checks (`security-check.sh`, Three-Tier network isolation from `Rixus_RE_Project`, `security-headers.conf` from `Business_Analyzer_Project`) "
            "and opens ready-to-merge PRs that actually fix the compliance gaps."
        ),
        usage_and_retention_metrics=(
            "Continuous daily automated control checks + instant RFP/CAIQ security questionnaire answering; 95% annual retention because SOC 2 Type II "
            "and ISO surveillance audits recur every 12 months."
        ),
        tam_and_growth_tailwinds=(
            "$6.9B TAM in continuous GRC, SOC 2/ISO 27001/ISO 42001 compliance automation, and third-party risk management."
        ),
        competition_and_defensible_edge=(
            "Vanta and Drata alert on problems but don't write the Terraform/Docker/Nginx/Flyway remediation PRs; traditional vCISO firms charge $8k–$15k/mo "
            "for manual spreadsheets. AuditGuard's edge is automated PR remediation + deterministic security-check scripts."
        ),
        why_customers_switch=(
            "Founders and CTOs switch when a $200,000 enterprise deal is stalled in procurement security review and they don't have a dedicated DevSecOps engineer to fix 35 flagged controls."
        ),
        cac_ltv_and_payback=(
            "CAC is $2,700 via a free 'Repo & Docker Compose SOC 2 Readiness Grader' based on `visual-lab/scripts/security-check.sh`. At $27,000 ACV, "
            "88% gross margin, and 5% churn, LTV is $475,200 (LTV:CAC = 176.0x) with a 1.4-month payback."
        ),
        nature_of_revenue=(
            "Sticky annual B2B retainer ($2,250/mo) bundling platform monitoring + automated security questionnaire responses."
        ),
        actual_paying_customers=(
            "Series A/B SaaS CTOs, Healthcare/FinTech founders, and mid-market B2B software vendors selling into Fortune 500 procurement."
        ),
        burn_rate_and_runway=(
            "$2,700/month burn on $30,000 initial capital; cash-flow positive with 2 retainer clients."
        ),
        unit_economics_scaling=(
            "88%+ gross margin: control verification scripts run deterministically in CI; questionnaire answers reuse a pgvector-indexed answer vault."
        ),
        fundraising_and_cap_table=(
            "100% founder-owned; high upfront annual contract collections fund all growth organically."
        ),
        founder_product_fit=(
            "95/100 fit: directly leverages `Business_Analyzer_Project`'s NAICS `541512` playbook, `visual-lab/scripts/security-check.sh`, and "
            "`Rixus_RE_Project`'s Three-Tier network security architecture."
        ),
        pressure_and_pivot_playbook=(
            "Partner with boutique CPA audit firms who perform the final SOC 2 attestation—giving them a fast evidence portal while they refer all readiness clients to AuditGuard."
        ),
        signal_inspiration="Business_Analyzer_Project NAICS 541512 + visual-lab/scripts/security-check.sh",
    ),
])
