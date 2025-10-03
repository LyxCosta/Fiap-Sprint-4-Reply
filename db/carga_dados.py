import sqlite3
import pandas as pd
import os # Biblioteca para interagir com o sistema operacional

# --- Configuração dos Nomes dos Arquivos ---
# O nome do arquivo do banco de dados que será criado.
DB_FILE = "sensores.db"
# O caminho para o arquivo CSV. Usamos '..' para "voltar" uma pasta.
CSV_FILE = os.path.join('..', 'ingest', 'dados_sensores.csv') 
# O caminho para o script SQL.
SQL_FILE = 'criar_banco.sql'


# --- Conexão com o Banco de Dados ---
# Conecta ao banco de dados. O arquivo .db será criado na mesma pasta que este script.
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
print(f"Banco de dados '{DB_FILE}' conectado com sucesso.")


# --- Criação da Tabela ---
# Abre e lê o arquivo SQL que define a estrutura da tabela.
with open(SQL_FILE, 'r') as f:
    sql_script = f.read()

# Executa o script SQL para criar a tabela.
cursor.executescript(sql_script)
print(f"Tabela 'leituras_sensor' verificada/criada com sucesso a partir de '{SQL_FILE}'.")


# --- Carga dos Dados ---
# Lê os dados do arquivo CSV usando a biblioteca Pandas.
print(f"Lendo dados de '{CSV_FILE}'...")
df = pd.read_csv(CSV_FILE)

# Usa a função to_sql do Pandas para inserir todos os dados do CSV na tabela de uma só vez.
# if_exists='append' significa que os dados serão adicionados, sem apagar o que já existe.
df.to_sql('leituras_sensor', conn, if_exists='append', index=False)
print(f"{len(df)} registros de '{CSV_FILE}' inseridos na tabela 'leituras_sensor'.")


# --- Verificação (Evidência) ---
# Executa um comando SQL para selecionar e mostrar os 5 primeiros registros da tabela.
# Isso serve como prova de que os dados foram inseridos corretamente.
print("\n--- Verificando os 5 primeiros registros no banco: ---")
cursor.execute("SELECT * FROM leituras_sensor ORDER BY id DESC LIMIT 5") # Mostra os últimos 5 inseridos
for row in cursor.fetchall():
    print(row)
print("--------------------------------------------------")


# --- Finalização ---
# Salva as alterações (commit) e fecha a conexão com o banco de dados.
conn.commit()
conn.close()
print("Alterações salvas e conexão com o banco de dados fechada.")