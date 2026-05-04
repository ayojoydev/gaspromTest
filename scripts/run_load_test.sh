#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORTS_DIR="$ROOT_DIR/reports/load_tests"
TIMESTAMP="$(date +"%Y%m%d_%H%M%S")"
RUN_DIR="$REPORTS_DIR/$TIMESTAMP"

mkdir -p "$RUN_DIR"

echo "Load testing"
echo "Project root: $ROOT_DIR"
echo "Artifacts:    $RUN_DIR"

if ! command -v locust >/dev/null 2>&1; then
    echo "Locust is not installed. Install it first or run Locust in Docker."
    exit 1
fi

locust \
  -f "$ROOT_DIR/tests/locustfile.py" \
  --host=http://localhost:8000 \
  --users "${LOCUST_USERS:-50}" \
  --spawn-rate "${LOCUST_SPAWN_RATE:-5}" \
  --run-time "${LOCUST_RUN_TIME:-5m}" \
  --headless \
  --csv "$RUN_DIR/results" \
  --html "$RUN_DIR/report.html"

echo
echo "Load test completed."
echo "Results saved to: $RUN_DIR"
