-- =============================================================================
-- Migration: 003_gemini_argon_agent.sql
-- Purpose:   Replace the 5-hour-window and multi-provider telemetry with token
--            telemetry for the single allowed model, and record every billed
--            Gemini call, including answers that were rejected.
-- =============================================================================

BEGIN;

ALTER TABLE agent_runs
    DROP COLUMN IF EXISTS window_cycle,
    DROP COLUMN IF EXISTS auto_resume_on_refresh,
    DROP COLUMN IF EXISTS remaining_seconds,
    DROP COLUMN IF EXISTS max_runtime_seconds,
    DROP COLUMN IF EXISTS estimated_cost_usd,
    ADD COLUMN IF NOT EXISTS thinking_level VARCHAR(16) NOT NULL DEFAULT 'high',
    ADD COLUMN IF NOT EXISTS ideas_rejected INTEGER NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS input_tokens BIGINT NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS output_tokens BIGINT NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS thought_tokens BIGINT NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS refresh_waits INTEGER NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS resume_at TIMESTAMPTZ;

ALTER TABLE agent_runs RENAME COLUMN provider TO model;
ALTER TABLE agent_runs
    ADD CONSTRAINT agent_runs_only_gemini_4_argon CHECK (model = 'gemini-4-argon' AND thinking_level = 'high');

CREATE INDEX IF NOT EXISTS idx_agent_runs_updated_desc ON agent_runs (updated_at DESC);

CREATE TABLE IF NOT EXISTS gemini_calls (
    id BIGSERIAL PRIMARY KEY,
    run_id VARCHAR(64) NOT NULL,
    interaction_id TEXT NOT NULL DEFAULT '',
    model VARCHAR(64) NOT NULL CHECK (model = 'gemini-4-argon'),
    thinking_level VARCHAR(16) NOT NULL CHECK (thinking_level = 'high'),
    outcome VARCHAR(32) NOT NULL CHECK (outcome IN ('stored', 'invalid_output', 'duplicate')),
    idea_id VARCHAR(32) REFERENCES product_ideas(id) ON DELETE SET NULL,
    input_tokens BIGINT NOT NULL DEFAULT 0,
    output_tokens BIGINT NOT NULL DEFAULT 0,
    thought_tokens BIGINT NOT NULL DEFAULT 0,
    total_tokens BIGINT NOT NULL DEFAULT 0,
    error TEXT NOT NULL DEFAULT '',
    raw_text TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_gemini_calls_created_desc ON gemini_calls (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_gemini_calls_outcome ON gemini_calls (outcome);

COMMIT;
