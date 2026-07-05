#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import os
import re
import shutil
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parents[2]
PROFILE_NAME = "hudut-osint"
PROFILE_DIR_NAME = "hudut-osint"
MARKER_START = "/* HUDUT_FIREFOX_OSINT_START */"
MARKER_END = "/* HUDUT_FIREFOX_OSINT_END */"


def run(cmd):
    print(f"[RUN] {cmd}")
    return subprocess.run(cmd, shell=True)


def firefox_base_candidates():
    home = Path.home()
    return [
        home / "snap/firefox/common/.mozilla/firefox",
        home / ".mozilla/firefox",
        home / ".var/app/org.mozilla.firefox/.mozilla/firefox",
    ]


def detect_firefox_base():
    for candidate in firefox_base_candidates():
        if candidate.exists():
            return candidate

    # Xubuntu/Snap için en mantıklı varsayılan
    return Path.home() / "snap/firefox/common/.mozilla/firefox"


def profiles_ini_path():
    return detect_firefox_base() / "profiles.ini"


def profile_path():
    return detect_firefox_base() / PROFILE_DIR_NAME


def research_paths():
    root = BASE_DIR / "research" / "firefox"
    return {
        "root": root,
        "downloads": root / "downloads",
        "notes": root / "notes",
        "screenshots": root / "screenshots",
        "evidence": root / "evidence",
        "reports": root / "reports",
    }


def ensure_research_dirs():
    for path in research_paths().values():
        path.mkdir(parents=True, exist_ok=True)


def ensure_profiles_ini():
    base = detect_firefox_base()
    base.mkdir(parents=True, exist_ok=True)

    ini = profiles_ini_path()
    if not ini.exists():
        ini.write_text("[General]\nStartWithLastProfile=1\nVersion=2\n\n", encoding="utf-8")

    text = ini.read_text(encoding="utf-8", errors="ignore")

    # Profil zaten ekliyse dokunma
    if re.search(r"(?m)^Name=" + re.escape(PROFILE_NAME) + r"$", text):
        return False

    indexes = [int(x) for x in re.findall(r"\[Profile(\d+)\]", text)]
    next_index = max(indexes) + 1 if indexes else 0

    section = (
        f"\n[Profile{next_index}]\n"
        f"Name={PROFILE_NAME}\n"
        f"IsRelative=1\n"
        f"Path={PROFILE_DIR_NAME}\n"
    )

    ini.write_text(text.rstrip() + "\n" + section + "\n", encoding="utf-8")
    return True


def osint_user_js_block():
    downloads = research_paths()["downloads"]
    return f'''{MARKER_START}
// Hudut Firefox OSINT Profile
// Amaç: Kişisel Firefox profilinden ayrı, açık web OSINT araştırma profili.
// Not: Bu profil Tor değildir. Trafik normal internet üzerinden gider.

user_pref("browser.startup.homepage", "about:blank");
user_pref("browser.shell.checkDefaultBrowser", false);

// Proxy kapalı / direct
user_pref("network.proxy.type", 0);

// Parola ve form kayıtlarını kapat
user_pref("signon.rememberSignons", false);
user_pref("signon.autofillForms", false);
user_pref("browser.formfill.enable", false);
user_pref("extensions.formautofill.addresses.enabled", false);
user_pref("extensions.formautofill.creditCards.enabled", false);

// Arama önerileri ve URL önerilerini azalt
user_pref("browser.search.suggest.enabled", false);
user_pref("browser.urlbar.suggest.searches", false);
user_pref("browser.urlbar.suggest.history", false);
user_pref("browser.urlbar.suggest.bookmark", false);
user_pref("browser.urlbar.suggest.openpage", false);
user_pref("browser.urlbar.suggest.topsites", false);

// Takip koruması
user_pref("privacy.trackingprotection.enabled", true);
user_pref("privacy.trackingprotection.socialtracking.enabled", true);
user_pref("privacy.trackingprotection.cryptomining.enabled", true);
user_pref("privacy.trackingprotection.fingerprinting.enabled", true);

// HTTPS-only
user_pref("dom.security.https_only_mode", true);

// WebRTC / konum / kamera / mikrofon kısıtları
user_pref("media.peerconnection.enabled", false);
user_pref("geo.enabled", false);
user_pref("permissions.default.geo", 2);
user_pref("permissions.default.camera", 2);
user_pref("permissions.default.microphone", 2);

// İndirme klasörü
user_pref("browser.download.useDownloadDir", true);
user_pref("browser.download.folderList", 2);
user_pref("browser.download.dir", "{downloads}");

// Telemetri / raporlama azaltma
user_pref("datareporting.healthreport.uploadEnabled", false);
user_pref("datareporting.policy.dataSubmissionEnabled", false);
user_pref("toolkit.telemetry.enabled", false);
user_pref("toolkit.telemetry.unified", false);
user_pref("app.shield.optoutstudies.enabled", false);
user_pref("extensions.pocket.enabled", false);

// Çıkışta temizlik
user_pref("privacy.sanitize.sanitizeOnShutdown", true);
user_pref("privacy.clearOnShutdown.cookies", true);
user_pref("privacy.clearOnShutdown.cache", true);
user_pref("privacy.clearOnShutdown.offlineApps", true);
user_pref("privacy.clearOnShutdown.sessions", true);

// Parmak izi azaltma. Bazı siteleri bozarsa bu satır kapatılabilir.
user_pref("privacy.resistFingerprinting", true);

{MARKER_END}
'''


def write_user_js():
    pdir = profile_path()
    pdir.mkdir(parents=True, exist_ok=True)

    user_js = pdir / "user.js"
    block = osint_user_js_block()

    if user_js.exists():
        text = user_js.read_text(encoding="utf-8", errors="ignore")
        pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
        if pattern.search(text):
            text = pattern.sub(block.strip(), text)
        else:
            text = text.rstrip() + "\n\n" + block
    else:
        text = block

    user_js.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_launcher():
    launcher = BASE_DIR / "launchers" / "hudut-firefox-osint.desktop"
    launcher.parent.mkdir(parents=True, exist_ok=True)

    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Hudut Firefox OSINT
Comment=Open separated Firefox OSINT profile
Exec=python3 {BASE_DIR}/apps/firefox/hudut_firefox_osint.py launch
Icon=firefox
Terminal=false
Categories=Network;Security;Research;
"""
    launcher.write_text(content, encoding="utf-8")
    launcher.chmod(0o755)
    return launcher


def prepare():
    ensure_research_dirs()
    changed = ensure_profiles_ini()
    write_user_js()
    launcher = write_launcher()

    print("[OK] Firefox OSINT profili hazırlandı.")
    print(f"[INFO] Firefox base: {detect_firefox_base()}")
    print(f"[INFO] Profil adı: {PROFILE_NAME}")
    print(f"[INFO] Profil yolu: {profile_path()}")
    print(f"[INFO] user.js: {profile_path() / 'user.js'}")
    print(f"[INFO] Launcher: {launcher}")

    if changed:
        print("[INFO] profiles.ini içine hudut-osint profili eklendi.")
    else:
        print("[INFO] profiles.ini içinde hudut-osint profili zaten vardı.")


def status():
    ensure_research_dirs()
    ini = profiles_ini_path()
    pdir = profile_path()
    user_js = pdir / "user.js"

    print()
    print("HUDUT FIREFOX OSINT PROFILE STATUS")
    print("=" * 86)
    print(f"Firefox base     : {detect_firefox_base()}")
    print(f"profiles.ini     : {ini} {'[OK]' if ini.exists() else '[WARN]'}")
    print(f"Profile name     : {PROFILE_NAME}")
    print(f"Profile path     : {pdir} {'[OK]' if pdir.exists() else '[WARN]'}")
    print(f"user.js          : {user_js} {'[OK]' if user_js.exists() else '[WARN]'}")

    if ini.exists():
        text = ini.read_text(encoding="utf-8", errors="ignore")
        print(f"profiles.ini ref : {'[OK]' if PROFILE_NAME in text else '[WARN]'}")

    if user_js.exists():
        text = user_js.read_text(encoding="utf-8", errors="ignore")
        print(f"Hudut block      : {'[OK]' if MARKER_START in text and MARKER_END in text else '[WARN]'}")
        checks = {
            "Proxy direct": 'user_pref("network.proxy.type", 0);',
            "Password save off": 'user_pref("signon.rememberSignons", false);',
            "WebRTC off": 'user_pref("media.peerconnection.enabled", false);',
            "HTTPS-only": 'user_pref("dom.security.https_only_mode", true);',
            "Telemetry off": 'user_pref("toolkit.telemetry.enabled", false);',
        }
        for label, needle in checks.items():
            print(f"{label:<18}: {'[OK]' if needle in text else '[WARN]'}")

    print()
    print("Not:")
    print("- Bu profil Tor değildir.")
    print("- Açık web OSINT için kişisel Firefox profilinden ayrılmıştır.")
    print("- Kişisel hesaplara giriş yapılmamalıdır.")
    print("=" * 86)
    print()


def launch():
    prepare()

    firefox = shutil.which("firefox")
    if not firefox:
        print("[ERROR] firefox komutu bulunamadı.")
        sys.exit(1)

    print("[HUDUT] Firefox OSINT profili açılıyor...")
    print("[INFO] Kişisel Firefox profilinden ayrı profil kullanılacak.")
    print(f"[INFO] Komut: firefox --new-instance --profile {profile_path()}")
    subprocess.Popen([firefox, "--new-instance", "--profile", str(profile_path())])


def report():
    ensure_research_dirs()
    reports = research_paths()["reports"]
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out = reports / f"firefox-osint-status-{now}.md"

    ini = profiles_ini_path()
    pdir = profile_path()
    user_js = pdir / "user.js"

    out.write_text(f"""# Hudut Firefox OSINT Profile Report

Date: {now}

## Status

- Firefox base: `{detect_firefox_base()}`
- profiles.ini: `{ini}` {"OK" if ini.exists() else "WARN"}
- Profile name: `{PROFILE_NAME}`
- Profile path: `{pdir}` {"OK" if pdir.exists() else "WARN"}
- user.js: `{user_js}` {"OK" if user_js.exists() else "WARN"}

## Notes

This profile is for open web OSINT research.

It is not Tor Browser.
It is not an anonymity guarantee.
It separates research browsing from the user's personal Firefox profile.

## Rules

- Do not login to personal accounts.
- Do not save passwords.
- Do not import browser data.
- Do not mix personal browsing and OSINT research.
""", encoding="utf-8")

    print(f"[OK] Firefox OSINT raporu oluşturuldu: {out}")


def help_text():
    print("""Hudut Firefox OSINT Manager

Komutlar:
  prepare   Firefox OSINT profilini hazırla
  status    Profil durumunu göster
  launch    Firefox OSINT profilini aç
  report    Durum raporu oluştur

Örnek:
  python3 apps/firefox/hudut_firefox_osint.py prepare
  python3 apps/firefox/hudut_firefox_osint.py launch
""")


def main():
    if len(sys.argv) < 2:
        help_text()
        return

    cmd = sys.argv[1]

    if cmd == "prepare":
        prepare()
    elif cmd == "status":
        status()
    elif cmd == "launch":
        launch()
    elif cmd == "report":
        report()
    else:
        help_text()
        sys.exit(1)


if __name__ == "__main__":
    main()
