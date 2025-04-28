
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gloriosa Enciclopédia", page_icon="⚽", layout="wide")

# Simulando base de dados (substituir depois por importação dos links reais)
dados = pd.DataFrame({
    'Jogador': ['Jogador A', 'Jogador B', 'Jogador C', 'Jogador D'],
    'Gols': [55, 48, 42, 36],
    'Mata_Mata_Gols': [20, 18, 15, 12],
    'Temporada': [18, 18, 17, 16]
})

# Interface
st.title("⚽ Gloriosa Enciclopédia")
st.markdown("### Pergunte sobre os artilheiros, temporadas ou gols em mata-mata!")

pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    pergunta = pergunta.lower()

    if "maior artilheiro" in pergunta or "mais gols" in pergunta:
        artilheiro = dados.loc[dados['Gols'].idxmax()]
        st.success(f"O maior artilheiro é **{artilheiro['Jogador']}**, com **{artilheiro['Gols']} gols**.")

    elif "mata-mata" in pergunta and "mais gols" in pergunta:
        mata_mata = dados.loc[dados['Mata_Mata_Gols'].idxmax()]
        st.success(f"Quem mais marcou em mata-mata foi **{mata_mata['Jogador']}**, com **{mata_mata['Mata_Mata_Gols']} gols**.")

    elif "temporada" in pergunta:
        # Captura o número da temporada que o usuário quer saber
        import re
        numeros = re.findall(r'\d+', pergunta)
        if numeros:
            temporada = int(numeros[0])
            dados_temp = dados[dados['Temporada'] == temporada]
            if not dados_temp.empty:
                jogador_temp = dados_temp.loc[dados_temp['Gols'].idxmax()]
                st.success(f"Na temporada {temporada}, o maior artilheiro foi **{jogador_temp['Jogador']}** com **{jogador_temp['Gols']} gols**.")
            else:
                st.error(f"Não há dados cadastrados para a temporada {temporada}.")
        else:
            st.error("Por favor, especifique a temporada na pergunta.")

    else:
        st.warning("Pergunta não reconhecida ainda. Tente algo como: 'Quem é o maior artilheiro?' ou 'Quem fez mais gols no mata-mata?'")

st.divider()
st.write("Versão de testes - base de dados simulada.")
