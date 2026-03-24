import codecs

# 1. Update index.html
with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# Hero Buttons
html = html.replace(
    '<div class="hero-actions">\n          <a href="#" class="btn btn-primary" data-page="contrata-nos">\n            JUNTA-TE A NÓS\n          </a>\n          <a href="#" class="btn btn-secondary" data-page="formacao">\n            DESCOBRE A AUGUSTUNA\n          </a>\n        </div>',
    '<div class="hero-actions" style="justify-content: center; flex-wrap: wrap; gap: 1rem;">\n          <a href="#" class="btn btn-primary" data-page="contrata-nos" style="min-width: 280px; text-align: center; justify-content: center;">\n            JUNTA-TE A NÓS\n          </a>\n          <a href="#" class="btn btn-secondary" data-page="formacao" style="min-width: 280px; text-align: center; justify-content: center;">\n            DESCOBRE A AUGUSTUNA\n          </a>\n        </div>'
)

# Email Address in Contactos
html = html.replace('placeholder="tunos@augustuna.pt"', 'placeholder="augustunataum@gmail.com"')

# Book Now to Agende Já
html = html.replace('<span class="section-label">Book Now</span>', '<span class="section-label">Agende Já</span>')

# Contacta-nos Button
html = html.replace(
    '<a href="#" class="btn btn-primary" data-page="contactos">\n              <i data-lucide="music" style="width:18px;height:18px;"></i>\n              Contacta-nos\n            </a>',
    '<a href="#" class="btn btn-primary" data-page="contactos" style="justify-content:center;">\n              Contacta-nos\n            </a>'
)

# Social Media Links
html = html.replace('href="https://www.youtube.com/@augustuna"', 'href="https://www.youtube.com/@AugustunaTAUM"')
html = html.replace('href="https://www.facebook.com/augustuna"', 'href="https://www.facebook.com/Augustuna96"')
html = html.replace('href="https://www.linkedin.com/company/augustuna/"', 'href="https://www.linkedin.com/company/augustunataum"')
html = html.replace('href="https://open.spotify.com/artist/3CFxMDWwHFbqbCTqsAanWE"', 'href="https://open.spotify.com/intl-pt/artist/0kFalW9M0bBIOxvUwNgB6c?si=J9BuLWERTXKAGSnQzaa8vw"')

# Footer Support Links
html = html.replace(
    '<img src="logotipos/UM LOGO.png" alt="Universidade do Minho"',
    '<a href="https://www.uminho.pt" target="_blank" rel="noopener noreferrer"><img src="logotipos/UM LOGO.png" alt="Universidade do Minho"'
)
html = html.replace(
    '<img src="logotipos/AAUM LOGO.png" alt="AAUM"',
    '<a href="https://www.aaum.pt" target="_blank" rel="noopener noreferrer"><img src="logotipos/AAUM LOGO.png" alt="AAUM"'
)
html = html.replace(
    '<img src="logotipos/CAMARA BRAGA LOGO.png" alt="Câmara Municipal de Braga"',
    '<a href="https://www.cm-braga.pt" target="_blank" rel="noopener noreferrer"><img src="logotipos/CAMARA BRAGA LOGO.png" alt="Câmara Municipal de Braga"'
)
html = html.replace(
    '<img src="logotipos/BRAGA PARQUE LOGO.png" alt="Braga Parque"',
    '<a href="https://www.bragaparque.pt" target="_blank" rel="noopener noreferrer"><img src="logotipos/BRAGA PARQUE LOGO.png" alt="Braga Parque"'
)
html = html.replace(
    '<img src="logotipos/IPDJ LOGO.png" alt="IPDJ"',
    '<a href="https://ipdj.gov.pt" target="_blank" rel="noopener noreferrer"><img src="logotipos/IPDJ LOGO.png" alt="IPDJ"'
)

# Close the a tags safely
html = html.replace('opacity(0.8);">\n          </div>', 'opacity(0.8);"></a>\n          </div>')

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)


# 2. Update styles.css
with codecs.open('styles.css', 'r', 'utf-8') as f:
    css = f.read()

# History Stats Background
css = css.replace(
""".about-stats {
  display: flex;
  justify-content: center;
  gap: 4rem;
  margin-bottom: 4rem;
  padding: 2.5rem;
  border-radius: 1rem;
  background: rgba(27, 58, 92, 0.2);
  border: 1px solid rgba(201, 168, 76, 0.1);
}""", 
""".about-stats {
  display: flex;
  justify-content: center;
  gap: 4rem;
  margin-bottom: 4rem;
}""")

with codecs.open('styles.css', 'w', 'utf-8') as f:
    f.write(css)

print("UI fixes applied successfully.")
