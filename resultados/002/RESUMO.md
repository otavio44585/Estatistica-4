# 002 — Estrutura latente: resumo dos resultados

Executada em 2026-11-27 (`python -m analise.multivariada.analisa`; notebooks `analise/notebooks/02_pca_svd.ipynb` e `03_analise_fatorial.ipynb`). Cada número abaixo vem do CSV indicado em `resultados/002/tabelas/`.

**Como ler.** As hipóteses da 002 são decididas por **critérios descritivos** fixados na spec (análise paralela, cargas, coeficiente de Tucker, correlação entre escores), não por p-valor. O único teste com p é o de Bartlett, que confirma a existência de correlação entre os itens.

## Decisão sobre as hipóteses (`hipoteses.csv`)

| # | Conjunto | Critério | Valor obtido | Decisão |
|---|---|---|---|---|
| H2.1 | 3 sintomas, Vigitel 2024 | análise paralela retém 1 e cargas ≥ 0,50 | retém 1; menor carga 0,708; λ1 = 2,261 (75,4%) | atendido: 1 dimensão |
| H2.1 | 3 sintomas, NHANES 2005-06 | idem | retém 1; menor carga 0,631; λ1 = 2,120 (70,7%) | atendido: 1 dimensão |
| H2.2 | insônia, Vigitel × NHANES | Tucker φ ≥ 0,95 | φ = 0,998; maior diferença de carga 0,078 | atendido: equivalentes |
| H2.3 | PHQ-9, PNS × NHANES | mesmo nº de fatores e φ ≥ 0,95 | 1 fator nos dois; φ = 0,997; maior diferença 0,114 | atendido: equivalentes |
| H2.4 | item de sono do PHQ-9 | maior carga no mesmo fator | 1 fator retido nos dois países: o sono carrega no único fator (0,543 PNS; 0,549 NHANES) | atendido |
| H2.4 (exploratória) | idem, forçando 2 fatores | idem | o sono fica no fator do cansaço (somático) nos dois países: 0,597 PNS; 0,568 NHANES | atendido |
| H2.5 | SAS-SV, Xuzhou | análise paralela retém 1 | retém 2 (λ1 = 4,784; 47,8%) | não atendido: 2 dimensões |
| H2.5 | Doomscrolling (FK), Turquia | idem | retém 1 (λ1 = 8,750; 58,3%) | atendido: unidimensional |
| H2.5 | Procrastinação (UE), Turquia | idem | retém 2 (λ1 = 3,669; 40,8%) | não atendido: 2 dimensões |
| H2.5 | AIS, Japão | idem | retém 1 (λ1 = 4,690; 58,6%) | atendido: unidimensional |
| H2.5 | BPS, Japão | idem | retém 2 (λ1 = 3,822; 42,5%) | não atendido: 2 dimensões |
| H2.6 | 10 conjuntos | r(1º componente, escore fatorial) ≥ 0,95 | de 0,953 (SAS-SV) a 0,999 (doomscrolling) | atendido nos 10 |

A procrastinação da Turquia (UE) entrou em H2.5 porque a spec a cita na nota da hipótese. A solução de 2 fatores do PHQ-9 não foi retida pela análise paralela e está rotulada como exploratória.

## Adequação dos dados (`adequacao.csv`)

| Conjunto | n | α | KMO | Bartlett χ² (gl) | λ1 (% variância) | Kaiser | Paralela |
|---|---|---|---|---|---|---|---|
| 3 sintomas, Vigitel | 27.048 | 0,835 | 0,707 | 33.128 (3) | 2,261 (75,4%) | 1 | 1 |
| 3 sintomas, NHANES | 5.551 | 0,792 | 0,669 | 5.349 (3) | 2,120 (70,7%) | 1 | 1 |
| 7 sintomas de sono, NHANES | 5.520 | 0,833 | 0,826 | 14.839 (21) | 3,527 (50,4%) | 2 | 1 |
| PHQ-9, PNS 2019 | 88.531 | 0,856 | 0,903 | 291.781 (36) | 4,349 (48,3%) | 1 | 1 |
| PHQ-9, NHANES | 4.799 | 0,821 | 0,892 | 11.950 (36) | 3,897 (43,3%) | 1 | 1 |
| SAS-SV, Xuzhou | 2.317 | 0,877 | 0,864 | 11.200 (45) | 4,784 (47,8%) | 2 | 2 |
| Doomscrolling, Turquia | 1.216 | 0,947 | 0,956 | 12.808 (105) | 8,750 (58,3%) | 1 | 1 |
| Procrastinação, Turquia | 1.216 | 0,810 | 0,832 | 3.631 (36) | 3,669 (40,8%) | 2 | 2 |
| AIS, Japão | 381 | 0,897 | 0,891 | 1.661 (28) | 4,690 (58,6%) | 1 | 1 |
| BPS, Japão | 381 | 0,808 | 0,846 | 1.458 (36) | 3,822 (42,5%) | 2 | 2 |

O p de Bartlett é < 0,001 em todos os conjuntos.

## Números-chave

- **A PCA por SVD reproduz a referência.** Os autovalores σ²/(n − 1) batem com o `scikit-learn` e com os autovalores da matriz de correlação. No NHANES, 3 sintomas, a diferença máxima é de 6e-15 (notebook 02; `tests/test_002_resultados.py`).
- **A soma simples resume os 3 sintomas.** A correlação entre o índice 0–12 e o 1º componente é 0,9998 no Vigitel e no NHANES (`escores_correlacao.csv`). Isso sustenta o índice `insonia_idx` usado nas specs 003–005.
- **Robustez** (`robustez.csv`, `tucker.csv`):
  - A correlação policórica aumenta o 1º autovalor (PHQ-9 PNS: de 4,349 para 5,828), mas as cargas quase não mudam: Tucker com a solução de Pearson ≥ 0,994.
  - Com a policórica, Tucker BR × EUA = 0,999 para insônia e 0,999 para PHQ-9.
  - Ponderar pelo peso amostral quase não muda as cargas: Tucker ≥ 0,998 contra a solução sem peso.
- **7 sintomas de sono (NHANES).** O critério de Kaiser apontaria 2 componentes, porque λ2 = 1,032 fica pouco acima de 1. A análise paralela retém 1, porque o P95 aleatório é 1,043 (`pca_autovalores.csv`). No biplot, o 2º componente separa os sintomas noturnos dos diurnos.
- **Soluções com 2 fatores** (`af_cargas.csv`, `af_phi.csv`, figura `cargas_multifator.png`):
  - **BPS (Japão):** o 2º fator reúne exatamente os itens de redação invertida (BPS2R, 3R, 7R, 9R), com Φ = 0,188. O padrão é compatível com um fator de método.
  - **SAS-SV:** um fator de "abstinência" (impaciente, inquieto, não suporta ficar sem o celular) e outro de "perturbação da rotina", com Φ = 0,607.
  - **Procrastinação (Turquia):** UE2, 3, 6 e 7 separados dos demais, com Φ = 0,383. Sem codebook, não há como dizer se é efeito de redação.
- **PHQ-9 com 2 fatores (exploratório).** A composição difere entre os países: Tucker 0,852 e 0,859, "similar" mas não "igual". Na PNS, o fator do cansaço também absorve interesse, concentração e psicomotor. No NHANES, ele se limita a sono, cansaço e apetite.

## Limitações

- Com 3 itens, o modelo de 1 fator é exatamente identificado: não há graus de liberdade para testar o ajuste. A evidência de unidimensionalidade vem da análise paralela e das cargas.
- O coeficiente de Tucker tende a sair alto quando todas as cargas são positivas. Por isso o `tucker.csv` traz também a maior diferença absoluta entre cargas: 0,078 na insônia e 0,114 no PHQ-9.
- Tucker não é um teste formal de invariância. A AFC multigrupo ficou fora do escopo da spec.
- Os itens são ordinais e a análise principal usa Pearson. A policórica entrou como robustez e não mudou as conclusões.
- A AF não usa o desenho amostral; a correlação ponderada entra só como sensibilidade. No NHANES, o PHQ-9 foi ponderado com `WTINT2YR`, mas o peso apropriado ao exame no centro móvel (`WTMEC2YR`) não está no contrato da 001.
- Os itens FK, UE e BPS não têm rótulo de conteúdo nos depósitos, e a interpretação dos fatores de UE é limitada.
- Comparação de época: NHANES de 2005-06 × PNS 2019 e Vigitel 2024.
- Os limites de Tucker foram conferidos no resumo do artigo (Lorenzo-Seva; ten Berge, 2006, doi:10.1027/1614-2241.2.2.57) registrado no Crossref: 0,85–0,94 = similaridade razoável; acima de 0,95 = iguais. O limiar prático KMO ≥ 0,60 citado no notebook continua "a verificar".

## Arquivos

- **Tabelas:** `adequacao.csv`, `itens.csv` (descritiva, MSA, α sem o item, correlação item-total, cargas), `pca_autovalores.csv` (com P95 da análise paralela), `af_cargas.csv`, `af_phi.csv`, `tucker.csv`, `phq9_item_sono.csv`, `escores_correlacao.csv`, `robustez.csv`, `hipoteses.csv`, `correlacao_*.csv` e `correlacao_policorica_*.csv`.
- **Figuras:** `scree_todos.png`, `cargas_insonia_br_eua.png`, `cargas_phq9_br_eua.png`, `biplot_sono7_nhanes.png`, `cargas_multifator.png`.
- **Escores:** `analise/dados/processados/escores_<base>.parquet`, com o 1º componente, o escore fatorial e a soma de cada instrumento (fora do git).
