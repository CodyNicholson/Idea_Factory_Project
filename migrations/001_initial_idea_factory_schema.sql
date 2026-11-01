-- =============================================================================
-- Migration: 001_initial_idea_factory_schema.sql
-- Project:   Idea Factory (5-Hour Autonomous Startup & Product Idea Generator)
-- Purpose:   PostgreSQL schema for storing all product ideas, their 5 core
--            sections (14 investor diligence answers), actuarial survival &
--            unit-economics metrics, and 5-hour autonomous agent telemetry.
-- =============================================================================

BEGIN;

-- 1. Schema Migrations Tracking Table
CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(64) PRIMARY KEY,
    filename TEXT NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Master Product Ideas Table (All Metadata, 15 Metrics, and 14 Diligence Answers)
CREATE TABLE IF NOT EXISTS product_ideas (
    id VARCHAR(32) PRIMARY KEY,
    slug VARCHAR(255) UNIQUE NOT NULL,
    title TEXT NOT NULL,
    tagline TEXT NOT NULL,
    summary TEXT NOT NULL,
    category VARCHAR(160) NOT NULL,
    naics_code VARCHAR(16) NOT NULL,
    industry_name VARCHAR(255) NOT NULL,
    business_archetype VARCHAR(64) NOT NULL,
    target_metro VARCHAR(255) NOT NULL,

    -- Multi-valued lineage & attribution arrays
    pattern_ids TEXT[] NOT NULL DEFAULT '{}',
    referenced_skills TEXT[] NOT NULL DEFAULT '{}',
    referenced_projects TEXT[] NOT NULL DEFAULT '{}',
    causal_drivers TEXT[] NOT NULL DEFAULT '{}',
    mitigated_failure_modes TEXT[] NOT NULL DEFAULT '{}',

    -- Quantitative Actuarial & Unit-Economics Metrics (Business_Analyzer_Project)
    roi_score NUMERIC(6, 2) NOT NULL CHECK (roi_score >= 1.0 AND roi_score <= 99.9),
    survival_1yr NUMERIC(6, 4) NOT NULL CHECK (survival_1yr > 0.0 AND survival_1yr <= 1.0),
    survival_5yr NUMERIC(6, 4) NOT NULL CHECK (survival_5yr > 0.0 AND survival_5yr <= survival_1yr),
    projected_3yr_irr_pct NUMERIC(8, 2) NOT NULL,
    initial_capex_usd NUMERIC(14, 2) NOT NULL,
    steady_state_ebitda_usd NUMERIC(14, 2) NOT NULL,
    annual_contract_value_usd NUMERIC(14, 2) NOT NULL,
    cac_usd NUMERIC(14, 2) NOT NULL,
    ltv_usd NUMERIC(14, 2) NOT NULL CHECK (ltv_usd > cac_usd),
    ltv_cac_ratio NUMERIC(10, 2) NOT NULL,
    payback_months NUMERIC(8, 2) NOT NULL,
    gross_margin_pct NUMERIC(6, 2) NOT NULL,
    monthly_burn_usd NUMERIC(14, 2) NOT NULL,
    runway_months NUMERIC(8, 2) NOT NULL,
    founder_fit_score NUMERIC(6, 2) NOT NULL,

    -- Section 1: Product & Problem-Solving (Questions 1.1 - 1.3)
    acuteness_of_problem TEXT NOT NULL,
    ten_x_better_solution TEXT NOT NULL,
    usage_and_retention_metrics TEXT NOT NULL,

    -- Section 2: Market & Competition (Questions 2.1 - 2.3)
    tam_and_growth_tailwinds TEXT NOT NULL,
    competition_and_defensible_edge TEXT NOT NULL,
    why_customers_switch TEXT NOT NULL,

    -- Section 3: Business Model & Traction (Questions 3.1 - 3.3)
    cac_ltv_and_payback TEXT NOT NULL,
    nature_of_revenue TEXT NOT NULL,
    actual_paying_customers TEXT NOT NULL,

    -- Section 4: Financials & Runway (Questions 4.1 - 4.3)
    burn_rate_and_runway TEXT NOT NULL,
    unit_economics_scaling TEXT NOT NULL,
    fundraising_and_cap_table TEXT NOT NULL,

    -- Section 5: Team & Execution (Questions 5.1 - 5.2)
    founder_product_fit TEXT NOT NULL,
    pressure_and_pivot_playbook TEXT NOT NULL,

    -- Provenance, Timestamps & Full JSONB Document
    generation_source VARCHAR(128) NOT NULL DEFAULT 'SEED_SYNTHESIS',
    signal_inspiration TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    payload_json JSONB NOT NULL
);

-- 3. Dedicated Quantitative Metrics & Actuarial Table (1:1 with product_ideas)
CREATE TABLE IF NOT EXISTS idea_metrics (
    idea_id VARCHAR(32) PRIMARY KEY REFERENCES product_ideas(id) ON DELETE CASCADE,
    roi_score NUMERIC(6, 2) NOT NULL,
    survival_1yr NUMERIC(6, 4) NOT NULL,
    survival_5yr NUMERIC(6, 4) NOT NULL,
    projected_3yr_irr_pct NUMERIC(8, 2) NOT NULL,
    initial_capex_usd NUMERIC(14, 2) NOT NULL,
    steady_state_ebitda_usd NUMERIC(14, 2) NOT NULL,
    annual_contract_value_usd NUMERIC(14, 2) NOT NULL,
    cac_usd NUMERIC(14, 2) NOT NULL,
    ltv_usd NUMERIC(14, 2) NOT NULL,
    ltv_cac_ratio NUMERIC(10, 2) NOT NULL,
    payback_months NUMERIC(8, 2) NOT NULL,
    gross_margin_pct NUMERIC(6, 2) NOT NULL,
    monthly_burn_usd NUMERIC(14, 2) NOT NULL,
    runway_months NUMERIC(8, 2) NOT NULL,
    founder_fit_score NUMERIC(6, 2) NOT NULL,
    ebitda_capex_multiple NUMERIC(10, 2) GENERATED ALWAYS AS (
        CASE WHEN initial_capex_usd > 0 THEN ROUND(steady_state_ebitda_usd / initial_capex_usd, 2) ELSE 0 END
    ) STORED,
    net_ltv_spread_usd NUMERIC(14, 2) GENERATED ALWAYS AS (ltv_usd - cac_usd) STORED,
    survival_retention_ratio NUMERIC(6, 4) GENERATED ALWAYS AS (
        CASE WHEN survival_1yr > 0 THEN ROUND(survival_5yr / survival_1yr, 4) ELSE 0 END
    ) STORED,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Normalized 14 Diligence Questions Table (For Granular Section/Question SQL Queries)
CREATE TABLE IF NOT EXISTS idea_diligence_questions (
    idea_id VARCHAR(32) NOT NULL REFERENCES product_ideas(id) ON DELETE CASCADE,
    section_number SMALLINT NOT NULL CHECK (section_number BETWEEN 1 AND 5),
    question_number VARCHAR(8) NOT NULL,
    section_title VARCHAR(128) NOT NULL,
    question_key VARCHAR(64) NOT NULL,
    question_prompt TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (idea_id, question_number)
);

-- 5. Autonomous 5-Hour Agent Loop Runs & Telemetry Table
CREATE TABLE IF NOT EXISTS agent_runs (
    run_id VARCHAR(64) PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(64) NOT NULL,
    provider VARCHAR(64) NOT NULL,
    window_cycle INTEGER NOT NULL DEFAULT 1,
    auto_resume_on_refresh BOOLEAN NOT NULL DEFAULT TRUE,
    elapsed_seconds DOUBLE PRECISION NOT NULL,
    remaining_seconds DOUBLE PRECISION NOT NULL DEFAULT 18000.0,
    max_runtime_seconds INTEGER NOT NULL,
    ideas_generated INTEGER NOT NULL,
    ideas_count INTEGER NOT NULL DEFAULT 0,
    api_calls INTEGER NOT NULL,
    estimated_cost_usd NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    last_idea_id VARCHAR(32),
    stop_reason TEXT,
    state_json JSONB
);

-- 6. Performance & Analytical Indexes
CREATE INDEX IF NOT EXISTS idx_product_ideas_roi_desc ON product_ideas (roi_score DESC, id ASC);
CREATE INDEX IF NOT EXISTS idx_product_ideas_created_desc ON product_ideas (created_at DESC, id DESC);
CREATE INDEX IF NOT EXISTS idx_product_ideas_category ON product_ideas (category);
CREATE INDEX IF NOT EXISTS idx_product_ideas_naics ON product_ideas (naics_code);
CREATE INDEX IF NOT EXISTS idx_product_ideas_archetype ON product_ideas (business_archetype);
CREATE INDEX IF NOT EXISTS idx_product_ideas_skills_gin ON product_ideas USING GIN (referenced_skills);
CREATE INDEX IF NOT EXISTS idx_product_ideas_patterns_gin ON product_ideas USING GIN (pattern_ids);
CREATE INDEX IF NOT EXISTS idx_product_ideas_payload_gin ON product_ideas USING GIN (payload_json);
CREATE INDEX IF NOT EXISTS idx_idea_metrics_roi_irr ON idea_metrics (roi_score DESC, projected_3yr_irr_pct DESC);
CREATE INDEX IF NOT EXISTS idx_idea_diligence_question_key ON idea_diligence_questions (question_key);

-- 7. Analytical Views for Leaderboard & Portfolio Metrics
CREATE OR REPLACE VIEW v_idea_leaderboard AS
SELECT
    RANK() OVER (ORDER BY p.roi_score DESC, p.survival_5yr DESC, p.id ASC) AS portfolio_rank,
    p.id,
    p.slug,
    p.title,
    p.category,
    p.naics_code,
    p.industry_name,
    p.business_archetype,
    p.target_metro,
    p.roi_score,
    p.survival_1yr,
    p.survival_5yr,
    p.projected_3yr_irr_pct,
    p.initial_capex_usd,
    p.steady_state_ebitda_usd,
    p.annual_contract_value_usd,
    p.cac_usd,
    p.ltv_usd,
    p.ltv_cac_ratio,
    p.payback_months,
    p.gross_margin_pct,
    p.monthly_burn_usd,
    p.runway_months,
    p.founder_fit_score,
    m.ebitda_capex_multiple,
    m.net_ltv_spread_usd,
    p.referenced_skills,
    p.pattern_ids,
    p.generation_source,
    p.created_at
FROM product_ideas p
LEFT JOIN idea_metrics m ON m.idea_id = p.id
ORDER BY p.roi_score DESC, p.id ASC;

CREATE OR REPLACE VIEW v_portfolio_summary AS
SELECT
    COUNT(*)::INTEGER AS total_ideas,
    ROUND(AVG(roi_score), 2) AS avg_roi_score,
    ROUND(AVG(survival_1yr) * 100, 2) AS avg_survival_1yr_pct,
    ROUND(AVG(survival_5yr) * 100, 2) AS avg_survival_5yr_pct,
    ROUND(AVG(projected_3yr_irr_pct), 2) AS avg_3yr_irr_pct,
    ROUND(AVG(annual_contract_value_usd), 2) AS avg_acv_usd,
    ROUND(AVG(ltv_cac_ratio), 2) AS avg_ltv_cac_ratio,
    ROUND(AVG(payback_months), 2) AS avg_payback_months,
    ROUND(AVG(gross_margin_pct), 2) AS avg_gross_margin_pct,
    ROUND(AVG(founder_fit_score), 2) AS avg_founder_fit_score,
    MAX(created_at) AS latest_idea_created_at
FROM product_ideas;

CREATE OR REPLACE VIEW v_category_analytics AS
SELECT
    category,
    business_archetype,
    naics_code,
    COUNT(*)::INTEGER AS idea_count,
    ROUND(AVG(roi_score), 2) AS avg_roi_score,
    ROUND(AVG(survival_5yr) * 100, 2) AS avg_survival_5yr_pct,
    ROUND(AVG(projected_3yr_irr_pct), 2) AS avg_3yr_irr_pct,
    ROUND(AVG(ltv_cac_ratio), 2) AS avg_ltv_cac_ratio,
    ROUND(AVG(payback_months), 2) AS avg_payback_months
FROM product_ideas
GROUP BY category, business_archetype, naics_code
ORDER BY avg_roi_score DESC, idea_count DESC;

COMMIT;

