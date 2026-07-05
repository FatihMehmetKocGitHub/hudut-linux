#!/usr/bin/env python3
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox


BASE_DIR = os.path.expanduser("~/hudut-linux")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
RESEARCH_DIR = os.path.join(BASE_DIR, "research")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

LINKEDIN_URL = "https://www.linkedin.com/in/fatihmehmetkoc/"
INSTAGRAM_URL = "https://www.instagram.com/fatihmehmet_koc/"
GITHUB_URL = "https://github.com/FatihMehmetKocGitHub/hudut-linux"

WINDOW_TITLE = "Hudut Linux Welcome Center"

PROJECT_TEXT = (
    "Merhaba, ben Fatih Mehmet Koç.\n\n"
    "Hudut Linux; etik güvenlik araştırmacıları, OSINT analistleri ve siber "
    "istihbarat çalışmaları için geliştirilen Xubuntu tabanlı bir araştırma "
    "ve raporlama ortamıdır.\n\n"
    "Projenin amacı; açık kaynaklardan elde edilen bilgiyi yasal sınırlar içinde "
    "toplamak, doğrulamak, analiz etmek ve anlaşılır raporlara dönüştürmektir.\n\n"
    "Hudut Linux; kamu yararına farkındalık oluşturmak, tehditleri daha erken "
    "anlamak, dijital izleri düzenli incelemek ve elde edilen bulguları sorumlu "
    "şekilde değerlendirmek için hazırlanmıştır.\n\n"
    "Bu sistem saldırı aracı değildir. Yetkisiz erişim, istismar veya zarar verme "
    "amacı taşımaz. Temel prensip; etik, hukuka uygun ve raporlanabilir araştırmadır."
)


def run_command(command):
    try:
        subprocess.Popen(command)
    except Exception as error:
        messagebox.showerror("Hudut Linux", f"Komut çalıştırılamadı:\n{error}")


def open_url(url):
    run_command(["xdg-open", url])


def open_path(path):
    if os.path.exists(path):
        run_command(["xdg-open", path])
    else:
        messagebox.showwarning("Hudut Linux", f"Yol bulunamadı:\n{path}")


def show_about():
    messagebox.showinfo(
        "Hudut Linux Nedir?",
        "Hudut Linux; yasal OSINT, CTI ve GEOINT çalışmaları için geliştirilen "
        "Xubuntu tabanlı güvenli bir araştırma ve raporlama ortamıdır."
    )


def show_ethics():
    messagebox.showwarning(
        "Etik Kullanım",
        "Hudut Linux saldırı sistemi değildir.\n\n"
        "Bu sistem; izinsiz erişim, istismar, doxxing, kişisel veri yayma "
        "veya yetkisiz tarama amacıyla kullanılmaz.\n\n"
        "Temel yaklaşım: yasal araştırma, etik analiz ve raporlanabilir çalışma."
    )


def force_maximize(window):
    window.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(f"{screen_width}x{screen_height}+0+0")

    try:
        window.state("zoomed")
    except tk.TclError:
        pass

    try:
        window.attributes("-zoomed", True)
    except tk.TclError:
        pass

    try:
        subprocess.Popen([
            "wmctrl",
            "-r",
            WINDOW_TITLE,
            "-b",
            "add,maximized_vert,maximized_horz"
        ])
    except Exception:
        pass


root = tk.Tk()
root.title(WINDOW_TITLE)
root.configure(bg="#070b12")

force_maximize(root)
root.after(300, lambda: force_maximize(root))
root.after(900, lambda: force_maximize(root))
root.after(1500, lambda: force_maximize(root))

root.minsize(1100, 650)

style = ttk.Style()
style.theme_use("clam")

style.configure("Main.TFrame", background="#070b12")
style.configure("Card.TFrame", background="#111827")
style.configure("Side.TFrame", background="#0b1220")

style.configure(
    "Title.TLabel",
    background="#070b12",
    foreground="#ffffff",
    font=("Sans", 38, "bold")
)

style.configure(
    "Subtitle.TLabel",
    background="#070b12",
    foreground="#b8c7d9",
    font=("Sans", 15)
)

style.configure(
    "CardTitle.TLabel",
    background="#111827",
    foreground="#ffffff",
    font=("Sans", 20, "bold")
)

style.configure(
    "CardText.TLabel",
    background="#111827",
    foreground="#dbeafe",
    font=("Sans", 14),
    padding=10
)

style.configure(
    "SideTitle.TLabel",
    background="#0b1220",
    foreground="#ffffff",
    font=("Sans", 18, "bold")
)

style.configure(
    "SideText.TLabel",
    background="#0b1220",
    foreground="#dbeafe",
    font=("Sans", 11)
)

style.configure(
    "Hudut.TButton",
    font=("Sans", 11, "bold"),
    padding=10
)

style.configure(
    "Contact.TButton",
    font=("Sans", 12, "bold"),
    padding=12
)


main = ttk.Frame(root, padding=28, style="Main.TFrame")
main.pack(fill="both", expand=True)

header = ttk.Frame(main, style="Main.TFrame")
header.pack(fill="x", pady=(0, 18))

title = ttk.Label(
    header,
    text="HUDUT LINUX",
    style="Title.TLabel"
)
title.pack(anchor="w")

subtitle = ttk.Label(
    header,
    text="Yasal OSINT, CTI ve GEOINT araştırmaları için güvenli çalışma ortamı",
    style="Subtitle.TLabel"
)
subtitle.pack(anchor="w", pady=(4, 0))


content = ttk.Frame(main, style="Main.TFrame")
content.pack(fill="both", expand=True)

content.columnconfigure(0, weight=4)
content.columnconfigure(1, weight=1)
content.rowconfigure(0, weight=1)

left = ttk.Frame(content, style="Main.TFrame")
left.grid(row=0, column=0, sticky="nsew", padx=(0, 22))

right = ttk.Frame(content, padding=18, style="Side.TFrame")
right.grid(row=0, column=1, sticky="nsew")


intro_card = ttk.Frame(left, padding=24, style="Card.TFrame")
intro_card.pack(fill="both", expand=True)

intro_title = ttk.Label(
    intro_card,
    text="Proje Tanıtımı",
    style="CardTitle.TLabel"
)
intro_title.pack(anchor="w", pady=(0, 16))

intro_text = ttk.Label(
    intro_card,
    text=PROJECT_TEXT,
    style="CardText.TLabel",
    wraplength=1050,
    justify="left"
)
intro_text.pack(anchor="nw", fill="x")


contact_title = ttk.Label(
    right,
    text="İletişim",
    style="SideTitle.TLabel"
)
contact_title.pack(anchor="w", pady=(0, 12))

linkedin_label = ttk.Label(right, text="LinkedIn", style="SideText.TLabel")
linkedin_label.pack(anchor="w")

linkedin_button = ttk.Button(
    right,
    text="Fatih Mehmet Koç",
    command=lambda: open_url(LINKEDIN_URL),
    style="Contact.TButton"
)
linkedin_button.pack(fill="x", pady=(4, 4))

linkedin_url_label = ttk.Label(
    right,
    text="linkedin.com/in/fatihmehmetkoc",
    style="SideText.TLabel"
)
linkedin_url_label.pack(anchor="w", pady=(0, 14))


instagram_label = ttk.Label(right, text="Instagram", style="SideText.TLabel")
instagram_label.pack(anchor="w")

instagram_button = ttk.Button(
    right,
    text="fatihmehmet_koc",
    command=lambda: open_url(INSTAGRAM_URL),
    style="Contact.TButton"
)
instagram_button.pack(fill="x", pady=(4, 4))

instagram_url_label = ttk.Label(
    right,
    text="instagram.com/fatihmehmet_koc",
    style="SideText.TLabel"
)
instagram_url_label.pack(anchor="w", pady=(0, 14))


github_label = ttk.Label(right, text="GitHub", style="SideText.TLabel")
github_label.pack(anchor="w")

github_button = ttk.Button(
    right,
    text="Hudut Linux Açık Repo",
    command=lambda: open_url(GITHUB_URL),
    style="Contact.TButton"
)
github_button.pack(fill="x", pady=(4, 4))

github_url_label = ttk.Label(
    right,
    text="github.com/FatihMehmetKocGitHub/hudut-linux",
    style="SideText.TLabel"
)
github_url_label.pack(anchor="w", pady=(0, 22))


quick_title = ttk.Label(
    right,
    text="Hızlı Erişim",
    style="SideTitle.TLabel"
)
quick_title.pack(anchor="w", pady=(0, 12))

quick_buttons = [
    ("Hudut Linux Nedir?", show_about),
    ("Etik Kullanım", show_ethics),
    ("Dokümantasyon", lambda: open_path(DOCS_DIR)),
    ("Research", lambda: open_path(RESEARCH_DIR)),
    ("Reports", lambda: open_path(REPORTS_DIR)),
    ("Templates", lambda: open_path(TEMPLATES_DIR)),
    ("Proje Klasörü", lambda: open_path(BASE_DIR)),
]

for text, command in quick_buttons:
    button = ttk.Button(
        right,
        text=text,
        command=command,
        style="Hudut.TButton"
    )
    button.pack(fill="x", pady=4)


root.mainloop()
