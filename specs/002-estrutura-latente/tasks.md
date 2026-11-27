# 002 — Tarefas: PCA e análise fatorial

| # | Tarefa | Depende | Pronto quando | Responsável |
|---|---|---|---|---|
| T020 | Instalar `factor_analyzer`, fixar versão em `requirements.txt` e testar import | 001 | import funciona em 2 máquinas | Claude (2026-11-27) — factor_analyzer 0.5.1 instalado, mas o `fit` é incompatível com o scikit-learn 1.9; AF própria (`analise/comum/multivariada.py`) |
| T021 | `analise/comum/multivariada.py`: KMO, MSA, Bartlett, α, PCA-SVD, análise paralela, Tucker | T020 | testes: autovalores da PCA-SVD = `sklearn` até 1e-8; KMO = `factor_analyzer` até 1e-6 | Claude (2026-11-27) — `tests/test_002_multivariada.py` (autovalores = sklearn até 1e-8; KMO = factor_analyzer até 1e-6; AF e rotações conferidas) |
| T022 [P] | 3 sintomas de insônia: Vigitel | T021 | tabelas e figuras em `resultados/002/` | Claude (2026-11-27) — `resultados/002/tabelas/` (`insonia3_vigitel`) |
| T023 [P] | 3 sintomas de insônia e 7 sintomas de sono: NHANES | T021 | idem | Claude (2026-11-27) — `resultados/002/tabelas/` (`insonia3_nhanes`, `sono7_nhanes`), `biplot_sono7_nhanes.png` |
| T024 | Decidir e implementar a correlação policórica | T021 | método escrito no plano; teste com dado simulado de correlação conhecida | Claude (2026-11-27) — policórica de Olsson (dois passos), teste com ρ = 0,6 conhecido em `tests/test_002_multivariada.py` |
| T025 [P] | PHQ-9: PNS 2019 | T021 | idem T022 | Claude (2026-11-27) — `phq9_pns` em `adequacao.csv`, `af_cargas.csv` |
| T026 [P] | PHQ-9: NHANES | T021 | idem | Claude (2026-11-27) — `phq9_nhanes` em `adequacao.csv`, `af_cargas.csv` |
| T027 | Congruência de Tucker: insônia BR × EUA e PHQ-9 BR × EUA | T022, T023, T025, T026 | tabela de φ; H2.2 a H2.4 respondidas | Claude (2026-11-27) — `tucker.csv`, `phq9_item_sono.csv`, `hipoteses.csv` (H2.2–H2.4) |
| T028 [P] | SAS-SV (Xuzhou), doomscrolling e procrastinação (Turquia), AIS e BPS (Japão) | T021 | H2.5 respondida por conjunto | Claude (2026-11-27) — `hipoteses.csv` (H2.5), `cargas_multifator.png` |
| T029 | Comparação PCA × AF e correlação dos escores | T022–T028 | H2.6 respondida | Claude (2026-11-27) — `escores_correlacao.csv` (H2.6) |
| T030 | Robustez: policórica e correlação ponderada | T024, T027 | comparação com Pearson tabelada | Claude (2026-11-27) — `robustez.csv` |
| T031 | Exportar escores para 003 e 004 | T029 | parquets em `analise/dados/processados/` | Claude (2026-11-27) — `analise/dados/processados/escores_<base>.parquet` (6 bases) |
| T032 | Notebooks 02 e 03 com a narrativa das técnicas | T029 | rodam de ponta a ponta sem erro a partir dos processados | Claude (2026-11-27) — `analise/notebooks/02_pca_svd.ipynb`, `03_analise_fatorial.ipynb` (executados) |
| T033 | Revisão contra a spec por outro integrante | T032 | critérios de aceite marcados | pendente — revisão do grupo |
