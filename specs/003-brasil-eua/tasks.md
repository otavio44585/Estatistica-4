# 003 — Tarefas: Brasil (PNS 2019 e Vigitel 2024)

| # | Tarefa | Depende | Pronto quando | Responsável |
|---|---|---|---|---|
| T040 | Decidir ferramenta para o desenho amostral (Python ou R) e registrar no plano | spec aprovada | decisão com data no plano | Claude (2026-11-27) — decisão no plano; `analise/brasil_eua/survey.py` |
| T041 | Função de modelo Poisson robusto com peso e cluster, testada contra a RP de Mantel-Haenszel da exploração | T040, 001 | diferença < 0,01 na RP ajustada só por idade | Claude (2026-11-27) — `tests/test_003_survey.py` (6 casos < 0,01) |
| T042 [P] | H3.1, H3.4 no Vigitel | T041 | linhas em `hipoteses.csv` | Claude (2026-11-27) — `resultados/003/tabelas/hipoteses.csv` |
| T043 [P] | H3.2, H3.4 na PNS | T041 | idem | Claude (2026-11-27) — `hipoteses.csv` |
| T044 [P] | ~~H3.3, H3.4 no NHANES~~ (retirada em 2026-11-27, EUA fora do trabalho) | T041 | idem | Claude (2026-11-27) — `hipoteses.csv` |
| T045 | ~~Base empilhada e H3.6~~ (retirada em 2026-11-27, EUA fora do trabalho) | T042, T044 | idem | Claude (2026-11-27) — `resultados/003/tabelas/comparacoes_entre_bases.csv` |
| T046 | H3.7 (idade × tela) no Vigitel e na PNS | T042–T044 | idem | Claude (2026-11-27) — `interacao_idade.csv`, `rp_por_faixa_etaria.csv` |
| T047 | H3.8 e H3.9 | T042–T044 | idem | Claude (2026-11-27) — `tv_vs_digital.csv`, `comparacoes_entre_bases.csv` |
| T048 | Sensibilidades (depressão, sem peso, corte ≥ 4 h, renda) | T042–T044 | tabela à parte | Claude (2026-11-27) — `sensibilidade.csv` (renda ausente no contrato) |
| T049 | Holm, tabela final e figura | T045–T047 | `hipoteses.csv` e `rp_por_pais.png` | Claude (2026-11-27) — `hipoteses.csv`, `figuras/rp_por_pais.png` |
| T050 | Notebook 04 com a narrativa dos testes (H0, H1, estatística, decisão) | T049 | roda de ponta a ponta | Claude (2026-11-27) — `analise/notebooks/04_testes_brasil_eua.ipynb` |
| T051 | Revisão contra a spec por outro integrante | T050 | critérios de aceite marcados | pendente — revisão do grupo |
