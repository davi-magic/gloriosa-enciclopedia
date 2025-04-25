
import streamlit as st

senha = st.text_input("Digite a senha para acessar:", type="password")

if senha == "botaelasil":
    st.title("A Gloriosa Enciclopédia")
    st.write("Aqui você poderá interagir com sua inteligência artificial.")
else:
    st.warning("Acesso restrito. Digite a senha correta.")
