"""
╔══════════════════════════════════════════════════════════════╗
║              AUGUSTUNA ADMIN HUB  v1.1                       ║
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

# ─── PATHS ───────────────────────────────────────────────────
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
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Augustuna Admin Hub", "Seleciona a pasta do repositório do website.")
    path = filedialog.askdirectory(title="Seleciona a pasta do repositório")
    root.destroy()
    if not path:
        raise SystemExit(1)
    return path

def _get_repo_dir():
    cfg = _load_config()
    repo = cfg.get("repo_dir", "")
    if repo and os.path.isdir(repo) and os.path.isdir(os.path.join(repo, "data")):
        return repo
    repo = _ask_repo_path()
    cfg["repo_dir"] = repo
    _save_config(cfg)
    return repo

REPO_DIR = _get_repo_dir()
DATA_DIR = os.path.join(REPO_DIR, "data")
ASSETS_IMG = os.path.join(REPO_DIR, "assets", "img")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ASSETS_IMG, exist_ok=True)

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
    if not src_path or not os.path.exists(src_path): return ""
    basename = os.path.basename(src_path)
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
#  MAIN APP
# ═══════════════════════════════════════════════════════════════
class AdminHub(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Augustuna Admin Hub")
        self.geometry("1200x800")
        self.configure(fg_color=BG_DARK)
        self._build_sidebar()
        self.content = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)
        self.show_module("noticias")

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=BG_SIDEBAR, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        ctk.CTkLabel(self.sidebar, text="AUGUSTUNA", font=("Courier New", 20, "bold"), text_color=DOURADO).pack(pady=(25, 30))
        
        self.nav_buttons = {}
        modules = [
            ("📰", "Notícias", "noticias"),
            ("👥", "Membros", "membros"),
            ("🎉", "Eventos", "eventos"),
            ("🎵", "Atuações", "atuacoes"),
            ("🛍️", "Loja", "loja"),
            ("📞", "Contactos", "contactos"),
            ("🔧", "Ordenação", "layout"),
        ]
        for icon, label, key in modules:
            btn = ctk.CTkButton(self.sidebar, text=f"  {icon}  {label}", anchor="w", font=("Courier New", 13), height=42, fg_color="transparent", hover_color=AZUL_REAL, command=lambda k=key: self.show_module(k))
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[key] = btn

        ctk.CTkButton(self.sidebar, text="⬆  ATUALIZAR SITE", fg_color=DOURADO, text_color=BG_DARK, font=("Courier New", 11, "bold"), height=40, command=self.git_push).pack(side="bottom", fill="x", padx=12, pady=20)

    def show_module(self, key):
        for k, b in self.nav_buttons.items(): b.configure(fg_color=AZUL_REAL if k == key else "transparent")
        for w in self.content.winfo_children(): w.destroy()
        module_map = {
            "noticias": NoticiasModule, "membros": MembrosModule, "eventos": EventosModule,
            "atuacoes": AtuacoesModule, "loja": LojaModule, "contactos": ContactosModule, "layout": LayoutModule
        }
        if key in module_map: module_map[key](self.content)

    def git_push(self):
        try:
            subprocess.run(["git", "add", "."], cwd=REPO_DIR, check=True)
            subprocess.run(["git", "commit", "-m", f"Admin Update {datetime.now().strftime('%H:%M')}"], cwd=REPO_DIR)
            subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR)
            messagebox.showinfo("Sucesso", "Website atualizado!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

# ═══════════════════════════════════════════════════════════════
#  MODULES
# ═══════════════════════════════════════════════════════════════

class NoticiasModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("noticias.json")
        self._build()
    
    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header, text="📰 Notícias", font=("Courier New", 20, "bold"), text_color=DOURADO).pack(side="left")
        ctk.CTkButton(header, text="+ Nova", width=100, fg_color=DOURADO, text_color=BG_DARK, command=self._add).pack(side="right")
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=BG_DARK)
        self.scroll.pack(fill="both", expand=True)
        self._render()

    def _render(self):
        for w in self.scroll.winfo_children(): w.destroy()
        for i, item in enumerate(self.data):
            f = ctk.CTkFrame(self.scroll, fg_color=BG_CARD)
            f.pack(fill="x", pady=4, padx=5)
            ctk.CTkLabel(f, text=item.get("titulo", "Sem título"), font=("Courier New", 14, "bold")).pack(side="left", padx=15, pady=10)
            ctk.CTkButton(f, text="🗑️", width=30, fg_color=DANGER, command=lambda idx=i: self._del(idx)).pack(side="right", padx=5)
            ctk.CTkButton(f, text="✏️", width=30, fg_color=AZUL_REAL, command=lambda idx=i: self._edit(idx)).pack(side="right", padx=2)

    def _add(self): NoticiasEditor(self, None, self._on_save)
    def _edit(self, idx): NoticiasEditor(self, self.data[idx], lambda item: self._on_save(item, idx))
    def _del(self, idx):
        if messagebox.askyesno("Apagar", "Remover notícia?"):
            self.data.pop(idx); save_json("noticias.json", self.data); self._render()
    def _on_save(self, item, idx=None):
        if idx is not None: self.data[idx] = item
        else: self.data.insert(0, item)
        save_json("noticias.json", self.data); self._render()

class NoticiasEditor(ctk.CTkToplevel):
    def __init__(self, parent, item, callback):
        super().__init__(parent)
        self.item = item or {}; self.callback = callback; self.img_path = self.item.get("imagem", "")
        self.geometry("500x550"); self.configure(fg_color=BG_DARK); self.grab_set(); self._build()
    def _build(self):
        pad = {"padx":20, "pady":5}
        ctk.CTkLabel(self, text="Título").pack(**pad, anchor="w")
        self.titulo = ctk.CTkEntry(self, width=400); self.titulo.pack(**pad); self.titulo.insert(0, self.item.get("titulo", ""))
        ctk.CTkLabel(self, text="Corpo").pack(**pad, anchor="w")
        self.corpo = ctk.CTkTextbox(self, height=150); self.corpo.pack(fill="x", **pad); self.corpo.insert("1.0", self.item.get("corpo", ""))
        self.img_label = ctk.CTkLabel(self, text=os.path.basename(self.img_path) or "Sem imagem")
        self.img_label.pack(**pad)
        ctk.CTkButton(self, text="Selecionar Imagem", command=self._pick).pack(**pad)
        ctk.CTkButton(self, text="GUARDAR", fg_color=DOURADO, text_color=BG_DARK, command=self._save).pack(pady=20)
    def _pick(self):
        p = filedialog.askopenfilename(); 
        if p: self.img_path = p; self.img_label.configure(text=os.path.basename(p))
    def _save(self):
        img = self.img_path if self.img_path.startswith("assets") else copy_image(self.img_path)
        self.callback({"titulo": self.titulo.get(), "corpo": self.corpo.get("1.0", "end-1c"), "imagem": img, "data": datetime.now().strftime("%d %b %Y"), "id": self.item.get("id", gen_id())})
        self.destroy()

# ─── MEMBROS ─────────────────────────
class MembrosModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("membros.json")
        if "geracoes" not in self.data: self.data = {"geracoes": []}
        self._build()
    def _build(self):
        h = ctk.CTkFrame(self, fg_color="transparent"); h.pack(fill="x", pady=(0,15))
        ctk.CTkLabel(h, text="👥 Membros", font=("Courier New", 20, "bold"), text_color=DOURADO).pack(side="left")
        ctk.CTkButton(h, text="+ Geração", width=100, fg_color=DOURADO, text_color=BG_DARK, command=self._add_gen).pack(side="right")
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=BG_DARK); self.scroll.pack(fill="both", expand=True)
        self._render()
    def _render(self):
        for w in self.scroll.winfo_children(): w.destroy()
        for gi, gen in enumerate(self.data["geracoes"]):
            f = ctk.CTkFrame(self.scroll, fg_color=BG_CARD); f.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(f, text=gen["nome"], font=("Courier New", 14, "bold"), text_color=DOURADO).pack(side="left", padx=15, pady=10)
            ctk.CTkButton(f, text="+ Membro", width=80, command=lambda g=gi: self._add_mem(g)).pack(side="right", padx=5)
            ctk.CTkButton(f, text="🗑️", width=30, fg_color=DANGER, command=lambda g=gi: self._del_gen(g)).pack(side="right", padx=2)
            for mi, m in enumerate(gen.get("elementos", [])):
                mf = ctk.CTkFrame(f, fg_color="#222222"); mf.pack(fill="x", padx=15, pady=2)
                ctk.CTkLabel(mf, text=f"{m['nome']} ({m.get('alcunha','')})").pack(side="left", padx=10)
                ctk.CTkButton(mf, text="✕", width=25, fg_color=DANGER, command=lambda g=gi, m_=mi: self._del_mem(g, m_)).pack(side="right", padx=5)
                ctk.CTkButton(mf, text="✏️", width=25, fg_color=AZUL_REAL, command=lambda g=gi, m_=mi: self._edit_mem(g, m_)).pack(side="right", padx=2)
    def _add_gen(self):
        n = simpledialog.askstring("Geração", "Nome:"); 
        if n: self.data["geracoes"].append({"nome":n, "elementos":[]}); save_json("membros.json", self.data); self._render()
    def _del_gen(self, gi): self.data["geracoes"].pop(gi); save_json("membros.json", self.data); self._render()
    def _add_mem(self, gi): MemberEditor(self, None, lambda m: self._save_mem(gi, m))
    def _edit_mem(self, gi, mi): MemberEditor(self, self.data["geracoes"][gi]["elementos"][mi], lambda m: self._save_mem(gi, m, mi))
    def _del_mem(self, gi, mi): self.data["geracoes"][gi]["elementos"].pop(mi); save_json("membros.json", self.data); self._render()
    def _save_mem(self, gi, m, mi=None):
        if mi is not None: self.data["geracoes"][gi]["elementos"][mi] = m
        else: self.data["geracoes"][gi]["elementos"].append(m)
        save_json("membros.json", self.data); self._render()

class MemberEditor(ctk.CTkToplevel):
    def __init__(self, parent, item, callback):
        super().__init__(parent); self.item = item or {}; self.callback = callback; self.img_path = self.item.get("foto", "")
        self.geometry("450x650"); self.configure(fg_color=BG_DARK); self.grab_set(); self._build()
    def _build(self):
        pad = {"padx":20, "pady":5}
        self.nome = self._field("Nome", "nome")
        self.alcunha = self._field("Alcunha", "alcunha")
        self.inst = self._field("Instrumento", "instrumento")
        self.curso = self._field("Curso", "curso")
        self.evento = self._field("Evento de Passagem", "evento")
        self.data_pass = self._field("Data de Passagem (YYYY-MM-DD)", "data_passagem")
        self.img_label = ctk.CTkLabel(self, text=os.path.basename(self.img_path) or "Sem foto"); self.img_label.pack(**pad)
        ctk.CTkButton(self, text="Escolher Foto", command=self._pick).pack(**pad)
        ctk.CTkButton(self, text="GUARDAR", fg_color=DOURADO, text_color=BG_DARK, command=self._save).pack(pady=20)
    def _field(self, label, key):
        ctk.CTkLabel(self, text=label).pack(padx=20, anchor="w")
        e = ctk.CTkEntry(self, width=380); e.pack(padx=20, pady=5); e.insert(0, self.item.get(key,"")); return e
    def _pick(self):
        p = filedialog.askopenfilename(); 
        if p: self.img_path = p; self.img_label.configure(text=os.path.basename(p))
    def _save(self):
        img = self.img_path if self.img_path.startswith("assets") else copy_image(self.img_path)
        self.callback({"nome":self.nome.get(), "alcunha":self.alcunha.get(), "instrumento":self.inst.get(), "curso":self.curso.get(), "evento":self.evento.get(), "data_passagem":self.data_pass.get(), "foto":img})
        self.destroy()

# ─── EVENTOS (Magna/Semina) ──────────
class EventosModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("eventos.json")
        if not isinstance(self.data, dict): self.data = {"magna_augusta":[], "festa_semina":[]}
        self._build()
    def _build(self):
        self.tabs = ctk.CTkTabview(self, fg_color=BG_CARD)
        self.tabs.pack(fill="both", expand=True)
        self.tabs.add("Magna Augusta"); self.tabs.add("Festa do Semina")
        self._tab_ui(self.tabs.tab("Magna Augusta"), "magna_augusta")
        self._tab_ui(self.tabs.tab("Festa do Semina"), "festa_semina")
    def _tab_ui(self, tab, key):
        ctk.CTkButton(tab, text="+ Nova Edição", fg_color=DOURADO, text_color=BG_DARK, command=lambda: self._add(key, tab)).pack(pady=10)
        s = ctk.CTkScrollableFrame(tab, fg_color="transparent"); s.pack(fill="both", expand=True)
        self._render_ev(s, key)
    def _render_ev(self, scroll, key):
        for w in scroll.winfo_children(): w.destroy()
        for i, ev in enumerate(self.data.get(key, [])):
            f = ctk.CTkFrame(scroll, fg_color="#222222"); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{ev['edicao']} ({ev['ano']})").pack(side="left", padx=10)
            ctk.CTkButton(f, text="🗑️", width=30, fg_color=DANGER, command=lambda idx=i: self._del(key, idx, scroll)).pack(side="right", padx=5)
            ctk.CTkButton(f, text="✏️", width=30, fg_color=AZUL_REAL, command=lambda idx=i: self._edit(key, idx, scroll)).pack(side="right", padx=2)
    def _add(self, key, tab):
        s = [c for c in tab.winfo_children() if isinstance(c, ctk.CTkScrollableFrame)][0]
        EventEditor(self, None, lambda e: self._save_ev(key, e, s))
    def _edit(self, key, idx, scroll):
        EventEditor(self, self.data[key][idx], lambda e: self._save_ev(key, e, scroll, idx))
    def _del(self, key, idx, scroll):
        self.data[key].pop(idx); save_json("eventos.json", self.data); self._render_ev(scroll, key)
    def _save_ev(self, key, e, scroll, idx=None):
        if idx is not None: self.data[key][idx] = e
        else: self.data[key].insert(0, e)
        save_json("eventos.json", self.data); self._render_ev(scroll, key)

class EventEditor(ctk.CTkToplevel):
    def __init__(self, parent, item, callback):
        super().__init__(parent); self.item = item or {}; self.callback = callback; self.img_path = self.item.get("imagem", "")
        self.geometry("450x550"); self.configure(fg_color=BG_DARK); self.grab_set(); self._build()
    def _build(self):
        pad = {"padx":20, "pady":5}
        self.ed = self._field("Edição (ex: X)", "edicao")
        self.ano = self._field("Ano", "ano")
        ctk.CTkLabel(self, text="Descrição").pack(padx=20, anchor="w")
        self.desc = ctk.CTkTextbox(self, height=100); self.desc.pack(fill="x", padx=20); self.desc.insert("1.0", self.item.get("descricao",""))
        self.img_label = ctk.CTkLabel(self, text=os.path.basename(self.img_path) or "Sem cartaz"); self.img_label.pack(**pad)
        ctk.CTkButton(self, text="Escolher Cartaz", command=self._pick).pack(**pad)
        ctk.CTkButton(self, text="GUARDAR", fg_color=DOURADO, text_color=BG_DARK, command=self._save).pack(pady=20)
    def _field(self, label, key):
        ctk.CTkLabel(self, text=label).pack(padx=20, anchor="w")
        e = ctk.CTkEntry(self, width=380); e.pack(padx=20, pady=5); e.insert(0, str(self.item.get(key,""))); return e
    def _pick(self):
        p = filedialog.askopenfilename(); 
        if p: self.img_path = p; self.img_label.configure(text=os.path.basename(p))
    def _save(self):
        img = self.img_path if self.img_path.startswith("assets") else copy_image(self.img_path)
        self.callback({"edicao":self.ed.get(), "ano":self.ano.get(), "descricao":self.desc.get("1.0","end-1c"), "imagem":img})
        self.destroy()

# ─── ATUAÇÕES ────────────────────────
MONTHS = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
class AtuacoesModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("atuacoes.json")
        if not isinstance(self.data, dict): self.data = {"festivais_concurso":[], "festivais_convite":[], "outras":[]}
        self._build()
    def _build(self):
        self.tabs = ctk.CTkTabview(self, fg_color=BG_CARD)
        self.tabs.pack(fill="both", expand=True)
        tab_map = [("Concurso", "festivais_concurso"), ("Convite", "festivais_convite"), ("Outras", "outras")]
        for label, key in tab_map:
            self.tabs.add(label); self._tab_ui(self.tabs.tab(label), key)
    def _tab_ui(self, tab, key):
        ctk.CTkButton(tab, text="+ Nova Atuação", fg_color=DOURADO, text_color=BG_DARK, command=lambda: self._add(key, tab)).pack(pady=10)
        s = ctk.CTkScrollableFrame(tab, fg_color="transparent"); s.pack(fill="both", expand=True)
        self._render(s, key)
    def _render(self, scroll, key):
        for w in scroll.winfo_children(): w.destroy()
        items = self.data.get(key, [])
        # Ordenar cronologicamente (DD MMM YYYY)
        try:
            items.sort(key=lambda x: datetime.strptime(x['data'], '%d %b %Y'), reverse=True)
        except: pass
        for i, item in enumerate(items):
            f = ctk.CTkFrame(scroll, fg_color="#222222"); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{item['data']} — {item['titulo']}").pack(side="left", padx=10)
            ctk.CTkButton(f, text="🗑️", width=30, fg_color=DANGER, command=lambda idx=i: self._del(key, idx, scroll)).pack(side="right", padx=5)
            ctk.CTkButton(f, text="✏️", width=30, fg_color=AZUL_REAL, command=lambda idx=i: self._edit(key, idx, scroll)).pack(side="right", padx=2)
    def _add(self, key, tab):
        s = [c for c in tab.winfo_children() if isinstance(c, ctk.CTkScrollableFrame)][0]
        AtuacaoEditor(self, None, lambda a: self._save(key, a, s))
    def _edit(self, key, idx, scroll):
        AtuacaoEditor(self, self.data[key][idx], lambda a: self._save(key, a, scroll, idx))
    def _del(self, key, idx, scroll):
        self.data[key].pop(idx); save_json("atuacoes.json", self.data); self._render(scroll, key)
    def _save(self, key, a, scroll, idx=None):
        if idx is not None: self.data[key][idx] = a
        else: self.data[key].insert(0, a)
        save_json("atuacoes.json", self.data); self._render(scroll, key)

class AtuacaoEditor(ctk.CTkToplevel):
    def __init__(self, parent, item, callback):
        super().__init__(parent); self.item = item or {}; self.callback = callback
        self.geometry("500x500"); self.configure(fg_color=BG_DARK); self.grab_set(); self._build()
    def _build(self):
        pad = {"padx":20, "pady":5}
        ctk.CTkLabel(self, text="Título").pack(**pad, anchor="w")
        self.tit = ctk.CTkEntry(self, width=400); self.tit.pack(**pad); self.tit.insert(0, self.item.get("titulo",""))
        ctk.CTkLabel(self, text="Data").pack(**pad, anchor="w")
        f = ctk.CTkFrame(self, fg_color="transparent"); f.pack(fill="x", padx=20)
        d_val, m_val, y_val = "01", "JAN", "2024"
        parts = self.item.get("data","").split(" ")
        if len(parts)==3: d_val, m_val, y_val = parts[0], parts[1].upper(), parts[2]
        self.dia = ctk.CTkComboBox(f, values=[str(i).zfill(2) for i in range(1,32)], width=70); self.dia.pack(side="left", padx=2); self.dia.set(d_val)
        self.mes = ctk.CTkComboBox(f, values=MONTHS, width=80); self.mes.pack(side="left", padx=2); self.mes.set(m_val)
        self.ano = ctk.CTkEntry(f, width=80); self.ano.pack(side="left", padx=2); self.ano.insert(0, y_val)
        ctk.CTkLabel(self, text="Local").pack(**pad, anchor="w")
        self.loc = ctk.CTkEntry(self, width=400); self.loc.pack(**pad); self.loc.insert(0, self.item.get("localizacao",""))
        ctk.CTkButton(self, text="GUARDAR", fg_color=DOURADO, text_color=BG_DARK, command=self._save).pack(pady=20)
    def _save(self):
        self.callback({"titulo":self.tit.get(), "data":f"{self.dia.get()} {self.mes.get()} {self.ano.get()}", "localizacao":self.loc.get()})
        self.destroy()

# ─── LOJA ────────────────────────────
class LojaModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("loja.json")
        self._build()
    def _build(self):
        h = ctk.CTkFrame(self, fg_color="transparent"); h.pack(fill="x", pady=(0,15))
        ctk.CTkLabel(h, text="🛍️ Loja", font=("Courier New", 20, "bold"), text_color=DOURADO).pack(side="left")
        ctk.CTkButton(h, text="+ Produto", width=100, fg_color=DOURADO, text_color=BG_DARK, command=self._add).pack(side="right")
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=BG_DARK); self.scroll.pack(fill="both", expand=True)
        self._render()
    def _render(self):
        for w in self.scroll.winfo_children(): w.destroy()
        for i, p in enumerate(self.data):
            f = ctk.CTkFrame(self.scroll, fg_color=BG_CARD); f.pack(fill="x", pady=4, padx=5)
            ctk.CTkLabel(f, text=f"{p['nome']} — {p['preco']}€", font=("Courier New", 14, "bold")).pack(side="left", padx=15, pady=10)
            ctk.CTkButton(f, text="🗑️", width=30, fg_color=DANGER, command=lambda idx=i: self._del(idx)).pack(side="right", padx=5)
            ctk.CTkButton(f, text="✏️", width=30, fg_color=AZUL_REAL, command=lambda idx=i: self._edit(idx)).pack(side="right", padx=2)
    def _add(self): LojaEditor(self, None, self._on_save)
    def _edit(self, idx): LojaEditor(self, self.data[idx], lambda p: self._on_save(p, idx))
    def _del(self, idx): self.data.pop(idx); save_json("loja.json", self.data); self._render()
    def _on_save(self, p, idx=None):
        if idx is not None: self.data[idx] = p
        else: self.data.append(p)
        save_json("loja.json", self.data); self._render()

class LojaEditor(ctk.CTkToplevel):
    def __init__(self, parent, item, callback):
        super().__init__(parent); self.item = item or {}; self.callback = callback; self.img_path = self.item.get("imagem", "")
        self.geometry("450x550"); self.configure(fg_color=BG_DARK); self.grab_set(); self._build()
    def _build(self):
        pad = {"padx":20, "pady":5}
        self.nome = self._field("Nome", "nome")
        self.preco = self._field("Preço (€)", "preco")
        ctk.CTkLabel(self, text="Descrição").pack(padx=20, anchor="w")
        self.desc = ctk.CTkTextbox(self, height=80); self.desc.pack(fill="x", padx=20); self.desc.insert("1.0", self.item.get("descricao",""))
        self.img_label = ctk.CTkLabel(self, text=os.path.basename(self.img_path) or "Sem imagem"); self.img_label.pack(**pad)
        ctk.CTkButton(self, text="Escolher Imagem", command=self._pick).pack(**pad)
        ctk.CTkButton(self, text="GUARDAR", fg_color=DOURADO, text_color=BG_DARK, command=self._save).pack(pady=20)
    def _field(self, label, key):
        ctk.CTkLabel(self, text=label).pack(padx=20, anchor="w")
        e = ctk.CTkEntry(self, width=380); e.pack(padx=20, pady=5); e.insert(0, str(self.item.get(key,""))); return e
    def _pick(self):
        p = filedialog.askopenfilename(); 
        if p: self.img_path = p; self.img_label.configure(text=os.path.basename(p))
    def _save(self):
        img = self.img_path if self.img_path.startswith("assets") else copy_image(self.img_path)
        try: pr = float(self.preco.get().replace(",","."))
        except: pr = 0.0
        self.callback({"nome":self.nome.get(), "preco":pr, "descricao":self.desc.get("1.0","end-1c"), "imagem":img, "id":self.item.get("id", gen_id()), "tamanhos":["S","M","L","XL"]})
        self.destroy()

# ─── CONTACTOS ──────────────────────
class ContactosModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("contactos.json")
        self._build()
    def _build(self):
        h = ctk.CTkFrame(self, fg_color="transparent"); h.pack(fill="x", pady=(0,15))
        ctk.CTkLabel(h, text="📞 Contactos", font=("Courier New", 20, "bold"), text_color=DOURADO).pack(side="left")
        self.tabs = ctk.CTkTabview(self, fg_color=BG_CARD); self.tabs.pack(fill="both", expand=True)
        self.tabs.add("Geral"); self.tabs.add("Redes"); self.tabs.add("Dirigentes")
        self._ui_geral(self.tabs.tab("Geral"))
        self._ui_redes(self.tabs.tab("Redes"))
        self._ui_dir(self.tabs.tab("Dirigentes"))
    def _ui_geral(self, tab):
        g = self.data.get("informacoes_gerais", {})
        self.morada = self._f(tab, "Morada", g.get("morada",""))
        self.email = self._f(tab, "Email", g.get("email",""))
        self.fone = self._f(tab, "Telefone", g.get("telefone",""))
        ctk.CTkButton(tab, text="Guardar", fg_color=DOURADO, text_color=BG_DARK, command=self._save_g).pack(pady=20)
    def _ui_redes(self, tab):
        r = self.data.get("redes_sociais", {})
        self.yt = self._f(tab, "YouTube", r.get("youtube",""))
        self.ig = self._f(tab, "Instagram", r.get("instagram",""))
        self.fb = self._f(tab, "Facebook", r.get("facebook",""))
        self.li = self._f(tab, "LinkedIn", r.get("linkedin",""))
        self.sp = self._f(tab, "Spotify", r.get("spotify",""))
        ctk.CTkButton(tab, text="Guardar", fg_color=DOURADO, text_color=BG_DARK, command=self._save_r).pack(pady=20)
    def _ui_dir(self, tab):
        ctk.CTkButton(tab, text="+ Dirigente", fg_color=DOURADO, text_color=BG_DARK, command=self._add_d).pack(pady=10)
        self.ds = ctk.CTkScrollableFrame(tab, fg_color="transparent"); self.ds.pack(fill="both", expand=True)
        self._render_d()
    def _f(self, tab, l, v):
        ctk.CTkLabel(tab, text=l).pack(padx=20, anchor="w"); e = ctk.CTkEntry(tab, width=400); e.pack(padx=20, pady=5); e.insert(0, v); return e
    def _render_d(self):
        for w in self.ds.winfo_children(): w.destroy()
        for i, d in enumerate(self.data.get("dirigentes", [])):
            f = ctk.CTkFrame(self.ds, fg_color="#222222"); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{d['cargo']}: {d['nome']}").pack(side="left", padx=10)
            ctk.CTkButton(f, text="🗑️", width=30, fg_color=DANGER, command=lambda idx=i: self._del_d(idx)).pack(side="right", padx=5)
    def _save_g(self):
        self.data["informacoes_gerais"] = {"morada":self.morada.get(), "email":self.email.get(), "telefone":self.fone.get()}
        save_json("contactos.json", self.data); messagebox.showinfo("OK", "Guardado")
    def _save_r(self):
        self.data["redes_sociais"] = {"youtube":self.yt.get(), "instagram":self.ig.get(), "facebook":self.fb.get(), "linkedin":self.li.get(), "spotify":self.sp.get()}
        save_json("contactos.json", self.data); messagebox.showinfo("OK", "Guardado")
    def _add_d(self):
        n = simpledialog.askstring("Nome", "Nome:"); c = simpledialog.askstring("Cargo", "Cargo:"); t = simpledialog.askstring("Telefone", "Telefone:")
        if n and c: self.data.setdefault("dirigentes",[]).append({"nome":n, "cargo":c, "telefone":t}); save_json("contactos.json", self.data); self._render_d()
    def _del_d(self, i): self.data["dirigentes"].pop(i); save_json("contactos.json", self.data); self._render_d()

# ─── ORDENAÇÃO (LAYOUT) ────────────
class LayoutModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.data = load_json("layout.json")
        if not self.data: self.data = {"order": ["Hero", "Notícias", "História", "Traje", "Augustunos", "Reportório", "Magna Augusta", "Festa do Semina", "Atuações", "Loja", "Contactos"]}
        self._build()
    def _build(self):
        ctk.CTkLabel(self, text="🔧 Ordenação das Secções", font=("Courier New", 20, "bold"), text_color=DOURADO).pack(anchor="w", pady=(0,15))
        self.s = ctk.CTkScrollableFrame(self, fg_color=BG_DARK); self.s.pack(fill="both", expand=True)
        self._render()
        ctk.CTkButton(self, text="GUARDAR ORDENAÇÃO", fg_color=DOURADO, text_color=BG_DARK, command=self._save).pack(pady=20)
    def _render(self):
        for w in self.s.winfo_children(): w.destroy()
        for i, name in enumerate(self.data["order"]):
            f = ctk.CTkFrame(self.s, fg_color=BG_CARD, height=40); f.pack(fill="x", pady=2, padx=10); f.pack_propagate(False)
            ctk.CTkLabel(f, text=f"{i+1}. {name}").pack(side="left", padx=15)
            bf = ctk.CTkFrame(f, fg_color="transparent"); bf.pack(side="right", padx=10)
            ctk.CTkButton(bf, text="▲", width=30, command=lambda idx=i: self._move(idx, -1)).pack(side="left", padx=2)
            ctk.CTkButton(bf, text="▼", width=30, command=lambda idx=i: self._move(idx, 1)).pack(side="left", padx=2)
    def _move(self, idx, d):
        ni = idx + d
        if 0 <= ni < len(self.data["order"]):
            self.data["order"][idx], self.data["order"][ni] = self.data["order"][ni], self.data["order"][idx]
            self._render()
    def _save(self): save_json("layout.json", self.data); messagebox.showinfo("OK", "Ordenação guardada")

if __name__ == "__main__":
    app = AdminHub(); app.mainloop()
