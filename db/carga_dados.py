import sqlite3
import pandas as pd
import os # Biblioteca que interage com o sistema operacional

# Configuração dos Nomes dos Arquivos
DB_FILE = "sensores.db"
CSV_FILE = os.path.join('..', 'ingest', 'dados_sensores.csv') 
SQL_FILE = 'criar_banco.sql'


# Conexão com o Banco de Dados
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
print(f"Banco de dados '{DB_FILE}' conectado com sucesso.")


# Criação da Tabela
with open(SQL_FILE, 'r') as f:
    sql_script = f.read()
cursor.executescript(sql_script)
print(f"Tabela 'leituras_sensor' verificada/criada com sucesso a partir de '{SQL_FILE}'.")


# Lê os dados do arquivo CSV usando a biblioteca Pandas.
print(f"Lendo dados de '{CSV_FILE}'...")
df = pd.read_csv(CSV_FILE)


# Uso do Pandas para inserir todos os dados do CSV na tabela de uma só vez.
df.to_sql('leituras_sensor', conn, if_exists='append', index=False)
print(f"{len(df)} registros de '{CSV_FILE}' inseridos na tabela 'leituras_sensor'.")


# Verificação
print("\n--- Verificando os 5 primeiros registros no banco: ---")
cursor.execute("SELECT * FROM leituras_sensor ORDER BY id DESC LIMIT 5") # Mostra os últimos 5 inseridos
for row in cursor.fetchall():
    print(row)
print("--------------------------------------------------")

 
# Commit e fechamento da conexão com o banco de dados.
conn.commit()
conn.close()
print("Alterações salvas e conexão com o banco de dados fechada.")