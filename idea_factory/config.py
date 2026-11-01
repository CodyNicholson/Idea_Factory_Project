"""Environment-driven settings for the Idea Factory agent."""
from __future__ import annotations

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = ROOT_DIR / "web"
MIGRATIONS_DIR = ROOT_DIR / "migrations"
CATALOG_MD_PATH = ROOT_DIR / "IDEAS_CATALOG.md"

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

# The only model this project may use. These are deliberately constants, not
# environment settings, so no .env value can switch the model or lower the effort.
GEMINI_MODEL = "gemini-4-argon"
GEMINI_THINKING_LEVEL = "high"
GENERATION_SOURCE = "GEMINI_4_ARGON_HIGH"
GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")).strip()

# Google recommends at least 32,768 and a client timeout of 15 minutes for this model.
# Thinking tokens count toward this cap, so a low value truncates the answer.
GEMINI_MAX_OUTPUT_TOKENS = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "65536"))
GEMINI_TIMEOUT_SECONDS = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "900"))

# Agent loop
AGENT_LOOP_INTERVAL_SECONDS = float(os.getenv("AGENT_LOOP_INTERVAL_SECONDS", "5"))

# Public signal scrapers
SEC_USER_AGENT = os.getenv("SEC_USER_AGENT", "IdeaFactory/1.0 (research@ideafactory.local)")
PORT = int(os.getenv("PORT", "8020"))

# PostgreSQL (Docker container: idea-factory-postgres)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1").strip()
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5435"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "idea_factory").strip()
POSTGRES_USER = os.getenv("POSTGRES_USER", "idea_factory").strip()
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "").strip()
