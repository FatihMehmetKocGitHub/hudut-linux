#!/usr/bin/env bash
set -euo pipefail

echo "[HUDUT] LXD network onarım başlıyor..."

sudo snap restart lxd

if lxc network show lxdbr0 >/dev/null 2>&1; then
  echo "[HUDUT] lxdbr0 mevcut."
else
  echo "[HUDUT] lxdbr0 oluşturuluyor..."
  lxc network create lxdbr0 ipv4.address=auto ipv4.nat=true ipv6.address=none
fi

lxc network set lxdbr0 ipv4.nat true
lxc network set lxdbr0 ipv6.address none

lxc profile device remove default eth0 >/dev/null 2>&1 || true
lxc profile device add default eth0 nic nictype=bridged parent=lxdbr0

sudo sysctl -w net.ipv4.ip_forward=1

if command -v ufw >/dev/null 2>&1; then
  sudo ufw allow in on lxdbr0 || true
fi

echo "[HUDUT] Container restart deneniyor..."
for c in hudut-osint hudut-cti hudut-techint hudut-dev hudut-sandbox; do
  if lxc info "$c" >/dev/null 2>&1; then
    lxc restart "$c" || true
  fi
done

echo "[HUDUT] Test:"
lxc exec hudut-osint -- ping -c 2 1.1.1.1 || true
lxc exec hudut-osint -- ping -c 2 archive.ubuntu.com || true

echo "[HUDUT] Bitti."
