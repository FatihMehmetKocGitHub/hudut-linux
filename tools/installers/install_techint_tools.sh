#!/usr/bin/env bash
set -euo pipefail

CONTAINER="hudut-techint"

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
  whois dnsutils traceroute net-tools iputils-ping \
  python3 python3-pip python3-venv \
  nmap
mkdir -p /opt/hudut-techint /root/hudut-workspace/techint
'

echo "[HUDUT] TECHINT araçları kuruldu."
echo "[INFO] nmap yalnızca kendi lab ortamın, kendi sistemlerin veya yazılı izinli hedeflerde kullanılmalıdır."
