import os

filepath = r"c:\Users\José Cunha\Desktop\AG\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_until = -1
for i, line in enumerate(lines):
    if i < skip_until:
        continue
    
    if i == 587: 
        new_lines.append('        <div class="container tab-group" id="magnaAugustaContent"></div>\n')
        skip_until = 745
        continue
    if i == 758:
        new_lines.append('        <div class="container tab-group" id="festaSeminaContent"></div>\n')
        skip_until = 802
        continue
    if i == 818:
        new_lines.append('        <div class="performances-list stagger-children" id="concursoContent"></div>\n')
        skip_until = 850
        continue
    if i == 863:
        new_lines.append('        <div class="performances-list stagger-children" id="conviteContent"></div>\n')
        skip_until = 1096
        continue
    if i == 1112:
        new_lines.append('        <div class="performances-list stagger-children" id="outrasContent"></div>\n')
        skip_until = 2102
        continue
    if i == 2119:
        new_lines.append('        <div class="shop-grid stagger-children" id="lojaContent"></div>\n')
        skip_until = 2212
        continue
    if i == 2319:
        new_lines.append('          <div class="social-links-grid" id="socialLinksContent"></div>\n')
        skip_until = 2372
        continue
    if i == 2402:
        new_lines.append('              <div class="personal-contacts-grid" id="dirigentesContent"></div>\n')
        skip_until = 2473
        continue
    if i == 2476:
        new_lines.append('          <div class="contact-info-section reveal-right" id="infogeraisContent"></div>\n')
        skip_until = 2505
        continue

    new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Replacement completed!")
