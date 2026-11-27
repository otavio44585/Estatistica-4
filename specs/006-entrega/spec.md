# 006 — Entrega

Status: **primeira versão gerada** (2026-11-27). Formato final depende do enunciado da disciplina.

## Pergunta

O que é entregue, em que formato e como alguém de fora confere que cada número sai dos dados?

## Proposta de conteúdo (ajustar ao enunciado)

| Seção do relatório | Fonte |
|---|---|
| Introdução e pergunta | specs 001–005 |
| Estado da arte | `docs/estado-da-arte.md` |
| Dados e harmonização | spec 001, `resultados/001/` |
| Métodos — cada técnica mostrada (PCA por SVD, análise fatorial, testes de hipótese, meta-análise, regressão linear múltipla, ANOVA, teste t) | planos 002–005 |
| Resultados | `resultados/002/` a `resultados/005/` |
| Conferência dos p-valores (Excel × fórmula × script) | `resultados/005/conferencia.csv` |
| Discussão: Brasil × EUA × mundo × literatura | specs 003, 004 e 005 |
| Limitações | seções de limitação das specs |
| Referências ABNT, só as citadas | `docs/estado-da-arte.md` |

## Critérios de aceite

- Todo número do relatório tem a origem rastreável (arquivo em `resultados/` + script que o gerou).
- Alguém que não participou clona o repositório, define `STAT4_BRUTOS`, roda os scripts e obtém os mesmos números.
- Hipóteses formuladas depois da análise exploratória aparecem rotuladas como tal.
- Nenhuma frase causal para resultado observacional.

## Perguntas em aberto

1. Formato exigido: relatório, notebook, slides, apresentação oral?
2. Prazo e tamanho.
3. Integrantes e divisão das specs.

## Histórico

- 2026-11-27: rascunho.
- 2026-11-27: renumerada de 005 para 006; a 005 passou a ser a regressão linear múltipla.
- 2026-11-27: primeira versão gerada sem o enunciado. Entregáveis:
  - `docs/relatorio.md` (gerado de `docs/modelos/relatorio.md`; todo número vem de `resultados/` por `analise/relatorio/numeros.py`);
  - `docs/roteiro_apresentacao.md` (roteiro de 19 min com falas, telas e perguntas prováveis);
  - `site/*.html` (7 páginas autocontidas);
  - explicações em `docs/explicacoes/`;
  - `tests/test_006_entrega.py`, que cobre: nenhum marcador pendente, nenhuma frase causal afirmativa, páginas sem dependência externa, referências com DOI.
- 2026-11-27: slides em `site/apresentacao.html` (19 slides 16:9, gerados de `docs/modelos/apresentacao.html` com os números dos CSVs, notas do apresentador, exportação em PDF pelo navegador); design system da ESEG nas páginas do site; README gerado de `docs/modelos/README.md`; `index.html` e `.nojekyll` na raiz para o GitHub Pages servir da branch `main` (ativação pelo dono do repositório). Bloco de conclusões do roteiro passou de 1 para 2 min (19 min no total).
