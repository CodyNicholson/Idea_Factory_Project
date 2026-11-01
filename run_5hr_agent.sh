#!/usr/bin/env bash
# =============================================================================
# Idea Factory — Continuous 5-Hour Token-Window Loop Runner (with Auto-Resume)
# Continuously generates ideas until the 5-hour token/credit limit is reached,
# waits until the 5-hour token limit refreshes, and resumes where it left off.
# =============================================================================
set -euo pipefail

cd "$(dirname "$0")"
mkdir -p logs data

HOURS="${1:-5.0}"
INTERVAL="${2:-15}"

echo "Starting Idea Factory Continuous 5-Hour Agent Loop with Auto-Resume (max_hours=${HOURS}, interval=${INTERVAL}s)..."
python3 -m idea_factory run --hours "${HOURS}" --interval "${INTERVAL}" --auto-resume

