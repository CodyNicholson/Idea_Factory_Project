# Idea Factory

Generates product ideas continuously with **Gemini 4 Argon at High effort**, scores them, and stores
everything in PostgreSQL running in Docker.

## Quick start

1. Run `./run_agent.sh --db-only`. This creates `.env` with a random database password and starts PostgreSQL. It spends no tokens.
2. Add a paid-tier key to `.env` as `GEMINI_API_KEY=...`. Gemini 4 Argon is not on the free tier.
3. **Set a spend limit first** (see [Cost](#cost)), because the agent runs until the allowance runs out.
4. Run `./run_agent.sh` to build and start the agent.

```bash
docker compose logs -f agent         # follow the agent
docker compose --profile agent stop agent   # stop generating
python3 -m idea_factory serve        # read-only dashboard on http://127.0.0.1:8020
```

## Model

Only `gemini-4-argon` with `thinking_level: high` is used. There is no fallback model and no template engine.

- The model and effort are constants in `idea_factory/config.py`, so no environment setting can change them.
- The agent stops if a response reports a different model.
- Database `CHECK` constraints on `gemini_calls` and `agent_runs` refuse any other model or effort.

## When the tokens run out

The Gemini API has no single token window, so the agent reads each error and waits accordingly:

| Signal | Meaning | What the agent does |
| :--- | :--- | :--- |
| 429, per-minute or rate limit | Short-term limit reached | Waits for Google's retry hint, otherwise backs off up to 1 hour |
| 429, per-day or `quota_exceeded` | Daily quota used up | Waits until midnight Pacific time, when it resets |
| 402, or a credit or spend-cap message | Prepay credits or spend cap used up | Retries hourly, and resumes after the 1st of the month or once credits are added |
| 5xx, 408 or a network error | Temporary failure | Backs off up to 1 hour |
| 401, 403, 404, other 400, or a 429 with `limit: 0` | Bad key, wrong tier or bad request | Exits with an error, and Docker restarts the container |

The wait reason and resume time are saved in `agent_runs`. Because the next idea's id and context come from
the database, the agent resumes correctly after a restart or a reboot.

## Data

All data lives in the Docker volume `idea_factory_pgdata`, mounted at `/var/lib/postgresql/data`. It is
declared `external`, so stopping or removing the container, `docker compose down` and even
`docker compose down -v` all leave it in place. Only `docker volume rm idea_factory_pgdata` deletes it.

PostgreSQL listens on `127.0.0.1:5435` only.

| Table | Contents |
| :--- | :--- |
| `product_ideas` | Every idea, including the full JSON document |
| `idea_metrics` | Actuarial and unit-economics metrics |
| `idea_diligence_questions` | The 14 diligence answers, one row each |
| `gemini_calls` | Every billed call: tokens, outcome, raw answer (including rejected answers) |
| `agent_runs` | Agent status, token totals, wait reason and resume time |

`generation_source` separates the sources: `GEMINI_4_ARGON_HIGH` for new ideas, and
`WORKSPACE_SYNTHESIS` or `AUTONOMOUS_LOOP_SYNTHESIS` for the 879 ideas imported from the old
template engine.

## Commands

```bash
python3 -m idea_factory status      # latest agent run
python3 -m idea_factory db-status   # connection, migrations, row counts, portfolio metrics
python3 -m idea_factory verify      # validate all stored ideas
python3 -m idea_factory catalog     # export all ideas to IDEAS_CATALOG.md (git-ignored)
python3 -m idea_factory rescore     # recalculate scores for all stored ideas
python3 -m idea_factory run --max-iterations 1   # store one idea, then exit
python3 -m unittest discover -s tests            # tests (no tokens spent; integration tests need PostgreSQL)
```

Each idea's scores come from `idea_factory/scoring.py`, which blends the model's estimates toward industry
benchmarks. `validate_idea` in `idea_factory/models.py` must pass before an idea is stored.

## Cost

Gemini 4 Argon costs $2 per 1M input tokens and $10 per 1M output and thinking tokens until November 30, 2026,
then $4 and $20. The agent has no budget of its own: it stops only when Google stops it.

Set a limit before starting, in one of these ways:

- A **project spend cap** on the AI Studio Spend page. This is the safest option because it affects only this project.
- **Prepay credits** with auto-reload off.

Avoid relying on the account-wide tier cap, or on depleting prepay credits on a shared billing account. Either
one pauses every project on that billing account, not just this one.
