# 002 — Plano: PCA e análise fatorial

Status: executado (2026-11-27).

## Viabilidade já medida (exploratória, Pearson, casos completos)

| Base | Itens | n | α | KMO | Autovalores > 1 |
|---|---|---|---|---|---|
| Vigitel 2024 | 3 sintomas de insônia | 27.048 | 0,84 | 0,71 | 1 (75%) |
| NHANES 2005-06 | 3 sintomas de insônia | 5.551 | 0,79 | 0,67 | 1 (71%) |
| NHANES 2005-06 | 7 sintomas de sono `SLQ080`–`SLQ140` | 6.093 | 0,83 | 0,83 | 2 (65%) |
| PNS 2019 | PHQ-9 | 88.531 | 0,86 | 0,90 | 1 (48%) |
| NHANES 2005-06 | PHQ-9 | 4.799 | 0,82 | 0,89 | 1 (43%) |
| Xuzhou | SAS-SV | 2.317 | 0,88 | 0,86 | 2 (60%) |
| Turquia | doomscrolling / procrastinação | 1.216 | 0,95 / 0,81 | 0,96 / 0,83 | 1 / 2 |
| Japão | AIS / BPS | 381 | 0,90 / 0,81 | 0,89 / 0,85 | 1 / 2 |

## Técnicas e como cada uma é mostrada

| Passo | Implementação | O que vai para o notebook |
|---|---|---|
| Padronização | Z = (X − média) / DP | médias e DP por item |
| Adequação | KMO e MSA pela matriz de correlação parcial (inversa de R); Bartlett χ² = −(n − 1 − (2p + 5)/6) · ln det R, gl = p(p − 1)/2 | fórmulas e valores |
| **PCA por SVD** | `numpy.linalg.svd(Z, full_matrices=False)`: Z = U Σ Vᵀ; autovalores λᵢ = σᵢ² / (n − 1); cargas = V · Σ / √(n − 1); escores = U · Σ | matriz Σ, tabela de variância explicada, scree, biplot; conferência com `sklearn.decomposition.PCA` |
| Número de fatores | Kaiser (λ > 1); scree; análise paralela de Horn (1.000 matrizes aleatórias de mesmo n e p, percentil 95) | gráfico com as três referências |
| Análise fatorial | implementação própria em `analise/comum/multivariada.py` (o `FactorAnalyzer.fit` do factor_analyzer 0.5.1 não roda com o scikit-learn 1.9): máxima verossimilhança, eixos principais iterados; varimax e oblimin (gradiente projetado, com normalização de Kaiser); conferida contra o factor_analyzer nos testes | cargas, comunalidades, unicidades, Φ (correlação entre fatores) |
| Escores fatoriais | método de regressão (Thurstone) | correlação com o escore da PCA |
| Congruência | Tucker φ = Σ aᵢbᵢ / √(Σaᵢ² · Σbᵢ²) sobre as cargas de cada par de bases | tabela de φ |
| Robustez | correlação policórica em dois passos (Olsson, 1979): limiares pelas marginais e ρ por máxima verossimilhança da tabela cruzada (decisão da T024); matriz corrigida para positiva definida se preciso; correlação ponderada pelo peso amostral | comparação com a solução de Pearson |

`analise/comum/multivariada.py` concentra as funções (KMO, Bartlett, α, PCA-SVD, análise paralela, Tucker), com testes contra implementações de referência.

## Saídas

- `analise/notebooks/02_pca_svd.ipynb` e `03_analise_fatorial.ipynb`, com a narrativa de cada técnica.
- `resultados/002/tabelas/*.csv` e `resultados/002/figuras/*.png`.
- `analise/dados/processados/escores_<base>.parquet`.

## Riscos

| Risco | Efeito | Mitigação |
|---|---|---|
| 3 itens são o mínimo para um fator | solução justa, sem graus de liberdade para testar ajuste | tratar os 3 sintomas como índice validado por PCA e AF; comparar com os 7 sintomas do NHANES |
| Itens ordinais com Pearson | cargas subestimadas | policórica como robustez |
| AF não aceita peso amostral | estimativa não populacional | declarar; sensibilidade com correlação ponderada |
| `factor_analyzer` incompatível com o scikit-learn 1.9 | `fit` falha | AF própria, testada contra o factor_analyzer com um adaptador do `check_array` nos testes |

## Histórico

- 2026-11-27: executado. Código em `analise/comum/multivariada.py` (funções) e `analise/multivariada/` (`conjuntos.py`, `analisa.py`, `notebooks.py`). Análise paralela com 1.000 réplicas, P95, semente 2026 + índice do conjunto. Policórica feita em 6 conjuntos (3 sintomas × 2, PHQ-9 × 2, 7 sintomas, AIS); correlação ponderada nos 5 conjuntos de inquérito. No NHANES, o PHQ-9 ponderado usa `WTINT2YR` (o `WTMEC2YR` não está no contrato da 001). Tempo total da análise: cerca de 25 s.
- 2026-11-27: EUA fora do trabalho (decisão do grupo). As linhas do NHANES na tabela de viabilidade ficam como registro histórico. Os conjuntos `insonia3_nhanes`, `sono7_nhanes` e `phq9_nhanes` e os pares de Tucker entre países saíram de `analise/multivariada/conjuntos.py`. O passo a passo da PCA (notebook 02) passou a usar o Vigitel 2024 e o da AF (notebook 03), o PHQ-9 da PNS. Novas saídas: `vigitel_indice.csv`, `vigitel_indice_resumo.csv`, `cargas_insonia_vigitel.png` e `biplot_phq9_pns.png`. Removidas: `cargas_insonia_br_eua.png`, `cargas_phq9_br_eua.png`, `biplot_sono7_nhanes.png` e as correlações do NHANES. `tucker.csv` ficou só com o cabeçalho.
