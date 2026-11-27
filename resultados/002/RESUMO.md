# 002 — Estrutura latente: resumo dos resultados

Executada em 2026-11-27 (`python -m analise.multivariada.analisa`; notebooks `analise/notebooks/02_pca_svd.ipynb` e `03_analise_fatorial.ipynb`). Cada número abaixo vem do CSV indicado em `resultados/002/tabelas/`.

> **2026-11-27: EUA fora do trabalho.** A única base americana (NHANES) é de 2005-06, antes do smartphone, e saiu do trabalho por decisão do grupo. Saíram os conjuntos do NHANES e as comparações Brasil × EUA. **H2.2, H2.3 e H2.4 foram retiradas** (ver o Histórico da spec).

**Como ler.** As hipóteses da 002 são decididas por **critérios descritivos** fixados na spec (análise paralela, cargas, correlação entre escores), não por p-valor. O único teste com p é o de Bartlett, que só confirma que há correlação a modelar.

## Índice de insônia do Vigitel 2024 (`vigitel_indice.csv`, `vigitel_indice_resumo.csv`)

Juntamos as três perguntas de insônia do Vigitel 2024, respondidas de 1 (nunca) a 5 (sempre) e recodificadas para 0 a 4. A soma delas, de 0 a 12, é o índice de insônia.

| Pergunta (variável) | Carga na PCA | Carga na AF | Comunalidade | MSA | α sem o item |
|---|---|---|---|---|---|
| Dificuldade para dormir (`r703`) | 0,834 | 0,708 | 0,501 | 0,776 | 0,824 |
| Acordou e teve dificuldade para dormir de novo (`r704`) | 0,899 | 0,885 | 0,783 | 0,663 | 0,718 |
| Acordou antes da hora e não dormiu de novo (`r705`) | 0,871 | 0,793 | 0,629 | 0,702 | 0,770 |

| Indicador | Valor | Leitura |
|---|---|---|
| n | 27.048 | adultos com as 3 respostas |
| α de Cronbach | 0,835 | as perguntas andam juntas (consistência interna) |
| KMO | 0,707 | as correlações vêm de algo comum às três perguntas |
| Bartlett | χ² = 33.128, gl = 3, p < 0,001 | há correlação a modelar |
| Autovalores (PCA) | 2,261; 0,450; 0,289 | só o 1º passa de 1 |
| Análise paralela (P95 aleatório) | 1,017; 1,004 | retém 1 fator |
| Variância do 1º componente | 75,4% | — |
| Variância comum (AF, 1 fator) | 63,8% | — |
| Correlação soma × 1º componente | 0,9998 | a soma 0–12 resume o fator |

O **α de Cronbach** vai de 0 a 1 e mede se as perguntas "andam juntas". O **KMO** vai de 0 a 1 e mede se a correlação entre as perguntas vem de algo comum a todas; o MSA é o KMO de cada pergunta.

## Decisão sobre as hipóteses (`hipoteses.csv`)

| # | Conjunto | Critério | Valor obtido | Decisão |
|---|---|---|---|---|
| H2.1 | 3 sintomas, Vigitel 2024 | análise paralela retém 1 e cargas ≥ 0,50 | retém 1; menor carga 0,708; λ1 = 2,261 (75,4%) | atendido: 1 dimensão |
| H2.2 | — | Tucker entre Brasil e EUA | — | retirada em 2026-11-27 (EUA fora do trabalho) |
| H2.3 | — | PHQ-9 com a mesma estrutura na PNS e no NHANES | — | retirada em 2026-11-27 (EUA fora do trabalho) |
| H2.4 | — | item de sono do PHQ-9 no mesmo fator nos dois países | descritivo, só PNS: carga 0,543 no único fator | retirada em 2026-11-27 (EUA fora do trabalho) |
| H2.5 | SAS-SV, China | análise paralela retém 1 | retém 2 (λ1 = 4,784; 47,8%) | não atendido: 2 dimensões |
| H2.5 | Doomscrolling (FK), Turquia | idem | retém 1 (λ1 = 8,750; 58,3%) | atendido: unidimensional |
| H2.5 | Procrastinação (UE), Turquia | idem | retém 2 (λ1 = 3,669; 40,8%) | não atendido: 2 dimensões |
| H2.5 | AIS, Japão | idem | retém 1 (λ1 = 4,690; 58,6%) | atendido: unidimensional |
| H2.5 | BPS, Japão | idem | retém 2 (λ1 = 3,822; 42,5%) | não atendido: 2 dimensões |
| H2.6 | 7 conjuntos | r(1º componente, escore fatorial) ≥ 0,95 | de 0,953 (SAS-SV) a 0,999 (doomscrolling) | atendido nos 7 |

A procrastinação da Turquia (UE) entrou em H2.5 porque a spec a cita na nota da hipótese.

## Quais itens entraram em cada PCA (`itens.csv`)

| Conjunto | Base | Itens |
|---|---|---|
| Índice de insônia | Vigitel 2024 | r703, r704, r705 (acima) |
| PHQ-9 | PNS 2019 | interesse, humor deprimido, sono, cansaço, apetite, fracasso, concentração, lentidão/agitação, autolesão |
| SAS-SV | China | 10 itens de uso problemático do celular (abstinência e perturbação da rotina) |
| Doomscrolling | Turquia | FK1 a FK15 (sem rótulo de conteúdo) |
| Procrastinação do sono | Turquia | UE1 a UE9 (sem rótulo) |
| AIS | Japão | 8 itens de insônia (indução, despertares, despertar precoce, duração, qualidade, bem-estar, funcionamento, sonolência) |
| BPS | Japão | 9 itens, 4 de redação invertida |

## Adequação dos dados (`adequacao.csv`)

| Conjunto | n | α | KMO | Bartlett χ² (gl) | λ1 (% variância) | Kaiser | Paralela |
|---|---|---|---|---|---|---|---|
| 3 sintomas, Vigitel | 27.048 | 0,835 | 0,707 | 33.128 (3) | 2,261 (75,4%) | 1 | 1 |
| PHQ-9, PNS 2019 | 88.531 | 0,856 | 0,903 | 291.781 (36) | 4,349 (48,3%) | 1 | 1 |
| SAS-SV, China | 2.317 | 0,877 | 0,864 | 11.200 (45) | 4,784 (47,8%) | 2 | 2 |
| Doomscrolling, Turquia | 1.216 | 0,947 | 0,956 | 12.808 (105) | 8,750 (58,3%) | 1 | 1 |
| Procrastinação, Turquia | 1.216 | 0,810 | 0,832 | 3.631 (36) | 3,669 (40,8%) | 2 | 2 |
| AIS, Japão | 381 | 0,897 | 0,891 | 1.661 (28) | 4,690 (58,6%) | 1 | 1 |
| BPS, Japão | 381 | 0,808 | 0,846 | 1.458 (36) | 3,822 (42,5%) | 2 | 2 |

O p de Bartlett é < 0,001 em todos os conjuntos.

## Números-chave

- **A PCA por SVD reproduz a referência.** Os autovalores σ²/(n − 1) batem com o `scikit-learn` e com os autovalores da matriz de correlação até 10⁻⁸ (notebook 02, no Vigitel; `tests/test_002_resultados.py`).
- **A soma simples resume os instrumentos.** A correlação entre a soma e o 1º componente é 0,9998 no índice de insônia do Vigitel e 0,995 no PHQ-9 da PNS (`escores_correlacao.csv`).
- **Robustez** (`robustez.csv`, coluna `tucker_vs_pearson`, que compara as cargas com as da solução de Pearson na mesma base):
  - A correlação policórica aumenta o 1º autovalor (Vigitel: de 2,261 para 2,382; PHQ-9 PNS: de 4,349 para 5,828), mas as cargas quase não mudam (Tucker ≥ 0,995).
  - Ponderar pelo peso amostral quase não muda as cargas (Tucker 1,000).
- **PHQ-9 da PNS com 2 fatores (exploratório).** O item de sono fica no fator do cansaço (somático), com carga 0,597, separado do humor deprimido; Φ = 0,692 entre os fatores (`phq9_item_sono.csv`, `af_phi.csv`). No biplot (`biplot_phq9_pns.png`), o 2º componente separa sono e cansaço de fracasso e autolesão.
- **Soluções com 2 fatores** (`af_cargas.csv`, `af_phi.csv`, figura `cargas_multifator.png`):
  - **BPS (Japão):** o 2º fator reúne exatamente os itens de redação invertida (BPS2R, 3R, 7R, 9R), com Φ = 0,188. O padrão é compatível com um fator de método.
  - **SAS-SV:** um fator de "abstinência" (impaciente, inquieto, não suporta ficar sem o celular) e outro de "perturbação da rotina", com Φ = 0,607.
  - **Procrastinação (Turquia):** UE2, 3, 6 e 7 separados dos demais, com Φ = 0,383. Sem codebook, não há como dizer se é efeito de redação.

## Limitações

- Com 3 itens, o modelo de 1 fator é exatamente identificado: não há graus de liberdade para testar o ajuste. A evidência de unidimensionalidade vem da análise paralela e das cargas.
- Os itens são ordinais e a análise principal usa Pearson. A policórica entrou como robustez e não mudou as conclusões.
- A AF não usa o desenho amostral; a correlação ponderada entra só como sensibilidade.
- Os itens FK, UE e BPS não têm rótulo de conteúdo nos depósitos, e a interpretação dos fatores de UE é limitada.
- A regra prática de KMO ≥ 0,60 citada no notebook continua "a verificar" na fonte.

## Arquivos

- **Tabelas:** `vigitel_indice.csv` e `vigitel_indice_resumo.csv` (índice de insônia do Vigitel, para a apresentação), `adequacao.csv`, `itens.csv` (descritiva, MSA, α sem o item, correlação item-total, cargas), `pca_autovalores.csv` (com P95 da análise paralela), `af_cargas.csv`, `af_phi.csv`, `phq9_item_sono.csv`, `escores_correlacao.csv`, `robustez.csv`, `correlacao_*.csv`. O `tucker.csv` ficou só com o cabeçalho: não há mais comparação entre países.
- **Figuras:** `cargas_insonia_vigitel.png`, `biplot_phq9_pns.png`, `scree_todos.png`, `cargas_multifator.png`.
- **Escores:** `analise/dados/processados/escores_<base>.parquet`, com o 1º componente, o escore fatorial e a soma de cada instrumento (fora do git).
