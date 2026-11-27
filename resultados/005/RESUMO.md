# 005 — Resumo dos resultados: regressão linear múltipla, ANOVA e teste t

Gerado por `python -m analise.regressao.resumo` a partir de `resultados/005/tabelas/*.csv` e `resultados/005/conferencia.csv`. α = 0,05 bilateral; Holm dentro de cada família. Associação observacional, sem interpretação causal.

**EUA fora do trabalho (decisão do grupo, 2026-11-27).** H5.2, H5.8, H5.10 e H5.11 (NHANES 2005-06 e base empilhada Vigitel + NHANES) foram retiradas; a numeração original é mantida. Famílias: R1 = H5.1, H5.3–H5.6; R2 = H5.7, H5.9.

## Conferência dos p-valores (três caminhos)

- **Caminho A:** ferramenta Análise de Dados do Excel (Analysis ToolPak), executada por automação COM (`analise/regressao/excel_toolpak.ps1`, chamado por `roda_excel.py`): Regressão, Anova: fator único e Teste-t (variâncias diferentes e iguais), em 5 pastas de trabalho.
- **Caminho B:** fórmulas nativas do Excel ao lado de cada saída (`T.DIST.2T`, `F.DIST.RT`), recalculadas pelo próprio Excel.
- **Caminho C:** script (`analise/regressao/ols.py`, álgebra matricial, e `scipy`).
- **Resultado:** 611 de 611 números dentro da tolerância (1e-8), mais 1 exceções documentadas (abaixo); maior diferença relativa A × C = 4,5e-10, B × C = 4,5e-10. Arquivo: `resultados/005/conferencia.csv` (colunas `dentro_tolerancia` e `excecao_documentada`).
- **Exceções documentadas (1, do teste t do Vigitel):** o teste t de Welch do Excel arredonda os graus de liberdade para inteiro. O p do Excel difere do p com gl fracionário em até 4,5e-07 (relativo), acima da tolerância. O relatório usa o gl fracionário (caminho C); o Excel bate com o script quando o script usa o mesmo gl inteiro.
- **Equivalências verificadas** (`tabelas/equivalencias.csv`): F da ANOVA = F global da regressão nas 2 dummies (diferença 2,5e-14); t com variâncias iguais = t da dummy (diferença 8,8e-14); t de Welch difere do t com variâncias iguais em 1,0% (Vigitel).

**Peso amostral:** só o Vigitel tem peso, e ele não divulga estrato nem UPA. O erro padrão é o robusto (cada pessoa é a sua UPA), com gl = n − 1. Os Wald de mais de um coeficiente (ANOVA ponderada, F global) usam a correção de Korn-Graubard, F = (d − q + 1)/(d·q)·W, que com d na casa das dezenas de milhares coincide com W/q. Sem base com estrato e UPA, a regra de graus de liberdade não muda nenhuma decisão.

## Família R1 — coeficiente da tela na regressão múltipla

| H | Base | Y | Tela (coeficiente testado) | b (IC 95%) | t | gl | p | p Holm | Decisão | ΔR² do bloco de tela | Versão que decide |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H5.1 | Vigitel 2024 | índice de insônia (0-12) | tela_3h_mais | 0,591 (0,364 a 0,817) | 5,11 | 27028 | < 0,001 | < 0,001 | rejeita H0 | 0,0038 (f² 0,0039) | com peso (robusto (cada pessoa é a sua UPA)) |
| H5.3 | Xuzhou | PSQI (0-21) | sas_sv | 0,088 (0,075 a 0,101) | 13,07 | 2308 | < 0,001 | < 0,001 | rejeita H0 | 0,0680 (f² 0,0740) | sem peso (não há desenho complexo) |
| H5.4 | Argentina | latência (min) | tela_presono_h | -1,323 (-2,345 a -0,300) | -2,54 | 686 | 0,011 | 0,023 | rejeita H0 | 0,0092 (f² 0,0094) | sem peso (não há desenho complexo) |
| H5.5 | Turquia | latência (min) | doomscrolling | 0,101 (0,030 a 0,172) | 2,81 | 1213 | 0,005 | 0,015 | rejeita H0 | 0,0064 (f² 0,0065) | sem peso (não há desenho complexo) |
| H5.6 | Japão | AIS (8-32) | celular_presono_h | 0,847 (0,159 a 1,535) | 2,42 | 377 | 0,016 | 0,023 | rejeita H0 | 0,0153 (f² 0,0155) | sem peso (não há desenho complexo) |

Leitura (um coeficiente por base, unidades do desfecho, demais variáveis fixas):

- **Vigitel (H5.1):** quem usa tela digital ≥ 3 h/dia tem índice de insônia 0,59 ponto maior (IC 0,36 a 0,82) que quem usa < 1 h, com idade, sexo e escolaridade fixos. O bloco de tela acrescenta 0,38% de R² (ponderado).
- **Xuzhou (H5.3):** cada ponto a mais no SAS-SV se associa a 0,088 ponto a mais no PSQI (IC 0,075 a 0,101); 10 pontos de SAS-SV ≈ 0,88 ponto de PSQI. Maior tamanho de efeito da família (ΔR² = 0,068).
- **Argentina (H5.4):** cada hora de tela antes de dormir se associa a -1,32 min de latência (IC -2,34 a -0,30). **O sinal é o contrário do esperado** (menos latência com mais tela). Com a série escolar no lugar da idade (mais casos completos), o p fica acima de 0,05 (ver sensibilidade).
- **Turquia (H5.5):** cada ponto de doomscrolling se associa a 0,101 min de latência (IC 0,030 a 0,172); 10 pontos ≈ 1,01 min. Rótulo da escala confirmado por evidência indireta, sem codebook (T080).
- **Japão (H5.6):** cada hora de celular nas 3 h antes de dormir se associa a 0,85 ponto a mais na AIS (IC 0,16 a 1,54).

**Testes do modelo, fora das famílias** (o que o SUMMARY OUTPUT mostra; sem peso, como no Excel):

| Base | n | R² | R² ajustado | F global (gl) | p do F global | F parcial da tela (gl) | p | ΔR² |
|---|---|---|---|---|---|---|---|---|
| Vigitel 2024 | 27029 | 0,0545 | 0,0542 | 259,36 (6; 27022) | < 0,001 | 48,54 (2; 27022) | < 0,001 | 0,0034 |
| Xuzhou | 2317 | 0,0803 | 0,0771 | 25,17 (8; 2308) | < 0,001 | 170,71 (1; 2308) | < 0,001 | 0,0680 |
| Argentina | 692 | 0,0242 | 0,0170 | 3,40 (5; 686) | 0,005 | 6,45 (1; 686) | 0,011 | 0,0092 |
| Turquia | 1216 | 0,0086 | 0,0070 | 5,26 (2; 1213) | 0,005 | 7,87 (1; 1213) | 0,005 | 0,0064 |
| Japão | 381 | 0,0158 | 0,0080 | 2,02 (3; 377) | 0,111 | 5,86 (1; 377) | 0,016 | 0,0153 |

No Japão o F global não é significativo (p = 0,111), mas o coeficiente da tela é: idade (p = 0,774) e sexo (p = 0,659) diluem o F, que testa os três coeficientes juntos. O F global não substitui o teste da hipótese.

## Família R2 — ANOVA e teste t

| H | Base | Teste | Estatística (com peso) | gl | p | p Holm | Decisão | Efeito | Sem peso (Excel) |
|---|---|---|---|---|---|---|---|---|---|
| H5.7 | Vigitel 2024 | ANOVA de um fator (3 faixas de tela) | 9,61 | 2; 27027 | < 0,001 | < 0,001 | rejeita H0 | η² ponderado (R² da regressão nas dummies): 0,0028 | F = 34,91, gl = 2; 27026, p < 0,001, η² = 0,0026 |
| H5.9 | Vigitel 2024 | t de Welch: ≥ 3 h × < 1 h | 4,00 | 15774 | < 0,001 | < 0,001 | rejeita H0 | d de Cohen ponderado (DP combinado dentro dos grupos): 0,1241 | t = 6,89, gl = 15309,2, p < 0,001, d = 0,110 |

- **d de Cohen:** a mesma definição sem e com peso: diferença de médias dividida pelo DP combinado dentro dos grupos (com peso, pesos normalizados para somar n).

## Médias do índice de insônia por faixa de tela (`tabelas/medias_por_faixa.csv`)

| Base | Faixa | n | Média | DP | Média com peso |
|---|---|---|---|---|---|
| vigitel2024 | < 1 h | 8874 | 4,36 | 3,59 | 4,25 |
| vigitel2024 | 1 a < 3 h | 11254 | 4,34 | 3,23 | 4,30 |
| vigitel2024 | ≥ 3 h | 6901 | 4,74 | 3,32 | 4,68 |

## Bruta × ajustada (`tabelas/bruta_ajustada.csv`)

| Base | Versão | b simples (só tela) | p | b múltipla | p |
|---|---|---|---|---|---|
| vigitel2024 | sem peso | 0,381 (0,275 a 0,488) | < 0,001 | 0,557 (0,444 a 0,670) | < 0,001 |
| vigitel2024 | com peso (robusto (cada pessoa é a sua UPA)) | 0,429 (0,219 a 0,639) | < 0,001 | 0,591 (0,364 a 0,817) | < 0,001 |
| xuzhou | sem peso | 0,086 (0,073 a 0,099) | < 0,001 | 0,088 (0,075 a 0,101) | < 0,001 |
| argentina | sem peso | -1,203 (-2,228 a -0,178) | 0,022 | -1,323 (-2,345 a -0,300) | 0,011 |
| turquia | sem peso | 0,107 (0,037 a 0,178) | 0,003 | 0,101 (0,030 a 0,172) | 0,005 |
| japao | sem peso | 0,828 (0,155 a 1,502) | 0,016 | 0,847 (0,159 a 1,535) | 0,016 |

No Vigitel o coeficiente da tela cresce ao ajustar (confundimento negativo pelas covariáveis em conjunto). Quem usa ≥ 3 h é mais jovem: idade média 37,7 × 53,2 anos (< 1 h). Mesmo sentido do confundimento por idade visto na exploração da PNS.

## Pressupostos (`tabelas/diagnostico.csv`)

| Base | n | Breusch-Pagan p | Jarque-Bera p | VIF da tela | VIF máximo (regressor) | Influentes (Cook > 4/n) |
|---|---|---|---|---|---|---|
| vigitel2024 | 27029 | < 0,001 | < 0,001 | 1,57 | 1,98 (esc_superior) | 1183 (4,4%) |
| xuzhou | 2317 | < 0,001 | < 0,001 | 1,02 | 1,09 (serie_2) | 115 (5,0%) |
| argentina | 692 | 0,160 | < 0,001 | 1,01 | 1,03 (esc_pais_2) | 28 (4,0%) |
| turquia | 1216 | 0,064 | < 0,001 | 1,02 | 1,02 (idade) | 59 (4,9%) |
| japao | 381 | 0,269 | < 0,001 | 1,04 | 1,12 (sexo_cod2) | 20 (5,2%) |

- Resíduos não normais em todas as bases (desfechos discretos e assimétricos). Com n de centenas ou mais, t e F seguem aproximadamente válidos; os QQ-plots estão em `figuras/diagnostico_<base>.png`.
- Heterocedasticidade no Vigitel e em Xuzhou: a sensibilidade com EP robusto HC3 não muda nenhuma decisão das bases sem peso.
- VIF da tela ≤ 1,6 e VIF máximo ≤ 2,0 em todas as bases. A categoria de referência das dummies é a mais frequente; com a menor como referência (renda 1 em Xuzhou, escolaridade dos pais 1 na Argentina) o VIF dessas dummies passava de 10, sem mudar o coeficiente da tela.

## Sensibilidade (`tabelas/sensibilidade.csv`)

| H | Análise | b | p | Muda a decisão a 5%? |
|---|---|---|---|---|
| H5.1 | EP robusto HC3 (sem peso) | 0,557 | < 0,001 | não |
| H5.1 | sem observações influentes (Cook > 4/n) | 0,530 | < 0,001 | não |
| H5.1 | sem peso (o que o Excel calcula) | 0,557 | < 0,001 | não |
| H5.1 | desfecho secundário: sono_horas (com peso) (exploratória) | 0,095 | 0,087 | — |
| H5.3 | EP robusto HC3 (sem peso) | 0,088 | < 0,001 | não |
| H5.3 | sem observações influentes (Cook > 4/n) | 0,103 | < 0,001 | não |
| H5.4 | EP robusto HC3 (sem peso) | -1,323 | 0,001 | não |
| H5.4 | sem observações influentes (Cook > 4/n) | -0,986 | 0,002 | não |
| H5.4 | log(1 + latência) | -0,062 | 0,002 | não |
| H5.4 | série escolar no lugar da idade (mais casos completos) | -0,742 | 0,093 | sim |
| H5.4 | desfecho secundário: sono_horas (exploratória) | -0,023 | 0,432 | — |
| H5.5 | EP robusto HC3 (sem peso) | 0,101 | 0,013 | não |
| H5.5 | sem observações influentes (Cook > 4/n) | 0,048 | 0,096 | sim |
| H5.5 | log(1 + latência) | 0,004 | 0,014 | não |
| H5.5 | desfecho secundário: sono_horas (exploratória) | -0,000 | 0,947 | — |
| H5.6 | EP robusto HC3 (sem peso) | 0,847 | 0,033 | não |
| H5.6 | sem observações influentes (Cook > 4/n) | 0,960 | 0,003 | não |
| H5.6 | desfecho secundário: sono_horas (exploratória) | -0,097 | 0,319 | — |

Pontos de atenção da sensibilidade:
- **H5.4 (Argentina):** depende de quem entra na amostra: com a série escolar no lugar da idade (159 casos a mais), p > 0,05.
- **H5.5 (Turquia):** sem as observações influentes, p > 0,05; com log(1 + latência), mantém.

## Limitações

- Dados transversais: associação, não efeito.
- Vigitel cobre só as capitais. Sem os EUA, não há comparação entre países nesta spec (ver spec 004).
- Os desfechos são escalas diferentes em cada base; os coeficientes só são comparáveis dentro da base (a comparação padronizada entre países é a spec 004).
- Latência da Argentina e da Turquia concentrada em valores redondos (5, 10, 15, 30, 60 min).
- Turquia: rótulo da escala de doomscrolling inferido sem codebook; sexo sem rótulo, fora do modelo.
- Xuzhou e Japão: sexo entra como código 1/2 sem rótulo documentado.
- Argentina: adolescentes sem idade (163) ou sem escolaridade dos pais ficam fora do modelo principal (692 de 864).
