"""
╔══════════════════════════════════════════════════════════════╗
║              AUGUSTUNA ADMIN HUB  v1.0                       ║
║      Gestão de Conteúdo do Website — Desktop App             ║
╚══════════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
import json
import os
import shutil
import subprocess
import uuid
from datetime import datetime
from PIL import Image
import sys

# ─── THEME ────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Brand colors
AZUL_PROFUNDO = "#0A1628"
AZUL_REAL = "#1B3A5C"
DOURADO = "#C9A84C"
GOLD_HOVER = "#D4B85E"
BG_DARK = "#111111"
BG_SIDEBAR = "#0D0D0D"
BG_CARD = "#1A1A1A"
FG_TEXT = "#E0E0E0"
FG_MUTED = "#888888"
SUCCESS = "#2E8B57"
DANGER = "#B22222"

# ─── PATHS (Standalone — pede o caminho ao utilizador) ──────────
APP_NAME = "AugustunaAdminHub"
CONFIG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), APP_NAME)
os.makedirs(CONFIG_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def _load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def _ask_repo_path():
    """Prompt user to select the website repo folder."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(
        "Augustuna Admin Hub",
        "Bem-vindo ao Admin Hub!\n\n"
        "Seleciona a pasta do repositório do website\n"
        "(a pasta que contém o index.html, data/, etc.)"
    )
    path = filedialog.askdirectory(title="Seleciona a pasta do repositório")
    root.destroy()
    if not path:
        messagebox.showerror("Erro", "Nenhuma pasta selecionada. A aplicação vai fechar.")
        raise SystemExit(1)
    return path

def _get_repo_dir():
    cfg = _load_config()
    repo = cfg.get("repo_dir", "")
    # Validate the stored path still exists and contains data/
    if repo and os.path.isdir(repo) and os.path.isdir(os.path.join(repo, "data")):
        return repo
    # Ask the user
    repo = _ask_repo_path()
    cfg["repo_dir"] = repo
    _save_config(cfg)
    return repo

REPO_DIR = _get_repo_dir()
DATA_DIR = os.path.join(REPO_DIR, "data")
ASSETS_IMG = os.path.join(REPO_DIR, "assets", "img")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ASSETS_IMG, exist_ok=True)

# ─── DATA HELPERS ─────────────────────────────────────────────
def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return [] if filename in ["noticias.json", "loja.json"] else {}

def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def copy_image(src_path):
    """Copy an image to assets/img/ and return the relative path."""
    if not src_path or not os.path.exists(src_path):
        return ""
    basename = os.path.basename(src_path)
    # Avoid name collisions
    name, ext = os.path.splitext(basename)
    dest = os.path.join(ASSETS_IMG, basename)
    if os.path.exists(dest):
        basename = f"{name}_{uuid.uuid4().hex[:6]}{ext}"
        dest = os.path.join(ASSETS_IMG, basename)
    shutil.copy2(src_path, dest)
    return f"assets/img/{basename}"

def gen_id():
    return uuid.uuid4().hex[:8]


# ═══════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════
class AdminHub(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Augustuna Admin Hub")
        self.geometry("1200x750")
        self.minsize(1000, 600)
        self.configure(fg_color=BG_DARK)

        # Try to set icon
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        icon_path = os.path.join(base_path, "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except:
                pass

        self._build_ui()
        self.show_module("noticias")

    # ── Layout ────────────────────────────────────────────────
    def _build_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=BG_SIDEBAR, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand header
        brand = ctk.CTkLabel(self.sidebar, text="AUGUSTUNA", font=("Courier New", 18, "bold"),
                             text_color=DOURADO)
        brand.pack(pady=(25, 2))
        sub = ctk.CTkLabel(self.sidebar, text="Admin Hub", font=("Courier New", 11),
                           text_color=FG_MUTED)
        sub.pack(pady=(0, 30))

        # Nav buttons
        self.nav_buttons = {}
        modules = [
            ("📰", "Notícias", "noticias"),
            ("👥", "Membros", "membros"),
            ("🎉", "Eventos", "eventos"),
            ("🎵", "Atuações", "atuacoes"),
            ("🛍️", "Loja", "loja"),
            ("📞", "Contactos", "contactos"),
        ]
        for icon, label, key in modules:
            btn = ctk.CTkButton(
                self.sidebar, text=f"  {icon}  {label}", anchor="w",
                font=("Courier New", 13), height=42,
                fg_color="transparent", hover_color=AZUL_REAL,
                text_color=FG_TEXT, corner_radius=6,
                command=lambda k=key: self.show_module(k)
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[key] = btn

        # Spacer
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(expand=True)

        # Status label
        self.status_label = ctk.CTkLabel(self.sidebar, text="Pronto", font=("Courier New", 10),
                                         text_color=FG_MUTED, wraplength=190)
        self.status_label.pack(pady=(0, 5), padx=12)

        # Progress bar
        self.progress = ctk.CTkProgressBar(self.sidebar, width=190, height=6,
                                            progress_color=DOURADO, fg_color=BG_CARD)
        self.progress.pack(pady=(0, 10), padx=12)
        self.progress.set(0)

        # Push button
        self.push_btn = ctk.CTkButton(
            self.sidebar, text="⬆  GUARDAR E ATUALIZAR", height=40,
            font=("Courier New", 11, "bold"),
            fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
            corner_radius=8, command=self.git_push
        )
        self.push_btn.pack(fill="x", padx=12, pady=(0, 20))

        # Main content area
        self.content = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

    # ── Module switching ──────────────────────────────────────
    def show_module(self, key):
        # Highlight sidebar
        for k, btn in self.nav_buttons.items():
            btn.configure(fg_color=AZUL_REAL if k == key else "transparent")

        # Clear content
        for w in self.content.winfo_children():
            w.destroy()

        # Load module
        if key == "noticias":
            NoticiasModule(self.content)
        elif key == "membros":
            MembrosModule(self.content)
        elif key == "eventos":
            EventosModule(self.content)
        elif key == "atuacoes":
            AtuacoesModule(self.content)
        elif key == "loja":
            LojaModule(self.content)
        elif key == "contactos":
            ContactosModule(self.content)

    # ── Git Push ──────────────────────────────────────────────
    def git_push(self):
        self.push_btn.configure(state="disabled", text="A processar...")
        self.status_label.configure(text="A preparar ficheiros...", text_color=DOURADO)
        self.progress.set(0.1)
        self.update()

        try:
            # Stage
            self.status_label.configure(text="git add .")
            self.progress.set(0.3)
            self.update()
            subprocess.run(["git", "add", "."], cwd=REPO_DIR, check=True,
                         capture_output=True, text=True)

            # Commit
            self.status_label.configure(text="git commit...")
            self.progress.set(0.5)
            self.update()
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            subprocess.run(
                ["git", "commit", "-m", f"Update via Admin Hub — {timestamp}"],
                cwd=REPO_DIR, check=True, capture_output=True, text=True
            )

            # Push
            self.status_label.configure(text="git push origin main...")
            self.progress.set(0.7)
            self.update()
            subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, check=True,
                         capture_output=True, text=True)

            self.progress.set(1.0)
            self.status_label.configure(text="✓ Website atualizado!", text_color=SUCCESS)
        except subprocess.CalledProcessError as e:
            err = e.stderr or str(e)
            if "nothing to commit" in err:
                self.status_label.configure(text="Nada para atualizar.", text_color=FG_MUTED)
                self.progress.set(1.0)
            else:
                self.status_label.configure(text=f"Erro: {err[:80]}", text_color=DANGER)
                self.progress.set(0)
                messagebox.showerror("Erro Git", err)
        finally:
            self.push_btn.configure(state="normal", text="⬆  GUARDAR E ATUALIZAR")


# ═══════════════════════════════════════════════════════════════
#  MODULE: NOTÍCIAS
# ═══════════════════════════════════════════════════════════════
CATEGORIAS = ["destaque", "recrutamento", "festival", "cultura", "premio", "geral"]

class NoticiasModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("noticias.json")
        if not isinstance(self.data, list):
            self.data = []
        self._build()

    def _build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header, text="📰  Gestão de Notícias", font=("Courier New", 20, "bold"),
                     text_color=DOURADO).pack(side="left")
        ctk.CTkButton(header, text="+ Nova Notícia", font=("Courier New", 12, "bold"),
                      fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
                      width=150, height=34, command=self._add).pack(side="right")

        # Scrollable list
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=BG_DARK, corner_radius=8)
        self.scroll.pack(fill="both", expand=True)
        self._render_list()

    def _render_list(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        if not self.data:
            ctk.CTkLabel(self.scroll, text="Sem notícias. Clica em '+ Nova Notícia' para começar.",
                         text_color=FG_MUTED, font=("Courier New", 12)).pack(pady=40)
            return

        for i, item in enumerate(self.data):
            card = ctk.CTkFrame(self.scroll, fg_color=BG_CARD, corner_radius=8, height=80)
            card.pack(fill="x", pady=4, padx=4)
            card.pack_propagate(False)

            # Content
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=15, pady=10)

            ctk.CTkLabel(info, text=item.get("titulo", "Sem título"),
                         font=("Courier New", 14, "bold"), text_color=FG_TEXT,
                         anchor="w").pack(fill="x")

            meta = f"{item.get('data', '?')}  •  {item.get('categoria', 'geral').upper()}"
            ctk.CTkLabel(info, text=meta, font=("Courier New", 11),
                         text_color=FG_MUTED, anchor="w").pack(fill="x")

            # Buttons
            btns = ctk.CTkFrame(card, fg_color="transparent")
            btns.pack(side="right", padx=10)
            ctk.CTkButton(btns, text="✏️", width=34, height=34, fg_color=AZUL_REAL,
                          hover_color=AZUL_PROFUNDO, command=lambda idx=i: self._edit(idx)).pack(side="left", padx=2)
            ctk.CTkButton(btns, text="🗑️", width=34, height=34, fg_color=DANGER,
                          hover_color="#8B1111", command=lambda idx=i: self._delete(idx)).pack(side="left", padx=2)

    def _add(self):
        NoticiasEditor(self, None, self._on_save)

    def _edit(self, idx):
        NoticiasEditor(self, self.data[idx], lambda item: self._on_save(item, idx))

    def _delete(self, idx):
        if messagebox.askyesno("Apagar", f"Apagar '{self.data[idx].get('titulo', '')}'?"):
            self.data.pop(idx)
            save_json("noticias.json", self.data)
            self._render_list()

    def _on_save(self, item, idx=None):
        if idx is not None:
            self.data[idx] = item
        else:
            self.data.insert(0, item)
        save_json("noticias.json", self.data)
        self._render_list()


class NoticiasEditor(ctk.CTkToplevel):
    def __init__(self, parent, item, callback):
        super().__init__(parent)
        self.title("Notícia" if item else "Nova Notícia")
        self.geometry("550x520")
        self.configure(fg_color=BG_DARK)
        self.callback = callback
        self.item = item or {}
        self.img_path = self.item.get("imagem", "")
        self.grab_set()
        self._build()

    def _build(self):
        pad = {"padx": 20, "pady": (8, 0)}

        ctk.CTkLabel(self, text="Título", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.titulo = ctk.CTkEntry(self, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL)
        self.titulo.pack(fill="x", padx=20)
        self.titulo.insert(0, self.item.get("titulo", ""))

        ctk.CTkLabel(self, text="Data", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.data_entry = ctk.CTkEntry(self, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL,
                                        placeholder_text="ex: 15 Mar 2026")
        self.data_entry.pack(fill="x", padx=20)
        self.data_entry.insert(0, self.item.get("data", ""))

        ctk.CTkLabel(self, text="Categoria", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.categoria = ctk.CTkComboBox(self, values=CATEGORIAS, font=("Courier New", 13),
                                          fg_color=BG_CARD, border_color=AZUL_REAL,
                                          dropdown_fg_color=BG_CARD)
        self.categoria.pack(fill="x", padx=20)
        self.categoria.set(self.item.get("categoria", "geral"))

        ctk.CTkLabel(self, text="Corpo do texto", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.corpo = ctk.CTkTextbox(self, height=120, font=("Courier New", 12), fg_color=BG_CARD,
                                     border_color=AZUL_REAL, border_width=1)
        self.corpo.pack(fill="x", padx=20)
        self.corpo.insert("1.0", self.item.get("corpo", ""))

        # Image
        img_frame = ctk.CTkFrame(self, fg_color="transparent")
        img_frame.pack(fill="x", padx=20, pady=(10, 0))
        ctk.CTkButton(img_frame, text="📁 Selecionar Imagem", width=180,
                      fg_color=AZUL_REAL, hover_color=AZUL_PROFUNDO,
                      command=self._pick_image).pack(side="left")
        self.img_label = ctk.CTkLabel(img_frame, text=os.path.basename(self.img_path) if self.img_path else "Nenhuma",
                                       text_color=FG_MUTED, font=("Courier New", 11))
        self.img_label.pack(side="left", padx=10)

        # Save button
        ctk.CTkButton(self, text="GUARDAR", font=("Courier New", 13, "bold"), height=40,
                      fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
                      command=self._save).pack(pady=20)

    def _pick_image(self):
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.webp")])
        if path:
            self.img_path = path
            self.img_label.configure(text=os.path.basename(path))

    def _save(self):
        titulo = self.titulo.get().strip()
        if not titulo:
            messagebox.showwarning("Campo obrigatório", "O título é obrigatório.")
            return

        # Copy image if it's an external file
        img_rel = self.img_path
        if self.img_path and not self.img_path.startswith("assets/"):
            img_rel = copy_image(self.img_path)

        result = {
            "id": self.item.get("id", gen_id()),
            "titulo": titulo,
            "data": self.data_entry.get().strip(),
            "categoria": self.categoria.get(),
            "corpo": self.corpo.get("1.0", "end-1c").strip(),
            "imagem": img_rel
        }
        self.callback(result)
        self.destroy()


# ═══════════════════════════════════════════════════════════════
#  MODULE: MEMBROS
# ═══════════════════════════════════════════════════════════════
INSTRUMENTOS = [
    "Guitarra Clássica", "Guitarra Portuguesa", "Bandolim", "Cavaquinho",
    "Viola Baixo", "Acordeão", "Flauta", "Pandeireta", "Bombo",
    "Ferrinhos", "Voz", "Outro"
]

class MembrosModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("membros.json")
        if not isinstance(self.data, dict) or "geracoes" not in self.data:
            self.data = {"geracoes": []}
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header, text="👥  Augustunos", font=("Courier New", 20, "bold"),
                     text_color=DOURADO).pack(side="left")
        ctk.CTkButton(header, text="+ Nova Geração", font=("Courier New", 12, "bold"),
                      fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
                      width=160, height=34, command=self._add_gen).pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=BG_DARK, corner_radius=8)
        self.scroll.pack(fill="both", expand=True)
        self._render()

    def _render(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        if not self.data["geracoes"]:
            ctk.CTkLabel(self.scroll, text="Sem gerações. Clica em '+ Nova Geração' para começar.",
                         text_color=FG_MUTED, font=("Courier New", 12)).pack(pady=40)
            return

        for gi, gen in enumerate(self.data["geracoes"]):
            # Generation header
            gen_frame = ctk.CTkFrame(self.scroll, fg_color=BG_CARD, corner_radius=8)
            gen_frame.pack(fill="x", pady=6, padx=4)

            gen_header = ctk.CTkFrame(gen_frame, fg_color="transparent")
            gen_header.pack(fill="x", padx=15, pady=10)

            ctk.CTkLabel(gen_header, text=gen.get("nome", "Geração ?"),
                         font=("Courier New", 15, "bold"), text_color=DOURADO).pack(side="left")

            btn_row = ctk.CTkFrame(gen_header, fg_color="transparent")
            btn_row.pack(side="right")
            ctk.CTkButton(btn_row, text="+ Membro", width=100, height=30,
                          fg_color=AZUL_REAL, hover_color=AZUL_PROFUNDO, font=("Courier New", 11),
                          command=lambda g=gi: self._add_member(g)).pack(side="left", padx=2)
            ctk.CTkButton(btn_row, text="🗑️", width=30, height=30, fg_color=DANGER,
                          hover_color="#8B1111",
                          command=lambda g=gi: self._del_gen(g)).pack(side="left", padx=2)

            # Members list
            for mi, m in enumerate(gen.get("elementos", [])):
                mf = ctk.CTkFrame(gen_frame, fg_color="#222222", corner_radius=6)
                mf.pack(fill="x", padx=15, pady=2)

                info_text = f"{m.get('nome', '?')}  •  \"{m.get('alcunha', '')}\"  •  {m.get('instrumento', '?')}"
                ctk.CTkLabel(mf, text=info_text, font=("Courier New", 12), text_color=FG_TEXT,
                             anchor="w").pack(side="left", padx=10, pady=6)

                mb = ctk.CTkFrame(mf, fg_color="transparent")
                mb.pack(side="right", padx=5)
                ctk.CTkButton(mb, text="✏️", width=28, height=28, fg_color=AZUL_REAL,
                              hover_color=AZUL_PROFUNDO,
                              command=lambda g=gi, m_=mi: self._edit_member(g, m_)).pack(side="left", padx=1)
                ctk.CTkButton(mb, text="✕", width=28, height=28, fg_color=DANGER,
                              hover_color="#8B1111",
                              command=lambda g=gi, m_=mi: self._del_member(g, m_)).pack(side="left", padx=1)

            # Bottom padding
            ctk.CTkFrame(gen_frame, fg_color="transparent", height=8).pack()

    def _add_gen(self):
        name = simpledialog.askstring("Nova Geração", "Nome da Geração (ex: Geração 2024/2025):")
        if name:
            self.data["geracoes"].append({"nome": name, "elementos": []})
            save_json("membros.json", self.data)
            self._render()

    def _del_gen(self, gi):
        gen = self.data["geracoes"][gi]
        if messagebox.askyesno("Apagar", f"Apagar '{gen.get('nome', '')}'?"):
            self.data["geracoes"].pop(gi)
            save_json("membros.json", self.data)
            self._render()

    def _add_member(self, gi):
        MemberEditor(self, None, lambda m: self._on_save_member(gi, m))

    def _edit_member(self, gi, mi):
        member = self.data["geracoes"][gi]["elementos"][mi]
        MemberEditor(self, member, lambda m: self._on_save_member(gi, m, mi))

    def _del_member(self, gi, mi):
        m = self.data["geracoes"][gi]["elementos"][mi]
        if messagebox.askyesno("Apagar", f"Apagar '{m.get('nome', '')}'?"):
            self.data["geracoes"][gi]["elementos"].pop(mi)
            save_json("membros.json", self.data)
            self._render()

    def _on_save_member(self, gi, member, mi=None):
        if mi is not None:
            self.data["geracoes"][gi]["elementos"][mi] = member
        else:
            self.data["geracoes"][gi]["elementos"].append(member)
        save_json("membros.json", self.data)
        self._render()


class MemberEditor(ctk.CTkToplevel):
    def __init__(self, parent, item, callback):
        super().__init__(parent)
        self.title("Membro" if item else "Novo Membro")
        self.geometry("480x440")
        self.configure(fg_color=BG_DARK)
        self.callback = callback
        self.item = item or {}
        self.grab_set()
        self._build()

    def _build(self):
        pad = {"padx": 20, "pady": (8, 0)}
        fields = [
            ("Nome", "nome", "entry"),
            ("Alcunha", "alcunha", "entry"),
            ("Curso", "curso", "entry"),
            ("Data de Passagem", "data_passagem", "entry"),
        ]
        self.entries = {}
        for label, key, _ in fields:
            ctk.CTkLabel(self, text=label, text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
            e = ctk.CTkEntry(self, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL)
            e.pack(fill="x", padx=20)
            e.insert(0, self.item.get(key, ""))
            self.entries[key] = e

        ctk.CTkLabel(self, text="Instrumento", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.instrumento = ctk.CTkComboBox(self, values=INSTRUMENTOS, font=("Courier New", 13),
                                            fg_color=BG_CARD, border_color=AZUL_REAL,
                                            dropdown_fg_color=BG_CARD)
        self.instrumento.pack(fill="x", padx=20)
        self.instrumento.set(self.item.get("instrumento", "Guitarra Clássica"))

        ctk.CTkButton(self, text="GUARDAR", font=("Courier New", 13, "bold"), height=40,
                      fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
                      command=self._save).pack(pady=20)

    def _save(self):
        nome = self.entries["nome"].get().strip()
        if not nome:
            messagebox.showwarning("Campo obrigatório", "O nome é obrigatório.")
            return
        result = {k: e.get().strip() for k, e in self.entries.items()}
        result["instrumento"] = self.instrumento.get()
        self.callback(result)
        self.destroy()


# ═══════════════════════════════════════════════════════════════
#  MODULE: EVENTOS (Magna Augusta + Festa do Semina)
# ═══════════════════════════════════════════════════════════════
class EventosModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("eventos.json")
        if not isinstance(self.data, dict):
            self.data = {"magna_augusta": [], "festa_semina": []}
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="🎉  Eventos", font=("Courier New", 20, "bold"),
                     text_color=DOURADO).pack(anchor="w", pady=(0, 15))

        self.tabs = ctk.CTkTabview(self, fg_color=BG_CARD, segmented_button_fg_color=BG_SIDEBAR,
                                    segmented_button_selected_color=AZUL_REAL,
                                    segmented_button_unselected_color=BG_CARD)
        self.tabs.pack(fill="both", expand=True)

        self.tabs.add("Magna Augusta")
        self.tabs.add("Festa do Semina")

        self._build_event_tab(self.tabs.tab("Magna Augusta"), "magna_augusta")
        self._build_event_tab(self.tabs.tab("Festa do Semina"), "festa_semina")

    def _build_event_tab(self, tab, key):
        header = ctk.CTkFrame(tab, fg_color="transparent")
        header.pack(fill="x", pady=(5, 10))
        ctk.CTkButton(header, text="+ Nova Edição", width=140, height=32,
                      fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
                      font=("Courier New", 11, "bold"),
                      command=lambda: self._add_event(key, tab)).pack(side="right")

        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        scroll._key = key  # stash for re-render

        self._render_events(scroll, key)

    def _render_events(self, scroll, key):
        for w in scroll.winfo_children():
            w.destroy()

        events = self.data.get(key, [])
        if not events:
            ctk.CTkLabel(scroll, text="Sem edições.", text_color=FG_MUTED).pack(pady=30)
            return

        for i, ev in enumerate(events):
            card = ctk.CTkFrame(scroll, fg_color="#222222", corner_radius=8)
            card.pack(fill="x", pady=3, padx=2)
            info = f"{ev.get('edicao', '?')} ({ev.get('ano', '?')}) — {ev.get('descricao', '')[:60]}"
            ctk.CTkLabel(card, text=info, font=("Courier New", 12), text_color=FG_TEXT,
                         anchor="w").pack(side="left", padx=10, pady=8)
            btns = ctk.CTkFrame(card, fg_color="transparent")
            btns.pack(side="right", padx=5)
            ctk.CTkButton(btns, text="✏️", width=28, height=28, fg_color=AZUL_REAL,
                          command=lambda k=key, idx=i, s=scroll: self._edit_event(k, idx, s)).pack(side="left", padx=1)
            ctk.CTkButton(btns, text="🗑️", width=28, height=28, fg_color=DANGER,
                          command=lambda k=key, idx=i, s=scroll: self._del_event(k, idx, s)).pack(side="left", padx=1)

    def _add_event(self, key, tab):
        # Find the scrollable frame within this tab
        scroll = None
        for child in tab.winfo_children():
            if isinstance(child, ctk.CTkScrollableFrame):
                scroll = child
                break
        EventEditor(self, None, lambda ev: self._on_save_event(key, ev, scroll))

    def _edit_event(self, key, idx, scroll):
        EventEditor(self, self.data[key][idx], lambda ev: self._on_save_event(key, ev, scroll, idx))

    def _del_event(self, key, idx, scroll):
        if messagebox.askyesno("Apagar", "Apagar esta edição?"):
            self.data[key].pop(idx)
            save_json("eventos.json", self.data)
            self._render_events(scroll, key)

    def _on_save_event(self, key, ev, scroll, idx=None):
        if idx is not None:
            self.data[key][idx] = ev
        else:
            self.data[key].insert(0, ev)
        save_json("eventos.json", self.data)
        if scroll:
            self._render_events(scroll, key)


class EventEditor(ctk.CTkToplevel):
    def __init__(self, parent, item, callback):
        super().__init__(parent)
        self.title("Edição")
        self.geometry("500x400")
        self.configure(fg_color=BG_DARK)
        self.callback = callback
        self.item = item or {}
        self.img_path = self.item.get("imagem", "")
        self.grab_set()
        self._build()

    def _build(self):
        pad = {"padx": 20, "pady": (8, 0)}

        ctk.CTkLabel(self, text="Edição (ex: IX)", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.edicao = ctk.CTkEntry(self, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL)
        self.edicao.pack(fill="x", padx=20)
        self.edicao.insert(0, self.item.get("edicao", ""))

        ctk.CTkLabel(self, text="Ano", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.ano = ctk.CTkEntry(self, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL)
        self.ano.pack(fill="x", padx=20)
        self.ano.insert(0, str(self.item.get("ano", "")))

        ctk.CTkLabel(self, text="Descrição", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.descricao = ctk.CTkTextbox(self, height=100, font=("Courier New", 12), fg_color=BG_CARD,
                                         border_color=AZUL_REAL, border_width=1)
        self.descricao.pack(fill="x", padx=20)
        self.descricao.insert("1.0", self.item.get("descricao", ""))

        img_frame = ctk.CTkFrame(self, fg_color="transparent")
        img_frame.pack(fill="x", padx=20, pady=(10, 0))
        ctk.CTkButton(img_frame, text="📁 Imagem", width=120, fg_color=AZUL_REAL,
                      command=self._pick_image).pack(side="left")
        self.img_label = ctk.CTkLabel(img_frame, text=os.path.basename(self.img_path) if self.img_path else "Nenhuma",
                                       text_color=FG_MUTED, font=("Courier New", 11))
        self.img_label.pack(side="left", padx=10)

        ctk.CTkButton(self, text="GUARDAR", font=("Courier New", 13, "bold"), height=40,
                      fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
                      command=self._save).pack(pady=15)

    def _pick_image(self):
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.webp")])
        if path:
            self.img_path = path
            self.img_label.configure(text=os.path.basename(path))

    def _save(self):
        img_rel = self.img_path
        if self.img_path and not self.img_path.startswith("assets/"):
            img_rel = copy_image(self.img_path)
        try:
            ano = int(self.ano.get().strip())
        except ValueError:
            ano = 0
        result = {
            "edicao": self.edicao.get().strip(),
            "ano": ano,
            "descricao": self.descricao.get("1.0", "end-1c").strip(),
            "imagem": img_rel
        }
        self.callback(result)
        self.destroy()


# ═══════════════════════════════════════════════════════════════
#  MODULE: ATUAÇÕES
# ═══════════════════════════════════════════════════════════════
class AtuacoesModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("atuacoes.json")
        if not isinstance(self.data, dict):
            self.data = {"festivais_concurso": [], "festivais_convite": [], "outras": []}
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="🎵  Atuações", font=("Courier New", 20, "bold"),
                     text_color=DOURADO).pack(anchor="w", pady=(0, 15))

        self.tabs = ctk.CTkTabview(self, fg_color=BG_CARD, segmented_button_fg_color=BG_SIDEBAR,
                                    segmented_button_selected_color=AZUL_REAL,
                                    segmented_button_unselected_color=BG_CARD)
        self.tabs.pack(fill="both", expand=True)

        tab_map = [
            ("Festivais a Concurso", "festivais_concurso"),
            ("Festivais a Convite", "festivais_convite"),
            ("Outras Atuações", "outras")
        ]
        for tab_name, key in tab_map:
            self.tabs.add(tab_name)
            self._build_atuacao_tab(self.tabs.tab(tab_name), key)

    def _build_atuacao_tab(self, tab, key):
        header = ctk.CTkFrame(tab, fg_color="transparent")
        header.pack(fill="x", pady=(5, 10))
        ctk.CTkButton(header, text="+ Nova Atuação", width=150, height=32,
                      fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
                      font=("Courier New", 11, "bold"),
                      command=lambda: self._add_atuacao(key, tab)).pack(side="right")

        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        self._render_atuacoes(scroll, key)

    def _render_atuacoes(self, scroll, key):
        for w in scroll.winfo_children():
            w.destroy()
        items = self.data.get(key, [])
        if not items:
            ctk.CTkLabel(scroll, text="Sem atuações.", text_color=FG_MUTED).pack(pady=30)
            return

        for i, item in enumerate(items):
            card = ctk.CTkFrame(scroll, fg_color="#222222", corner_radius=8)
            card.pack(fill="x", pady=3, padx=2)
            info = f"{item.get('data', '?')} — {item.get('titulo', '?')}  ({item.get('localizacao', '?')})"
            ctk.CTkLabel(card, text=info, font=("Courier New", 12), text_color=FG_TEXT,
                         anchor="w").pack(side="left", padx=10, pady=8)
            btns = ctk.CTkFrame(card, fg_color="transparent")
            btns.pack(side="right", padx=5)
            ctk.CTkButton(btns, text="✏️", width=28, height=28, fg_color=AZUL_REAL,
                          command=lambda k=key, idx=i, s=scroll: self._edit_atuacao(k, idx, s)).pack(side="left", padx=1)
            ctk.CTkButton(btns, text="🗑️", width=28, height=28, fg_color=DANGER,
                          command=lambda k=key, idx=i, s=scroll: self._del_atuacao(k, idx, s)).pack(side="left", padx=1)

    def _add_atuacao(self, key, tab):
        scroll = None
        for child in tab.winfo_children():
            if isinstance(child, ctk.CTkScrollableFrame):
                scroll = child
                break
        AtuacaoEditor(self, None, lambda a: self._on_save(key, a, scroll))

    def _edit_atuacao(self, key, idx, scroll):
        AtuacaoEditor(self, self.data[key][idx], lambda a: self._on_save(key, a, scroll, idx))

    def _del_atuacao(self, key, idx, scroll):
        if messagebox.askyesno("Apagar", "Apagar esta atuação?"):
            self.data[key].pop(idx)
            save_json("atuacoes.json", self.data)
            self._render_atuacoes(scroll, key)

    def _on_save(self, key, item, scroll, idx=None):
        if idx is not None:
            self.data[key][idx] = item
        else:
            self.data[key].insert(0, item)
        save_json("atuacoes.json", self.data)
        if scroll:
            self._render_atuacoes(scroll, key)


class AtuacaoEditor(ctk.CTkToplevel):
    def __init__(self, parent, item, callback):
        super().__init__(parent)
        self.title("Atuação")
        self.geometry("500x400")
        self.configure(fg_color=BG_DARK)
        self.callback = callback
        self.item = item or {}
        self.grab_set()
        self._build()

    def _build(self):
        pad = {"padx": 20, "pady": (8, 0)}

        # Date Dropdowns
        ctk.CTkLabel(self, text="Data da Atuação", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        date_frame = ctk.CTkFrame(self, fg_color="transparent")
        date_frame.pack(fill="x", padx=20)
        
        self.dia = ctk.CTkComboBox(date_frame, values=[str(i).zfill(2) for i in range(1, 32)], width=70, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL)
        self.dia.pack(side="left", padx=(0, 10))
        
        meses = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
        self.mes = ctk.CTkComboBox(date_frame, values=meses, width=80, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL)
        self.mes.pack(side="left", padx=(0, 10))
        
        anos = [str(i) for i in range(1996, datetime.now().year + 5)]
        self.ano = ctk.CTkComboBox(date_frame, values=anos, width=80, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL)
        self.ano.pack(side="left")

        # Parse existing date (e.g. "22 MAR 2023")
        old_data = self.item.get("data", "")
        parts = old_data.split(" ")
        if len(parts) == 3:
            self.dia.set(parts[0])
            self.mes.set(parts[1][:3].upper())
            self.ano.set(parts[2])
        else:
            self.dia.set(str(datetime.now().day).zfill(2))
            self.mes.set(meses[datetime.now().month - 1])
            self.ano.set(str(datetime.now().year))

        # Other fields
        fields = [
            ("Título", "titulo", "Obrigatório"),
            ("Localização", "localizacao", "Obrigatório"),
        ]
        self.entries = {}
        for label, key, ph in fields:
            ctk.CTkLabel(self, text=label, text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
            e = ctk.CTkEntry(self, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL,
                              placeholder_text=ph)
            e.pack(fill="x", padx=20)
            e.insert(0, self.item.get(key, ""))
            self.entries[key] = e

        ctk.CTkLabel(self, text="Descrição", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.descricao = ctk.CTkTextbox(self, height=100, font=("Courier New", 12), fg_color=BG_CARD,
                                         border_color=AZUL_REAL, border_width=1)
        self.descricao.pack(fill="x", padx=20)
        self.descricao.insert("1.0", self.item.get("descricao", ""))

        ctk.CTkButton(self, text="GUARDAR", font=("Courier New", 13, "bold"), height=40,
                      fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
                      command=self._save).pack(pady=20)

    def _save(self):
        result = {k: e.get().strip() for k, e in self.entries.items()}
        result["data"] = f"{self.dia.get()} {self.mes.get()} {self.ano.get()}"
        result["descricao"] = self.descricao.get("1.0", "end-1c").strip()
        result["id"] = self.item.get("id", gen_id())
        self.callback(result)
        self.destroy()


# ═══════════════════════════════════════════════════════════════
#  MODULE: LOJA
# ═══════════════════════════════════════════════════════════════
TAMANHOS = ["S", "M", "L", "XL"]

class LojaModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("loja.json")
        if not isinstance(self.data, list):
            self.data = []
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header, text="🛍️  Loja", font=("Courier New", 20, "bold"),
                     text_color=DOURADO).pack(side="left")
        ctk.CTkButton(header, text="+ Novo Produto", font=("Courier New", 12, "bold"),
                      fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
                      width=150, height=34, command=self._add).pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=BG_DARK, corner_radius=8)
        self.scroll.pack(fill="both", expand=True)
        self._render()

    def _render(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        if not self.data:
            ctk.CTkLabel(self.scroll, text="Sem produtos.", text_color=FG_MUTED,
                         font=("Courier New", 12)).pack(pady=40)
            return

        for i, item in enumerate(self.data):
            card = ctk.CTkFrame(self.scroll, fg_color=BG_CARD, corner_radius=8, height=70)
            card.pack(fill="x", pady=4, padx=4)
            card.pack_propagate(False)

            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=15, pady=8)

            ctk.CTkLabel(info, text=item.get("nome", "?"), font=("Courier New", 14, "bold"),
                         text_color=FG_TEXT, anchor="w").pack(fill="x")

            sizes = ", ".join(item.get("tamanhos", []))
            meta = f"{item.get('preco', 0):.2f}€  •  Tamanhos: {sizes}"
            ctk.CTkLabel(info, text=meta, font=("Courier New", 11), text_color=FG_MUTED,
                         anchor="w").pack(fill="x")

            btns = ctk.CTkFrame(card, fg_color="transparent")
            btns.pack(side="right", padx=10)
            ctk.CTkButton(btns, text="✏️", width=34, height=34, fg_color=AZUL_REAL,
                          hover_color=AZUL_PROFUNDO, command=lambda idx=i: self._edit(idx)).pack(side="left", padx=2)
            ctk.CTkButton(btns, text="🗑️", width=34, height=34, fg_color=DANGER,
                          hover_color="#8B1111", command=lambda idx=i: self._delete(idx)).pack(side="left", padx=2)

    def _add(self):
        LojaEditor(self, None, self._on_save)

    def _edit(self, idx):
        LojaEditor(self, self.data[idx], lambda item: self._on_save(item, idx))

    def _delete(self, idx):
        if messagebox.askyesno("Apagar", f"Apagar '{self.data[idx].get('nome', '')}'?"):
            self.data.pop(idx)
            save_json("loja.json", self.data)
            self._render()

    def _on_save(self, item, idx=None):
        if idx is not None:
            self.data[idx] = item
        else:
            self.data.insert(0, item)
        save_json("loja.json", self.data)
        self._render()


class LojaEditor(ctk.CTkToplevel):
    def __init__(self, parent, item, callback):
        super().__init__(parent)
        self.title("Produto" if item else "Novo Produto")
        self.geometry("520x540")
        self.configure(fg_color=BG_DARK)
        self.callback = callback
        self.item = item or {}
        self.img_path = self.item.get("imagem", "")
        self.size_vars = {}
        self.grab_set()
        self._build()

    def _build(self):
        pad = {"padx": 20, "pady": (8, 0)}

        ctk.CTkLabel(self, text="Nome do Produto", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.nome = ctk.CTkEntry(self, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL)
        self.nome.pack(fill="x", padx=20)
        self.nome.insert(0, self.item.get("nome", ""))

        ctk.CTkLabel(self, text="Preço (€)", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.preco = ctk.CTkEntry(self, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL,
                                   placeholder_text="ex: 15.00")
        self.preco.pack(fill="x", padx=20)
        self.preco.insert(0, str(self.item.get("preco", "")))

        ctk.CTkLabel(self, text="Descrição", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        self.descricao = ctk.CTkTextbox(self, height=80, font=("Courier New", 12), fg_color=BG_CARD,
                                         border_color=AZUL_REAL, border_width=1)
        self.descricao.pack(fill="x", padx=20)
        self.descricao.insert("1.0", self.item.get("descricao", ""))

        # Sizes
        ctk.CTkLabel(self, text="Tamanhos Disponíveis", text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
        size_frame = ctk.CTkFrame(self, fg_color="transparent")
        size_frame.pack(fill="x", padx=20, pady=(5, 0))
        existing_sizes = self.item.get("tamanhos", [])
        for s in TAMANHOS:
            var = ctk.BooleanVar(value=s in existing_sizes)
            cb = ctk.CTkCheckBox(size_frame, text=s, variable=var, font=("Courier New", 12),
                                  fg_color=DOURADO, hover_color=GOLD_HOVER, border_color=AZUL_REAL)
            cb.pack(side="left", padx=8)
            self.size_vars[s] = var

        # Image
        img_frame = ctk.CTkFrame(self, fg_color="transparent")
        img_frame.pack(fill="x", padx=20, pady=(12, 0))
        ctk.CTkButton(img_frame, text="📁 Selecionar Imagem", width=180,
                      fg_color=AZUL_REAL, hover_color=AZUL_PROFUNDO,
                      command=self._pick_image).pack(side="left")
        self.img_label = ctk.CTkLabel(img_frame, text=os.path.basename(self.img_path) if self.img_path else "Nenhuma",
                                       text_color=FG_MUTED, font=("Courier New", 11))
        self.img_label.pack(side="left", padx=10)

        ctk.CTkButton(self, text="GUARDAR", font=("Courier New", 13, "bold"), height=40,
                      fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
                      command=self._save).pack(pady=18)

    def _pick_image(self):
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.webp")])
        if path:
            self.img_path = path
            self.img_label.configure(text=os.path.basename(path))

    def _save(self):
        nome = self.nome.get().strip()
        if not nome:
            messagebox.showwarning("Campo obrigatório", "O nome é obrigatório.")
            return
        try:
            preco = float(self.preco.get().strip().replace(",", "."))
        except ValueError:
            preco = 0.0

        img_rel = self.img_path
        if self.img_path and not self.img_path.startswith("assets/"):
            img_rel = copy_image(self.img_path)

        tamanhos = [s for s, v in self.size_vars.items() if v.get()]

        result = {
            "id": self.item.get("id", gen_id()),
            "nome": nome,
            "preco": preco,
            "descricao": self.descricao.get("1.0", "end-1c").strip(),
            "imagem": img_rel,
            "tamanhos": tamanhos,
        }
        self.callback(result)
        self.destroy()


# ═══════════════════════════════════════════════════════════════
#  MODULE: CONTACTOS
# ═══════════════════════════════════════════════════════════════
class ContactosModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("contactos.json")
        if not isinstance(self.data, dict) or "redes_sociais" not in self.data:
            self.data = {
                "redes_sociais": {},
                "informacoes_gerais": {},
                "dirigentes": []
            }
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header, text="📞  Contactos", font=("Courier New", 20, "bold"),
                     text_color=DOURADO).pack(side="left")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=BG_DARK, corner_radius=8)
        self.scroll.pack(fill="both", expand=True)
        self._render()

    def _render(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        pad = {"padx": 15, "pady": 10}

        # 1. Informações Gerais (Morada, Email, Telefone)
        geral_frame = ctk.CTkFrame(self.scroll, fg_color=BG_CARD, corner_radius=8)
        geral_frame.pack(fill="x", pady=10)
        geral_header = ctk.CTkFrame(geral_frame, fg_color="transparent")
        geral_header.pack(fill="x", **pad)
        ctk.CTkLabel(geral_header, text="Informações Gerais", font=("Courier New", 16, "bold"), text_color=FG_TEXT).pack(side="left")
        ctk.CTkButton(geral_header, text="✏️ Editar", width=80, height=28, fg_color=AZUL_REAL,
                      command=self._edit_geral).pack(side="right")
        
        info = self.data.get("informacoes_gerais", {})
        info_lines = [
            f"Morada: {info.get('morada', '')}",
            f"Email: {info.get('email', '')}",
            f"Telefone: {info.get('telefone', '')}",
        ]
        ctk.CTkLabel(geral_frame, text="\\n".join(info_lines), font=("Courier New", 12), text_color=FG_MUTED, justify="left", anchor="w").pack(fill="x", padx=15, pady=(0, 10))

        # 2. Redes Sociais
        social_frame = ctk.CTkFrame(self.scroll, fg_color=BG_CARD, corner_radius=8)
        social_frame.pack(fill="x", pady=10)
        social_header = ctk.CTkFrame(social_frame, fg_color="transparent")
        social_header.pack(fill="x", **pad)
        ctk.CTkLabel(social_header, text="Redes Sociais Gerais", font=("Courier New", 16, "bold"), text_color=FG_TEXT).pack(side="left")
        ctk.CTkButton(social_header, text="✏️ Editar", width=80, height=28, fg_color=AZUL_REAL,
                      command=self._edit_sociais).pack(side="right")
        
        redes = self.data.get("redes_sociais", {})
        redes_lines = [
            f"YouTube: {redes.get('youtube', '')}",
            f"Instagram: {redes.get('instagram', '')}",
            f"Facebook: {redes.get('facebook', '')}",
            f"LinkedIn: {redes.get('linkedin', '')}",
            f"Spotify: {redes.get('spotify', '')}",
        ]
        ctk.CTkLabel(social_frame, text="\\n".join(redes_lines), font=("Courier New", 12), text_color=FG_MUTED, justify="left", anchor="w").pack(fill="x", padx=15, pady=(0, 10))

        # 3. Dirigentes (Contacte-nos Pessoalmente)
        dir_frame = ctk.CTkFrame(self.scroll, fg_color=BG_CARD, corner_radius=8)
        dir_frame.pack(fill="x", pady=10)
        dir_header = ctk.CTkFrame(dir_frame, fg_color="transparent")
        dir_header.pack(fill="x", **pad)
        ctk.CTkLabel(dir_header, text="Dirigentes (Contacte-nos Pessoalmente)", font=("Courier New", 16, "bold"), text_color=FG_TEXT).pack(side="left")
        ctk.CTkButton(dir_header, text="+ Adicionar Dirigente", width=140, height=28, fg_color=DOURADO, text_color=BG_DARK,
                      command=self._add_dirigente).pack(side="right")
        
        dirigentes = self.data.get("dirigentes", [])
        if not dirigentes:
            ctk.CTkLabel(dir_frame, text="Sem dirigentes associados.", text_color=FG_MUTED).pack(pady=10)
        for i, d in enumerate(dirigentes):
            df = ctk.CTkFrame(dir_frame, fg_color="#222222", corner_radius=6)
            df.pack(fill="x", padx=15, pady=4)
            d_text = f"{d.get('cargo', '')}: {d.get('nome', '')} ({d.get('telefone', '')})"
            ctk.CTkLabel(df, text=d_text, font=("Courier New", 12), text_color=FG_TEXT, anchor="w").pack(side="left", padx=10, pady=8)
            btns = ctk.CTkFrame(df, fg_color="transparent")
            btns.pack(side="right", padx=5)
            ctk.CTkButton(btns, text="✏️", width=28, height=28, fg_color=AZUL_REAL,
                          command=lambda idx=i: self._edit_dirigente(idx)).pack(side="left", padx=1)
            ctk.CTkButton(btns, text="🗑️", width=28, height=28, fg_color=DANGER,
                          command=lambda idx=i: self._del_dirigente(idx)).pack(side="left", padx=1)
        ctk.CTkFrame(dir_frame, fg_color="transparent", height=10).pack()

    def _edit_geral(self):
        obj = self.data.get("informacoes_gerais", {})
        ContactDictEditor(self, "Informações Gerais", ["morada", "email", "telefone"], obj, self._on_save_geral)

    def _on_save_geral(self, new_obj):
        self.data["informacoes_gerais"] = new_obj
        save_json("contactos.json", self.data)
        self._render()

    def _edit_sociais(self):
        obj = self.data.get("redes_sociais", {})
        ContactDictEditor(self, "Redes Sociais", ["youtube", "instagram", "facebook", "linkedin", "spotify"], obj, self._on_save_sociais)

    def _on_save_sociais(self, new_obj):
        self.data["redes_sociais"] = new_obj
        save_json("contactos.json", self.data)
        self._render()

    def _add_dirigente(self):
        ContactDictEditor(self, "Novo Dirigente", ["cargo", "nome", "telefone"], {}, lambda x: self._on_save_dir(x))

    def _edit_dirigente(self, idx):
        ContactDictEditor(self, "Editar Dirigente", ["cargo", "nome", "telefone"], self.data["dirigentes"][idx], lambda x: self._on_save_dir(x, idx))

    def _del_dirigente(self, idx):
        if messagebox.askyesno("Apagar", "Apagar este dirigente?"):
            self.data["dirigentes"].pop(idx)
            save_json("contactos.json", self.data)
            self._render()
            
    def _on_save_dir(self, new_obj, idx=None):
        if idx is not None:
            self.data["dirigentes"][idx] = new_obj
        else:
            self.data["dirigentes"].append(new_obj)
        save_json("contactos.json", self.data)
        self._render()


class ContactDictEditor(ctk.CTkToplevel):
    def __init__(self, parent, title_str, fields, item, callback):
        super().__init__(parent)
        self.title(title_str)
        self.geometry("450x450")
        self.configure(fg_color=BG_DARK)
        self.callback = callback
        self.item = item or {}
        self.fields = fields
        self.grab_set()
        self._build()

    def _build(self):
        pad = {"padx": 20, "pady": (8, 0)}
        self.entries = {}
        for key in self.fields:
            ctk.CTkLabel(self, text=key.capitalize(), text_color=FG_MUTED, font=("Courier New", 11)).pack(**pad, anchor="w")
            e = ctk.CTkEntry(self, font=("Courier New", 13), fg_color=BG_CARD, border_color=AZUL_REAL)
            e.pack(fill="x", padx=20)
            e.insert(0, self.item.get(key, ""))
            self.entries[key] = e

        ctk.CTkButton(self, text="GUARDAR", font=("Courier New", 13, "bold"), height=40,
                      fg_color=DOURADO, text_color=BG_DARK, hover_color=GOLD_HOVER,
                      command=self._save).pack(pady=20)

    def _save(self):
        result = {k: e.get().strip() for k, e in self.entries.items()}
        self.callback(result)
        self.destroy()

# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = AdminHub()
    app.mainloop()
