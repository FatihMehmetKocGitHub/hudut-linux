#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs/lxc"
mkdir -p "$LOG_DIR"

exec > >(tee -a "$LOG_DIR/01_install_lxd.log") 2>&1

echo "[HUDUT] LXD kurulumu başlıyor..."

if ! command -v snap >/dev/null 2>&1; then
  echo "[HUDUT] snapd bulunamadı, kuruluyor..."
  sudo apt update
  sudo apt install -y snapd
fi

if snap list lxd >/dev/null 2>&1; then
  echo "[HUDUT] LXD zaten kurulu. Güncelleme deneniyor..."
  sudo snap refresh lxd || true
else
  echo "[HUDUT] LXD kuruluyor..."
  sudo snap install lxd
fi

if ! getent group lxd | grep -qw "$USER"; then
  echo "[HUDUT] Kullanıcı lxd grubuna ekleniyor: $USER"
  sudo usermod -aG lxd "$USER"
else
  echo "[HUDUT] Kullanıcı zaten lxd grubunda."
fi

if lxc profile show default >/dev/null 2>&1; then
  echo "[HUDUT] LXD zaten initialize edilmiş görünüyor."
else
  echo "[HUDUT] LXD minimal init çalıştırılıyor..."
  sudo lxd init --minimal
fi

echo
echo "[HUDUT] Kurulum tamam."
echo "[HUDUT] Şimdi yeni terminal aç veya şunu çalıştır:"
echo "newgrp lxd"
echo
echo "[HUDUT] Test komutu:"
echo "lxc list"
