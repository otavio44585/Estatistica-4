# Princípios

Valem para toda spec, plano e tarefa. Mudar um princípio é decisão do grupo, registrada aqui com data.

Versão 1 — rascunho de 2026-11-27, aguardando aprovação do grupo.

## Dados e fontes

1. **Só dado real com procedência documentada.** Dado sintético nunca aparece como amostra. Bases com procedência questionável (Paquistão, Bangladesh, "Sleep Patterns of College Students" — ver `docs/inventario-dados.md`) só entram em análise de sensibilidade, separadas e rotuladas.
2. **Todo número do relatório sai de um script versionado** que roda do zero a partir dos brutos. Nada digitado à mão, nada copiado de saída de console.
3. **Referência só com DOI verificado.** Nada citado de memória. Valor de referência sem fonte conferida aparece como "a verificar".
4. **Brutos e PDFs fora do git.** O repositório é público, vários PDFs são de uso pessoal e há arquivo bruto de 455 MB (o GitHub recusa acima de 100 MB). Recorte processado entra no git só se a licença da base permitir redistribuir (domínio público, CC BY 4.0), com atribuição.
5. **O dicionário da base manda.** Cada variável derivada registra código original, recodificação, tratamento de faltantes e grau de equivalência entre bases. Código especial (7, 9, 77, 99, 777, 888, 999, −999) nunca sobrevive como número.

## Estatística

6. **Hipótese antes do teste.** H0, H1, teste, α e modelo ficam registrados na spec antes da análise confirmatória. O que surgir depois é exploratório e assim rotulado. A análise exploratória de 2026-11-27 (`docs/exploratorio_*`) já foi vista: as hipóteses que nasceram dela dizem isso na spec.
7. **p-valor nunca sozinho.** Todo teste reporta estatística, graus de liberdade, p, tamanho de efeito e IC 95%. α = 0,05 bilateral. Correção de Holm dentro de cada família de hipóteses definida na spec.
8. **Desenho amostral respeitado.** Estimativa populacional de inquérito (PNS, Vigitel, NHANES, PeNSE, NSCH, YRBS, ATUS) usa peso e, quando a base tiver, estrato e UPA. Técnica que não aceita peso declara isso e ganha sensibilidade com peso.
9. **Comparação só entre medidas harmonizadas.** Quando a equivalência é aproximada (faixas diferentes, item diferente, ano diferente), a tabela de comparação diz o quê e quanto.
10. **Associação não é causalidade.** Os dados são transversais; o texto do relatório não usa "causa", "efeito de" nem "provoca" para resultados observacionais.
11. **Bruta e ajustada lado a lado.** Toda estimativa comparativa aparece sem e com o conjunto de covariáveis fixado no plano. A análise exploratória já mostrou confundimento forte por idade (PNS: RP bruta 0,90, ajustada 1,17).

## Trabalho em grupo

12. **Fluxo:** spec aprovada pelo grupo → plano → tarefas → execução. Ninguém executa spec em rascunho.
13. **Identidade e histórico:** cada integrante comita com a própria conta; commits pequenos, mensagem diz qual tarefa (`T0NN`) atende.
14. **Ambiente reproduzível:** dependências com versão fixada em `requirements.txt`; caminho dos brutos por variável de ambiente, nunca caminho pessoal no código.
15. **Teto de tempo em toda chamada externa** (download, API). Sem teto, processo pendura sem avisar.
