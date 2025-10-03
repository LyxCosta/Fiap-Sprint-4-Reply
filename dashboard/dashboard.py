import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime

# Configuração da Página 
st.set_page_config(
    page_title="Dashboard de Monitoramento do Motor",
    page_icon="📈", 
    layout="wide"  
)
 
DB_FILE = os.path.join('..', 'db', 'sensores.db')

@st.cache_data
def carregar_dados():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM leituras_sensor", conn)
    conn.close()
    df['data_leitura'] = pd.to_datetime(df['data_leitura'])
    return df

st.title("📈 Dashboard de Monitoramento do Motor Industrial")

df = carregar_dados()

# Exibição dos Dados
st.subheader("Dados Brutos Coletados")
st.dataframe(df)

# Métricas Principais
st.subheader("Métricas em Tempo Real")
leitura_recente = df.sort_values(by='timestamp', ascending=False).iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric("Última Temperatura", f"{leitura_recente['temperatura']:.2f} °C")
col2.metric("Última Umidade", f"{leitura_recente['umidade']:.2f} %")
col3.metric("Total de Registros", f"{len(df)}")


# Alertas
st.subheader("🚨 Sistema de Alertas")
THRESHOLD_TEMPERATURA = 40.0

if leitura_recente['temperatura'] > THRESHOLD_TEMPERATURA:
    st.error(f"ALERTA DE SUPERQUECIMENTO! Temperatura atual: {leitura_recente['temperatura']:.2f}°C.", icon="🔥")
else:
    st.success("Status do motor: Normal. Temperatura dentro dos limites seguros.", icon="✅")


# Graficos de Temperatura
st.subheader("Histórico de Leituras de Temperatura")
df_chart = df.set_index('data_leitura')
st.line_chart(df_chart['temperatura'])

st.write("---")
st.write(f"Dashboard atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")