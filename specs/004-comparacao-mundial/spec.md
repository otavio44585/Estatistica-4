# 004 — Comparação mundial

Status: **concluída** (2026-11-27). Executada a pedido de um integrante, antes da aprovação formal do grupo (pendente). Resultados: `resultados/004/RESUMO.md`.

## Pergunta

Como a associação entre uso de tela e sono estimada no Brasil se posiciona frente a outros países (reanálise dos microdados abertos) e frente às meta-análises publicadas?

## Por quê

As bases de outros países usam escalas diferentes (PSQI, AIS, SAS-SV, doomscrolling), então a RP da spec 003 não serve para todas. Uma métrica padronizada comum permite pôr todas as bases no mesmo gráfico e testar se o efeito varia entre países e entre tipos de exposição.

## Métrica comum

Correlação entre a medida de exposição e o escore de sono de cada base: ρ de Spearman como principal e r de Pearson como conferência, com IC 95% por transformação z de Fisher. Sinal padronizado: **positivo = mais tela, pior sono** (inverte-se o sinal quando o desfecho for "quanto maior, melhor", como duração).

## Bases e pares exposição × desfecho (proposta)

| Base | País | Tipo de exposição | Exposição | Desfecho |
|---|---|---|---|---|
| PNS 2019 | Brasil | tempo total diário | `tela_digital_cat` | `problema_sono_freq` (ordinal original) |
| Vigitel 2024 | Brasil | tempo total diário | `tela_digital_cat` | `insonia_idx` |
| NHANES 2005-06 | EUA | tempo total diário | `tela_digital_cat` | `insonia_idx` |
| Argentina | Argentina | tempo total e pré-sono | horas/dia; horas antes de dormir | latência; duração |
| Japão | Japão | pré-sono | horas de celular nas 3 h antes de dormir | AIS |
| Xuzhou | China | uso problemático | SAS-SV | PSQI |
| Turquia | Turquia | uso problemático | doomscrolling | PSQI; latência |
| Holanda (complementar) | Holanda | pré-sono, por log de app | `prebed_use` | `sleep_qual` (associação intrapessoal; marcada à parte) |

## Hipóteses

| # | H1 | H0 |
|---|---|---|
| H4.1 | A associação varia entre as bases (heterogeneidade) | efeito comum a todas (Q de Cochran não significativo) |
| H4.2 | O tipo de exposição explica parte da variação: tempo total < pré-sono < uso problemático | sem diferença entre subgrupos (Q entre subgrupos) |
| H4.3 | A estimativa brasileira difere da estimativa combinada dos outros países com o mesmo tipo de exposição (tempo total) | igual |
| H4.4 | A estimativa combinada das nossas reanálises fica dentro do IC da meta-análise de referência para o mesmo par (Han, Zhou e Liu, 2024: uso geral × qualidade do sono r = 0,28; IC 0,21–0,35) | fora do IC |

A ordem de H4.2 vem da literatura: uso problemático com efeito maior que uso geral (Han, Zhou e Liu, 2024) e uso na cama com efeito maior que uso diário (Bourke et al., 2026; Hjetland et al., 2025).

## Critérios de aceite

- Tabela com a definição exata de exposição e desfecho em cada base, o n e o grau de equivalência.
- Gráfico de floresta com todas as bases, Brasil destacado, e a estimativa combinada por modelo de efeitos aleatórios.
- Q, gl, p, I² e τ² globais e por subgrupo.
- Teste de H4.3 e posição frente à meta-análise de referência (H4.4).
- Sensibilidade: deixar uma base de fora por vez; incluir as bases de procedência questionável em separado.

## Fora de escopo

Uma meta-análise sistemática da literatura. As meta-análises publicadas entram só como referência de comparação.

## Perguntas em aberto

1. Os pares exposição × desfecho acima estão aprovados? Cada base entra com um par só ou com vários?
2. A Holanda (associação intrapessoal) entra no mesmo gráfico ou só como contraponto?

## Histórico

- 2026-11-27: rascunho.
- 2026-11-27: executada. Decisões (revisáveis pelo grupo):
  - **Pares:** um par principal por base, fixado no plano antes do cálculo (Argentina: tempo total × latência; Turquia: doomscrolling × PSQI). Os demais pares entram em sensibilidade.
  - **Holanda:** contraponto intrapessoal à parte (correlação de medidas repetidas), fora do gráfico e da meta-análise.
  - **H4.3:** "Brasil" = PNS + Vigitel combinados por efeitos aleatórios, comparado com NHANES + Argentina (outros com tempo total).
  - **H4.4:** testada como equivalência (TOST) com as margens no IC de Han, Zhou e Liu (2024).
  - **Família de testes:** H4.1–H4.4, com Holm.
  - **Resultados:** H4.1 rejeita H0 (I² = 98,4%); H4.2, H4.3 e H4.4 não rejeitam.
  - **Desvio do plano:** foi acrescentada uma sensibilidade exploratória com o ρ parcial ajustado por idade (princípio 11), porque a PNS mostrou sinal invertido pelo confundimento por idade. Ela não substitui a análise principal.
- 2026-11-27, correções da verificação independente. **Nenhuma decisão de H4.1–H4.4 mudou.**
  - **IC de Hartung-Knapp** ao lado do DerSimonian-Laird, porque o IC normal é otimista com k = 7. O global passa de 0,017–0,146 (DL, p = 0,014) para −0,016–0,178 (HK, p = 0,087) e deixa de excluir o zero. Nenhum teste da família usa esse IC.
  - **H4.2 registrada como hipótese ordenada e testada como omnibus.** O Q entre subgrupos, fixado no plano, não usa a ordem. Uma meta-regressão das médias de subgrupo sobre o escore 0/1/2 entra como **exploratória**, fora de Holm: inclinação 0,099 na escala z, p = 0,026. O subgrupo pré-sono tem k = 1 (só o Japão), sem τ² próprio.
  - **Efeito do desenho.** Os EP das correlações nos inquéritos ignoram o desenho. O deff de Kish dos pesos é PNS 3,21, Vigitel 3,74 e NHANES 1,61. Sensibilidade com a variância × deff: global 0,082; Q 242,6; I² 97,5%; τ² 0,0107; H4.3 p = 0,752.
  - **Texto.** "Brasil não difere" virou "não foi detectada diferença", com o IC da diferença (−0,112 a 0,080, escala z).
- 2026-11-27, **decisão do grupo: NHANES 2005-06 sai do trabalho inteiro.** Motivo dado pelo integrante: a única base dos EUA é de 2005, antes do smartphone, e mistura país com época. Registrada antes de mudar o código.
  - A meta-análise passa a ter **6 bases** (PNS, Vigitel, Argentina, Japão, Xuzhou, Turquia). O subgrupo "tempo total" fica com PNS, Vigitel e Argentina.
  - H1–H0 das hipóteses não mudam. Em H4.3 (Brasil × outros com tempo total), o grupo "outros" passa a ter **k = 1** (só a Argentina, adolescentes): o teste compara o Brasil com uma única base e deve ser lido com essa ressalva.
  - **Análise nova, EXPLORATÓRIA (decidida depois de ver os resultados, fora de Holm):** Brasil (PNS + Vigitel) × resto do mundo (Argentina, Japão, China, Turquia, todas as exposições juntas), com DL e Hartung-Knapp. Linha "resto do mundo (4 bases)" em `meta_analise.csv` e comparação em `exploratorio_referencia.csv`. Mistura tipos de exposição (tempo total, pré-sono, uso problemático); por isso não substitui H4.3.
