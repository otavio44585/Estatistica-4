# 004 — Plano: comparação mundial

Status: executado (2026-11-27).

## Pares fixados (T060, 2026-11-27, antes de calcular qualquer correlação)

Um par principal por base. Sinal: positivo = mais tela, pior sono. Em todos os pares principais o desfecho já é "quanto maior, pior", então nenhum sinal é invertido; a inversão vale para os pares de duração do sono nas sensibilidades.

| Base | Tipo de exposição | Exposição | Desfecho principal | Inverte sinal? | Sensibilidade (fora da meta-análise principal) |
|---|---|---|---|---|---|
| PNS 2019 | tempo total | `tela_digital_ord` (0 = não usa, 1..5 faixas) | `problema_sono_ord` (0–3) | não | correlação ponderada |
| Vigitel 2024 | tempo total | `tela_digital_ord` (0..7) | `insonia_idx` (0–12) | não | correlação ponderada |
| NHANES 2005-06 | tempo total | `tela_digital_ord` (0..6) | `insonia_idx` (0–12) | não | correlação ponderada |
| Argentina | tempo total | `tela_total_h` | `latencia_min` | não | pré-sono × latência; tempo total × duração e pré-sono × duração (invertidos) |
| Japão | pré-sono | `tela_presono_h` | AIS (`escore_sono_escala`) | não | pré-sono × duração (invertido) |
| Xuzhou | uso problemático | SAS-SV (`uso_problematico`) | PSQI (`escore_sono_escala`) | não | — |
| Turquia | uso problemático | doomscrolling (`uso_problematico`) | PSQI (`escore_sono_escala`) | não | doomscrolling × latência |

Procedência questionável (só sensibilidade, rotulada, nunca na estimativa principal): Paquistão (uso diário de redes sociais em 6 faixas × PSQI global; tempo total), Bangladesh v2 (frequência de uso de dispositivos antes de dormir × frequência de dificuldade para adormecer; pré-sono), Sleep Patterns 2.722 e 1.222 (tempo no celular antes de dormir × qualidade do sono, invertida; pré-sono). Holanda (Siebers): contraponto à parte, associação intrapessoal (correlação de medidas repetidas, Bakdash e Marusich, 2017) entre `prebed_use` do celular e `sleep_qual` (invertida), fora da meta-análise.

**Família de testes da 004** (definida aqui, antes de rodar): H4.1, H4.2, H4.3 e H4.4, com Holm sobre os quatro p.

**Regras de decisão fixadas antes de rodar:**

- T061: se o EP por bootstrap (B = 1.000, semente 2026) divergir do EP de Fieller, Hartley e Pearson em mais de 10% em qualquer base do núcleo, a meta-análise usa o EP por bootstrap em todas as bases; senão, a fórmula.
- H4.3: Brasil = PNS + Vigitel combinados por efeitos aleatórios (DerSimonian-Laird); outros com tempo total = NHANES + Argentina, mesmo método; z = (z_BR − z_outros) / √(EP_BR² + EP_outros²).
- H4.4: equivalência por dois testes unilaterais (TOST) sobre a escala z de Fisher, com as margens no IC da referência (Han, Zhou e Liu, 2024: 0,21 e 0,35). H0: a estimativa combinada de tempo total está fora de [0,21; 0,35]; H1: está dentro. p = maior dos dois p unilaterais. Como a referência mede uso geral × qualidade e nossos desfechos são insônia, problema de sono e latência, a correspondência é aproximada. O uso problemático contra r = 0,33 (IC 0,28–0,38) da mesma meta-análise é exploratório.
- H4.2: τ² estimado separadamente em cada subgrupo; Q entre subgrupos = Q das estimativas combinadas de cada subgrupo, gl = número de subgrupos − 1.

## Cálculo por base

- ρ de Spearman e r de Pearson com `scipy.stats`.
- Fisher: z = atanh(r); EP = 1/√(n − 3) para Pearson. Para Spearman usa-se a aproximação EP ≈ √(1,06/(n − 3)) (Fieller, Hartley e Pearson, 1957, Biometrika 44(3-4):470-481, doi:10.1093/biomet/44.3-4.470 — DOI conferido no Crossref em 2026-11-27). T061: o EP por bootstrap (B = 1.000, semente 2026) divergiu no máximo 5,4% (Japão) da fórmula, abaixo do limiar de 10%, então a fórmula foi mantida (`resultados/004/tabelas/efeitos_por_base.csv`).
- Inquéritos: correlação sem peso como principal; com peso como sensibilidade. Fica declarado, porque a ponderação da correlação de postos não é padrão.
- Bases com vários pares (Argentina, Turquia): um par principal fixado antes de calcular (o primeiro da tabela da spec); os demais em sensibilidade.

## Meta-análise das reanálises

- Efeitos aleatórios (DerSimonian-Laird) sobre z de Fisher, com `statsmodels.stats.meta_analysis.combine_effects` (statsmodels 0.14.6, já instalado), conferido com cálculo manual.
- Q de Cochran, I² e τ²; Q entre subgrupos para H4.2.
- H4.3: z = (z_BR − z_combinado_outros) / √(EP_BR² + EP_outros²).
- Volta para r com tanh() para reportar.

## Referência da literatura

Valores das meta-análises tirados de `docs/inventario-papers-internacional.md` (já conferidos no abstract ou no texto do PMC): Han, Zhou e Liu (2024) r = 0,28 (uso geral × qualidade) e r = 0,33 (uso problemático × problemas de sono); Bourke et al. (2026), intrapessoal. Valor que não estiver no inventário é conferido no PDF antes de entrar.

## Saídas

- `analise/notebooks/05_comparacao_mundial.ipynb`.
- `resultados/004/tabelas/efeitos_por_base.csv`, `meta_analise.csv`.
- `resultados/004/figuras/floresta.png`.

## Riscos

| Risco | Efeito | Mitigação |
|---|---|---|
| Escalas e populações muito diferentes | estimativa combinada pouco interpretável | foco em heterogeneidade e subgrupos, não no número combinado |
| Poucas bases por subgrupo (2 a 4) | Q com pouco poder | reportar I² com IC e não concluir "homogêneo" a partir de p > 0,05 |
| Exposição ordinal em faixas (inquéritos) | correlação atenuada | Spearman como principal; nota de limitação |

## Histórico

- 2026-11-27: executado com `python -m analise.mundial.rodar`; notebook gerado por `python -m analise.mundial.notebook`.
  - **Código:** `analise/mundial/` (`pares.py`, `metodos.py`, `questionaveis.py`, `floresta.py`, `rodar.py`, `notebook.py`); testes em `tests/test_004_meta.py`.
  - **DOIs conferidos no Crossref:**
    - DerSimonian e Laird (1986), doi:10.1016/0197-2456(86)90046-2;
    - Higgins e Thompson (2002), doi:10.1002/sim.1186 (I² e IC de I² pelo método de H);
    - Bakdash e Marusich (2017), doi:10.3389/fpsyg.2017.00456 (correlação de medidas repetidas, Holanda);
    - Han, Zhou e Liu (2024), doi:10.2196/48356 — valores conferidos no inventário: r = 0,28 (0,21–0,35) e r = 0,33 (0,28–0,38).
  - **ρ ponderado pelo peso amostral:** Pearson ponderado dos postos ponderados (ponto médio do peso acumulado). É uma sensibilidade, porque a ponderação da correlação de postos não é padrão.
  - **Acréscimo exploratório:** ρ parcial de Spearman ajustado por idade, com EP √(1,06/(n − 4)). O motivo foi o sinal invertido na PNS.

- 2026-11-27, correções da verificação independente:
  - `metodos.hartung_knapp` (Hartung e Knapp, 2001, doi:10.1002/sim.1009, conferido no Crossref), sem truncamento de q. É igual a `statsmodels.combine_effects(...).sd_eff_w_re_hksj` e está testado em `tests/test_004_meta.py`. Colunas novas em `meta_analise.csv`: `ep_hk`, `gl_hk`, `rho_ic_inf_hk`, `rho_ic_sup_hk`, `p_efeito_hk`, `nota`.
  - `metodos.deff_kish` (n·Σw²/(Σw)²). Coluna `deff_kish` em `efeitos_por_base.csv`, e linhas do grupo "efeito do desenho (deff)" em `sensibilidade.csv`, com as colunas novas `deff`, `tau2`, `ic_inf_hk`, `ic_sup_hk`, `z_teste`, `p` e `rho_outros`.
  - `metodos.tendencia_ordenada` (exploratório de H4.2): linha nova em `exploratorio_referencia.csv`.
  - A floresta mostra o IC de Hartung-Knapp do global em linha tracejada.
  - Nenhuma regra de decisão do plano mudou.
