# Insônia digital — Estatística 4 (ESEG)

Associação entre uso de telas e sono em adultos no Brasil, nos EUA e em outros quatro países, com microdados abertos e comparação com a literatura.

**Comece pelas páginas:** [`site/index.html`](site/index.html) (visão geral, conclusões) e [`site/roteiro.html`](site/roteiro.html) (roteiro da apresentação). São arquivos HTML autocontidos: abrem direto no navegador, sem internet.

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `specs/` | Planejamento por SDD: princípios (`constitution.md`) e uma pasta por etapa com especificação, plano e tarefas. Começar por [`specs/README.md`](specs/README.md) |
| `analise/` | Código: harmonização das bases (`harmonizacao/`), PCA e análise fatorial (`multivariada/`), Brasil × EUA (`brasil_eua/`), comparação mundial (`mundial/`), regressão linear (`regressao/`), relatório e páginas (`relatorio/`) |
| `analise/notebooks/` | Um notebook por etapa, já executado, com a narrativa de cada técnica |
| `resultados/` | Tabelas (CSV com `;` e vírgula decimal) e figuras geradas pelos scripts; `RESUMO.md` por etapa |
| `docs/` | Estado da arte, inventários, explicações didáticas (`docs/explicacoes/`), relatório e roteiro |
| `site/` | Páginas HTML da entrega, geradas por `analise/relatorio/gerar_site.py` |
| `tests/` | Testes automáticos (`python -m pytest`) |
| `data_test_sono/` | Firmware do monitor de sono, pré-existente; fora do escopo desta análise |

## Como reproduzir

Os microdados brutos não ficam no repositório (público; licença do Vigitel não declarada; arquivo da PNS de 455 MB). Baixe as bases listadas em [`docs/inventario-dados.md`](docs/inventario-dados.md) numa pasta e aponte a variável `STAT4_BRUTOS` para ela.

```bash
pip install -r requirements.txt
export STAT4_BRUTOS=/caminho/para/pesquisa/dados   # PowerShell: $env:STAT4_BRUTOS = "..."
python -m analise.rodar_tudo                       # harmoniza, analisa, gera notebooks, relatório e páginas
python -m pytest
```

Sem os microdados, os testes que dependem dos dados processados aparecem como `skipped` (não como aprovados); só os testes de código rodam. A automação do Excel (`analise.regressao.roda_excel`) exige Windows com Excel; em outra máquina use `python -m analise.rodar_tudo --sem-excel`, e a conferência lê as saídas já exportadas em `resultados/005/excel_saidas/`.

Todo resultado próprio do relatório sai de um arquivo em `resultados/`, gerado por script. Os p-valores da regressão são conferidos de três formas: saída do Excel, fórmula no Excel e script (`resultados/005/conferencia.csv`).

## Princípios (resumo)

Só dado real com procedência; hipótese registrada antes do teste; p-valor sempre com tamanho de efeito e IC 95%; correção de Holm por família; peso amostral nos inquéritos; associação não é causalidade. Texto completo em [`specs/constitution.md`](specs/constitution.md).
