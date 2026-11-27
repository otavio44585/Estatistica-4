# 004 — Comparação mundial: resumo dos resultados

Gerado por `python -m analise.mundial.rodar` em 2026-11-27. Notebook: `analise/notebooks/05_comparacao_mundial.ipynb`. Todos os números abaixo vêm dos CSV citados em `resultados/004/tabelas/`.

**Métrica:** ρ de Spearman entre exposição e desfecho; sinal padronizado, **positivo = mais tela, pior sono**. IC 95% pela transformação z de Fisher com EP de Fieller, Hartley e Pearson (1957).

## Efeito por base (par principal fixado antes do cálculo) — `efeitos_por_base.csv`

| Base | Tipo | Exposição × desfecho | n | ρ (IC 95%) | r de Pearson | Peso aleatório |
|---|---|---|---|---|---|---|
| PNS 2019 (Brasil) | tempo total | computador/celular no lazer × problema no sono (PHQ-9) | 88.531 | −0,031 (−0,038; −0,024) | −0,029 | 15,8% |
| Vigitel 2024 (Brasil) | tempo total | computador/celular no tempo livre × índice de insônia | 27.029 | 0,063 (0,051; 0,076) | 0,054 | 15,7% |
| NHANES 2005-06 (EUA) | tempo total | computador/games × índice de insônia | 5.551 | 0,034 (0,007; 0,061) | 0,031 | 15,4% |
| Pérez-Chada (Argentina) | tempo total | horas de tela/dia × latência | 733 | 0,021 (−0,054; 0,095) | 0,024 | 13,1% |
| Okajima (Japão) | pré-sono | celular nas 3 h antes de dormir × AIS | 381 | 0,145 (0,042; 0,244) | 0,123 | 11,3% |
| Xuzhou (China) | uso problemático | SAS-SV × PSQI | 2.317 | 0,279 (0,240; 0,317) | 0,259 | 14,8% |
| Doomscrolling (Turquia) | uso problemático | doomscrolling × PSQI | 1.216 | 0,070 (0,013; 0,128) | 0,080 | 14,0% |

**T061 (erro padrão):** o EP por bootstrap (1.000 reamostragens, semente 2026) divergiu no máximo 5,4% (Japão) da fórmula de Fieller, Hartley e Pearson. Ficou abaixo do limiar de 10% fixado no plano, então a meta-análise usa a fórmula.

## Meta-análise — `meta_analise.csv`

IC 95% por dois métodos: DerSimonian-Laird (normal, o fixado no plano) e Hartung-Knapp (t com k − 1 gl, acrescentado na verificação independente; mais honesto com poucas bases).

| Combinação | k | ρ | IC 95% DL | IC 95% Hartung-Knapp | Q (gl), p | I² | τ² |
|---|---|---|---|---|---|---|---|
| Global, efeitos aleatórios | 7 | 0,081 | 0,017; 0,146 (p = 0,014) | −0,016; 0,178 (p = 0,087) | 382,2 (6), p < 0,001 | 98,4% (IC 97,8%–98,9%) | 0,0070 |
| Tempo total | 4 | 0,022 | −0,041; 0,084 | −0,044; 0,087 | 184,6 (3), p < 0,001 | 98,4% | 0,0038 |
| Pré-sono | 1 | 0,145 | 0,042; 0,244 | — (k = 1, uma base só) | — | — | — |
| Uso problemático | 2 | 0,178 | −0,032; 0,372 | −0,831; 0,914 | 35,0 (1), p < 0,001 | 97,1% | 0,0226 |
| Brasil (PNS + Vigitel) | 2 | 0,016 | −0,077; 0,108 | −0,526; 0,549 | 175,0 (1), p < 0,001 | 99,4% | 0,0045 |
| Outros com tempo total (NHANES + Argentina) | 2 | 0,032 | 0,007; 0,058 | −0,021; 0,085 | 0,10 (1), p = 0,749 | 0% | 0 |

**Leitura do Hartung-Knapp.** Com o IC de Hartung-Knapp, a estimativa global deixa de excluir o zero. Com k = 2, o t tem 1 gl e o intervalo fica enorme. Nenhum teste da família (H4.1–H4.4) usa esse IC, então nenhuma decisão muda. O que muda é a leitura do "número combinado", que já era fraca por causa da heterogeneidade. O EP manual de Hartung-Knapp bate com `statsmodels` (`sd_eff_w_re_hksj`; `conferencia_statsmodels.csv`).

O modelo de efeito fixo daria ρ global ≈ 0,000, porque a PNS (n = 88 mil, ρ negativo) concentra o peso. O plano fixou efeitos aleatórios; com τ² > 0 cada base pesa entre 11% e 16%. A média manual bate com `statsmodels.combine_effects` (diferença ≤ 6e-14; `conferencia_statsmodels.csv`).

## Hipóteses (família H4.1–H4.4, Holm) — `hipoteses.csv`

| # | H0 | Teste | Estatística | p | p Holm | Decisão |
|---|---|---|---|---|---|---|
| H4.1 | efeito comum a todas as bases | Q de Cochran | Q = 382,2; gl = 6 | < 0,001 | < 0,001 | rejeita H0: a associação varia entre as bases (I² = 98,4%) |
| H4.2 | sem diferença entre tipos de exposição | Q entre subgrupos | Q = 5,27; gl = 2 | 0,072 | 0,216 | não rejeita H0 |
| H4.3 | Brasil = outros países com tempo total | z da diferença (escala z) | z = −0,33; diferença −0,016 (IC −0,112 a 0,080) | 0,743 | 1,000 | não rejeita H0: não foi detectada diferença; o IC é compatível com diferenças pequenas nos dois sentidos |
| H4.4 | tempo total fora de [0,21; 0,35] (Han, Zhou e Liu, 2024) | equivalência (TOST) | z = −5,98 (limite inferior) | 1,000 | 1,000 | não rejeita H0: equivalência não demonstrada; a estimativa (0,022) fica abaixo do intervalo |

- **H4.2, ordem × teste:** a spec registrou H4.2 como hipótese **ordenada**, mas o plano fixou um teste **omnibus** (Q entre subgrupos), que não usa a ordem.
  - A ordem observada é a que a literatura prevê: tempo total 0,022 < pré-sono 0,145 < uso problemático 0,178.
  - O Q entre subgrupos não é significativo. Com 1 a 4 bases por subgrupo o teste tem pouco poder, e "não rejeitar" não mostra igualdade.
  - O pré-sono tem uma base só (Japão), sem τ² próprio.
  - **Exploratório, fora da família de Holm:** uma meta-regressão das três médias de subgrupo sobre o escore 0/1/2 dá inclinação 0,099 na escala z (EP 0,045; z = 2,22; p bilateral 0,026). Isso é compatível com a ordem, mas são só três pontos, e o teste foi escolhido depois de ver os dados (`exploratorio_referencia.csv`).
- **H4.4:** como complemento, a diferença entre a estimativa de tempo total e r = 0,28 dá z = −5,29, p < 0,001.
- **Exploratório, fora da família:** não foi detectada diferença entre o uso problemático (0,178; IC −0,032 a 0,372) e r = 0,33 da mesma meta-análise (z = −1,46, p = 0,143; `exploratorio_referencia.csv`).

## Sensibilidades — `sensibilidade.csv`, `bruta_ajustada_idade.csv`

- **Bruta × ajustada por idade (ρ parcial).** Isto foi acrescentado na execução e é exploratório (ver Histórico da spec).
  - PNS: −0,031 → **0,027** (0,021; 0,034). O sinal se inverte, mesmo padrão da exploração de 27/11 (RP bruta 0,90 → ajustada 1,17).
  - Vigitel: 0,063 → 0,067. NHANES: 0,034 → 0,051.
  - Global ajustado: 0,092 (0,047; 0,136). Tempo total ajustado: 0,045 (0,017; 0,073). Brasil ajustado: 0,047 (0,008; 0,086).
- **Deixar uma base de fora.** O ρ global varia de 0,044 (sem Xuzhou) a 0,102 (sem PNS). Só sem Xuzhou e sem Vigitel o IC inclui 0.
- **ρ ponderado pelo peso amostral:** PNS −0,041, Vigitel 0,069, NHANES 0,015. Global 0,078 (0,008; 0,148).
- **Efeito do desenho (verificação independente).** Os EP das correlações nos inquéritos supõem amostra aleatória simples. O deff de Kish dos pesos é 3,21 na PNS, 3,74 no Vigitel e 1,61 no NHANES (coluna `deff_kish` de `efeitos_por_base.csv`). Com a variância multiplicada pelo deff:
  - global 0,082 (DL 0,003 a 0,161; Hartung-Knapp −0,015 a 0,178);
  - Q cai de 382,2 para 242,6, I² de 98,4% para 97,5%, e τ² vai a 0,0107;
  - tempo total 0,021 (−0,037 a 0,079), com Q de 184,6 para 55,0;
  - H4.3 com deff: z = −0,32, p = 0,752.

  Nenhuma decisão muda. Esse deff só considera os pesos desiguais; estrato e conglomerado não entram.
- **Pares alternativos:**

  | Base | Par | ρ (IC 95%) |
  |---|---|---|
  | Argentina | tela antes de dormir × latência | −0,072 (−0,140; −0,003) |
  | Argentina | tela/dia × duração (invertida) | 0,152 (0,078; 0,224) |
  | Japão | celular antes de dormir × duração (invertida) | 0,124 (0,019; 0,226) |
  | Turquia | doomscrolling × latência | 0,085 (0,027; 0,142) |

- **Procedência questionável** (só aqui, nunca na estimativa principal):

  | Base | ρ |
  |---|---|
  | Paquistão | −0,048 |
  | Bangladesh | 0,341 |
  | Sleep Patterns 2.722 | 0,016 |
  | Sleep Patterns 1.222 | 0,035 |

  Com elas, o global vai a 0,086 (0,030; 0,141).
- **Contraponto intrapessoal, Holanda (Siebers):** nas noites em que o adolescente usou mais o celular na hora antes de deitar (registro por app), a qualidade da noite não foi pior que a habitual dele: r de medidas repetidas = 0,016 (−0,032; 0,064), 1.804 noites. Está fora da meta-análise, porque mede outra coisa (variação dentro da pessoa).

## Limitações

1. **Heterogeneidade extrema** (I² ≈ 98%): a média global resume bases com escalas, populações e anos diferentes. A informação está nos subgrupos e nas bases, não no número combinado.
2. **Exposição em faixas** nos inquéritos (6 a 8 categorias): a correlação de postos com muitos empates fica atenuada.
3. **Correlação bruta como métrica principal:** a PNS mostra confundimento forte por idade. A versão ajustada por idade é sensibilidade, não a análise fixada no plano.
4. **Correspondência aproximada com a referência:** Han, Zhou e Liu (2024) combinam uso geral × qualidade do sono, majoritariamente em jovens. Nossos desfechos são insônia, problema de sono e latência em populações gerais, então H4.4 compara medidas próximas, não idênticas.
5. **Subgrupos pequenos:** pré-sono tem 1 base (sem τ² e sem IC de Hartung-Knapp) e uso problemático tem 2. O τ² com k = 2 é instável.
6. **Dados transversais:** o resultado é uma associação entre tela e sono, não uma relação de causa.
7. **EP dos inquéritos sem o desenho:** a correlação de postos não tem variância por linearização padrão. O deff de Kish (sensibilidade acima) é um limite inferior do efeito do desenho, e a heterogeneidade dos inquéritos fica superestimada.
8. **Poucas bases:** com k = 7, o IC normal do DerSimonian-Laird é otimista. O de Hartung-Knapp inclui o zero na estimativa global.
