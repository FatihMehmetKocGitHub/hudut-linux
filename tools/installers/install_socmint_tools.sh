#!/usr/bin/env bash
set -euo pipefail

CONTAINER="hudut-socmint"

echo "[HUDUT] Target container: $CONTAINER"

if ! lxc info "$CONTAINER" >/dev/null 2>&1; then
  echo "[ERROR] Container bulunamadı: $CONTAINER"
  exit 1
fi

lxc start "$CONTAINER" >/dev/null 2>&1 || true

echo "[HUDUT] Ağ testi..."
lxc exec "$CONTAINER" -- ping -c 1 1.1.1.1 >/dev/null
lxc exec "$CONTAINER" -- getent hosts archive.ubuntu.com >/dev/null

echo "[HUDUT] apt update..."
lxc exec "$CONTAINER" -- bash -lc 'apt-get update'

echo "[HUDUT] Kurulum başlıyor..."

lxc exec "$CONTAINER" -- bash -lc '
export DEBIAN_FRONTEND=noninteractive
apt-get install -y \
  curl wget git jq tree unzip zip nano vim less \
  python3 python3-pip python3-venv \
  ca-certificates
mkdir -p /opt/hudut-socmint /root/hudut-workspace/socmint
python3 -m venv /opt/hudut-socmint/venv
/opt/hudut-socmint/venv/bin/pip install --upgrade pip wheel
/opt/hudut-socmint/venv/bin/pip install requests beautifulsoup4 pandas
'

echo "[HUDUT] SOCMINT yardımcı ortamı kuruldu."
