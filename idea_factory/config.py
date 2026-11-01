"""Environment-driven settings for the Idea Factory 5-Hour Autonomous Agent."""
from __future__ import annotations

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = ROOT_DIR / "docs"
WEB_DIR = ROOT_DIR / "web"

IDEAS_JSON_PATH = DATA_DIR / "ideas.json"
AGENT_STATE_PATH = DATA_DIR / "agent_state.json"
SQLITE_DB_PATH = DATA_DIR / "idea_factory.db"
CATALOG_MD_PATH = ROOT_DIR / "IDEAS_CATALOG.md"
PATTERNS_MD_PATH = DOCS_DIR / "STARTUP_PATTERNS_AND_PLAYBOOK.md"
MIGRATIONS_DIR = ROOT_DIR / "migrations"

# Sibling workspace references
WORKSPACE_DIR = ROOT_DIR.parent
CLAUDE_SKILLS_DIR = Path(
    os.getenv("CLAUDE_SKILLS_DIR", str(WORKSPACE_DIR / "Claude_Skills_Project"))
)
BUSINESS_ANALYZER_DIR = Path(
    os.getenv("BUSINESS_ANALYZER_DIR", str(WORKSPACE_DIR / "Business_Analyzer_Project"))
)


def _load_dotenv() -> None:
    """Load key=value pairs from .env if present (zero external dependencies)."""
    env_file = ROOT_DIR / ".env"
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        # Strip inline comments if unquoted
        if "#" in val and not (val.strip().startswith('"') or val.strip().startswith("'")):
            val = val.split("#", 1)[0]
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


_load_dotenv()

# LLM Provider Configuration
IDEA_LLM_PROVIDER = os.getenv("IDEA_LLM_PROVIDER", "").strip().lower()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5").strip()
GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")).strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-pro").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "google/gemma-4-31b-it:free,nvidia/nemotron-3.5-super-vl:free",
).strip()

# 5-Hour Continuous Loop Configuration
AGENT_MAX_HOURS = float(os.getenv("AGENT_MAX_HOURS", "5.0"))
AGENT_MAX_RUNTIME_SECONDS = int(AGENT_MAX_HOURS * 3600)
AGENT_LOOP_INTERVAL_SECONDS = float(os.getenv("AGENT_LOOP_INTERVAL_SECONDS", "45.0"))
AGENT_MAX_CREDIT_USD = float(os.getenv("AGENT_MAX_CREDIT_USD", "50.0"))
AGENT_STOP_ON_RATE_LIMIT = os.getenv("AGENT_STOP_ON_RATE_LIMIT", "true").lower() in ("1", "true", "yes")
LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "120.0"))

# Public signal scrapers
SEC_USER_AGENT = os.getenv("SEC_USER_AGENT", "IdeaFactory/1.0 (research@ideafactory.local)")
PORT = int(os.getenv("PORT", "8020"))

# PostgreSQL Database Configuration (Docker container: idea-factory-postgres)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1").strip()
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5435"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "idea_factory").strip()
POSTGRES_USER = os.getenv("POSTGRES_USER", "idea_factory").strip()
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "idea_factory_password").strip()
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
).strip()


