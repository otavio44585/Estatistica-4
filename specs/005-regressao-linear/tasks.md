# 005 — Tarefas: regressão linear múltipla, ANOVA e teste t

| # | Tarefa | Depende | Pronto quando | Responsável |
|---|---|---|---|---|
| T080 | Confirmar o rótulo de `FK_TOPLAM` (Turquia) no depósito ou no artigo; decidir se H5.5 é confirmatória | spec aprovada | decisão registrada no histórico da spec | Claude (2026-11-27) — decisão no Histórico da spec |
| T081 | `analise/regressao/ols.py`: MQO por álgebra matricial (b, EP, t, p, IC, ANOVA, R², R² ajustado, F parcial) | T001 | reproduz o exercício 2 da aula com diferença relativa < 1e-9 e bate com `statsmodels` | Claude (2026-11-27) — `analise/regressao/ols.py`; `tests/test_005_confere_excel.py` (diferença < 1e-9 no exercício 2) |
| T082 | `tests/test_confere_excel.py` e `tests/test_consistencia.py` | T081 | testes passam; falham com um p alterado de propósito | Claude (2026-11-27) — `tests/test_005_confere_excel.py`, `tests/test_005_consistencia.py` (falham com p alterado de propósito) |
| T083 | `analise/regressao/prepara_excel.py` gera `<base>_dados.xlsx` das 6 bases | T081, T005–T010 | planilhas e log de n por base | Claude (2026-11-27) — `analise/regressao/prepara_excel.py` → `analise/dados/excel/<base>_resultados.xlsx` (aba `log`) |
| T084 | `PROTOCOLO_EXCEL.md`, testado primeiro no Japão (menor base) | T083 | outro integrante segue o protocolo sem ajuda e a conferência passa | Claude (2026-11-27) — `analise/regressao/PROTOCOLO_EXCEL.md` (teste por outro integrante pendente) |
| T085 [P] | Excel: Japão, Argentina, Turquia e Xuzhou (Regressão simples, Regressão com covariáveis, Regressão só com covariáveis) | T084 | `<base>_resultados.xlsx` com as abas do protocolo | Claude (2026-11-27) — ToolPak automatizado: `roda_excel.py`, saídas em `resultados/005/excel_saidas/` |
| T086 [P] | Excel: Vigitel e NHANES sem peso (Regressões, ANOVA de um fator e Teste-t) | T084 | idem | Claude (2026-11-27) — idem (Vigitel e NHANES, com ANOVA e testes t) |
| T087 | `analise/regressao/modelos.py`: todos os modelos no script, sem peso e com peso (Vigitel, NHANES) | T081, T040 | tabelas `summary_*.csv` em `resultados/005/` | Claude (2026-11-27) — `analise/regressao/modelos.py` → `resultados/005/tabelas/summary_*.csv` |
| T088 | `analise/regressao/confere_excel.py`: caminhos A × B × C | T085–T087 | `conferencia.csv` sem falha | Claude (2026-11-27) — `resultados/005/conferencia.csv` (920 números, 0 falhas) |
| T089 | Base empilhada Vigitel + NHANES e H5.11 | T087 | linha em `hipoteses.csv` | Claude (2026-11-27) — `hipoteses.csv`, linha H5.11 |
| T090 | Diagnóstico de pressupostos e sensibilidades (HC3, log da latência, sem influentes, horas de sono) | T087 | figuras e tabela de sensibilidade | Claude (2026-11-27) — `tabelas/diagnostico.csv`, `tabelas/sensibilidade.csv`, `figuras/diagnostico_*.png` |
| T091 | Holm nas famílias R1 e R2 e tabela final | T088–T090 | `hipoteses.csv` completo | Claude (2026-11-27) — `resultados/005/tabelas/hipoteses.csv` |
| T092 | Notebook 06: fórmulas, saída do Excel, conferência e decisão de cada hipótese | T091 | roda de ponta a ponta a partir dos processados | Claude (2026-11-27) — `analise/notebooks/06_regressao_linear.ipynb` (executado, sem erro) |
| T093 | Revisão contra a spec por outro integrante | T092 | critérios de aceite marcados | pendente — revisão do grupo |
