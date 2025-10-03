import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime

# Configuração da Página 
# Configurações iniciais da página do dashboard
st.set_page_config(
    page_title="Dashboard de Monitoramento do Motor",
    page_icon="📈", 
    layout="wide"  
)

# Caminho do Banco de Dados 
DB_FILE = os.path.join('..', 'db', 'sensores.db')

# Função para Carregar Dados
# Esta função conecta ao banco de dados e carrega todos os dados da tabela.

@st.cache_data
def carregar_dados():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM leituras_sensor", conn)
    conn.close()
    # Converte a coluna de data para o formato datetime do pandas
    df['data_leitura'] = pd.to_datetime(df['data_leitura'])
    return df

# Título do Dashboard
st.title("📈 Dashboard de Monitoramento do Motor Industrial")

# - Carregar os Dados
df = carregar_dados()

# Exibição dos Dados
st.subheader("Dados Brutos Coletados")
st.dataframe(df)

# Métricas Principais
st.subheader("Métricas em Tempo Real")
# Pega a leitura mais recente (a última linha do DataFrame ordenado por data)
leitura_recente = df.sort_values(by='data_leitura', ascending=False).iloc[0]

# Criação de colunas para organizar as métricas
col1, col2, col3 = st.columns(3)

col1.metric("Última Temperatura", f"{leitura_recente['temperatura']:.2f} °C")
col2.metric("Última Umidade", f"{leitura_recente['umidade']:.2f} %")
col3.metric("Total de Registros", f"{len(df)}")


# Sistema de Alertas
st.subheader("🚨 Sistema de Alertas")
THRESHOLD_TEMPERATURA = 40.0

# Verifica se a temperatura mais recente ultrapassou o limite
if leitura_recente['temperatura'] > THRESHOLD_TEMPERATURA:
    # Exibe uma mensagem de erro destacada
    st.error(f"ALERTA DE SUPERQUECIMENTO! Temperatura atual: {leitura_recente['temperatura']:.2f}°C.", icon="🔥")
else:
    # Exibe uma mensagem de sucesso
    st.success("Status do motor: Normal. Temperatura dentro dos limites seguros.", icon="✅")


# Gráfico do Histórico de Temperatura
st.subheader("Histórico de Leituras de Temperatura")
# Prepara o dataframe para o gráfico, usando a data como índice
df_chart = df.set_index('data_leitura')
# Gráfico de linha
st.line_chart(df_chart['temperatura'])

# Rodapé
st.write("---")
st.write(f"Dashboard atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")