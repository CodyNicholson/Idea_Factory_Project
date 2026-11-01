"""Zero-dependency PostgreSQL v3 Wire-Protocol Client, Migration Runner & Idea Store."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import math
import secrets
import socket
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import config
from .gemini import GeminiCall
from .models import ProductIdea

# Arbitrary fixed key for the advisory lock that keeps a single agent running per database.
AGENT_LOCK_KEY = 7246310955


class PostgresError(RuntimeError):
    """Raised when PostgreSQL returns an ErrorResponse ('E') or connection error."""

    def __init__(self, message: str, sqlstate: str | None = None) -> None:
        super().__init__(message)
        self.sqlstate = sqlstate


def is_transient_db_error(exc: BaseException) -> bool:
    """True for connection-level failures worth retrying, False when the statement itself was rejected."""
    if isinstance(exc, OSError):
        return True
    if isinstance(exc, PostgresError):
        return exc.sqlstate is None or exc.sqlstate[:2] in ("08", "53", "57")
    return False


def pg_literal(val: Any) -> str:
    """Safely format a Python value as a PostgreSQL literal for simple-query execution."""
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if isinstance(val, float) and not math.isfinite(val):
        return "NULL"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, (list, tuple)):
        if not val:
            return "'{}'::text[]"
        items = ", ".join(pg_literal(str(x)) for x in val)
        return f"ARRAY[{items}]::text[]"
    if isinstance(val, dict):
        return f"{pg_literal(json.dumps(val, ensure_ascii=False))}::jsonb"
    # PostgreSQL text cannot hold NUL, and NUL would end a simple-query message early.
    s = str(val).replace("\x00", "").replace("'", "''")
    if "\\" in s:
        s = s.replace("\\", "\\\\")
        return f"E'{s}'"
    return f"'{s}'"


class PostgresWireClient:
    """Pure-Python PostgreSQL v3 wire-protocol client (supports trust, md5, and SCRAM-SHA-256)."""

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        user: str | None = None,
        password: str | None = None,
        database: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.host = host or config.POSTGRES_HOST
        self.port = port or config.POSTGRES_PORT
        self.user = user or config.POSTGRES_USER
        self.password = config.POSTGRES_PASSWORD if password is None else password
        self.database = database or config.POSTGRES_DB
        self.timeout = timeout
        self._sock: socket.socket | None = None

    def __enter__(self) -> PostgresWireClient:
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def connect(self) -> None:
        self._sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        params = (
            b"user\x00" + self.user.encode("utf-8") + b"\x00"
            b"database\x00" + self.database.encode("utf-8") + b"\x00"
            b"client_encoding\x00UTF8\x00\x00"
        )
        startup = struct.pack("!II", len(params) + 8, 196608) + params
        self._sock.sendall(startup)

        while True:
            msg_type, body = self._read_msg()
            if msg_type == b"R":
                auth_code = struct.unpack("!I", body[:4])[0]
                if auth_code == 0:
                    continue
                elif auth_code == 3:
                    pw = self.password.encode("utf-8") + b"\x00"
                    self._send_msg(b"p", pw)
                elif auth_code == 5:
                    salt = body[4:8]
                    inner = hashlib.md5((self.password + self.user).encode("utf-8")).hexdigest().encode("ascii")
                    digest = "md5" + hashlib.md5(inner + salt).hexdigest()
                    self._send_msg(b"p", digest.encode("ascii") + b"\x00")
                elif auth_code == 10:
                    self._handle_scram_sha256()
                else:
                    raise PostgresError(f"Unsupported PostgreSQL auth code: {auth_code}")
            elif msg_type == b"E":
                raise self._error_from(body)
            elif msg_type == b"Z":
                break

    def _handle_scram_sha256(self) -> None:
        c_nonce = base64.b64encode(secrets.token_bytes(18)).decode("ascii")
        client_first_bare = f"n=,r={c_nonce}"
        client_first = f"n,,{client_first_bare}".encode("utf-8")
        sasl_init = b"SCRAM-SHA-256\x00" + struct.pack("!I", len(client_first)) + client_first
        self._send_msg(b"p", sasl_init)

        msg_type, body = self._read_msg()
        if msg_type == b"E":
            raise self._error_from(body)
        auth_code = struct.unpack("!I", body[:4])[0]
        if auth_code != 11:
            raise PostgresError(f"Expected SASLContinue (11), got {auth_code}")
        server_first = body[4:].decode("utf-8")
        parts = dict(item.split("=", 1) for item in server_first.split(","))
        r_nonce = parts["r"]
        salt = base64.b64decode(parts["s"])
        iterations = int(parts["i"])

        salted_pw = hashlib.pbkdf2_hmac("sha256", self.password.encode("utf-8"), salt, iterations)
        client_key = hmac.new(salted_pw, b"Client Key", hashlib.sha256).digest()
        stored_key = hashlib.sha256(client_key).digest()
        client_final_no_proof = f"c=biws,r={r_nonce}"
        auth_msg = f"{client_first_bare},{server_first},{client_final_no_proof}".encode("utf-8")
        client_sig = hmac.new(stored_key, auth_msg, hashlib.sha256).digest()
        proof = bytes(a ^ b for a, b in zip(client_key, client_sig))
        client_final = f"{client_final_no_proof},p={base64.b64encode(proof).decode('ascii')}".encode("utf-8")
        self._send_msg(b"p", client_final)

        msg_type, body = self._read_msg()
        if msg_type == b"E":
            raise self._error_from(body)

    def execute(self, sql: str) -> list[dict[str, Any]]:
        """Execute a SQL statement or multi-statement script and return any result rows."""
        if not self._sock:
            self.connect()
        payload = sql.encode("utf-8") + b"\x00"
        self._send_msg(b"Q", payload)
        columns: list[str] = []
        rows: list[dict[str, Any]] = []
        first_error: PostgresError | None = None

        while True:
            msg_type, body = self._read_msg()
            if msg_type == b"T":
                columns = self._parse_row_description(body)
            elif msg_type == b"D":
                rows.append(self._parse_data_row(body, columns))
            elif msg_type == b"E":
                first_error = first_error or self._error_from(body)
            elif msg_type == b"Z":
                break
        if first_error:
            raise first_error
        return rows

    def close(self) -> None:
        if self._sock:
            try:
                self._send_msg(b"X", b"")
            except Exception:
                pass
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None

    def _send_msg(self, msg_type: bytes, payload: bytes) -> None:
        assert self._sock is not None
        header = msg_type + struct.pack("!I", len(payload) + 4)
        self._sock.sendall(header + payload)

    def _recv_exact(self, n: int) -> bytes:
        assert self._sock is not None
        buf = bytearray()
        while len(buf) < n:
            chunk = self._sock.recv(n - len(buf))
            if not chunk:
                raise PostgresError("PostgreSQL socket closed unexpectedly")
            buf.extend(chunk)
        return bytes(buf)

    def _read_msg(self) -> tuple[bytes, bytes]:
        msg_type = self._recv_exact(1)
        length = struct.unpack("!I", self._recv_exact(4))[0]
        body = self._recv_exact(length - 4) if length > 4 else b""
        return msg_type, body

    @staticmethod
    def _error_from(body: bytes) -> PostgresError:
        parts = body.split(b"\x00")
        fields = {p[:1]: p[1:].decode("utf-8", errors="replace") for p in parts if p}
        message = f"{fields.get(b'S', 'ERROR')}: {fields.get(b'M', 'Unknown error')} ({fields.get(b'D', '')})"
        return PostgresError(message, sqlstate=fields.get(b"C"))

    @staticmethod
    def _parse_row_description(body: bytes) -> list[str]:
        num_fields = struct.unpack("!H", body[:2])[0]
        pos = 2
        cols: list[str] = []
        for _ in range(num_fields):
            end = body.index(b"\x00", pos)
            cols.append(body[pos:end].decode("utf-8"))
            pos = end + 1 + 18
        return cols

    @staticmethod
    def _parse_data_row(body: bytes, columns: list[str]) -> dict[str, Any]:
        num_cols = struct.unpack("!H", body[:2])[0]
        pos = 2
        row: dict[str, Any] = {}
        for idx in range(num_cols):
            col_len = struct.unpack("!i", body[pos : pos + 4])[0]
            pos += 4
            col_name = columns[idx] if idx < len(columns) else f"col_{idx}"
            if col_len == -1:
                row[col_name] = None
            else:
                row[col_name] = body[pos : pos + col_len].decode("utf-8", errors="replace")
                pos += col_len
        return row


DILIGENCE_QUESTION_SPECS: list[tuple[int, str, str, str, str]] = [
    (1, "1.1", "1. Product & Problem-Solving", "acuteness_of_problem", "How acute is the problem?"),
    (1, "1.2", "1. Product & Problem-Solving", "ten_x_better_solution", "Is the solution 10x better?"),
    (1, "1.3", "1. Product & Problem-Solving", "usage_and_retention_metrics", "What are the usage and retention metrics?"),
    (2, "2.1", "2. Market & Competition", "tam_and_growth_tailwinds", "How big is the market and is it growing?"),
    (2, "2.2", "2. Market & Competition", "competition_and_defensible_edge", "Who is the competition and what is the 'edge'?"),
    (2, "2.3", "2. Market & Competition", "why_customers_switch", "Why do customers switch?"),
    (3, "3.1", "3. Business Model & Traction", "cac_ltv_and_payback", "What does customer acquisition look like?"),
    (3, "3.2", "3. Business Model & Traction", "nature_of_revenue", "What is the nature of the revenue?"),
    (3, "3.3", "3. Business Model & Traction", "actual_paying_customers", "Who are the actual paying customers?"),
    (4, "4.1", "4. Financials & Runway", "burn_rate_and_runway", "What is the burn rate and runway?"),
    (4, "4.2", "4. Financials & Runway", "unit_economics_scaling", "Are unit economics improving?"),
    (4, "4.3", "4. Financials & Runway", "fundraising_and_cap_table", "What are the fundraising and cap table realities?"),
    (5, "5.1", "5. Team & Execution", "founder_product_fit", "Do they have founder-product fit?"),
    (5, "5.2", "5. Team & Execution", "pressure_and_pivot_playbook", "How do they handle pressure and pivot?"),
]


def is_postgres_available(timeout: float = 1.5) -> bool:
    """Return True if the Docker PostgreSQL database is reachable."""
    try:
        with PostgresWireClient(timeout=timeout) as client:
            client.execute("SELECT 1;")
        return True
    except Exception:
        return False


def run_migrations(migrations_dir: Path = config.MIGRATIONS_DIR) -> list[str]:
    """Apply pending SQL migration files in `migrations/` (skips versions already recorded in schema_migrations)."""
    applied: list[str] = []
    sql_files = sorted(migrations_dir.glob("*.sql"))
    with PostgresWireClient() as client:
        client.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            "version VARCHAR(64) PRIMARY KEY, filename TEXT NOT NULL, "
            "checksum VARCHAR(64) NOT NULL, applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW());"
        )
        done = {r["version"]: r["checksum"] for r in client.execute("SELECT version, checksum FROM schema_migrations;")}
        for sql_file in sql_files:
            content = sql_file.read_text(encoding="utf-8")
            checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()
            version = sql_file.stem.split("_", 1)[0]
            if version in done:
                if done[version] != checksum:
                    print(
                        f"WARNING: migration {sql_file.name} changed after being applied; "
                        "create a new numbered migration instead of editing an applied one.",
                        file=sys.stderr,
                    )
                continue
            client.execute(content)
            record_sql = (
                "INSERT INTO schema_migrations (version, filename, checksum, applied_at) VALUES ("
                f"{pg_literal(version)}, {pg_literal(sql_file.name)}, {pg_literal(checksum)}, NOW()"
                ") ON CONFLICT (version) DO UPDATE SET "
                "filename = EXCLUDED.filename, checksum = EXCLUDED.checksum, applied_at = NOW();"
            )
            client.execute(record_sql)
            applied.append(sql_file.name)
    return applied


def _idea_to_upsert_sql(idea: ProductIdea) -> str:
    """Build idempotent PostgreSQL UPSERT statements for `product_ideas`, `idea_metrics`, and `idea_diligence_questions`."""
    created_ts = idea.created_at or datetime.now(timezone.utc).isoformat()
    p1 = idea.product_and_problem_solving
    p2 = idea.market_and_competition
    p3 = idea.business_model_and_traction
    p4 = idea.financials_and_runway
    p5 = idea.team_and_execution
    payload_dict = idea.to_dict()

    q_map = {
        "acuteness_of_problem": p1.acuteness_of_problem,
        "ten_x_better_solution": p1.ten_x_better_solution,
        "usage_and_retention_metrics": p1.usage_and_retention_metrics,
        "tam_and_growth_tailwinds": p2.tam_and_growth_tailwinds,
        "competition_and_defensible_edge": p2.competition_and_defensible_edge,
        "why_customers_switch": p2.why_customers_switch,
        "cac_ltv_and_payback": p3.cac_ltv_and_payback,
        "nature_of_revenue": p3.nature_of_revenue,
        "actual_paying_customers": p3.actual_paying_customers,
        "burn_rate_and_runway": p4.burn_rate_and_runway,
        "unit_economics_scaling": p4.unit_economics_scaling,
        "fundraising_and_cap_table": p4.fundraising_and_cap_table,
        "founder_product_fit": p5.founder_product_fit,
        "pressure_and_pivot_playbook": p5.pressure_and_pivot_playbook,
    }

    sql_parts = [
        f"""
        INSERT INTO product_ideas (
            id, slug, title, tagline, summary, category, naics_code, industry_name,
            business_archetype, target_metro, pattern_ids, referenced_skills,
            referenced_projects, causal_drivers, mitigated_failure_modes,
            roi_score, survival_1yr, survival_5yr, projected_3yr_irr_pct,
            initial_capex_usd, steady_state_ebitda_usd, annual_contract_value_usd,
            cac_usd, ltv_usd, ltv_cac_ratio, payback_months, gross_margin_pct,
            monthly_burn_usd, runway_months, founder_fit_score,
            annual_churn_pct, capital_required_usd, customers_to_steady_state,
            customer_segment, scoring_version, scoring_inputs,
            acuteness_of_problem, ten_x_better_solution, usage_and_retention_metrics,
            tam_and_growth_tailwinds, competition_and_defensible_edge, why_customers_switch,
            cac_ltv_and_payback, nature_of_revenue, actual_paying_customers,
            burn_rate_and_runway, unit_economics_scaling, fundraising_and_cap_table,
            founder_product_fit, pressure_and_pivot_playbook,
            generation_source, signal_inspiration, created_at, updated_at, payload_json
        ) VALUES (
            {pg_literal(idea.id)}, {pg_literal(idea.slug)}, {pg_literal(idea.title)},
            {pg_literal(idea.tagline)}, {pg_literal(idea.summary)}, {pg_literal(idea.category)},
            {pg_literal(idea.naics_code)}, {pg_literal(idea.industry_name)},
            {pg_literal(idea.business_archetype)}, {pg_literal(idea.target_metro)},
            {pg_literal(idea.pattern_ids)}, {pg_literal(idea.referenced_skills)},
            {pg_literal(idea.referenced_projects)}, {pg_literal(idea.causal_drivers)},
            {pg_literal(idea.mitigated_failure_modes)},
            {pg_literal(idea.roi_score)}, {pg_literal(idea.survival_1yr)}, {pg_literal(idea.survival_5yr)},
            {pg_literal(idea.projected_3yr_irr_pct)}, {pg_literal(idea.initial_capex_usd)},
            {pg_literal(idea.steady_state_ebitda_usd)}, {pg_literal(idea.annual_contract_value_usd)},
            {pg_literal(idea.cac_usd)}, {pg_literal(idea.ltv_usd)}, {pg_literal(idea.ltv_cac_ratio)},
            {pg_literal(idea.payback_months)}, {pg_literal(idea.gross_margin_pct)},
            {pg_literal(idea.monthly_burn_usd)}, {pg_literal(idea.runway_months)},
            {pg_literal(idea.founder_fit_score)},
            {pg_literal(idea.annual_churn_pct)}, {pg_literal(idea.capital_required_usd)},
            {pg_literal(idea.customers_to_steady_state)}, {pg_literal(idea.customer_segment)},
            {pg_literal(idea.scoring_version)}, {pg_literal(idea.scoring_inputs)},
            {pg_literal(p1.acuteness_of_problem)}, {pg_literal(p1.ten_x_better_solution)},
            {pg_literal(p1.usage_and_retention_metrics)}, {pg_literal(p2.tam_and_growth_tailwinds)},
            {pg_literal(p2.competition_and_defensible_edge)}, {pg_literal(p2.why_customers_switch)},
            {pg_literal(p3.cac_ltv_and_payback)}, {pg_literal(p3.nature_of_revenue)},
            {pg_literal(p3.actual_paying_customers)}, {pg_literal(p4.burn_rate_and_runway)},
            {pg_literal(p4.unit_economics_scaling)}, {pg_literal(p4.fundraising_and_cap_table)},
            {pg_literal(p5.founder_product_fit)}, {pg_literal(p5.pressure_and_pivot_playbook)},
            {pg_literal(idea.generation_source)}, {pg_literal(idea.signal_inspiration)},
            {pg_literal(created_ts)}::timestamptz, NOW(), {pg_literal(payload_dict)}
        )
        ON CONFLICT (id) DO UPDATE SET
            slug = EXCLUDED.slug,
            title = EXCLUDED.title,
            tagline = EXCLUDED.tagline,
            summary = EXCLUDED.summary,
            category = EXCLUDED.category,
            naics_code = EXCLUDED.naics_code,
            industry_name = EXCLUDED.industry_name,
            business_archetype = EXCLUDED.business_archetype,
            target_metro = EXCLUDED.target_metro,
            pattern_ids = EXCLUDED.pattern_ids,
            referenced_skills = EXCLUDED.referenced_skills,
            referenced_projects = EXCLUDED.referenced_projects,
            causal_drivers = EXCLUDED.causal_drivers,
            mitigated_failure_modes = EXCLUDED.mitigated_failure_modes,
            roi_score = EXCLUDED.roi_score,
            survival_1yr = EXCLUDED.survival_1yr,
            survival_5yr = EXCLUDED.survival_5yr,
            projected_3yr_irr_pct = EXCLUDED.projected_3yr_irr_pct,
            initial_capex_usd = EXCLUDED.initial_capex_usd,
            steady_state_ebitda_usd = EXCLUDED.steady_state_ebitda_usd,
            annual_contract_value_usd = EXCLUDED.annual_contract_value_usd,
            cac_usd = EXCLUDED.cac_usd,
            ltv_usd = EXCLUDED.ltv_usd,
            ltv_cac_ratio = EXCLUDED.ltv_cac_ratio,
            payback_months = EXCLUDED.payback_months,
            gross_margin_pct = EXCLUDED.gross_margin_pct,
            monthly_burn_usd = EXCLUDED.monthly_burn_usd,
            runway_months = EXCLUDED.runway_months,
            founder_fit_score = EXCLUDED.founder_fit_score,
            annual_churn_pct = EXCLUDED.annual_churn_pct,
            capital_required_usd = EXCLUDED.capital_required_usd,
            customers_to_steady_state = EXCLUDED.customers_to_steady_state,
            customer_segment = EXCLUDED.customer_segment,
            scoring_version = EXCLUDED.scoring_version,
            scoring_inputs = EXCLUDED.scoring_inputs,
            acuteness_of_problem = EXCLUDED.acuteness_of_problem,
            ten_x_better_solution = EXCLUDED.ten_x_better_solution,
            usage_and_retention_metrics = EXCLUDED.usage_and_retention_metrics,
            tam_and_growth_tailwinds = EXCLUDED.tam_and_growth_tailwinds,
            competition_and_defensible_edge = EXCLUDED.competition_and_defensible_edge,
            why_customers_switch = EXCLUDED.why_customers_switch,
            cac_ltv_and_payback = EXCLUDED.cac_ltv_and_payback,
            nature_of_revenue = EXCLUDED.nature_of_revenue,
            actual_paying_customers = EXCLUDED.actual_paying_customers,
            burn_rate_and_runway = EXCLUDED.burn_rate_and_runway,
            unit_economics_scaling = EXCLUDED.unit_economics_scaling,
            fundraising_and_cap_table = EXCLUDED.fundraising_and_cap_table,
            founder_product_fit = EXCLUDED.founder_product_fit,
            pressure_and_pivot_playbook = EXCLUDED.pressure_and_pivot_playbook,
            generation_source = EXCLUDED.generation_source,
            signal_inspiration = EXCLUDED.signal_inspiration,
            updated_at = NOW(),
            payload_json = EXCLUDED.payload_json;
        """,
        f"""
        INSERT INTO idea_metrics (
            idea_id, roi_score, survival_1yr, survival_5yr, projected_3yr_irr_pct,
            initial_capex_usd, steady_state_ebitda_usd, annual_contract_value_usd,
            cac_usd, ltv_usd, ltv_cac_ratio, payback_months, gross_margin_pct,
            monthly_burn_usd, runway_months, founder_fit_score,
            annual_churn_pct, capital_required_usd, customers_to_steady_state,
            customer_segment, scoring_version, updated_at
        ) VALUES (
            {pg_literal(idea.id)}, {pg_literal(idea.roi_score)}, {pg_literal(idea.survival_1yr)},
            {pg_literal(idea.survival_5yr)}, {pg_literal(idea.projected_3yr_irr_pct)},
            {pg_literal(idea.initial_capex_usd)}, {pg_literal(idea.steady_state_ebitda_usd)},
            {pg_literal(idea.annual_contract_value_usd)}, {pg_literal(idea.cac_usd)},
            {pg_literal(idea.ltv_usd)}, {pg_literal(idea.ltv_cac_ratio)},
            {pg_literal(idea.payback_months)}, {pg_literal(idea.gross_margin_pct)},
            {pg_literal(idea.monthly_burn_usd)}, {pg_literal(idea.runway_months)},
            {pg_literal(idea.founder_fit_score)},
            {pg_literal(idea.annual_churn_pct)}, {pg_literal(idea.capital_required_usd)},
            {pg_literal(idea.customers_to_steady_state)}, {pg_literal(idea.customer_segment)},
            {pg_literal(idea.scoring_version)}, NOW()
        )
        ON CONFLICT (idea_id) DO UPDATE SET
            roi_score = EXCLUDED.roi_score,
            survival_1yr = EXCLUDED.survival_1yr,
            survival_5yr = EXCLUDED.survival_5yr,
            projected_3yr_irr_pct = EXCLUDED.projected_3yr_irr_pct,
            initial_capex_usd = EXCLUDED.initial_capex_usd,
            steady_state_ebitda_usd = EXCLUDED.steady_state_ebitda_usd,
            annual_contract_value_usd = EXCLUDED.annual_contract_value_usd,
            cac_usd = EXCLUDED.cac_usd,
            ltv_usd = EXCLUDED.ltv_usd,
            ltv_cac_ratio = EXCLUDED.ltv_cac_ratio,
            payback_months = EXCLUDED.payback_months,
            gross_margin_pct = EXCLUDED.gross_margin_pct,
            monthly_burn_usd = EXCLUDED.monthly_burn_usd,
            runway_months = EXCLUDED.runway_months,
            founder_fit_score = EXCLUDED.founder_fit_score,
            annual_churn_pct = EXCLUDED.annual_churn_pct,
            capital_required_usd = EXCLUDED.capital_required_usd,
            customers_to_steady_state = EXCLUDED.customers_to_steady_state,
            customer_segment = EXCLUDED.customer_segment,
            scoring_version = EXCLUDED.scoring_version,
            updated_at = NOW();
        """,
    ]

    q_values = []
    for sec_num, q_num, sec_title, q_key, q_prompt in DILIGENCE_QUESTION_SPECS:
        ans = q_map[q_key]
        q_values.append(
            f"({pg_literal(idea.id)}, {sec_num}, {pg_literal(q_num)}, "
            f"{pg_literal(sec_title)}, {pg_literal(q_key)}, {pg_literal(q_prompt)}, {pg_literal(ans)}, NOW())"
        )
    sql_parts.append(
        "INSERT INTO idea_diligence_questions ("
        "idea_id, section_number, question_number, section_title, question_key, question_prompt, answer_text, updated_at"
        ") VALUES "
        + ", ".join(q_values)
        + " ON CONFLICT (idea_id, question_number) DO UPDATE SET "
        "answer_text = EXCLUDED.answer_text, updated_at = NOW();"
    )
    return "\n".join(sql_parts)


def upsert_ideas_postgres(ideas: list[ProductIdea], chunk_size: int = 25) -> int:
    """Upsert one or more ProductIdeas (and their metrics & 14 diligence questions) into PostgreSQL."""
    if not ideas:
        return 0
    with PostgresWireClient() as client:
        for i in range(0, len(ideas), chunk_size):
            batch = ideas[i : i + chunk_size]
            stmts = ["BEGIN;"] + [_idea_to_upsert_sql(idea) for idea in batch] + ["COMMIT;"]
            client.execute("\n".join(stmts))
    return len(ideas)


def load_ideas_postgres() -> list[ProductIdea]:
    """Load all ProductIdeas from PostgreSQL ordered by Risk-Adjusted ROI score descending."""
    with PostgresWireClient() as client:
        rows = client.execute("SELECT payload_json FROM product_ideas ORDER BY roi_score DESC, id ASC;")
    return [ProductIdea.from_dict(json.loads(r["payload_json"])) for r in rows if r.get("payload_json")]


def upsert_agent_state_postgres(state: dict[str, Any]) -> None:
    """Persist the agent loop telemetry into `agent_runs`."""
    sql = f"""
    INSERT INTO agent_runs (
        run_id, started_at, updated_at, status, model, thinking_level, elapsed_seconds,
        ideas_generated, ideas_rejected, ideas_count, api_calls, input_tokens, output_tokens,
        thought_tokens, refresh_waits, resume_at, last_idea_id, stop_reason, state_json
    ) VALUES (
        {pg_literal(state["run_id"])}, {pg_literal(state["started_at"])}::timestamptz,
        {pg_literal(state["updated_at"])}::timestamptz, {pg_literal(state["status"])},
        {pg_literal(state["model"])}, {pg_literal(state["thinking_level"])},
        {pg_literal(float(state["elapsed_seconds"]))}, {pg_literal(int(state["new_ideas_added_this_run"]))},
        {pg_literal(int(state["ideas_rejected_this_run"]))}, {pg_literal(int(state["ideas_count"]))},
        {pg_literal(int(state["api_calls"]))}, {pg_literal(int(state["input_tokens"]))},
        {pg_literal(int(state["output_tokens"]))}, {pg_literal(int(state["thought_tokens"]))},
        {pg_literal(int(state["refresh_waits"]))}, {pg_literal(state["resume_at"])}::timestamptz,
        {pg_literal(state["last_idea_id"])}, {pg_literal(state["stop_reason"])}, {pg_literal(state)}
    )
    ON CONFLICT (run_id) DO UPDATE SET
        updated_at = EXCLUDED.updated_at,
        status = EXCLUDED.status,
        elapsed_seconds = EXCLUDED.elapsed_seconds,
        ideas_generated = EXCLUDED.ideas_generated,
        ideas_rejected = EXCLUDED.ideas_rejected,
        ideas_count = EXCLUDED.ideas_count,
        api_calls = EXCLUDED.api_calls,
        input_tokens = EXCLUDED.input_tokens,
        output_tokens = EXCLUDED.output_tokens,
        thought_tokens = EXCLUDED.thought_tokens,
        refresh_waits = EXCLUDED.refresh_waits,
        resume_at = EXCLUDED.resume_at,
        last_idea_id = EXCLUDED.last_idea_id,
        stop_reason = EXCLUDED.stop_reason,
        state_json = EXCLUDED.state_json;
    """
    with PostgresWireClient() as client:
        client.execute(sql)


def latest_agent_state() -> dict[str, Any] | None:
    """Return the telemetry of the most recently updated agent run, if any."""
    with PostgresWireClient() as client:
        rows = client.execute("SELECT state_json FROM agent_runs ORDER BY updated_at DESC LIMIT 1;")
    return json.loads(rows[0]["state_json"]) if rows else None


def acquire_agent_lock() -> PostgresWireClient | None:
    """Take the single-agent lock. Hold the returned connection open; closing it releases the lock."""
    client = PostgresWireClient()
    client.connect()
    rows = client.execute(f"SELECT pg_try_advisory_lock({AGENT_LOCK_KEY}) AS locked;")
    if rows[0]["locked"] == "t":
        return client
    client.close()
    return None


def record_gemini_call(
    run_id: str,
    call: GeminiCall,
    *,
    outcome: str,
    idea_id: str | None = None,
    error: str = "",
) -> None:
    """Record one billed Gemini call, keeping its raw answer so rejected output is not lost."""
    sql = f"""
    INSERT INTO gemini_calls (
        run_id, interaction_id, model, thinking_level, outcome, idea_id, input_tokens,
        output_tokens, thought_tokens, total_tokens, error, raw_text
    ) VALUES (
        {pg_literal(run_id)}, {pg_literal(call.interaction_id)}, {pg_literal(call.model)},
        {pg_literal(config.GEMINI_THINKING_LEVEL)}, {pg_literal(outcome)}, {pg_literal(idea_id)},
        {pg_literal(call.input_tokens)}, {pg_literal(call.output_tokens)},
        {pg_literal(call.thought_tokens)}, {pg_literal(call.total_tokens)},
        {pg_literal(error)}, {pg_literal(call.text)}
    );
    """
    with PostgresWireClient() as client:
        client.execute(sql)


def count_ideas() -> int:
    with PostgresWireClient() as client:
        return int(client.execute("SELECT COUNT(*) AS n FROM product_ideas;")[0]["n"])


def next_idea_number() -> int:
    """Return the number after the highest existing IDEA-NNN id."""
    with PostgresWireClient() as client:
        rows = client.execute("SELECT COALESCE(MAX(substring(id from '[0-9]+')::int), 0) AS n FROM product_ideas;")
    return int(rows[0]["n"]) + 1


def recent_titles(limit: int) -> list[str]:
    """Return shortened titles of the newest ideas, for the prompt's do-not-repeat list."""
    with PostgresWireClient() as client:
        rows = client.execute(f"SELECT left(title, 80) AS title FROM product_ideas ORDER BY created_at DESC, id DESC LIMIT {int(limit)};")
    return [r["title"] for r in rows]


def naics_counts() -> dict[str, int]:
    with PostgresWireClient() as client:
        rows = client.execute("SELECT naics_code, COUNT(*) AS n FROM product_ideas GROUP BY naics_code;")
    return {r["naics_code"]: int(r["n"]) for r in rows}


def get_postgres_status() -> dict[str, Any]:
    """Query live PostgreSQL connection, migration, table row counts, and portfolio summary metrics."""
    with PostgresWireClient() as client:
        mig_rows = client.execute(
            "SELECT version, filename, checksum, applied_at::text FROM schema_migrations ORDER BY version ASC;"
        )
        summary_rows = client.execute("SELECT * FROM v_portfolio_summary;")
        counts = client.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM product_ideas)::int AS product_ideas_count,
                (SELECT COUNT(*) FROM idea_metrics)::int AS idea_metrics_count,
                (SELECT COUNT(*) FROM idea_diligence_questions)::int AS idea_diligence_questions_count,
                (SELECT COUNT(*) FROM agent_runs)::int AS agent_runs_count,
                (SELECT COUNT(*) FROM gemini_calls)::int AS gemini_calls_count;
            """
        )
    return {
        "connected": True,
        "engine": "PostgreSQL 16 (Docker: idea-factory-postgres)",
        "host": config.POSTGRES_HOST,
        "port": config.POSTGRES_PORT,
        "database": config.POSTGRES_DB,
        "user": config.POSTGRES_USER,
        "migrations_applied": mig_rows,
        "table_counts": counts[0] if counts else {},
        "portfolio_summary": summary_rows[0] if summary_rows else {},
    }
