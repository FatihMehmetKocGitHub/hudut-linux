#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs/lxc"
mkdir -p "$LOG_DIR"

exec > >(tee -a "$LOG_DIR/02_create_containers.log") 2>&1

CONTAINERS=(
  "hudut-osint"
  "hudut-socmint"
  "hudut-cti"
  "hudut-techint"
  "hudut-geoint"
  "hudut-dev"
  "hudut-sandbox"
)

echo "[HUDUT] V1 dışı honeypot-lab temizleniyor..."
lxc stop honeypot-lab --force >/dev/null 2>&1 || true
lxc delete honeypot-lab >/dev/null 2>&1 || true

echo "[HUDUT] Container oluşturma başlıyor..."

for c in "${CONTAINERS[@]}"; do
  if lxc info "$c" >/dev/null 2>&1; then
    echo "[HUDUT] $c zaten var."
  else
    echo "[HUDUT] $c oluşturuluyor..."
    lxc init ubuntu:24.04 "$c" \
      --config limits.cpu=2 \
      --config limits.memory=2GiB
  fi
done

echo "[HUDUT] Container başlatma ve temel paket kurulumu..."

for c in "${CONTAINERS[@]}"; do
  echo "[HUDUT] $c başlatılıyor..."
  lxc start "$c" >/dev/null 2>&1 || true

  echo "[HUDUT] $c apt update..."
  lxc exec "$c" -- bash -lc 'apt-get update'

  echo "[HUDUT] $c temel paketler kuruluyor..."
  lxc exec "$c" -- bash -lc '
    export DEBIAN_FRONTEND=noninteractive
    apt-get install -y \
      ca-certificates curl wget git nano vim less unzip zip jq tree \
      python3 python3-pip python3-venv \
      dnsutils whois iputils-ping net-tools traceroute openssl
  '
done

echo "[HUDUT] TECHINT içine nmap kuruluyor. Sadece izinli lab/hedef için."
lxc exec hudut-techint -- bash -lc '
  export DEBIAN_FRONTEND=noninteractive
  apt-get install -y nmap
'

echo "[HUDUT] DEV içine geliştirme paketleri kuruluyor."
lxc exec hudut-dev -- bash -lc '
  export DEBIAN_FRONTEND=noninteractive
  apt-get install -y build-essential pipx
  mkdir -p /opt/hudut-dev
'

echo "[HUDUT] GEOINT hazırlığı."
lxc exec hudut-geoint -- bash -lc '
  mkdir -p /opt/hudut-geoint
'

echo "[HUDUT] Tüm containerlar hazır."
lxc list
