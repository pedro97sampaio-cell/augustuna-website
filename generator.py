import sys

festivais_raw = """
2019.06.01 - FITAM XVI
2019.06.07 - XII FeITunas - Festival de Tunas "Cidade de Felgueiras"
2020.00.00 - XI Collipo
2022.05.07 - XXIII Real Festa
2022.05.28 - XVII FITAM
2022.07.01 - Festival de Aldeia de Lobos
2022.10.22 - II Tunacel
2022.11.12 - X In'Vinus Veritas
2023.04.15 - XXIV Real FesTA
2023.04.30 - Estudantino '23
2023.06.02 - VIII AvenTUNATe
2023.11.03 - I Vivências
2023.11.18 - XI Scientiphicvs
2025.05.03 - XXV FITAB
"""

outras_raw = """
2019.06.05 - Projecto Sementes
2019.06.15 - Casamento
2019.06.17 - UM Vai ao S.João
2019.06.19 - Bodas de Prata
2019.06.28 - Aniversário Rick Universal 9 anos
2019.09.09 - Acolhimento
2019.09.19 - Sarau Cultural
2019.09.25 - Jantar do Caloiro
2019.10.02 - Receção ao Caloiro '19
2019.10.09 - Jantar Mãe do Pito
2019.11.20 - VII Salsichão
2019.12.01 - 1º de Dezembro
2019.12.11 - Serenata Escondidinhas
2019.12.13 - Festa de Natal Rick
2019.12.20 - Festa de Natal Fraião
2019.00.00 - Nespereira
2020.02.08 - Atuação Rua [Braga]
2020.02.23 - Atuação S.C.Braga
2020.12.22 - Demonstração CEAP
2021.04.10 - Gravações Braga Boémia
2021.09.11 - Atuação Rua [Porto]
2021.09.21 - Actuação de Barcos [Gaia]
2021.10.01 - Atuação Rotary Clube Taipas
2021.10.05 - Acolhimento
2021.10.08 - Atuação Contabilistas
2021.11.03 - Receção ao Caloiro
2021.11.18 - Atuação Acolhimento Sénior [Penafiel]
2021.12.09 - Atuação Solidária | Associação Maconde
2021.00.00 - Sarau Cultural
2021.00.00 - Serestas
2022.01.24 - Aniversário Diana
2022.06.17 - Gala Erasmus ELACH
2022.06.20 - A UM vai ao S. João
2022.08.05 - Ribeira de Fráguas
2022.08.17 - Actuação de Barcos [Gaia]
2022.09.07 - Actuação de Barcos [Gaia]
2022.09.10 - Actuação de Barcos [Gaia]
2022.09.17 - Actuação de Barcos [Gaia]
2022.09.29 - Actuação de Barcos [Leverinho]
2022.10.01 - Actuação Barcos [Gaia]
2022.10.09 - Actuação de Barcos [Gaia]
2022.10.13 - Receção ao Caloiro
2022.10.26 - Actuação de Barcos [Gaia]
2022.11.03 - Actuação de Barcos [Leverinho]
2022.11.10 - Actuação de Barcos [Leverinho]
2022.11.17 - Actuação de Barcos [Leverinho]
2022.11.24 - Actuação de Barcos [Leverinho]
2022.12.01 - 1º de Dezembro
2022.00.00 - Actuação de barcos [Gaia]
2023.03.24 - Serenata Raquel
2023.05.05 - Associação de S. José
2023.05.07 - Enterro da Gata
2023.06.01 - Actuação de Barcos [Gaia]
2023.06.04 - Actuação de Barcos [Gaia]
2023.06.08 - Actuação de Barcos [Gaia]
2023.06.16 - Actuação de Barcos [Gaia]
2023.06.19 - U.M. Vai ao São João
2023.06.22 - Actuação de Barcos [Gaia]
2023.07.08 - Festa do Estudante da Paróquia de Souto
2023.07.27 - Quinzena Cultural de S. Mamede de Infesta
2023.08.04 - Encontro de Tunas de S. Tiago (Ribeira de Fráguas)
2023.08.17 - Actuação de barcos [Gaia]
2023.09.07 - Sunset Cultural
2023.10.08 - Actuação de Barcos [Gaia]
2023.11.25 - Actuação Pingo Doce Braga Parque
2023.11.30 - Récita
2023.12.20 - Actuação de Barcos [Gaia]
2023.00.00 - Actuação de Barcos
2024.01.03 - Receção ao Caloiro
2024.02.03 - Actuação de Rua
2024.06.02 - Paredes de Coura
2024.06.18 - São João de Braga
2024.06.21 - Actuação de Rua
2024.07.18 - Actuação de Barcos [Gaia]
2024.08.01 - Actuação de Barcos [Leverinho]
2024.08.08 - Actuação de Barcos [Leverinho]
2024.08.10 - Casamento da Margarida e do Nuno
2024.08.15 - Actuação de Barcos [Leverinho]
2024.09.26 - Actuação de Barcos [Leverinho]
2024.11.21 - Actuação de Barcos [Leverinho]
2025.05.28 - Actuação de Barcos [Leverinho]
2025.06.19 - Aniversário do Avô do Engenheiro
2025.06.22 - Actuação de barcos [Cais da Lixa]
"""

# Existing HTML events
existing_festivais = [
    ("2026.03.22", "IX Magna Augusta", "O nosso festival — a edição dos 30 anos com tunas convidadas de 5 países", "Theatro Circo, Braga"),
    ("2025.10.24", "V Incognifest", "Prémios: Melhor instrumental, Melhor pandeireta", "Vila Nova de Famalicão"),
    ("2025.05.03", "XXV FITAB", "Prémios: Melhor Instrumental, Melhor pandeireta", "Bragança"),
    ("2025.03.22", "XIII Bagatunaço", "Prémios: Melhor original, Tuna mais tuna", "Rio Maior"),
    ("2024.05.20", "Festival de Tunas do Porto", "Encontro anual das tunas do norte de Portugal", "Coliseu do Porto")
]

existing_outras = [
    ("2026.02.27", "Encontro nacional de alunos de AP", "Escola de Economia e Gestão (EEG)", "Universidade do Minho"),
    ("2026.02.22", "Lançamento de Livro / Jornadas EB", "Atuação Solidária / VIII jornadas de educação básica", "Vimieiro / Univ. do Minho"),
    ("2026.01.03", "Atuação de Barcos (Ano Novo)", "Temperatura: 10 Graus", "Cais de Gaia"),
    ("2025.12.01", "Récita do 1º de Dezembro", "Atuação em conjunto com a Afonsina", "Theatro Circo, Braga"),
    ("2025.11.18", "Magusto Lloyd", "Atuação comemorativa de Magusto", "Residência Univ. Lloyd"),
    ("2025.11.11", "Celebração de São Martinho", "Celebração do dia de São Martinho", "Hospital de Braga"),
    ("2025.05.01", "Temporada de Atuações nos Barcos", "Recorrentes de maio a dezembro: mais de 15 atuações (Cais de Lixa e Gaia)", "Rio Douro (Gaia/Lixa)")
]

def parse_events(raw_text):
    events = []
    for line in raw_text.strip().split('\n'):
        if not line.strip(): continue
        parts = line.split(" - ", 1)
        if len(parts) == 2:
            date_str = parts[0].strip()
            name = parts[1].strip()
            # If dates like 2020.00.00
            events.append((date_str, name, "Atuação da Augustuna", "Portugal"))
    return events

all_festivais = parse_events(festivais_raw) + existing_festivais
all_outras = parse_events(outras_raw) + existing_outras

# Deduplicate by name and year roughly
def dedup_sort(events):
    unique = {}
    for date_str, name, desc, loc in events:
        key = date_str[:4] + name
        if key not in unique:
            unique[key] = (date_str, name, desc, loc)
    
    # sort descending by date (handled properly because format is YYYY.MM.DD)
    return sorted(list(unique.values()), key=lambda x: x[0], reverse=True)

final_festivais = dedup_sort(all_festivais)
final_outras = dedup_sort(all_outras)

months = {
    "01": "Jan", "02": "Fev", "03": "Mar", "04": "Abr", "05": "Mai", "06": "Jun",
    "07": "Jul", "08": "Ago", "09": "Set", "10": "Out", "11": "Nov", "12": "Dez",
    "00": "---"
}

def build_html(events):
    html = []
    last_year = None
    for date_str, name, desc, loc in events:
        year = date_str[:4]
        month = date_str[5:7] if len(date_str) >= 7 else "00"
        day = date_str[8:10] if len(date_str) >= 10 else "--"
        if year != last_year:
            margin = ' style="margin-top: 1.5rem;"' if last_year else ''
            html.append(f'          <h3 class="performance-year-divider"{margin}>{year}</h3>')
            last_year = year
        
        m_str = months.get(month, "---")
        d_str = day if day != "00" else "--"
        
        html.append('          <div class="performance-item">')
        html.append('            <div class="performance-date">')
        html.append(f'              <div class="performance-day">{d_str}</div>')
        html.append(f'              <div class="performance-month">{m_str}</div>')
        html.append('            </div>')
        html.append('            <div class="performance-info">')
        html.append(f'              <h4>{name}</h4>')
        html.append(f'              <p>{desc}</p>')
        html.append('            </div>')
        html.append('            <div class="performance-location">')
        html.append('              <i data-lucide="map-pin" style="width:16px;height:16px;"></i>')
        html.append(f'              {loc}')
        html.append('            </div>')
        html.append('          </div>')
    return "\\n".join(html)

open("festivais.html", "w", encoding="utf-8").write(build_html(final_festivais))
open("outras.html", "w", encoding="utf-8").write(build_html(final_outras))
print("Done. Generated festivais.html and outras.html")
