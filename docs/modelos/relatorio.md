# Insônia digital: uso de telas e sono no Brasil, nos EUA e em outros quatro países

Estatística 4 · ESEG · Relatório gerado em {{data}} por `analise/relatorio/relatorio.py`. Todos os resultados próprios deste texto (estimativas, IC, p, n) saem de arquivos em `resultados/` e `analise/dados/logs/`, lidos pelo script; nenhum foi digitado à mão. Números da literatura vêm das fontes citadas. Revisão do grupo pendente.

## Resumo

- **Pergunta.** Adultos que usam mais telas no lazer relatam mais problemas de sono? A associação tem o mesmo tamanho no Brasil e nos EUA, e onde o Brasil fica frente a outros países e à literatura?
- **Dados.** {{n_total}} pessoas em sete bases abertas: PNS 2019 e Vigitel 2024 (Brasil), NHANES 2005-06 (EUA) e amostras da China, Argentina, Turquia e Japão.
- **Mesma medida nos dois países.** Os três sintomas de insônia formam um único fator no Brasil e nos EUA, com cargas praticamente iguais (congruência de Tucker φ = {{tucker_insonia}}). Isso autoriza comparar o índice de insônia entre os dois países.
- **Associação presente nos dois países.** Quem usa computador, tablet ou celular 3 h ou mais por dia tem prevalência de problema de sono frequente {{rp_digital_vigitel2024}} vez a de quem usa menos de 1 h no Vigitel, {{rp_digital_pns2019}} na PNS e {{rp_digital_nhanes0506}} no NHANES. São razões de prevalência ajustadas, todas com p Holm < 0,05. No NHANES, essa conclusão depende da regra de graus de liberdade (ver §7).
- **Não foi detectada diferença entre Brasil e EUA.** A razão entre as duas razões de prevalência é {{h36_razao}} (IC 95% {{h36_ic}}). O intervalo é largo: vai de uma associação {{h36_ic_pct_inf}} menor a {{h36_ic_pct_sup}} maior nos EUA.
- **O efeito é pequeno.** Na regressão linear do Vigitel, o tempo de tela acrescenta {{H51_dr2}} ao R², ou {{H51_dr2_pct}} da variação do índice de insônia. Na comparação mundial, a correlação com tempo total de tela é ρ = {{meta_rho_total}}, bem abaixo da meta-análise de referência (r = 0,28). Uso problemático ({{meta_rho_problematico}}) e celular antes de dormir ({{meta_rho_presono}}) se associam mais.
- **Idade confunde.** Sem ajuste, a PNS mostra o contrário: os que mais usam tela relatam menos problema de sono (RP bruta {{rp_bruta_digital_pns2019}}). Isso acontece porque os que mais usam são mais jovens. Ajustada por idade, sexo e escolaridade, a RP vai a {{rp_ajustada_digital_pns2019}}.
- **Os dados não permitem dizer que a tela causa insônia.** São transversais, e a literatura descreve também o caminho inverso: quem não dorme pega o celular.

## 1. Pergunta e motivação

"Insônia digital" não é diagnóstico; aqui designa os problemas de sono associados ao uso de telas, sobretudo à noite. A literatura internacional é ampla, mas quase toda em crianças e adolescentes de países de alta renda. No Brasil, os estudos são locais, e os dois grandes inquéritos nacionais (PNS e Vigitel) perguntam sobre tela e sono, mas não foram analisados com essa pergunta.

O trabalho foi planejado por especificação antes da execução (`specs/`). Cada etapa registrou hipóteses, testes e critérios antes de rodar. As hipóteses da comparação Brasil × EUA foram formuladas depois de uma análise exploratória, e o texto diz isso onde elas aparecem.

## 2. O que a literatura já estabelece

- **A associação é consistente.** Em 67 estudos com crianças e adolescentes, 90% acharam associação adversa entre tela e sono (HALE; GUAN, 2015). Usar dispositivo portátil na hora de dormir se associa a sono insuficiente (OR 2,17) (CARTER et al., 2016).
- **O efeito medido em minutos é pequeno.** Cada hora de tela se associa a 3 a 8 minutos a menos de sono, e a tela explica menos de 2% da variação (PRZYBYLSKI, 2019).
- **O momento pesa mais que o total.** Checar redes sociais nos 30 minutos antes de dormir se associa a perturbação do sono independentemente do uso diário (LEVENSON et al., 2017). Cada hora de tela na cama se associa a OR 1,59 para sintomas de insônia (HJETLAND et al., 2025). No Brasil, tela por 2 h ou mais antes de deitar se associou a 17 minutos a mais de latência (CASTRO-SANTOS et al., 2023).
- **Uso problemático pesa mais que uso geral.** Na meta-análise de referência, o uso geral de mídia se correlaciona com pior qualidade de sono (r = 0,28) e o uso problemático, com mais problemas de sono (r = 0,33) (HAN; ZHOU; LIU, 2024).
- **A relação é bidirecional.** Comparando a mesma pessoa em dias diferentes, a única associação consistente é a da tela com o início mais tardio do sono (BOURKE et al., 2026). E o problema de sono também precede o uso de tela, que funciona como passatempo enquanto o sono não vem (BAUDUCCO et al., 2024).

Detalhes e as 52 referências do levantamento: `docs/estado-da-arte.md`.

## 3. Dados

| Base | País | Desenho | n | Sono | Tela |
|---|---|---|---|---|---|
| PNS 2019 | Brasil | inquérito domiciliar (peso, estrato, UPA) | {{n_pns2019}} | item de sono do PHQ-9 | horas de computador/tablet/celular e de TV |
| Vigitel 2024 | Brasil, 27 capitais | inquérito telefônico (peso) | {{n_vigitel2024}} | 3 sintomas de insônia | idem |
| NHANES 2005-06 | EUA | inquérito (peso, estrato, UPA) | {{n_nhanes0506}} | 3 sintomas de insônia, latência | horas de computador/games e de TV |
| Xuzhou | China | universitários | {{n_xuzhou}} | PSQI | uso problemático de smartphone (SAS-SV) |
| Pérez-Chada | Argentina | adolescentes | {{n_argentina}} | latência (min) | horas de tela por dia e antes de dormir |
| Doomscrolling | Turquia | 18 a 40 anos | {{n_turquia}} | PSQI, latência | escala de doomscrolling |
| Okajima | Japão | 18 a 29 anos | {{n_japao}} | escala de insônia de Atenas (AIS) | celular nas 3 h antes de dormir |

Cada base foi **harmonizada** (spec 001):

- os códigos de "não sabe" e "recusou" viraram faltantes;
- as faixas de horas foram cortadas em 1 h e 3 h nas três bases de inquérito;
- cada variável recebeu um grau de equivalência entre bases (`resultados/001/tabelas/equivalencia.csv`).

Usavam tela digital 3 h ou mais por dia, com peso amostral:

- {{tela3h_pns2019}} dos adultos na PNS 2019;
- {{tela3h_vigitel2024}} no Vigitel 2024;
- {{tela3h_nhanes0506}} no NHANES 2005-06, antes do smartphone.

![Exposição à tela digital por base](../resultados/001/figuras/exposicao_tela_digital.png)

## 4. Métodos

| Técnica | Etapa | Para quê |
|---|---|---|
| PCA por decomposição em valores singulares (Z = UΣVᵀ) | 002 | resumir os itens de cada escala e ver quantas dimensões existem |
| Análise fatorial (máxima verossimilhança, eixos principais; varimax e oblimin) | 002 | separar a variância comum da específica de cada item |
| Análise paralela de Horn, KMO, Bartlett, α de Cronbach | 002 | decidir o número de fatores e a adequação dos itens (HORN, 1965) |
| Congruência de Tucker | 002 | testar se o fator é o mesmo nos dois países (LORENZO-SEVA; TEN BERGE, 2006) |
| Regressão de Poisson com peso e variância por linearização (estrato e UPA) | 003 | razão de prevalências ajustada nos inquéritos |
| Regressão linear múltipla, ANOVA, teste t de Welch | 005 | formato da disciplina; Excel e script |
| Correlação de Spearman com z de Fisher; meta-análise de efeitos aleatórios; Q de Cochran e I² | 004 | pôr as sete bases na mesma escala e medir a heterogeneidade (FIELLER; HARTLEY; PEARSON, 1957; DERSIMONIAN; LAIRD, 1986; HIGGINS; THOMPSON, 2002) |

Regras comuns (`specs/constitution.md`):

- α = 0,05 bilateral, com correção de Holm dentro de cada família de hipóteses.
- Todo teste traz estatística, graus de liberdade, p, tamanho de efeito e IC 95%.
- Nos inquéritos, a decisão usa peso amostral e, quando a base tem, estrato e UPA.
- Estimativas brutas e ajustadas aparecem lado a lado.

## 5. Resultados

### 5.1 O índice de insônia mede a mesma coisa no Brasil e nos EUA (spec 002)

**Insônia.** Os três sintomas (dificuldade para adormecer, para voltar a dormir e acordar cedo demais) formam uma única dimensão nas duas bases. A análise paralela retém uma única componente, que explica {{var_pc1_insonia3_vigitel}} da variância no Vigitel e {{var_pc1_insonia3_nhanes}} no NHANES (α = {{alfa_insonia3_vigitel}} e {{alfa_insonia3_nhanes}}). As cargas são equivalentes entre os países (Tucker φ = {{tucker_insonia}}; o limite de equivalência é 0,95). A soma simples dos três itens correlaciona {{r_soma_pc1_insonia3_vigitel}} com a primeira componente, o que justifica usar o índice 0–12 nas etapas seguintes.

**PHQ-9.** O questionário de depressão tem 1 fator na PNS e no NHANES, com φ = {{tucker_phq9}}. O item de sono carrega nesse fator nos dois países.

**Escalas dos outros países:**

- doomscrolling (Turquia) e insônia de Atenas (Japão): unidimensionais;
- uso problemático de smartphone (China), procrastinação do sono (Turquia) e procrastinação do sono (Japão): 2 dimensões. No Japão, a segunda é a dos itens de redação invertida.

Os escores da PCA e da análise fatorial ordenam as pessoas quase igual: correlação de {{r_pc1_af_min}} a {{r_pc1_af_max}}.

![Cargas do fator de insônia no Brasil e nos EUA](../resultados/002/figuras/cargas_insonia_br_eua.png)

### 5.2 Brasil × EUA: razões de prevalência (spec 003)

Desfecho: dificuldade para adormecer "quase sempre/sempre" no Vigitel, "often/almost always" (5 ou mais vezes por mês) no NHANES, e problema de sono em mais da metade dos dias na PNS. Exposição: tela ≥ 3 h contra < 1 h por dia. Ajuste: faixa etária, sexo e escolaridade.

| Base | Tela digital: RP (IC 95%) | p Holm | TV: RP (IC 95%) | p Holm |
|---|---|---|---|---|
| Vigitel 2024 | {{rp_digital_vigitel2024}} ({{rp_digital_vigitel2024_ic}}) | {{rp_digital_vigitel2024_pholm}} | {{rp_tv_vigitel2024}} ({{rp_tv_vigitel2024_ic}}) | {{rp_tv_vigitel2024_pholm}} |
| PNS 2019 | {{rp_digital_pns2019}} ({{rp_digital_pns2019_ic}}) | {{rp_digital_pns2019_pholm}} | {{rp_tv_pns2019}} ({{rp_tv_pns2019_ic}}) | {{rp_tv_pns2019_pholm}} |
| NHANES 2005-06 | {{rp_digital_nhanes0506}} ({{rp_digital_nhanes0506_ic}}) | {{rp_digital_nhanes0506_pholm}} | {{rp_tv_nhanes0506}} ({{rp_tv_nhanes0506_ic}}) | {{rp_tv_nhanes0506_pholm}} |

- **Bruta × ajustada.** A RP bruta da tela digital é {{rp_bruta_digital_pns2019}} na PNS, {{rp_bruta_digital_vigitel2024}} no Vigitel e {{rp_bruta_digital_nhanes0506}} no NHANES. Na PNS o sinal se inverte depois do ajuste, porque os que mais usam tela são mais jovens e os jovens relatam menos problema de sono.
- **Dose-resposta.** A tendência nas 3 faixas é significativa em {{h34_rejeita}} combinações de base e exposição. A faixa de 1 a 3 h, porém, fica perto da de < 1 h: o excesso aparece em ≥ 3 h, e a relação não é uma reta.
- **Brasil × EUA.** Para tela digital, a razão NHANES ÷ Vigitel das RP é {{h36_razao}} (IC 95% {{h36_ic}}; p Holm {{h36_pholm}}). Entre PNS e Vigitel também não foi detectada diferença (razão {{h39_razao}}, IC 95% {{h39_ic}}; p Holm {{h39_pholm}}), mas as duas usam perguntas diferentes. Nem variação por faixa etária (menor p Holm {{h37_pholm_min}}).
  - Na TV, a razão entre países é {{h36_tv_razao}} (p = {{h36_tv_p}}), mas cai para {{h36_tv_semPeso_razao}} (p = {{h36_tv_semPeso_p}}) sem o peso do NHANES. Essa comparação está fora da família de Holm e não é robusta.

![RP por país](../resultados/003/figuras/rp_por_pais.png)

### 5.3 Regressão linear múltipla, ANOVA e teste t (spec 005)

Mesmo formato do exercício da disciplina (SUMMARY OUTPUT do Excel), com dummies de tela (referência < 1 h) e covariáveis.

Cada hipótese aparece com duas estatísticas. A **sem peso** é a que o Excel calcula, no formato da aula. A **com peso** usa o desenho amostral e é a que decide nos inquéritos (Vigitel e NHANES). Nas bases de repositório não há desenho, e as duas coincidem.

| H | Base | Teste | Coeficiente com peso (IC 95%) | Sem peso (Excel) | Com peso (decisão) | p Holm | Decisão |
|---|---|---|---|---|---|---|---|
| H5.1 | Vigitel | t da tela ≥ 3 h; Y = índice de insônia | {{H51_b}} ({{H51_ic}}) | {{H51_sp}} | {{H51_cp}} | {{H51_pholm}} | {{H51_decisao}} |
| H5.2 | NHANES | idem | {{H52_b}} ({{H52_ic}}) | {{H52_sp}} | {{H52_cp}} | {{H52_pholm}} | {{H52_decisao}} |
| H5.3 | Xuzhou | t do SAS-SV; Y = PSQI | {{H53_b}} por ponto ({{H53_ic}}) | {{H53_sp}} | {{H53_cp}} | {{H53_pholm}} | {{H53_decisao}} |
| H5.4 | Argentina | t da tela antes de dormir; Y = latência (min) | {{H54_b}} min por hora ({{H54_ic}}) | {{H54_sp}} | {{H54_cp}} | {{H54_pholm}} | {{H54_decisao}} |
| H5.5 | Turquia | t do doomscrolling; Y = latência (min) | {{H55_b}} min por ponto ({{H55_ic}}) | {{H55_sp}} | {{H55_cp}} | {{H55_pholm}} | {{H55_decisao}} |
| H5.6 | Japão | t do celular antes de dormir; Y = AIS | {{H56_b}} ponto por hora ({{H56_ic}}) | {{H56_sp}} | {{H56_cp}} | {{H56_pholm}} | {{H56_decisao}} |
| H5.7 | Vigitel | ANOVA de um fator, 3 faixas | — | {{H57_sp}} | {{H57_cp}} (Wald) | {{H57_pholm}} | {{H57_decisao}} |
| H5.8 | NHANES | ANOVA de um fator, 3 faixas | — | {{H58_sp}} | {{H58_cp}} (Wald) | {{H58_pholm}} | {{H58_decisao}} |
| H5.9 | Vigitel | t de Welch, ≥ 3 h × < 1 h | diferença {{H59_b}} ({{H59_ic}}) | {{H59_sp}} (Welch) | {{H59_cp}} (média ponderada) | {{H59_pholm}} | {{H59_decisao}} |
| H5.10 | NHANES | t de Welch, ≥ 3 h × < 1 h | diferença {{H510_b}} ({{H510_ic}}) | {{H510_sp}} (Welch) | {{H510_cp}} (média ponderada) | {{H510_pholm}} | {{H510_decisao}} |
| H5.11 | Vigitel + NHANES | F parcial da interação país × tela | {{H511_b}} ({{H511_ic}}) | {{H511_sp}} | {{H511_cp}} | {{H511_pholm}} | {{H511_decisao}} |

**Pontos de leitura:**

- **O peso amostral muda as conclusões no NHANES.** Sem peso, como o Excel calcula, H5.2 teria p = {{H52_p_sempeso}}. Com o desenho amostral (só {{nhanes_estratos}} estratos e {{nhanes_upas}} UPAs, {{nhanes_gl}} gl), o intervalo alarga e o p vai a {{H52_p}}. Na regra do `svyglm`, p = {{H52_p_svyglm}}, e sem as observações influentes, p = {{H52_p_seminfl}}; a decisão não muda.
- **Significativo não quer dizer grande.** No Vigitel, a tela acrescenta {{H51_dr2}} ao R² e a diferença de médias tem d de Cohen = {{H59_efeito}}. Em Xuzhou, o uso problemático acrescenta {{H53_dr2}}.
- **Dois resultados são frágeis:**
  - Na Argentina, o sinal é o contrário do esperado (mais tela, menos latência) e some quando a série escolar substitui a idade (p = {{H54_p_serie}}).
  - Na Turquia, a associação some sem as observações influentes (p = {{H55_p_seminfl}}).
- **Conferência dos p-valores.** A ferramenta Análise de Dados do Excel foi executada de verdade, por automação. Cada número (coeficiente, erro padrão, t, p, F, R²) foi comparado por três caminhos: saída do Excel, fórmula no Excel e script. Foram {{conf_n}} comparações: {{conf_dentro}} dentro da tolerância (diferença relativa < 1e-8) e {{conf_excecoes}} exceções documentadas. Entre fórmula e script, a maior diferença relativa foi {{conf_max_B}}, e entre Excel e script, {{conf_max_A}}. As exceções (diferença {{conf_max_A_exc}}) vêm do teste t de Welch: o Excel arredonda o grau de liberdade para inteiro, e o relatório usa o fracionário.

![Efeitos padronizados](../resultados/005/figuras/efeitos_padronizados.png)

### 5.4 O Brasil no mundo (spec 004)

Correlação de Spearman entre exposição e escore de sono em cada base (positivo = mais tela, pior sono):

| Base | Tipo de exposição | ρ (IC 95%) |
|---|---|---|
| PNS 2019 | tempo total | {{rho_pns2019}} ({{rho_pns2019_ic}}) |
| Vigitel 2024 | tempo total | {{rho_vigitel2024}} ({{rho_vigitel2024_ic}}) |
| NHANES 2005-06 | tempo total | {{rho_nhanes0506}} ({{rho_nhanes0506_ic}}) |
| Argentina | tempo total | {{rho_argentina}} ({{rho_argentina_ic}}) |
| Japão | celular antes de dormir | {{rho_japao}} ({{rho_japao_ic}}) |
| China (Xuzhou) | uso problemático | {{rho_xuzhou}} ({{rho_xuzhou_ic}}) |
| Turquia | uso problemático (doomscrolling) | {{rho_turquia}} ({{rho_turquia_ic}}) |

Resultados da meta-análise de efeitos aleatórios:

- **Estimativa global:** ρ = {{meta_rho}}. Pelo IC de DerSimonian-Laird ({{meta_rho_ic}}; p = {{meta_p_dl}}), fica acima de zero. Pelo IC de Hartung-Knapp, mais adequado com só 7 bases ({{meta_rho_ic_hk}}; p = {{meta_p_hk}}), não se distingue de zero.
- **H4.1, heterogeneidade:** enorme e significativa (Q = {{meta_Q}}, gl = {{meta_glQ}}, p {{meta_pQ}}; I² = {{meta_I2}}).
- **H4.2, tipo de exposição:** a ordem é a da literatura, tempo total {{meta_rho_total}} < pré-sono {{meta_rho_presono}} < uso problemático {{meta_rho_problematico}}. A diferença entre os subgrupos não é significativa (Q = {{H42_Q}}, p Holm {{H42_pholm}}), com só 1 a 4 bases por subgrupo.
- **H4.3, Brasil × outros países com tempo total:** sem diferença. O Brasil (PNS + Vigitel) tem ρ = {{meta_rho_brasil}} e os outros, {{meta_rho_outros}} (z = {{H43_z}}, p Holm {{H43_pholm}}).
- **H4.4, comparação com a meta-análise de referência:** o tempo total combinado ({{meta_rho_total}}) fica fora do intervalo 0,21–0,35 de Han, Zhou e Liu (2024), e o teste de equivalência não rejeita H0 (p Holm {{H44_pholm}}). A associação com tempo total, nos nossos dados, é muito menor que a da literatura.
- **Desenho amostral (deff):** as correlações dos inquéritos foram calculadas sem o desenho amostral. Multiplicando a variância pelo deff de Kish (PNS {{deff_pns2019}}, Vigitel {{deff_vigitel2024}}, NHANES {{deff_nhanes0506}}), a estimativa global fica {{meta_deff_rho}} ({{meta_deff_ic}}) e o I², {{meta_deff_I2}}. Nenhuma decisão muda.
- **Ajuste por idade:** a PNS passa de {{rho_pns2019}} para {{rho_aj_pns2019}}, e o tempo total combinado, de {{meta_rho_total}} para {{rho_aj_total}} ({{rho_aj_total_ic}}).

![Gráfico de floresta](../resultados/004/figuras/floresta.png)

## 6. Discussão

**Tamanho.** A associação entre tela e problema de sono aparece nos dois países e na maioria das bases, mas é pequena. Os grandes inquéritos detectam com folga efeitos sem importância prática. Esse é o padrão descrito por Przybylski (2019): efeitos consistentes, que explicam poucos por cento da variação. As razões de prevalência entre {{rp_digital_min}} e {{rp_digital_max}} descrevem um grupo extremo (≥ 3 h) contra o de baixo uso. Por hora de tela ou por desvio-padrão, o efeito é modesto.

**Não foi detectada diferença entre Brasil e EUA.** Isso vale para a razão de prevalências (003), o coeficiente da regressão (005) e a correlação (004). Ausência de diferença detectada não é prova de igualdade: o IC de H3.6 vai de {{h36_ic}}, porque o desenho do NHANES 2005-06 tem só {{nhanes_estratos}} estratos.

A comparabilidade também é parcial:

- o desfecho é equivalente (002), mas com âncoras de frequência diferentes;
- a exposição é computador e games em 2005 contra celular em 2024;
- a congruência de Tucker mostra cargas parecidas, mas não testa invariância formal.

**O que importa é o tipo de uso.** As maiores correlações vieram do uso problemático (China) e do celular nas horas antes de dormir (Japão), não do tempo total. Isso concorda com Han, Zhou e Liu (2024), com Levenson et al. (2017) e com Hjetland et al. (2025). Mas cada subgrupo tem uma ou duas bases, e o teste não confirma a diferença.

**Confundimento.** A inversão do sinal na PNS mostra que a idade confunde a relação: jovens usam mais tela e relatam menos problema de sono. Uma comparação sem ajuste levaria à conclusão oposta.

## 7. Limitações

- **Dados transversais.** Não dá para separar "tela piora o sono" de "quem dorme mal usa mais tela" (BAUDUCCO et al., 2024).
- **NHANES 2005-06 é de antes do smartphone.** A comparação Brasil × EUA mistura país e época, e o Vigitel cobre só as capitais.
- **O item de sono da PNS é outro.** É o do PHQ-9 (inclui dormir demais) e só é comparável de forma aproximada.
- **Medidas autorrelatadas e em faixas.** Isso atenua as correlações.
- **Bases de repositório sem desenho amostral.**
  - Sexo sem rótulo em Xuzhou e no Japão.
  - Rótulo da escala da Turquia inferido, sem dicionário.
  - {{n_arg_sem_idade}} adolescentes argentinos sem idade.
- **Graus de liberdade do NHANES.** O projeto usa gl = UPAs − estratos ({{nhanes_gl}}) em todas as specs. A regra do `svyglm` do R desconta os parâmetros do modelo ({{h33_gl_svyglm}} gl na H3.3). Por essa regra, a H3.3 deixaria de rejeitar H0: p Holm {{h33_pholm_svyglm}}, contra {{rp_digital_nhanes0506_pholm}}. As demais decisões não mudam (`resultados/003/tabelas/hipoteses.csv`, colunas `*_svyglm`).
- **Tucker não é um teste formal de invariância.** A análise fatorial confirmatória multigrupo ficou fora do escopo.

## 8. Conclusões

1. Em adultos brasileiros, usar tela digital no lazer 3 h ou mais por dia se associa a uma prevalência de problema de sono {{rp_br_pct_min}} a {{rp_br_pct_max}} maior, depois de ajustar por idade, sexo e escolaridade. Não foi detectada diferença entre as duas pesquisas nacionais.
2. Nos EUA (2005-06) a associação tem a mesma direção. Não foi detectada diferença entre os países, com intervalo largo ({{h36_ic}}).
3. O efeito é pequeno: no Vigitel, o tempo de tela explica {{H51_dr2_pct}} da variação do índice de insônia.
4. Uso problemático e uso antes de dormir se associam mais ao sono que o tempo total, como diz a literatura. Com tão poucas bases, a diferença não foi confirmada.
5. Sem ajuste por idade a conclusão se inverte. Comparações entre grupos de uso de tela precisam sempre de ajuste.
6. Os dados são transversais. O resultado é uma associação; mostrar causa exigiria estudo longitudinal ou experimental.

## 9. Como conferir

```bash
export STAT4_BRUTOS=/caminho/para/pesquisa/dados
python -m analise.rodar_tudo
python -m pytest
```

Cada etapa tem:

- uma spec com as hipóteses (`specs/00N-*/spec.md`);
- um notebook executado (`analise/notebooks/`);
- um resumo (`resultados/00N/RESUMO.md`);
- uma explicação didática (`docs/explicacoes/`).

## Referências

BAUDUCCO, S. et al. A bidirectional model of sleep and technology use: A theoretical review of How much, for whom, and which mechanisms. **Sleep Medicine Reviews**, v. 76, p. 101933, 2024. DOI: https://doi.org/10.1016/j.smrv.2024.101933.

BOURKE, M. et al. Within-Person Association Between Daily Screen Use and Sleep in Youth: A Systematic Review and Meta-Analysis. **JAMA Pediatrics**, v. 180, n. 5, p. 500, 2026. DOI: https://doi.org/10.1001/jamapediatrics.2025.6490.

CARTER, B. et al. Association Between Portable Screen-Based Media Device Access or Use and Sleep Outcomes: A Systematic Review and Meta-analysis. **JAMA Pediatrics**, v. 170, n. 12, p. 1202, 2016. DOI: https://doi.org/10.1001/jamapediatrics.2016.2341.

CASTRO-SANTOS, L. et al. Sleep and circadian hygiene practices association with sleep quality among Brazilian adults. **Sleep Medicine: X**, v. 6, p. 100088, 2023. DOI: https://doi.org/10.1016/j.sleepx.2023.100088.

DERSIMONIAN, R.; LAIRD, N. Meta-analysis in clinical trials. **Controlled Clinical Trials**, v. 7, n. 3, p. 177-188, 1986. DOI: https://doi.org/10.1016/0197-2456(86)90046-2.

FIELLER, E. C.; HARTLEY, H. O.; PEARSON, E. S. Tests for rank correlation coefficients. I. **Biometrika**, v. 44, n. 3-4, p. 470-481, 1957. DOI: https://doi.org/10.1093/biomet/44.3-4.470.

HALE, L.; GUAN, S. Screen time and sleep among school-aged children and adolescents: A systematic literature review. **Sleep Medicine Reviews**, v. 21, p. 50-58, 2015. DOI: https://doi.org/10.1016/j.smrv.2014.07.007.

HAN, X.; ZHOU, E.; LIU, D. Electronic Media Use and Sleep Quality: Updated Systematic Review and Meta-Analysis. **Journal of Medical Internet Research**, v. 26, p. e48356, 2024. DOI: https://doi.org/10.2196/48356.

HIGGINS, J. P. T.; THOMPSON, S. G. Quantifying heterogeneity in a meta-analysis. **Statistics in Medicine**, v. 21, n. 11, p. 1539-1558, 2002. DOI: https://doi.org/10.1002/sim.1186.

HJETLAND, G. J. et al. How and when screens are used: comparing different screen activities and sleep in Norwegian university students. **Frontiers in Psychiatry**, v. 16, 1548273, 2025. DOI: https://doi.org/10.3389/fpsyt.2025.1548273.

HORN, J. L. A rationale and test for the number of factors in factor analysis. **Psychometrika**, v. 30, n. 2, p. 179-185, 1965. DOI: https://doi.org/10.1007/BF02289447.

LEVENSON, J. C. et al. Social Media Use Before Bed and Sleep Disturbance Among Young Adults in the United States: A Nationally Representative Study. **Sleep**, v. 40, n. 9, zsx113, 2017. DOI: https://doi.org/10.1093/sleep/zsx113.

LORENZO-SEVA, U.; TEN BERGE, J. M. F. Tucker's congruence coefficient as a meaningful index of factor similarity. **Methodology**, v. 2, n. 2, p. 57-64, 2006. DOI: https://doi.org/10.1027/1614-2241.2.2.57.

PRZYBYLSKI, A. K. Digital Screen Time and Pediatric Sleep: Evidence from a Preregistered Cohort Study. **The Journal of Pediatrics**, v. 205, p. 218-223.e1, 2019. DOI: https://doi.org/10.1016/j.jpeds.2018.09.054.
