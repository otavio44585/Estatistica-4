# 002 — Estrutura latente: PCA e análise fatorial

Status: **concluída** (2026-11-27), aprovação do grupo pendente. Resultados em `resultados/002/RESUMO.md`.

## Perguntas

- **Q2.1** Os três sintomas de insônia formam um único construto, e esse construto é o mesmo no Brasil (Vigitel 2024) e nos EUA (NHANES 2005-06)?
- **Q2.2** O PHQ-9 tem a mesma estrutura no Brasil (PNS 2019) e nos EUA (NHANES 2005-06), e em que fator carrega o item de sono?
- **Q2.3** As escalas de uso problemático e de procrastinação do sono (SAS-SV na China, doomscrolling e procrastinação na Turquia, AIS e BPS no Japão) são unidimensionais?
- **Q2.4** PCA e análise fatorial contam a mesma história? Quanto da variância é comum e quanto é total, e os escores dos dois métodos ordenam as pessoas da mesma forma?

## Por quê

Os índices usados nos testes de hipótese (003) e na comparação mundial (004) precisam medir a mesma coisa em todas as bases. A análise fatorial verifica isso, em vez de presumir. É também onde o trabalho mostra as técnicas multivariadas pedidas.

## Hipóteses

Viabilidade já medida em 2026-11-27, com correlação de Pearson (ver `docs/` e o plano):

| # | H1 | H0 | Critério |
|---|---|---|---|
| H2.1 | Os 3 sintomas formam 1 componente/fator em cada base | mais de 1 dimensão | análise paralela retém 1; cargas ≥ 0,50 |
| H2.2 | As cargas do fator de insônia são equivalentes entre BR e EUA | estruturas diferentes | coeficiente de congruência de Tucker φ ≥ 0,95 = equivalente; 0,85–0,94 = similar (limites de Lorenzo-Seva e ten Berge, 2006, doi:10.1027/1614-2241.2.2.57 — conferidos no resumo registrado no Crossref em 2026-11-27) |
| H2.3 | O PHQ-9 tem a mesma estrutura em PNS e NHANES | estruturas diferentes | mesmo número de fatores retido; Tucker φ ≥ 0,95 |
| H2.4 | O item de sono do PHQ-9 carrega no mesmo fator nos dois países | carrega em fatores diferentes | maior carga no mesmo fator |
| H2.5 | SAS-SV, doomscrolling, AIS e BPS são unidimensionais | mais de 1 dimensão | análise paralela; a exploração prévia já viu 2 autovalores > 1 no SAS-SV de Xuzhou, no BPS do Japão e na procrastinação da Turquia |
| H2.6 | O escore do 1º componente (PCA) e o escore fatorial correlacionam r ≥ 0,95 | r < 0,95 | correlação de Pearson entre escores |

H2.5 e o fato de alguns conjuntos terem 2 autovalores > 1 vêm da análise exploratória; a decisão sobre o número de fatores segue os critérios do plano, não os autovalores sozinhos.

## Critérios de aceite

Para cada conjunto de itens:

- Descritiva por item e matriz de correlação.
- α de Cronbach e α se o item for removido; KMO global e MSA por item; teste de Bartlett.
- **PCA mostrada por decomposição em valores singulares**, com o passo a passo, e conferida com uma implementação de referência (autovalores iguais até 1e-8).
- Número de fatores decidido por três critérios (Kaiser, scree, análise paralela) e justificado.
- Análise fatorial com extração, rotação ortogonal e oblíqua, cargas, comunalidades, unicidades e correlação entre fatores.
- Comparação PCA × AF (variância total × comum, cargas, correlação dos escores).
- Coeficiente de Tucker para cada par de bases com o mesmo instrumento.
- Robustez com correlação policórica nos itens ordinais, pelo menos para os 3 sintomas e para o PHQ-9.
- Escores exportados para as specs 003 e 004.

## Fora de escopo

Análise fatorial confirmatória multigrupo (invariância métrica e escalar formal). Fica como extensão se houver tempo.

## Perguntas em aberto

1. A congruência de Tucker basta como teste de equivalência, ou o enunciado exige AFC?
2. Quais conjuntos do núcleo entram no relatório e quais ficam no apêndice?

## Histórico

- 2026-11-27: rascunho, com a viabilidade exploratória.
- 2026-11-27: executada (T020–T032). Decisões e desvios:
  - Resultado: H2.1, H2.2, H2.3, H2.4 e H2.6 atendidas; H2.5 atendida para doomscrolling e AIS, não atendida para SAS-SV, procrastinação (Turquia) e BPS (2 dimensões cada).
  - Número de fatores decidido pela análise paralela (regra do plano). Nos 7 sintomas de sono do NHANES, Kaiser daria 2 e a paralela dá 1: vale 1.
  - H2.4: além da solução retida (1 fator), rodada uma solução de 2 fatores do PHQ-9, rotulada exploratória, porque com 1 fator a pergunta "em que fator carrega o sono" é trivial.
  - H2.5 inclui a procrastinação da Turquia (UE), citada na nota da hipótese.
  - H2.6 compara o 1º componente com o escore fatorial da solução de 1 fator em todos os conjuntos, inclusive os de 2 dimensões, porque os dois escores resumem o instrumento num índice só.
  - Tucker acompanhado da maior diferença absoluta entre cargas (φ fica inflado quando todas as cargas são positivas).
  - Limite de Tucker conferido; "a verificar" retirado.
