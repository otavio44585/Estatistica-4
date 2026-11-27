# SDD — como conduzimos a análise

Spec-Driven Development adaptado a análise de dados. A especificação (pergunta, hipóteses, critérios de aceite) é a fonte de verdade; scripts, notebooks e números do relatório derivam dela. O layout segue o do GitHub Spec Kit (`specs/NNN-nome/` com `spec.md`, `plan.md`, `tasks.md`), então adotar a CLI depois não exige mover nada.

Tema: **insônia digital** — associação entre uso de telas e sono, comparando Brasil, EUA e outros países com microdados abertos e com a literatura.

## Ciclo

| Etapa | Arquivo | Responde | Quem aprova |
|---|---|---|---|
| 0. Princípios | [`constitution.md`](constitution.md) | O que vale para toda análise | Grupo |
| 1. Especificar | `specs/NNN-nome/spec.md` | Pergunta, hipóteses (H0/H1), população, critérios de aceite. Não fala de ferramenta | Grupo |
| 2. Planejar | `specs/NNN-nome/plan.md` | Dados, variáveis, modelo estatístico, ferramentas, saídas, riscos | Quem executa + 1 revisor |
| 3. Quebrar | `specs/NNN-nome/tasks.md` | Tarefas pequenas, ordenadas, cada uma com critério de pronto | Quem executa |
| 4. Executar | `analise/` | Scripts e notebooks | Revisão contra a spec |
| 5. Relatar | `resultados/` + relatório | Número com origem rastreável | Grupo |

Regras:

- `spec.md` não fala de tecnologia. `plan.md` não muda o que a spec pede; se precisar, volta-se à spec.
- **Hipótese antes do teste.** Toda spec registra H0/H1, teste e α antes da execução. O que aparecer depois é exploratório e sai rotulado assim no relatório.
- Mudança de rumo se registra na seção "Histórico" da spec, com data, antes de mexer no código.
- Tarefa concluída aponta o arquivo que prova o critério de aceite.
- Status de cada spec: `rascunho` → `aprovada` → `em execução` → `concluída`.

## Roadmap

| Spec | Pergunta | Depende de | Status |
|---|---|---|---|
| [000-levantamento](000-levantamento/spec.md) | Qual é o estado da arte e que dados abertos existem? | — | concluída (2026-11-13) |
| [001-dados-harmonizados](001-dados-harmonizados/spec.md) | Dá para medir tela e sono de forma comparável entre as bases? | 000 | executada (2026-11-27); aprovação do grupo pendente |
| [002-estrutura-latente](002-estrutura-latente/spec.md) | Que construtos os itens medem, e são os mesmos entre países? (PCA + AF) | 001 | executada (2026-11-27); aprovação do grupo pendente |
| [003-brasil-eua](003-brasil-eua/spec.md) | A associação tela × sono tem a mesma magnitude no Brasil e nos EUA? | 001, 002 | executada (2026-11-27); aprovação do grupo pendente |
| [004-comparacao-mundial](004-comparacao-mundial/spec.md) | Onde o Brasil se posiciona frente a outros países e à literatura? | 001, 002 | executada (2026-11-27); aprovação do grupo pendente |
| [005-regressao-linear](005-regressao-linear/spec.md) | Quanto o sono varia com a tela, com covariáveis fixas? (regressão linear múltipla, ANOVA, t, conferência dos p-valores) | 001, 002 | executada (2026-11-27); aprovação do grupo pendente |
| [006-entrega](006-entrega/spec.md) | Relatório, apresentação e reprodutibilidade | 002–005, enunciado | primeira versão gerada (2026-11-27); ajustar ao enunciado |

## Fluxo de dados

```text
brutos  (../pesquisa/dados — fora do git, ~1,7 GB)
   │  001: um script de harmonização por base + dicionário harmonizado (contrato)
   ▼
analise/dados/processados/<base>.parquet
   │
   ├─ 002: PCA por SVD + análise fatorial ─► escores latentes (insônia, PHQ-9, uso problemático)
   │                                            │
   ├─ 003: Brasil × EUA ◄───────────────────────┤  RP ajustada, interação país × tela
   ├─ 004: mundo ◄──────────────────────────────┤  efeito comum (r), meta-análise, Q / I², subgrupos
   └─ 005: regressão linear ◄───────────────────┘  MQO (Excel + script), ANOVA, t, conferência dos p
                 │
                 ▼
           006: relatório + apresentação
```

## Onde fica cada coisa

| Pasta | Conteúdo | No git? |
|---|---|---|
| `specs/` | Princípios e uma pasta por spec | sim |
| `docs/` | Estado da arte, inventários de papers e de dados, análise exploratória de 2026-11-27 | sim |
| `analise/` | Código (criado na execução da 001) | sim |
| `analise/dados/processados/`, `analise/dados/excel/` | Recortes harmonizados e planilhas do Excel com microdados | **não** (regenerados pelos scripts) |
| `resultados/` | Tabelas e figuras geradas pelos scripts; `RESUMO.md` por spec | sim |
| `docs/explicacoes/` | Explicação didática de cada técnica, por spec | sim |
| `docs/modelos/` | Modelos do relatório e do roteiro, com marcadores `{{chave}}` preenchidos por `analise/relatorio/relatorio.py` | sim |
| `site/` | Páginas HTML autocontidas da entrega (`analise/relatorio/gerar_site.py`) | sim |
| `data_test_sono/` | Firmware do monitor de sono, pré-existente; fora do escopo atual | sim (já estava) |
| `../pesquisa/` | PDFs dos papers e microdados brutos | **não** |

## Execução

Em 2026-11-27 as specs 001–005 foram executadas a pedido de um integrante, antes da aprovação formal do grupo (exceção ao princípio 12, registrada aqui). Cada spec tem no Histórico as decisões tomadas na execução; o grupo revisa e pode reabrir qualquer uma. Pipeline completo: `python -m analise.rodar_tudo`.
