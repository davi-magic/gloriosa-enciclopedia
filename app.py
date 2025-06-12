import streamlit as st
import pandas as pd
import re

jogadores_df = pd.read_csv("data/jogadores.csv")
campeoes_df = pd.read_csv("data/campeoes.csv")

def responder_pergunta(pergunta: str) -> str:
    pergunta = pergunta.lower()

    if match := re.search(r'artilheiro da temporada (\d+)', pergunta):
        temporada = int(match.group(1))
        temp = jogadores_df[jogadores_df['temporada'] == temporada]
        if temp.empty:
            return "Temporada não encontrada."
        top = temp.sort_values('gols', ascending=False).iloc[0]
        return f"O artilheiro da temporada {temporada} foi {top['jogador']} com {top['gols']} gols."

    if match := re.search(r'gols o ([\w\s]+) fez na temporada (\d+)', pergunta):
        jogador = match.group(1).strip().capitalize()
        temporada = int(match.group(2))
        row = jogadores_df[(jogadores_df['jogador'].str.lower() == jogador.lower()) & (jogadores_df['temporada'] == temporada)]
        if row.empty:
            return f"Sem dados do jogador {jogador} na temporada {temporada}."
        return f"{jogador} fez {row.iloc[0]['gols']} gols na temporada {temporada}."

    if match := re.search(r'campe[aã]o da temporada (\d+)', pergunta):
        temporada = int(match.group(1))
        row = campeoes_df[campeoes_df['temporada'] == temporada]
        if row.empty:
            return "Sem dados de campeão para essa temporada."
        return f"O campeão da temporada {temporada} foi o {row.iloc[0]['time']}."

    return "Desculpe, não entendi a pergunta."

st.title("📘 Gloriosa Enciclopédia")
pergunta = st.text_input("Faça sua pergunta")
if st.button("Perguntar"):
    resposta = responder_pergunta(pergunta)
    st.write(resposta)
