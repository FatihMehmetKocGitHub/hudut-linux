#!/usr/bin/env bash
set -euo pipefail

CONTAINER="hudut-cti"

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
  whois dnsutils ca-certificates
mkdir -p /opt/hudut-cti /root/hudut-workspace/cti
python3 -m venv /opt/hudut-cti/venv
/opt/hudut-cti/venv/bin/pip install --upgrade pip wheel
/opt/hudut-cti/venv/bin/pip install requests feedparser pandas stix2 taxii2-client
'

echo "[HUDUT] CTI temel ortamı kuruldu."
