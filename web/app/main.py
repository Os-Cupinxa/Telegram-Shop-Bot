import streamlit as st
from components import home, about, contact, sidebar

# Título da aplicação
st.markdown("# Simple Streamlit App")

# Barra lateral para navegação
menu = sidebar.show_sidebar()

# Conteúdo com base na seleção do menu
if menu == "Home":
    home.show_home()
elif menu == "About":
    about.show_about()
elif menu == "Contact":
    contact.show_contact()
