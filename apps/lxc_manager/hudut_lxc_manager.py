#!/usr/bin/env python3
import subprocess
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

ROOT = Path.home() / "hudut-linux"
REPORT_DIR = ROOT / "reports" / "lxc"
STATUS_SCRIPT = ROOT / "lxc" / "scripts" / "06_container_status.sh"

CONTAINERS = [
    "hudut-osint",
    "hudut-socmint",
    "hudut-cti",
    "hudut-techint",
    "hudut-geoint",
    "hudut-dev",
    "hudut-sandbox",
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
        output = result.stdout.strip()
        if not output:
            output = "[OK] Komut tamamlandı."
        return output
    except subprocess.TimeoutExpired:
        return "[ERROR] Komut zaman aşımına uğradı."
    except Exception as exc:
        return f"[ERROR] {exc}"

def run_in_terminal(cmd: str) -> None:
    terminal = shutil.which("x-terminal-emulator")
    if not terminal:
        terminal = shutil.which("xfce4-terminal")

    terminal_cmd = f'cd "{ROOT}" && {cmd}; echo; read -p "Kapatmak için Enter..."'

    try:
        if terminal and "xfce4-terminal" in terminal:
            subprocess.Popen([terminal, "--command", f"bash -lc '{terminal_cmd}'"])
        elif terminal:
            subprocess.Popen([terminal, "-e", "bash", "-lc", terminal_cmd])
        else:
            messagebox.showwarning(
                "Terminal bulunamadı",
                "x-terminal-emulator veya xfce4-terminal bulunamadı. Komutu ana terminalde çalıştır.",
            )
    except Exception as exc:
        messagebox.showerror("Terminal açılamadı", str(exc))

class HudutLXCManager(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hudut LXC Manager")
        self.geometry("980x650")
        self.minsize(900, 560)

        self.selected_name = tk.StringVar(value="")

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        header = tk.Label(
            self,
            text="HUDUT LXC MANAGER",
            font=("Sans", 18, "bold"),
            pady=10,
        )
        header.pack(fill="x")

        subtitle = tk.Label(
            self,
            text="Hudut Linux V1 container durum, başlat/durdur, snapshot ve rapor yönetimi",
            font=("Sans", 10),
        )
        subtitle.pack(fill="x")

        main = tk.Frame(self)
        main.pack(fill="both", expand=True, padx=12, pady=12)

        left = tk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left, text="Containerlar", font=("Sans", 11, "bold")).pack(anchor="w")

        self.listbox = tk.Listbox(left, width=42, height=20)
        self.listbox.pack(fill="y", expand=False, pady=(5, 8))
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        selected_frame = tk.Frame(left)
        selected_frame.pack(fill="x", pady=(0, 8))

        tk.Label(selected_frame, text="Seçili:").pack(side="left")
        tk.Label(selected_frame, textvariable=self.selected_name, font=("Sans", 10, "bold")).pack(side="left", padx=5)

        btn_frame = tk.Frame(left)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="Yenile", command=self.refresh).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="Seçileni Başlat", command=self.start_selected).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="Seçileni Durdur", command=self.stop_selected).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="Seçileni Restart", command=self.restart_selected).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="Restore Komutunu Göster", command=self.show_restore_command).pack(fill="x", pady=2)

        tk.Label(left, text="Toplu İşlemler", font=("Sans", 11, "bold")).pack(anchor="w", pady=(14, 4))
        tk.Button(left, text="Tümünü Başlat", command=self.start_all).pack(fill="x", pady=2)
        tk.Button(left, text="Tümünü Durdur", command=self.stop_all).pack(fill="x", pady=2)
        tk.Button(left, text="Snapshotları Göster", command=self.show_snapshots).pack(fill="x", pady=2)
        tk.Button(left, text="LXC Status Raporu Üret", command=self.generate_report).pack(fill="x", pady=2)
        tk.Button(left, text="Rapor Klasörünü Aç", command=self.open_reports).pack(fill="x", pady=2)
        tk.Button(left, text="Çıkış", command=self.destroy).pack(fill="x", pady=(14, 2))

        right = tk.Frame(main)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Çıktı", font=("Sans", 11, "bold")).pack(anchor="w")

        self.output = tk.Text(right, wrap="none")
        self.output.pack(fill="both", expand=True)

        bottom = tk.Label(
            self,
            text="Not: clean-base restore işlemi otomatik yapılmaz. Güvenlik için sadece komut gösterilir.",
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

    def get_selected_container(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Seçim yok", "Önce bir container seç.")
            return None

        line = self.listbox.get(selection[0])
        name = line.split()[0].strip()
        if name not in CONTAINERS:
            messagebox.showerror("Geçersiz seçim", "Container adı çözülemedi.")
            return None

        return name

    def on_select(self, _event=None):
        name = self.get_selected_container()
        if name:
            self.selected_name.set(name)

    def refresh(self):
        csv = run_cmd("lxc list -c ns4S --format csv")
        self.listbox.delete(0, tk.END)

        if csv.startswith("[ERROR]"):
            for c in CONTAINERS:
                self.listbox.insert(tk.END, c)
            self.set_output(csv)
            return

        for line in csv.splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 4:
                name, state, ipv4, snaps = parts[0], parts[1], parts[2], parts[3]
                if name in CONTAINERS:
                    display = f"{name:<15} {state:<8} {ipv4:<18} snapshots:{snaps}"
                    self.listbox.insert(tk.END, display)

        self.set_output(run_cmd("lxc list"))

    def start_selected(self):
        name = self.get_selected_container()
        if not name:
            return
        self.set_output(run_cmd(f"lxc start {name} || true && lxc list"))
        self.refresh()

    def stop_selected(self):
        name = self.get_selected_container()
        if not name:
            return
        if not messagebox.askyesno("Onay", f"{name} durdurulsun mu?"):
            return
        self.set_output(run_cmd(f"lxc stop {name} --force || true && lxc list"))
        self.refresh()

    def restart_selected(self):
        name = self.get_selected_container()
        if not name:
            return
        self.set_output(run_cmd(f"lxc restart {name} && lxc list"))
        self.refresh()

    def start_all(self):
        cmd = "for c in " + " ".join(CONTAINERS) + "; do lxc start \"$c\" 2>/dev/null || true; done; lxc list"
        self.set_output(run_cmd(cmd))
        self.refresh()

    def stop_all(self):
        if not messagebox.askyesno("Onay", "Tüm containerlar durdurulsun mu?"):
            return
        cmd = "for c in " + " ".join(CONTAINERS) + "; do lxc stop \"$c\" --force 2>/dev/null || true; done; lxc list"
        self.set_output(run_cmd(cmd))
        self.refresh()

    def show_snapshots(self):
        cmd = """
for c in hudut-osint hudut-socmint hudut-cti hudut-techint hudut-geoint hudut-dev hudut-sandbox; do
  echo "===== $c ====="
  lxc info "$c" | sed -n '/Snapshots:/,$p'
  echo
done
"""
        self.set_output(run_cmd(cmd))

    def show_restore_command(self):
        name = self.get_selected_container()
        if not name:
            return

        text = f"""
DİKKAT:
Bu işlem {name} containerını clean-base snapshotına geri döndürür.
Container içindeki sonradan yapılan değişiklikler kaybolabilir.

Manuel restore komutu:

lxc stop {name} --force
lxc restore {name} clean-base
lxc start {name}

Toplu restore önermiyorum. İnsanlık zaten yeterince yanlış butona bastı.
"""
        self.set_output(text)

    def generate_report(self):
        if not STATUS_SCRIPT.exists():
            messagebox.showerror("Script yok", f"Bulunamadı: {STATUS_SCRIPT}")
            return
        run_in_terminal("bash lxc/scripts/06_container_status.sh")
        self.append_output("LXC status raporu terminalde üretilecek. Sudo şifresi isterse gir.")

    def open_reports(self):
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.Popen(["xdg-open", str(REPORT_DIR)])

if __name__ == "__main__":
    app = HudutLXCManager()
    app.mainloop()
