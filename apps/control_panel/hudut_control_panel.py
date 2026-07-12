#!/usr/bin/env python3
import json
import shutil
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

ROOT = Path.home() / "hudut-linux"

APPS = {
    "shield": ROOT / "apps" / "shield" / "hudut_shield.py",
    "proxy": ROOT / "apps" / "proxy" / "hudut_proxy.py",
    "lxc_manager": ROOT / "apps" / "lxc_manager" / "hudut_lxc_manager.py",
    "tool_installer": ROOT / "apps" / "tool_installer" / "hudut_tool_installer.py",
}

STATUS_SCRIPT = ROOT / "lxc" / "scripts" / "06_container_status.sh"
VERSION_FILE = ROOT / "version.json"

def run_cmd(cmd: str, timeout: int = 120) -> str:
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=str(ROOT),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
        out = result.stdout.strip()
        return out if out else "[OK] Komut tamamlandı."
    except subprocess.TimeoutExpired:
        return "[ERROR] Komut zaman aşımına uğradı."
    except Exception as exc:
        return f"[ERROR] {exc}"

def run_in_terminal(cmd: str) -> None:
    terminal = shutil.which("xfce4-terminal") or shutil.which("x-terminal-emulator")
    terminal_cmd = f'cd "{ROOT}" && {cmd}; echo; read -p "Kapatmak için Enter..."'

    try:
        if terminal and "xfce4-terminal" in terminal:
            subprocess.Popen([terminal, "--command", f"bash -lc '{terminal_cmd}'"])
        elif terminal:
            subprocess.Popen([terminal, "-e", "bash", "-lc", terminal_cmd])
        else:
            messagebox.showwarning(
                "Terminal bulunamadı",
                "xfce4-terminal veya x-terminal-emulator bulunamadı.",
            )
    except Exception as exc:
        messagebox.showerror("Terminal açılamadı", str(exc))

def open_path(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.Popen(["xdg-open", str(path)])

def open_python_gui(path: Path) -> None:
    if not path.exists():
        messagebox.showerror("Dosya yok", f"Bulunamadı: {path}")
        return
    subprocess.Popen(["python3", str(path)], cwd=str(ROOT))

class HudutControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hudut Control Panel")
        self.geometry("1080x700")
        self.minsize(980, 620)

        self._build_ui()
        self.show_overview()

    def _build_ui(self):
        header = tk.Label(
            self,
            text="HUDUT CONTROL PANEL",
            font=("Sans", 20, "bold"),
            pady=10,
        )
        header.pack(fill="x")

        subtitle = tk.Label(
            self,
            text="Hudut Linux V1 merkezi yönetim paneli",
            font=("Sans", 10),
        )
        subtitle.pack(fill="x")

        main = tk.Frame(self)
        main.pack(fill="both", expand=True, padx=12, pady=12)

        left = tk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 10))

        right = tk.Frame(main)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="Ana Modüller", font=("Sans", 11, "bold")).pack(anchor="w")

        tk.Button(left, text="Hudut Shield Aç", command=self.open_shield).pack(fill="x", pady=2)
        tk.Button(left, text="Hudut LXC Manager Aç", command=self.open_lxc_manager).pack(fill="x", pady=2)
        tk.Button(left, text="Hudut Tool Installer Aç", command=self.open_tool_installer).pack(fill="x", pady=2)

        tk.Label(left, text="Hızlı Kontroller", font=("Sans", 11, "bold")).pack(anchor="w", pady=(14, 4))

        tk.Button(left, text="LXC Durumu Göster", command=self.show_lxc_status).pack(fill="x", pady=2)
        tk.Button(left, text="LXC Status Raporu Üret", command=self.generate_lxc_report).pack(fill="x", pady=2)
        tk.Button(left, text="Proxy Özeti", command=self.proxy_summary).pack(fill="x", pady=2)
        tk.Button(left, text="Tor Servis Durumu", command=self.tor_status).pack(fill="x", pady=2)
        tk.Button(left, text="Git Status", command=self.git_status).pack(fill="x", pady=2)
        tk.Button(left, text="Version Bilgisi", command=self.version_info).pack(fill="x", pady=2)

        tk.Label(left, text="Klasörler", font=("Sans", 11, "bold")).pack(anchor="w", pady=(14, 4))

        tk.Button(left, text="Proje Klasörünü Aç", command=lambda: open_path(ROOT)).pack(fill="x", pady=2)
        tk.Button(left, text="Docs Klasörünü Aç", command=lambda: open_path(ROOT / "docs")).pack(fill="x", pady=2)
        tk.Button(left, text="Reports Klasörünü Aç", command=lambda: open_path(ROOT / "reports")).pack(fill="x", pady=2)
        tk.Button(left, text="Intelligence Klasörünü Aç", command=lambda: open_path(ROOT / "intelligence")).pack(fill="x", pady=2)
        tk.Button(left, text="Tools Klasörünü Aç", command=lambda: open_path(ROOT / "tools")).pack(fill="x", pady=2)

        tk.Label(left, text="Tarayıcı / Araştırma", font=("Sans", 11, "bold")).pack(anchor="w", pady=(14, 4))

        tk.Button(left, text="Firefox OSINT Aç", command=self.open_firefox_osint).pack(fill="x", pady=2)
        tk.Button(left, text="Tor Research Klasörlerini Hazırla", command=self.tor_research_prepare).pack(fill="x", pady=2)

        tk.Button(left, text="Yenile / Genel Özet", command=self.show_overview).pack(fill="x", pady=(18, 2))
        tk.Button(left, text="Çıkış", command=self.destroy).pack(fill="x", pady=2)

        tk.Label(right, text="Çıktı", font=("Sans", 11, "bold")).pack(anchor="w")

        self.output = tk.Text(right, wrap="none")
        self.output.pack(fill="both", expand=True)

        bottom = tk.Label(
            self,
            text="Hudut Linux V1: yasal OSINT, CTI, TECHINT, GEOINT ve güvenli araştırma workstation katmanı.",
            anchor="w",
            padx=12,
            pady=6,
        )
        bottom.pack(fill="x")

    def set_output(self, text: str):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def append_output(self, text: str):
        self.output.insert(tk.END, "\n" + text + "\n")
        self.output.see(tk.END)

    def show_overview(self):
        parts = []

        parts.append("HUDUT CONTROL PANEL GENEL ÖZET")
        parts.append("=" * 80)
        parts.append("")
        parts.append("## Git")
        parts.append(run_cmd("git status --short && git branch --show-current"))
        parts.append("")
        parts.append("## LXC")
        parts.append(run_cmd("lxc list"))
        parts.append("")
        parts.append("## UFW")
        parts.append(run_cmd("sudo ufw status verbose || true"))
        parts.append("")
        parts.append("## Version")
        parts.append(self._read_version())

        self.set_output("\n".join(parts))

    def _read_version(self) -> str:
        if not VERSION_FILE.exists():
            return "[WARN] version.json bulunamadı."

        try:
            data = json.loads(VERSION_FILE.read_text(encoding="utf-8"))
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as exc:
            return f"[ERROR] version.json okunamadı: {exc}"

    def open_shield(self):
        path = APPS["shield"]
        if not path.exists():
            messagebox.showerror("Dosya yok", f"Bulunamadı: {path}")
            return
        run_in_terminal("python3 apps/shield/hudut_shield.py menu")

    def open_lxc_manager(self):
        open_python_gui(APPS["lxc_manager"])

    def open_tool_installer(self):
        open_python_gui(APPS["tool_installer"])

    def show_lxc_status(self):
        self.set_output(run_cmd("lxc list"))

    def generate_lxc_report(self):
        if not STATUS_SCRIPT.exists():
            messagebox.showerror("Script yok", f"Bulunamadı: {STATUS_SCRIPT}")
            return
        run_in_terminal("bash lxc/scripts/06_container_status.sh")
        self.append_output("[HUDUT] LXC status raporu terminalde üretilecek.")

    def proxy_summary(self):
        path = APPS["proxy"]
        if not path.exists():
            self.set_output(f"[ERROR] Proxy Manager bulunamadı: {path}")
            return
        self.set_output(run_cmd("python3 apps/proxy/hudut_proxy.py summary"))

    def tor_status(self):
        self.set_output(run_cmd("systemctl status tor --no-pager 2>/dev/null || service tor status 2>/dev/null || echo 'Tor servisi bulunamadı veya aktif değil.'"))

    def git_status(self):
        self.set_output(run_cmd("git status && echo && git log --oneline -5"))

    def version_info(self):
        self.set_output(self._read_version())

    def open_firefox_osint(self):
        cmd = "firefox -P hudut-osint --no-remote 2>/dev/null || firefox 2>/dev/null || echo 'Firefox açılamadı.'"
        run_in_terminal(cmd)
        self.append_output("[HUDUT] Firefox OSINT açma komutu terminalde çalıştırıldı.")

    def tor_research_prepare(self):
        path = APPS["shield"]
        if path.exists():
            run_in_terminal("python3 apps/shield/hudut_shield.py menu")
            self.append_output("[INFO] Shield menüsünden Tor Research klasör hazırlama seçeneğini kullan.")
        else:
            tor_dir = ROOT / "reports" / "tor-research"
            tor_dir.mkdir(parents=True, exist_ok=True)
            open_path(tor_dir)
            self.append_output(f"[HUDUT] Tor research klasörü açıldı: {tor_dir}")

if __name__ == "__main__":
    app = HudutControlPanel()
    app.mainloop()
