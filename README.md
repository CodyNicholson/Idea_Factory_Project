# Idea Factory — Autonomous 5-Hour Startup & Product Intelligence Engine

An autonomous product-ideation, actuarial-scoring, and 14-point investor due-diligence engine grounded in:
* **[`Claude_Skills_Project`](file:///Users/codynicholson/workspace/Claude_Skills_Project/README.md)** (`software-intake-planner`, `visual-lab`, `design-game`, `claude-skill-factory`, `enterprise-fullstack-plugin`)
* **[`Business_Analyzer_Project`](file:///Users/codynicholson/workspace/Business_Analyzer_Project/README.md)** (Cox PH survival curves, LightGBM quantile yields, Israelsen Risk-Adjusted ROI math, SHAP causal attributions across 23 metros and 21 NAICS industries)
* **Sibling Workspace Assets** (`Kafka_Visual_Lab_Project`, `Rixus_RE_Project`, `Accounting_Backend_API_Project`, `Resume_Creator_Project`, `Airship_Blender_Assets_Project`, `Video_Game_Music_Generator_Project`, `Cameo_HoldEm_Project`)

---

## Key Outputs & Documentation

1. **[`docs/STARTUP_PATTERNS_AND_PLAYBOOK.md`](file:///Users/codynicholson/workspace/Idea_Factory_Project/docs/STARTUP_PATTERNS_AND_PLAYBOOK.md)** — Deep analysis answering:
   * *What are the most successful startup companies doing right now (2025–2026)?*
   * *What 8 repeatable patterns (`PAT-01`–`PAT-08`) can we follow to generate our own profitable products?*
   * *How does our Founder-Product Fit Matrix map onto high-survival NAICS verticals?*
2. **[`IDEAS_CATALOG.md`](file:///Users/codynicholson/workspace/Idea_Factory_Project/IDEAS_CATALOG.md)** — Master Markdown catalog ranked by **Israelsen Risk-Adjusted ROI Score (0–100)**, containing executive summaries, quantitative unit economics ($S(12)$, $S(60)$, 3-Yr IRR, LTV:CAC, Payback, Gross Margin, Founder Fit), and exhaustive answers to all **5 Core Sections & 14 Diligence Questions** for every product idea.
3. **[`docker-compose.yml`](file:///Users/codynicholson/workspace/Idea_Factory_Project/docker-compose.yml) & [`migrations/001_initial_idea_factory_schema.sql`](file:///Users/codynicholson/workspace/Idea_Factory_Project/migrations/001_initial_idea_factory_schema.sql)** — Production PostgreSQL 16 Docker container (`idea-factory-postgres` on `127.0.0.1:5435`) storing all product ideas (`product_ideas`), actuarial & unit-economics metrics (`idea_metrics`), normalized 14 investor diligence answers (`idea_diligence_questions`), and 5-hour agent telemetry (`agent_runs`), synced automatically with [`data/ideas.json`](file:///Users/codynicholson/workspace/Idea_Factory_Project/data/ideas.json) & `data/idea_factory.db`.

---

## Quick Start (Docker PostgreSQL + Zero External Python Dependencies)

```bash
# 0. Spin up the Docker PostgreSQL 16 database (port 5435) and apply SQL migrations
docker compose up -d --wait
python3 -m idea_factory migrate
python3 -m idea_factory db-status

# 1. Seed & generate the initial product ideas catalog
python3 -m idea_factory seed

# 2. Synthesize and append 1 new product idea immediately
python3 -m idea_factory generate-one

# 3. Run the 5-Hour Continuous Autonomous Loop Agent (runs for 5 hours or until AI credits are exhausted)
./run_5hr_agent.sh
# Or with custom parameters:
python3 -m idea_factory run --hours 5.0 --interval 45

# 4. Deterministically verify all ideas against the 14-question schema & actuarial invariants
python3 -m idea_factory verify

# 5. Launch the interactive Web Dashboard & API Server (http://127.0.0.1:8020)
python3 -m idea_factory serve --port 8020

# 6. Run the automated unit & integration test suite
python3 -m unittest discover -s tests -v
```

---

## How the 5-Hour Autonomous Agent Loop Works

`idea_factory/agent.py` runs in a continuous loop bounded by `AGENT_MAX_HOURS=5.0` (18,000 seconds) and automatically detects AI credit/quota exhaustion (`HTTP 402`, `HTTP 429` rate-limit/quota errors, `insufficient_quota`, or `claude -p` 5-hour session limits):

1. **Provider Priority (`idea_factory/generator.py`):**
   * `anthropic` (`ANTHROPIC_API_KEY`) -> `claude_cli` (`claude -p`) -> `gemini` (`GEMINI_API_KEY`) -> `openai` (`OPENAI_API_KEY`) -> `openrouter` (`OPENROUTER_API_KEY`) -> `synthesis` (Built-in Actuarial & Combinatorial Synthesis Engine + live HN Algolia signals).
2. ** Quantitative Scoring (`idea_factory/scoring.py`):**
   * Fits a Weibull survival curve through 1-year ($S_{12}$) and 5-year ($S_{60}$) survival probabilities.
   * Computes Israelsen-corrected Risk-Adjusted ROI:
     $$\text{raw} = \frac{S_{60} \cdot (\text{EBITDA}/\text{CapEx}) - (1 - S_{60}) \cdot \text{LGD}}{\sigma_{\text{sector}}}$$
   * Maps to a 0–100 score and solves for the 3-year survival-weighted IRR, LTV, LTV:CAC ratio, and CAC payback months.
3. **Deterministic Validation (`idea_factory/models.py`):**
   * Every generated idea is checked by `validate_idea()` to ensure all 14 diligence questions across the 5 required sections are thoroughly answered before atomic persistence to SQLite, `data/ideas.json`, and `IDEAS_CATALOG.md`.

