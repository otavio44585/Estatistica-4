# 004 — Tarefas: comparação mundial

| # | Tarefa | Depende | Pronto quando | Responsável |
|---|---|---|---|---|
| T060 | Fixar a tabela de pares exposição × desfecho (um principal por base) | spec aprovada | tabela no plano, com data | Claude (2026-11-27) — tabela de pares no plano (seção "Pares fixados"); `analise/mundial/pares.py` |
| T061 | Verificar a fonte da aproximação do EP de Spearman e implementar Fisher | T060 | referência conferida ou trocada por bootstrap | Claude (2026-11-27) — DOI conferido; bootstrap × fórmula em `resultados/004/tabelas/efeitos_por_base.csv` (máx. 5,4%) |
| T062 [P] | Calcular ρ e r por base | T061, 001 | `efeitos_por_base.csv` | Claude (2026-11-27) — `resultados/004/tabelas/efeitos_por_base.csv` |
| T063 | Meta-análise de efeitos aleatórios, Q, I², τ² (H4.1) | T062 | `meta_analise.csv`; combinado igual ao cálculo manual | Claude (2026-11-27) — `meta_analise.csv`; `conferencia_statsmodels.csv` (diferença ≤ 6e-14) |
| T064 | Subgrupos por tipo de exposição (H4.2) | T063 | Q entre subgrupos | Claude (2026-11-27) — `hipoteses.csv` (H4.2: Q entre = 5,27, gl = 2) |
| T065 | Brasil × demais com tempo total (H4.3) e referência da literatura (H4.4) | T063 | linhas em `meta_analise.csv` | Claude (2026-11-27) — `hipoteses.csv` (H4.3, H4.4); `exploratorio_referencia.csv` |
| T066 | Sensibilidade: deixar uma de fora; procedência questionável à parte; correlação com peso | T063 | tabela à parte | Claude (2026-11-27) — `sensibilidade.csv`, `bruta_ajustada_idade.csv` |
| T067 | Gráfico de floresta | T063–T065 | `floresta.png` com Brasil destacado | Claude (2026-11-27) — `resultados/004/figuras/floresta.png` |
| T068 | Notebook 05 com a narrativa | T067 | roda de ponta a ponta | Claude (2026-11-27) — `analise/notebooks/05_comparacao_mundial.ipynb` (executado por `analise/mundial/notebook.py`) |
| T069 | Revisão contra a spec por outro integrante | T068 | critérios de aceite marcados | pendente — revisão do grupo |
