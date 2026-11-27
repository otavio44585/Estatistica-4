# Comparação mundial: como pusemos 6 bases de 5 países no mesmo gráfico

**Decisão do grupo (2026-11-27):** o NHANES 2005-06 (EUA) saiu do trabalho inteiro. A única base dos EUA era de 2005, antes do smartphone, e a comparação misturava país com época.

Explicação para o grupo da spec 004. Os números estão em `resultados/004/RESUMO.md`, e o passo a passo com código está no notebook `analise/notebooks/05_comparacao_mundial.ipynb`.

## O problema

Cada base mede sono e tela de um jeito:

- **Brasil:** faixas de horas de tela e frequência de sintomas de insônia (Vigitel) ou problema de sono (PNS).
- **China e Turquia:** escalas de dependência do celular e o PSQI.
- **Japão:** horas de celular antes de dormir e a Escala de Insônia de Atenas.
- **Argentina:** horas de tela e minutos para adormecer.

Uma razão de prevalências (spec 003) ou um coeficiente de regressão (spec 005) dependem da unidade de cada escala. Por isso não dá para comparar esses números entre bases.

## A solução: uma correlação comum

A **correlação de Spearman (ρ)** não depende da unidade: ela compara a ordem das pessoas na exposição com a ordem delas no desfecho.

- ρ = 0: não há relação monotônica.
- ρ = 1: quem usa mais tela sempre dorme pior.
- ρ = −1: o contrário.

Combinamos o sinal antes de calcular: **positivo = mais tela, pior sono**. Quando o desfecho é "quanto maior, melhor" (duração, qualidade), o sinal é invertido.

Por que Spearman e não Pearson? A exposição dos inquéritos vem em faixas (6 a 8 categorias), e várias escalas são assimétricas. Spearman só usa a ordem, então é menos sensível a isso. O r de Pearson aparece ao lado como conferência, e os dois ficaram próximos em todas as bases.

## Intervalo de confiança: a transformação z de Fisher

A distribuição de ρ não é simétrica perto de ±1. O truque de Fisher é transformar z = atanh(ρ). Na escala z a distribuição é quase normal, e o erro padrão depende só de n. Para Spearman, Fieller, Hartley e Pearson (1957) propuseram EP ≈ √(1,06/(n − 3)).

Essa fórmula supõe dados contínuos sem empates, e nossos dados têm muitos empates. Por isso conferimos o EP por **bootstrap**: reamostramos as pessoas 1.000 vezes e medimos quanto o ρ varia. A diferença máxima foi de 5,4%, dentro do limite de 10% fixado antes. A fórmula ficou.

## Meta-análise: juntar as 7 correlações

Uma meta-análise é uma média ponderada dos efeitos, em que estimativas mais precisas pesam mais.

- **Efeito fixo** supõe que todas as bases medem o mesmo efeito verdadeiro, então o peso é 1/variância. Aqui a PNS, com 88 mil pessoas, levaria quase todo o peso.
- **Efeitos aleatórios (DerSimonian e Laird)** supõe que cada base tem seu efeito verdadeiro, espalhado em torno de uma média com variância τ². O peso vira 1/(variância + τ²). Quando τ² é grande, as bases pesam quase igual. Foi o modelo fixado no plano.

As medidas de heterogeneidade:

- **Q de Cochran** testa se as diferenças entre bases são maiores que o acaso explicaria.
- **I²** é a parte da variação que vem de diferença real entre bases. Nossos 98% são muito altos: as bases discordam de verdade.
- **τ²** é a variância dos efeitos verdadeiros, na escala z.

Cada passo é feito à mão no notebook e conferido com o `statsmodels`; a diferença ficou abaixo de 1e-13.

**Dois intervalos para a média combinada.**

- O **DerSimonian-Laird** usa a distribuição normal. Com poucas bases (aqui 6), esse intervalo sai estreito demais.
- O **Hartung-Knapp** corrige isso: reescala o erro padrão pela dispersão observada entre as bases e usa t com k − 1 graus de liberdade.

Mostramos os dois lado a lado. No global, o DL dá 0,015 a 0,165 e o Hartung-Knapp, −0,029 a 0,207, que inclui o zero. Nenhum dos quatro testes usa esse intervalo, então nenhuma decisão muda. Muda a leitura: o "número combinado" é ainda menos firme do que parecia. O Hartung-Knapp foi acrescentado depois da verificação independente.

**Efeito do desenho nos inquéritos.** O EP de cada correlação supõe amostra aleatória simples, mas PNS e Vigitel têm pesos desiguais. Isso aumenta a variância por um fator chamado *deff*: pelo menos 1 + CV² dos pesos (Kish).

- O deff deu 3,2 na PNS e 3,7 no Vigitel.
- Multiplicando a variância desses dois inquéritos pelo deff, I² cai de 98,7% para 97,9% e Q de 376 para 241. A heterogeneidade continua enorme e as decisões não mudam.
- Esse deff ignora estrato e conglomerado, então ainda subestima a incerteza.

## Os quatro testes e como ler cada um

| Hipótese | Pergunta | Resultado | Como ler |
|---|---|---|---|
| H4.1 | O efeito é o mesmo em todas as bases? | Q = 376, p < 0,001 | Não é. Varia muito (I² = 99%). |
| H4.2 | O tipo de exposição muda a associação? | Q entre = 4,8, p = 0,090 (Holm 0,270) | A ordem bate com a literatura: tempo total 0,02 < pré-sono 0,14 < uso problemático 0,18. Mas com tão poucas bases por grupo, o teste não tem poder para afirmar a diferença. "Não rejeitar" não quer dizer "são iguais". |
| H4.3 | O Brasil difere dos outros países com tempo total? | z = −0,08, p = 0,939 | Não foi detectada diferença. Sem o NHANES, o outro lado é só a Argentina (k = 1, adolescentes): o teste compara o Brasil com uma base. As duas bases brasileiras discordam entre si (ver abaixo). |
| H4.4 | Nossa estimativa de tempo total é equivalente à da meta-análise de referência (r = 0,28)? | TOST p = 1,000 | Não. Ficamos bem abaixo (0,017). |
| Exploratório | Os estudos brasileiros diferem do resto do mundo (Argentina, Japão, China, Turquia, todas as exposições)? | Brasil 0,016 × resto 0,131; z = −1,36, p = 0,173 | Não foi detectada diferença. Pedido depois de ver os resultados, fora de Holm, e mistura tipos de exposição: o resto do mundo sobe por causa das escalas de uso problemático e de pré-sono. |

**H4.2 foi registrada com uma ordem, mas testada sem ela.**

- A spec escreveu H4.2 como "tempo total < pré-sono < uso problemático". O teste fixado no plano (Q entre subgrupos) só pergunta se os grupos diferem, sem usar a ordem.
- Como análise **exploratória**, fora da correção de Holm, ajustamos uma reta às três médias de subgrupo (escore 0, 1, 2). A inclinação é positiva (z = 2,11, p = 0,035; valores em `resultados/004/RESUMO.md`). Isso combina com a ordem prevista, mas são só três pontos, e o teste foi escolhido depois de ver os dados.
- O subgrupo pré-sono tem uma base só (Japão), então não tem τ² nem intervalo de Hartung-Knapp próprios.

**Teste de equivalência (TOST).** Num teste comum, H0 é "igual" e só se conclui "diferente". Para concluir "equivalente", invertemos: H0 é "fora do intervalo 0,21–0,35" e fazemos dois testes unilaterais, um contra cada limite. Só se os dois rejeitarem dá para dizer que a estimativa está dentro.

**Holm.** São 4 testes na mesma família. Holm ordena os p e multiplica o menor por 4, o seguinte por 3, e assim por diante, mantendo a ordem. Isso controla a chance de pelo menos um falso positivo na família.

## O caso da PNS: por que o sinal muda

Na PNS, o ρ bruto é **negativo** (−0,031): quem usa mais tela relata um pouco *menos* problema de sono. Mas quem usa mais tela é mais jovem, e jovens relatam menos problema de sono. A idade confunde a relação.

O **ρ parcial** remove a parte da ordem que é explicada pela idade. Ajustado por idade, o ρ da PNS vira **+0,027**, positivo como nas outras bases. É o mesmo fenômeno que a exploração de 27/11 viu na razão de prevalências (bruta 0,90, ajustada 1,17). Ajustadas por idade, as bases de tempo total combinadas dão 0,045 (IC 0,017 a 0,073).

## Por que ficamos abaixo da literatura

A meta-análise de referência (Han, Zhou e Liu, 2024) encontrou r = 0,28 para uso geral × qualidade do sono. Nossa estimativa de tempo total é bem menor. Explicações possíveis, que este trabalho **não** consegue separar:

- **População:** a referência tem sobretudo estudantes e jovens. PNS e Vigitel cobrem todos os adultos.
- **Medida:** qualidade do sono (PSQI) é diferente de frequência de sintomas de insônia, problema de sono em 2 semanas ou latência.
- **Exposição:** faixas grosseiras de horas por dia atenuam a correlação.
- **Seleção da literatura:** estudos publicados tendem a ter efeitos maiores do que inquéritos nacionais, que não foram feitos para testar essa associação.

Quando a exposição é **uso problemático** (China, Turquia) ou **tela antes de dormir** (Japão), a associação fica mais perto da da literatura. Não foi detectada diferença entre o uso problemático e r = 0,33 (análise exploratória, IC largo).

## Armadilhas que evitamos

- **Ler a média global como "a associação verdadeira".** Com I² = 98% ela é só um resumo, e o IC de Hartung-Knapp inclui o zero.
- **Concluir igualdade a partir de p > 0,05.** Vale para H4.2 e H4.3.
- **Misturar as bases suspeitas** (Paquistão, Bangladesh, Sleep Patterns) na estimativa principal. Elas aparecem só na sensibilidade, rotuladas.
- **Falar em causa.** São dados transversais, então o resultado é uma associação. O contraponto da Holanda, que acompanha os mesmos adolescentes por 21 noites, não encontrou pior sono nas noites com mais celular antes de deitar (r = 0,016).
