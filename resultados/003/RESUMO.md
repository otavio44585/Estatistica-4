# 003 — Brasil: tela e sono na PNS 2019 e no Vigitel 2024 — resultados

Gerado por `python -m analise.brasil_eua.resumo` a partir de `resultados/003/tabelas/*.csv`. Execução de 2026-11-27; aprovação do grupo pendente.

## Transparência

**Os EUA (NHANES 2005-06) saíram do trabalho inteiro em 2026-11-27**, por decisão do grupo: a única base dos EUA é de 2005, antes do smartphone, e o tempo de tela daquela época não é comparável com o de 2019–2024. A decisão veio depois de os resultados com o NHANES já terem sido estimados, e fica registrada aqui. H3.3 e H3.6 foram retiradas; H3.4, H3.7 e H3.8 rodam só no Vigitel e na PNS. A comparação com outros países fica na spec 004.

As hipóteses H3.1–H3.9 (exceto as retiradas) foram formuladas depois da análise exploratória de 2026-11-27 (`docs/exploratorio_comparativo_br_eua_2026-11-27.*`). O modelo, as covariáveis e os pesos foram fixados no plano antes desta execução. A exposição digital foi fixada no código como a principal da família 2 antes de rodar (o foco da spec é a tela digital); a TV na família 2 é **complementar** e não entra na correção de Holm. Todos os testes são bilaterais (H1: RP ≠ 1; o sinal esperado, RP > 1, vem da literatura e não muda o teste).

## Método em uma tabela

| Item | Escolha |
|---|---|
| Modelo | Poisson com ligação log, peso amostral; exp(β) = razão de prevalências (RP) |
| Covariáveis (ajustada) | faixa etária (18–29, 30–44, 45–59, 60+), sexo, escolaridade em 3 faixas |
| Exposição alta × baixa | tela ≥ 3 h/dia × não usa ou < 1 h/dia (`tela_digital_cat`, `tela_tv_cat`) |
| Desfechos | Vigitel: dificuldade para adormecer quase sempre ou sempre; PNS: problema de sono em mais da metade dos dias |
| Variância | linearização de Taylor com estrato e UPA (PNS); sanduíche robusto só com peso (Vigitel) |
| Graus de liberdade do desenho | regra única do projeto: UPAs − estratos (PNS 7453); Vigitel: normal. Sensibilidade: regra do svyglm (d − p + 1) |
| Wald conjunto (q > 1) | correção de Korn-Graubard: F = (d − q + 1)/(d·q)·W, gl (q, d − q + 1) |
| RP por faixa etária | estimadas por domínio: ajuste na faixa, variância com todas as UPAs e estratos |
| Correção | Holm na família 1 (por exposição: digital e TV) e na família 2 |
| α | 0,05 bilateral |

## Hipóteses: decisão

Fonte: `resultados/003/tabelas/hipoteses.csv`.

| Família | H | Base | Exposição | Estimativa (IC 95%) | Estatística | p | p Holm | Decisão |
|---|---|---|---|---|---|---|---|---|
| 1 (digital) | H3.1 | Vigitel 2024 (Brasil) | digital | 1,32 (1,17–1,48) | z = 4,51 | < 0,001 | < 0,001 | rejeita H0 |
| 1 (digital) | H3.2 | PNS 2019 (Brasil) | digital | 1,19 (1,10–1,28) | t(7453) = 4,57 | < 0,001 | < 0,001 | rejeita H0 |
| 1 (digital) | H3.4 | Vigitel 2024 (Brasil) | digital | 1,15 (1,08–1,22) | z = 4,42 | < 0,001 | < 0,001 | rejeita H0 |
| 1 (digital) | H3.4 | PNS 2019 (Brasil) | digital | 1,07 (1,03–1,11) | t(7453) = 3,60 | < 0,001 | < 0,001 | rejeita H0 |
| 1 (TV) | H3.1 | Vigitel 2024 (Brasil) | TV | 1,20 (1,07–1,35) | z = 3,09 | 0,002 | 0,006 | rejeita H0 |
| 1 (TV) | H3.2 | PNS 2019 (Brasil) | TV | 1,13 (1,05–1,20) | t(7453) = 3,41 | < 0,001 | 0,003 | rejeita H0 |
| 1 (TV) | H3.4 | Vigitel 2024 (Brasil) | TV | 1,08 (1,02–1,15) | z = 2,60 | 0,009 | 0,009 | rejeita H0 |
| 1 (TV) | H3.4 | PNS 2019 (Brasil) | TV | 1,06 (1,02–1,10) | t(7453) = 2,87 | 0,004 | 0,008 | rejeita H0 |
| 2 | H3.7 | Vigitel 2024 (Brasil) | digital | RP por faixa: 1,08 a 1,44 | χ²(6) = 4,55 | 0,603 | 1,000 | não rejeita H0 |
| 2 | H3.7 | PNS 2019 (Brasil) | digital | RP por faixa: 1,10 a 1,42 | F(6; 7448) = 1,08 | 0,370 | 1,000 | não rejeita H0 |
| 2 | H3.8 | Vigitel 2024 (Brasil) | TV × digital | 0,90 (0,75–1,07) | χ²(1) = 1,41 | 0,236 | 0,943 | não rejeita H0 |
| 2 | H3.8 | PNS 2019 (Brasil) | TV × digital | 0,95 (0,86–1,06) | F(1; 7453) = 0,77 | 0,381 | 1,000 | não rejeita H0 |
| 2 | H3.9 | pns2019 × vigitel2024 | digital | 1,11 (0,96–1,28) | z = 1,44 | 0,150 | 0,750 | não rejeita H0 |

Estimativas: H3.1–H3.2 = RP de tela alta; H3.4 = RP por faixa de exposição (escore 0/1/2); H3.8 = razão RP da TV ÷ RP digital no mesmo modelo; H3.9 = razão das RP (Vigitel ÷ PNS). H3.3 e H3.6 (NHANES) foram retiradas em 2026-11-27.

## Sensibilidade à regra de graus de liberdade

Fonte: colunas `gl2_svyglm`, `p_svyglm`, `p_holm_svyglm` de `resultados/003/tabelas/hipoteses.csv` (Holm refeito por família com a regra do svyglm). Só linhas com gl de desenho finito.

| Família | H | Base | Exposição | gl (regra principal) | p Holm | gl (svyglm) | p Holm (svyglm) | Decisão (svyglm) |
|---|---|---|---|---|---|---|---|---|
| 1 (digital) | H3.2 | PNS 2019 (Brasil) | digital | 7453 | < 0,001 | 7445 | < 0,001 | rejeita H0 |
| 1 (digital) | H3.4 | PNS 2019 (Brasil) | digital | 7453 | < 0,001 | 7446 | < 0,001 | rejeita H0 |
| 1 (TV) | H3.2 | PNS 2019 (Brasil) | TV | 7453 | 0,003 | 7445 | 0,003 | rejeita H0 |
| 1 (TV) | H3.4 | PNS 2019 (Brasil) | TV | 7453 | 0,008 | 7446 | 0,008 | rejeita H0 |
| 2 | H3.7 | PNS 2019 (Brasil) | digital | 7448 | 1,000 | 7439 | 1,000 | não rejeita H0 |
| 2 | H3.8 | PNS 2019 (Brasil) | TV × digital | 7453 | 1,000 | 7443 | 1,000 | não rejeita H0 |

## Bruta, só idade e ajustada lado a lado (tela ≥ 3 h vs < 1 h)

Fonte: `resultados/003/tabelas/rp_bruta_ajustada.csv`.

| Base | Exposição | Bruta | Só idade | Ajustada | n |
|---|---|---|---|---|---|
| Vigitel 2024 (Brasil) | digital | 1,28 (1,14–1,43) | 1,26 (1,13–1,42) | 1,32 (1,17–1,48) | 27029 |
| Vigitel 2024 (Brasil) | TV | 1,17 (1,05–1,31) | 1,22 (1,09–1,37) | 1,20 (1,07–1,35) | 27048 |
| PNS 2019 (Brasil) | digital | 0,85 (0,80–0,91) | 1,16 (1,08–1,25) | 1,19 (1,10–1,28) | 88531 |
| PNS 2019 (Brasil) | TV | 1,22 (1,14–1,30) | 1,13 (1,06–1,21) | 1,13 (1,05–1,20) | 88531 |

## Prevalências ponderadas por faixa de tela

Fonte: `resultados/003/tabelas/prevalencias.csv`.

| Base | Exposição | < 1 h | 1 a < 3 h | ≥ 3 h |
|---|---|---|---|---|
| Vigitel 2024 (Brasil) | digital | 20,7% (n = 8874) | 20,1% (n = 11254) | 26,5% (n = 6901) |
| Vigitel 2024 (Brasil) | TV | 22,0% (n = 10318) | 20,2% (n = 11940) | 25,8% (n = 4790) |
| PNS 2019 (Brasil) | digital | 21,0% (n = 45716) | 15,8% (n = 26006) | 18,0% (n = 16809) |
| PNS 2019 (Brasil) | TV | 18,6% (n = 26072) | 16,9% (n = 43210) | 22,6% (n = 19249) |

## Comparação entre as duas pesquisas brasileiras (H3.9; inclui TV, complementar)

Fonte: `resultados/003/tabelas/comparacoes_entre_bases.csv`.

| H | Exposição | Método | Razão (IC 95%) | Estatística | p |
|---|---|---|---|---|---|
| H3.9 | digital | z da diferença dos log-RP (modelos separados) | 1,11 (0,96–1,28) | z = 1,44 | 0,150 |
| H3.9 | TV | z da diferença dos log-RP (modelos separados) | 1,07 (0,93–1,22) | z = 0,93 | 0,351 |

## Sensibilidades (não entram nas famílias)

Fonte: `resultados/003/tabelas/sensibilidade.csv`. Renda não existe no contrato de variáveis (ausente no Vigitel e não harmonizada na PNS): sensibilidade não feita.

| Base | Exposição | Modelo | Comparação | RP (IC 95%) | p | n |
|---|---|---|---|---|---|---|
| Vigitel 2024 (Brasil) | digital | ajustada + depressão | 2 vs 0 | 1,28 (1,14–1,43) | < 0,001 | 27005 |
| Vigitel 2024 (Brasil) | digital | ajustada sem peso | 2 vs 0 | 1,29 (1,21–1,37) | < 0,001 | 27029 |
| Vigitel 2024 (Brasil) | digital | ajustada, corte alternativo | ≥ 4 h vs não usa ou < 1 h | 1,37 (1,19–1,57) | < 0,001 | 13219 |
| Vigitel 2024 (Brasil) | TV | ajustada + depressão | 2 vs 0 | 1,20 (1,07–1,34) | 0,002 | 27022 |
| Vigitel 2024 (Brasil) | TV | ajustada sem peso | 2 vs 0 | 1,22 (1,15–1,29) | < 0,001 | 27048 |
| Vigitel 2024 (Brasil) | TV | ajustada, corte alternativo | ≥ 4 h vs não usa ou < 1 h | 1,27 (1,10–1,46) | < 0,001 | 12970 |
| PNS 2019 (Brasil) | digital | ajustada + depressão | 2 vs 0 | 1,10 (1,03–1,18) | 0,003 | 88531 |
| PNS 2019 (Brasil) | digital | ajustada sem peso | 2 vs 0 | 1,18 (1,13–1,23) | < 0,001 | 88531 |
| PNS 2019 (Brasil) | digital | ajustada, corte alternativo | ≥ 6 h (a PNS não separa 4 h) vs não usa ou < 1 h | 1,36 (1,23–1,50) | < 0,001 | 52173 |
| PNS 2019 (Brasil) | TV | ajustada + depressão | 2 vs 0 | 1,14 (1,07–1,21) | < 0,001 | 88531 |
| PNS 2019 (Brasil) | TV | ajustada sem peso | 2 vs 0 | 1,15 (1,11–1,19) | < 0,001 | 88531 |
| PNS 2019 (Brasil) | TV | ajustada, corte alternativo | ≥ 6 h (a PNS não separa 4 h) vs não usa ou < 1 h | 1,36 (1,24–1,48) | < 0,001 | 31240 |
| PNS 2019 (Brasil) | digital | ajustada, gl pela regra do svyglm (d − p + 1) | 2 vs 0 | 1,19 (nan–nan) | < 0,001 | 88531 |
| PNS 2019 (Brasil) | TV | ajustada, gl pela regra do svyglm (d − p + 1) | 2 vs 0 | 1,13 (nan–nan) | < 0,001 | 88531 |

## Forma da relação (exploratório)

Fonte: `resultados/003/tabelas/desvio_linearidade_exploratorio.csv`. Teste não previsto na spec: sob tendência linear no log com escores 0/1/2, a RP de 1–3 h seria a raiz quadrada da RP de ≥ 3 h (β₁ = β₂/2).

| Base | Exposição | RP 1–3 h vs < 1 h | RP ≥ 3 h vs < 1 h | Estatística | p |
|---|---|---|---|---|---|
| Vigitel 2024 (Brasil) | digital | 1,01 | 1,32 | χ²(1) = 7,96 | 0,005 |
| Vigitel 2024 (Brasil) | TV | 0,96 | 1,20 | χ²(1) = 9,08 | 0,003 |
| PNS 2019 (Brasil) | digital | 0,92 | 1,19 | F(1; 7453) = 32,07 | < 0,001 |
| PNS 2019 (Brasil) | TV | 0,88 | 1,13 | F(1; 7453) = 51,24 | < 0,001 |

## Variância: linearização × alternativas (T040)

Fonte: `resultados/003/tabelas/comparacao_variancia.csv`. Erro padrão do log-RP de tela alta (modelo ajustado).

| Base | Exposição | Linearização (usada) | Cluster do statsmodels | Poisson ponderado sem desenho | Robusto sem peso |
|---|---|---|---|---|---|
| Vigitel 2024 (Brasil) | digital | 0,0608 | — | 0,0365 | 0,0308 |
| Vigitel 2024 (Brasil) | TV | 0,0587 | — | 0,0351 | 0,0302 |
| PNS 2019 (Brasil) | digital | 0,0376 | 0,0374 | 0,0233 | 0,0210 |
| PNS 2019 (Brasil) | TV | 0,0345 | 0,0344 | 0,0211 | 0,0184 |

## Leitura

- **Nas duas pesquisas brasileiras (família 1).** Com ajuste por idade, sexo e escolaridade, tela digital ≥ 3 h/dia se associou a mais problema de sono frequente no Vigitel (RP 1,32 (1,17–1,48)) e na PNS (RP 1,19 (1,10–1,28)). 2 de 2 rejeitam H0 depois de Holm. Com TV, 2 de 2 (RP de 1,13 a 1,20).
- **Regra de graus de liberdade.** Na PNS (7453 gl de desenho), a regra do svyglm (7445 gl) dá p Holm < 0,001 (rejeita H0): com tantas UPAs, a regra não muda nada. O Vigitel não tem estrato nem UPA.
- **Confundimento por idade na PNS.** A RP bruta da tela digital é 0,85 (0,80–0,91): quem usa mais tela é mais jovem e jovens relatam menos problema de sono. Ajustada, passa a 1,19 (1,10–1,28).
- **Dose-resposta (H3.4).** O teste de tendência rejeita H0 em 4 das 4 combinações, mas a forma não é uma reta. A RP ajustada de 1 a 3 h contra < 1 h fica abaixo de 1 em 3 das 4 combinações (1 ou mais em: Vigitel 2024 (Brasil), digital (1,01)), e o excesso aparece em ≥ 3 h. O teste exploratório de desvio da linearidade tem p < 0,05 em 4 das 4. Os dados apontam um limiar perto de 3 h, não uma relação linear.
- **Idade, TV × digital e PNS × Vigitel (H3.7–H3.9).** 0 das 5 hipóteses da família 2 rejeitam H0 depois de Holm: não foi detectada variação por faixa etária, entre TV e tela digital, nem entre PNS e Vigitel (razão 1,11 (0,96–1,28); itens de sono diferentes). Na PNS, a RP ajustada em 18–29 anos é 1,42 (1,16–1,74) (estimada por domínio), perto do que a exploração viu, mas o teste de interação não detecta diferença entre as faixas.
- **Desenho amostral importa.** O erro padrão com desenho é 1,61 a 1,68 vezes o do Poisson ponderado que ignora o desenho. No Vigitel, o peso rake multiplica o erro padrão por 1,94 a 1,98 em relação à análise sem peso.

## Limitações

- Transversal: associação, não efeito. Causalidade reversa (quem dorme mal pode usar mais tela à noite) e confundimento residual (saúde mental, trabalho em turnos, renda) seguem possíveis.
- Sem comparação internacional nesta spec: os EUA saíram do trabalho (base única de 2005, antes do smartphone). A posição do Brasil frente a outros países fica na spec 004.
- O item da PNS (problema de sono em geral, 2 semanas) não é o mesmo do Vigitel (dificuldade para adormecer); H3.9 mistura pesquisa e item.
- Vigitel cobre só as capitais e não divulga estrato e UPA: a variância usa só o peso.
- Renda não entrou (ausente no contrato de variáveis).
