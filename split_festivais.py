import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Navigation Dropdowns
nav_find = """          <div class="nav-dropdown-menu">
            <a href="#" data-page="festivais">Festivais de Tunas</a>
            <a href="#" data-page="outras-atuacoes">Outras Atuações</a>
          </div>"""
nav_replace = """          <div class="nav-dropdown-menu">
            <a href="#" data-page="festivais-concurso">Festivais a concurso</a>
            <a href="#" data-page="festivais-convite">Festivais a convite</a>
            <a href="#" data-page="outras-atuacoes">Outras Atuações</a>
          </div>"""
html = html.replace(nav_find, nav_replace)

mobile_find = """      <div class="nav-bottom-menu" id="menuAtuacoes">
        <a href="#" data-page="festivais">Festivais</a>
        <a href="#" data-page="outras-atuacoes">Outras Atuações</a>
      </div>"""
mobile_replace = """      <div class="nav-bottom-menu" id="menuAtuacoes">
        <a href="#" data-page="festivais-concurso">Festivais a concurso</a>
        <a href="#" data-page="festivais-convite">Festivais a convite</a>
        <a href="#" data-page="outras-atuacoes">Outras Atuações</a>
      </div>"""
html = html.replace(mobile_find, mobile_replace)

# 2. Split Festivais into Festivais a Concurso and Festivais a Convite
festivais_concurso_html = """
  <section class="page-section" id="page-festivais-concurso">
    <div class="page-hero-mini section-dark">
      <span class="section-label">Atuações</span>
      <h2 class="section-title">Festivais a <span class="text-gold">Concurso</span></h2>
      <p class="section-subtitle">As nossas conquistas pelos palcos do país</p>
    </div>

    <div class="section-dark-alt section-padding">
      <div class="container">
        <div class="performances-list stagger-children">
          <h3 class="performance-year-divider">2025</h3>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">24</div>
              <div class="performance-month">Out</div>
            </div>
            <div class="performance-info">
              <h4>V Incognifest</h4>
              <p>Prémios: Melhor instrumental, Melhor pandeireta</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Vila Nova de Famalicão
            </div>
          </div>
          <h3 class="performance-year-divider" style="margin-top: 1.5rem;">2024</h3>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">22</div>
              <div class="performance-month">Mar</div>
            </div>
            <div class="performance-info">
              <h4>XIII Bagatunaço</h4>
              <p>Prémios: Melhor original, Tuna mais tuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Rio Maior
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="page-section" id="page-festivais-convite">
    <div class="page-hero-mini section-dark">
      <span class="section-label">Atuações</span>
      <h2 class="section-title">Festivais a <span class="text-gold">Convite</span></h2>
      <p class="section-subtitle">As nossas participações especiais em festivais e encontros</p>
    </div>

    <div class="section-dark-alt section-padding">
      <div class="container">
        <div class="performances-list stagger-children">
          <h3 class="performance-year-divider">2026</h3>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">22</div>
              <div class="performance-month">Mar</div>
            </div>
            <div class="performance-info">
              <h4>IX Magna Augusta</h4>
              <p>O nosso festival — a edição dos 30 anos com tunas convidadas de 5 países</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Theatro Circo, Braga
            </div>
          </div>
          <h3 class="performance-year-divider" style="margin-top: 1.5rem;">2025</h3>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">03</div>
              <div class="performance-month">Mai</div>
            </div>
            <div class="performance-info">
              <h4>XXV FITAB</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <h3 class="performance-year-divider" style="margin-top: 1.5rem;">2024</h3>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">20</div>
              <div class="performance-month">Mai</div>
            </div>
            <div class="performance-info">
              <h4>Festival de Tunas do Porto</h4>
              <p>Encontro anual das tunas do norte de Portugal</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Coliseu do Porto
            </div>
          </div>
          <h3 class="performance-year-divider" style="margin-top: 1.5rem;">2023</h3>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">18</div>
              <div class="performance-month">Nov</div>
            </div>
            <div class="performance-info">
              <h4>XI Scientiphicvs</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">03</div>
              <div class="performance-month">Nov</div>
            </div>
            <div class="performance-info">
              <h4>I Vivências</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">02</div>
              <div class="performance-month">Jun</div>
            </div>
            <div class="performance-info">
              <h4>VIII AvenTUNATe</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">30</div>
              <div class="performance-month">Abr</div>
            </div>
            <div class="performance-info">
              <h4>Estudantino '23</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">15</div>
              <div class="performance-month">Abr</div>
            </div>
            <div class="performance-info">
              <h4>XXIV Real FesTA</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <h3 class="performance-year-divider" style="margin-top: 1.5rem;">2022</h3>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">12</div>
              <div class="performance-month">Nov</div>
            </div>
            <div class="performance-info">
              <h4>X In'Vinus Veritas</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">22</div>
              <div class="performance-month">Out</div>
            </div>
            <div class="performance-info">
              <h4>II Tunacel</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">01</div>
              <div class="performance-month">Jul</div>
            </div>
            <div class="performance-info">
              <h4>Festival de Aldeia de Lobos</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">28</div>
              <div class="performance-month">Mai</div>
            </div>
            <div class="performance-info">
              <h4>XVII FITAM</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">07</div>
              <div class="performance-month">Mai</div>
            </div>
            <div class="performance-info">
              <h4>XXIII Real Festa</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <h3 class="performance-year-divider" style="margin-top: 1.5rem;">2020</h3>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">--</div>
              <div class="performance-month">---</div>
            </div>
            <div class="performance-info">
              <h4>XI Collipo</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <h3 class="performance-year-divider" style="margin-top: 1.5rem;">2019</h3>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">07</div>
              <div class="performance-month">Jun</div>
            </div>
            <div class="performance-info">
              <h4>XII FeITunas - Festival de Tunas "Cidade de Felgueiras"</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
          <div class="performance-item">
            <div class="performance-date">
              <div class="performance-day">01</div>
              <div class="performance-month">Jun</div>
            </div>
            <div class="performance-info">
              <h4>FITAM XVI</h4>
              <p>Atuação da Augustuna</p>
            </div>
            <div class="performance-location">
              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>
              Portugal
            </div>
          </div>
        </div>
      </div>
    </div>
"""

festivais_section_regex = r'<section class="page-section" id="page-festivais">.*?</section>'
html = re.sub(festivais_section_regex, festivais_concurso_html, html, flags=re.DOTALL)

# 3. Fix recruit section (Animação de Festas)
recruit_find = """            <div class="recruit-card">
              <div class="recruit-card-icon"><i data-lucide="music"
                  style="width:32px;height:32px;color:var(--dourado);"></i></div>
              <h4>Casamentos & Festas</h4>
              <p>Animação musical para tornar o teu evento inesquecível</p>
            </div>
            <div class="recruit-card">
              <div class="recruit-card-icon"><i data-lucide="building"
                  style="width:32px;height:32px;color:var(--dourado);"></i></div>
              <h4>Eventos Corporativos</h4>
              <p>Entretenimento cultural para empresas e organizações</p>
            </div>
            <div class="recruit-card">
              <div class="recruit-card-icon"><i data-lucide="party-popper"
                  style="width:32px;height:32px;color:var(--dourado);"></i></div>
              <h4>Festivais & Concertos</h4>
              <p>Participação em festivais de tunas e eventos musicais</p>
            </div>"""

recruit_replace = """            <div class="recruit-card" style="display:flex; flex-direction:column; align-items:flex-start; text-align:left;">
              <div class="recruit-card-icon"><i data-lucide="music"
                  style="width:32px;height:32px;color:var(--dourado);"></i></div>
              <h4 style="white-space:nowrap;">Animação de Festas</h4>
              <p>Animação musical para tornar o teu evento inesquecível</p>
            </div>
            <div class="recruit-card" style="display:flex; flex-direction:column; align-items:flex-start; text-align:left;">
              <div class="recruit-card-icon"><i data-lucide="building"
                  style="width:32px;height:32px;color:var(--dourado);"></i></div>
              <h4 style="white-space:nowrap;">Eventos Corporativos</h4>
              <p>Entretenimento cultural para empresas e organizações</p>
            </div>
            <div class="recruit-card" style="display:flex; flex-direction:column; align-items:flex-start; text-align:left;">
              <div class="recruit-card-icon"><i data-lucide="party-popper"
                  style="width:32px;height:32px;color:var(--dourado);"></i></div>
              <h4 style="white-space:nowrap;">Festivais</h4>
              <p>Participação em festivais de tunas e eventos musicais</p>
            </div>"""
html = html.replace(recruit_find, recruit_replace)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make buttons same color and border radius
css = css.replace("border-radius: 0.5rem;", "border-radius: 3rem;")

btn_secondary_find = """.btn-secondary {
  border: 2px solid var(--dourado);
  color: var(--dourado);
  background: transparent;
}"""
btn_secondary_replace = """.btn-secondary {
  background: linear-gradient(135deg, var(--dourado), var(--dourado-brilho));
  color: var(--azul-profundo);
  box-shadow: var(--shadow-gold);
  border: none;
}"""
css = css.replace(btn_secondary_find, btn_secondary_replace)

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Done")
