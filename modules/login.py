import streamlit as st

def login():
    password = st.text_input("Senha", type="password")
    if password == "botaelasil":
        return True
    elif password:
        st.error("Senha incorreta.")
    return False