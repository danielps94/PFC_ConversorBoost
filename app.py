import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="PFC ConversorBoost",
    page_icon="⚡",
    layout="wide"
)

# Título principal
st.title("⚡ PFC ConversorBoost")
st.subheader("Conversor e Analisador de Dados")

# Sidebar
with st.sidebar:
    st.header("Configurações")
    opcao = st.radio(
        "Selecione uma opção:",
        ["Início", "Conversor", "Análise"]
    )

# Conteúdo principal
if opcao == "Início":
    st.write("""
    Bem-vindo ao **PFC ConversorBoost**! 
    
    Esta aplicação foi desenvolvida para facilitar a conversão e análise de dados.
    
    ### Como usar:
    1. Acesse as seções no menu lateral
    2. Upload seus dados ou utilize as ferramentas disponíveis
    3. Exporte os resultados
    """)

elif opcao == "Conversor":
    st.header("Conversor de Dados")
    uploaded_file = st.file_uploader("Faça upload de um arquivo", type=["csv", "xlsx", "json"])
    
    if uploaded_file:
        st.write("Arquivo carregado com sucesso!")
        st.write(uploaded_file.name)

elif opcao == "Análise":
    st.header("Análise de Dados")
    st.write("Ferramentas de análise em desenvolvimento...")
