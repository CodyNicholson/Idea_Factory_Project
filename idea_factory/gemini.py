"""Client for Gemini 4 Argon at High effort, the only model this project calls.

The model and effort are constants in `config`, and `call_gemini` takes neither as an argument.
Errors are sorted into the three cases the agent loop treats differently: tokens ran out (wait for
the refresh), transient failure (back off and retry), and fatal misconfiguration (stop).
"""
from __future__ import annotations

import json
import re
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping
from zoneinfo import ZoneInfo

from . import config

API_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"

# Google resets requests-per-day quotas at midnight Pacific time.
_QUOTA_TIMEZONE = ZoneInfo("America/Los_Angeles")
_SPEND_TERMS = ("prepay", "credit", "spend cap", "spending cap", "spend limit", "monthly spend")
_BILLING_TERMS = (*_SPEND_TERMS, "billing", "payment")
_DAILY_TERMS = ("perday", "per day", "per_day", "daily")


class GeminiError(Exception):
    """Base class for Gemini API failures."""


class TokensExhaustedError(GeminiError):
    """The token, request or spend allowance ran out. The agent waits and then resumes.

    `kind` is `rate_limit`, `daily_quota` or `billing`. `resume_at` is set when the reset time is
    known, `retry_after` when the API gave a delay. With neither, the agent polls.
    """

    def __init__(
        self,
        message: str,
        *,
        kind: str,
        retry_after: float | None = None,
        resume_at: datetime | None = None,
    ) -> None:
        super().__init__(message)
        self.kind = kind
        self.retry_after = retry_after
        self.resume_at = resume_at


class TransientGeminiError(GeminiError):
    """Network failure or server error. Retry with backoff."""


class FatalGeminiError(GeminiError):
    """Bad key, unknown model or malformed request. Retrying cannot help."""


@dataclass
class GeminiCall:
    """A completed, billed call. `text` is the model's answer, or the raw body if it had none."""

    interaction_id: str
    model: str
    status: str
    text: str
    has_answer: bool
    input_tokens: int
    output_tokens: int
    thought_tokens: int
    total_tokens: int


def next_quota_reset(now: datetime | None = None) -> datetime:
    """Return the next midnight Pacific time, when daily quotas reset."""
    current = (now or datetime.now(timezone.utc)).astimezone(_QUOTA_TIMEZONE)
    next_day = (current + timedelta(days=1)).date()
    midnight = datetime(next_day.year, next_day.month, next_day.day, tzinfo=_QUOTA_TIMEZONE)
    return midnight.astimezone(timezone.utc)


def _retry_delay_seconds(error: Mapping[str, Any], headers: Mapping[str, str]) -> float | None:
    """Read the server's retry hint from the Retry-After header or a RetryInfo error detail."""
    header = headers.get("Retry-After") or headers.get("retry-after")
    if header:
        try:
            return max(0.0, float(header))
        except ValueError:
            pass
    details = error.get("details")
    if isinstance(details, list):
        for detail in details:
            delay = detail.get("retryDelay") if isinstance(detail, dict) else None
            match = re.fullmatch(r"(\d+(?:\.\d+)?)s", str(delay or ""))
            if match:
                return float(match.group(1))
    return None


def classify_http_error(
    status: int,
    body: str,
    headers: Mapping[str, str] | None = None,
    now: datetime | None = None,
) -> GeminiError:
    """Map an HTTP error response from the Gemini API to the exception the agent loop acts on."""
    headers = headers or {}
    try:
        parsed = json.loads(body)
    except ValueError:
        parsed = {}
    # This endpoint wraps errors in a one-item JSON array.
    if isinstance(parsed, list) and parsed:
        parsed = parsed[0]
    error = parsed.get("error") if isinstance(parsed, dict) else None
    error = error if isinstance(error, dict) else {}
    code = str(error.get("code", "")).lower()
    message = str(error.get("message") or body)
    summary = f"HTTP {status}: {message[:300]}"
    message_lower = message.lower()
    # Only the message is searched for billing terms, because error details carry help links.
    is_billing = any(term in message_lower for term in _BILLING_TERMS)

    if status == 402 or (status in (400, 403) and is_billing):
        return TokensExhaustedError(summary, kind="billing")
    if status == 429:
        text = body.lower()
        # A limit of zero never refreshes: the key's tier does not include this model.
        if re.search(r"limit: ?0\b", text):
            return FatalGeminiError(f"{summary} Gemini 4 Argon needs a paid-tier API key.")
        if code == "quota_exceeded" or any(term in text for term in _DAILY_TERMS):
            return TokensExhaustedError(summary, kind="daily_quota", resume_at=next_quota_reset(now))
        retry_after = _retry_delay_seconds(error, headers)
        # Rate-limit messages can say "check your plan and billing details", so a retry hint wins.
        if retry_after is None and "perminute" not in text and any(term in message_lower for term in _SPEND_TERMS):
            return TokensExhaustedError(summary, kind="billing")
        return TokensExhaustedError(summary, kind="rate_limit", retry_after=retry_after)
    if status >= 500 or status in (408, 409, 499):
        return TransientGeminiError(summary)
    return FatalGeminiError(summary)


def _extract_text(body: Mapping[str, Any]) -> str:
    """Concatenate the text of every `model_output` step, skipping thinking steps."""
    parts: list[str] = []
    for step in body.get("steps") or []:
        if not isinstance(step, dict) or step.get("type") != "model_output":
            continue
        for item in step.get("content") or []:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text") or ""))
    return "".join(parts)


def call_gemini(prompt: str, schema: dict[str, Any]) -> GeminiCall:
    """Send one prompt to Gemini 4 Argon at High effort and return its JSON answer as text."""
    if not config.GEMINI_API_KEY:
        raise FatalGeminiError("GEMINI_API_KEY is not set. Add it to .env.")

    payload = {
        "model": config.GEMINI_MODEL,
        "input": prompt,
        "generation_config": {
            "thinking_level": config.GEMINI_THINKING_LEVEL,
            "max_output_tokens": config.GEMINI_MAX_OUTPUT_TOKENS,
        },
        "response_format": {"type": "text", "mime_type": "application/json", "schema": schema},
        "store": False,
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        # Sent as a header, not in the URL, so the key cannot leak through error messages or logs.
        headers={"content-type": "application/json", "x-goog-api-key": config.GEMINI_API_KEY},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.GEMINI_TIMEOUT_SECONDS) as response:
            raw_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise classify_http_error(exc.code, exc.read().decode("utf-8", errors="replace"), exc.headers) from exc
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as exc:
        raise TransientGeminiError(f"Network error calling Gemini: {exc}") from exc

    try:
        body = json.loads(raw_body)
    except ValueError as exc:
        raise TransientGeminiError(f"Gemini returned a non-JSON body: {raw_body[:200]}") from exc

    served_model = str(body.get("model") or config.GEMINI_MODEL).removeprefix("models/")
    if not served_model.startswith(config.GEMINI_MODEL):
        raise FatalGeminiError(f"Gemini served '{served_model}' instead of '{config.GEMINI_MODEL}'. Stopping.")

    text = _extract_text(body)
    usage = body.get("usage") or {}
    return GeminiCall(
        interaction_id=str(body.get("id") or ""),
        model=config.GEMINI_MODEL,
        status=str(body.get("status") or ""),
        # Keep the whole body when there is no answer, so a failed paid call can still be diagnosed.
        text=text or raw_body,
        has_answer=bool(text),
        input_tokens=int(usage.get("total_input_tokens") or 0),
        output_tokens=int(usage.get("total_output_tokens") or 0),
        thought_tokens=int(usage.get("total_thought_tokens") or 0),
        total_tokens=int(usage.get("total_tokens") or 0),
    )
