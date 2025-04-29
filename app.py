import streamlit as st
from modules.login import login
from modules.parser import parse_data
from modules.qa import answer_question

st.set_page_config(page_title="Gloriosa Enciclopédia", layout="centered")
if login():
    st.title("A Gloriosa Enciclopédia")
    uploaded = st.file_uploader("Envie o campeonato (.json):")
    if uploaded:
        data = parse_data(uploaded)
        question = st.text_input("Faça sua pergunta:")
        if question:
            answer = answer_question(data, question)
            st.write(answer)