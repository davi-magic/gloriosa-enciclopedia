import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="A Gloriosa Enciclopédia", layout="centered")

# Estilo preto e dourado
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: #FFD700;
        }
        .stApp {
            background-color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

# Proteção por senha
if 'acesso_liberado' not in st.session_state:
    senha = st.text_input("Digite a senha para acessar:", type="password")
    if senha == "botaelasil":
        st.session_state.acesso_liberado = True
    else:
        st.stop()

st.title("🏆 A Gloriosa Enciclopédia")

# Entrada de link do Challenge Place
url = st.text_input("Cole o link do campeonato no Challenge Place:")

def extrair_dados_challenge_place(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")

        nome_torneio = soup.find("h1")
        titulo = nome_torneio.text.strip() if nome_torneio else "Torneio Desconhecido"

        # Simplesmente extrair times listados
        times = [tag.text.strip() for tag in soup.find_all("span") if tag.text.strip()]
        times_filtrados = list(set([t for t in times if len(t) > 2 and len(t) < 50]))[:20]  # Limite para teste

        return {
            "titulo": titulo,
            "times": times_filtrados,
        }
    except Exception as e:
        return {"erro": str(e)}

if url:
    st.subheader("📋 Dados Extraídos")
    dados = extrair_dados_challenge_place(url)
    if "erro" in dados:
        st.error("Erro ao extrair dados: " + dados["erro"])
    else:
        st.write(f"**Nome do Torneio:** {dados['titulo']}")
        st.write("**Times detectados:**")
        st.write(dados["times"])
        st.info("Versão de teste — IA ainda será conectada para responder com base nesses dados.")