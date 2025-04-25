
import streamlit as st

st.set_page_config(page_title="A Gloriosa Enciclopédia", layout="centered")
senha = st.text_input("Digite a senha para acessar a Gloriosa Enciclopédia:", type="password")

if senha != "botaelasil":
    st.warning("Acesso restrito. Digite a senha correta.")
    st.stop()

st.title("A Gloriosa Enciclopédia")
st.write("Versão preliminar em funcionamento.")
st.write("Em breve você poderá fazer perguntas sobre campeonatos, jogadores e previsões.")
