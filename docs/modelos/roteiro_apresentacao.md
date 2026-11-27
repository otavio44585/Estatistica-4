# Roteiro da apresentação — Insônia digital

Duração-alvo: **18 minutos + 5 de perguntas**. Material de apoio: as páginas `site/*.html` (abrem no navegador, sem internet). Os números abaixo são preenchidos pelo script a partir de `resultados/`. Se algum resultado mudar, rode `python -m analise.rodar_tudo` e o roteiro se atualiza.

Quem fala em cada bloco vem de `docs/modelos/integrantes.csv` (coluna `nome`). Enquanto o grupo não preencher, aparece o papel do bloco. Basta preencher os nomes e rodar `python -m analise.relatorio.relatorio`.

| Bloco | Tempo | Quem | Tela |
|---|---|---|---|
| 1. Pergunta e por que importa | 2 min | {{apresentador_1}} | `index.html`, topo |
| 2. O que a literatura diz | 2 min | {{apresentador_1}} | `index.html`, seção 2 |
| 3. Dados e harmonização | 2 min | {{apresentador_2}} | `001.html` |
| 4. PCA e análise fatorial | 3 min | {{apresentador_2}} | `002.html` |
| 5. Brasil × EUA (testes de hipótese) | 3 min | {{apresentador_3}} | `003.html` |
| 6. Regressão, ANOVA, t e conferência dos p-valores | 3 min | {{apresentador_3}} | `005.html` |
| 7. O Brasil no mundo | 2 min | {{apresentador_4}} | `004.html` |
| 8. Conclusões e limitações | 1 min | {{apresentador_4}} | `index.html`, seções 7 e 8 |

---

## 1. Pergunta e por que importa ({{apresentador_1}}, 2 min)

**Dizer:**

- "Todo mundo já ouviu que celular à noite atrapalha o sono. Fomos ver se isso aparece nos dados brasileiros e se o tamanho é o mesmo de outros países."
- "Insônia digital não é diagnóstico. Chamamos assim os problemas de sono associados ao uso de telas."
- "A pergunta tem três partes:
  - quem usa mais tela relata mais problema de sono?
  - o tamanho disso é igual no Brasil e nos EUA?
  - onde o Brasil fica frente a outros países e à literatura?"

**Mostrar:** o resumo no topo da `index.html`.

## 2. O que a literatura diz ({{apresentador_1}}, 2 min)

**Dizer:**

- "A associação é consistente: em 67 estudos, 90% acharam associação adversa (Hale e Guan, 2015)."
- "O efeito é pequeno: de 3 a 8 minutos de sono a menos por hora de tela (Przybylski, 2019)."
- "Pesa mais quando e como se usa: tela na cama e uso problemático se associam mais que o tempo total (Levenson, 2017; Hjetland, 2025; Han, Zhou e Liu, 2024)."
- "A relação vai nos dois sentidos: quem dorme mal também pega o celular (Bauducco, 2024)."

**Transição:** "Com isso em mente, fomos aos microdados."

## 3. Dados e harmonização ({{apresentador_2}}, 2 min)

**Dizer:**

- "Usamos {{n_total}} pessoas de sete bases abertas.
  - No Brasil: PNS 2019 ({{n_pns2019}} adultos) e Vigitel 2024 ({{n_vigitel2024}}).
  - Nos EUA: NHANES 2005-06 ({{n_nhanes0506}}).
  - E quatro amostras de China, Argentina, Turquia e Japão."
- "Cada pesquisa pergunta de um jeito. Harmonizar é criar as mesmas variáveis em todas:
  - 'não sabe' virou faltante;
  - as horas de tela foram cortadas em 1 h e 3 h;
  - cada variável ganhou uma nota de equivalência entre as bases."
- "No Brasil, {{tela3h_pns2019}} dos adultos (PNS) usam tela digital 3 h ou mais por dia no lazer; no Vigitel, {{tela3h_vigitel2024}}. No NHANES de 2005, antes do smartphone, eram {{tela3h_nhanes0506}}."

**Mostrar:** a figura de exposição em `001.html`.

**Atenção:** dizer já aqui que o NHANES é de 2005; isso volta nas limitações.

## 4. PCA e análise fatorial ({{apresentador_2}}, 3 min)

**Dizer:**

- "Antes de comparar países, precisamos saber se o índice de insônia mede a mesma coisa nos dois."
- "Os 3 sintomas são: dificuldade para adormecer, para voltar a dormir e acordar cedo demais."
- "A PCA, feita pela decomposição em valores singulares, mostra uma dimensão só. O primeiro componente explica {{var_pc1_insonia3_vigitel}} da variância no Vigitel e {{var_pc1_insonia3_nhanes}} no NHANES."
- "Três critérios dizem quantos fatores ficar: autovalor > 1, gráfico scree e análise paralela. Os três dão 1."
- "A análise fatorial separa a parte comum dos itens. O coeficiente de Tucker compara as cargas dos dois países: {{tucker_insonia}}. Acima de 0,95 as estruturas são consideradas equivalentes."
- "Conclusão: dá para comparar o índice entre os dois países, e a soma simples dos 3 itens serve (correlação {{r_soma_pc1_insonia3_vigitel}} com o componente)."

**Mostrar:** o gráfico de cargas Brasil × EUA em `002.html`.

**Se perguntarem** "por que PCA e análise fatorial?": a PCA resume a variância total; a análise fatorial modela só a variância comum. Aqui as duas contam a mesma história (escores correlacionam de {{r_pc1_af_min}} a {{r_pc1_af_max}}).

## 5. Brasil × EUA ({{apresentador_3}}, 3 min)

**Dizer:**

- "Comparamos quem usa tela 3 h ou mais com quem usa menos de 1 h, ajustando por idade, sexo e escolaridade."
- "A medida é a razão de prevalências. Com tela digital:
  - Vigitel {{rp_digital_vigitel2024}} ({{rp_digital_vigitel2024_ic}});
  - PNS {{rp_digital_pns2019}};
  - NHANES {{rp_digital_nhanes0506}}.
  Nos três, rejeitamos H0 de RP = 1, já com a correção de Holm."
- "Cuidado com o NHANES: o desenho tem só {{nhanes_estratos}} estratos. Com uma regra mais conservadora de graus de liberdade, a do `svyglm` do R, o p Holm vai a {{h33_pholm_svyglm}}. Por isso dizemos que, nos EUA, a evidência é mais fraca."
- "Brasil e EUA são diferentes? A razão entre as duas RP é {{h36_razao}}, com intervalo de {{h36_ic}}, que contém o 1. Não detectamos diferença, o que não prova que sejam iguais: o intervalo é largo."
- **Ponto forte da fala:** "Sem ajuste, a PNS mostra o contrário: RP de {{rp_bruta_digital_pns2019}}, como se tela protegesse. É confundimento por idade: jovens usam mais tela e relatam menos problema de sono. Ajustada, vai a {{rp_ajustada_digital_pns2019}}."

**Mostrar:** `rp_por_pais.png` em `003.html`.

**Se perguntarem** "por que peso amostral?": cada entrevistado representa um número diferente de pessoas. Sem peso e sem estrato e UPA, o p-valor sai pequeno demais.

## 6. Regressão, ANOVA, t e conferência dos p-valores ({{apresentador_3}}, 3 min)

**Dizer:**

- "Fizemos a regressão linear múltipla no formato da aula: SUMMARY OUTPUT do Excel, ANOVA, t de cada coeficiente, IC 95% e dummies."
- "No Vigitel, quem usa 3 h ou mais tem índice de insônia {{H51_b}} ponto maior, numa escala de 0 a 12 (p Holm {{H51_pholm}})."
- "É significativo, mas pequeno: a tela acrescenta {{H51_dr2_pct}} ao R²."
- "No NHANES, sem peso o p seria {{H52_p_sempeso}}. Com o desenho amostral, vai a {{H52_p}} e não rejeitamos H0. O peso muda a conclusão."
- "A ANOVA de um fator do Excel no Vigitel (F = {{H57_f_sempeso}}) dá exatamente o mesmo F que a regressão nas dummies de tela, sem covariáveis. É a mesma conta vista de dois jeitos. A decisão usa a versão com peso amostral (F de Wald = {{H57_est}})."
- "Conferimos cada p-valor de três formas:
  - a ferramenta Análise de Dados do Excel;
  - a fórmula `T.DIST.2T` na planilha;
  - o script em Python.
  Foram {{conf_n}} números: {{conf_dentro}} dentro da tolerância e {{conf_excecoes}} exceções documentadas, porque o Excel arredonda o grau de liberdade do teste de Welch."

**Mostrar:** a tabela de hipóteses e a figura de efeitos em `005.html`. Se der tempo, a aba do SUMMARY OUTPUT de uma base.

**Se perguntarem** "por que o resultado da Argentina tem sinal contrário?": é frágil. Some quando a série escolar substitui a idade (p = {{H54_p_serie}}), e são adolescentes com outra medida de tela.

## 7. O Brasil no mundo ({{apresentador_4}}, 2 min)

**Dizer:**

- "Para pôr bases com escalas diferentes no mesmo gráfico, usamos a correlação de Spearman e uma meta-análise de efeitos aleatórios."
- "O efeito varia muito entre as bases: I² = {{meta_I2}}."
- "Com tempo total de tela, a correlação combinada é {{meta_rho_total}}. Bem abaixo dos 0,28 da meta-análise de referência."
- "Uso problemático ({{meta_rho_problematico}}) e celular antes de dormir ({{meta_rho_presono}}) se associam mais, como diz a literatura. Mas com uma ou duas bases por grupo, o teste não confirma a diferença (p Holm {{H42_pholm}})."
- "Entre o Brasil ({{meta_rho_brasil}}) e os outros países com tempo total, não detectamos diferença (p Holm {{H43_pholm}})."

**Mostrar:** `floresta.png` em `004.html`.

## 8. Conclusões e limitações ({{apresentador_4}}, 1 min)

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
| p < 0,001 em quase tudo não é suspeito? | Com {{n_vigitel2024}} a {{n_pns2019}} pessoas, qualquer diferença pequena fica significativa. Por isso mostramos tamanho de efeito e IC, não só p |
| Por que Holm e não Bonferroni? | Holm mantém a chance de pelo menos um falso positivo na família em no máximo 5%, como Bonferroni, mas rejeita mais |
| Por que a RP e não o odds ratio? | O desfecho é comum ({{prev_adormecer_nhanes0506}} a {{prev_adormecer_vigitel2024}}). Nesse caso o OR exagera a associação, e a RP se lê direto como "quantas vezes mais" |
| Tela causa insônia? | Os dados não permitem dizer. São transversais, e a literatura mostra também o caminho inverso |
| Os resultados do Excel batem com os do Python? | Sim. A ferramenta do Excel foi executada de verdade e comparada número a número: {{conf_dentro}} de {{conf_n}} dentro da tolerância. As {{conf_excecoes}} exceções vêm do Excel arredondar o grau de liberdade de Welch |
| Por que o NHANES de 2005 e não um mais recente? | É o único ciclo do NHANES com os mesmos 3 sintomas de insônia do Vigitel e com latência em minutos. Os ciclos recentes só têm horas de sono |
