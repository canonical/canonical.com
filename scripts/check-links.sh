#!/usr/bin/env bash
# check-links.sh — run LinkChecker with retry logic for transient failures.
#
# Usage:
#   ./scripts/check-links.sh [URL]
#
# Defaults to https://canonical.com when no URL is given.
# Uses .linkchecker/linkcheckerrc from the repo root for config.
#
# Examples:
#   ./scripts/check-links.sh                        # check live site
#   ./scripts/check-links.sh http://localhost:8002  # check local dev server

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET_URL="${1:-https://canonical.com}"

runtime_error() {
  echo "LinkChecker failed unexpectedly. See the output above for details." >&2
  exit 2
}

# Print the unique failed URLs (valid=False) from a linkchecker CSV.
extract_failed() {
  python3 - "$1" <<'PY'
import csv
import sys

seen = set()
with open(sys.argv[1], newline="") as f:
    rows = (line for line in f if not line.startswith("#"))
    for row in csv.DictReader(rows, delimiter=";"):
        if row.get("valid", "").strip().lower() == "false":
            url = row.get("urlname")
            if url and url not in seen:
                seen.add(url)
                print(url)
PY
}

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

if linkchecker \
    --config "${REPO_ROOT}/.linkchecker/linkcheckerrc" \
    --no-warning \
    -F "csv/${WORK_DIR}/failed-links.csv" \
    "${TARGET_URL}"; then
  echo "No broken links found."
  exit 0
else
  checker_status=$?
fi

[ "$checker_status" -eq 1 ] || runtime_error
extract_failed "${WORK_DIR}/failed-links.csv" > "${WORK_DIR}/current-urls.txt" || runtime_error
[ -s "${WORK_DIR}/current-urls.txt" ] || runtime_error

attempt=1
max_attempts=3
delay=60

# Re-check only the previously failed links
while [ "$attempt" -le "$max_attempts" ] && [ -s "${WORK_DIR}/current-urls.txt" ]; do
  echo "Attempt $attempt/$max_attempts: rechecking $(wc -l < "${WORK_DIR}/current-urls.txt") link(s) after ${delay}s"
  sleep "$delay"

  mapfile -t urls < "${WORK_DIR}/current-urls.txt"
  retry_csv="${WORK_DIR}/retry-${attempt}.csv"
  if linkchecker \
      --config "${REPO_ROOT}/.linkchecker/linkcheckerrc" \
      --no-warning \
      --recursion-level=0 \
      --timeout=30 \
      -F "csv/${retry_csv}" \
      "${urls[@]}"; then
    echo "All remaining links resolved on attempt $attempt."
    exit 0
  else
    checker_status=$?
  fi

  [ "$checker_status" -eq 1 ] || runtime_error
  extract_failed "$retry_csv" > "${WORK_DIR}/next-urls.txt" || runtime_error
  [ -s "${WORK_DIR}/next-urls.txt" ] || runtime_error
  mv "${WORK_DIR}/next-urls.txt" "${WORK_DIR}/current-urls.txt"
  attempt=$((attempt + 1))
  delay=$((delay * 2))
done

echo "Links still broken after $max_attempts attempts:"
cat "${WORK_DIR}/current-urls.txt"
exit 1
