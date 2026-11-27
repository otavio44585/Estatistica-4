# 003 — Brasil: tela e sono nas duas pesquisas nacionais (PNS 2019 e Vigitel 2024)

Status: **concluída** (2026-11-27), aprovação do grupo pendente. Resultados em `resultados/003/RESUMO.md`.

> **Decisão de 2026-11-27: os EUA (NHANES 2005-06) saíram do trabalho inteiro.** A única base dos EUA é de 2005, antes do smartphone, e o tempo de tela daquela época não é comparável com o de 2019–2024. As hipóteses que usavam o NHANES (H3.3, H3.6 e as partes NHANES de H3.4, H3.7 e H3.8) foram retiradas; a numeração original foi mantida. A pasta e o pacote mantêm o nome `brasil-eua`/`brasil_eua` só para não quebrar links.

## Pergunta

Em adultos brasileiros, o tempo de tela no lazer se associa a problemas de sono nas duas pesquisas nacionais (PNS 2019 e Vigitel 2024), e a associação tem o mesmo tamanho nas duas, entre faixas etárias e entre TV e tela digital?

(Pergunta original, até 2026-11-27: "a associação tem a mesma magnitude no Brasil e nos EUA?". Ver Histórico.)

## Contexto e transparência

A análise exploratória de 2026-11-27 (`docs/exploratorio_comparativo_br_eua_2026-11-27.*`) estimou razões de prevalência (RP) ajustadas só por idade, comparando tela ≥ 3 h/dia com < 1 h/dia:

| Base | Computador/celular | TV |
|---|---|---|
| PNS 2019 | 1,17 (1,12–1,22) | 1,18 (1,14–1,22) |
| Vigitel 2024 | 1,23 (1,15–1,31) | 1,24 (1,17–1,32) |
| NHANES 2005-06 | 1,38 (1,14–1,68) | 1,36 (1,14–1,64) |

A diferença Brasil × EUA não foi significativa (p de 0,10 a 0,34). A linha do NHANES fica aqui como registro histórico da exploração; os EUA saíram do trabalho em 2026-11-27. **As hipóteses abaixo foram formuladas depois de ver esses números.** A análise confirmatória usa o modelo, as covariáveis e os pesos fixados no plano, e o relatório declara isso.

## População e medidas

Adultos (≥ 18 anos) de PNS 2019 e Vigitel 2024, com as variáveis harmonizadas da spec 001: exposição `tela_digital_cat` e `tela_tv_cat`; desfechos `dif_adormecer_freq` (Vigitel) e `problema_sono_freq` (PNS). O índice de insônia (`insonia_idx`, 0–12) em regressão linear está na spec 005.

## Hipóteses

α = 0,05 bilateral. Holm dentro de cada família.

**Família 1 — associação em cada pesquisa brasileira** (exposição alta × baixa, ajustada por idade, sexo e escolaridade)

| # | H1 | H0 |
|---|---|---|
| H3.1 | Vigitel 2024: RP de dificuldade para adormecer quase sempre/sempre ≠ 1 com tela digital alta (sinal esperado > 1) | RP = 1 |
| H3.2 | PNS 2019: RP de problema de sono frequente ≠ 1 com tela digital alta (sinal esperado > 1) | RP = 1 |
| ~~H3.3~~ | ~~NHANES 2005-06~~ — **retirada em 2026-11-27, EUA fora do trabalho** | — |
| H3.4 | Há tendência dose-resposta nas 3 faixas de exposição no Vigitel e na PNS (a parte NHANES foi retirada em 2026-11-27) | sem tendência |

A H3.5 (diferença de médias do índice de insônia) foi transferida para a spec 005, em 2026-11-27.

**Família 2 — comparação**

| # | H1 | H0 |
|---|---|---|
| ~~H3.6~~ | ~~Brasil (Vigitel) × EUA (NHANES)~~ — **retirada em 2026-11-27, EUA fora do trabalho** | — |
| H3.7 | A RP difere por faixa etária, no Vigitel e na PNS (a exploração viu 1,42 em 18–29 anos na PNS; a parte NHANES foi retirada em 2026-11-27) | sem interação idade × tela |
| H3.8 | A RP da TV difere da RP da tela digital, no Vigitel e na PNS (a parte NHANES foi retirada em 2026-11-27) | RP_TV = RP_digital |
| H3.9 | A RP difere entre as duas bases brasileiras (PNS × Vigitel) | RP_PNS = RP_Vigitel |

**Sensibilidade** (não entra nas famílias): adicionar depressão como covariável, reportada à parte porque pode ser mediadora; estimativas sem peso; corte alternativo de exposição alta (≥ 4 h); renda onde existir.

## Critérios de aceite

- Para cada hipótese: estimativa, IC 95% com o desenho amostral, estatística do teste, p e p ajustado por Holm.
- Bruta e ajustada lado a lado.
- Figura com as RP das duas pesquisas brasileiras e intervalo de confiança.
- Seção de limitações com, no mínimo: itens diferentes na PNS e no Vigitel, Vigitel restrito às capitais, dados transversais, e a ausência de comparação internacional nesta spec (EUA retirados; a comparação com outros países fica na 004).

## Fora de escopo

Causalidade e análise formal de mediação.

## Perguntas em aberto

1. Ferramenta para o desenho amostral: decidida em 2026-11-27 (Python, linearização com estrato e UPA; ver plano). O grupo pode revisar.
2. Renda entra no conjunto mínimo de covariáveis? O Vigitel não tem a variável no inventário.

## Histórico

- 2026-11-27: rascunho, depois da análise exploratória.
- 2026-11-27: H3.5 e o critério de regressão linear transferidos para a spec 005; a família 1 fica com H3.1–H3.4.
- 2026-11-27: executada (T040–T050). Decisões e desvios:
  - Ferramenta: Python (R não instalado). Variância por linearização de Taylor com estrato e UPA, implementada em `analise/brasil_eua/survey.py` e testada contra o `statsmodels`. Vigitel: só peso (sanduíche robusto). Testes de coeficiente com t e gl do desenho (UPAs − estratos: PNS 7.453, NHANES 15).
  - Família 1 rodada por exposição (digital e TV), com Holm separado em cada uma, como no plano.
  - Família 2: exposição digital fixada no código como principal antes de rodar; TV reportada como complementar, fora de Holm. H3.7 e H3.8 têm um teste por base (3 + 3); família 2 = 8 testes.
  - H3.6: teste principal = interação país × tela (categoria ≥ 3 h, 1 gl) na base empilhada; z dos log-RP e interação conjunta (2 gl) como conferência.
  - H3.8: TV e digital no mesmo modelo (RP mutuamente ajustadas), contraste β_TV − β_digital.
  - Sensibilidade de corte alternativo: ≥ 4 h no Vigitel e no NHANES; na PNS, ≥ 6 h (a PNS não separa 4 h). Renda não existe no contrato: não feita.
  - Exploratório, fora da spec: teste de desvio da linearidade (β₁ = β₂/2) e H3.6 sem peso. Ambos rotulados no RESUMO.
- 2026-11-27: correções da verificação independente (revisor externo, modelo Fable). Mudanças:
  - **H1 de H3.1–H3.3** reescrita como bilateral ("RP ≠ 1, sinal esperado > 1"), que é o teste que sempre rodou (α bilateral); o texto antigo dizia "RP > 1". Desfecho do NHANES descrito como "often/almost always (5 ou mais vezes por mês)".
  - **Graus de liberdade:** UPAs − estratos passa a ser a regra única do projeto (a 005 se alinha). A regra do `svyglm` (d − p + 1) entra como sensibilidade em `hipoteses.csv` (`p_svyglm`, `p_holm_svyglm`) e `sensibilidade.csv`. **A decisão de H3.3 é sensível à regra:** p Holm 0,033 com 15 gl (rejeita) e 0,061 com 7 gl (não rejeita). Nenhuma outra decisão muda.
  - **Wald conjunto (H3.7) com correção de Korn-Graubard:** no NHANES, F(6; 15) = 2,80, p = 0,050 passa a F(6; 10), p = 0,183. A decisão não muda (Holm 1,000), e o resultado deixa de parecer limítrofe.
  - **Base empilhada (H3.6):** o gl mostrado passa de 27.043 para 15 (gl do NHANES). Satterthwaite dá 8,9 (digital) e 12,5 (TV); a verificação estimava ~17. p digital 0,617 (Satterthwaite 0,622), sem mudança de decisão. Na TV (complementar, fora de Holm), p 0,004 passa a 0,012, e sem peso 0,233.
  - **RP por faixa etária por domínio:** variância com todas as UPAs e estratos. Na PNS, 8.027 UPAs e 7.453 gl; antes, segundo a verificação, 6.076 gl e 10 estratos com 1 UPA.
  - **Textos:** RESUMO, notebook e explicação trocam "não diferem / a mesma" por "não foi detectada diferença", com IC. Holm descrito como "no máximo 5%".
  - **Decisões que mudaram:** nenhuma na regra principal. H3.3 muda só na sensibilidade de gl.
- 2026-11-27: **EUA (NHANES 2005-06) retirados do trabalho inteiro**, por decisão do usuário: "a única base deles foi de 2005; pode tirar do trabalho inteiro". Motivo: tempo de tela de 2005, antes do smartphone, não é comparável com o de 2019–2024, e a comparação mistura país e época. Decisão tomada depois de ver os resultados (H3.3 e H3.6 já tinham sido estimadas), registrada aqui por transparência. Mudanças:
  - Spec passa a ser "Brasil: tela e sono nas duas pesquisas nacionais (PNS 2019 e Vigitel 2024)".
  - Retiradas: H3.3, H3.6 e as partes NHANES de H3.4, H3.7 e H3.8 (numeração mantida).
  - Famílias de Holm: família 1 = H3.1, H3.2 e H3.4 (Vigitel e PNS), por exposição, como antes; família 2 = H3.7 (Vigitel, PNS), H3.8 (Vigitel, PNS) e H3.9 (PNS × Vigitel), 5 testes.
  - Sensibilidades sem NHANES; a regra de gl do `svyglm` fica só para a PNS (o Vigitel não tem estrato nem UPA).
  - Figura `rp_por_pais.png` (nome de arquivo mantido) passa a mostrar só PNS e Vigitel.
