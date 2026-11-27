# 004 — Comparação mundial: resumo dos resultados

Gerado por `python -m analise.mundial.resumo` a partir de `resultados/004/tabelas/` (nenhum número digitado). Notebook: `analise/notebooks/05_comparacao_mundial.ipynb`.

**Decisão do grupo (2026-11-27):** o NHANES 2005-06 (EUA) saiu do trabalho inteiro — a única base dos EUA é de 2005, antes do smartphone, e misturava país com época. A meta-análise tem 6 bases (Histórico da spec 004).

**Métrica:** ρ de Spearman entre exposição e desfecho; sinal padronizado, **positivo = mais tela, pior sono**. IC 95% pela transformação z de Fisher com EP de Fieller, Hartley e Pearson (1957).

## Efeito por base (par principal fixado antes do cálculo) — `efeitos_por_base.csv`

| Base | Tipo | Exposição × desfecho | n | ρ (IC 95%) | r de Pearson | Peso aleatório |
|---|---|---|---|---|---|---|
| PNS 2019 (Brasil) | tempo total | computador/tablet/celular no lazer (6 faixas) × problema no sono nas últimas 2 semanas (0-3) | 88.531 | −0,031 (−0,038; −0,024) | −0,029 | 18,4% |
| Vigitel 2024 (Brasil) | tempo total | computador/tablet/celular no tempo livre (8 faixas) × índice de insônia, 3 sintomas (0-12) | 27.029 | 0,063 (0,051; 0,076) | 0,054 | 18,3% |
| Pérez-Chada (Argentina) | tempo total | horas de tela por dia × latência do sono (min) | 733 | 0,021 (−0,054; 0,095) | 0,024 | 15,6% |
| Okajima (Japão) | pré-sono | horas de celular nas 3 h antes de dormir × Escala de Insônia de Atenas (8-32) | 381 | 0,145 (0,042; 0,244) | 0,123 | 13,7% |
| Xuzhou (China) | uso problemático | SAS-SV, dependência de smartphone (10-60) × PSQI (0-21) | 2.317 | 0,279 (0,240; 0,317) | 0,259 | 17,4% |
| Doomscrolling (Turquia) | uso problemático | escala de doomscrolling (15-105) × PSQI turco (0-21) | 1.216 | 0,070 (0,013; 0,128) | 0,080 | 16,6% |

**T061 (erro padrão):** o EP por bootstrap divergiu no máximo 5,4% (Okajima (Japão)) da fórmula de Fieller, Hartley e Pearson, abaixo do limiar de 10% do plano; a meta-análise usa a fórmula (Fieller-Hartley-Pearson).

## Meta-análise — `meta_analise.csv`

IC 95% por DerSimonian-Laird (normal, fixado no plano) e por Hartung-Knapp (t com k − 1 gl; mais honesto com poucas bases).

| Combinação | Papel | k | ρ | IC 95% DL | IC 95% Hartung-Knapp | Q (gl), p | I² | τ² |
|---|---|---|---|---|---|---|---|---|
| global (6 bases) | H4.1 | 6 | 0,090 | 0,015; 0,165 (p = 0,019) | −0,029; 0,207 (p = 0,108) | 375,9 (5), p < 0,001 | 98,7% | 0,0080 |
| subgrupo: tempo total | H4.2 | 3 | 0,017 | −0,060; 0,095 (p = 0,662) | −0,105; 0,139 (p = 0,605) | 175,6 (2), p < 0,001 | 98,9% | 0,0043 |
| subgrupo: pré-sono | H4.2 | 1 | 0,145 | 0,042; 0,244 (p = 0,006) | — (k = 1) | — | — | — |
| subgrupo: uso problemático | H4.2 | 2 | 0,178 | −0,032; 0,372 (p = 0,096) | −0,831; 0,914 (p = 0,345) | 35,0 (1), p < 0,001 | 97,1% | 0,0226 |
| Brasil (PNS + Vigitel) | H4.3 | 2 | 0,016 | −0,077; 0,108 (p = 0,734) | −0,526; 0,549 (p = 0,791) | 175,0 (1), p < 0,001 | 99,4% | 0,0045 |
| outros países, tempo total (Argentina) | H4.3 | 1 | 0,021 | −0,054; 0,095 (p = 0,586) | — (k = 1) | — | — | — |
| resto do mundo (4 bases) | exploratório | 4 | 0,131 | −0,007; 0,265 (p = 0,062) | −0,055; 0,308 (p = 0,110) | 56,2 (3), p < 0,001 | 94,7% | 0,0187 |

**Leitura.** Pelo DerSimonian-Laird a estimativa global (0,090) exclui o zero; pelo Hartung-Knapp (−0,029; 0,207) não exclui. Nenhum teste da família usa esse IC. Com k = 2 o t de Hartung-Knapp tem 1 gl e o intervalo fica enorme. A média manual bate com `statsmodels.combine_effects` (`conferencia_statsmodels.csv`).

## Hipóteses (família H4.1–H4.4, Holm) — `hipoteses.csv`

| # | H0 | Teste | Estatística | p | p Holm | Decisão | Detalhe |
|---|---|---|---|---|---|---|---|
| H4.1 | efeito comum a todas as bases | Q de Cochran | 375,89; gl = 5 | < 0,001 | < 0,001 | rejeita H0 | I² = 98.7% (IC 98.1% a 99.1%); τ² = 0.0080 |
| H4.2 | sem diferença entre os tipos de exposição | Q entre subgrupos | 4,81; gl = 2 | 0,090 | 0,270 | não rejeita H0 | tempo total: ρ = 0.017 (k = 3); pré-sono: ρ = 0.145 (k = 1); uso problemático: ρ = 0.178 (k = 2). Registrada como hipótese ordenada; testada como omnibus (Q entre subgrupos não usa a ordem) |
| H4.3 | Brasil = outros países com tempo total | z da diferença (escala z de Fisher) | −0,08 | 0,939 | 1,000 | não rejeita H0 | ρ Brasil = 0.016; ρ outros = 0.021 (outros com tempo total: k = 1, só a Argentina, adolescentes) |
| H4.4 | estimativa de tempo total fora de [0,21; 0,35] (Han, Zhou e Liu, 2024) | equivalência por dois testes unilaterais (TOST) | −4,93 | 1,000 | 1,000 | não rejeita H0 | ρ tempo total = 0.017 (IC -0.060 a 0.095); diferença para r = 0,28: z = -4.87, p = < 0,001 |

- **H4.2:** registrada como hipótese ordenada e testada como omnibus (Q entre subgrupos, fixado no plano). Com 1 a 3 bases por subgrupo, "não rejeitar" não mostra igualdade. O pré-sono tem uma base só (Japão).
- **H4.3:** sem o NHANES, o lado "outros com tempo total" tem **k = 1** (só a Argentina, adolescentes). Não foi detectada diferença, mas o teste compara o Brasil com uma única base.

## Exploratório (fora da família de Holm) — `exploratorio_referencia.csv`

- exploratório: uso problemático × Han, Zhou e Liu (2024) r = 0,33 (IC 0,28–0,38): ρ = 0,178 (−0,032; 0,372); z = −1,46, p = 0,143.
- complemento de H4.4: diferença tempo total × r = 0,28: ρ = 0,017 (−0,060; 0,095); z = −4,87, p = < 0,001.
- **Tendência ordenada de H4.2:** inclinação 0,100 na escala z (EP 0,048; z = 2,11; p = 0,035). Compatível com a ordem prevista, mas são só três pontos.
- **Brasil × resto do mundo** (pedido do grupo depois de ver os resultados; mistura os tipos de exposição): Brasil (PNS + Vigitel) ρ = 0,016 (−0,077; 0,108) × resto do mundo (Argentina, Japão, China, Turquia) ρ = 0,131 (DL −0,007; 0,265; Hartung-Knapp −0,055; 0,308); diferença na escala z −0,116 (IC −0,283; 0,051), z = −1,36, p = 0,173. Não foi detectada diferença; a associação no resto do mundo puxa para cima por causa das escalas de uso problemático e pré-sono. Figura: `figuras/brasil_vs_resto.png`.

## Sensibilidades — `sensibilidade.csv`, `bruta_ajustada_idade.csv`

- **Bruta × ajustada por idade (ρ parcial; exploratório):**
  - PNS 2019 (Brasil): −0,031 → 0,027 (0,021; 0,034)
  - Vigitel 2024 (Brasil): 0,063 → 0,067 (0,055; 0,080)
  - Pérez-Chada (Argentina): 0,021 → 0,015 (−0,068; 0,097)
  - Okajima (Japão): 0,145 → 0,139 (0,036; 0,239)
  - Doomscrolling (Turquia): 0,070 → 0,068 (0,010; 0,126)
  - subgrupo tempo total com ρ ajustado por idade: 0,043 (0,007; 0,078)
  - Brasil (PNS + Vigitel) com ρ ajustado por idade: 0,047 (0,008; 0,086)
- **Deixar uma base de fora:** ρ global de 0,047 (sem Xuzhou (China)) a 0,117 (sem PNS 2019 (Brasil)).
- **ρ ponderado pelo peso amostral:** PNS 2019 (Brasil) −0,041; Vigitel 2024 (Brasil) 0,069; global com ρ ponderado nos 2 inquéritos 0,090.
- **Desenho amostral (deff de Kish, só PNS e Vigitel):** PNS 2019 (Brasil): EP × √deff de Kish: −0,031 (−0,043; −0,019); Vigitel 2024 (Brasil): EP × √deff de Kish: 0,063 (0,040; 0,087); global com variância × deff de Kish nos inquéritos: 0,091 (−0,004; 0,185), I² 97,9%; subgrupo tempo total com variância × deff de Kish: 0,017 (−0,058; 0,092), I² 95,9%; H4.3 com variância × deff de Kish (Brasil − outros, escala z): 0,016 (−0,124; 0,114), p = 0,933. Nenhuma decisão muda.
- **Pares alternativos:** Pérez-Chada (Argentina): horas de tela antes de dormir × latência do sono (min): −0,072 (−0,140; −0,003); Pérez-Chada (Argentina): horas de tela por dia × duração do sono em dia de semana (h, invertida): 0,152 (0,078; 0,224); Pérez-Chada (Argentina): horas de tela antes de dormir × duração do sono em dia de semana (h, invertida): 0,061 (−0,008; 0,129); Okajima (Japão): horas de celular nas 3 h antes de dormir × duração do sono em dia de semana (h, invertida): 0,124 (0,019; 0,226); Doomscrolling (Turquia): escala de doomscrolling (15-105) × latência do sono (min): 0,085 (0,027; 0,142).
- **Procedência questionável (nunca na estimativa principal):** [procedência questionável] Paquistão (redes sociais × PSQI): −0,048 (−0,153; 0,059); [procedência questionável] Bangladesh v2 (dispositivo antes de dormir × dificuldade para adormecer): 0,341 (0,284; 0,397); [procedência questionável] Sleep Patterns 2.722 (celular antes de dormir × qualidade): 0,016 (−0,023; 0,055); [procedência questionável] Sleep Patterns 1.222 (celular antes de dormir × qualidade): 0,035 (−0,023; 0,092); global incluindo as 4 bases de procedência questionável: 0,092 (0,030; 0,153).
- **Contraponto intrapessoal (Holanda, fora da meta-análise):** [contraponto, intrapessoal] Holanda, Siebers: celular na hora antes de deitar × qualidade da noite (invertida): 0,016 (−0,032; 0,064).

## Limitações

1. **Heterogeneidade extrema** (I² = 98,7%): a média global resume bases com escalas, populações e anos diferentes.
2. **Exposição em faixas** nos inquéritos: a correlação de postos com muitos empates fica atenuada.
3. **Correlação bruta como métrica principal:** a PNS mostra confundimento por idade; a versão ajustada é sensibilidade.
4. **Referência aproximada:** Han, Zhou e Liu (2024) combinam uso geral × qualidade do sono, majoritariamente em jovens.
5. **Subgrupos pequenos:** pré-sono tem 1 base e uso problemático 2; em H4.3 o lado "outros" tem 1 base.
6. **Dados transversais:** o resultado é uma associação entre tela e sono, não uma relação de causa.
7. **EP dos inquéritos sem o desenho:** o deff de Kish é um limite inferior do efeito do desenho.
8. **Poucas bases** (k = 6): o IC normal do DerSimonian-Laird é otimista; o de Hartung-Knapp inclui o zero.
