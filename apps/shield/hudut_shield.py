#!/usr/bin/env python3
import argparse
import datetime
import os
import shlex
import shutil
import subprocess
import time
from pathlib import Path


BASE_DIR = Path.home() / "hudut-linux"
REPORT_DIR = BASE_DIR / "reports" / "security"
NETWORK_REPORT_DIR = BASE_DIR / "reports" / "network"

PROFILES = [
    "normal",
    "secure",
    "osint",
    "tor-research",
    "public-wifi",
    "honeypot-lab",
    "lab",
]


DNS_PROFILES = {
    "normal": {
        "name": "Normal DNS",
        "ipv4_dns": "",
        "ipv6_dns": "",
        "desc": "Ağ sağlayıcısının varsayılan DNS ayarını kullanır."
    },
    "secure": {
        "name": "Secure DNS",
        "ipv4_dns": "9.9.9.9 149.112.112.112 1.1.1.1",
        "ipv6_dns": "2620:fe::fe 2620:fe::9 2606:4700:4700::1111",
        "desc": "Quad9 ve Cloudflare DNS ile güvenli genel kullanım profili."
    },
    "osint": {
        "name": "OSINT DNS",
        "ipv4_dns": "1.1.1.1 1.0.0.1 9.9.9.9",
        "ipv6_dns": "2606:4700:4700::1111 2606:4700:4700::1001 2620:fe::fe",
        "desc": "OSINT araştırmaları için hızlı ve sade DNS profili."
    },
    "lab": {
        "name": "Lab DNS",
        "ipv4_dns": "192.168.1.1",
        "ipv6_dns": "",
        "desc": "Yerel lab veya modem DNS profili."
    }
}


PROFILE_TABLES = {
    "normal": {
        "Amaç": "Günlük güvenli kullanım",
        "Firewall": "Gelen kapalı, giden açık",
        "Bluetooth": "Değiştirilmez",
        "SSH": "Değiştirilmez",
        "DNS": "Normal DNS",
        "Proxy": "Durum gösterilir, değiştirilmez",
        "MAC": "Mevcut ayar",
        "Mikrofon/Kamera": "Profil uygulanınca kapatılır",
        "Not": "Varsayılan günlük profil"
    },
    "secure": {
        "Amaç": "En üst seviye temel güvenlik",
        "Firewall": "Gelen kapalı, giden açık, log açık",
        "Bluetooth": "Kapatılır / bloklanır",
        "SSH": "Kapatılır",
        "DNS": "Secure DNS",
        "Proxy": "Terminal temizleme komutu gösterilir, Firefox direct yapılır",
        "MAC": "Stable random",
        "Mikrofon/Kamera": "Profil uygulanınca kapatılır",
        "Not": "Kurumsal sunum için en temiz güvenlik profili"
    },
    "osint": {
        "Amaç": "Yasal OSINT araştırma ortamı",
        "Firewall": "Gelen kapalı, giden açık, log açık",
        "Bluetooth": "Kapatılması önerilir",
        "SSH": "Kapalı kalmalı",
        "DNS": "OSINT DNS",
        "Proxy": "Durum gösterilir, kullanıcı bilinçli seçer",
        "MAC": "Stable random",
        "Mikrofon/Kamera": "Profil uygulanınca kapatılır",
        "Not": "Kişisel hesaplarla karıştırılmamalı"
    },
    "tor-research": {
        "Amaç": "Tor Browser ile yasal araştırma",
        "Firewall": "Gelen kapalı",
        "Bluetooth": "Kapalı önerilir",
        "SSH": "Kapalı önerilir",
        "DNS": "Tor Browser kendi ağını kullanır",
        "Proxy": "Tor Browser dışı proxy yönetilmez",
        "MAC": "Stable random",
        "Mikrofon/Kamera": "Profil uygulanınca kapatılır",
        "Not": "V1'de tüm sistemi Tor'a yönlendirmiyoruz"
    },
    "public-wifi": {
        "Amaç": "Ortak ağlarda güvenli kullanım",
        "Firewall": "Gelen tamamen kapalı",
        "Bluetooth": "Kapatılır / bloklanır",
        "SSH": "Kapatılır",
        "DNS": "Secure DNS",
        "Proxy": "Terminal temizleme komutu gösterilir, Firefox direct yapılır",
        "MAC": "Random",
        "Mikrofon/Kamera": "Profil uygulanınca kapatılır",
        "Not": "Kafe, otel, belediye Wi-Fi gibi ağlarda"
    },
    "honeypot-lab": {
        "Amaç": "İzole honeypot laboratuvarı",
        "Firewall": "Ana sistem korumalı kalır",
        "Bluetooth": "Kapalı önerilir",
        "SSH": "Ana sistemde kapalı",
        "DNS": "Lab DNS",
        "Proxy": "Ana sistem proxy temiz olmalı",
        "MAC": "Lab / stable",
        "Mikrofon/Kamera": "Profil uygulanınca kapatılır",
        "Not": "Honeypot sadece LXC/VM içinde çalıştırılır"
    },
    "lab": {
        "Amaç": "Yerel test ve geliştirme laboratuvarı",
        "Firewall": "Kontrollü",
        "Bluetooth": "Kapalı önerilir",
        "SSH": "Sadece gerekirse açık",
        "DNS": "Lab DNS",
        "Proxy": "Durum gösterilir",
        "MAC": "Stable random",
        "Mikrofon/Kamera": "Profil uygulanınca kapatılır",
        "Not": "Kendi cihazların ve izinli test ortamı"
    }
}


def run(cmd):
    return subprocess.run(
        cmd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def run_live(cmd):
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, shell=True)


def exists(cmd):
    return shutil.which(cmd) is not None


def quote(value):
    return shlex.quote(str(value))


def short(text, limit=180):
    text = " ".join(text.strip().split())
    if not text:
        return "Bilgi yok"
    return text[:limit] + "..." if len(text) > limit else text


def get_active_connection():
    result = run("nmcli -t -f NAME,DEVICE connection show --active 2>/dev/null")
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    for line in lines:
        parts = line.split(":")
        if len(parts) >= 2 and parts[1] not in ["lo", ""]:
            return parts[0], parts[1]

    return None, None


def get_default_interface():
    result = run("ip route | awk '/default/ {print $5; exit}'")
    iface = result.stdout.strip()
    return iface if iface else "bilinmiyor"


def get_ipv4():
    iface = get_default_interface()
    if iface == "bilinmiyor":
        return "bilinmiyor"
    result = run(f"ip -4 addr show {quote(iface)} | awk '/inet / {{print $2}}'")
    return result.stdout.strip() or "bilinmiyor"


def get_ipv6():
    iface = get_default_interface()
    if iface == "bilinmiyor":
        return "bilinmiyor"
    result = run(f"ip -6 addr show {quote(iface)} | awk '/inet6 / {{print $2}}'")
    return short(result.stdout.strip(), 220)


def check_firewall():
    if not exists("ufw"):
        return ("Firewall", "WARN", "ufw kurulu değil")

    result = run("sudo -n ufw status verbose 2>/dev/null")
    out = (result.stdout + " " + result.stderr).strip()

    if not out:
        result = run("ufw status verbose 2>/dev/null")
        out = (result.stdout + " " + result.stderr).strip()

    if "Status: active" in out:
        return ("Firewall", "OK", "ufw aktif")

    if "Status: inactive" in out:
        return ("Firewall", "WARN", "ufw pasif")

    if not out:
        return ("Firewall", "WARN", "ufw durumu için sudo gerekebilir")

    if "need to be root" in out.lower() or "must be root" in out.lower():
        return ("Firewall", "WARN", "ufw durumu için sudo gerekebilir")

    return ("Firewall", "WARN", short(out))

def check_dns():
    if exists("resolvectl"):
        out = run("resolvectl dns").stdout.strip()
        if out:
            return ("DNS", "INFO", short(out, 260))

    out = run("grep -E '^nameserver' /etc/resolv.conf").stdout.strip()
    if out:
        return ("DNS", "INFO", short(out, 260))

    return ("DNS", "WARN", "DNS bilgisi okunamadı")


def check_proxy():
    keys = ["http_proxy", "https_proxy", "all_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"]
    found = []

    for key in keys:
        value = os.environ.get(key)
        if value:
            found.append(f"{key}={value}")

    if found:
        return ("Proxy", "INFO", short(" | ".join(found), 220))

    return ("Proxy", "OK", "Proxy değişkeni görünmüyor")


def check_tor():
    paths = [
        Path.home() / ".local/share/torbrowser",
        Path.home() / "tor-browser",
        Path("/usr/bin/torbrowser-launcher"),
    ]

    if exists("torbrowser-launcher"):
        return ("Tor Browser", "OK", "torbrowser-launcher bulundu")

    for path in paths:
        if path.exists():
            return ("Tor Browser", "OK", f"Bulundu: {path}")

    return ("Tor Browser", "WARN", "Tor Browser bulunamadı")


def check_bluetooth():
    if not exists("rfkill"):
        return ("Bluetooth", "WARN", "rfkill kurulu değil")

    service_state = run("systemctl is-active bluetooth 2>/dev/null").stdout.strip()
    rfkill_out = run("rfkill list bluetooth").stdout.strip().lower()

    if "soft blocked: yes" in rfkill_out or "hard blocked: yes" in rfkill_out:
        return ("Bluetooth", "OK", "Bluetooth rfkill ile kapalı / bloklu")

    if exists("bluetoothctl"):
        bt_out = run("bluetoothctl show 2>/dev/null").stdout.strip().lower()

        if "powered: no" in bt_out:
            return ("Bluetooth", "OK", "Bluetooth adaptörü kapalı")

        if "no default controller available" in bt_out:
            return ("Bluetooth", "OK", "Bluetooth denetleyici görünmüyor")

        if "powered: yes" in bt_out:
            return ("Bluetooth", "WARN", "Bluetooth adaptörü açık")

    if service_state in ["inactive", "failed", "unknown"]:
        return ("Bluetooth", "OK", "Bluetooth servisi kapalı")

    if service_state == "active":
        return ("Bluetooth", "INFO", "Bluetooth servisi aktif, adaptör durumu net değil")

    return ("Bluetooth", "INFO", "Bluetooth durumu net okunamadı")


def check_ssh():
    for service in ["ssh", "sshd"]:
        out = run(f"systemctl is-active {service} 2>/dev/null").stdout.strip()
        if out == "active":
            return ("SSH", "WARN", f"{service} servisi aktif")

    return ("SSH", "OK", "SSH aktif görünmüyor")


def check_apparmor():
    if not exists("aa-status"):
        return ("AppArmor", "WARN", "aa-status bulunamadı")

    out = run("aa-status").stdout.strip()

    if "apparmor module is loaded" in out or "profiles are loaded" in out:
        return ("AppArmor", "OK", "AppArmor aktif")

    return ("AppArmor", "WARN", short(out, 220))


def check_lxc():
    if not exists("lxc"):
        return ("LXC/LXD", "WARN", "lxc komutu bulunamadı")

    out = run("lxc --version").stdout.strip()
    if out:
        return ("LXC/LXD", "OK", f"lxc sürüm: {out}")

    return ("LXC/LXD", "WARN", "lxc var ama sürüm okunamadı")


def check_ports():
    if not exists("ss"):
        return ("Açık Portlar", "WARN", "ss komutu bulunamadı")

    out = run("ss -tulnH").stdout.strip().splitlines()

    if not out:
        return ("Açık Portlar", "OK", "Dinleyen port görünmüyor")

    ports = []
    for line in out[:8]:
        parts = line.split()
        if len(parts) >= 5:
            ports.append(parts[4])

    detail = ", ".join(ports) if ports else f"{len(out)} dinleyen kayıt var"

    if len(out) > 8:
        detail += f" ... toplam {len(out)} kayıt"

    return ("Açık Portlar", "INFO", detail)


def check_disk():
    out = run("lsblk -f").stdout.lower()

    if "crypto_luks" in out or "crypt" in out:
        return ("Disk Şifreleme", "OK", "LUKS / crypt tespit edildi")

    return ("Disk Şifreleme", "WARN", "Disk şifreleme tespit edilemedi")


def check_honeypot():
    out = run("ps aux | grep -i cowrie | grep -v grep | grep -v hudut_shield").stdout.strip()

    if out:
        return ("Honeypot", "INFO", "Cowrie süreci çalışıyor olabilir")

    return ("Honeypot", "OK", "Honeypot aktif görünmüyor")


def check_mac_randomization():
    con, dev = get_active_connection()
    if not con:
        return ("MAC Randomization", "WARN", "Aktif NetworkManager bağlantısı bulunamadı")

    qcon = quote(con)
    out = run(
        f"nmcli -g 802-3-ethernet.cloned-mac-address,802-11-wireless.cloned-mac-address "
        f"connection show {qcon} 2>/dev/null"
    ).stdout.strip()

    clean = out.replace("\n", " ").strip()

    if "random" in clean:
        return ("MAC Randomization", "OK", f"{con}: random")
    if "stable" in clean:
        return ("MAC Randomization", "OK", f"{con}: stable")
    if "permanent" in clean:
        return ("MAC Randomization", "WARN", f"{con}: permanent")
    if clean:
        return ("MAC Randomization", "INFO", f"{con}: {clean}")

    return ("MAC Randomization", "INFO", f"{con}: ayar belirtilmemiş")


def check_ipv6_privacy():
    out = run("sysctl net.ipv6.conf.all.use_tempaddr net.ipv6.conf.default.use_tempaddr 2>/dev/null").stdout.strip()

    if " = 2" in out:
        return ("IPv6 Privacy", "OK", "IPv6 temporary address / privacy aktif görünüyor")

    if " = 1" in out:
        return ("IPv6 Privacy", "INFO", "IPv6 privacy kısmen aktif")

    if out:
        return ("IPv6 Privacy", "WARN", short(out, 220))

    return ("IPv6 Privacy", "WARN", "IPv6 privacy durumu okunamadı")


def get_active_vpn_names():
    active = run("nmcli -t -f NAME,TYPE connection show --active 2>/dev/null").stdout.strip()
    vpn_names = []

    for line in active.splitlines():
        parts = line.split(":")
        if len(parts) >= 2 and parts[1].lower() in ["vpn", "wireguard"]:
            vpn_names.append(parts[0])

    return vpn_names


def get_vpn_profiles():
    out = run("nmcli -t -f NAME,TYPE connection show 2>/dev/null").stdout.strip()
    profiles = []

    for line in out.splitlines():
        parts = line.split(":")
        if len(parts) >= 2 and parts[1].lower() in ["vpn", "wireguard"]:
            profiles.append((parts[0], parts[1]))

    return profiles


def check_vpn():
    active_vpns = get_active_vpn_names()

    if active_vpns:
        return ("VPN", "OK", "Aktif VPN/WireGuard: " + ", ".join(active_vpns))

    if exists("wg"):
        wg = run("sudo -n wg show 2>/dev/null").stdout.strip()
        if wg:
            return ("VPN", "OK", "WireGuard aktif görünüyor")

    return ("VPN", "INFO", "Aktif VPN görünmüyor")


def show_vpn_status():
    print()
    print("HUDUT VPN DURUMU")
    print("=" * 86)

    name, state, detail = check_vpn()
    print(f"[{state:<4}] {name:<22} {detail}")

    active = run("nmcli -t -f NAME,TYPE,DEVICE connection show --active 2>/dev/null").stdout.strip()
    if active:
        print()
        print("Aktif bağlantılar:")
        for line in active.splitlines():
            print(f"- {line}")

    print("=" * 86)
    print()


def list_vpn_profiles():
    profiles = get_vpn_profiles()

    print()
    print("HUDUT VPN PROFİLLERİ")
    print("=" * 86)

    if not profiles:
        print("[INFO] Kayıtlı VPN/WireGuard profili bulunamadı.")
        print("Not: VPN profili NetworkManager üzerinden eklenmelidir.")
    else:
        for name, kind in profiles:
            print(f"[VPN] {name:<40} Tür: {kind}")

    print("=" * 86)
    print()


def connect_vpn(profile_name):
    if not profile_name:
        print("[ERROR] VPN profil adı boş olamaz.")
        return

    profiles = [name for name, kind in get_vpn_profiles()]
    if profile_name not in profiles:
        print(f"[ERROR] VPN profili bulunamadı: {profile_name}")
        list_vpn_profiles()
        return

    run_live(f"sudo nmcli connection up {quote(profile_name)}")
    print(f"[OK] VPN bağlantı denemesi yapıldı: {profile_name}")


def disconnect_vpn():
    active_vpns = get_active_vpn_names()

    if not active_vpns:
        print("[INFO] Aktif VPN bağlantısı bulunamadı.")
        return

    for vpn in active_vpns:
        run_live(f"sudo nmcli connection down {quote(vpn)}")

    print("[OK] Aktif VPN bağlantıları kapatıldı.")


def vpn_watch(interval=10):
    print()
    print("HUDUT VPN INTEGRITY MONITOR")
    print("=" * 86)
    print(f"VPN durumu her {interval} saniyede bir kontrol edilir.")
    print("Amaç: bağlantı bütünlüğü ve güvenli ağ farkındalığı.")
    print("Çıkmak için CTRL+C kullan.")
    print("=" * 86)

    try:
        while True:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            name, state, detail = check_vpn()

            if state == "OK":
                print(f"[{now}] [OK] VPN aktif: {detail}")
            else:
                print(f"[{now}] [WARN] VPN aktif görünmüyor: {detail}")

            time.sleep(interval)

    except KeyboardInterrupt:
        print()
        print("[INFO] VPN izleme durduruldu.")



def check_kernel_hardening():
    checks = [
        ("kernel.kptr_restrict", "eq", 2),
        ("kernel.dmesg_restrict", "eq", 1),
        ("kernel.yama.ptrace_scope", "eq", 1),
        ("kernel.perf_event_paranoid", "min", 3),
        ("kernel.unprivileged_bpf_disabled", "min", 1),
        ("kernel.kexec_load_disabled", "eq", 1),
        ("kernel.randomize_va_space", "eq", 2),
        ("kernel.sysrq", "eq", 0),
        ("fs.protected_hardlinks", "eq", 1),
        ("fs.protected_symlinks", "eq", 1),
        ("fs.protected_fifos", "min", 1),
        ("fs.protected_regular", "min", 1),
        ("net.ipv4.tcp_syncookies", "eq", 1),
        ("net.ipv4.conf.all.accept_redirects", "eq", 0),
        ("net.ipv6.conf.all.accept_redirects", "eq", 0),
        ("net.ipv4.conf.all.rp_filter", "min", 1),
    ]

    ok_count = 0
    total = len(checks)
    failed = []

    for key, mode, wanted in checks:
        result = run(f"sysctl -n {key} 2>/dev/null")
        raw = result.stdout.strip()

        try:
            current = int(raw)
        except ValueError:
            failed.append(f"{key}=N/A")
            continue

        if mode == "eq" and current == wanted:
            ok_count += 1
        elif mode == "min" and current >= wanted:
            ok_count += 1
        else:
            failed.append(f"{key}={current}")

    if ok_count == total:
        return ("Kernel Hardening", "OK", "Temel kernel sertleştirme aktif")

    if ok_count >= int(total * 0.70):
        return ("Kernel Hardening", "INFO", f"Kısmen aktif: {ok_count}/{total}")

    return ("Kernel Hardening", "WARN", f"Eksik ayar var: {ok_count}/{total}")


def check_microphone():
    if not exists("pactl"):
        return ("Mikrofon", "INFO", "pactl bulunamadı, mikrofon durumu okunamadı")

    out = run("pactl list sources 2>/dev/null").stdout

    if not out.strip():
        return ("Mikrofon", "INFO", "Mikrofon kaynağı görünmüyor")

    blocks = out.split("Source #")
    mic_states = []

    for block in blocks[1:]:
        lowered = block.lower()

        # Monitor kaynakları gerçek mikrofon değildir
        if 'device.class = "monitor"' in lowered:
            continue

        if "mute: yes" in lowered:
            mic_states.append(True)
        elif "mute: no" in lowered:
            mic_states.append(False)

    if not mic_states:
        return ("Mikrofon", "INFO", "Fiziksel mikrofon kaynağı net görünmüyor")

    if all(mic_states):
        return ("Mikrofon", "OK", "Mikrofon kaynakları kapalı / mute")

    return ("Mikrofon", "WARN", "Açık mikrofon kaynağı olabilir")


def check_camera():
    video_devices = list(Path("/dev").glob("video*"))

    if not video_devices:
        return ("Kamera", "OK", "Kamera cihazı görünmüyor")

    lsmod = run("lsmod | grep '^uvcvideo'").stdout.strip()

    if lsmod:
        devices = ", ".join(str(p) for p in video_devices[:4])
        return ("Kamera", "WARN", f"Kamera erişilebilir olabilir: {devices}")

    return ("Kamera", "INFO", "Video cihazı var ama uvcvideo modülü görünmüyor")


def apply_privacy_lock():
    print("[HUDUT] Mikrofon/Kamera privacy lock uygulanıyor...")

    if exists("pactl"):
        run_live("pactl list short sources 2>/dev/null | awk '{print $1}' | while read src; do pactl set-source-mute \"$src\" 1 2>/dev/null || true; done")
        print("[OK] Mikrofon kaynakları mute edilmeye çalışıldı.")
    else:
        print("[WARN] pactl bulunamadı, mikrofon mute işlemi atlandı.")

    run_live("sudo modprobe -r uvcvideo 2>/dev/null || true")
    print("[OK] Kamera modülü kapatılmaya çalışıldı.")
    print("[INFO] Kamera kullanımda ise kapatılamayabilir. Tarayıcı/kamera uygulamalarını kapatıp tekrar deneyebilirsin.")


def show_kernel_hardening_status():
    print()
    print("HUDUT KERNEL HARDENING KONTROLÜ")
    print("=" * 86)

    name, state, detail = check_kernel_hardening()
    print(f"[{state:<4}] {name:<22} {detail}")

    print()
    print("Detaylı kontrol için:")
    print("./scripts/check_kernel_hardening.sh")
    print("=" * 86)
    print()


def proxy_script_path():
    return BASE_DIR / "apps" / "proxy" / "hudut_proxy.py"


def run_proxy_manager(*args):
    script = proxy_script_path()

    if not script.exists():
        print(f"[WARN] Hudut Proxy Manager bulunamadı: {script}")
        print("[INFO] Beklenen dosya: apps/proxy/hudut_proxy.py")
        return

    cmd = "python3 " + quote(script) + " " + " ".join(quote(arg) for arg in args)
    run_live(cmd)


def show_proxy_status():
    run_proxy_manager("status")


def show_proxy_clear_command():
    run_proxy_manager("clear")


def show_firefox_proxy_status():
    run_proxy_manager("firefox-status")


def apply_firefox_proxy_direct():
    run_proxy_manager("firefox-direct", "--profile", "all")


def create_proxy_report():
    run_proxy_manager("report")


def show_proxy_summary():
    run_proxy_manager("summary")


def apply_profile_proxy_policy(profile):
    print()
    print("[HUDUT] Proxy profil politikası kontrol ediliyor...")

    if profile in ["secure", "public-wifi"]:
        print("[INFO] Bu profilde proxy temiz kullanım hedeflenir.")
        print("[INFO] Terminal proxy değişkenleri alt süreçten kalıcı silinemez; temizleme komutu gösterilecek.")
        print("[INFO] Firefox proxy direct moda alınacak.")
        show_proxy_clear_command()
        apply_firefox_proxy_direct()

    elif profile == "tor-research":
        print("[INFO] Tor Research profilinde Hudut Proxy Manager Tor Browser ayarlarına dokunmaz.")
        print("[INFO] Tüm sistem Tor ağına yönlendirilmez.")
        print("[INFO] Tor Browser kendi iç ağ davranışıyla kullanılmalıdır.")

    elif profile == "osint":
        print("[INFO] OSINT profilinde proxy zorla açılmaz veya kapatılmaz.")
        print("[INFO] Proxy kullanımı araştırmaya göre bilinçli seçilmelidir.")
        show_proxy_summary()

    elif profile in ["normal", "lab", "honeypot-lab"]:
        print("[INFO] Bu profilde proxy zorla değiştirilmez, sadece durum gösterilir.")
        show_proxy_summary()

    else:
        print("[INFO] Proxy için özel profil politikası yok.")



def status_lookup(items):
    return {name: (state, detail) for name, state, detail in items}


def print_single_status(status_map, label, fallback_name=None):
    key = fallback_name or label
    state, detail = status_map.get(key, ("INFO", "Durum okunamadı"))
    print(f"[{state:<4}] {label:<24} {detail}")


def print_profile_result_summary(profile):
    status_map = status_lookup(collect_status())

    print()
    print("HUDUT PROFILE RESULT SUMMARY")
    print(f"Uygulanan profil: {profile}")
    print("=" * 86)

    print_single_status(status_map, "Firewall")
    print_single_status(status_map, "DNS")
    print_single_status(status_map, "Proxy")
    print_single_status(status_map, "Bluetooth")
    print_single_status(status_map, "Mikrofon")
    print_single_status(status_map, "Kamera")
    print_single_status(status_map, "SSH")
    print_single_status(status_map, "AppArmor")
    print_single_status(status_map, "Kernel Hardening")
    print_single_status(status_map, "MAC Randomization")
    print_single_status(status_map, "IPv6 Privacy")
    print_single_status(status_map, "Tor Browser")
    print_single_status(status_map, "LXC/LXD")
    print_single_status(status_map, "Disk Şifreleme")
    print_single_status(status_map, "Honeypot")

    print()
    print("Proxy özeti:")
    show_proxy_summary()

    print("Profil yorumu:")

    if profile == "normal":
        print("- Günlük kullanım profili. Proxy değiştirilmedi, durum gösterildi.")
        print("- Mikrofon/kamera privacy lock uygulandı.")

    elif profile == "secure":
        print("- Güvenli profil. Firewall, DNS, SSH, Bluetooth, mikrofon/kamera ve proxy temizliği hedeflendi.")
        print("- Firefox direct moda alındı. Terminal için proxy temizleme komutu gösterildi.")

    elif profile == "osint":
        print("- OSINT profili. Proxy zorlanmadı; araştırmaya göre bilinçli seçilmeli.")
        print("- Kişisel hesaplarla karıştırılmamalı.")

    elif profile == "tor-research":
        print("- Tor Research profili. Tor Browser ayarlarına dokunulmadı.")
        print("- Tüm sistem Tor'a yönlendirilmedi. Tor Browser ayrı araştırma aracı olarak kalır.")

    elif profile == "public-wifi":
        print("- Public Wi-Fi profili. Ortak ağlar için Bluetooth/SSH kapatma, firewall ve MAC random hedeflendi.")
        print("- Firefox direct moda alındı. Terminal için proxy temizleme komutu gösterildi.")

    elif profile == "honeypot-lab":
        print("- Honeypot Lab profili. Honeypot ana sistemde değil LXC/VM içinde çalıştırılmalı.")
        print("- Proxy zorlanmadı, durum gösterildi.")

    elif profile == "lab":
        print("- Lab profili. Yerel test ve geliştirme için proxy zorlanmadı, durum gösterildi.")

    print("=" * 86)
    print()



def tor_research_dir():
    return BASE_DIR / "research" / "tor"


def tor_research_paths():
    tor_dir = tor_research_dir()
    return {
        "base": tor_dir,
        "downloads": tor_dir / "downloads",
        "notes": tor_dir / "notes",
        "screenshots": tor_dir / "screenshots",
        "reports": tor_dir / "reports",
        "evidence": tor_dir / "evidence",
        "warnings": tor_dir / "warnings.md",
        "template": tor_dir / "tor_research_template.md",
    }


def prepare_tor_research():
    paths = tor_research_paths()

    for key, path in paths.items():
        if path.suffix:
            continue
        path.mkdir(parents=True, exist_ok=True)

    if not paths["warnings"].exists():
        paths["warnings"].write_text(
            "# Hudut Tor Research Uyarıları\n\n"
            "- Kişisel hesaplara giriş yapma.\n"
            "- Eklenti kurma.\n"
            "- Torrent kullanma.\n"
            "- Bilinmeyen dosyaları ana sistemde açma.\n"
            "- Tor Browser dışında aynı araştırmayı kişisel tarayıcıyla sürdürme.\n"
            "- Tor Browser ayarlarına Hudut Proxy Manager ile müdahale etme.\n",
            encoding="utf-8"
        )

    if not paths["template"].exists():
        paths["template"].write_text(
            "# Hudut Tor Research Notu\n\n"
            "## Araştırma Bilgisi\n\n"
            "- Tarih:\n"
            "- Konu:\n"
            "- Amaç:\n"
            "- Kaynaklar:\n\n"
            "## Güvenlik Kontrolü\n\n"
            "- [ ] Kişisel hesaplara giriş yapılmadı\n"
            "- [ ] Eklenti kurulmadı\n"
            "- [ ] Torrent kullanılmadı\n"
            "- [ ] İndirilen dosyalar ana sistemde açılmadı\n"
            "- [ ] Kaynaklar kaydedildi\n\n"
            "## Bulgular\n\n"
            "-\n",
            encoding="utf-8"
        )

    print("[OK] Tor Research klasörleri hazırlandı.")
    print(f"[INFO] Ana klasör: {paths['base']}")


def check_tor_browser_status():
    candidates = [
        Path.home() / ".local/share/torbrowser",
        Path.home() / "tor-browser",
        Path.home() / "Downloads" / "tor-browser",
        Path.home() / "snap" / "tor-browser",
        Path("/usr/bin/torbrowser-launcher"),
        Path("/usr/bin/tor-browser"),
    ]

    if exists("torbrowser-launcher"):
        return ("Tor Browser", "OK", "torbrowser-launcher bulundu")

    if exists("tor-browser"):
        return ("Tor Browser", "OK", "tor-browser komutu bulundu")

    for path in candidates:
        if path.exists():
            return ("Tor Browser", "OK", f"Bulundu: {path}")

    return ("Tor Browser", "WARN", "Tor Browser bulunamadı")




def firefox_osint_manager_path():
    return BASE_DIR / "apps" / "firefox" / "hudut_firefox_osint.py"


def run_firefox_osint_manager(command):
    manager = firefox_osint_manager_path()

    if not manager.exists():
        print(f"[ERROR] Firefox OSINT manager bulunamadı: {manager}")
        return

    run_live(f"python3 {manager} {command}")


def firefox_osint_status():
    run_firefox_osint_manager("status")


def firefox_osint_prepare():
    run_firefox_osint_manager("prepare")


def firefox_osint_launch():
    print("[HUDUT] Firefox OSINT profili açılıyor...")
    print("[INFO] Bu profil Tor değildir. Açık web OSINT için ayrılmış Firefox profilidir.")
    print("[INFO] Kişisel hesaplara giriş yapılmamalıdır.")
    run_firefox_osint_manager("launch")


def firefox_osint_report():
    run_firefox_osint_manager("report")


def show_tor_service_status():
    print()
    print("HUDUT TOR SERVICE STATUS")
    print("Amaç: Sistem Tor servisi durumunu göstermek")
    print("=" * 86)

    print("[INFO] tor.service durumu:")
    run_live("systemctl status tor --no-pager || true")

    print()
    print("[INFO] tor@default.service durumu varsa:")
    run_live("systemctl status tor@default --no-pager || true")

    print()
    print("[INFO] Tor SOCKS port kontrolü:")
    run_live("ss -ltnp | grep -E ':9050|:9150' || true")

    print()
    print("Not:")
    print("- 9050 genelde sistem Tor servisi içindir.")
    print("- 9150 genelde Tor Browser iç Tor portu olabilir.")
    print("- Tor Browser normal kullanımda kendi bağlantısını yönetebilir.")
    print("=" * 86)
    print()


def start_tor_service():
    print()
    print("[HUDUT] Tor system service başlatılıyor...")
    print("[INFO] Bu işlem sistem Tor servisi içindir.")
    print("[INFO] Tor Browser normal kullanımda kendi bağlantısını ayrıca yönetebilir.")

    run_live("sudo systemctl start tor 2>/dev/null || true")
    run_live("sudo systemctl start tor@default 2>/dev/null || true")

    show_tor_service_status()


def stop_tor_service():
    print()
    print("[HUDUT] Tor system service durduruluyor...")
    print("[INFO] Tor Browser açıksa kendi iç bağlantısı ayrıca devam edebilir.")

    run_live("sudo systemctl stop tor@default 2>/dev/null || true")
    run_live("sudo systemctl stop tor 2>/dev/null || true")

    show_tor_service_status()


def show_tor_research_status():
    prepare_tor_research()

    print()
    print("HUDUT TOR RESEARCH PROFILE")
    print("Amaç: Tor Browser ile yasal araştırma hazırlığı")
    print("=" * 86)

    name, state, detail = check_tor_browser_status()
    print(f"[{state:<4}] {name:<22} {detail}")

    paths = tor_research_paths()

    for label, path in paths.items():
        if path.exists():
            print(f"[OK  ] {label:<22} {path}")
        else:
            print(f"[WARN] {label:<22} Eksik: {path}")

    print()
    print("V1 Kararı:")
    print("- Tüm sistem Tor ağına zorlanmaz.")
    print("- Tor Browser ayrı araştırma profili olarak kullanılır.")
    print("- Hudut Proxy Manager Tor Browser ayarlarına dokunmaz.")
    print("- Kişisel hesaplara giriş yapılmaz.")
    print("- Torrent kullanılmaz.")
    print("- Eklenti/plugin kurulmaz.")
    print("=" * 86)
    print()


def create_tor_research_note():
    prepare_tor_research()

    notes_dir = tor_research_dir() / "notes"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    note_path = notes_dir / f"tor-research-note-{timestamp}.md"

    template_path = tor_research_dir() / "tor_research_template.md"

    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
    else:
        content = "# Hudut Tor Research Notu\n\n## Bulgular\n\n-\n"

    note_path.write_text(content, encoding="utf-8")

    print(f"[OK] Tor Research notu oluşturuldu: {note_path}")


def collect_status():
    return [
        check_firewall(),
        check_dns(),
        check_proxy(),
        check_tor(),
        check_bluetooth(),
        check_microphone(),
        check_camera(),
        check_ssh(),
        check_apparmor(),
        check_kernel_hardening(),
        check_lxc(),
        check_ports(),
        check_disk(),
        check_honeypot(),
        check_mac_randomization(),
        check_ipv6_privacy(),
    ]


def collect_network_status():
    con, dev = get_active_connection()

    return [
        ("Aktif Bağlantı", "INFO", con or "bulunamadı"),
        ("Aktif Arayüz", "INFO", dev or get_default_interface()),
        ("IPv4", "INFO", get_ipv4()),
        ("IPv6", "INFO", get_ipv6()),
        check_dns(),
        check_proxy(),
        check_mac_randomization(),
        check_ipv6_privacy(),
        check_bluetooth(),
        check_ports(),
    ]


def print_table(title, rows):
    print()
    print(title)
    print("=" * 86)
    for name, state, detail in rows:
        print(f"[{state:<4}] {name:<22} {detail}")
    print("=" * 86)


def print_status():
    print_table(
        "HUDUT SHIELD SECURITY CENTER\nAmaç: Hudut Linux güvenlik durumunu kontrol etmek",
        collect_status()
    )

    print("Profil komutları:")
    for p in PROFILES:
        print(f"hudut-shield apply {p}")

    print()
    print("Network komutları:")
    print("hudut-shield network status")
    print("hudut-shield network report")
    print("hudut-shield network renew-ipv4")
    print("hudut-shield network dns secure")
    print("hudut-shield network mac stable")
    print("hudut-shield network mac random")
    print()
    print("Proxy komutları:")
    print("hudut-shield proxy status")
    print("hudut-shield proxy clear")
    print("hudut-shield proxy firefox-status")
    print("hudut-shield proxy firefox-direct")
    print("hudut-shield proxy report")
    print()


def print_network_status():
    print_table(
        "HUDUT NETWORK PROFILE MANAGER\nAmaç: Ağ, DNS, IP, MAC, IPv6 privacy, proxy ve açık port durumunu göstermek",
        collect_network_status()
    )


def print_profiles():
    print()
    print("HUDUT SHIELD PROFİL TABLOLARI")
    print("=" * 86)

    for profile, data in PROFILE_TABLES.items():
        print()
        print(f"[{profile.upper()}]")
        print("-" * 86)
        for key, value in data.items():
            print(f"{key:<14}: {value}")

    print("=" * 86)
    print()


def create_report():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = REPORT_DIR / f"security-status-{timestamp}.md"

    lines = []
    lines.append("# Hudut Shield Güvenlik Durum Raporu\n")
    lines.append(f"**Tarih:** {timestamp}\n")
    lines.append("## Durum Özeti\n")

    for name, state, detail in collect_status():
        lines.append(f"- **{name}:** `{state}` - {detail}")

    lines.append("\n## Not\n")
    lines.append("Bu rapor otomatik oluşturulmuştur. Bulgular manuel olarak doğrulanmalıdır.\n")

    path.write_text("\n".join(lines), encoding="utf-8")

    print(f"[OK] Rapor oluşturuldu: {path}")


def create_network_report():
    NETWORK_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = NETWORK_REPORT_DIR / f"network-status-{timestamp}.md"

    lines = []
    lines.append("# Hudut Network Durum Raporu\n")
    lines.append(f"**Tarih:** {timestamp}\n")
    lines.append("## Ağ Durumu\n")

    for name, state, detail in collect_network_status():
        lines.append(f"- **{name}:** `{state}` - {detail}")

    lines.append("\n## Not\n")
    lines.append("Bu rapor ağ durumunu gösterir. Yetkisiz erişim veya iz gizleme amacıyla kullanılmamalıdır.\n")

    path.write_text("\n".join(lines), encoding="utf-8")

    print(f"[OK] Network raporu oluşturuldu: {path}")


def confirm(profile):
    print()
    print(f"Uygulanacak profil: {profile}")
    print("Bu işlem firewall, SSH, Bluetooth, DNS veya NetworkManager ayarlarını değiştirebilir.")
    answer = input("Devam edilsin mi? [evet/HAYIR]: ").strip().lower()

    if answer not in ["evet", "e", "yes", "y"]:
        print("[CANCEL] İşlem iptal edildi.")
        raise SystemExit(1)


def apply_dns(profile):
    if profile not in DNS_PROFILES:
        print(f"[ERROR] DNS profili bilinmiyor: {profile}")
        return

    con, dev = get_active_connection()
    if not con:
        print("[ERROR] Aktif NetworkManager bağlantısı bulunamadı.")
        return

    conf = DNS_PROFILES[profile]
    ipv4_dns = conf.get("ipv4_dns", "")
    ipv6_dns = conf.get("ipv6_dns", "")

    if profile == "normal":
        run_live(f"sudo nmcli connection modify '{con}' ipv4.ignore-auto-dns no ipv4.dns ''")
        run_live(f"sudo nmcli connection modify '{con}' ipv6.ignore-auto-dns no ipv6.dns ''")
    else:
        if ipv4_dns:
            run_live(f"sudo nmcli connection modify '{con}' ipv4.ignore-auto-dns yes ipv4.dns '{ipv4_dns}'")

        if ipv6_dns:
            run_live(f"sudo nmcli connection modify '{con}' ipv6.ignore-auto-dns yes ipv6.dns '{ipv6_dns}'")
        else:
            run_live(f"sudo nmcli connection modify '{con}' ipv6.ignore-auto-dns no ipv6.dns ''")

    run_live(f"sudo nmcli connection up '{con}'")
    print(f"[OK] DNS profili uygulandı: {profile} - {conf['name']}")

def renew_ipv4():
    con, dev = get_active_connection()

    if not con:
        print("[ERROR] Aktif bağlantı bulunamadı.")
        return

    qcon = quote(con)

    print(f"[INFO] IPv4 DHCP yenileniyor: {con}")
    run_live(f"sudo nmcli connection down {qcon}")
    run_live(f"sudo nmcli connection up {qcon}")
    print("[OK] IPv4 DHCP yenileme denemesi tamamlandı.")


def set_mac_mode(mode):
    con, dev = get_active_connection()

    if not con:
        print("[ERROR] Aktif bağlantı bulunamadı.")
        return

    if mode not in ["stable", "random", "permanent"]:
        print("[ERROR] MAC modu stable/random/permanent olmalı.")
        return

    qcon = quote(con)

    print(f"[INFO] MAC modu ayarlanıyor: {mode}")

    run_live(f"sudo nmcli connection modify {qcon} 802-3-ethernet.cloned-mac-address {quote(mode)} 2>/dev/null || true")
    run_live(f"sudo nmcli connection modify {qcon} 802-11-wireless.cloned-mac-address {quote(mode)} 2>/dev/null || true")
    run_live(f"sudo nmcli connection up {qcon}")

    print(f"[OK] MAC randomization modu uygulandı: {mode}")


def apply_profile(profile):
    if profile not in PROFILES:
        print(f"[ERROR] Bilinmeyen profil: {profile}")
        raise SystemExit(1)

    confirm(profile)
    apply_privacy_lock()
    apply_profile_proxy_policy(profile)

    if profile == "normal":
        run_live("sudo ufw default deny incoming")
        run_live("sudo ufw default allow outgoing")
        run_live("sudo ufw logging on")
        run_live("sudo ufw --force enable")
        apply_dns("normal")
        print("[OK] Normal profil uygulandı.")

    elif profile == "secure":
        run_live("sudo ufw default deny incoming")
        run_live("sudo ufw default allow outgoing")
        run_live("sudo ufw logging on")
        run_live("sudo ufw --force enable")
        run_live("sudo systemctl disable --now ssh 2>/dev/null || true")
        run_live("sudo systemctl disable --now sshd 2>/dev/null || true")
        run_live("sudo rfkill block bluetooth 2>/dev/null || true")
        apply_dns("secure")
        set_mac_mode("stable")
        print("[OK] Secure profil uygulandı.")

    elif profile == "osint":
        run_live("sudo ufw default deny incoming")
        run_live("sudo ufw default allow outgoing")
        run_live("sudo ufw logging on")
        run_live("sudo ufw --force enable")
        (BASE_DIR / "research").mkdir(parents=True, exist_ok=True)
        (BASE_DIR / "reports").mkdir(parents=True, exist_ok=True)
        apply_dns("osint")
        set_mac_mode("stable")
        print("[OK] OSINT Research profili uygulandı.")

    elif profile == "tor-research":
        tor_dir = BASE_DIR / "research" / "tor"
        (tor_dir / "downloads").mkdir(parents=True, exist_ok=True)
        (tor_dir / "notes").mkdir(parents=True, exist_ok=True)
        (tor_dir / "warnings.md").write_text(
            "# Tor Research Uyarıları\n\n"
            "- Kişisel hesaplara giriş yapma.\n"
            "- Eklenti kurma.\n"
            "- Bilinmeyen dosyaları ana sistemde açma.\n"
            "- Tor Browser dışında aynı araştırmayı kişisel tarayıcıyla sürdürme.\n",
            encoding="utf-8"
        )
        run_live("sudo rfkill block bluetooth 2>/dev/null || true")
        set_mac_mode("stable")
        print("[OK] Tor Research klasörleri hazırlandı.")
        print("[INFO] V1 kararı: Tüm sistemi Tor'a zorlamıyoruz. Tor Browser ayrı kullanılacak.")

    elif profile == "public-wifi":
        run_live("sudo ufw default deny incoming")
        run_live("sudo ufw default allow outgoing")
        run_live("sudo ufw logging on")
        run_live("sudo ufw --force enable")
        run_live("sudo systemctl disable --now ssh 2>/dev/null || true")
        run_live("sudo systemctl disable --now sshd 2>/dev/null || true")
        run_live("sudo rfkill block bluetooth 2>/dev/null || true")
        apply_dns("secure")
        set_mac_mode("random")
        print("[OK] Public Wi-Fi profili uygulandı.")

    elif profile == "honeypot-lab":
        (BASE_DIR / "reports" / "honeypot").mkdir(parents=True, exist_ok=True)
        (BASE_DIR / "logs" / "honeypot").mkdir(parents=True, exist_ok=True)
        apply_dns("lab")
        print("[OK] Honeypot Lab klasörleri hazırlandı.")
        print("[INFO] Honeypot ana sistemde değil, LXC/VM içinde çalıştırılmalıdır.")

    elif profile == "lab":
        (BASE_DIR / "research" / "lab").mkdir(parents=True, exist_ok=True)
        apply_dns("lab")
        set_mac_mode("stable")
        print("[OK] Lab profili uygulandı.")

    print()
    print_profile_result_summary(profile)
    print_status()


def interactive_menu():
    while True:
        print()
        print("HUDUT SHIELD MENÜ")
        print("=" * 56)
        print("1. Genel güvenlik durumu")
        print("2. Ağ durumu göster")
        print("3. Profil tablolarını göster")
        print("4. Normal profil uygula")
        print("5. Secure profil uygula")
        print("6. OSINT profil uygula")
        print("7. Tor Research profil uygula")
        print("8. Public Wi-Fi profil uygula")
        print("9. Lab profil uygula")
        print("10. IPv4 DHCP yenile")
        print("11. DNS secure uygula")
        print("12. MAC stable random uygula")
        print("13. MAC random uygula")
        print("14. Network raporu üret")
        print("15. Security raporu üret")
        print("16. Kernel hardening kontrolü")
        print("17. Mikrofon/Kamera kapat")
        print("18. Proxy durumunu göster")
        print("19. Terminal proxy temizleme komutu")
        print("20. Firefox proxy durumunu göster")
        print("21. Firefox proxy direct yap")
        print("22. Proxy raporu üret")
        print("23. Proxy kısa özeti")
        print("24. Tor Research durumunu göster")
        print("25. Tor Research klasörlerini hazırla")
        print("26. Tor Research notu oluştur")
        print("27. Tor servis durumunu göster")
        print("28. Tor servisini başlat")
        print("29. Tor servisini durdur")
        print("30. Firefox OSINT durumunu göster")
        print("31. Firefox OSINT profilini hazırla")
        print("32. Firefox OSINT profilini aç")
        print("33. Firefox OSINT raporu üret")
        print("0. Çıkış")
        print("=" * 56)

        choice = input("Seçim: ").strip()

        if choice == "1":
            print_status()
        elif choice == "2":
            print_network_status()
        elif choice == "3":
            print_profiles()
        elif choice == "4":
            apply_profile("normal")
        elif choice == "5":
            apply_profile("secure")
        elif choice == "6":
            apply_profile("osint")
        elif choice == "7":
            apply_profile("tor-research")
        elif choice == "8":
            apply_profile("public-wifi")
        elif choice == "9":
            apply_profile("lab")
        elif choice == "10":
            renew_ipv4()
        elif choice == "11":
            apply_dns("secure")
        elif choice == "12":
            set_mac_mode("stable")
        elif choice == "13":
            set_mac_mode("random")
        elif choice == "14":
            create_network_report()
        elif choice == "15":
            create_report()
        elif choice == "16":
            show_kernel_hardening_status()
        elif choice == "17":
            apply_privacy_lock()
        elif choice == "18":
            show_proxy_status()
        elif choice == "19":
            show_proxy_clear_command()
        elif choice == "20":
            show_firefox_proxy_status()
        elif choice == "21":
            apply_firefox_proxy_direct()
        elif choice == "22":
            create_proxy_report()
        elif choice == "23":
            show_proxy_summary()
        elif choice == "24":
            show_tor_research_status()
        elif choice == "25":
            prepare_tor_research()
        elif choice == "26":
            create_tor_research_note()
        elif choice == "27":
            show_tor_service_status()
        elif choice == "28":
            start_tor_service()
        elif choice == "29":
            stop_tor_service()
        elif choice == "30":
            firefox_osint_status()
        elif choice == "31":
            firefox_osint_prepare()
        elif choice == "32":
            firefox_osint_launch()
        elif choice == "33":
            firefox_osint_report()
        elif choice == "0":
            print("Çıkılıyor.")
            break
        else:
            print("[ERROR] Geçersiz seçim.")


def main():
    parser = argparse.ArgumentParser(
        prog="hudut-shield",
        description="Hudut Linux Security Center"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Güvenlik durumunu göster")
    sub.add_parser("report", help="Güvenlik raporu oluştur")
    sub.add_parser("profiles", help="Profil tablolarını göster")
    sub.add_parser("menu", help="Etkileşimli Hudut Shield menüsü")

    apply_parser = sub.add_parser("apply", help="Güvenlik profili uygula")
    apply_parser.add_argument("profile", choices=PROFILES)

    tor_parser = sub.add_parser("tor", help="Tor Research profil işlemleri")
    tor_sub = tor_parser.add_subparsers(dest="tor_command")

    tor_sub.add_parser("status", help="Tor Research durumunu göster")
    tor_sub.add_parser("prepare", help="Tor Research klasörlerini hazırla")
    tor_sub.add_parser("note", help="Yeni Tor Research notu oluştur")
    tor_sub.add_parser("service-status", help="Tor systemd servis durumunu göster")
    tor_sub.add_parser("service-start", help="Tor systemd servisini başlat")
    tor_sub.add_parser("service-stop", help="Tor systemd servisini durdur")

    proxy_parser = sub.add_parser("proxy", help="Proxy durum, Firefox proxy ve rapor işlemleri")
    proxy_sub = proxy_parser.add_subparsers(dest="proxy_command")

    proxy_sub.add_parser("status", help="Proxy durumunu göster")
    proxy_sub.add_parser("clear", help="Terminal proxy temizleme komutunu göster")
    proxy_sub.add_parser("firefox-status", help="Firefox proxy durumunu göster")
    proxy_sub.add_parser("firefox-direct", help="Firefox proxy ayarını direct yap")
    proxy_sub.add_parser("summary", help="Proxy kısa özetini göster")
    proxy_sub.add_parser("report", help="Proxy raporu oluştur")

    network_parser = sub.add_parser("network", help="Ağ profili ve ağ durumu işlemleri")
    network_sub = network_parser.add_subparsers(dest="network_command")

    network_sub.add_parser("status", help="Ağ durumunu göster")
    network_sub.add_parser("report", help="Network raporu oluştur")
    network_sub.add_parser("renew-ipv4", help="IPv4 DHCP yenile")

    dns_parser = network_sub.add_parser("dns", help="DNS profili uygula")
    dns_parser.add_argument("profile", choices=list(DNS_PROFILES.keys()))

    mac_parser = network_sub.add_parser("mac", help="MAC randomization modu uygula")
    mac_parser.add_argument("mode", choices=["stable", "random", "permanent"])

    vpn_parser = network_sub.add_parser("vpn", help="VPN durum ve izleme işlemleri")
    vpn_sub = vpn_parser.add_subparsers(dest="vpn_command")

    vpn_sub.add_parser("status", help="VPN durumunu göster")
    vpn_sub.add_parser("list", help="VPN profillerini listele")
    vpn_sub.add_parser("disconnect", help="Aktif VPN bağlantısını kes")

    vpn_watch_parser = vpn_sub.add_parser("watch", help="VPN durumunu belirli aralıkla izle")
    vpn_watch_parser.add_argument("--interval", type=int, default=10)

    vpn_connect_parser = vpn_sub.add_parser("connect", help="Belirtilen VPN profiline bağlan")
    vpn_connect_parser.add_argument("profile_name")


    firefox_parser = sub.add_parser("firefox-osint", help="Firefox OSINT profil yönetimi")
    firefox_sub = firefox_parser.add_subparsers(dest="firefox_osint_command")
    firefox_sub.add_parser("status", help="Firefox OSINT profil durumunu göster")
    firefox_sub.add_parser("prepare", help="Firefox OSINT profilini hazırla")
    firefox_sub.add_parser("launch", help="Firefox OSINT profilini aç")
    firefox_sub.add_parser("report", help="Firefox OSINT raporu üret")

    args = parser.parse_args()

    if args.command == "status":
        print_status()

    elif args.command == "report":
        create_report()

    elif args.command == "profiles":
        print_profiles()

    elif args.command == "menu":
        interactive_menu()

    elif args.command == "apply":
        apply_profile(args.profile)

    elif args.command == "tor":
        if args.tor_command == "status":
            show_tor_research_status()
        elif args.tor_command == "prepare":
            prepare_tor_research()
        elif args.tor_command == "note":
            create_tor_research_note()
        elif args.tor_command == "service-status":
            show_tor_service_status()
        elif args.tor_command == "service-start":
            start_tor_service()
        elif args.tor_command == "service-stop":
            stop_tor_service()
        else:
            tor_parser.print_help()

    elif args.command == "firefox-osint":
        if args.firefox_osint_command == "status":
            firefox_osint_status()
        elif args.firefox_osint_command == "prepare":
            firefox_osint_prepare()
        elif args.firefox_osint_command == "launch":
            firefox_osint_launch()
        elif args.firefox_osint_command == "report":
            firefox_osint_report()
        else:
            firefox_parser.print_help()

    elif args.command == "proxy":
        if args.proxy_command == "status":
            show_proxy_status()
        elif args.proxy_command == "clear":
            show_proxy_clear_command()
        elif args.proxy_command == "firefox-status":
            show_firefox_proxy_status()
        elif args.proxy_command == "firefox-direct":
            apply_firefox_proxy_direct()
        elif args.proxy_command == "summary":
            show_proxy_summary()
        elif args.proxy_command == "report":
            create_proxy_report()
        else:
            proxy_parser.print_help()

    elif args.command == "network":
        if args.network_command == "status":
            print_network_status()
        elif args.network_command == "report":
            create_network_report()
        elif args.network_command == "renew-ipv4":
            renew_ipv4()
        elif args.network_command == "dns":
            apply_dns(args.profile)
        elif args.network_command == "mac":
            set_mac_mode(args.mode)
        elif args.network_command == "vpn":
            if args.vpn_command == "status":
                show_vpn_status()
            elif args.vpn_command == "list":
                list_vpn_profiles()
            elif args.vpn_command == "disconnect":
                disconnect_vpn()
            elif args.vpn_command == "watch":
                vpn_watch(args.interval)
            elif args.vpn_command == "connect":
                connect_vpn(args.profile_name)
            else:
                vpn_parser.print_help()
        else:
            network_parser.print_help()

    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Hudut Shield kapatıldı.")
