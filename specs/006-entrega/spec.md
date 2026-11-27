# 006 — Entrega

Status: **primeira versão gerada** (2026-11-27), refeita sem os EUA no mesmo dia. Formato final depende do enunciado da disciplina.

## Pergunta

O que é entregue, em que formato e como alguém de fora confere que cada número sai dos dados?

## Proposta de conteúdo (ajustar ao enunciado)

| Seção do relatório | Fonte |
|---|---|
| Introdução e pergunta (Brasil: PNS × Vigitel; Brasil frente ao mundo) | specs 001–005 |
| Estado da arte | `docs/estado-da-arte.md` |
| Dados e harmonização | spec 001, `resultados/001/` |
| Métodos — cada técnica mostrada (PCA por SVD, análise fatorial, testes de hipótese, meta-análise, regressão linear múltipla, ANOVA, teste t) | planos 002–005 |
| Resultados | `resultados/002/` a `resultados/005/`; figuras-síntese em `resultados/006/` |
| Conferência dos p-valores (Excel × fórmula × script) | `resultados/005/conferencia.csv` |
| Discussão: PNS × Vigitel, Brasil × resto do mundo, literatura | specs 003, 004 e 005 |
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
- 2026-11-27, **decisão do grupo: EUA fora do trabalho inteiro** (NHANES 2005-06, base anterior ao smartphone; decisão tomada depois de ver os resultados, registrada nas specs 001–005 e em `specs/README.md`). Na entrega:
  - `docs/modelos/relatorio.md` reescrito para o escopo sem os EUA: no Brasil, quem usa mais tela relata mais problema de sono? PNS e Vigitel concordam? Onde o Brasil fica frente ao resto do mundo e à literatura? Inclui os testes de hipótese com H0, α, estatística, p e p Holm; o teste desenhado (`resultados/006/figuras/teste_explicado.png`); a decomposição do R² (a tela explica menos que o sexo e, na PNS, menos que a idade); o confundimento por idade na PNS; Brasil × resto do mundo (exploratório) com DerSimonian-Laird e Hartung-Knapp; e a nota da retirada dos EUA. Sem Tucker (só servia para comparar com os EUA);
  - `docs/modelos/README.md` com os resultados em 1 minuto sem os EUA;
  - `analise/relatorio/numeros.py`: chaves novas `brasil_resto_*` (lidas de `resultados/004/tabelas/exploratorio_referencia.csv`), `*_decisao` das RP da 003, `h39_z`, `h39_decisao` e `fam2_rejeita`;
  - `analise/relatorio/gerar_site.py`: página nova `site/006.html` com as figuras-síntese e as tabelas de `resultados/006/`; 002 mostra o índice de insônia do Vigitel no lugar do Tucker; 003 ganha a RP bruta × ajustada; 004 ganha a tabela da meta-análise (com o resto do mundo); conferência da 005 lida pelas colunas `dentro_tolerancia` e `excecao_documentada`;
  - testes: `tests/test_verificacao_independente.py` (itens 1, 6 e 9 adaptados à PNS e à ausência de base empilhada), `tests/test_006_entrega.py` e `tests/test_006_site_design.py` (página 006, retirada dos EUA registrada, README sem NHANES nas fontes); `docs/verificacao_independente.md` com a seção "Itens superados pela retirada dos EUA (2026-11-27)";
  - slides (`docs/modelos/apresentacao.html`) e roteiro (`docs/modelos/roteiro_apresentacao.md`) refeitos em paralelo, com `tests/test_006_apresentacao.py`.
