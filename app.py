
import streamlit as st

st.set_page_config(page_title="A Gloriosa Enciclopédia", page_icon="⭐")

PASSWORD = "botaelasil"

def check_password():
    def password_entered():
        return st.session_state["password"] == PASSWORD

    if "password" not in st.session_state:
        st.session_state["password"] = ""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.title("Login")
        password = st.text_input("Senha:", type="password", key="password")
        if st.button("Entrar"):
            if password == PASSWORD:
                st.session_state["password_correct"] = True
                st.experimental_rerun()
            else:
                st.error("Senha incorreta")
        return False
    else:
        return True

if check_password():
    st.title("A Gloriosa Enciclopédia está no ar")

    st.markdown("Cole um ou mais links do Challenge Place abaixo, um por linha.")
    links = st.text_area("Links do Challenge Place (um por linha)")
    if st.button("Importar dados"):
        link_list = [l.strip() for l in links.split("\n") if l.strip()]
        st.write(f"Importando {len(link_list)} links...")
        # Aqui entraria a lógica real para importar e processar dados
        # Simulação para demo
        st.success("Dados importados com sucesso!")
        st.write("Agora você pode fazer perguntas como:")
        st.write("- Quem é o artilheiro da temporada?")
        st.write("- Top 10 assistências")
        st.write("- Quem tem mais participações em gols?")
