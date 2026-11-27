# 001 — Tarefas: dados harmonizados

`[P]` = pode rodar em paralelo com as outras `[P]` do mesmo bloco. Responsável a definir.

| # | Tarefa | Depende | Pronto quando | Responsável |
|---|---|---|---|---|
| T001 | `requirements.txt` com versões fixadas, `.gitignore`, pastas de `analise/`, `analise/comum/caminhos.py` lendo `STAT4_BRUTOS` | — | `python -c "import analise.comum.caminhos"` funciona nas máquinas de 2 integrantes | Claude (2026-11-27) — `requirements.txt`, `pytest.ini`, `analise/comum/caminhos.py` |
| T002 | `analise/comum/faltantes.py` com a tabela de códigos especiais por base | T001 | tabela cobre as 7 bases do núcleo | Claude (2026-11-27) — `analise/comum/faltantes.py` |
| T003 | `analise/comum/validacao.py` + `tests/test_faltantes.py` | T002 | teste falha com dado sujo de propósito e passa com dado limpo | Claude (2026-11-27) — `tests/test_001_faltantes.py` (falha com código 9 de propósito) |
| T004 [P] | Harmonizar PNS 2019 | T003 | parquet + log; n = 90.846 / 88.531; teste passa | Claude (2026-11-27) — `analise/dados/logs/pns2019.log`: 90.846 / 88.531 |
| T005 [P] | Harmonizar Vigitel 2024 | T003 | parquet + log; n = 27.048 | Claude (2026-11-27) — `logs/vigitel2024.log`: 27.048 |
| T006 [P] | Harmonizar NHANES 2005-06 (sono, atividade, demografia, PHQ-9); confirmar estrato e UPA | T003 | parquet + log; n = 6.139 / 5.563 | Claude (2026-11-27) — `logs/nhanes0506.log`: 6.139 / 5.563; `SDMVSTRA`/`SDMVPSU` presentes |
| T007 [P] | Harmonizar Xuzhou | T003 | parquet; n = 2.317 | Claude (2026-11-27) — `logs/xuzhou.log`: 2.317 |
| T008 [P] | Harmonizar Argentina (PDSS em texto → número) | T003 | parquet; n = 864 completos | Claude (2026-11-27) — `logs/argentina.log`: 864 |
| T009 [P] | Harmonizar Turquia | T003 | parquet; n = 1.216 | Claude (2026-11-27) — `logs/turquia.log`: 1.216 |
| T010 [P] | Harmonizar Japão (itens BPS invertidos) | T003 | parquet; n = 381 | Claude (2026-11-27) — `logs/japao.log`: 381 |
| T011 | `dicionario_harmonizado.csv` e `resultados/001/equivalencia.csv` | T004–T010 | toda variável do contrato presente ou marcada como ausente, com equivalência | Claude (2026-11-27) — `analise/dados/dicionario_harmonizado.csv`, `resultados/001/tabelas/equivalencia.csv` |
| T012 | Revisão contra a spec por outro integrante | T011 | critérios de aceite da spec marcados | pendente — revisão do grupo |
| T013 | (complementar) PNS 2013, PeNSE 2015, NHANES 2011–16 e demais | T011 | mesmo padrão | não executada (complementar) |
