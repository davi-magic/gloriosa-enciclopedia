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

# Função para extrair dados do Challenge Place
def extrair_dados_challenge_place(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")

        nome_torneio = soup.find("h1")
        titulo = nome_torneio.text.strip() if nome_torneio else "Torneio Desconhecido"

        times = [tag.text.strip() for tag in soup.find_all("span") if tag.text.strip()]
        times_filtrados = list(set([t for t in times if len(t) > 2 and len(t) < 50]))[:20]

        return {
            "titulo": titulo,
            "times": times_filtrados,
        }
    except Exception as e:
        return {"erro": str(e)}

# Estado inicial
if "dados_torneio" not in st.session_state:
    st.session_state.dados_torneio = None

# Atualizar ou carregar dados
def carregar_dados():
    url = st.text_input("Cole o link do campeonato no Challenge Place:")
    if st.button("🔄 Atualizar Dados"):
        if url:
            dados = extrair_dados_challenge_place(url)
            if "erro" in dados:
                st.error("Erro ao extrair dados: " + dados["erro"])
            else:
                st.session_state.dados_torneio = dados
        else:
            st.warning("Cole um link válido para atualizar.")

carregar_dados()

# Exibir dados extraídos
if st.session_state.dados_torneio:
    dados = st.session_state.dados_torneio
    st.subheader("📋 Dados Extraídos")
    st.write(f"**Nome do Torneio:** {dados['titulo']}")
    st.write("**Times detectados:**")
    st.write(dados["times"])

    # Função de resposta da IA
    def responder_ia(pergunta):
        pergunta = pergunta.lower()
        titulo = dados['titulo']
        times = dados['times']
        
        if "nome" in pergunta or "torneio" in pergunta:
            return f"O nome do torneio é **{titulo}**."
        elif "quantos times" in pergunta or "número de times" in pergunta:
            return f"O torneio tem **{len(times)} times**."
        elif "quais times" in pergunta or "times participantes" in pergunta:
            return "Os times participantes são: " + ", ".join(times) + "."
        elif "resumo" in pergunta or "visão geral" in pergunta:
            return f"O torneio **{titulo}** conta com **{len(times)} times** participantes: {', '.join(times)}."
        else:
            return "Ainda não sei responder essa pergunta nessa versão de teste. Em breve saberei muito mais!"

    # Campo de chat
    st.subheader("🤖 Pergunte algo sobre o campeonato:")
    pergunta = st.text_input("Digite sua pergunta:")
    if pergunta:
        resposta = responder_ia(pergunta)
        st.success(resposta)
else:
    st.info("Cole o link de um campeonato para começar!")