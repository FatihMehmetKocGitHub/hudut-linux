#!/usr/bin/env python3
import subprocess
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

ROOT = Path.home() / "hudut-linux"
INSTALLER_DIR = ROOT / "tools" / "installers"

TOOLS = [
    {
        "title": "OSINT Tools",
        "container": "hudut-osint",
        "script": "install_osint_tools.sh",
        "desc": "Genel açık kaynak araştırma araçları",
    },
    {
        "title": "SOCMINT Tools",
        "container": "hudut-socmint",
        "script": "install_socmint_tools.sh",
        "desc": "Sosyal medya / platform araştırma yardımcıları",
    },
    {
        "title": "CTI Tools",
        "container": "hudut-cti",
        "script": "install_cti_tools.sh",
        "desc": "Siber tehdit istihbaratı ve IOC çalışma araçları",
    },
    {
        "title": "TECHINT Tools",
        "container": "hudut-techint",
        "script": "install_techint_tools.sh",
        "desc": "DNS / IP / ASN / ağ teknik analiz araçları",
    },
    {
        "title": "GEOINT Tools",
        "container": "hudut-geoint",
        "script": "install_geoint_tools.sh",
        "desc": "GEOINT / IMINT hazırlık araçları",
    },
    {
        "title": "DEV Tools",
        "container": "hudut-dev",
        "script": "install_dev_tools.sh",
        "desc": "Python geliştirme ve kalite araçları",
    },
    {
        "title": "SANDBOX Tools",
        "container": "hudut-sandbox",
        "script": "install_sandbox_tools.sh",
        "desc": "İzole deneme / test ortamı araçları",
    },
]

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
                "xfce4-terminal veya x-terminal-emulator bulunamadı. Komutu ana terminalde çalıştır.",
            )
    except Exception as exc:
        messagebox.showerror("Terminal açılamadı", str(exc))

class HudutToolInstaller(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hudut Tool Installer")
        self.geometry("1050x680")
        self.minsize(950, 600)

        self.selected_index = None

        self._build_ui()
        self.refresh_status()

    def _build_ui(self):
        header = tk.Label(
            self,
            text="HUDUT TOOL INSTALLER",
            font=("Sans", 18, "bold"),
            pady=10,
        )
        header.pack(fill="x")

        subtitle = tk.Label(
            self,
            text="Hudut Linux V1 container bazlı yasal OSINT / CTI / TECHINT / GEOINT araç kurulum merkezi",
            font=("Sans", 10),
        )
        subtitle.pack(fill="x")

        main = tk.Frame(self)
        main.pack(fill="both", expand=True, padx=12, pady=12)

        left = tk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left, text="Tool Profilleri", font=("Sans", 11, "bold")).pack(anchor="w")

        self.listbox = tk.Listbox(left, width=55, height=18)
        self.listbox.pack(fill="y", pady=(5, 8))
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        for item in TOOLS:
            self.listbox.insert(
                tk.END,
                f"{item['title']:<16} → {item['container']:<15} | {item['desc']}"
            )

        tk.Button(left, text="Seçili Profili Kur", command=self.install_selected).pack(fill="x", pady=2)
        tk.Button(left, text="Seçili Scripti Göster", command=self.show_selected_script).pack(fill="x", pady=2)
        tk.Button(left, text="Container Durumunu Yenile", command=self.refresh_status).pack(fill="x", pady=2)
        tk.Button(left, text="Tüm Scriptleri Syntax Kontrol", command=self.syntax_check_all).pack(fill="x", pady=2)
        tk.Button(left, text="Installer Klasörünü Aç", command=self.open_installer_dir).pack(fill="x", pady=2)
        tk.Button(left, text="Çıkış", command=self.destroy).pack(fill="x", pady=(14, 2))

        note = tk.Label(
            left,
            text="Not: Kurulumlar terminalde çalışır.\nSudo gerekmez; araçlar LXC container içine kurulur.",
            justify="left",
            wraplength=380,
            pady=12,
        )
        note.pack(fill="x")

        right = tk.Frame(main)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Çıktı", font=("Sans", 11, "bold")).pack(anchor="w")

        self.output = tk.Text(right, wrap="none")
        self.output.pack(fill="both", expand=True)

        bottom = tk.Label(
            self,
            text="Güvenlik çizgisi: Bu araçlar yalnızca yasal araştırma, kendi lab ortamı ve izinli hedefler için kullanılmalıdır.",
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

    def on_select(self, _event=None):
        selection = self.listbox.curselection()
        if not selection:
            self.selected_index = None
            return
        self.selected_index = selection[0]
        item = TOOLS[self.selected_index]
        script = INSTALLER_DIR / item["script"]

        text = f"""Seçili profil: {item['title']}
Container: {item['container']}
Script: {script}
Açıklama: {item['desc']}

Kurulum terminalde çalıştırılacak.
"""
        self.set_output(text)

    def get_selected(self):
        if self.selected_index is None:
            messagebox.showwarning("Seçim yok", "Önce bir tool profili seç.")
            return None
        return TOOLS[self.selected_index]

    def install_selected(self):
        item = self.get_selected()
        if not item:
            return

        script = INSTALLER_DIR / item["script"]
        if not script.exists():
            messagebox.showerror("Script yok", f"Bulunamadı: {script}")
            return

        msg = (
            f"{item['title']} kurulacak.\n\n"
            f"Container: {item['container']}\n"
            f"Script: {script.name}\n\n"
            "Devam edilsin mi?"
        )
        if not messagebox.askyesno("Kurulum onayı", msg):
            return

        run_in_terminal(f"bash tools/installers/{script.name}")
        self.append_output(f"[HUDUT] Terminalde başlatıldı: {script.name}")

    def show_selected_script(self):
        item = self.get_selected()
        if not item:
            return

        script = INSTALLER_DIR / item["script"]
        if not script.exists():
            self.set_output(f"[ERROR] Script bulunamadı: {script}")
            return

        self.set_output(script.read_text(encoding="utf-8"))

    def refresh_status(self):
        self.set_output(run_cmd("lxc list"))

    def syntax_check_all(self):
        cmd = "for f in tools/installers/*.sh; do echo ===== $f =====; bash -n \"$f\" && echo OK; done"
        self.set_output(run_cmd(cmd))

    def open_installer_dir(self):
        subprocess.Popen(["xdg-open", str(INSTALLER_DIR)])

if __name__ == "__main__":
    app = HudutToolInstaller()
    app.mainloop()
