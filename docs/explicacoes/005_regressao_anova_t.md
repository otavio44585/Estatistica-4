# Regressão linear múltipla, ANOVA e teste t — explicação para o grupo

Spec 005. Números em `resultados/005/RESUMO.md`; passo a passo no notebook `analise/notebooks/06_regressao_linear.ipynb`.

## 1. O que a regressão múltipla responde

Pergunta: **quanto o sono muda, em média, quando o uso de tela muda e as outras variáveis ficam fixas?**

O modelo do Vigitel e do NHANES é:

```text
índice de insônia = β0 + β1·D(1 a <3 h) + β2·D(≥3 h) + β3·idade + β4·feminino + β5·D(médio) + β6·D(superior) + erro
```

- **D(·) são dummies (0/1).** Cada variável categórica entra com uma dummy a menos que o número de categorias; a categoria
  que fica de fora é a **referência** (tela < 1 h, sexo masculino, escolaridade abaixo do médio). Pôr todas as categorias
  causa a "armadilha das dummies": as colunas somam 1 e a regressão não tem solução única.
- **β2** é a diferença média do índice entre quem usa ≥ 3 h e quem usa < 1 h, **com idade, sexo e escolaridade iguais**. É o
  coeficiente testado na H5.1 e na H5.2.
- Nas bases de repositório a tela é contínua, e o β é a mudança em Y para cada hora (ou ponto de escala) a mais.

## 2. Como ler o SUMMARY OUTPUT do Excel, linha por linha

| Bloco | Linha | O que é | Como usamos |
|---|---|---|---|
| Estatística de regressão | R múltiplo | correlação entre Y observado e Y ajustado (√R²) | só descritivo |
| | R-quadrado | fração da variância de Y explicada pelo modelo, SQReg/SQTot | tamanho do modelo |
| | R-quadrado ajustado | R² penalizado pelo número de regressores, 1 − (1 − R²)(n − 1)/(n − k − 1) | comparar modelos com k diferente |
| | Erro padrão | desvio-padrão dos resíduos, √(SQRes/(n − k − 1)) | escala do erro, em unidades de Y |
| | Observações | n usado (só casos completos) | conferir com o log de n |
| ANOVA | Regressão: gl, SQ, MQ | k; variação explicada; SQ/gl | numerador do F |
| | Resíduo: gl, SQ, MQ | n − k − 1; variação não explicada; s² | denominador do F |
| | F e F de significação | F = MQReg/MQRes e o seu p | testa "todos os β (menos o intercepto) = 0" |
| Coeficientes | Coeficientes | b = (XᵀX)⁻¹Xᵀy | a estimativa |
| | Erro padrão | incerteza de cada b | entra no t e no IC |
| | Stat t | b / erro padrão | testa "este β = 0" |
| | valor-P | 2·P(T > \|t\|) com n − k − 1 gl | decisão, depois de Holm |
| | 95% inferiores / superiores | b ± t crítico · erro padrão | IC; exclui 0 exatamente quando p < 0,05 |

O **F global** e o **t de um coeficiente** respondem perguntas diferentes. No Japão, o F global não é significativo
(p = 0,111) e o t da tela é (p = 0,016): idade e sexo não ajudam a prever a insônia e diluem o F, que testa os três
coeficientes juntos. A hipótese é sobre a tela, então quem decide é o t (ou o F parcial do bloco de tela).

**F parcial.** Compara o modelo completo com o modelo só com covariáveis:
F = [(SQRes_restrito − SQRes_completo)/q] / [SQRes_completo/(n − k − 1)]. Responde "o bloco de tela, junto, acrescenta algo?".
Com uma variável só (q = 1), F parcial = t². O ganho de R² (ΔR²) e o f² = ΔR²/(1 − R²) medem o tamanho desse acréscimo.

## 3. ANOVA de um fator e teste t são casos da regressão

- **ANOVA de um fator** compara as médias de Y nas 3 faixas de tela: F = MQ entre grupos / MQ dentro dos grupos. É
  **exatamente** o F global da regressão de Y nas 2 dummies de tela (conferido: diferença de 10⁻¹⁴).
- **Teste t com variâncias iguais** (≥ 3 h × < 1 h) é **exatamente** o t da dummy numa regressão com só esses dois grupos.
- **Teste t de Welch** não supõe variâncias iguais e usa um gl fracionário (Welch–Satterthwaite). É o que a spec usa; no
  Vigitel o t muda cerca de 1% em relação ao de variâncias iguais.

## 4. p-valor, α e Holm

- O **p** é a probabilidade de ver uma estatística tão extrema quanto a observada **se H0 fosse verdadeira**. Não é a
  probabilidade de H0 ser verdadeira, nem mede o tamanho do efeito.
- α = 0,05 bilateral. Como cada família tem vários testes (6 na R1, 5 na R2), a chance de pelo menos um falso positivo
  cresce. A **correção de Holm** ordena os p, multiplica o menor por m, o segundo por m − 1 e assim por diante (mantendo a
  ordem), e só então compara com 0,05.
- **Amostra grande torna quase tudo significativo.** No Vigitel (27 mil pessoas), a tela explica 0,38% da variância do
  índice de insônia e o p é < 0,001. Por isso cada teste vem com tamanho de efeito e IC.

## 5. Peso amostral: por que o NHANES muda de resposta

Vigitel e NHANES são amostras complexas: cada pessoa representa um número diferente de pessoas da população (peso), e no
NHANES as entrevistas vêm em conglomerados (30 UPAs em 15 estratos). A Regressão do Excel trata todo mundo como amostra
aleatória simples. A versão com peso usa:

- **WLS** (mínimos quadrados ponderados) para a estimativa;
- **erro padrão por linearização** (o mesmo princípio do pacote `survey` do R), que reconhece que pessoas da mesma UPA se
  parecem.

No NHANES, isso aumenta muito o erro padrão e deixa só 15 graus de liberdade (30 UPAs − 15 estratos, a regra única do
projeto, a mesma da spec 003). Sem peso, o coeficiente de ≥ 3 h é significativo (p < 0,001). Com o desenho, não é
(p = 0,145; com a regra do `svyglm` do R, que desconta os parâmetros e deixa 9 gl, p = 0,158 — a decisão não muda).
A spec manda decidir pela versão com peso. A versão do Excel fica como demonstração da técnica e sensibilidade.

O resultado sem peso do NHANES também é **frágil** por outro motivo: sem as observações influentes (Cook > 4/n), o p
sobe para cerca de 0,167.

**Quando o teste envolve mais de um coeficiente** (a ANOVA ponderada, o F global ponderado e a interação da H5.11), o F de
Wald recebe a correção de Korn-Graubard: F = (d − q + 1)/(d·q)·W, com gl (q, d − q + 1), onde d é o gl do desenho e q o
número de coeficientes testados. Com poucos graus de liberdade (NHANES), ela evita que o p fique pequeno demais.
Na H5.11, a variância da interação vem quase toda do NHANES, então o teste usa o gl de desenho do NHANES (15), e não
o da base empilhada (que seria de 27 mil, dominado pelas pessoas do Vigitel).

**d de Cohen** tem a mesma definição sem e com peso: diferença de médias dividida pelo desvio-padrão combinado dentro
dos grupos (com peso, os pesos são normalizados para somar n).

## 6. Por que conferir cada p de três jeitos

| Caminho | O quê | Pega que tipo de erro |
|---|---|---|
| A | saída da Análise de Dados do Excel | erro de quem montou o modelo no script (coluna trocada, dummy errada) |
| B | fórmula `T.DIST.2T` / `F.DIST.RT` ao lado da saída | p copiado ou digitado errado; gl errado |
| C | script, por álgebra matricial | erro de clique no Excel; intervalo errado; planilha editada à mão |

Resultado: 920 de 920 números dentro da tolerância nos três caminhos (maior diferença relativa 4,5 × 10⁻¹⁰), mais
**2 exceções documentadas**, uma por base com teste t (Vigitel e NHANES). Elas mostram um detalhe que ninguém via: no
teste t de Welch, **o Excel arredonda os graus de liberdade para inteiro**, então o p dele difere do p exato em até
1,5 × 10⁻⁵ (relativo), acima da tolerância. O relatório usa o gl fracionário; com o mesmo gl inteiro, Excel e script batem.
Em `resultados/005/conferencia.csv`, as colunas `dentro_tolerancia` e `excecao_documentada` separam os dois casos.

## 7. Pressupostos e o que fizemos quando falharam

| Pressuposto | Achado | O que fizemos |
|---|---|---|
| Normalidade dos resíduos | rejeitada em todas as bases (desfechos discretos e assimétricos) | com n de centenas ou mais, t e F são aproximadamente válidos; QQ-plots no relatório |
| Variância constante | violada em Vigitel, NHANES e Xuzhou (Breusch-Pagan) | erro padrão robusto HC3 como sensibilidade: nenhuma decisão muda |
| Multicolinearidade | VIF da tela ≤ 1,6; com a categoria menos frequente como referência, dummies de renda (Xuzhou) e escolaridade dos pais (Argentina) tinham VIF > 10 | referência passou a ser a categoria mais frequente: VIF máximo ≤ 2,0, coeficiente da tela igual |
| Observações influentes | cerca de 5% com Cook > 4/n | reestimar sem elas: a Turquia perde significância |

## 8. O que concluímos (sem linguagem causal)

- Em 5 das 6 bases o coeficiente da tela é diferente de zero depois de Holm; em 4 delas o sinal é o esperado (mais tela, pior sono).
- O efeito é **pequeno**: o bloco de tela acrescenta de 0,1% (NHANES) a 1,5% (Japão) de R², exceto no uso problemático de
  smartphone em Xuzhou (6,8%).
- **Argentina:** mais tela antes de dormir se associa a **menor** latência. O resultado não se sustenta com outra
  definição de amostra.
- **Brasil × EUA (H5.11):** não foi detectada diferença entre os coeficientes da tela dos dois países (F(2; 14) = 0,19,
  p = 0,830), mas o IC é largo (−0,81 a 0,47 ponto na diferença do coeficiente de ≥ 3 h): não dá para afirmar que é igual.
- **NHANES (H5.2):** com o desenho amostral, não se rejeita H0 (p = 0,145); o resultado sem peso também perde
  significância sem as observações influentes.
- É associação em dados transversais: a direção pode ser a inversa (quem dorme mal fica mais tempo na tela) e pode
  haver confundimento não medido.
