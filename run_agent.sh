#!/usr/bin/env bash
# Starts PostgreSQL and the continuous Gemini 4 Argon idea agent in Docker.
# Usage: ./run_agent.sh            start the database and the agent
#        ./run_agent.sh --db-only  start only the database (spends no tokens)
set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  cp .env.example .env
  sed -i "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$(openssl rand -hex 24)/" .env
  chmod 600 .env
  echo "Created .env with a random database password."
fi

docker volume create idea_factory_pgdata >/dev/null

if [[ "${1:-}" == "--db-only" ]]; then
  docker compose up -d --wait postgres
  exit 0
fi

if ! grep -Eq '^GEMINI_API_KEY=.+' .env; then
  echo "GEMINI_API_KEY is empty. Add a paid-tier key to .env, then run this again." >&2
  exit 1
fi

docker compose --profile agent up -d --build --wait postgres
docker compose --profile agent up -d --build agent
echo "Agent started. Follow it with: docker compose logs -f agent"
