# Brasil × EUA: como ler a razão de prevalências e os testes (spec 003)

Texto de apoio para o grupo. Os números citados vêm de `resultados/003/tabelas/` (gerados por `python -m analise.brasil_eua.executa`); o resumo completo está em `resultados/003/RESUMO.md` e o passo a passo em `analise/notebooks/04_testes_brasil_eua.ipynb`.

## A pergunta

Quem passa 3 horas ou mais por dia em telas no lazer relata mais problema de sono do que quem usa menos de 1 hora? E essa diferença tem o mesmo tamanho no Brasil e nos EUA?

## As bases

| Base | Quem | Desfecho usado | Desenho amostral |
|---|---|---|---|
| Vigitel 2024 | adultos das 27 capitais, por telefone | dificuldade para adormecer "quase sempre" ou "sempre" | só peso (o Vigitel não divulga estrato e UPA) |
| PNS 2019 | adultos do Brasil todo, domicílios | problema de sono em mais da metade dos dias nas últimas 2 semanas | peso, estrato e UPA |
| NHANES 2005-06 | adultos dos EUA | dificuldade para adormecer "often" ou "almost always" (5 ou mais vezes por mês) | peso, estrato e UPA |

O desfecho da PNS é outra pergunta (inclui acordar à noite e dormir demais). Por isso a comparação principal Brasil × EUA usa Vigitel × NHANES, que fazem a mesma pergunta, mas com âncoras de frequência diferentes ("quase sempre/sempre" no Vigitel; "5 ou mais vezes por mês" no NHANES).

## A técnica: razão de prevalências

**Prevalência** é a proporção de pessoas com o problema. **Razão de prevalências (RP)** divide a prevalência do grupo de tela alta pela do grupo de tela baixa:

- RP = 1: as duas prevalências são iguais.
- RP = 1,30: o grupo de tela alta tem 30% a mais de pessoas com o problema (em termos relativos).

Para ajustar por idade, sexo e escolaridade usamos **regressão de Poisson com ligação log**. O coeficiente da tela, exponenciado, é a RP ajustada: a comparação entre pessoas da mesma faixa etária, sexo e escolaridade. Usamos Poisson, e não regressão logística, porque o desfecho é comum (15% a 25%) e a razão de chances da logística exageraria a diferença.

O notebook confere à mão: a RP bruta do Vigitel calculada pela tabela 2×2 é igual à do modelo de Poisson.

## Por que o desenho amostral muda o resultado

PNS e NHANES não sorteiam pessoas soltas: sorteiam áreas (UPA) dentro de regiões (estratos) e depois domicílios dentro das áreas. Pessoas da mesma área se parecem, então a amostra tem menos informação do que o n sugere.

- O **peso** corrige quem foi mais ou menos sorteado e muda a estimativa.
- **Estrato e UPA** mudam o erro padrão. Usamos a linearização de Taylor, o mesmo método do pacote `survey` do R. O R não está instalado na máquina, então o método foi implementado em Python e testado contra o `statsmodels`.

Na prática, o erro padrão com desenho ficou 1,1 a 1,7 vezes maior que o de um modelo que ignora o desenho (`comparacao_variancia.csv`). Os intervalos ficam mais largos e honestos.

O NHANES tem só 15 graus de liberdade de desenho (30 UPAs em 15 estratos). Por isso os testes usam a distribuição t com 15 gl, e os intervalos dos EUA são bem mais largos que os do Brasil.

**Atenção: a regra de graus de liberdade pesa no NHANES.** A regra do projeto é gl = UPAs − estratos (15), a orientação do NCHS. O `svyglm` do R desconta ainda os parâmetros do modelo (15 − 9 + 1 = 7 gl). Com 15 gl, H3.3 rejeita H0 (p Holm 0,033); com 7 gl, não rejeita (p Holm 0,061). A estimativa da RP é a mesma, e só a incerteza muda. Os dois resultados estão em `hipoteses.csv` (colunas `p_holm` e `p_holm_svyglm`). Vigitel e PNS não dependem da regra.

**Testes com várias restrições ao mesmo tempo** (H3.7: 6 interações idade × tela) usam a correção de Korn-Graubard, F = (d − q + 1)/(d·q) · W. Sem ela, com só 15 gl, o teste rejeitaria H0 com facilidade demais. Com a correção, o NHANES passa a F com 6 e 10 gl.

**RP dentro de uma faixa etária** é estimada por **domínio**: o modelo é ajustado só na faixa, mas a variância usa o desenho inteiro (todas as UPAs e estratos). Filtrar as linhas antes do cálculo faria parecer que o desenho tem menos UPAs do que tem.

## Os testes

Cada hipótese tem H0 (não há diferença), H1 (há), uma estatística e um p-valor. Como fazemos vários testes, a **correção de Holm** ajusta os p-valores dentro de cada família, para que a chance de pelo menos um falso positivo na família fique em no máximo 5%. Todos os testes são bilaterais (H1: RP ≠ 1); o sinal esperado (RP > 1) vem da literatura.

**Família 1 (dentro de cada país)**, separada por exposição (tela digital e TV):

- H3.1 a H3.3: a RP de tela alta é diferente de 1 no Vigitel, na PNS e no NHANES?
- H3.4: há gradiente (dose-resposta) nas três faixas de tela?

**Família 2 (comparações)**:

- H3.6: a RP é diferente entre Brasil e EUA?
- H3.7: a RP muda com a faixa etária?
- H3.8: a RP da TV é diferente da RP da tela digital?
- H3.9: PNS e Vigitel dão RP diferentes?

## O que encontramos

1. **Nas três bases, tela digital ≥ 3 h/dia se associa a mais problema de sono**, já ajustando por idade, sexo e escolaridade. As três rejeitam H0 depois de Holm com a regra de gl do projeto (`hipoteses.csv`); no NHANES, a decisão depende da regra de gl (ver acima). Com TV, as três também rejeitam H0.
2. **A idade confunde a relação na PNS.** Sem ajuste, a RP da tela digital fica abaixo de 1. Quem usa mais tela é mais jovem, e jovens relatam menos problema de sono. Com idade no modelo, a RP passa para acima de 1. É o exemplo de por que olhamos a bruta e a ajustada lado a lado.
3. **A forma é de limiar, não de reta.** Em quem usa de 1 a 3 h, a RP fica perto de 1 ou abaixo, em relação a quem usa menos de 1 h; o excesso aparece a partir de 3 h. O teste de tendência linear dá significativo, mas descreve mal a forma (o teste de desvio da linearidade é exploratório, não estava previsto).
4. **Não foi detectada diferença entre Brasil e EUA para a tela digital** (H3.6 não rejeita H0). Isso é falta de evidência de diferença, não prova de igualdade: o IC da razão das RP vai de 0,80 a 1,44 (`comparacoes_entre_bases.csv`), o que é compatível tanto com uma RP dos EUA 20% menor quanto 44% maior. Além disso, a exposição do NHANES é computador/games de 2005 e a do Vigitel é computador/tablet/celular de 2024. Para a TV a diferença aparece com peso e some sem peso, então não tratamos como resultado robusto.
5. **Nenhuma comparação da família 2 rejeita H0** depois de Holm: a RP não muda de forma detectável com a idade, entre TV e tela digital, nem entre PNS e Vigitel.

## Como falar disso (e como não falar)

- Dizer: "quem usa tela 3 h ou mais por dia **relata mais** problema de sono", "**não foi detectada diferença** entre Brasil e EUA, com intervalo de confiança largo".
- Não dizer: "a tela **causa** insônia", "o efeito da tela". Os dados são de um momento só (transversais). Quem dorme mal pode usar mais o celular à noite (causalidade reversa), e outras coisas (ansiedade, trabalho em turnos) podem explicar parte da associação.

## Limitações

- NHANES 2005-06 é anterior ao smartphone: comparar com o Vigitel 2024 mistura país e época.
- A pergunta de sono da PNS é diferente.
- O Vigitel só cobre as capitais e não tem estrato/UPA.
- Renda não entrou no ajuste (não existe no Vigitel).
- As hipóteses foram escritas depois de olhar a análise exploratória; o relatório declara isso.
