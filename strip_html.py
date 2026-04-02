import re
import os

repo_dir = r"c:\Users\José Cunha\Desktop\AG"
index_file = os.path.join(repo_dir, "index.html")

with open(index_file, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Notícias: replace content inside <div class="news-grid-v2 stagger-children">...</div>
news_grid_start = html.find('<div class="news-grid-v2 stagger-children">')
if news_grid_start != -1:
    # Find the closing div for news-grid-v2. We'll add an ID to the news-grid-v2
    # It has a few cards inside. We'll use regex to clear it but we need to match it.
    html = re.sub(
        r'(<div class="news-grid-v2 stagger-children"[^>]*>).*?(</section>)',
        r'\g<1>\n          <!-- Dinamicamente preenchido pelo script.js -->\n        </div>\n      </div>\n    \g<2>',
        html,
        flags=re.DOTALL
    )
    # Give it an ID: newsContent
    html = html.replace('<div class="news-grid-v2 stagger-children">', '<div class="news-grid-v2 stagger-children" id="newsContent">')

# 2. Magna Augusta: replace content inside <section id="page-magna-augusta"> ...
html = re.sub(
    r'(<section class="page-section"\s+id="page-magna-augusta">.*?</p>\s*</div>\s*</div>\s*<div class="container section-padding">).*?(</section>)',
    r'\1\n      <div id="magnaAugustaContent" class="stagger-children">\n        <!-- Dinamicamente preenchido pelo script.js -->\n      </div>\n    </div>\n  \2',
    html,
    flags=re.DOTALL
)

# 3. Festa do Semina: replace content inside <section id="page-festa-semina"> ...
html = re.sub(
    r'(<section class="page-section"\s+id="page-festa-semina">.*?</p>\s*</div>\s*</div>\s*<div class="container section-padding">).*?(</section>)',
    r'\1\n      <div id="festaSeminaContent" class="stagger-children">\n        <!-- Dinamicamente preenchido pelo script.js -->\n      </div>\n    </div>\n  \2',
    html,
    flags=re.DOTALL
)

# 4. Atuações: Concurso
html = re.sub(
    r'(<section class="page-section"\s+id="page-festivais-concurso">.*?</p>\s*</div>\s*</div>\s*<div class="container section-padding">).*?(</section>)',
    r'\1\n      <div id="concursoContent" class="performance-list stagger-children">\n        <!-- Dinamicamente preenchido pelo script.js -->\n      </div>\n    </div>\n  \2',
    html,
    flags=re.DOTALL
)

# 5. Atuações: Convite
html = re.sub(
    r'(<section class="page-section"\s+id="page-festivais-convite">.*?</p>\s*</div>\s*</div>\s*<div class="container section-padding">).*?(</section>)',
    r'\1\n      <div id="conviteContent" class="performance-list stagger-children">\n        <!-- Dinamicamente preenchido pelo script.js -->\n      </div>\n    </div>\n  \2',
    html,
    flags=re.DOTALL
)

# 6. Atuações: Outras
html = re.sub(
    r'(<section class="page-section"\s+id="page-outras-atuacoes">.*?</p>\s*</div>\s*</div>\s*<div class="container section-padding">).*?(</section>)',
    r'\1\n      <div id="outrasContent" class="performance-list stagger-children">\n        <!-- Dinamicamente preenchido pelo script.js -->\n      </div>\n    </div>\n  \2',
    html,
    flags=re.DOTALL
)

# 7. Loja: Marketplace
html = re.sub(
    r'(<section class="page-section"\s+id="page-marketplace">.*?<div class="shop-grid">).*?(</section>)',
    r'\1\n          <!-- Dinamicamente preenchido pelo script.js -->\n        </div>\n      </div>\n    </div>\n  \2',
    html,
    flags=re.DOTALL
)
html = html.replace('<div class="shop-grid">', '<div class="shop-grid" id="lojaContent">')

with open(index_file, "w", encoding="utf-8") as f:
    f.write(html)
print("index.html atualizado!")
