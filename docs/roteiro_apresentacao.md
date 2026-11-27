<!-- Arquivo GERADO por analise/relatorio/relatorio.py a partir de docs/modelos/roteiro_apresentacao.md. Edite o modelo, não este arquivo. -->

# Roteiro da apresentação — Insônia digital

Duração-alvo: **18 minutos + 5 de perguntas**. Material de apoio: as páginas `site/*.html` (abrem no navegador, sem internet). Os números abaixo são preenchidos pelo script a partir de `resultados/`. Se algum resultado mudar, rode `python -m analise.rodar_tudo` e o roteiro se atualiza.

Quem fala em cada bloco vem de `docs/modelos/integrantes.csv` (coluna `nome`). Enquanto o grupo não preencher, aparece o papel do bloco. Basta preencher os nomes e rodar `python -m analise.relatorio.relatorio`.

| Bloco | Tempo | Quem | Tela |
|---|---|---|---|
| 1. Pergunta e por que importa | 2 min | Apresentação da pergunta e da literatura | `index.html`, topo |
| 2. O que a literatura diz | 2 min | Apresentação da pergunta e da literatura | `index.html`, seção 2 |
| 3. Dados e harmonização | 2 min | Apresentação dos dados, da PCA e da análise fatorial | `001.html` |
| 4. PCA e análise fatorial | 3 min | Apresentação dos dados, da PCA e da análise fatorial | `002.html` |
| 5. Brasil × EUA (testes de hipótese) | 3 min | Apresentação dos testes de hipótese e da regressão | `003.html` |
| 6. Regressão, ANOVA, t e conferência dos p-valores | 3 min | Apresentação dos testes de hipótese e da regressão | `005.html` |
| 7. O Brasil no mundo | 2 min | Apresentação da comparação mundial e das conclusões | `004.html` |
| 8. Conclusões e limitações | 1 min | Apresentação da comparação mundial e das conclusões | `index.html`, seções 7 e 8 |

---

## 1. Pergunta e por que importa (Apresentação da pergunta e da literatura, 2 min)

**Dizer:**

- "Todo mundo já ouviu que celular à noite atrapalha o sono. Fomos ver se isso aparece nos dados brasileiros e se o tamanho é o mesmo de outros países."
- "Insônia digital não é diagnóstico. Chamamos assim os problemas de sono associados ao uso de telas."
- "A pergunta tem três partes:
  - quem usa mais tela relata mais problema de sono?
  - o tamanho disso é igual no Brasil e nos EUA?
  - onde o Brasil fica frente a outros países e à literatura?"

**Mostrar:** o resumo no topo da `index.html`.

## 2. O que a literatura diz (Apresentação da pergunta e da literatura, 2 min)

**Dizer:**

- "A associação é consistente: em 67 estudos, 90% acharam associação adversa (Hale e Guan, 2015)."
- "O efeito é pequeno: de 3 a 8 minutos de sono a menos por hora de tela (Przybylski, 2019)."
- "Pesa mais quando e como se usa: tela na cama e uso problemático se associam mais que o tempo total (Levenson, 2017; Hjetland, 2025; Han, Zhou e Liu, 2024)."
- "A relação vai nos dois sentidos: quem dorme mal também pega o celular (Bauducco, 2024)."

**Transição:** "Com isso em mente, fomos aos microdados."

## 3. Dados e harmonização (Apresentação dos dados, da PCA e da análise fatorial, 2 min)

**Dizer:**

- "Usamos 125.920 pessoas de sete bases abertas.
  - No Brasil: PNS 2019 (88.531 adultos) e Vigitel 2024 (27.048).
  - Nos EUA: NHANES 2005-06 (5.563).
  - E quatro amostras de China, Argentina, Turquia e Japão."
- "Cada pesquisa pergunta de um jeito. Harmonizar é criar as mesmas variáveis em todas:
  - 'não sabe' virou faltante;
  - as horas de tela foram cortadas em 1 h e 3 h;
  - cada variável ganhou uma nota de equivalência entre as bases."
- "No Brasil, 22% dos adultos (PNS) usam tela digital 3 h ou mais por dia no lazer; no Vigitel, 27%. No NHANES de 2005, antes do smartphone, eram 7%."

**Mostrar:** a figura de exposição em `001.html`.

**Atenção:** dizer já aqui que o NHANES é de 2005; isso volta nas limitações.

## 4. PCA e análise fatorial (Apresentação dos dados, da PCA e da análise fatorial, 3 min)

**Dizer:**

- "Antes de comparar países, precisamos saber se o índice de insônia mede a mesma coisa nos dois."
- "Os 3 sintomas são: dificuldade para adormecer, para voltar a dormir e acordar cedo demais."
- "A PCA, feita pela decomposição em valores singulares, mostra uma dimensão só. O primeiro componente explica 75% da variância no Vigitel e 71% no NHANES."
- "Três critérios dizem quantos fatores ficar: autovalor > 1, gráfico scree e análise paralela. Os três dão 1."
- "A análise fatorial separa a parte comum dos itens. O coeficiente de Tucker compara as cargas dos dois países: 0,998. Acima de 0,95 as estruturas são consideradas equivalentes."
- "Conclusão: dá para comparar o índice entre os dois países, e a soma simples dos 3 itens serve (correlação 0,9998 com o componente)."

**Mostrar:** o gráfico de cargas Brasil × EUA em `002.html`.

**Se perguntarem** "por que PCA e análise fatorial?": a PCA resume a variância total; a análise fatorial modela só a variância comum. Aqui as duas contam a mesma história (escores correlacionam de 0,953 a 0,999).

## 5. Brasil × EUA (Apresentação dos testes de hipótese e da regressão, 3 min)

**Dizer:**

- "Comparamos quem usa tela 3 h ou mais com quem usa menos de 1 h, ajustando por idade, sexo e escolaridade."
- "A medida é a razão de prevalências. Com tela digital:
  - Vigitel 1,32 (1,17 a 1,48);
  - PNS 1,19;
  - NHANES 1,41.
  Nos três, rejeitamos H0 de RP = 1, já com a correção de Holm."
- "Cuidado com o NHANES: o desenho tem só 15 estratos. Com uma regra mais conservadora de graus de liberdade, a do `svyglm` do R, o p Holm vai a 0,061. Por isso dizemos que, nos EUA, a evidência é mais fraca."
- "Brasil e EUA são diferentes? A razão entre as duas RP é 1,07, com intervalo de 0,80 a 1,44, que contém o 1. Não detectamos diferença, o que não prova que sejam iguais: o intervalo é largo."
- **Ponto forte da fala:** "Sem ajuste, a PNS mostra o contrário: RP de 0,85, como se tela protegesse. É confundimento por idade: jovens usam mais tela e relatam menos problema de sono. Ajustada, vai a 1,19."

**Mostrar:** `rp_por_pais.png` em `003.html`.

**Se perguntarem** "por que peso amostral?": cada entrevistado representa um número diferente de pessoas. Sem peso e sem estrato e UPA, o p-valor sai pequeno demais.

## 6. Regressão, ANOVA, t e conferência dos p-valores (Apresentação dos testes de hipótese e da regressão, 3 min)

**Dizer:**

- "Fizemos a regressão linear múltipla no formato da aula: SUMMARY OUTPUT do Excel, ANOVA, t de cada coeficiente, IC 95% e dummies."
- "No Vigitel, quem usa 3 h ou mais tem índice de insônia 0,59 ponto maior, numa escala de 0 a 12 (p Holm < 0,001)."
- "É significativo, mas pequeno: a tela acrescenta 0,4% ao R²."
- "No NHANES, sem peso o p seria < 0,001. Com o desenho amostral, vai a 0,145 e não rejeitamos H0. O peso muda a conclusão."
- "A ANOVA de um fator do Excel no Vigitel (F = 34,91) dá exatamente o mesmo F que a regressão nas dummies de tela, sem covariáveis. É a mesma conta vista de dois jeitos. A decisão usa a versão com peso amostral (F de Wald = 9,61)."
- "Conferimos cada p-valor de três formas:
  - a ferramenta Análise de Dados do Excel;
  - a fórmula `T.DIST.2T` na planilha;
  - o script em Python.
  Foram 922 números: 920 dentro da tolerância e 2 exceções documentadas, porque o Excel arredonda o grau de liberdade do teste de Welch."

**Mostrar:** a tabela de hipóteses e a figura de efeitos em `005.html`. Se der tempo, a aba do SUMMARY OUTPUT de uma base.

**Se perguntarem** "por que o resultado da Argentina tem sinal contrário?": é frágil. Some quando a série escolar substitui a idade (p = 0,093), e são adolescentes com outra medida de tela.

## 7. O Brasil no mundo (Apresentação da comparação mundial e das conclusões, 2 min)

**Dizer:**

- "Para pôr bases com escalas diferentes no mesmo gráfico, usamos a correlação de Spearman e uma meta-análise de efeitos aleatórios."
- "O efeito varia muito entre as bases: I² = 98,4%."
- "Com tempo total de tela, a correlação combinada é 0,022. Bem abaixo dos 0,28 da meta-análise de referência."
- "Uso problemático (0,178) e celular antes de dormir (0,145) se associam mais, como diz a literatura. Mas com uma ou duas bases por grupo, o teste não confirma a diferença (p Holm 0,216)."
- "Entre o Brasil (0,016) e os outros países com tempo total, não detectamos diferença (p Holm 1,000)."

**Mostrar:** `floresta.png` em `004.html`.

## 8. Conclusões e limitações (Apresentação da comparação mundial e das conclusões, 1 min)

**Dizer:**

1. "Mais tela, mais problema de sono no Brasil, de forma consistente, mas com associação pequena."
2. "Não detectamos diferença entre Brasil e EUA, mas o intervalo é largo."
3. "Como e quando se usa parece importar mais do que quanto."
4. "Os dados são transversais: é associação, não causa."
5. "Principais limitações: NHANES de 2005, autorrelato e itens diferentes na PNS."

**Fechar:** "Todo número que mostramos sai de um script, e qualquer pessoa pode rodar tudo de novo a partir do repositório."

---

## Perguntas prováveis

| Pergunta | Resposta curta |
|---|---|
| Por que não usaram só uma base? | Uma base responde se há associação; a pergunta era comparar países. Para isso, as medidas precisam ser equivalentes, o que a etapa 002 testou |
| p < 0,001 em quase tudo não é suspeito? | Com 27.048 a 88.531 pessoas, qualquer diferença pequena fica significativa. Por isso mostramos tamanho de efeito e IC, não só p |
| Por que Holm e não Bonferroni? | Holm mantém a chance de pelo menos um falso positivo na família em no máximo 5%, como Bonferroni, mas rejeita mais |
| Por que a RP e não o odds ratio? | O desfecho é comum (16% a 22%). Nesse caso o OR exagera a associação, e a RP se lê direto como "quantas vezes mais" |
| Tela causa insônia? | Os dados não permitem dizer. São transversais, e a literatura mostra também o caminho inverso |
| Os resultados do Excel batem com os do Python? | Sim. A ferramenta do Excel foi executada de verdade e comparada número a número: 920 de 922 dentro da tolerância. As 2 exceções vêm do Excel arredondar o grau de liberdade de Welch |
| Por que o NHANES de 2005 e não um mais recente? | É o único ciclo do NHANES com os mesmos 3 sintomas de insônia do Vigitel e com latência em minutos. Os ciclos recentes só têm horas de sono |
