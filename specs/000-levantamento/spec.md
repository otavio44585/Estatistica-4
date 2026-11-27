# 000 — Levantamento: estado da arte e fontes de dados

Status: **concluída** em 2026-11-13. Spec registrada depois da execução, para fechar o histórico.

## Pergunta

O que a literatura internacional e brasileira estabelece sobre uso de telas e sono, e que microdados abertos permitem testar isso?

## Entregas

| Entrega | Arquivo |
|---|---|
| Síntese do estado da arte, questões metodológicas, estudos com regressão linear, evidência brasileira, lacunas, 52 referências ABNT | [`docs/estado-da-arte.md`](../../docs/estado-da-arte.md) |
| Inventário de 30 trabalhos internacionais (DOI verificado, achado, método, covariáveis) | [`docs/inventario-papers-internacional.md`](../../docs/inventario-papers-internacional.md) |
| Inventário de 22 trabalhos brasileiros e latino-americanos | [`docs/inventario-papers-brasil.md`](../../docs/inventario-papers-brasil.md) |
| Inventário de 28 bases baixadas, 17 restritas, ~35 descartadas, com códigos de variável conferidos no arquivo | [`docs/inventario-dados.md`](../../docs/inventario-dados.md) |

## Critérios de aceite

- [x] Toda referência com DOI resolvido no Crossref e no OpenAlex
- [x] Toda variável citada nas bases baixadas conferida no dicionário oficial e no arquivo
- [x] PDFs só de acesso aberto legal; o que não baixou listado com link e motivo
- [x] Bases sintéticas ou de procedência questionável identificadas

## Pendências que não bloqueiam

- 4 papers com versão aberta e 6 pagos sem PDF (lista em `docs/estado-da-arte.md`, seção 8).

## Histórico

- 2026-11-13: levantamento e inventários.
- 2026-11-27: teste de viabilidade para análise fatorial (KMO, Bartlett, α) e comparação exploratória Brasil × EUA (`docs/exploratorio_comparativo_br_eua_2026-11-27.*`). Resultados alimentam as specs 001–004 e estão marcados como exploratórios.
