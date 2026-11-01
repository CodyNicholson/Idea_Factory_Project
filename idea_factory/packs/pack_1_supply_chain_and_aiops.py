"""Pack 1: Supply Chain, Multi-Facility Fulfillment, and Event-Driven AIOps."""
from __future__ import annotations

from ..models import ProductIdea
from ..seed_ideas import make_idea

IDEAS_PACK_1: list[ProductIdea] = [
    make_idea(
        id="IDEA-001",
        slug="dlt-sentinel-kafka-self-healing",
        title="DLT Sentinel — Autonomous Dead-Letter Triage & Replay Engine for Multi-Facility Order Pipelines",
        tagline="Self-healing Kafka & event-streaming plane that diagnoses poison-pill payloads, synthesizes schema patches, and replays quarantined orders with zero head-of-line blocking.",
        summary=(
            "Productizes the exact architecture proven in `Kafka_Visual_Lab_Project` and `enterprise-fullstack-plugin/skills/event-streaming`: "
            "an autonomous control plane for multi-facility ecommerce, grocery, and 3PL fulfillment pipelines that monitors retry topics "
            "and Dead Letter Topics (`*-dlt`), clusters poison-pill exceptions by root cause, validates idempotency invariants, and "
            "executes safe consumer-group offset replays—cutting on-call incident volume by 70%+."
        ),
        category="Developer & Supply-Chain Infra",
        naics_code="518210",
        business_archetype="VERTICAL_SAAS",
        target_metro="Chicago-Naperville-Elgin MSA (US-IL-16980)",
        pattern_ids=["PAT-04", "PAT-05", "PAT-06"],
        referenced_skills=["enterprise-fullstack-plugin", "visual-lab", "software-intake-planner"],
        referenced_projects=["Kafka_Visual_Lab_Project", "Resume_Creator_Project", "Business_Analyzer_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_NO_MARKET_NEED", "FAIL_UNIT_ECON_CAC", "FAIL_CASH_BURN_RUNWAY"],
        s12=0.91,
        s60=0.64,
        initial_capex_usd=35_000,
        steady_state_ebitda_usd=680_000,
        annual_contract_value_usd=36_000,
        cac_usd=3_800,
        gross_margin_pct=88.0,
        annual_churn_pct=6.0,
        monthly_burn_usd=3_200,
        runway_months=24.0,
        founder_fit_score=99.0,
        acuteness_of_problem=(
            "Mission-critical severity: in multi-facility ecommerce and logistics (fulfilling millions of orders across 10–50 warehouses), "
            "a single upstream schema drift or malformed EDI/JSON payload triggers a poison-pill loop. If teams use blocking retries, an entire "
            "partition stalls (head-of-line blocking), freezing thousands of perishable or SLA-bound orders; if they route to a Dead Letter Topic "
            "(DLT), messages silently rot there while on-call engineers spend 15+ hours/week writing ad-hoc replay scripts."
        ),
        ten_x_better_solution=(
            "10x faster MTTR and 73% lower on-call page volume: unlike generic APM dashboards (Datadog, Confluent Control Center) that only alert "
            "that a DLT count rose, DLT Sentinel inspects the `kafka_dlt-exception-stacktrace` and payload headers, runs deterministic schema diffing "
            "locally (zero LLM cost for 90% of messages), generates a quarantined transform rule or PR via the `backend-engineer` agent pattern, "
            "verifies consumer idempotency in an isolated Testcontainers shadow topic, and replays offsets via `ConsumerSeekAware` with one click."
        ),
        usage_and_retention_metrics=(
            "Daily active operational dependency: platform and fulfillment ops teams keep the live SSE topology stream open 24/7. "
            "Target metrics: 94%+ Gross Revenue Retention (GRR), 128%+ Net Revenue Retention (NRR) via topic/cluster volume expansion, "
            "and <5% annual logo churn because removing DLT Sentinel brings back 2 a.m. pager storms."
        ),
        tam_and_growth_tailwinds=(
            "$6.8B global TAM across 45,000+ enterprises running Apache Kafka, Redpanda, AWS MSK, Azure Event Hubs, and RabbitMQ for order, "
            "payment, and inventory pipelines, growing at 21% CAGR as real-time omnichannel fulfillment and agentic event buses proliferate."
        ),
        competition_and_defensible_edge=(
            "Incumbents are Confluent Control Center, lenses.io, and Datadog Data Streams Monitoring. They stop at observability. "
            "DLT Sentinel's defensible moat is its deterministic remediation + shadow-replay state machine (`INV-n` idempotency verification "
            "before replay) and an ever-growing proprietary library of ERP/WMS/OMS poison-pill signatures."
        ),
        why_customers_switch=(
            "Customers switch after a single Friday-night poison-pill outage where Orders or Inventory events get stuck in a DLT and manual "
            "CLI `kafka-console-consumer` replay accidentally double-ships or double-charges customers."
        ),
        cac_ltv_and_payback=(
            "CAC is $3,800 via Product-Led Growth (PLG): an open interactive browser sandbox modeled directly on `Kafka_Visual_Lab_Project` "
            "ranks for top Spring Kafka / MSK / DLT error queries and converts engineering leads in-product. At $36,000 ACV and 88% gross margin, "
            "LTV is $528,000 (LTV:CAC = 138.9x) with a 1.4-month CAC payback period."
        ),
        nature_of_revenue=(
            "100% sticky annual B2B subscription (base platform fee of $2,000/month + tiered throughput per monitored broker/cluster), "
            "billed annually upfront with net-zero cloud inference COGS since the agent deploys inside the customer's VPC."
        ),
        actual_paying_customers=(
            "VPs of Platform Engineering, Directors of Supply Chain/Fulfillment Systems, and Principal Architects at mid-market to enterprise "
            "retailers, grocers, 3PLs, and fintechs—reachable directly through Chicago supply-chain tech networks and Kafka engineering communities."
        ),
        burn_rate_and_runway=(
            "Monthly burn is $3,200/month (cloud test clusters, CI, domain/infra) on a $35,000 initial capital allocation, yielding 11+ months "
            "of pure zero-revenue runway and 24+ months with just 1 design-partner contract ($3k/mo)."
        ),
        unit_economics_scaling=(
            "Gross margins start at 85% and scale to 91% because the heavy inspection and shadow-topic replay run on the customer's own Kubernetes/Docker "
            "compute, while LLM reasoning is invoked only once per unique exception signature hash."
        ),
        fundraising_and_cap_table=(
            "100% founder-owned bootstrapping to $1M ARR (no messy uncapped SAFEs, no convertible debt overhang). Optional $1.5M seed at a $15M+ "
            "post-money valuation once 25 enterprise logos are live."
        ),
        founder_product_fit=(
            "Unmatched 99/100 founder-product fit: Cody Nicholson architected the Java/Spring Boot/Kafka order-processing ETL pipeline fulfilling "
            "3,000,000+ orders/year across 25 facilities at Peapod Digital Labs / Ahold Delhaize USA, cut on-call incident volume by 73% with "
            "self-service operational tooling, and already built the working prototype in `Kafka_Visual_Lab_Project`."
        ),
        pressure_and_pivot_playbook=(
            "If enterprise security teams delay VPC agent installation, pivot immediately to a zero-data-egress CLI/Sidecar Docker image sold via "
            "AWS/Azure Marketplace (using existing cloud credits), or widen from Kafka to RabbitMQ/SQS/ServiceBus dead-letter queues."
        ),
        signal_inspiration="Kafka_Visual_Lab_Project + Peapod 25-facility 73% incident reduction track record",
    ),
    make_idea(
        id="IDEA-002",
        slug="coldchain-guard-otif-reconciliation",
        title="ColdChainGuard — Multi-Facility Cold-Chain OTIF & Detention Dispute Recovery Agent",
        tagline="Autonomous EDI/Kafka/WMS reconciliation engine that recovers chargebacks, detention fees, and temperature-excursion claims for refrigerated food & pharma shippers.",
        summary=(
            "Anchored on NAICS `493120` (Refrigerated Warehousing & Storage) and `488510` (Freight Arrangement) from `Business_Analyzer_Project` "
            "(which score among the highest Midwest B2B survival sectors at 54–61%), ColdChainGuard ingests IoT reefer telemetry, WMS gate timestamps, "
            "and EDI 204/214/210 invoices to automatically dispute invalid retailer OTIF (On-Time In-Full) chargebacks and carrier detention fees."
        ),
        category="Supply-Chain & Logistics AI",
        naics_code="493120",
        business_archetype="AI_NATIVE_SERVICE",
        target_metro="Chicago-Naperville-Elgin MSA (US-IL-16980)",
        pattern_ids=["PAT-01", "PAT-02", "PAT-06"],
        referenced_skills=["enterprise-fullstack-plugin", "software-intake-planner"],
        referenced_projects=["Business_Analyzer_Project", "Kafka_Visual_Lab_Project", "Resume_Creator_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_NO_MARKET_NEED", "FAIL_RENT_LABOR_SQUEEZE"],
        s12=0.90,
        s60=0.62,
        initial_capex_usd=40_000,
        steady_state_ebitda_usd=620_000,
        annual_contract_value_usd=42_000,
        cac_usd=4_500,
        gross_margin_pct=84.0,
        annual_churn_pct=5.5,
        monthly_burn_usd=3_500,
        runway_months=22.0,
        founder_fit_score=97.0,
        acuteness_of_problem=(
            "Hair-on-fire financial bleed: grocery and cold-chain suppliers lose 2% to 4% of gross revenue to automated retail OTIF fines "
            "(Walmart, Kroger, Target, Ahold) and carrier detention disputes because proving whether a delay or temperature dip happened at the "
            "carrier, dock door, or retailer requires manually cross-referencing PDF bills of lading, ELD GPS logs, and reefer IoT CSVs within a 14-day dispute window."
        ),
        ten_x_better_solution=(
            "10x speed and 95% lower labor cost: ColdChainGuard connects to the facility's event stream and TMS, deterministically aligns dock-door "
            "check-in timestamps with GPS geofences and reefer temperature curves, and auto-generates a complete, evidence-stamped dispute packet "
            "(PDF + portal submission) in under 60 seconds per claim—recovering $150k–$800k/year per mid-market shipper."
        ),
        usage_and_retention_metrics=(
            "Continuous background execution on 100% of outbound loads; weekly executive digest of dollars recovered. "
            "Net Revenue Retention exceeds 130% as customers expand from 1 cold-storage facility to their entire multi-state network."
        ),
        tam_and_growth_tailwinds=(
            "$4.9B TAM across 18,000+ North American food/beverage processors, cold-chain 3PLs, and pharma distributors; massive tailwinds from "
            "stricter FDA FSMA Rule 204 traceability mandates and aggressive big-box retail OTIF fining algorithms."
        ),
        competition_and_defensible_edge=(
            "Legacy TMS tools (MercuryGate, Blue Yonder) don't automate evidence assembly for retail dispute portals; manual audit firms charge 25–35% "
            "contingency and miss deadlines. ColdChainGuard's edge is its deterministic multi-source event correlation engine + proprietary database of "
            "facility dock-turn benchmarks in the Midwest freight corridor."
        ),
        why_customers_switch=(
            "Zero-risk ROI: shippers switch because a 30-day historical audit of their past 90 days of OTIF deductions immediately uncovers $20,000+ "
            "in recoverable fines before they pay their first invoice."
        ),
        cac_ltv_and_payback=(
            "CAC is $4,500 via targeted "
            "'Free 90-Day OTIF Chargeback Audit' offers to Midwest food/cold-storage CFOs and VPs of Logistics. With $42,000 ACV ($2,500/mo base + 10% "
            "of recovered chargebacks), 84% gross margin, and 5.5% churn, LTV is $641,454 (LTV:CAC = 142.5x) and payback is 1.5 months."
        ),
        nature_of_revenue=(
            "Hybrid recurring SaaS retainer ($2,500/mo per facility) plus outcome-aligned recovery share (10% of approved dispute reversals), "
            "combining predictable ARR with high-upside performance expansion."
        ),
        actual_paying_customers=(
            "CFOs, VPs of Supply Chain, and Directors of Cold-Chain Operations at mid-market food manufacturers, grocery commissaries, and refrigerated "
            "warehouses concentrated in the Chicago (I-55/I-80) and Midwest logistics hub."
        ),
        burn_rate_and_runway=(
            "$3,500/month burn rate on $40,000 initial capital; cash-flow positive upon signing the second cold-storage customer in Month 3."
        ),
        unit_economics_scaling=(
            "Unit economics improve with every facility onboarded: once a retail portal connector (e.g., Retail Link, Supplier Gateways) is built once, "
            "marginal cost per additional disputed claim is <$0.04 in compute and PDF rendering (reusing `Resume_Creator_Project` PDF vector primitives)."
        ),
        fundraising_and_cap_table=(
            "Clean 100% founder equity structure; eligible for non-dilutive supply-chain innovation grants and customer prepayments, avoiding early VC dilution."
        ),
        founder_product_fit=(
            "97/100 founder fit: directly leverages Cody's 6+ years building grocery/ecommerce order fulfillment pipelines at Peapod Digital Labs and "
            "Ahold Delhaize USA in Chicago, combined with `Business_Analyzer_Project`'s NAICS `493120` actuarial insights."
        ),
        pressure_and_pivot_playbook=(
            "If a retailer changes its portal UI, fall back to automated EDI 812 credit/debit adjustment generation and FSMA Rule 204 compliance reporting, "
            "which is legally mandated regardless of retailer portal changes."
        ),
        signal_inspiration="Business_Analyzer_Project NAICS 493120 + Ahold/Peapod 25-facility grocery fulfillment domain expertise",
    ),
]

IDEAS_PACK_1.extend([
    make_idea(
        id="IDEA-003",
        slug="borderlane-ai-usmca-freight-customs",
        title="BorderLane AI — Autonomous US-Mexico Cross-Border Freight & USMCA Customs Brokerage Desk",
        tagline="AI-native customs & freight reconciliation desk that eliminates border drayage delays, Carta Porte errors, and HTS tariff misclassifications.",
        summary=(
            "Grounded in `Business_Analyzer_Project`'s NAICS `488510` playbook ('Start as a tech-enabled brokerage on one cross-border lane; earn take rate "
            "before building a marketplace'), BorderLane AI automates commercial invoice parsing, Mexican CFDI Carta Porte 3.0 validation, USMCA certificate-of-origin "
            "verification, and drayage handoff coordination across Laredo/Monterrey/Dallas/Chicago freight lanes."
        ),
        category="Supply-Chain & Logistics AI",
        naics_code="488510",
        business_archetype="AI_NATIVE_SERVICE",
        target_metro="Dallas-Fort Worth MSA (US-TX-19100)",
        pattern_ids=["PAT-01", "PAT-02", "PAT-04"],
        referenced_skills=["enterprise-fullstack-plugin", "software-intake-planner"],
        referenced_projects=["Business_Analyzer_Project", "Kafka_Visual_Lab_Project"],
        causal_drivers=["SUCC_RECURRING_B2B", "SUCC_LOCAL_OLIGOPOLY"],
        mitigated_failure_modes=["FAIL_NO_MARKET_NEED", "FAIL_PREMATURE_SCALING"],
        s12=0.89,
        s60=0.58,
        initial_capex_usd=45_000,
        steady_state_ebitda_usd=640_000,
        annual_contract_value_usd=38_000,
        cac_usd=4_200,
        gross_margin_pct=83.0,
        annual_churn_pct=6.5,
        monthly_burn_usd=3_800,
        runway_months=20.0,
        founder_fit_score=91.0,
        acuteness_of_problem=(
            "Severe border bottleneck: 40%+ of US-Mexico cross-border truckloads experience 6–36 hour border holds at Laredo, Otay Mesa, or El Paso "
            "due to mismatched HTS tariff codes, missing Mexican SAT Carta Porte 3.0 fields, or manual WhatsApp/email handoffs between Mexican carrier, "
            "customs broker, transfer drayage, and US linehaul—costing shippers $500–$1,800 per delayed load."
        ),
        ten_x_better_solution=(
            "10x faster clearance packet preparation (under 90 seconds vs. 4 hours of manual broker data entry): BorderLane AI ingests packing lists, "
            "Spanish/English PDF commercial invoices, and BOMs, runs a deterministic Carta Porte 3.0 + USMCA rule-of-origin validator (`INV-n` schema check), "
            "and synchronizes Mexican and US brokers via a unified event-driven state machine."
        ),
        usage_and_retention_metrics=(
            "Used on every cross-border load shipped daily; 93% annual gross retention and 135% NRR as shippers route additional cross-border lanes "
            "through the platform."
        ),
        tam_and_growth_tailwinds=(
            "$8.2B TAM in North American cross-border freight arrangement and customs brokerage; supercharged by the historic US-Mexico nearshoring boom "
            "(Mexico surpassed China as top US trade partner) and complex 2025–2026 tariff compliance enforcement."
        ),
        competition_and_defensible_edge=(
            "Incumbents are fragmented local customs brokers using 1990s AS/400 software and bloated digital forwarders with massive human ops overhead. "
            "BorderLane's moat is its SKU-level bilingual HTS + Carta Porte knowledge graph that learns each shipper's exact part catalog."
        ),
        why_customers_switch=(
            "Shippers switch immediately after a single SAT Carta Porte fine ($2,500–$5,000) or border hold stalls an automotive/industrial assembly line."
        ),
        cac_ltv_and_payback=(
            "CAC is $4,200 via free 'Carta Porte & HTS Audit' tools for cross-border 3PLs and mid-market manufacturers. At $38,000 ACV, 83% gross margin, "
            "and 6.5% churn, LTV is $485,230 (LTV:CAC = 115.5x) with a 1.6-month payback."
        ),
        nature_of_revenue=(
            "Recurring monthly platform subscription ($2,000/mo) plus per-crossing automated clearance fee ($25/load), creating high-margin recurring + volume revenue."
        ),
        actual_paying_customers=(
            "Mid-market automotive/industrial suppliers, nearshoring manufacturers, and cross-border freight brokers operating along the Monterrey–Laredo–Dallas–Chicago corridor."
        ),
        burn_rate_and_runway=(
            "$3,800/month burn rate; reaches break-even with just 2 paying mid-market shippers or 1 regional freight brokerage."
        ),
        unit_economics_scaling=(
            "Once a shipper's SKU catalog is mapped and validated, repeat crossings require zero LLM calls—running purely on deterministic lookup tables at 94% marginal gross margin."
        ),
        fundraising_and_cap_table=(
            "Bootstrapped to initial $500k ARR on a single Cross-Border lane (Dallas/Laredo to Chicago) before optional seed round; zero debt or toxic SAFEs."
        ),
        founder_product_fit=(
            "91/100 fit: combines Cody's multi-facility ETL and event-streaming architecture (`enterprise-fullstack-plugin/skills/etl-pipeline`) with "
            "`Business_Analyzer_Project`'s NAICS `488510` cross-border brokerage playbook."
        ),
        pressure_and_pivot_playbook=(
            "If direct shipper sales cycles lengthen, sell white-label seat/API licenses directly to existing licensed customs brokers who are drowning in Carta Porte paperwork."
        ),
        signal_inspiration="Business_Analyzer_Project NAICS 488510 nearshoring playbook + YC 2026 AI-native brokerage pattern",
    ),
    make_idea(
        id="IDEA-004",
        slug="runbookforge-autonomous-oncall-mttr",
        title="RunbookForge — Deterministic Incident Auto-Remediation & Self-Service Ops Portal Generator",
        tagline="Turns recurring PagerDuty/Datadog alerts and post-mortems into deterministic, RBAC-governed self-service remediation workflows.",
        summary=(
            "Directly productizes Cody's Peapod Digital Labs achievement ('Engineered self-service support tooling for on-call operations, cutting incident "
            "volume by 73% and significantly reducing MTTR'): RunbookForge ingests incident tickets, Slack war-room transcripts, and Datadog/CloudWatch alerts, "
            "identifies the top 20% of recurring operational fixes (stuck orders, cache flushes, pod restarts, DB lock kills), and compiles them into "
            "safe, dry-run-verified self-service buttons for L1 support and operations teams."
        ),
        category="Developer & Supply-Chain Infra",
        naics_code="518210",
        business_archetype="VERTICAL_SAAS",
        target_metro="Chicago-Naperville-Elgin MSA (US-IL-16980)",
        pattern_ids=["PAT-04", "PAT-05", "PAT-06"],
        referenced_skills=["claude-skill-factory", "enterprise-fullstack-plugin", "software-intake-planner"],
        referenced_projects=["Resume_Creator_Project", "Business_Analyzer_Project", "Kafka_Visual_Lab_Project"],
        causal_drivers=["SUCC_RECURRING_B2B"],
        mitigated_failure_modes=["FAIL_UNIT_ECON_CAC", "FAIL_CASH_BURN_RUNWAY"],
        s12=0.90,
        s60=0.60,
        initial_capex_usd=30_000,
        steady_state_ebitda_usd=590_000,
        annual_contract_value_usd=30_000,
        cac_usd=3_200,
        gross_margin_pct=89.0,
        annual_churn_pct=6.0,
        monthly_burn_usd=2_800,
        runway_months=24.0,
        founder_fit_score=98.0,
        acuteness_of_problem=(
            "Chronic engineering burnout & SLA drain: in mid-to-large engineering orgs, 60–75% of L3 senior engineer on-call pages are repetitive "
            "operational state fixes (re-syncing a stuck order, clearing a corrupted Redis key, re-triggering a failed webhook) that L1 support cannot "
            "execute safely because raw DB/SSH access is too dangerous."
        ),
        ten_x_better_solution=(
            "Uses `claude-skill-factory`'s 'Low-Freedom Deterministic Guardrail' pattern: instead of an AI agent running arbitrary bash commands in prod "
            "(which CISOs block), RunbookForge compiles recurring incident fixes into strongly typed, parameterized, dry-run-validated micro-workflows "
            "with pre/post invariant checks (`INV-n`) and audit logging, cutting L3 escalations by 70%+ within 30 days."
        ),
        usage_and_retention_metrics=(
            "Executed dozens of times daily by L1/L2 support and ops managers; 95% annual retention because every workflow added permanently offloads "
            "a class of pager alerts from senior engineers."
        ),
        tam_and_growth_tailwinds=(
            "$5.4B TAM in AIOps, incident management, and internal developer portals (Retool/PagerDuty/Rundeck replacement); strong tailwinds as lean "
            "engineering teams must support more microservices per engineer."
        ),
        competition_and_defensible_edge=(
            "PagerDuty Process Automation (Rundeck) requires heavy manual YAML/script authoring; AI SRE startups (Resolve, Traversal) face security pushback "
            "over unconstrained agent actions. RunbookForge wins by auto-mining the incident corpus to propose workflows while enforcing deterministic, "
            "hook-guarded execution (`PreToolUse`/`PostToolUse` verification)."
        ),
        why_customers_switch=(
            "Engineering directors switch when senior engineers threaten to quit over pager fatigue or when building internal Retool apps falls months behind."
        ),
        cac_ltv_and_payback=(
            "CAC is $3,200 via a free 'Incident Corpus Pareto Analyzer' CLI that scans 90 days of Jira/PagerDuty history and outputs the exact % of "
            "alerts that can be automated. At $30,000 ACV and 89% gross margin, LTV is $445,000 (LTV:CAC = 139.1x) with a 1.4-month payback."
        ),
        nature_of_revenue=(
            "Sticky annual B2B subscription tiered by number of active automated runbooks and on-call seats."
        ),
        actual_paying_customers=(
            "VPs of Engineering, SRE Leads, and Heads of Technical Support at 50–1,000 person SaaS, ecommerce, and fintech companies."
        ),
        burn_rate_and_runway=(
            "$2,800/month burn rate on $30,000 initial capital; profitable from the second annual contract."
        ),
        unit_economics_scaling=(
            "89%+ gross margin: LLM tokens are used only during initial runbook synthesis from post-mortems; runtime executions are 100% deterministic API/SQL calls."
        ),
        fundraising_and_cap_table=(
            "Bootstrapped with zero institutional dilution required; optional strategic angel round from CTO/VP Eng operators."
        ),
        founder_product_fit=(
            "98/100 fit: Cody personally built the internal self-service on-call tooling at Peapod Digital Labs that cut incident volume by 73%, "
            "and authored the deterministic hook/skill architecture in `claude-skill-factory`."
        ),
        pressure_and_pivot_playbook=(
            "If a prospect already uses Retool or Backstage, sell RunbookForge as an automated 'Post-Mortem-to-Backstage/Retool Action Compiler' plugin."
        ),
        signal_inspiration="Resume_Creator_Project (73% incident reduction at Peapod) + claude-skill-factory deterministic hooks",
    ),
])
