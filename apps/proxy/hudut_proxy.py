#!/usr/bin/env python3
"""
Hudut Proxy Manager

Amaç:
Firefox ve terminal için proxy durumunu yönetmek, göstermek, temizlemek ve raporlamak.

V1 sınırı:
- Sistem geneli proxy ayarı yapmaz.
- GNOME/XFCE sistem proxy ayarlarına dokunmaz.
- Tor Browser ayarlarına dokunmaz.
- Terminal environment değişkenlerini doğrudan değiştirmez; sadece export/unset komutu üretir.
- Firefox normal profilleri için user.js içinde sadece Hudut proxy bloğunu yönetir.
- user.js dosyasını tamamen overwrite etmez.
- Anonimlik garantisi vermez.

Not:
Proxy tek başına anonimlik sağlamaz. DNS, tarayıcı profili, çerezler,
kişisel hesap kullanımı, WebRTC, indirme davranışı ve hedef servis logları
ayrı risk alanlarıdır. Tor kullanımı için Tor Browser önerilir.
"""

import argparse
import datetime
import os
from pathlib import Path


BASE_DIR = Path.home() / "hudut-linux"
REPORT_DIR = BASE_DIR / "reports" / "network"
FIREFOX_DIRS = [
    Path.home() / ".mozilla" / "firefox",
    Path.home() / "snap" / "firefox" / "common" / ".mozilla" / "firefox",
    Path.home() / ".var" / "app" / "org.mozilla.firefox" / ".mozilla" / "firefox",
]

HUDUT_PROXY_START = "// HUDUT_PROXY_START"
HUDUT_PROXY_END = "// HUDUT_PROXY_END"

PROXY_KEYS = [
    "http_proxy",
    "https_proxy",
    "ftp_proxy",
    "all_proxy",
    "no_proxy",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "FTP_PROXY",
    "ALL_PROXY",
    "NO_PROXY",
]

FIREFOX_PROXY_PREFS = [
    "network.proxy.type",
    "network.proxy.http",
    "network.proxy.http_port",
    "network.proxy.ssl",
    "network.proxy.ssl_port",
    "network.proxy.ftp",
    "network.proxy.ftp_port",
    "network.proxy.socks",
    "network.proxy.socks_port",
    "network.proxy.socks_version",
    "network.proxy.socks_remote_dns",
    "network.proxy.no_proxies_on",
    "network.proxy.share_proxy_settings",
]


# ------------------------------------------------------------
# Genel yardımcılar
# ------------------------------------------------------------

def now_stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def ensure_report_dir():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def short(text, limit=220):
    text = " ".join(str(text).strip().split())
    if not text:
        return "Bilgi yok"
    return text[:limit] + "..." if len(text) > limit else text


# ------------------------------------------------------------
# Terminal proxy durumu
# ------------------------------------------------------------

def get_terminal_proxy_vars():
    found = []

    for key in PROXY_KEYS:
        value = os.environ.get(key)
        if value:
            found.append((key, value))

    return found


def print_terminal_status():
    proxies = get_terminal_proxy_vars()

    print()
    print("HUDUT TERMINAL PROXY STATUS")
    print("=" * 86)

    if not proxies:
        print("[OK  ] Terminal proxy değişkeni görünmüyor.")
    else:
        print("[INFO] Terminal proxy değişkenleri bulundu:")
        for key, value in proxies:
            print(f"[INFO] {key:<12} {value}")

    print()
    print("Not:")
    print("Bu kontrol sadece mevcut terminal oturumundaki environment değişkenlerini okur.")
    print("Sistem geneli proxy ayarı yapmaz ve masaüstü ayarlarına dokunmaz.")
    print("Proxy anonimlik garantisi vermez.")
    print("=" * 86)
    print()


def build_export_commands(proxy_type, host, port, no_proxy):
    if proxy_type == "http":
        proxy_url = f"http://{host}:{port}"
        return [
            f'export http_proxy="{proxy_url}"',
            f'export https_proxy="{proxy_url}"',
            f'export HTTP_PROXY="{proxy_url}"',
            f'export HTTPS_PROXY="{proxy_url}"',
            f'export no_proxy="{no_proxy}"',
            f'export NO_PROXY="{no_proxy}"',
        ]

    if proxy_type == "socks5":
        # socks5h:// DNS çözümlemeyi proxy tarafına bırakmayı hedefler.
        # İnsanlığın socks5:// ile DNS sızıntısı üretme geleneğine küçük bir set.
        proxy_url = f"socks5h://{host}:{port}"
        return [
            f'export all_proxy="{proxy_url}"',
            f'export ALL_PROXY="{proxy_url}"',
            f'export no_proxy="{no_proxy}"',
            f'export NO_PROXY="{no_proxy}"',
        ]

    raise ValueError(f"Bilinmeyen proxy tipi: {proxy_type}")


def print_terminal_export(proxy_type, host, port, no_proxy):
    commands = build_export_commands(proxy_type, host, port, no_proxy)

    print()
    print("HUDUT TERMINAL PROXY EXPORT")
    print("=" * 86)
    print("Aşağıdaki komutlar sadece mevcut terminal oturumu için geçicidir:")
    print()

    for cmd in commands:
        print(cmd)

    print()
    print("Kontrol:")
    print("python3 apps/proxy/hudut_proxy.py status")
    print("=" * 86)
    print()


def build_clear_command():
    return "unset " + " ".join(PROXY_KEYS)


def print_terminal_clear():
    print()
    print("HUDUT TERMINAL PROXY CLEAR")
    print("=" * 86)
    print("Mevcut terminal oturumundaki proxy değişkenlerini temizlemek için:")
    print()
    print(build_clear_command())
    print()
    print("Not:")
    print("Bu komut sadece mevcut terminal oturumunu etkiler.")
    print(".bashrc, .profile veya başka dosyalara yazılmış kalıcı proxy satırlarını silmez.")
    print("=" * 86)
    print()


# ------------------------------------------------------------
# Firefox profil / user.js yönetimi
# ------------------------------------------------------------

def is_tor_browser_profile(path):
    lowered = str(path).lower()

    tor_markers = [
        "tor browser",
        "tor-browser",
        "torbrowser",
        "browser/torbrowser",
        "/tor/",
        "\\tor\\",
    ]

    return any(marker in lowered for marker in tor_markers)


def find_firefox_profiles():
    profiles = []

    for firefox_dir in FIREFOX_DIRS:
        if not firefox_dir.exists():
            continue

        for prefs_file in firefox_dir.glob("*/prefs.js"):
            profile = prefs_file.parent

            if is_tor_browser_profile(profile):
                continue

            profiles.append(profile)

        for user_file in firefox_dir.glob("*/user.js"):
            profile = user_file.parent

            if is_tor_browser_profile(profile):
                continue

            if profile not in profiles:
                profiles.append(profile)

    return sorted(set(profiles))


def resolve_firefox_profiles(profile_name):
    profiles = find_firefox_profiles()

    if profile_name == "all":
        return profiles

    selected = []

    for profile in profiles:
        if profile.name == profile_name or profile_name in profile.name:
            selected.append(profile)

    return selected


def read_firefox_proxy_lines(profile):
    lines = []

    for filename in ["user.js", "prefs.js"]:
        path = profile / filename

        if not path.exists():
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for line in content.splitlines():
            if "network.proxy." in line:
                lines.append((filename, line.strip()))

    return lines



def detect_firefox_proxy_mode_from_lines(proxy_lines):
    joined = "\n".join(line for _, line in proxy_lines)

    if 'network.proxy.type", 0' in joined:
        return "KAPALI / DIRECT"

    if 'network.proxy.type", 1' in joined:
        if "network.proxy.socks" in joined:
            if 'network.proxy.socks_remote_dns", true' in joined:
                return "AÇIK / SOCKS5 + remote DNS"
            return "AÇIK / SOCKS5"
        if "network.proxy.http" in joined or "network.proxy.ssl" in joined:
            return "AÇIK / HTTP-HTTPS"
        return "AÇIK / MANUAL"

    if 'network.proxy.type", 5' in joined:
        return "SİSTEM PROXY / V1 DIŞI"

    return "BİLİNMİYOR"


def print_proxy_summary():
    print()
    print("HUDUT PROXY SUMMARY")
    print("=" * 86)

    terminal_proxies = get_terminal_proxy_vars()

    if terminal_proxies:
        print("[INFO] Terminal Proxy       AÇIK")
        for key, value in terminal_proxies:
            print(f"[INFO] {key:<20} {value}")
    else:
        print("[OK  ] Terminal Proxy       KAPALI")

    profiles = find_firefox_profiles()

    if not profiles:
        print("[WARN] Firefox Proxy        Firefox profili bulunamadı")
    else:
        for profile in profiles:
            proxy_lines = read_firefox_proxy_lines(profile)
            if not proxy_lines:
                print(f"[OK  ] Firefox Proxy        {profile.name}: KAPALI / AYAR YOK")
            else:
                mode = detect_firefox_proxy_mode_from_lines(proxy_lines)
                print(f"[INFO] Firefox Proxy        {profile.name}: {mode}")

    print("[INFO] Tor Browser          Proxy Manager Tor Browser ayarlarına dokunmaz")
    print("=" * 86)
    print()


def print_firefox_status():
    profiles = find_firefox_profiles()

    print()
    print("HUDUT FIREFOX PROXY STATUS")
    print("=" * 86)

    if not profiles:
        print("[WARN] Firefox profili bulunamadı.")
        print("Kontrol edilen klasörler:")
        for firefox_dir in FIREFOX_DIRS:
            print(f"- {firefox_dir}")
        print("=" * 86)
        print()
        return

    for profile in profiles:
        proxy_lines = read_firefox_proxy_lines(profile)

        print()
        print(f"[PROFILE] {profile.name}")
        print(f"[PATH   ] {profile}")

        if not proxy_lines:
            print("[OK    ] Proxy ayarı görünmüyor.")
            continue

        for filename, line in proxy_lines:
            print(f"[INFO  ] {filename:<8} {line}")

    print()
    print("Not:")
    print("Tor Browser profilleri bu listeye dahil edilmez ve değiştirilmez.")
    print("=" * 86)
    print()


def backup_firefox_user_js(profile):
    user_js = profile / "user.js"

    if not user_js.exists():
        return None

    backup = profile / f"user.js.hudut-backup-{now_stamp()}"
    backup.write_text(
        user_js.read_text(encoding="utf-8", errors="ignore"),
        encoding="utf-8"
    )

    return backup


def remove_existing_hudut_proxy_block(content):
    """
    user.js içindeki eski Hudut proxy bloğunu kaldırır.
    Dosyanın geri kalanına dokunmaz.

    Blok yapısı:
    // HUDUT_PROXY_START
    ...
    // HUDUT_PROXY_END
    """

    lines = content.splitlines()
    new_lines = []

    inside_hudut_block = False

    for line in lines:
        if line.strip() == HUDUT_PROXY_START:
            inside_hudut_block = True
            continue

        if line.strip() == HUDUT_PROXY_END:
            inside_hudut_block = False
            continue

        if not inside_hudut_block:
            new_lines.append(line)

    # Sonda gereksiz boşluk patlamasını azalt.
    while new_lines and not new_lines[-1].strip():
        new_lines.pop()

    return "\n".join(new_lines)


def build_hudut_proxy_block(lines):
    block = []

    block.append(HUDUT_PROXY_START)
    block.append("// Hudut Linux Firefox Proxy Settings")
    block.append("// Bu blok Hudut Proxy Manager tarafından oluşturuldu.")
    block.append("// user.js dosyasının geri kalanına dokunulmaz.")
    block.append("// Tor Browser ayarlarına dokunulmaz.")
    block.append("// Proxy anonimlik garantisi vermez.")
    block.append(f"// Tarih: {now_stamp()}")
    block.append("")

    block.extend(lines)

    block.append(HUDUT_PROXY_END)

    return "\n".join(block)


def write_firefox_hudut_block(profile, lines):
    profile.mkdir(parents=True, exist_ok=True)

    if is_tor_browser_profile(profile):
        print(f"[SKIP] Tor Browser profili atlandı: {profile}")
        return

    user_js = profile / "user.js"

    old_content = ""
    if user_js.exists():
        backup = backup_firefox_user_js(profile)
        if backup:
            print(f"[OK] Yedek alındı: {backup}")

        old_content = user_js.read_text(encoding="utf-8", errors="ignore")

    cleaned_content = remove_existing_hudut_proxy_block(old_content)
    hudut_block = build_hudut_proxy_block(lines)

    if cleaned_content.strip():
        new_content = cleaned_content.rstrip() + "\n\n" + hudut_block + "\n"
    else:
        new_content = hudut_block + "\n"

    user_js.write_text(new_content, encoding="utf-8")

    print(f"[OK] Firefox user.js Hudut proxy bloğu güncellendi: {user_js}")


def firefox_direct_lines():
    return [
        'user_pref("network.proxy.type", 0);',
    ]


def firefox_http_lines(host, port, no_proxy):
    return [
        'user_pref("network.proxy.type", 1);',
        f'user_pref("network.proxy.http", "{host}");',
        f'user_pref("network.proxy.http_port", {int(port)});',
        f'user_pref("network.proxy.ssl", "{host}");',
        f'user_pref("network.proxy.ssl_port", {int(port)});',
        'user_pref("network.proxy.share_proxy_settings", true);',
        f'user_pref("network.proxy.no_proxies_on", "{no_proxy}");',
    ]


def firefox_socks_lines(host, port, no_proxy):
    return [
        'user_pref("network.proxy.type", 1);',
        f'user_pref("network.proxy.socks", "{host}");',
        f'user_pref("network.proxy.socks_port", {int(port)});',
        'user_pref("network.proxy.socks_version", 5);',
        'user_pref("network.proxy.socks_remote_dns", true);',
        f'user_pref("network.proxy.no_proxies_on", "{no_proxy}");',
    ]


def apply_firefox_proxy(profile_name, mode, host=None, port=None, no_proxy="localhost, 127.0.0.1"):
    profiles = resolve_firefox_profiles(profile_name)

    if not profiles:
        print(f"[ERROR] Firefox profili bulunamadı: {profile_name}")
        print("Önce şunu çalıştır:")
        print("python3 apps/proxy/hudut_proxy.py firefox-status")
        return

    if mode == "direct":
        lines = firefox_direct_lines()
    elif mode == "http":
        lines = firefox_http_lines(host, port, no_proxy)
    elif mode == "socks5":
        lines = firefox_socks_lines(host, port, no_proxy)
    else:
        print(f"[ERROR] Bilinmeyen Firefox proxy modu: {mode}")
        return

    for profile in profiles:
        write_firefox_hudut_block(profile, lines)

    print()
    print("[INFO] Firefox açıksa kapatıp yeniden açman gerekebilir.")
    print("[INFO] Tor Browser ayarlarına dokunulmadı.")
    print()


# ------------------------------------------------------------
# Rapor
# ------------------------------------------------------------

def create_report():
    ensure_report_dir()

    timestamp = now_stamp()
    path = REPORT_DIR / f"proxy-status-{timestamp}.md"

    terminal_proxies = get_terminal_proxy_vars()
    firefox_profiles = find_firefox_profiles()

    lines = []

    lines.append("# Hudut Proxy Durum Raporu\n")
    lines.append(f"**Tarih:** {timestamp}\n")

    lines.append("## Amaç\n")
    lines.append(
        "Firefox ve terminal için proxy durumunu yönetmek, göstermek, temizlemek ve raporlamak.\n"
    )

    lines.append("## Terminal Proxy Durumu\n")

    if terminal_proxies:
        for key, value in terminal_proxies:
            lines.append(f"- **{key}:** `{value}`")
    else:
        lines.append("- Terminal proxy değişkeni görünmüyor.")

    lines.append("\n## Firefox Proxy Durumu\n")

    if firefox_profiles:
        for profile in firefox_profiles:
            lines.append(f"### {profile.name}\n")
            lines.append(f"- **Path:** `{profile}`")

            proxy_lines = read_firefox_proxy_lines(profile)

            if proxy_lines:
                for filename, line in proxy_lines:
                    lines.append(f"- `{filename}`: `{line}`")
            else:
                lines.append("- Proxy ayarı görünmüyor.")
    else:
        lines.append("- Firefox profili bulunamadı.")

    lines.append("\n## Tor Browser Notu\n")
    lines.append(
        "- Tor Browser ayarlarına dokunulmadı. Tor kullanımı kendi tarayıcı ayarları içinde değerlendirilmelidir."
    )

    lines.append("\n## Etik / Güvenlik Notu\n")
    lines.append(
        "- Proxy anonimlik garantisi vermez. DNS, tarayıcı profili, çerezler, kişisel hesap kullanımı, WebRTC, indirme davranışı ve hedef servis logları ayrıca değerlendirilmelidir."
    )

    path.write_text("\n".join(lines), encoding="utf-8")

    print(f"[OK] Proxy raporu oluşturuldu: {path}")


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="hudut-proxy",
        description="Hudut Linux Proxy Manager"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser(
        "status",
        help="Terminal proxy durumunu göster"
    )

    export_parser = sub.add_parser(
        "export",
        help="Terminal için geçici proxy export komutu üret"
    )
    export_parser.add_argument(
        "--type",
        choices=["http", "socks5"],
        required=True,
        help="Proxy tipi"
    )
    export_parser.add_argument(
        "--host",
        required=True,
        help="Proxy host"
    )
    export_parser.add_argument(
        "--port",
        required=True,
        type=int,
        help="Proxy port"
    )
    export_parser.add_argument(
        "--no-proxy",
        default="localhost, 127.0.0.1",
        help="Proxy dışı bırakılacak adresler"
    )

    sub.add_parser(
        "clear",
        help="Terminal proxy temizleme komutu üret"
    )

    sub.add_parser(
        "shell-clear",
        help="Sadece unset komutunu sade çıktı olarak üret"
    )

    sub.add_parser(
        "summary",
        help="Terminal ve Firefox proxy kısa özetini göster"
    )

    sub.add_parser(
        "firefox-status",
        help="Firefox profillerindeki proxy ayarlarını göster"
    )

    firefox_direct = sub.add_parser(
        "firefox-direct",
        help="Firefox proxy ayarını doğrudan bağlantı yap"
    )
    firefox_direct.add_argument(
        "--profile",
        default="all",
        help="Firefox profil adı veya all"
    )

    firefox_http = sub.add_parser(
        "firefox-http",
        help="Firefox HTTP/HTTPS proxy ayarla"
    )
    firefox_http.add_argument(
        "--profile",
        default="all",
        help="Firefox profil adı veya all"
    )
    firefox_http.add_argument(
        "--host",
        required=True,
        help="Proxy host"
    )
    firefox_http.add_argument(
        "--port",
        required=True,
        type=int,
        help="Proxy port"
    )
    firefox_http.add_argument(
        "--no-proxy",
        default="localhost, 127.0.0.1",
        help="Proxy dışı bırakılacak adresler"
    )

    firefox_socks = sub.add_parser(
        "firefox-socks",
        help="Firefox SOCKS5 proxy ayarla"
    )
    firefox_socks.add_argument(
        "--profile",
        default="all",
        help="Firefox profil adı veya all"
    )
    firefox_socks.add_argument(
        "--host",
        required=True,
        help="Proxy host"
    )
    firefox_socks.add_argument(
        "--port",
        required=True,
        type=int,
        help="Proxy port"
    )
    firefox_socks.add_argument(
        "--no-proxy",
        default="localhost, 127.0.0.1",
        help="Proxy dışı bırakılacak adresler"
    )

    sub.add_parser(
        "report",
        help="Proxy durum raporu oluştur"
    )

    args = parser.parse_args()

    if args.command == "status":
        print_terminal_status()

    elif args.command == "export":
        print_terminal_export(
            proxy_type=args.type,
            host=args.host,
            port=args.port,
            no_proxy=args.no_proxy
        )

    elif args.command == "clear":
        print_terminal_clear()

    elif args.command == "shell-clear":
        print(build_clear_command())

    elif args.command == "summary":
        print_proxy_summary()

    elif args.command == "firefox-status":
        print_firefox_status()

    elif args.command == "firefox-direct":
        apply_firefox_proxy(
            profile_name=args.profile,
            mode="direct"
        )

    elif args.command == "firefox-http":
        apply_firefox_proxy(
            profile_name=args.profile,
            mode="http",
            host=args.host,
            port=args.port,
            no_proxy=args.no_proxy
        )

    elif args.command == "firefox-socks":
        apply_firefox_proxy(
            profile_name=args.profile,
            mode="socks5",
            host=args.host,
            port=args.port,
            no_proxy=args.no_proxy
        )

    elif args.command == "report":
        create_report()

    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Hudut Proxy Manager kapatıldı.")
