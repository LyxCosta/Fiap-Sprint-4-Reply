import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Configuração dos Caminhos
DB_FILE = os.path.join('..', 'db', 'sensores.db')

# 1. Conecta ao Banco de Dados
print(f"Conectando ao banco de dados em '{DB_FILE}'...")
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM leituras_sensor", conn)
conn.close()
print(f"{len(df)} registros carregados do banco de dados.")


# 2. Preparação dos Dados para o Modelo
# Esta é a etapa em que criamos a nossa variável "alvo" (o que queremos prever).
# Se a temperatura for maior que 40, o estado é 1 (Alerta). Caso contrário, é 0 (Normal).
df['estado'] = (df['temperatura'] > 40).astype(int)
print("Coluna 'estado' criada: 1 para Alerta (>40°C), 0 para Normal.")


# 3. Preparação de Dados para Treino
# X -> são as variáveis que o modelo usará para aprender.
X = df[['temperatura', 'umidade']]
# y -> é a resposta que queremos que o modelo aprenda a prever).
y = df['estado']

# Os dados são divididos: 80% para o modelo treinar, 20% para testarmos se ele aprendeu bem.
# stratify=y é importante para garantir que a proporção de 0s e 1s seja a mesma no treino e no teste.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Dados divididos em treino ({len(X_train)} registros) e teste ({len(X_test)} registros).")


# 4. Treinamento do Modelo de Machine Learning
# Usaremos um modelo simples e eficaz para classificação: a Árvore de Decisão.
modelo = DecisionTreeClassifier(random_state=42)
# O comando .fit() é o momento em que o modelo "estuda" os dados de treino para encontrar padrões.
modelo.fit(X_train, y_train)
print("Modelo de Árvore de Decisão treinado com sucesso!")


# 5. Avaliar o Modelo
# Pedimos para o modelo prever o estado dos dados de teste (que ele nunca viu antes).
y_pred = modelo.predict(X_test)

# Comparamos as previsões (y_pred) com o gabarito real (y_test) para calcular a acurácia.
acuracia = accuracy_score(y_test, y_pred)
print(f"\nAcurácia do modelo nos dados de teste: {acuracia:.2f} ({acuracia*100:.2f}%)")


# 6. Visualização do Resultado
# A Matriz de Confusão é um gráfico que mostra de forma clara onde o modelo acertou e errou.
print("Gerando a Matriz de Confusão...")
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Normal', 'Alerta'], yticklabels=['Normal', 'Alerta'])
plt.xlabel('Previsão do Modelo')
plt.ylabel('Valor Real')
plt.title('Matriz de Confusão')

# Salva a imagem na mesma pasta do script
plt.savefig('matriz_confusao.png')
print("Gráfico da Matriz de Confusão salvo como 'matriz_confusao.png'")
# 7. Visualização Alternativa: Gráfico de Dispersão das Previsões
print("Gerando gráfico de dispersão das previsões...")

# Criar um DataFrame com os dados de teste e as previsões
df_pred = X_test.copy()
df_pred['Valor Real'] = y_test
df_pred['Previsão do Modelo'] = y_pred

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_pred,
    x='temperatura',
    y='umidade',
    hue='Previsão do Modelo', # Colore os pontos pela previsão do modelo
    style='Valor Real',      # Define o estilo do marcador pelo valor real
    palette={0: 'green', 1: 'red'}, # Cores: Normal=Verde, Alerta=Vermelho
    s=100,                   # Tamanho dos pontos
    alpha=0.8                # Transparência
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
# Mostra o gráfico em uma nova janela
plt.show()