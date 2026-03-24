import re
import json

# Fix Social Icons in HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

youtube_icon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg>'

instagram_icon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>'

facebook_icon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>'

linkedin_icon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>'

html = re.sub(r'<i\s+data-lucide="youtube"\s+style=".*?"></i>', youtube_icon, html)
html = re.sub(r'<i\s+data-lucide="instagram"\s+style=".*?"></i>', instagram_icon, html)
html = re.sub(r'<i\s+data-lucide="facebook"\s+style=".*?"></i>', facebook_icon, html)
html = re.sub(r'<i\s+data-lucide="linkedin"\s+style=".*?"></i>', linkedin_icon, html)

# Fix missing styles or layout issues? All good.
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Icons fixed!")

# Extract Members Data and append to NOTION_EXPORT.md
try:
    with open('script.js', 'r', encoding='utf-8') as f:
        js = f.read()
    
    match = re.search(r'const MEMBERS_DATA = \[(.*?)\];', js, re.DOTALL)
    if match:
        members_text = match.group(1)
        # We can extract the items loosely
        items = re.findall(r'\{.*?name:\s*[\'"](.*?)[\'"].*?role:\s*[\'"](.*?)[\'"].*?instrument:\s*[\'"](.*?)[\'"].*?generation:\s*(\d+).*?\}', members_text, re.DOTALL)
        
        md_members = "\n## 👥 Listagem de Tunos (Membros)\n\n"
        md_members += "| Nome Académico | Função | Instrumento | Geração |\n"
        md_members += "|---|---|---|---|\n"
        for name, role, instr, gen in items:
            md_members += f"| {name} | {role} | {instr} | {gen} |\n"
        
        with open('NOTION_EXPORT.md', 'a', encoding='utf-8') as f:
            f.write(md_members)
        print("Members appended to NOTION_EXPORT.md")
    else:
        print("Members JS object not found.")

except Exception as e:
    print(f"Error extracting members: {e}")
