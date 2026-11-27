# Brasil: como ler a razão de prevalências e os testes (spec 003)

Texto de apoio para o grupo. Os números citados vêm de `resultados/003/tabelas/`, gerados por `python -m analise.brasil_eua.executa`. O resumo completo está em `resultados/003/RESUMO.md`, e o passo a passo, em `analise/notebooks/04_testes_brasil_eua.ipynb`.

> **Os EUA saíram do trabalho em 27/11/2026.** A única base dos EUA (NHANES) é de 2005, antes do smartphone. O tempo de tela daquela época não se compara com o de 2019–2024, e a comparação misturava país e época. Por isso saíram H3.3 (NHANES) e H3.6 (Brasil × EUA). A decisão veio depois de os resultados com o NHANES já terem sido calculados e está registrada no Histórico da spec. A comparação do Brasil com outros países está na spec 004.

## A pergunta

Quem passa 3 horas ou mais por dia em telas no lazer relata mais problema de sono do que quem usa menos de 1 hora? Testamos isso nas duas pesquisas nacionais do Brasil. E perguntamos se o tamanho dessa associação muda entre as duas pesquisas, entre faixas etárias e entre TV e tela digital.

## As bases

| Base | Quem | Desfecho usado | Desenho amostral |
|---|---|---|---|
| Vigitel 2024 | adultos das 27 capitais, por telefone | dificuldade para adormecer "quase sempre" ou "sempre" | só peso (o Vigitel não divulga estrato e UPA) |
| PNS 2019 | adultos do Brasil todo, em domicílios | problema de sono em mais da metade dos dias nas últimas 2 semanas | peso, estrato e UPA |

As duas pesquisas perguntam sobre sono de jeitos diferentes. A da PNS inclui acordar à noite e dormir demais. Por isso, comparar PNS e Vigitel (H3.9) mistura pesquisa e pergunta.

## A técnica: razão de prevalências

**Prevalência** é a proporção de pessoas com o problema. A **razão de prevalências (RP)** divide a prevalência do grupo de tela alta pela do grupo de tela baixa:

- RP = 1: as duas prevalências são iguais.
- RP = 1,30: o grupo de tela alta tem 30% a mais de pessoas com o problema, em termos relativos.

Para ajustar por idade, sexo e escolaridade, usamos **regressão de Poisson com ligação log**. O coeficiente da tela, exponenciado, é a RP ajustada: a comparação entre pessoas da mesma faixa etária, sexo e escolaridade. Não usamos regressão logística porque o desfecho é comum (15% a 25%), e a razão de chances da logística exageraria a diferença.

O notebook confere à mão que a RP bruta do Vigitel, calculada pela tabela 2×2, é igual à do modelo de Poisson.

## Por que o desenho amostral muda o resultado

A PNS não sorteia pessoas soltas. Ela sorteia áreas (UPA) dentro de regiões (estratos) e depois domicílios dentro das áreas. Pessoas da mesma área se parecem, então a amostra tem menos informação do que o n sugere.

- O **peso** corrige quem teve mais ou menos chance de ser sorteado e muda a estimativa.
- **Estrato e UPA** mudam o erro padrão. Usamos a linearização de Taylor, o mesmo método do pacote `survey` do R. O R não está instalado na máquina, então o método foi implementado em Python e testado contra o `statsmodels`.

Com o desenho, o erro padrão fica maior que o de um modelo que o ignora (`comparacao_variancia.csv`). Os intervalos ficam mais largos e mais honestos. No Vigitel, só o peso já quase dobra o erro padrão.

**Graus de liberdade.** A regra do projeto é gl = UPAs − estratos. Na PNS, são 8.027 UPAs em 574 estratos, ou 7.453 gl. Com tantos gl, a regra alternativa do `svyglm` do R (d − p + 1) dá o mesmo resultado prático.

**Testes com várias restrições ao mesmo tempo**, como na H3.7 (6 interações idade × tela), usam a correção de Korn-Graubard: F = (d − q + 1)/(d·q) · W.

**RP dentro de uma faixa etária** é estimada por **domínio**: o modelo é ajustado só na faixa, mas a variância usa o desenho inteiro, com todas as UPAs e estratos. Filtrar as linhas antes do cálculo faria parecer que o desenho tem menos UPAs do que tem.

## Os testes

Cada hipótese tem H0 (não há diferença), H1 (há), uma estatística e um p-valor. Como fazemos vários testes, a **correção de Holm** ajusta os p-valores dentro de cada família, para que a chance de pelo menos um falso positivo na família fique em no máximo 5%. Todos os testes são bilaterais (H1: RP ≠ 1); o sinal esperado (RP > 1) vem da literatura.

**Família 1: associação em cada pesquisa**, separada por exposição (tela digital e TV):

- H3.1 e H3.2: a RP de tela alta é diferente de 1 no Vigitel e na PNS?
- H3.4: há gradiente (dose-resposta) nas três faixas de tela, em cada pesquisa?

**Família 2: comparações**:

- H3.7: a RP muda com a faixa etária (Vigitel, PNS)?
- H3.8: a RP da TV é diferente da RP da tela digital (Vigitel, PNS)?
- H3.9: PNS e Vigitel dão RP diferentes?

## O que encontramos

1. **Nas duas pesquisas, tela digital ≥ 3 h/dia se associa a mais problema de sono**, já ajustando por idade, sexo e escolaridade: RP 1,32 no Vigitel e 1,19 na PNS (`hipoteses.csv`). As duas rejeitam H0 depois de Holm. Com TV, as duas também rejeitam.
2. **A idade confunde a relação na PNS.** Sem ajuste, a RP da tela digital fica abaixo de 1, porque quem usa mais tela é mais jovem e os jovens relatam menos problema de sono. Com idade no modelo, a RP passa para acima de 1. Por isso olhamos a bruta e a ajustada lado a lado.
3. **A forma é de limiar, não de reta.** Para quem usa de 1 a 3 h, a RP fica perto de 1 ou abaixo, em relação a quem usa menos de 1 h; o excesso aparece a partir de 3 h. O teste de tendência linear dá significativo, mas descreve mal a forma. O teste de desvio da linearidade é exploratório: não estava previsto.
4. **Nenhuma comparação da família 2 rejeita H0** depois de Holm. Não foi detectada variação por faixa etária, entre TV e tela digital, nem entre PNS e Vigitel (razão Vigitel ÷ PNS 1,11, IC 0,96 a 1,28; `comparacoes_entre_bases.csv`). É falta de evidência de diferença, não prova de igualdade.

## Como falar disso (e como não falar)

- **Dizer:** "quem usa tela 3 h ou mais por dia **relata mais** problema de sono"; "**não foi detectada diferença** entre PNS e Vigitel, com intervalo de confiança largo".
- **Não dizer:** "a tela **causa** insônia" ou "o efeito da tela". Os dados são de um momento só (transversais). Quem dorme mal pode usar mais o celular à noite (causalidade reversa), e outras coisas, como ansiedade ou trabalho em turnos, podem explicar parte da associação.

## Limitações

- As perguntas de sono da PNS e do Vigitel são diferentes.
- O Vigitel só cobre as capitais e não tem estrato e UPA.
- Renda não entrou no ajuste: não existe no Vigitel.
- Esta spec não compara países. Os EUA saíram do trabalho, e a posição do Brasil no mundo está na spec 004.
- As hipóteses foram escritas depois da análise exploratória, e o relatório declara isso.
