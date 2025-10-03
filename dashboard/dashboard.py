import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime

# --- Configuração da Página ---
# st.set_page_config define as configurações iniciais da página do dashboard
st.set_page_config(
    page_title="Dashboard de Monitoramento do Motor",
    page_icon="📈", # Ícone da página
    layout="wide"  # Layout 'largo' para usar mais espaço da tela
)

# --- Caminho do Banco de Dados ---
DB_FILE = os.path.join('..', 'db', 'sensores.db')

# --- Função para Carregar Dados ---
# Esta função conecta ao banco de dados e carrega todos os dados da tabela.
# O @st.cache_data faz com que o Streamlit seja inteligente e não recarregue os dados
# desnecessariamente, melhorando a performance.
@st.cache_data
def carregar_dados():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM leituras_sensor", conn)
    conn.close()
    # Converte a coluna de data para o formato datetime do pandas
    df['data_leitura'] = pd.to_datetime(df['data_leitura'])
    return df

# --- Título do Dashboard ---
st.title("📈 Dashboard de Monitoramento do Motor Industrial")

# --- Carregar os Dados ---
df = carregar_dados()

# --- Exibindo os Dados ---
# st.dataframe exibe a tabela de dados de forma interativa.
st.subheader("Dados Brutos Coletados")
st.dataframe(df)

# --- KPIs (Key Performance Indicators) / Métricas Principais ---
st.subheader("Métricas em Tempo Real")
# Pega a leitura mais recente (a última linha do DataFrame ordenado por data)
leitura_recente = df.sort_values(by='data_leitura', ascending=False).iloc[0]

# st.columns cria colunas para organizar os KPIs lado a lado
col1, col2, col3 = st.columns(3)
# st.metric exibe uma métrica com um rótulo, valor e pode mostrar uma variação (delta)
col1.metric("Última Temperatura", f"{leitura_recente['temperatura']:.2f} °C")
col2.metric("Última Umidade", f"{leitura_recente['umidade']:.2f} %")
col3.metric("Total de Registros", f"{len(df)}")


# --- Sistema de Alertas ---
st.subheader("🚨 Sistema de Alertas")
THRESHOLD_TEMPERATURA = 40.0

# Verifica se a temperatura mais recente ultrapassou o limite
if leitura_recente['temperatura'] > THRESHOLD_TEMPERATURA:
    # st.error exibe uma mensagem de erro destacada
    st.error(f"ALERTA DE SUPERQUECIMENTO! Temperatura atual: {leitura_recente['temperatura']:.2f}°C.", icon="🔥")
else:
    # st.success exibe uma mensagem de sucesso
    st.success("Status do motor: Normal. Temperatura dentro dos limites seguros.", icon="✅")


# --- Gráfico do Histórico de Temperatura ---
st.subheader("Histórico de Leituras de Temperatura")
# Prepara o dataframe para o gráfico, usando a data como índice
df_chart = df.set_index('data_leitura')
# st.line_chart desenha um gráfico de linha
st.line_chart(df_chart['temperatura'])

# --- Rodapé ---
st.write("---")
st.write(f"Dashboard atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")