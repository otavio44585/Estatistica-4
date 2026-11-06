import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import os

# Ajustando o diretório de trabalho caso seja executado de fora
caminho_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carregando os dados do dataset
caminho_csv = os.path.join(caminho_base, 'dataset', 'dados_insonia.csv')
df = pd.read_csv(caminho_csv)

# Preparando os dados
X = df[['Tempo_Tela_Min']]
y = df['Tempo_Adormecer_Min']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinando a máquina
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Avaliando
previsoes = modelo.predict(X_test)
r2 = r2_score(y_test, previsoes)
coeficiente = modelo.coef_[0]

print("--- RESULTADOS DO MODELO ---")
print(f"Precisão do modelo (R²): {r2:.2f}")
print(f"Impacto da Tela: Para cada 1 minuto de tela, o atraso no sono é de {coeficiente:.2f} minutos.")

# Gerando e salvando o gráfico
plt.figure(figsize=(8,5))
plt.scatter(X_test, y_test, color='blue', label='Dados Reais')
plt.plot(X_test, previsoes, color='red', linewidth=2, label='Previsão do Modelo')
plt.title('Impacto da Insônia Digital no Atraso do Sono')
plt.xlabel('Tempo de Tela Antes de Dormir (Minutos)')
plt.ylabel('Tempo para Adormecer (Minutos)')
plt.legend()
plt.grid(True)

# Salvando o gráfico direto na pasta do relatório
caminho_grafico = os.path.join(caminho_base, 'relatorio', 'grafico_resultado.png')
plt.savefig(caminho_grafico)
print(f"\nGráfico de resultados salvo com sucesso em: {caminho_grafico}")
