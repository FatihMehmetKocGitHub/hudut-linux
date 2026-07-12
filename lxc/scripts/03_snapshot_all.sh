#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs/lxc"
mkdir -p "$LOG_DIR"

exec > >(tee -a "$LOG_DIR/03_snapshot_all.log") 2>&1

SNAP_NAME="${1:-clean-base-$(date +%Y%m%d-%H%M)}"

CONTAINERS=(
  "hudut-osint"
  "hudut-socmint"
  "hudut-cti"
  "hudut-techint"
  "hudut-geoint"
  "hudut-dev"
  "hudut-sandbox"
)

echo "[HUDUT] Snapshot adı: $SNAP_NAME"

for c in "${CONTAINERS[@]}"; do
  if lxc info "$c" >/dev/null 2>&1; then
    if lxc info "$c" | grep -q "clean-base"; then
      echo "[INFO] $c içinde clean-base snapshot zaten var, atlanıyor."
    else
      echo "[HUDUT] Snapshot alınıyor: $c/$SNAP_NAME"
      lxc snapshot "$c" "$SNAP_NAME"
    fi
  else
    echo "[WARN] Container yok: $c"
  fi
done

echo "[HUDUT] Snapshot işlemi tamam."
lxc list
