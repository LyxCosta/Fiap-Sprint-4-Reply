import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Configuração do path
DB_FILE = os.path.join('..', 'db', 'sensores.db')

# Conectando ao Banco de Dados
print(f"Conectando ao banco de dados em '{DB_FILE}'...")
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM leituras_sensor", conn)
conn.close()
print(f"{len(df)} registros carregados do banco de dados.")


df['estado'] = (df['temperatura'] > 40).astype(int)
print("Coluna 'estado' criada: 1 para Alerta (>40°C), 0 para Normal.")


# Dados para Treinamento
X = df[['temperatura', 'umidade']]
y = df['estado']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Dados divididos em treino ({len(X_train)} registros) e teste ({len(X_test)} registros).")


# Treinamento de ML
modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X_train, y_train)
print("Modelo de Árvore de Decisão treinado com sucesso!")


# Avaliação
y_pred = modelo.predict(X_test)

acuracia = accuracy_score(y_test, y_pred)
print(f"\nAcurácia do modelo nos dados de teste: {acuracia:.2f} ({acuracia*100:.2f}%)")


print("Gerando a Matriz de Confusão...")
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Normal', 'Alerta'], yticklabels=['Normal', 'Alerta'])
plt.xlabel('Previsão do Modelo')
plt.ylabel('Valor Real')
plt.title('Matriz de Confusão')

plt.savefig('matriz_confusao.png')
print("Gráfico da Matriz de Confusão salvo como 'matriz_confusao.png'")
print("Gerando gráfico de dispersão das previsões...")

# DataFrame
df_pred = X_test.copy()
df_pred['Valor Real'] = y_test
df_pred['Previsão do Modelo'] = y_pred

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_pred,
    x='temperatura',
    y='umidade',
    hue='Previsão do Modelo', 
    style='Valor Real',    
    palette={0: 'green', 1: 'red'}, 
    s=100,                 
    alpha=0.8                
)
plt.axvline(x=40, color='gray', linestyle='--', label='Limite de Alerta (Temp=40°C)')
plt.title('Previsão do Modelo: Temperatura vs. Umidade')
plt.xlabel('Temperatura (°C)')
plt.ylabel('Umidade (%)')
plt.legend(title='Classe')
plt.grid(True)
plt.savefig('scatter_previsao.png')
plt.show()
print("Gráfico de dispersão salvo como 'scatter_previsao.png'")
plt.show()