# Roteiro da apresentação — Insônia digital

Duração-alvo: **19 minutos + 5 de perguntas**, em 18 slides. Os slides são `site/apresentacao.html` (abre no navegador, sem internet): setas para navegar, **F** tela cheia, **N** mostra estas falas embaixo do slide, **T** zera o relógio. As falas abaixo são as mesmas das notas do apresentador. Os números são preenchidos pelo script a partir de `resultados/`; se algum resultado mudar, rode `python -m analise.rodar_tudo` e o roteiro e os slides se atualizam juntos.

Quem fala em cada bloco vem de `docs/modelos/integrantes.csv` (coluna `nome`). Enquanto o grupo não preencher, aparece o papel do bloco. Basta preencher os nomes e rodar `python -m analise.relatorio.relatorio`.

| Bloco | Slides | Tempo | Quem |
|---|---|---|---|
| 1. Pergunta e literatura | 1 a 3 | 3 min | {{apresentador_1}} |
| 2. Dados, normalização e PCA | 4 a 6 | 4 min | {{apresentador_2}} |
| 3. Testes de hipótese e regressão | 7 a 12 | 6 min | {{apresentador_3}} |
| 4. Brasil no mundo, limitações e conclusões | 13 a 18 | 6 min | {{apresentador_4}} |

Regras de linguagem para todos: falar em **associação**, nunca em causalidade; quando um teste não rejeita H0, dizer **"não foi detectada diferença"**, não "são iguais".

---

## 1. Pergunta e literatura ({{apresentador_1}}, 3 min)

**Slide 1 — Capa**

- Apresentar o grupo e o tema.
- "Todo mundo já ouviu que celular à noite atrapalha o sono. Fomos ver se isso aparece nos dados brasileiros e como o Brasil se compara com pesquisas de outros países."

**Slide 2 — Três perguntas sobre tela e sono, com o Brasil no centro**

- "Nossa pergunta tem três partes."
- "Primeira: quem usa mais tela no lazer relata mais problema de sono?"
- "Segunda: isso aparece nas duas pesquisas nacionais do Brasil, a PNS 2019, feita em todo o país, e o Vigitel 2024, feito nas 27 capitais? E com o mesmo tamanho?"
- "Terceira: como os estudos brasileiros se comparam com o resto do mundo, com pesquisas da China, da Argentina, da Turquia e do Japão?"

**Slide 3 — A literatura descreve uma associação consistente**

- "A literatura descreve uma associação consistente: 90% dos 67 estudos com crianças e adolescentes acharam associação entre tela e sono (Hale e Guan, 2015)."
- "Na maior parte, ela é pequena: em média, o sono cai de 3 a 8 minutos por hora de tela (Przybylski, 2019)."
- "Pesa mais como e quando se usa. Como: o uso problemático, compulsivo, tem correlação de 0,33 com problemas de sono, contra 0,28 do uso geral, numa escala de 0 a 1 (Han, Zhou e Liu, 2024). Quando: cada hora de tela já deitado na cama se associa a uma chance 59% maior de sintomas de insônia (Hjetland et al., 2025)."
- "E a relação pode ser de mão dupla: quem dorme mal usa mais o celular para tentar pegar no sono, ou não pega no sono porque usa mais o celular (Bauducco et al., 2024)."

**Transição:** "Com isso em mente, fomos aos dados."

## 2. Dados, normalização e PCA ({{apresentador_2}}, 4 min)

**Slide 4 — {{n_total}} pessoas em seis pesquisas: {{pct_n_brasil}} delas no Brasil**

- "Juntamos {{n_total}} pessoas de seis pesquisas com dados abertos."
- "O Brasil é quase tudo: {{n_brasil}} pessoas, {{pct_n_brasil}} do total, nas duas pesquisas nacionais. A PNS 2019, com {{n_pns2019}} pessoas de todo o país, e o Vigitel 2024, com {{n_vigitel2024}} pessoas das 27 capitais."
- "Depois vem a Argentina, com {{n_argentina_reg}} pessoas, e o resto do mundo, com {{n_resto3}}: China ({{n_xuzhou}}), Turquia ({{n_turquia}}) e Japão ({{n_japao}})."

**Slide 5 — Normalização da base**

- "Antes de comparar, normalizamos a base. Primeiro, retiramos as respostas 'não sabe', 'recusou' e os dados faltantes."
- "Segundo, juntamos as faixas de tempo de tela em três: menos de 1 hora, de 1 a 3 horas e 3 horas ou mais. Por exemplo, na PNS, '1 a menos de 2 horas' e '2 a menos de 3 horas' viraram '1 a 3 horas'."
- "Terceiro, cada variável ganhou um grau de equivalência entre as bases: equivalente, aproximada ou não comparável. Onde as escalas não são comparáveis, comparamos por correlação, que não depende da unidade."

**Slide 6 — No Vigitel, as três perguntas de insônia formam um único fator**

- "No Vigitel, o sono é medido por três perguntas: dificuldade para adormecer; acordar e ter dificuldade de voltar a dormir; e acordar antes da hora e não voltar a dormir."
- "A PCA mostra que as três medem uma coisa só: um fator, que explica {{var_pc1_insonia3_vigitel}} da variância. As cargas são altas: {{vig_item1_carga_pc1}}, {{vig_item2_carga_pc1}} e {{vig_item3_carga_pc1}}."
- "Três critérios dizem quantos fatores ficar: autovalor maior que 1, gráfico scree e análise paralela. Os três dão {{fatores_insonia3_vigitel}}."
- "O alfa de Cronbach, {{alfa_insonia3_vigitel}}, mede se as perguntas andam juntas. O KMO, {{kmo_insonia3_vigitel}}, mede se as correlações entre elas bastam para resumir em fatores. Os dois vão de 0 a 1."
- "Por isso somamos as três respostas num índice de insônia de 0 a 12. A soma simples praticamente coincide com o componente (r = {{r_soma_pc1_insonia3_vigitel}})."

**Se perguntarem** "por que PCA e análise fatorial?": a PCA resume a variância total; a análise fatorial modela só a parte comum dos itens. Aqui as duas contam a mesma história (escores com r = {{r_pc1_af_insonia3_vigitel}}).

## 3. Testes de hipótese e regressão ({{apresentador_3}}, 6 min)

**Slide 7 — Como lemos um teste de hipótese (curva normal)**

- "Antes dos resultados, como lemos um teste de hipótese. A hipótese nula, H0, diz que não há associação: a razão de prevalências é 1."
- "Se H0 fosse verdade, a estatística do teste seguiria esta curva normal, quase sempre perto de zero."
- "Com α = 0,05 bilateral, as caudas em âmbar, 2,5% de cada lado, além de mais ou menos 1,96, são a região de rejeição."
- "No Vigitel, a estatística observada foi z = {{rp_digital_vigitel2024_est}}, bem dentro da cauda direita. O p-valor é {{rp_digital_vigitel2024_p}}: rejeitamos H0."
- "Como fazemos vários testes, corrigimos os p-valores por Holm, que mantém em no máximo 5% a chance de algum falso positivo na família."

**Slide 8 — Tela digital 3 h ou mais se associa a mais problema de sono nas duas pesquisas brasileiras**

- "O resultado principal: comparamos quem usa tela digital 3 h ou mais com quem usa menos de 1 h, ajustando por idade, sexo e escolaridade."
- "A medida é a razão de prevalências. No Vigitel, {{rp_digital_vigitel2024}} ({{rp_digital_vigitel2024_ic}}); na PNS, {{rp_digital_pns2019}} ({{rp_digital_pns2019_ic}}). Ou seja, problema de sono de {{rp_br_pct_min}} a {{rp_br_pct_max}} mais frequente no grupo de mais tela. Nas duas, rejeitamos H0, já com Holm."
- "As duas pesquisas dão o mesmo tamanho? A razão entre as RP é {{h39_razao}}, com intervalo de {{h39_ic}}, que contém o 1 (p Holm {{h39_pholm}}). Não foi detectada diferença; lembrando que as perguntas de sono das duas são diferentes."

**Se perguntarem** "por que peso amostral?": cada entrevistado representa um número diferente de pessoas. Sem peso e sem o desenho da amostra, o p-valor sai pequeno demais.

**Slide 9 — Regressão no Vigitel**

- "Também fizemos a regressão linear múltipla no formato da aula: SUMMARY OUTPUT do Excel, ANOVA, t de cada coeficiente, IC 95% e dummies."
- "No Vigitel, quem usa 3 h ou mais tem índice de insônia {{H51_b}} ponto maior, numa escala de 0 a 12 (t = {{H51_est}}, p Holm {{H51_pholm}})."
- "É significativo, mas pequeno: a tela acrescenta {{H51_dr2_pct}} ao R²."
- "No gráfico, a mesma associação em desvios-padrão nas outras pesquisas: positiva na China, na Turquia e no Japão; na Argentina, o sinal é contrário."

**Se perguntarem** "por que a Argentina tem sinal contrário?": é frágil. Some quando a série escolar substitui a idade (p = {{H54_p_serie}}), e a medida de tela é outra.

**Slide 10 — ANOVA e teste t no Vigitel**

- "Com médias: o índice de insônia fica parecido entre menos de 1 h e 1 a 3 h, e sobe na faixa de 3 h ou mais."
- "A ANOVA de um fator do Excel no Vigitel (F = {{H57_f_sempeso}}) dá exatamente o mesmo F que a regressão nas dummies de tela, sem covariáveis. É a mesma conta vista de dois jeitos. A decisão usa a versão com peso amostral (F de Wald = {{H57_est}}, p Holm {{H57_pholm}})."
- "O teste t de Welch compara só os extremos, 3 h ou mais contra menos de 1 h: t = {{H59_est}}, p Holm {{H59_pholm}}. A diferença é pequena: d de Cohen = {{H59_efeito}}."

**Slide 11 — Todos os testes t e z, cada um na sua curva**

- "Aqui estão todos os testes t e z, cada um na sua curva. O âmbar é a região de rejeição; a seta é o valor observado."
- "Quase todos caem fora da faixa central. A exceção é a comparação entre PNS e Vigitel, H3.9, que fica no centro: não foi detectada diferença entre as duas pesquisas."
- "Na Argentina, H5.4, a estatística cai na cauda esquerda: associação no sentido contrário, e frágil."

**Slide 12 — Tabela dos testes com as pesquisas brasileiras**

- "Esta tabela resume os testes feitos com as duas pesquisas brasileiras."
- "Os testes de associação rejeitam H0: razão de prevalências na PNS e no Vigitel, tendência por faixa de tela, regressão, ANOVA e teste t."
- "Os testes de diferença não rejeitam: não foi detectada variação por faixa etária, entre TV e tela digital, nem entre PNS e Vigitel."
- "Com dezenas de milhares de pessoas, até diferenças pequenas ficam significativas. Por isso olhamos também o tamanho, como fizemos com o R² e o d de Cohen."

## 4. Brasil no mundo, limitações e conclusões ({{apresentador_4}}, 6 min)

**Slide 13 — O Brasil no mundo**

- "Agora, o Brasil no mundo. Como cada pesquisa mede tela e sono de um jeito, usamos a correlação de Spearman, que vai de −1 a +1."
- "Em âmbar, o Brasil: PNS {{rho_pns2019}} e Vigitel {{rho_vigitel2024}}. Em azul-escuro, as outras pesquisas."
- "O experimento foi combinar as pesquisas de cada lado numa média ponderada pela precisão, a meta-análise. Brasil combinado: {{meta_rho_brasil}}. Resto do mundo combinado: {{meta_rho_resto}}. Os intervalos se sobrepõem."
- "A correlação é pequena em todas: ela pode ir até +1, e o máximo aqui é {{rho_max}}, na China, com uso problemático do celular."

**Se perguntarem** "por que a PNS dá negativo?": é a idade. Quem usa mais tela é mais jovem, e os jovens relatam menos problema de sono. Ajustada por idade, a correlação da PNS vai a {{rho_aj_pns2019}}.

**Slide 14 — Tabela dos testes com as outras pesquisas e a combinação**

- "Os testes com as outras pesquisas: na China, na Turquia e no Japão, a associação é positiva e rejeitamos H0. Na Argentina, o sinal é contrário."
- "Na combinação, a associação varia muito entre as pesquisas (H4.1, I² = {{meta_I2}}). Não foi detectada diferença entre os tipos de uso (H4.2), nem entre o Brasil e a Argentina, o único outro país com tempo total de tela (H4.3)."
- "E o tempo total de tela combinado, {{meta_rho_total}}, fica abaixo do valor da literatura: o teste de equivalência não rejeita H0 (H4.4)."

**Slide 15 — Limitações: associação não é causalidade**

- "A principal limitação: associação não é causalidade. Os dados são transversais, tudo medido ao mesmo tempo, então não dá para separar a direção: se a tela vem antes do sono ruim, ou se quem dorme mal usa mais tela."
- "Autorrelato: a própria pessoa informa as horas de tela, em faixas, e como dorme."
- "E não dá para separar a tela da pessoa. Na PNS, quem usa mais tela é mais jovem, e os jovens relatam menos problema de sono. Sem ajuste, a RP é {{rp_bruta_digital_pns2019}}, como se mais tela viesse com menos problema de sono. Ajustada por idade, sexo e escolaridade, vai a {{rp_ajustada_digital_pns2019}}. E pode haver outros fatores que não medimos."
- "Por fim, as perguntas de sono e as amostras não são as mesmas em todas as pesquisas."

**Slide 16 — A tela explica pouco do sono**

- "Quanto a tela explica do sono? Separamos o quanto cada fator explica sozinho na regressão: tela, idade, sexo e escolaridade."
- "A tela explica pouco: {{r2u_vigitel2024_tela}} da variação do sono no Vigitel e {{r2u_pns2019_tela}} na PNS. Menos que o sexo ({{r2u_vigitel2024_sexo}} e {{r2u_pns2019_sexo}}) e, na PNS, menos que a idade ({{r2u_pns2019_idade}})."
- "Os quatro fatores juntos explicam {{r2c_vigitel2024}} no Vigitel e {{r2c_pns2019}} na PNS. A associação existe, mas o sono depende sobretudo de outras coisas."

**Slide 17 — Conclusões**

1. "Nas duas pesquisas brasileiras, quem usa tela digital 3 h ou mais por dia relata mais problema de sono: {{rp_br_pct_min}} a {{rp_br_pct_max}} mais frequente, com ajuste. Não foi detectada diferença entre a PNS e o Vigitel."
2. "Mas a tela explica pouco do sono: menos que o sexo e, na PNS, menos que a idade."
3. "No mundo, a correlação também é pequena; as maiores aparecem com uso problemático e celular antes de dormir."
4. "Sem ajuste por idade, a PNS mostraria o contrário. Comparar grupos de uso de tela exige ajuste."
5. "São dados transversais: é associação, não causalidade."

**Slide 18 — Repositório público e perguntas**

- **Fechar:** "Tudo o que mostramos está num repositório público: o código, as tabelas de resultados, o relatório e estes slides. O endereço é github.com/otavio44585/Estatistica-4, e o site é otavio44585.github.io/Estatistica-4."
- "Obrigado. Perguntas?"

---

## Perguntas prováveis

| Pergunta | Resposta curta |
|---|---|
| p < 0,001 em quase tudo não é suspeito? | Com {{n_vigitel2024}} a {{n_pns2019}} pessoas, qualquer diferença pequena fica significativa. Por isso mostramos tamanho de efeito e IC, não só p |
| Por que Holm e não Bonferroni? | Holm mantém a chance de pelo menos um falso positivo na família em no máximo 5%, como Bonferroni, mas rejeita mais |
| Por que a RP e não o odds ratio? | O desfecho é comum ({{prev_sono_pns2019}} a {{prev_adormecer_vigitel2024}}). Nesse caso o OR exagera a associação, e a RP se lê direto como "quantas vezes mais" |
| Tela causa insônia? | Os dados não permitem dizer. São transversais, e a literatura mostra também o caminho inverso |
| Por que juntar pesquisas de outros países? | Para ver se o tamanho no Brasil é parecido com o de fora. Como as escalas são diferentes, a comparação é pela correlação, não pelos valores brutos |
| O que o α de Cronbach e o KMO dizem? | O α ({{alfa_insonia3_vigitel}}) mede se as perguntas andam juntas; a partir de 0,7 é o usual para somar itens. O KMO ({{kmo_insonia3_vigitel}}) mede se as correlações bastam para resumir em fatores; abaixo de 0,5 não serve |
| Por que a PNS dá correlação negativa? | Idade: quem usa mais tela é mais jovem, e os jovens relatam menos problema de sono. Ajustada por idade, a correlação vai a {{rho_aj_pns2019}}; a RP vai de {{rp_bruta_digital_pns2019}} a {{rp_ajustada_digital_pns2019}} |
| Os resultados do Excel batem com os do Python? | Sim. A ferramenta do Excel foi executada de verdade e comparada número a número: {{conf_dentro}} de {{conf_n}} dentro da tolerância. As {{conf_excecoes}} exceções vêm do Excel arredondar o grau de liberdade de Welch |
