# PCA e análise fatorial: o que fizemos e como ler

Guia da spec 002 para o grupo. Os números estão em `resultados/002/RESUMO.md`. O passo a passo com código está nos notebooks `analise/notebooks/02_pca_svd.ipynb` e `03_analise_fatorial.ipynb`.

> Em 2026-11-27 os EUA (NHANES 2005-06) saíram do trabalho, porque a única base americana é de 2005, antes do smartphone. As hipóteses que comparavam Brasil e EUA (H2.2 a H2.4) foram retiradas.

## Para que serve esta etapa

Nas etapas seguintes usamos o **índice de insônia de 0 a 12** do Vigitel 2024. Ele é a soma de três perguntas. Também usamos o PHQ-9 da PNS e as escalas dos outros países (SAS-SV, doomscrolling, AIS). Antes de somar perguntas, precisamos saber se elas medem **uma coisa só**. Se medirem duas, a soma mistura assuntos diferentes. PCA e análise fatorial respondem isso com os dados, em vez de supor.

## Quais perguntas juntamos em cada PCA

| Conjunto | Base | Itens que entraram |
|---|---|---|
| **Índice de insônia** | Vigitel 2024 | `r703` dificuldade para dormir; `r704` acordou e teve dificuldade para dormir de novo; `r705` acordou antes da hora desejada e não conseguiu dormir de novo. Respostas de 1 (nunca) a 5 (sempre), recodificadas para 0 a 4 |
| PHQ-9 (depressão) | PNS 2019 | interesse, humor deprimido, sono, cansaço, apetite, sentir-se um fracasso, concentração, lentidão/agitação, pensamentos de autolesão (perguntas N010 a N018, de 0 a 3) |
| SAS-SV (uso problemático do celular) | China | 10 itens: perde planos por causa do celular, perde eficiência, dor no punho/pescoço, não suporta ficar sem, impaciente sem o celular, inquieto sem o celular, não desiste apesar dos efeitos, checa o tempo todo, usa mais que o previsto, outros dizem que usa demais |
| Doomscrolling | Turquia | 15 itens (FK1 a FK15), sem rótulo de conteúdo no depósito |
| Procrastinação do sono | Turquia | 9 itens (UE1 a UE9), sem rótulo |
| AIS (insônia de Atenas) | Japão | 8 itens: indução do sono, despertares noturnos, despertar precoce, duração total, qualidade, bem-estar diurno, funcionamento diurno, sonolência diurna |
| BPS (procrastinação do sono) | Japão | 9 itens, 4 deles com redação invertida (BPS2R, BPS3R, BPS7R, BPS9R) |

## Dois indicadores antes de tudo: α de Cronbach e KMO

- **α de Cronbach (consistência interna).** Mede se as perguntas "andam juntas": quem responde alto numa tende a responder alto nas outras. Vai de 0 a 1, e acima de 0,7 costuma ser considerado bom para somar os itens num índice. No índice de insônia do Vigitel, α = 0,84.
- **KMO (Kaiser-Meyer-Olkin).** Mede se as correlações entre as perguntas vêm de algo **em comum a todas**, e não só de pares de perguntas parecidas. Vai de 0 a 1; perto de 1 indica que vale a pena procurar um fator comum. A regra prática de 0,60 ainda está "a verificar" na fonte. No Vigitel, KMO = 0,71; o MSA é o mesmo índice calculado pergunta a pergunta.
- **Bartlett** testa se as perguntas são independentes entre si. Com milhares de pessoas ele sempre rejeita; só confirma que há correlação a modelar.

## PCA (análise de componentes principais)

**Ideia.** Procurar combinações das perguntas que concentrem o máximo de variância. O 1º componente é a combinação que mais "explica" as diferenças entre as pessoas; o 2º explica o que sobra, sem se correlacionar com o 1º; e assim por diante.

**Como calculamos: pela decomposição em valores singulares (SVD).**

1. Padronizamos cada item: Z = (X − média) / desvio padrão.
2. Decompomos Z = U Σ Vᵀ.
3. Calculamos os **autovalores** λ = σ² / (n − 1). Cada autovalor é a variância de um componente. A soma deles é o número de itens, então λ / p é a proporção explicada.
4. Calculamos as **cargas** = V Σ / √(n − 1). A carga é a correlação entre o item e o componente.
5. Calculamos os **escores** = U Σ = Z V, um valor por pessoa.

Conferimos com o `scikit-learn`: os autovalores batem até 10⁻⁸.

**Como ler, no Vigitel 2024.** O 1º componente explica 75% da variância das três perguntas, e as cargas vão de 0,83 a 0,90. Há um eixo dominante de "insônia em geral". A soma simples das três perguntas correlaciona 0,9998 com esse componente, então o índice 0–12 resume bem o que o componente mede.

## Quantas dimensões? Três critérios

| Critério | Regra | Problema |
|---|---|---|
| Kaiser | reter autovalor > 1 | com muitos dados, aceita componentes que são só ruído |
| Scree | olhar o "cotovelo" do gráfico | subjetivo |
| **Análise paralela de Horn** | reter o componente só se o autovalor for maior que o de dados **aleatórios** (P95 de 1.000 simulações com o mesmo n e p) | é a regra que decide no nosso plano |

No Vigitel, o 1º autovalor é 2,26 contra 1,02 dos aleatórios, e o 2º é 0,45 contra 1,00: a análise paralela retém **um fator**.

## Análise fatorial (AF)

**Diferença para a PCA.** A PCA resume toda a variância das perguntas. A AF supõe que cada resposta = fator comum + erro próprio da pergunta, e modela só a parte **comum**. Por isso a AF é o modelo de "construto latente" e a PCA é um resumo de dados. No Vigitel as cargas da AF (0,71 a 0,88) ficam um pouco abaixo das da PCA, como esperado, porque a AF desconta o erro de cada pergunta.

**O que aparece na saída:**

- **Carga:** quanto a pergunta depende do fator (de −1 a 1).
- **Comunalidade (h²):** fração da variância da pergunta explicada pelos fatores.
- **Unicidade:** 1 − h², a parte própria da pergunta.
- **Rotação:** com 2 fatores ou mais, gira a solução para facilitar a leitura.
  - **Varimax** força os fatores a serem independentes.
  - **Oblimin** deixa que se correlacionem; Φ é essa correlação.
- **Escore fatorial:** a posição estimada de cada pessoa no fator. Usamos o método de regressão.

## O que concluímos

- **Insônia (H2.1):** as três perguntas do Vigitel 2024 formam um único fator. Somar as três é legítimo.
- **PHQ-9 da PNS (descritivo):** 1 fator. Quando forçamos 2 fatores (análise exploratória), o item de sono fica junto com o cansaço (fator "somático"), e não com o humor deprimido.
- **Escalas dos outros países (H2.5):**
  - Doomscrolling (Turquia) e AIS (Japão) são unidimensionais.
  - SAS-SV (China) tem 2 dimensões: abstinência e perturbação da rotina.
  - A procrastinação do sono tem 2 dimensões na Turquia e no Japão. No Japão, o 2º fator reúne exatamente os itens de redação invertida, sinal de efeito de redação e não de outro construto.
- **PCA × AF (H2.6):** os escores dos dois métodos ordenam as pessoas quase igual (r de 0,95 a 0,999).
- **H2.2 a H2.4:** retiradas em 2026-11-27, com a saída dos EUA do trabalho.

## Armadilhas e limitações

- **Três itens são o mínimo para um fator.** O modelo fica exatamente identificado e não há como testar o ajuste.
- **Itens ordinais** (nunca/às vezes/sempre) com correlação de Pearson subestimam a associação. Repetimos com a correlação **policórica**: o 1º autovalor sobe, mas as cargas mantêm o padrão.
- **Peso amostral:** a AF não usa o desenho do inquérito. Repetimos com a correlação ponderada pelo peso, e nada mudou.
- **Itens sem rótulo:** os depósitos da Turquia e do Japão não descrevem o conteúdo de cada item de FK, UE e BPS.
