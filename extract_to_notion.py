import re
import os
import zipfile
import xml.etree.ElementTree as ET

def get_docx_text(path):
    try:
        if not os.path.exists(path): return ""
        document = zipfile.ZipFile(path)
        xml_content = document.read('word/document.xml')
        document.close()
        tree = ET.XML(xml_content)
        paragraphs = []
        for paragraph in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            texts = [node.text for node in paragraph.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
            if texts:
                paragraphs.append("".join(texts))
        return "\n\n".join(paragraphs)
    except:
        return ""

def extract_content(html_file):
    if not os.path.exists(html_file): return
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    md = "# 🎵 Augustuna — Base de Dados & Conteúdo\n\n"
    md += "Este documento centraliza toda a informação do projeto Augustuna para importação direta no Notion.\n\n"

    # --- SITEMAP ---
    nav_match = re.search(r'<div class="nav-links".*?>(.*?)</div>', html, re.DOTALL)
    if nav_match:
        links = re.findall(r'data-page="(.*?)".*?>(.*?)</a>', nav_match.group(1))
        md += "## 📂 Estrutura do Site (Sitemap)\n"
        for page_id, page_name in links:
            md += f"- **{page_name.strip()}** (`#page-{page_id}`)\n"
        md += "\n"

    # --- SECTIONS ---
    sections = re.findall(r'<section class="page-section" id="(.*?)">(.*?)</section>', html, re.DOTALL)
    for sec_id, sec_content in sections:
        title_match = re.search(r'<h2 class="section-title">(.*?)</h2>', sec_content, re.DOTALL)
        name = re.sub(r'<.*?>', '', title_match.group(1)).strip() if title_match else sec_id
        
        md += f"## 📍 {name}\n"
        
        # Performances
        if "performances-list" in sec_content:
            years = re.findall(r'<h3 class="performance-year-divider".*?>(.*?)</h3>(.*?)(?=<h3|</div>\s*</div>\s*</section>|<!--)', sec_content, re.DOTALL)
            for year, year_content in years:
                year = year.strip()
                md += f"\n#### Ano: {year}\n"
                items = re.findall(r'<div class="performance-item">(.*?)</div>\s*</div>', year_content, re.DOTALL)
                for item in items:
                    d_m = re.search(r'<div class="performance-day">(.*?)</div>.*?<div class="performance-month">(.*?)</div>', item, re.DOTALL)
                    if d_m:
                        day, month = d_m.groups()
                        p_t_m = re.search(r'<h4>(.*?)</h4>', item)
                        p_title = p_t_m.group(1) if p_t_m else "Sem Título"
                        p_d_m = re.search(r'<p>(.*?)</p>', item)
                        p_desc = p_d_m.group(1) if p_d_m else ""
                        l_m = re.search(r'class="performance-location".*?>(.*?)</div>', item, re.DOTALL)
                        loc = re.sub(r'<.*?>', '', l_m.group(1)).strip() if l_m else ""
                        md += f"- **{day}/{month}/{year}**: {p_title} — *{p_desc}* ({loc})\n"
            md += "\n"
        
        # News
        elif "news-grid" in sec_content:
            news = re.findall(r'<div class="news-card".*?>(.*?)</div>\s*</div>', sec_content, re.DOTALL)
            for n in news:
                t_m = re.search(r'<h3>(.*?)</h3>', n)
                tag_m = re.search(r'<span class="news-tag">(.*?)</span>', n)
                if t_m:
                    md += f"- [{tag_m.group(1) if tag_m else 'INFO'}] **{t_m.group(1)}**\n"
            md += "\n"

    # --- CONTACTS EXACT DATA ---
    contact_grid = re.search(r'id="page-contactos".*?<div class="contact-grid">(.*?)</div>', html, re.DOTALL)
    if contact_grid:
        md += "## 📞 Contactos Oficiais\n"
        cards = re.findall(r'<div class="contact-card".*?>.*?<h4>(.*?)</h4>.*?<p>(.*?)</p>', contact_grid.group(1), re.DOTALL)
        for c_title, c_val in cards:
            md += f"- **{c_title}**: {c_val}\n"
        md += "\n"

    # --- HISTORY / LOG DATA ---
    docx_text = get_docx_text('log.docx')
    if docx_text:
        md += "## 📜 Histórico Adicional & Playlists (Arquivo Discord/Docx)\n"
        md += docx_text + "\n\n"

    with open('NOTION_EXPORT.md', 'w', encoding='utf-8') as f:
        f.write(md)
    print("Export complete: NOTION_EXPORT.md")

if __name__ == "__main__":
    extract_content('index.html')
