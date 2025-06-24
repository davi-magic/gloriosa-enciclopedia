import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="A Gloriosa Enciclopédia", page_icon="⭐", layout="wide")

# 🔒 Senha
PASSWORD = "botaelasil"

# 🔐 Função de autenticação corrigida
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.markdown("<h1 style='color:gold'>⭐ A Gloriosa Enciclopédia ⭐</h1>", unsafe_allow_html=True)
        st.markdown("#### 🔐 Acesso restrito")
        password = st.text_input("Digite a senha:", type="password")

        if password == PASSWORD:
            st.session_state["authenticated"] = True
            st.success("✅ Acesso liberado!")
        elif password != "":
            st.error("❌ Senha incorreta")

        return False
    else:
        return True


# 🔗 Função para extrair dados de um link do Challenge Place
def extrair_dados(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')

        tabela = soup.find('table')
        headers = [th.get_text(strip=True) for th in tabela.find_all('th')]
        rows = tabela.find_all('tr')

        dados = []
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                nome = cols[1].get_text(strip=True)
                gols = int(cols[2].get_text(strip=True) or 0)
                assist = int(cols[3].get_text(strip=True) or 0)
                particip = gols + assist
                time = cols[4].get_text(strip=True) if len(cols) >= 5 else 'N/A'

                dados.append({
                    'Nome': nome,
                    'Gols': gols,
                    'Assistências': assist,
                    'Participações': particip,
                    'Time': time,
                    'Fonte': link
                })
        df = pd.DataFrame(dados)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao processar {link}: {e}")
        return pd.DataFrame()


# 🔥 Função para importar múltiplos links
@st.cache_data(show_spinner="⏳ Importando dados...")
def importar_dados(links):
    dfs = []
    for link in links:
        df = extrair_dados(link)
        if not df.empty:
            dfs.append(df)
    if dfs:
        base = pd.concat(dfs, ignore_index=True)
        return base
    else:
        return pd.DataFrame()


# 🔍 Função para responder perguntas
def responder_pergunta(pergunta, df):
    pergunta = pergunta.lower()

    if "artilheiro" in pergunta or "mais gols" in pergunta:
        tabela = df.groupby('Nome').agg({'Gols':'sum'}).sort_values('Gols', ascending=False).reset_index()
        titulo = "🏆 Artilheiros"
    elif "assist" in pergunta:
        tabela = df.groupby('Nome').agg({'Assistências':'sum'}).sort_values('Assistências', ascending=False).reset_index()
        titulo = "🎯 Assistências"
    elif "participa" in pergunta:
        tabela = df.groupby('Nome').agg({'Participações':'sum'}).sort_values('Participações', ascending=False).reset_index()
        titulo = "🔗 Participações em Gols"
    else:
        return "❌ Não entendi a pergunta. Tente: 'Top 10 artilheiros', 'Quem tem mais assistências?', 'Top 15 participações'."

    match = re.search(r"top (\d+)", pergunta)
    n = int(match.group(1)) if match else 10

    return titulo, tabela.head(n)


# 🚀 APP PRINCIPAL
if check_password():
    st.markdown("<h1 style='color:gold'>⭐ A Gloriosa Enciclopédia está no ar ⭐</h1>", unsafe_allow_html=True)

    links_input = st.text_area("🔗 Cole os links do Challenge Place (um por linha):")

    if st.button("Importar Dados"):
        links = [l.strip() for l in links_input.split("\n") if l.strip()]
        if links:
            df = importar_dados(links)

            if df.empty:
                st.error("❌ Não foi possível extrair dados dos links fornecidos.")
            else:
                st.success(f"✅ {len(links)} temporadas importadas com sucesso!")
                st.subheader("📊 Dados Consolidados:")
                st.dataframe(df)

                pergunta = st.text_input("🔎 Faça sua pergunta (Ex.: 'Top 10 artilheiros', 'Quem tem mais assistências?'):")

                if pergunta:
                    resultado = responder_pergunta(pergunta, df)
                    if isinstance(resultado, str):
                        st.warning(resultado)
                    else:
                        titulo, tabela = resultado
                        st.subheader(titulo)
                        st.dataframe(tabela)
        else:
            st.warning("⚠️ Insira pelo menos um link válido.")
