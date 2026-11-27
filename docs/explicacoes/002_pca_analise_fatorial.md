# PCA e análise fatorial: o que fizemos e como ler

Guia da spec 002 para o grupo. Os números estão em `resultados/002/RESUMO.md`; o passo a passo com código está nos notebooks `analise/notebooks/02_pca_svd.ipynb` e `03_analise_fatorial.ipynb`.

## Para que serve esta etapa

Nas specs 003 a 005 usamos índices como "insônia de 0 a 12", que é a soma de três perguntas: dificuldade para adormecer, para voltar a dormir e acordar cedo demais. Também usamos o PHQ-9 e escalas como SAS-SV, doomscrolling e AIS. Antes de somar perguntas e comparar países, precisamos checar duas coisas:

1. As perguntas medem **uma coisa só**? Se medirem duas, a soma mistura construtos.
2. Medem **a mesma coisa no Brasil e nos EUA**? Se não, a diferença entre países pode ser só diferença de medida.

PCA e análise fatorial respondem a isso com os dados, em vez de supor.

## PCA (análise de componentes principais)

**Ideia.** Procurar combinações dos itens que concentrem o máximo de variância. O 1º componente é a combinação que mais "explica" as diferenças entre as pessoas; o 2º explica o que sobra, sem se correlacionar com o 1º; e assim por diante.

**Como calculamos: pela SVD.**

1. Padronizamos cada item: Z = (X − média) / desvio padrão.
2. Decompomos Z = U Σ Vᵀ (decomposição em valores singulares).
3. Calculamos os **autovalores** λ = σ² / (n − 1). Cada autovalor é a variância de um componente. A soma deles é o número de itens, então λ / p é a proporção explicada.
4. Calculamos as **cargas** = V Σ / √(n − 1). A carga é a correlação entre o item e o componente.
5. Calculamos os **escores** = U Σ = Z V, um valor por pessoa.

Conferimos com o `scikit-learn`: os autovalores batem até a 14ª casa decimal.

**Como ler.** Nos 3 sintomas de insônia, o 1º componente explica 75% da variância no Vigitel e 71% no NHANES. Todas as cargas ficaram entre 0,79 e 0,90. Há, portanto, um eixo dominante de "insônia em geral".

## Quantas dimensões? Três critérios

| Critério | Regra | Problema |
|---|---|---|
| Kaiser | reter autovalor > 1 | com muitos dados, aceita componentes que são só ruído |
| Scree | olhar o "cotovelo" do gráfico | subjetivo |
| **Análise paralela de Horn** | reter o componente só se o autovalor for maior que o de dados **aleatórios** (P95 de 1.000 simulações com o mesmo n e p) | é a regra que decide no nosso plano |

Exemplo em que os critérios discordam: nos 7 sintomas de sono do NHANES, o 2º autovalor é 1,03. Kaiser reteria esse componente, mas o aleatório chega a 1,04, então a análise paralela retém só 1.

## Análise fatorial (AF)

**Diferença para a PCA.** A PCA resume toda a variância dos itens. A AF supõe que cada resposta = fator comum + erro próprio do item e modela só a parte **comum**. Por isso a AF é o modelo de "construto latente" e a PCA é um resumo de dados.

**O que aparece na saída:**

- **Carga:** quanto o item depende do fator (de −1 a 1).
- **Comunalidade (h²):** fração da variância do item explicada pelos fatores.
- **Unicidade:** 1 − h², a parte própria do item.
- **Rotação:** com 2 fatores ou mais, gira a solução para facilitar a leitura.
  - **Varimax** força os fatores a serem independentes.
  - **Oblimin** deixa que se correlacionem; Φ é essa correlação.
- **Escore fatorial:** a posição estimada de cada pessoa no fator. Usamos o método de regressão.

**Os dados servem para AF?**

- **KMO e MSA:** comparam as correlações com as correlações parciais. Perto de 1 é bom; obtivemos de 0,67 a 0,96.
- **Bartlett:** testa se os itens são independentes entre si. Com milhares de pessoas, sempre rejeita, então só confirma que há o que modelar.
- **α de Cronbach:** consistência interna; obtivemos de 0,79 a 0,95.

## Mesma estrutura entre países: coeficiente de Tucker

Comparamos as cargas do Brasil e dos EUA com φ = Σ aᵢbᵢ / √(Σaᵢ² Σbᵢ²). A referência (Lorenzo-Seva e ten Berge, 2006) diz:

- de 0,85 a 0,94: similaridade razoável;
- acima de 0,95: os fatores podem ser considerados iguais.

| Instrumento | Brasil × EUA | φ | Leitura |
|---|---|---|---|
| 3 sintomas de insônia | Vigitel × NHANES | 0,998 | iguais |
| PHQ-9 | PNS × NHANES | 0,997 | iguais |

**Armadilha.** Quando todas as cargas são positivas, φ tende a sair alto. Por isso também olhamos a maior diferença entre cargas: 0,08 na insônia e 0,11 no PHQ-9. Tucker não substitui um teste formal de invariância (AFC multigrupo), que ficou fora do escopo.

## O que concluímos

- **Insônia (H2.1, H2.2):** os 3 sintomas formam um único fator no Brasil e nos EUA, com a mesma estrutura. Somar os 3 itens é legítimo: a soma correlaciona 0,9998 com o 1º componente.
- **PHQ-9 (H2.3, H2.4):** 1 fator nos dois países, com estrutura equivalente. Quando forçamos 2 fatores (análise exploratória), o item de sono fica junto com o cansaço (fator "somático"), e não com o humor deprimido, nos dois países.
- **Escalas dos outros países (H2.5):**
  - Doomscrolling (Turquia) e AIS (Japão) são unidimensionais.
  - SAS-SV (China) tem 2 dimensões: abstinência e perturbação da rotina.
  - A procrastinação do sono tem 2 dimensões na Turquia e no Japão. No Japão, o 2º fator reúne exatamente os itens de redação invertida, sinal de efeito de redação e não de outro construto.
- **PCA × AF (H2.6):** os escores dos dois métodos ordenam as pessoas quase igual (r de 0,95 a 0,999).

## Armadilhas e limitações

- **Três itens são o mínimo para um fator.** O modelo fica exatamente identificado e não há como testar o ajuste.
- **Itens ordinais** (nunca/às vezes/sempre) com correlação de Pearson subestimam a associação. Repetimos com a correlação **policórica**: o 1º autovalor sobe, mas as cargas mantêm o padrão.
- **Peso amostral:** a AF não usa o desenho do inquérito. Repetimos com a correlação ponderada pelo peso, e nada mudou.
- **Época:** o NHANES é de 2005-06; a PNS é de 2019 e o Vigitel, de 2024.
- **Itens sem rótulo:** os depósitos da Turquia e do Japão não descrevem o conteúdo de cada item de FK, UE e BPS.
