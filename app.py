import streamlit as st
import pandas as pd
import re

# 🎨 Tema preto e dourado + Estrela Gloriosa
st.set_page_config(page_title="⭐ Gloriosa Enciclopédia", page_icon="⭐", layout="centered")
st.markdown(
    """
    <h1 style='text-align: center; color: gold;'>⭐ Gloriosa Enciclopédia ⭐</h1>
    <h4 style='text-align: center; color: white;'>Onde dados viram lendas</h4>
    """, 
    unsafe_allow_html=True
)

# 📂 Carregando dados
jogadores = pd.read_csv('data/jogadores.csv')
partidas = pd.read_csv('data/partidas.csv')
campeoes = pd.read_csv('data/campeoes.csv')
eventos = pd.read_csv('data/eventos.csv')

# 🎚️ Controle de Top N
top_n = st.slider('Selecione o tamanho do ranking (Top N)', 3, 50, 10)

# 🧠 Função para responder perguntas
def responder(pergunta):
    p = pergunta.lower()

    # 🔥 Artilheiro da temporada
    m = re.search(r'artilheiro da temporada (\d+)', p)
    if m:
        temporada = int(m.group(1))
        temp = jogadores[jogadores['temporada'] == temporada]
        if temp.empty:
            return "Temporada não encontrada."
        top = temp.sort_values('gols', ascending=False).iloc[0]
        return f"O artilheiro da temporada {temporada} foi {top['jogador']} com {top['gols']} gols."

    # 🔥 Artilheiro histórico
    if 'artilheiro da história' in p or 'artilheiro historico' in p:
        top = jogadores.groupby('jogador')['gols'].sum().reset_index().sort_values('gols', ascending=False).iloc[0]
        return f"O artilheiro histórico é {top['jogador']} com {top['gols']} gols."

    # 🔥 Campeão da temporada
    m = re.search(r'campe[aã]o da temporada (\d+)', p)
    if m:
        temporada = int(m.group(1))
        linha = campeoes[campeoes['temporada'] == temporada]
        if linha.empty:
            return "Temporada não encontrada."
        time = linha.iloc[0]['time']
        return f"O campeão da temporada {temporada} foi o {time}."

    return "❌ Pergunta não entendida ou fora do escopo atual."

# 🗣️ Interface de Perguntas
st.subheader("Pergunte algo:")
pergunta = st.text_input("Exemplos: 'Quem foi o artilheiro da temporada 3?', 'Artilheiro da história', 'Quem foi o campeão da temporada 2?'")

if st.button('Perguntar'):
    resposta = responder(pergunta)
    st.success(resposta)

# 📊 Rankings
st.subheader(f"Top {top_n} Artilheiros da História")
ranking = jogadores.groupby('jogador')['gols'].sum().reset_index().sort_values('gols', ascending=False).head(top_n)
st.dataframe(ranking)
