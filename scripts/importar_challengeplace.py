from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Links do campeonato
LINKS = [
    "https://challenge.place/c/6811755390eab96cd7457c15",
    "https://challenge.place/c/6807e82d2effc5981ebaafa9",
    "https://challenge.place/c/6811754114fd883a743fec98",
    "https://challenge.place/c/6811752b30f744705565b2b9",
    "https://challenge.place/c/6811751cc4e2ad796c8f1e09",
    "https://challenge.place/c/681175014719499549303a9c",
    "https://challenge.place/c/681174bf1a32a5334748ff9f",
    "https://challenge.place/c/681175668ba0074afb6e70d9"
]

# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Simulação (exemplo de estrutura real)
jogadores = []
partidas = []
campeoes = []
eventos = []

for idx, link in enumerate(LINKS, start=1):
    driver.get(link)
    time.sleep(3)
    print(f"Processando temporada {idx}...")

    # 🔥 Aqui entraria o código real de scraping

    jogadores.append({'temporada': idx, 'jogador': 'Exemplo', 'gols': 10})
    partidas.append({'temporada': idx, 'casa': 'Time A', 'fora': 'Time B', 'gols_casa': 2, 'gols_fora': 1, 'estadio': 'Estadio X'})
    campeoes.append({'temporada': idx, 'time': 'Time Exemplo'})
    eventos.append({'temporada': idx, 'jogo_id': idx, 'jogador': 'Exemplo', 'minuto': 45, 'tipo': 'gol', 'assistente': 'Outro'})

driver.quit()

# 🔄 Salvando CSVs
pd.DataFrame(jogadores).to_csv('data/jogadores.csv', index=False)
pd.DataFrame(partidas).to_csv('data/partidas.csv', index=False)
pd.DataFrame(campeoes).to_csv('data/campeoes.csv', index=False)
pd.DataFrame(eventos).to_csv('data/eventos.csv', index=False)

print("✅ Dados salvos na pasta /data")
