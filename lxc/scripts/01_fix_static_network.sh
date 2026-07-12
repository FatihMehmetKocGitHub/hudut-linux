#!/usr/bin/env bash
set -euo pipefail

declare -A IPS=(
  ["hudut-osint"]="10.99.10.10"
  ["hudut-socmint"]="10.99.10.11"
  ["hudut-cti"]="10.99.10.12"
  ["hudut-techint"]="10.99.10.13"
  ["hudut-geoint"]="10.99.10.14"
  ["hudut-dev"]="10.99.10.15"
  ["hudut-sandbox"]="10.99.10.16"
)

GATEWAY="10.99.10.1"

echo "[HUDUT] Statik LXC IPv4 + DNS temiz yapılandırma başlıyor..."

for c in hudut-osint hudut-socmint hudut-cti hudut-techint hudut-geoint hudut-dev hudut-sandbox; do
  ip="${IPS[$c]}"

  if ! lxc info "$c" >/dev/null 2>&1; then
    echo "[WARN] Container yok: $c"
    continue
  fi

  echo "[HUDUT] $c -> $ip"

  lxc start "$c" >/dev/null 2>&1 || true

  lxc exec "$c" -- bash -lc "
set -e

mkdir -p /etc/netplan /etc/cloud/cloud.cfg.d

cat > /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg << CLOUD
network: {config: disabled}
CLOUD

rm -f /etc/netplan/*.yaml

cat > /etc/netplan/10-hudut-static.yaml << NETPLAN
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      dhcp6: false
      addresses:
        - ${ip}/24
      routes:
        - to: default
          via: ${GATEWAY}
      nameservers:
        addresses:
          - 10.99.10.1
          - 1.1.1.1
          - 8.8.8.8
NETPLAN

rm -f /etc/resolv.conf
cat > /etc/resolv.conf << RESOLV
nameserver 10.99.10.1
nameserver 1.1.1.1
nameserver 8.8.8.8
RESOLV

netplan generate
netplan apply

ip addr flush dev eth0
ip link set eth0 up
ip addr add ${ip}/24 dev eth0
ip route replace default via ${GATEWAY}
"
done

echo "[HUDUT] Containerlar yeniden başlatılıyor..."
for c in hudut-osint hudut-socmint hudut-cti hudut-techint hudut-geoint hudut-dev hudut-sandbox; do
  lxc restart "$c"
done

sleep 5

echo "[HUDUT] Test ediliyor..."
lxc exec hudut-osint -- ping -c 2 1.1.1.1
lxc exec hudut-osint -- ping -c 2 archive.ubuntu.com

echo "[HUDUT] Statik LXC ağ yapılandırması tamam."
lxc list
