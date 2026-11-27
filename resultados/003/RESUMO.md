# 003 — Brasil × EUA: resultados

Gerado por `python -m analise.brasil_eua.resumo` a partir de `resultados/003/tabelas/*.csv`. Execução de 2026-11-27; aprovação do grupo pendente.

## Transparência

As hipóteses H3.1–H3.9 foram formuladas depois da análise exploratória de 2026-11-27 (`docs/exploratorio_comparativo_br_eua_2026-11-27.*`). O modelo, as covariáveis e os pesos foram fixados no plano antes desta execução. A exposição digital foi fixada no código como a principal da família 2 antes de rodar (o foco da spec é a tela digital); a TV na família 2 é **complementar** e não entra na correção de Holm. Todos os testes são bilaterais (H1: RP ≠ 1; o sinal esperado, RP > 1, vem da literatura e não muda o teste).

## Método em uma tabela

| Item | Escolha |
|---|---|
| Modelo | Poisson com ligação log, peso amostral; exp(β) = razão de prevalências (RP) |
| Covariáveis (ajustada) | faixa etária (18–29, 30–44, 45–59, 60+), sexo, escolaridade em 3 faixas |
| Exposição alta × baixa | tela ≥ 3 h/dia × não usa ou < 1 h/dia (`tela_digital_cat`, `tela_tv_cat`) |
| Desfechos | Vigitel: dificuldade para adormecer quase sempre ou sempre; NHANES: often/almost always (5 ou mais vezes por mês); PNS: problema de sono em mais da metade dos dias |
| Variância | linearização de Taylor com estrato e UPA (PNS, NHANES); sanduíche robusto só com peso (Vigitel) |
| Graus de liberdade do desenho | regra única do projeto: UPAs − estratos (PNS 7453; NHANES 15); Vigitel: normal. Sensibilidade: regra do svyglm (d − p + 1) |
| Wald conjunto (q > 1) | correção de Korn-Graubard: F = (d − q + 1)/(d·q)·W, gl (q, d − q + 1) |
| RP por faixa etária | estimadas por domínio: ajuste na faixa, variância com todas as UPAs e estratos |
| Base empilhada (H3.6) | gl mostrado = gl do NHANES (15); Satterthwaite registrado como sensibilidade |
| Correção | Holm na família 1 (por exposição: digital e TV) e na família 2 |
| α | 0,05 bilateral |

## Hipóteses: decisão

Fonte: `resultados/003/tabelas/hipoteses.csv`.

| Família | H | Base | Exposição | Estimativa (IC 95%) | Estatística | p | p Holm | Decisão |
|---|---|---|---|---|---|---|---|---|
| 1 (digital) | H3.1 | Vigitel 2024 (Brasil) | digital | 1,32 (1,17–1,48) | z = 4,51 | < 0,001 | < 0,001 | rejeita H0 |
| 1 (digital) | H3.2 | PNS 2019 (Brasil) | digital | 1,19 (1,10–1,28) | t(7453) = 4,57 | < 0,001 | < 0,001 | rejeita H0 |
| 1 (digital) | H3.3 | NHANES 2005-06 (EUA) | digital | 1,41 (1,07–1,84) | t(15) = 2,70 | 0,016 | 0,033 | rejeita H0 |
| 1 (digital) | H3.4 | Vigitel 2024 (Brasil) | digital | 1,15 (1,08–1,22) | z = 4,42 | < 0,001 | < 0,001 | rejeita H0 |
| 1 (digital) | H3.4 | PNS 2019 (Brasil) | digital | 1,07 (1,03–1,11) | t(7453) = 3,60 | < 0,001 | < 0,001 | rejeita H0 |
| 1 (digital) | H3.4 | NHANES 2005-06 (EUA) | digital | 1,11 (0,97–1,26) | t(15) = 1,70 | 0,109 | 0,109 | não rejeita H0 |
| 1 (TV) | H3.1 | Vigitel 2024 (Brasil) | TV | 1,20 (1,07–1,35) | z = 3,09 | 0,002 | 0,006 | rejeita H0 |
| 1 (TV) | H3.2 | PNS 2019 (Brasil) | TV | 1,13 (1,05–1,20) | t(7453) = 3,41 | < 0,001 | 0,003 | rejeita H0 |
| 1 (TV) | H3.3 | NHANES 2005-06 (EUA) | TV | 1,67 (1,30–2,14) | t(15) = 4,40 | < 0,001 | 0,003 | rejeita H0 |
| 1 (TV) | H3.4 | Vigitel 2024 (Brasil) | TV | 1,08 (1,02–1,15) | z = 2,60 | 0,009 | 0,009 | rejeita H0 |
| 1 (TV) | H3.4 | PNS 2019 (Brasil) | TV | 1,06 (1,02–1,10) | t(7453) = 2,87 | 0,004 | 0,008 | rejeita H0 |
| 1 (TV) | H3.4 | NHANES 2005-06 (EUA) | TV | 1,36 (1,21–1,53) | t(15) = 5,57 | < 0,001 | < 0,001 | rejeita H0 |
| 2 | H3.6 | vigitel2024 + nhanes0506 | digital | 1,07 (0,80–1,44) | t(15) = 0,51 | 0,617 | 1,000 | não rejeita H0 |
| 2 | H3.7 | Vigitel 2024 (Brasil) | digital | RP por faixa: 1,08 a 1,44 | χ²(6) = 4,55 | 0,603 | 1,000 | não rejeita H0 |
| 2 | H3.7 | PNS 2019 (Brasil) | digital | RP por faixa: 1,10 a 1,42 | F(6; 7448) = 1,08 | 0,370 | 1,000 | não rejeita H0 |
| 2 | H3.7 | NHANES 2005-06 (EUA) | digital | RP por faixa: 0,80 a 2,20 | F(6; 10) = 1,86 | 0,183 | 1,000 | não rejeita H0 |
| 2 | H3.8 | Vigitel 2024 (Brasil) | TV × digital | 0,90 (0,75–1,07) | χ²(1) = 1,41 | 0,236 | 1,000 | não rejeita H0 |
| 2 | H3.8 | PNS 2019 (Brasil) | TV × digital | 0,95 (0,86–1,06) | F(1; 7453) = 0,77 | 0,381 | 1,000 | não rejeita H0 |
| 2 | H3.8 | NHANES 2005-06 (EUA) | TV × digital | 1,28 (0,99–1,65) | F(1; 15) = 4,11 | 0,061 | 0,486 | não rejeita H0 |
| 2 | H3.9 | pns2019 × vigitel2024 | digital | 1,11 (0,96–1,28) | z = 1,44 | 0,150 | 1,000 | não rejeita H0 |

Estimativas: H3.1–H3.3 = RP de tela alta; H3.4 = RP por faixa de exposição (escore 0/1/2); H3.6 = razão das RP (NHANES ÷ Vigitel); H3.8 = razão RP da TV ÷ RP digital no mesmo modelo; H3.9 = razão das RP (Vigitel ÷ PNS).

## Sensibilidade à regra de graus de liberdade

Fonte: colunas `gl2_svyglm`, `p_svyglm`, `p_holm_svyglm` de `resultados/003/tabelas/hipoteses.csv` (Holm refeito por família com a regra do svyglm). Só linhas com gl de desenho finito.

| Família | H | Base | Exposição | gl (regra principal) | p Holm | gl (svyglm) | p Holm (svyglm) | Decisão (svyglm) |
|---|---|---|---|---|---|---|---|---|
| 1 (digital) | H3.2 | PNS 2019 (Brasil) | digital | 7453 | < 0,001 | 7445 | < 0,001 | rejeita H0 |
| 1 (digital) | H3.3 | NHANES 2005-06 (EUA) | digital | 15 | 0,033 | 7 | 0,061 | não rejeita H0 |
| 1 (digital) | H3.4 | PNS 2019 (Brasil) | digital | 7453 | < 0,001 | 7446 | < 0,001 | rejeita H0 |
| 1 (digital) | H3.4 | NHANES 2005-06 (EUA) | digital | 15 | 0,109 | 8 | 0,127 | não rejeita H0 |
| 1 (TV) | H3.2 | PNS 2019 (Brasil) | TV | 7453 | 0,003 | 7445 | 0,003 | rejeita H0 |
| 1 (TV) | H3.3 | NHANES 2005-06 (EUA) | TV | 15 | 0,003 | 7 | 0,010 | rejeita H0 |
| 1 (TV) | H3.4 | PNS 2019 (Brasil) | TV | 7453 | 0,008 | 7446 | 0,010 | rejeita H0 |
| 1 (TV) | H3.4 | NHANES 2005-06 (EUA) | TV | 15 | < 0,001 | 8 | 0,003 | rejeita H0 |
| 2 | H3.6 | vigitel2024 + nhanes0506 | digital | 15 | 1,000 | 4 | 1,000 | não rejeita H0 |
| 2 | H3.7 | PNS 2019 (Brasil) | digital | 7448 | 1,000 | 7439 | 1,000 | não rejeita H0 |
| 2 | H3.7 | NHANES 2005-06 (EUA) | digital | 10 | 1,000 | 1 | 1,000 | não rejeita H0 (não calculável: d − p + 1 < q; Holm usa o p da regra principal) |
| 2 | H3.8 | PNS 2019 (Brasil) | TV × digital | 7453 | 1,000 | 7443 | 1,000 | não rejeita H0 |
| 2 | H3.8 | NHANES 2005-06 (EUA) | TV × digital | 15 | 0,486 | 5 | 0,788 | não rejeita H0 |

## Bruta, só idade e ajustada lado a lado (tela ≥ 3 h vs < 1 h)

Fonte: `resultados/003/tabelas/rp_bruta_ajustada.csv`.

| Base | Exposição | Bruta | Só idade | Ajustada | n |
|---|---|---|---|---|---|
| Vigitel 2024 (Brasil) | digital | 1,28 (1,14–1,43) | 1,26 (1,13–1,42) | 1,32 (1,17–1,48) | 27029 |
| Vigitel 2024 (Brasil) | TV | 1,17 (1,05–1,31) | 1,22 (1,09–1,37) | 1,20 (1,07–1,35) | 27048 |
| PNS 2019 (Brasil) | digital | 0,85 (0,80–0,91) | 1,16 (1,08–1,25) | 1,19 (1,10–1,28) | 88531 |
| PNS 2019 (Brasil) | TV | 1,22 (1,14–1,30) | 1,13 (1,06–1,21) | 1,13 (1,05–1,20) | 88531 |
| NHANES 2005-06 (EUA) | digital | 1,32 (0,99–1,75) | 1,29 (0,96–1,73) | 1,41 (1,07–1,84) | 5552 |
| NHANES 2005-06 (EUA) | TV | 1,67 (1,32–2,12) | 1,70 (1,34–2,17) | 1,67 (1,30–2,14) | 5547 |

## Prevalências ponderadas por faixa de tela

Fonte: `resultados/003/tabelas/prevalencias.csv`.

| Base | Exposição | < 1 h | 1 a < 3 h | ≥ 3 h |
|---|---|---|---|---|
| Vigitel 2024 (Brasil) | digital | 20,7% (n = 8874) | 20,1% (n = 11254) | 26,5% (n = 6901) |
| Vigitel 2024 (Brasil) | TV | 22,0% (n = 10318) | 20,2% (n = 11940) | 25,8% (n = 4790) |
| PNS 2019 (Brasil) | digital | 21,0% (n = 45716) | 15,8% (n = 26006) | 18,0% (n = 16809) |
| PNS 2019 (Brasil) | TV | 18,6% (n = 26072) | 16,9% (n = 43210) | 22,6% (n = 19249) |
| NHANES 2005-06 (EUA) | digital | 16,2% (n = 3950) | 13,9% (n = 1158) | 21,4% (n = 444) |
| NHANES 2005-06 (EUA) | TV | 12,5% (n = 841) | 13,2% (n = 2362) | 20,9% (n = 2344) |

## Comparações entre bases (inclui TV, complementar)

Fonte: `resultados/003/tabelas/comparacoes_entre_bases.csv`.

| H | Exposição | Método | Razão (IC 95%) | Estatística | p | gl Satterthwaite (p) |
|---|---|---|---|---|---|---|
| H3.6 | digital | interação país × tela na base empilhada (1 gl, categoria 2) | 1,07 (0,80–1,44) | t(15) = 0,51 | 0,617 | 8,9 (0,622) |
| H3.6 | digital | interação conjunta (2 gl) | — | F(2; 14) = 0,50 | 0,615 | — |
| H3.6 | digital | z da diferença dos log-RP (modelos separados) | 1,07 (0,81–1,40) | z = 0,47 | 0,639 | — |
| H3.9 | digital | z da diferença dos log-RP (modelos separados) | 1,11 (0,96–1,28) | z = 1,44 | 0,150 | — |
| H3.6 (sensibilidade) | digital | z da diferença dos log-RP, modelos ajustados SEM peso | 1,14 (0,99–1,33) | z = 1,78 | 0,074 | — |
| H3.6 | TV | interação país × tela na base empilhada (1 gl, categoria 2) | 1,42 (1,09–1,85) | t(15) = 2,87 | 0,012 | 12,5 (0,014) |
| H3.6 | TV | interação conjunta (2 gl) | — | F(2; 14) = 4,83 | 0,025 | — |
| H3.6 | TV | z da diferença dos log-RP (modelos separados) | 1,39 (1,08–1,80) | z = 2,53 | 0,011 | — |
| H3.9 | TV | z da diferença dos log-RP (modelos separados) | 1,07 (0,93–1,22) | z = 0,93 | 0,351 | — |
| H3.6 (sensibilidade) | TV | z da diferença dos log-RP, modelos ajustados SEM peso | 1,10 (0,94–1,28) | z = 1,19 | 0,233 | — |

Na base empilhada, a variância da interação país × tela vem quase toda do NHANES: o gl mostrado é o do desenho do NHANES (regra do projeto), e não o da base empilhada (~27 mil, otimista). O gl de Satterthwaite fica abaixo de 15 e não muda nenhuma decisão.

## Sensibilidades (não entram nas famílias)

Fonte: `resultados/003/tabelas/sensibilidade.csv`. Renda não existe no contrato de variáveis (ausente no Vigitel e não harmonizada na PNS/NHANES): sensibilidade não feita.

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
| NHANES 2005-06 (EUA) | digital | ajustada + depressão | 2 vs 0 | 1,45 (1,10–1,92) | 0,012 | 4797 |
| NHANES 2005-06 (EUA) | digital | ajustada sem peso | 2 vs 0 | 1,47 (1,27–1,70) | < 0,001 | 5552 |
| NHANES 2005-06 (EUA) | digital | ajustada, corte alternativo | ≥ 4 h vs não usa ou < 1 h | 1,59 (1,15–2,18) | 0,008 | 4225 |
| NHANES 2005-06 (EUA) | TV | ajustada + depressão | 2 vs 0 | 1,79 (1,29–2,46) | 0,002 | 4793 |
| NHANES 2005-06 (EUA) | TV | ajustada sem peso | 2 vs 0 | 1,33 (1,14–1,55) | 0,001 | 5547 |
| NHANES 2005-06 (EUA) | TV | ajustada, corte alternativo | ≥ 4 h vs não usa ou < 1 h | 1,95 (1,49–2,54) | < 0,001 | 2242 |
| PNS 2019 (Brasil) | digital | ajustada, gl pela regra do svyglm (d − p + 1) | 2 vs 0 | 1,19 (nan–nan) | < 0,001 | 88531 |
| NHANES 2005-06 (EUA) | digital | ajustada, gl pela regra do svyglm (d − p + 1) | 2 vs 0 | 1,41 (nan–nan) | 0,031 | 5552 |
| PNS 2019 (Brasil) | TV | ajustada, gl pela regra do svyglm (d − p + 1) | 2 vs 0 | 1,13 (nan–nan) | < 0,001 | 88531 |
| NHANES 2005-06 (EUA) | TV | ajustada, gl pela regra do svyglm (d − p + 1) | 2 vs 0 | 1,67 (nan–nan) | 0,003 | 5547 |

## Forma da relação (exploratório)

Fonte: `resultados/003/tabelas/desvio_linearidade_exploratorio.csv`. Teste não previsto na spec: sob tendência linear no log com escores 0/1/2, a RP de 1–3 h seria a raiz quadrada da RP de ≥ 3 h (β₁ = β₂/2).

| Base | Exposição | RP 1–3 h vs < 1 h | RP ≥ 3 h vs < 1 h | Estatística | p |
|---|---|---|---|---|---|
| Vigitel 2024 (Brasil) | digital | 1,01 | 1,32 | χ²(1) = 7,96 | 0,005 |
| Vigitel 2024 (Brasil) | TV | 0,96 | 1,20 | χ²(1) = 9,08 | 0,003 |
| PNS 2019 (Brasil) | digital | 0,92 | 1,19 | F(1; 7453) = 32,07 | < 0,001 |
| PNS 2019 (Brasil) | TV | 0,88 | 1,13 | F(1; 7453) = 51,24 | < 0,001 |
| NHANES 2005-06 (EUA) | digital | 0,95 | 1,41 | F(1; 15) = 4,65 | 0,048 |
| NHANES 2005-06 (EUA) | TV | 1,08 | 1,67 | F(1; 15) = 8,84 | 0,009 |

## Variância: linearização × alternativas (T040)

Fonte: `resultados/003/tabelas/comparacao_variancia.csv`. Erro padrão do log-RP de tela alta (modelo ajustado).

| Base | Exposição | Linearização (usada) | Cluster do statsmodels | Poisson ponderado sem desenho | Robusto sem peso |
|---|---|---|---|---|---|
| Vigitel 2024 (Brasil) | digital | 0,0608 | — | 0,0365 | 0,0308 |
| Vigitel 2024 (Brasil) | TV | 0,0587 | — | 0,0351 | 0,0302 |
| PNS 2019 (Brasil) | digital | 0,0376 | 0,0374 | 0,0233 | 0,0210 |
| PNS 2019 (Brasil) | TV | 0,0345 | 0,0344 | 0,0211 | 0,0184 |
| NHANES 2005-06 (EUA) | digital | 0,1260 | 0,1165 | 0,1166 | 0,0992 |
| NHANES 2005-06 (EUA) | TV | 0,1165 | 0,1294 | 0,1062 | 0,0964 |

## Leitura

- **Dentro de cada país (família 1).** Com ajuste por idade, sexo e escolaridade, tela digital ≥ 3 h/dia se associou a mais problema de sono frequente no Vigitel (RP 1,32 (1,17–1,48)), na PNS (RP 1,19 (1,10–1,28)) e no NHANES (RP 1,41 (1,07–1,84)). 3 de 3 rejeitam H0 depois de Holm com a regra de gl do projeto. Com TV, 3 de 3 (RP de 1,13 a 1,67).
- **A decisão de H3.3 depende da regra de graus de liberdade.** Com UPAs − estratos (15 gl, regra do projeto) o p Holm é 0,033 (rejeita H0). Com a regra do svyglm (7 gl), o p Holm vai a 0,061 (não rejeita H0). A estimativa (RP 1,41) é a mesma; muda só a incerteza atribuída a um desenho com 15 gl. Vigitel e PNS não dependem da regra.
- **Confundimento por idade na PNS.** A RP bruta da tela digital é 0,85 (0,80–0,91): quem usa mais tela é mais jovem e jovens relatam menos problema de sono. Ajustada, passa a 1,19 (1,10–1,28).
- **Dose-resposta (H3.4).** O teste de tendência rejeita H0 em 5 das 6 combinações, mas a forma não é uma reta. A RP ajustada de 1 a 3 h contra < 1 h fica abaixo de 1 em 4 das 6 combinações (1 ou mais em: Vigitel 2024 (Brasil), digital (1,01); NHANES 2005-06 (EUA), TV (1,08)), e o excesso aparece em ≥ 3 h. O teste exploratório de desvio da linearidade tem p < 0,05 em 6 das 6. Os dados apontam um limiar perto de 3 h, não uma relação linear.
- **Brasil × EUA (H3.6).** Para a tela digital, não foi detectada diferença entre a RP do NHANES e a do Vigitel (razão 1,07 (0,80–1,44), p Holm 1,000). O IC é compatível com uma RP dos EUA de 20% menor a 44% maior que a do Brasil: ausência de evidência de diferença, não prova de igualdade. Para a TV (complementar, fora de Holm) a razão foi 1,42 (1,09–1,85), p 0,012, mas sem peso fica em 1,10 (0,94–1,28) (p 0,233): a diferença depende da ponderação do NHANES e não deve ser lida como robusta.
- **Idade, TV × digital e PNS × Vigitel (H3.7–H3.9).** 0 das 8 hipóteses da família 2 rejeitam H0 depois de Holm: não foi detectada variação por faixa etária, entre TV e tela digital, nem entre PNS e Vigitel (razão 1,11 (0,96–1,28); itens de sono diferentes). Na PNS, a RP ajustada em 18–29 anos é 1,42 (1,16–1,74) (estimada por domínio), perto do que a exploração viu, mas o teste de interação não detecta diferença entre as faixas.
- **Desenho amostral importa.** O erro padrão com desenho é 1,08 a 1,68 vezes o do Poisson ponderado que ignora o desenho. No Vigitel, o peso rake multiplica o erro padrão por 1,94 a 1,98 em relação à análise sem peso.

## Limitações

- Transversal: associação, não efeito. Causalidade reversa (quem dorme mal pode usar mais tela à noite) e confundimento residual (saúde mental, trabalho em turnos, renda) seguem possíveis.
- NHANES 2005-06 é anterior ao smartphone; a comparação mistura país e época (2005 × 2024).
- O item da PNS (problema de sono em geral, 2 semanas) não é o mesmo do Vigitel e do NHANES (dificuldade para adormecer); H3.9 mistura base e item.
- Vigitel cobre só as capitais e não divulga estrato e UPA: a variância usa só o peso.
- NHANES tem 15 graus de liberdade de desenho: intervalos largos e testes com pouco poder; a decisão de H3.3 muda com a regra de gl (ver acima).
- Renda não entrou (ausente no contrato de variáveis).
