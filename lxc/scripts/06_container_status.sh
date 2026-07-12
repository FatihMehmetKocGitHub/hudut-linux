#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPORT_DIR="$PROJECT_ROOT/reports/lxc"
mkdir -p "$REPORT_DIR"

TS="$(date +%Y%m%d-%H%M%S)"
REPORT="$REPORT_DIR/lxc-status-$TS.md"

{
  echo "# Hudut LXC Status Report"
  echo
  echo "- Date: $(date)"
  echo "- Host: $(hostname)"
  echo "- User: $(whoami)"
  echo
  echo "## LXC Version"
  echo
  echo '```text'
  lxc version
  echo '```'
  echo
  echo "## Network List"
  echo
  echo '```text'
  lxc network list
  echo '```'
  echo
  echo "## Container List"
  echo
  echo '```text'
  lxc list
  echo '```'
  echo
  echo "## UFW Status"
  echo
  echo '```text'
  sudo ufw status verbose || true
  echo '```'
  echo
  echo "## Container Connectivity Tests"
  echo
  for c in hudut-osint hudut-socmint hudut-cti hudut-techint hudut-geoint hudut-dev hudut-sandbox; do
    echo
    echo "### $c"
    echo
    echo '```text'
    if lxc info "$c" >/dev/null 2>&1; then
      lxc exec "$c" -- ip -4 addr show eth0 || true
      lxc exec "$c" -- ip route || true
      lxc exec "$c" -- ping -c 1 1.1.1.1 || true
      lxc exec "$c" -- getent hosts archive.ubuntu.com || true
    else
      echo "Container yok: $c"
    fi
    echo '```'
  done
} > "$REPORT"

echo "[HUDUT] LXC status raporu üretildi: $REPORT"
