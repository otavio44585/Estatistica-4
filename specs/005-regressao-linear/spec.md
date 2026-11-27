# 005 — Regressão linear múltipla, ANOVA e teste t

Status: **concluída** (2026-11-27), aprovação do grupo pendente. **EUA fora do trabalho desde 2026-11-27** (ver Histórico): H5.2, H5.8, H5.10 e H5.11 retiradas. Resultados em `resultados/005/RESUMO.md`.

## Pergunta

Quanto o sono (índice de insônia, latência, escore de insônia ou de qualidade) varia com o uso de tela, mantidas fixas idade, sexo e escolaridade? O coeficiente da tela é o mesmo no Brasil e nos EUA?

## Por quê

A disciplina cobra regressão linear múltipla no formato do Excel: R², ANOVA com F, t e p-valor de cada coeficiente, IC 95% e variáveis dummy, como no exercício da aula (salário ~ sexo + qualificado + tempo de serviço). Esta spec aplica a mesma técnica aos microdados e confere cada p-valor por três caminhos independentes.

## Bases e modelos (proposta — o grupo aprova)

| Base | População | Y (desfecho) | X de interesse | Covariáveis | n de partida |
|---|---|---|---|---|---|
| Vigitel 2024 | adultos, 27 capitais | `insonia_idx` (0–12) | tela digital: dummies 1 a < 3 h e ≥ 3 h (referência < 1 h) | idade, sexo, escolaridade (3 faixas) | 27.048 |
| ~~NHANES 2005-06~~ | adultos, EUA | `insonia_idx` (0–12) | computador/games: mesmas faixas | idade, sexo, escolaridade (3 faixas) | 5.563 — **retirada em 2026-11-27 (EUA fora do trabalho)** |
| Xuzhou | universitários, China | PSQI total | SAS-SV (uso problemático de smartphone, 10–60) | sexo, série, renda | 2.317 |
| Pérez-Chada | adolescentes, Argentina | latência (min) | horas de tela antes de dormir | idade, sexo, escolaridade dos pais | 864 |
| Doomscrolling | 18–40 anos, Turquia | latência (min) | escore `FK_TOPLAM` (provável escala de doomscrolling) | idade | 1.216 |
| Okajima | 18–29 anos, Japão | AIS (8–32) | horas de celular nas 3 h antes de dormir | idade, sexo | 381 |

A PNS 2019 fica fora: não tem desfecho de sono contínuo, só o item ordinal do PHQ-9, que a spec 003 trata como binário.

Desfechos secundários, exploratórios e fora das famílias: horas de sono (Vigitel, NHANES, Argentina, Turquia, Japão) e latência no NHANES (topo censurado em 60 min).

## Transparência

A exploração de 2026-11-27 olhou Vigitel e NHANES com outro desfecho (dificuldade frequente para adormecer, binário) e outra medida (razão de prevalências). O índice 0–12 em regressão linear e as quatro bases de repositório ainda não foram analisados.

## Hipóteses

α = 0,05 bilateral. Holm dentro de cada família. O sinal esperado vem da literatura (`docs/estado-da-arte.md`) e não muda o teste, que é bilateral.

**Família R1 — regressão múltipla: coeficiente da tela, com as covariáveis no modelo** (6 testes registrados; 5 depois da retirada de H5.2 em 2026-11-27)

| # | Base | H0 | H1 | Sinal esperado | Teste |
|---|---|---|---|---|---|
| H5.1 | Vigitel | β(≥ 3 h) = 0 | β ≠ 0 | + | t do coeficiente |
| ~~H5.2~~ | NHANES | β(≥ 3 h) = 0 | β ≠ 0 | + | t do coeficiente — **retirada em 2026-11-27 (EUA fora do trabalho)** |
| H5.3 | Xuzhou | β(SAS-SV) = 0 | β ≠ 0 | + | t do coeficiente |
| H5.4 | Argentina | β(tela antes de dormir) = 0 | β ≠ 0 | + | t do coeficiente |
| H5.5 | Turquia | β(`FK_TOPLAM`) = 0 | β ≠ 0 | + | t do coeficiente; só entra se o rótulo da escala for confirmado, senão sai da família como exploratória |
| H5.6 | Japão | β(celular antes de dormir) = 0 | β ≠ 0 | + | t do coeficiente |

**Família R2 — ANOVA, teste t e Brasil × EUA** (5 testes registrados; 2 depois da retirada de H5.8, H5.10 e H5.11 em 2026-11-27)

| # | Base | H0 | H1 | Teste |
|---|---|---|---|---|
| H5.7 | Vigitel | média de `insonia_idx` igual nas 3 faixas de tela | ao menos uma média diferente | ANOVA de um fator (F) |
| ~~H5.8~~ | NHANES | idem | idem | ANOVA de um fator (F) — **retirada em 2026-11-27 (EUA fora do trabalho)** |
| H5.9 | Vigitel | média em ≥ 3 h = média em < 1 h | médias diferentes | t de Welch |
| ~~H5.10~~ | NHANES | idem | idem | t de Welch — **retirada em 2026-11-27 (EUA fora do trabalho)** |
| ~~H5.11~~ | Vigitel + NHANES | coeficientes da tela iguais nos dois países | diferentes | F parcial da interação país × tela (teste de Chow restrito aos coeficientes da tela) — **retirada em 2026-11-27 (EUA fora do trabalho)** |

H5.11 compara diferença de médias (escala aditiva). A spec 003 (H3.6) compara razão de prevalências. As duas podem discordar sem contradição, porque a escala é outra.

**Testes do modelo, reportados fora das famílias.** Aparecem no SUMMARY OUTPUT e ajudam a ler o modelo, mas não respondem à pergunta:

- F global de cada regressão (ANOVA da regressão);
- t de cada covariável;
- F parcial da tela (modelo completo × modelo só com covariáveis) e o ganho de R²;
- testes de pressupostos dos resíduos.

## Verificação dos p-valores

Todo p-valor do relatório é obtido por três caminhos, que precisam concordar:

1. a saída da ferramenta Análise de Dados do Excel (Regressão, ANOVA, Teste-t);
2. o recálculo por fórmula na própria planilha, a partir da estatística e dos graus de liberdade;
3. o recálculo por script, independente do Excel.

Checagens de consistência obrigatórias:

- p < 0,05 se e somente se o IC 95% do coeficiente não contém 0.
- gl do resíduo = n − k − 1, e o "F de significação" é P(F com k e n − k − 1 gl > F observado).
- F parcial com uma restrição = t² do coeficiente.
- F da ANOVA de um fator = F global da regressão de Y nas 2 dummies de tela, sem covariáveis.
- t de duas amostras com variâncias iguais = t da dummy numa regressão simples. O t de Welch difere desse valor, e a diferença é registrada.
- p ajustado por Holm ≥ p bruto. A decisão usa o ajustado.

Formato no relatório: p com 3 casas decimais; abaixo de 0,001, "< 0,001". Nunca "0,000", e a notação científica do Excel (por exemplo 5,07E-18) não vai para o texto.

## Critérios de aceite

- Cada modelo tem tabela no formato SUMMARY OUTPUT: R múltiplo, R², R² ajustado, erro padrão, observações; ANOVA com gl, SQ, MQ, F e F de significação; coeficientes com erro padrão, t, p e IC 95%.
- Cada hipótese tem estatística, gl, p, p Holm, decisão, tamanho de efeito (ganho de R² e f² na regressão, η² na ANOVA, d de Cohen no teste t) e IC 95%.
- Regressão simples (só a tela) e múltipla aparecem lado a lado (princípio 11).
- Vigitel e NHANES têm a estimativa sem peso (a do Excel) e com peso, lado a lado. As decisões de H5.1, H5.2 e H5.7 a H5.11 usam a estimativa com peso (princípio 8).
- A conferência dos três caminhos não tem divergência acima da tolerância do plano.
- Cada modelo tem diagnóstico de resíduos e registro do que foi feito quando um pressuposto falhou.
- O n antes e depois de remover faltantes aparece por base.

## Fora de escopo

Causalidade. Modelos para desfecho censurado (Tobit) ou ordinal, citados como limitação. Regressão de Poisson e razão de prevalências, que estão na spec 003.

## Perguntas em aberto

1. O enunciado exige tudo no Excel, ou Excel mais script é aceito?
2. A Turquia entra sem o codebook de `FK_TOPLAM`?
3. Os adolescentes da Argentina entram? É a mesma pergunta da spec 001.
4. As covariáveis propostas para Xuzhou e Argentina estão aprovadas?

## Histórico

- 2026-11-27: rascunho, a pedido do grupo (regressão linear múltipla, ANOVA, teste t e verificação dos p-valores). A H3.5 da spec 003 (diferença de médias do índice de insônia) foi transferida para cá e virou H5.1, H5.2, H5.9 e H5.10. A entrega passou de 005 para 006.
- 2026-11-27: executada (T080–T092). Decisões e desvios:
  - **T080 (pergunta 2):** rótulo de `FK_TOPLAM` confirmado por evidência indireta, sem codebook: a descrição do depósito lista doomscrolling entre os construtos medidos e FK é o único bloco de 15 itens de 7 pontos (escore 15–105; FK1…FK15 somam `FK_TOPLAM`). H5.5 fica confirmatória com essa ressalva.
  - **Pergunta 3:** adolescentes da Argentina entraram, rotulados. **Pergunta 4:** covariáveis como propostas; Xuzhou com sexo (código 1/2 sem rótulo), série e renda em dummies (referência = categoria 1); Argentina com idade, sexo e escolaridade dos pais em dummies (referência = 1). **Pergunta 1** (Excel × script) continua com o enunciado.
  - Argentina: 163 sem idade → modelo principal com casos completos (n = 692 de 864), como a spec manda; sensibilidade com a série escolar no lugar da idade (n = 851).
  - Caminho A foi a própria ferramenta Análise de Dados (Analysis ToolPak), automatizada por COM; 920 números iguais nos três caminhos.
  - Achado da conferência: o teste t de Welch do Excel arredonda o gl para inteiro; o relatório usa o gl fracionário.
  - Versão com peso: NHANES com linearização (15 estratos, 30 UPAs) e gl pela regra do `svyglm` (UPAs − estratos + 1 − nº de parâmetros = 9 no modelo completo). A spec 003 usou gl = UPAs − estratos = 15; com 15 gl o p de H5.2 muda de 0,158 para 0,145 e a decisão se mantém (`resultados/005/tabelas/sensibilidade.csv`). Vigitel: só peso, erro padrão robusto.
  - H5.7–H5.8 com peso: F de Wald das 2 dummies na regressão ponderada; H5.9–H5.10 com peso: diferença de médias ponderada (regressão na dummy, só os dois grupos); H5.11 com peso: F de Wald das 2 interações.
  - Resultado que contraria o sinal esperado: H5.4 (Argentina), b < 0; rejeita H0, registrado como tal.
- 2026-11-27: correções da verificação independente (nenhuma decisão de hipótese mudou):
  - **Graus de liberdade com peso:** regra única do projeto, igual à da spec 003: gl = UPAs − estratos (NHANES: 15). A regra do `svyglm` (d − p + 1 = 9) passou a ser linha de sensibilidade. H5.2: p de 0,158 para 0,145 (continua não rejeitando H0); H5.10: gl 15, p = 0,393.
  - **Wald com q > 1:** correção de Korn-Graubard, F = (d − q + 1)/(d·q)·W com gl (q, d − q + 1), na ANOVA ponderada, no F global ponderado e na H5.11. H5.8: F(2; 14) = 0,46, p = 0,638.
  - **H5.11:** o gl do teste da interação passou a ser o gl de desenho do NHANES (15), porque a variância da interação vem quase toda dele; antes era o da base empilhada (≈ 27 mil). F(2; 14) = 0,19, p = 0,830.
  - **Estrato com 1 UPA:** `mqp` agora segue a mesma regra de `analise/brasil_eua/survey.py` (centrado na média geral das UPAs, fator 1). Nenhuma base do modelo tem esse caso.
  - **d de Cohen:** a mesma definição sem e com peso (diferença de médias / DP combinado dentro dos grupos; com peso, pesos normalizados para somar n). Vigitel com peso: d = 0,124.
  - **Referência das dummies:** categoria mais frequente (Xuzhou: série e renda; Argentina: escolaridade dos pais e, na sensibilidade, série). VIF máximo caiu de 18,1 (Xuzhou) e 11,4 (Argentina) para ≤ 2,0; o coeficiente da tela não mudou. As planilhas foram regeradas e a Análise de Dados do Excel rodou de novo.
  - **Conferência:** `conferencia.csv` ganhou `dentro_tolerancia` e `excecao_documentada`: 920 de 920 dentro da tolerância + 2 exceções documentadas (p de Welch com gl inteiro no Excel). Em clone limpo, sem `analise/dados/excel/`, a conferência lê `resultados/005/excel_saidas/*.csv`.
  - Texto: "não foi detectada diferença" no lugar de igualdade afirmada; fragilidade de H5.2 sem influentes (p = 0,167) registrada.
- 2026-11-27, **decisão do grupo: EUA fora do trabalho inteiro** ("a única base deles foi de 2005; pode tirar do trabalho inteiro"). Registrado antes de mudar o código. H5.2, H5.8, H5.10 e H5.11 (NHANES 2005-06 e base empilhada Vigitel + NHANES) **retiradas em 2026-11-27 (EUA fora do trabalho)**; a numeração original é mantida. Famílias passam a ser R1 = H5.1, H5.3, H5.4, H5.5, H5.6 e R2 = H5.7, H5.9 (Holm recalculado). Planilhas e saídas do Excel do NHANES e da base empilhada removidas; sem NHANES não sobra base com estrato e UPA na 005, e a sensibilidade pela regra do `svyglm` sai.
