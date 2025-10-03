import json
import pandas as pd
import matplotlib.pyplot as plt

# Ler cada linha do arquivo e converter de JSON para um dicionário
dados = []
with open('dados_brutos.txt', 'r') as f:
    for linha in f:
        try:
            dados.append(json.loads(linha))
        except json.JSONDecodeError:
            continue # Ignora linhas que não são JSON válido

# Criar um DataFrame do Pandas
df = pd.DataFrame(dados)

# Salvar como CSV para usar nas próximas etapas
df.to_csv('dados_sensores.csv', index=False)
print("Arquivo dados_sensores.csv criado com sucesso!")

# Criar um gráfico simples
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['temperatura'], marker='o', linestyle='-')
plt.title('Leituras de Temperatura do Sensor')
plt.xlabel('Ordem da Leitura')
plt.ylabel('Temperatura (°C)')
plt.grid(True)
plt.savefig('grafico_inicial.png') # Salva o gráfico como imagem
plt.show()
print("Gráfico inicial salvo como grafico_inicial.png")