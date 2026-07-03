#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

SOURCE_FILE="$PROJECT_DIR/security/kernel/99-hudut-kernel-hardening.conf"
TARGET_FILE="/etc/sysctl.d/99-hudut-kernel-hardening.conf"

echo "[HUDUT] Kernel hardening uygulanıyor..."
echo "[INFO] Kaynak: $SOURCE_FILE"
echo "[INFO] Hedef : $TARGET_FILE"

if [ ! -f "$SOURCE_FILE" ]; then
    echo "[ERROR] Kaynak dosya bulunamadı: $SOURCE_FILE"
    exit 1
fi

sudo cp "$SOURCE_FILE" "$TARGET_FILE"
sudo sysctl --system

echo "[OK] Kernel hardening uygulandı."
echo "[INFO] Reboot sonrası bazı ayarlar daha net oturabilir."
