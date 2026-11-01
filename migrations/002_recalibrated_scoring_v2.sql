-- =============================================================================
-- Migration: 002_recalibrated_scoring_v2.sql
-- Project:   Idea Factory (5-Hour Autonomous Startup & Product Idea Generator)
-- Purpose:   Add benchmark-calibrated scoring v2 fields (finite discounted LTV,
--            annual churn, funded customer acquisition, customer segment) to
--            product_ideas and idea_metrics, and update analytical views.
-- =============================================================================

BEGIN;

-- 1. Add v2 columns to product_ideas table
ALTER TABLE product_ideas
    ADD COLUMN IF NOT EXISTS annual_churn_pct NUMERIC(6, 2) NOT NULL DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS capital_required_usd NUMERIC(14, 2) NOT NULL DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS customers_to_steady_state NUMERIC(10, 2) NOT NULL DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS customer_segment VARCHAR(32) NOT NULL DEFAULT '',
    ADD COLUMN IF NOT EXISTS scoring_version VARCHAR(64) NOT NULL DEFAULT 'v1-face-value',
    ADD COLUMN IF NOT EXISTS scoring_inputs JSONB NOT NULL DEFAULT '{}'::jsonb;

-- 2. Add v2 columns to idea_metrics table
ALTER TABLE idea_metrics
    ADD COLUMN IF NOT EXISTS annual_churn_pct NUMERIC(6, 2) NOT NULL DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS capital_required_usd NUMERIC(14, 2) NOT NULL DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS customers_to_steady_state NUMERIC(10, 2) NOT NULL DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS customer_segment VARCHAR(32) NOT NULL DEFAULT '',
    ADD COLUMN IF NOT EXISTS scoring_version VARCHAR(64) NOT NULL DEFAULT 'v1-face-value';

-- 3. Update v_idea_leaderboard view
DROP VIEW IF EXISTS v_idea_leaderboard;
CREATE VIEW v_idea_leaderboard AS
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
    p.annual_churn_pct,
    p.capital_required_usd,
    p.customers_to_steady_state,
    p.customer_segment,
    p.scoring_version,
    p.referenced_skills,
    p.pattern_ids,
    p.generation_source,
    p.created_at
FROM product_ideas p
LEFT JOIN idea_metrics m ON m.idea_id = p.id
ORDER BY p.roi_score DESC, p.id ASC;

-- 4. Update v_portfolio_summary view
DROP VIEW IF EXISTS v_portfolio_summary;
CREATE VIEW v_portfolio_summary AS
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
    ROUND(AVG(annual_churn_pct), 2) AS avg_annual_churn_pct,
    ROUND(AVG(capital_required_usd), 2) AS avg_capital_required_usd,
    MAX(created_at) AS latest_idea_created_at
FROM product_ideas;

COMMIT;
