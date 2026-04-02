"""
Extract all website content from index.html and script.js into JSON data files.
Run once to populate the data/ folder for the Admin Hub.
"""
import re, json, os
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(REPO, "data")
os.makedirs(DATA, exist_ok=True)

# ── 1. MEMBERS (from script.js MEMBERS_DATA) ──────────────────
def extract_members():
    with open(os.path.join(REPO, "script.js"), "r", encoding="utf-8") as f:
        js = f.read()
    
    # Find the MEMBERS_DATA array
    match = re.search(r'const MEMBERS_DATA\s*=\s*\[(.*?)\];', js, re.DOTALL)
    if not match:
        print("MEMBERS_DATA not found!")
        return
    
    block = match.group(1)
    # Parse each object
    members = []
    for m in re.finditer(r'\{(.*?)\}', block, re.DOTALL):
        obj = {}
        for kv in re.finditer(r'(\w+)\s*:\s*"([^"]*)"', m.group(1)):
            obj[kv.group(1)] = kv.group(2)
        if obj:
            members.append(obj)
    
    # Group by geracao
    gen_order = []
    gen_map = {}
    for m in members:
        g = m.get("geracao", "Desconhecida")
        if g not in gen_map:
            gen_order.append(g)
            gen_map[g] = []
        gen_map[g].append({
            "nome": m.get("name", ""),
            "alcunha": m.get("alcunha", ""),
            "instrumento": m.get("instrumento", ""),
            "curso": m.get("curso", ""),
            "data_passagem": m.get("data", ""),
            "evento": m.get("evento", ""),
        })
    
    data = {"geracoes": [{"nome": g, "elementos": gen_map[g]} for g in gen_order]}
    save(data, "membros.json")
    total = sum(len(gen_map[g]) for g in gen_map)
    print(f"  Membros: {total} membros em {len(gen_order)} gerações")

# ── 2. NEWS (hardcoded in HTML) ────────────────────────────────
def extract_news():
    news = [
        {
            "id": "n001",
            "data": "15 Mar 2026",
            "titulo": "IX Magna Augusta — 30 Anos de Augustuna",
            "corpo": "A Augustuna celebra três décadas de tradição e boémia com o IX Magna Augusta, o seu festival internacional de tunas académicas nos dias 14 e 15 de Março no Theatro Circo, em Braga.",
            "imagem": "Logo oficial 2.png",
            "categoria": "destaque"
        },
        {
            "id": "n002",
            "data": "Set 2025",
            "titulo": "Recrutamento 2025/2026 — Junta-te à Família",
            "corpo": "Novo ano letivo, nova oportunidade! A Augustuna abre portas a todos os estudantes da UMinho que queiram viver a tradição tunante. Não precisas de saber tocar — basta vontade!",
            "imagem": "",
            "categoria": "recrutamento"
        },
        {
            "id": "n003",
            "data": "Mai 2024",
            "titulo": "XXVII Galardões \"A Nossa Terra\"",
            "corpo": "A Augustuna atuou nos XXVII Galardões \"A Nossa Terra\", um evento de referência na região minhota que homenageia personalidades e projetos de destaque.",
            "imagem": "",
            "categoria": "premio"
        },
        {
            "id": "n004",
            "data": "Dez 2025",
            "titulo": "Serenata de Natal — Braga",
            "corpo": "Tradição anual da Augustuna: uma noite de serenatas pelas ruas do centro histórico de Braga, levando a música académica aos bracarenses na época natalícia.",
            "imagem": "",
            "categoria": "cultura"
        }
    ]
    save(news, "noticias.json")
    print(f"  Notícias: {len(news)} itens")

# ── 3. MAGNA AUGUSTA + FESTA DO SEMINA (eventos.json) ─────────
def extract_eventos():
    magna = [
        {"edicao": "IX", "ano": 2026, "descricao": "O Magna Augusta é o festival oficial de Tunas Académicas organizado pela Augustuna, reunindo tunas de todo o mundo numa celebração da música académica. A próxima edição — IX Magna Augusta — promete ser a maior de sempre, com a participação de tunas de Portugal, Espanha, Itália e América Latina.", "imagem": "logo magna.jpeg"},
        {"edicao": "VIII", "ano": 2024, "descricao": "Uma edição memorável que encheu o Theatro Circo de melodias e vivências académicas inesquecíveis.", "imagem": ""},
        {"edicao": "VII", "ano": 2022, "descricao": "Mais um grande festival que marcou a cidade de Braga com a presença de tunas de excelência.", "imagem": ""},
        {"edicao": "VI", "ano": 2020, "descricao": "Uma noite de enorme partilha musical, de prémios renhidos e serenatas encantadoras pelo centro de Braga.", "imagem": ""},
        {"edicao": "V", "ano": 2018, "descricao": "Quinta edição do nosso festival, já firmado como um dos momentos altos da academia Minhota.", "imagem": ""},
        {"edicao": "IV", "ano": 2016, "descricao": "Edição que solidificou o formato internacional e a vasta procura de bilhetes por parte dos estudantes e da cidade.", "imagem": ""},
        {"edicao": "III", "ano": 2014, "descricao": "Terceira edição, repleta de clássicos do cancioneiro português reinventados.", "imagem": ""},
        {"edicao": "II", "ano": 2012, "descricao": "O festival começa a ganhar o seu espaço de renome no calendário nacional de tunas.", "imagem": ""},
        {"edicao": "I", "ano": 2010, "descricao": "A primeira e mítica edição do Magna Augusta. O início de uma tradição que dita o rumo da Augustuna e da sua música.", "imagem": ""},
    ]
    festa = [
        {"edicao": "2025", "ano": 2025, "descricao": "A Festa do Semina é um evento totalmente organizado pelos caloiros da Augustuna. A edição de 2025 celebrou-se a 8 de Outubro no Largo dos Peões. Contou com atuações musicais eletrizantes, excelentes comes e bebes e o genuíno espírito de academia que une as gerações.", "imagem": ""},
        {"edicao": "Anteriores", "ano": 0, "descricao": "A tradição da Festa do Semina mantém-se viva ano após ano. É o momento onde cada nova geração de caloiros deixa a sua marca irreverente e demonstra a sua união e valor à Tuna.", "imagem": ""},
    ]
    save({"magna_augusta": magna, "festa_semina": festa}, "eventos.json")
    print(f"  Eventos: {len(magna)} Magna Augusta + {len(festa)} Festa do Semina")

# ── 4. ATUAÇÕES (from HTML performance items) ──────────────────
def extract_performances(html):
    """Parse performance-item blocks from a section of HTML."""
    results = []
    # Find all performance-item blocks
    items = re.findall(
        r'<div class="performance-day">(.*?)</div>\s*'
        r'<div class="performance-month">(.*?)</div>.*?'
        r'<h4>(.*?)</h4>\s*<p>(.*?)</p>.*?'
        r'map-pin.*?</i>\s*(.*?)\s*</div>',
        html, re.DOTALL
    )
    # Also track year dividers
    years = re.findall(r'performance-year-divider[^>]*>(\d{4})', html)
    
    # Parse year assignment by position
    # Find positions of year dividers and items
    year_positions = [(m.start(), m.group(1)) for m in re.finditer(r'performance-year-divider[^>]*>(\d{4})', html)]
    item_positions = [(m.start(),) + m.groups() for m in re.finditer(
        r'<div class="performance-day">(.*?)</div>\s*'
        r'<div class="performance-month">(.*?)</div>.*?'
        r'<h4>(.*?)</h4>\s*<p>(.*?)</p>.*?'
        r'map-pin.*?</i>\s*(.*?)\s*</div>',
        html, re.DOTALL
    )]
    
    current_year = ""
    all_events = sorted(
        [("year", pos, yr) for pos, yr in year_positions] +
        [("item", pos, day, month, title, desc, loc) for pos, day, month, title, desc, loc in item_positions],
        key=lambda x: x[1]
    )
    
    for ev in all_events:
        if ev[0] == "year":
            current_year = ev[2]
        elif ev[0] == "item":
            _, _, day, month, title, desc, loc = ev
            day = day.strip()
            month = month.strip()
            data_str = f"{day} {month} {current_year}" if day != "--" else current_year
            results.append({
                "id": f"a{len(results):03d}",
                "data": data_str,
                "titulo": title.strip(),
                "descricao": desc.strip(),
                "localizacao": loc.strip()
            })
    return results

def extract_atuacoes():
    with open(os.path.join(REPO, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()
    
    # Extract Festivais a Concurso (page-festivais-concurso section)
    concurso_match = re.search(r'id="page-festivais-concurso">(.*?)</section>', html, re.DOTALL)
    concurso = extract_performances(concurso_match.group(1)) if concurso_match else []
    
    # Extract Festivais a Convite (page-festivais-convite section)
    convite_match = re.search(r'id="page-festivais-convite">(.*?)</section>', html, re.DOTALL)
    convite = extract_performances(convite_match.group(1)) if convite_match else []
    
    # Extract Outras Atuações (page-outras-atuacoes section)
    outras_match = re.search(r'id="page-outras-atuacoes">(.*?)</section>', html, re.DOTALL)
    outras = extract_performances(outras_match.group(1)) if outras_match else []
    
    save({
        "festivais_concurso": concurso,
        "festivais_convite": convite,
        "outras": outras
    }, "atuacoes.json")
    print(f"  Atuações: {len(concurso)} concurso + {len(convite)} convite + {len(outras)} outras")

# ── 5. LOJA (from HTML shop cards) ─────────────────────────────
def extract_loja():
    with open(os.path.join(REPO, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()
    
    products = []
    # Find shop cards with data attributes
    for m in re.finditer(
        r'data-product-id="([^"]*)"[^>]*'
        r'data-product-name="([^"]*)"[^>]*'
        r'data-product-price="([^"]*)"',
        html
    ):
        pid, name, price = m.groups()
        # Try to find sizes nearby
        # Look for the card's section to find size-select options
        card_start = m.start()
        card_end = html.find('</div>\n', card_start + 500)
        card_html = html[card_start:card_end+200] if card_end > 0 else ""
        sizes = re.findall(r'<option value="([^"]+)"', card_html)
        
        products.append({
            "id": pid,
            "nome": name,
            "preco": float(price),
            "descricao": "",
            "imagem": "",
            "tamanhos": sizes if sizes else []
        })
    
    # If no products found from data attributes, try alternate pattern
    if not products:
        # Try finding shop section and extract manually
        shop_match = re.search(r'shop-card|product-card', html)
        if shop_match:
            print("  Loja: Found shop cards but couldn't parse data attributes")
        else:
            # Check for inline product data
            for m in re.finditer(r'productId.*?productName.*?productPrice', html):
                print(f"  Found product data at position {m.start()}")
    
    save(products, "loja.json")
    print(f"  Loja: {len(products)} produtos")

def save(data, filename):
    path = os.path.join(DATA, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print("Extraindo conteúdo do website...")
    extract_members()
    extract_news()
    extract_eventos()
    extract_atuacoes()
    extract_loja()
    print("\n✓ Dados extraídos com sucesso para data/")
