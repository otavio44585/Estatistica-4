# Relatório Analítico: Insônia Digital

## 1. Visão Geral do Projeto
Este trabalho analisa o impacto do tempo de exposição a telas antes de dormir sobre a latência do sono (tempo necessário para adormecer). 

## 2. Estrutura de Arquivos
- **`/dataset`**: Contém o arquivo `dados_insonia.csv` com a amostra de 100 usuários.
- **`/codigo`**: Contém o script `treinar_modelo.py` que treina a máquina via Regressão Linear.
- **`/relatorio`**: Pasta para armazenar este documento e os gráficos gerados pela IA.

## 3. Metodologia Estatística
A máquina foi treinada utilizando **Regressão Linear Simples**. A variável independente (X) é o tempo de tela em minutos, e a variável dependente (Y) é o tempo para adormecer. 80% dos dados foram usados para treino e 20% para teste.

## 4. Como Executar
1. Certifique-se de ter o Python instalado com as bibliotecas `pandas`, `scikit-learn` e `matplotlib`.
2. Navegue até a pasta `codigo` no seu terminal.
3. Rode o comando: `python treinar_modelo.py`
4. Os resultados aparecerão no terminal e o gráfico será salvo automaticamente nesta pasta `/relatorio`.
