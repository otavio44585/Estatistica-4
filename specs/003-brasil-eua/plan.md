# 003 — Plano: Brasil (PNS 2019 e Vigitel 2024)

Status: executado (2026-11-27).

## Modelos

| Hipótese | Modelo | Estatística |
|---|---|---|
| H3.1–H3.2 | Poisson com ligação log e variância robusta: `desfecho ~ tela_cat + faixa_etaria + sexo + escolaridade3`, com peso amostral | exp(β) = RP; teste de Wald (z) |
| H3.4 | mesmo modelo com a exposição como escore 0/1/2 | Wald do coeficiente linear |
| ~~H3.6~~ | retirada em 2026-11-27 (EUA fora do trabalho) | — |
| H3.7 | `+ faixa_etaria:tela_cat` | Wald conjunto da interação |
| H3.8 | TV e digital no mesmo modelo, ou modelos separados com teste z da diferença | z |
| H3.9 | teste z sobre a diferença dos log-RP de PNS e Vigitel | z |

Sem base empilhada desde 2026-11-27 (era Vigitel + NHANES, para H3.6). H3.9 compara PNS e Vigitel por teste z dos log-RP de modelos separados.

## Desenho amostral

| Base | Peso | Estrato | UPA |
|---|---|---|---|
| PNS 2019 | `V00291` | `V0024` | `UPA_PNS` |
| Vigitel 2024 | `pesorake2025` | — | — (inquérito telefônico; só peso) |

**Decisão de ferramenta — T040, 2026-11-27: Python**, porque o R não está instalado na máquina de referência (`Rscript` não encontrado). A variância é a da linearização com estrato e UPA, como no `svyglm`, implementada em `analise/brasil_eua/survey.py`. Opções avaliadas:

| Opção | Como | A favor | Contra |
|---|---|---|---|
| Python | `statsmodels` GLM Poisson com `var_weights` e erro padrão robusto por cluster (UPA) | um só ambiente; já instalado | aproxima o desenho: não usa o estrato, e o IC tende a ficar conservador |
| R | pacote `survey` (`svydesign` + `svyglm`, família quasipoisson) | variância por linearização com estrato e UPA, referência para inquérito complexo | segunda linguagem no projeto; R não verificado na máquina |

## Correção para múltiplos testes

Holm separadamente na família 1 (H3.1–H3.4, por exposição) e na família 2 (H3.6–H3.9). A regressão linear (antiga H3.5) está na spec 005, com famílias próprias.

## Saídas

- `analise/notebooks/04_testes_brasil_eua.ipynb` (gerado e executado por `python -m analise.brasil_eua.notebook`).
- `resultados/003/RESUMO.md` (gerado por `python -m analise.brasil_eua.resumo`).
- `resultados/003/tabelas/hipoteses.csv` (uma linha por hipótese: estimativa, IC, estatística, p, p Holm, decisão).
- `resultados/003/figuras/rp_por_pais.png`.

## Riscos

| Risco | Efeito | Mitigação |
|---|---|---|
| EUA retirados em 2026-11-27 | sem comparação internacional nesta spec | a comparação com outros países fica na 004 |
| Item da PNS diferente do Vigitel | H3.9 mistura pesquisa e item | declarado como limitação; H3.9 compara as duas pesquisas brasileiras sem pretender equivalência de item |
| Poisson com variância robusta não converge em subgrupos pequenos | sem estimativa | juntar faixas etárias; reportar o n por célula |

## Histórico

- 2026-11-27: executado. Comparação de erros padrão em `resultados/003/tabelas/comparacao_variancia.csv`: na PNS, linearização e cluster do `statsmodels` quase coincidem (8.027 UPAs); no NHANES diferem em até 10% porque o cluster do `statsmodels` não centra dentro do estrato e aplica outra correção de pequena amostra. Com um só estrato e sem correção, os dois métodos coincidem após o fator G/(G − 1) (`tests/test_003_survey.py`). Nenhum estrato com uma só UPA nas amostras analisadas. A T041 bateu: Poisson ajustado só por faixa etária × Mantel-Haenszel da exploração, diferença < 0,01 nas 6 combinações.
- 2026-11-27: correções da verificação independente.
  - `survey.py` ganhou:
    - Korn-Graubard em `Ajuste.wald`;
    - estimação por domínio (`dominio=`);
    - `gl_svyglm()` (d − p + 1) e `satterthwaite()`.
  - `executa.py`:
    - base empilhada com o gl do NHANES (15);
    - RP por faixa etária por domínio;
    - sensibilidade da regra de gl com Holm refeito por família.
  - Testes novos em `tests/test_003_survey.py`: Korn-Graubard, domínio contra a variância montada à mão, regra de gl e Satterthwaite.
  - Regra de gl do projeto: UPAs − estratos.
- 2026-11-27: **EUA (NHANES 2005-06) retirados** (decisão do usuário; ver Histórico da spec). Removidos do código o NHANES, a base empilhada e as hipóteses H3.3 e H3.6. Famílias de Holm: família 1 = H3.1, H3.2, H3.4 (Vigitel e PNS) por exposição; família 2 = H3.7 (Vigitel, PNS), H3.8 (Vigitel, PNS), H3.9. Os testes de linearização com estrato e UPA passam a usar a PNS.
