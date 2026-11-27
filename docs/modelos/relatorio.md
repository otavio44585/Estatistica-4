# Insônia digital: uso de telas e sono no Brasil e em outros quatro países

Estatística 4 · ESEG · Relatório gerado em {{data}} por `analise/relatorio/relatorio.py`. Todos os resultados próprios deste texto (estimativas, IC, p, n) saem de arquivos em `resultados/` e `analise/dados/logs/`, lidos pelo script; nenhum foi digitado à mão. Números da literatura vêm das fontes citadas. Revisão do grupo pendente.

> **Mudança de escopo em 2026-11-27: os EUA saíram do trabalho.** A única base americana (NHANES 2005-06) é de antes do smartphone, e o tempo de tela daquela época não é comparável com o de 2019–2024. O grupo decidiu retirá-la **depois de ver os resultados** que a incluíam. As hipóteses que dependiam dela foram retiradas, com a numeração original mantida, e o registro está no Histórico de cada spec (001 a 005). A decisão é contada aqui por transparência: uma escolha feita depois de ver os dados merece desconfiança, e quem quiser conferir encontra no histórico do git a versão com os EUA.

## Resumo

- **Pergunta.** No Brasil, adultos que usam mais telas no lazer relatam mais problema de sono? As duas pesquisas nacionais (PNS 2019 e Vigitel 2024) concordam? E onde o Brasil fica frente ao resto do mundo (China, Argentina, Turquia, Japão) e à literatura?
- **Dados.** {{n_total}} pessoas em seis bases abertas: {{n_brasil}} ({{pct_n_brasil}}) nas duas pesquisas brasileiras e {{n_mundo}} em amostras da China, Argentina, Turquia e Japão.
- **A associação aparece nas duas pesquisas.** Quem usa computador, tablet ou celular 3 h ou mais por dia tem prevalência de problema de sono frequente {{rp_digital_vigitel2024}} vez a de quem usa menos de 1 h no Vigitel e {{rp_digital_pns2019}} vez na PNS. São razões de prevalência ajustadas por idade, sexo e escolaridade (p Holm {{rp_digital_vigitel2024_pholm}} no Vigitel e {{rp_digital_pns2019_pholm}} na PNS).
- **As duas pesquisas concordam.** Não foi detectada diferença entre elas: a razão entre as duas razões de prevalência é {{h39_razao}} (IC 95% {{h39_ic}}; p Holm {{h39_pholm}}), mesmo com perguntas de sono diferentes.
- **O efeito é pequeno.** A tela explica {{r2u_vigitel2024_tela}} da variação do índice de insônia no Vigitel e {{r2u_pns2019_tela}} da do problema de sono na PNS. É menos que o sexo nas duas pesquisas e, na PNS, menos que a idade.
- **A idade confunde.** Sem ajuste, a PNS mostra o contrário: os que mais usam tela relatam menos problema de sono (RP bruta {{rp_bruta_digital_pns2019}}). Quem mais usa tela é jovem ({{pns_tela3h_18_29}} dos adultos de 18 a 29 anos usam 3 h ou mais, contra {{pns_tela3h_60mais}} dos de 60 ou mais), e os jovens relatam menos problema de sono ({{pns_sono_18_29}} contra {{pns_sono_60mais}}). Ajustada, a RP vai a {{rp_ajustada_digital_pns2019}}.
- **O Brasil no mundo.** Combinadas, as duas pesquisas brasileiras dão correlação ρ = {{meta_rho_brasil}}; as quatro bases dos outros países, ρ = {{meta_rho_resto}}. Não foi detectada diferença (análise exploratória, p = {{brasil_resto_p}}). Com tempo total de tela, a correlação (ρ = {{meta_rho_total}}) fica bem abaixo da meta-análise de referência (r = 0,28); uso problemático ({{meta_rho_problematico}}) e celular antes de dormir ({{meta_rho_presono}}) se associam mais.
- **Os dados não permitem dizer que a tela causa insônia.** São transversais, e a literatura descreve também o caminho inverso: quem não dorme pega o celular.

## 1. Pergunta e motivação

"Insônia digital" não é diagnóstico; aqui designa os problemas de sono associados ao uso de telas, sobretudo à noite. A literatura internacional é ampla, mas quase toda em crianças e adolescentes de países de alta renda. No Brasil, os estudos são locais, e os dois grandes inquéritos nacionais (PNS e Vigitel) perguntam sobre tela e sono, mas não foram analisados com essa pergunta.

Três perguntas guiam o trabalho:

1. Nas duas pesquisas nacionais, quem usa mais tela relata mais problema de sono, depois de ajustar por idade, sexo e escolaridade?
2. As duas pesquisas chegam ao mesmo tamanho de associação?
3. Onde o Brasil fica frente a outros países (China, Argentina, Turquia, Japão) e à literatura?

O trabalho foi planejado por especificação antes da execução (`specs/`). Cada etapa registrou hipóteses, testes e critérios antes de rodar. As hipóteses das pesquisas brasileiras foram formuladas depois de uma análise exploratória, e a comparação do Brasil com o resto do mundo foi pedida depois de ver os resultados; o texto diz isso onde elas aparecem.

## 2. O que a literatura já estabelece

- **A associação é consistente.** Em 67 estudos com crianças e adolescentes, 90% acharam associação adversa entre tela e sono (HALE; GUAN, 2015). Usar dispositivo portátil na hora de dormir se associa a sono insuficiente (OR 2,17) (CARTER et al., 2016).
- **O tamanho, medido em minutos, é pequeno.** Cada hora de tela se associa a 3 a 8 minutos a menos de sono, e a tela explica menos de 2% da variação (PRZYBYLSKI, 2019).
- **O momento pesa mais que o total.** Checar redes sociais nos 30 minutos antes de dormir se associa a perturbação do sono independentemente do uso diário (LEVENSON et al., 2017). Cada hora de tela na cama se associa a OR 1,59 para sintomas de insônia (HJETLAND et al., 2025). No Brasil, tela por 2 h ou mais antes de deitar se associou a 17 minutos a mais de latência (CASTRO-SANTOS et al., 2023).
- **Uso problemático pesa mais que uso geral.** Na meta-análise de referência, o uso geral de mídia se correlaciona com pior qualidade de sono (r = 0,28) e o uso problemático, com mais problemas de sono (r = 0,33) (HAN; ZHOU; LIU, 2024).
- **A relação é bidirecional.** Comparando a mesma pessoa em dias diferentes, a única associação consistente é a da tela com o início mais tardio do sono (BOURKE et al., 2026). E o problema de sono também precede o uso de tela, que funciona como passatempo enquanto o sono não vem (BAUDUCCO et al., 2024).

Detalhes e as 52 referências do levantamento: `docs/estado-da-arte.md`.

## 3. Dados

| Base | País | Desenho | n | Sono | Tela |
|---|---|---|---|---|---|
| PNS 2019 | Brasil | inquérito domiciliar nacional (peso, estrato, UPA) | {{n_pns2019}} | problema de sono nas últimas 2 semanas (item do PHQ-9) | horas de computador/tablet/celular e de TV no lazer |
| Vigitel 2024 | Brasil, 27 capitais | inquérito telefônico (peso) | {{n_vigitel2024}} | 3 sintomas de insônia | idem |
| Xuzhou | China | universitários | {{n_xuzhou}} | PSQI | uso problemático de smartphone (SAS-SV) |
| Pérez-Chada | Argentina | adolescentes | {{n_argentina}} | latência (min) | horas de tela por dia e antes de dormir |
| Doomscrolling | Turquia | 18 a 40 anos | {{n_turquia}} | PSQI, latência | escala de doomscrolling |
| Okajima | Japão | 18 a 29 anos | {{n_japao}} | escala de insônia de Atenas (AIS) | celular nas 3 h antes de dormir |

O Brasil responde por {{pct_n_brasil}} das pessoas analisadas. As quatro bases dos outros países ({{n_mundo}} pessoas) são amostras de conveniência de jovens, publicadas em repositórios abertos, sem peso amostral.

Cada base foi **harmonizada** (spec 001):

- os códigos de "não sabe" e "recusou" viraram faltantes;
- as faixas de horas de tela foram cortadas em 1 h e 3 h nas duas pesquisas brasileiras;
- cada variável recebeu um grau de equivalência entre bases (`resultados/001/tabelas/equivalencia.csv`).

Com peso amostral, usavam tela digital 3 h ou mais por dia {{tela3h_pns2019}} dos adultos na PNS 2019 e {{tela3h_vigitel2024}} no Vigitel 2024. Relatavam problema de sono em mais da metade dos dias {{prev_sono_pns2019}} na PNS, e dificuldade para adormecer quase sempre ou sempre {{prev_adormecer_vigitel2024}} no Vigitel.

![Exposição à tela digital por base](../resultados/001/figuras/exposicao_tela_digital.png)

## 4. Métodos

| Técnica | Etapa | Para quê |
|---|---|---|
| PCA por decomposição em valores singulares (Z = UΣVᵀ) | 002 | resumir os itens de cada escala e ver quantas dimensões existem |
| Análise fatorial (máxima verossimilhança, eixos principais; varimax e oblimin) | 002 | separar a variância comum da específica de cada item |
| Análise paralela de Horn, KMO, Bartlett, α de Cronbach | 002 | decidir o número de fatores e a adequação dos itens (HORN, 1965) |
| Regressão de Poisson com peso e variância por linearização (estrato e UPA) | 003 | razão de prevalências (RP) ajustada nas duas pesquisas |
| Regressão linear múltipla, ANOVA, teste t de Welch | 005 | formato da disciplina; Excel e script |
| Decomposição do R² (quanto o R² cai quando cada fator sai do modelo) | 006 | comparar o peso da tela com o da idade, do sexo e da escolaridade |
| Correlação de Spearman com z de Fisher; meta-análise de efeitos aleatórios (DerSimonian-Laird e Hartung-Knapp); Q de Cochran e I² | 004 | pôr as seis bases na mesma escala e medir a heterogeneidade (FIELLER; HARTLEY; PEARSON, 1957; DERSIMONIAN; LAIRD, 1986; HIGGINS; THOMPSON, 2002) |

Regras comuns (`specs/constitution.md`):

- **Teste de hipótese.** Cada hipótese tem H0 (não há associação ou não há diferença), H1 bilateral, α = 0,05, uma estatística (z, t, F, χ² ou Q) com seus graus de liberdade e um p-valor. Rejeita-se H0 quando o p, já corrigido, fica abaixo de 0,05.
- **Correção de Holm** dentro de cada família de hipóteses: mantém em no máximo 5% a chance de pelo menos um falso positivo na família. Todo p de decisão aparece também na versão corrigida ("p Holm").
- Todo teste traz estatística, graus de liberdade, p, tamanho de efeito e IC 95%.
- **Desenho amostral.** Nas pesquisas brasileiras, a decisão usa o peso amostral e, na PNS, também estrato e UPA. Os graus de liberdade da PNS seguem a regra única do projeto, UPAs − estratos ({{pns_gl}} gl); pela regra do `svyglm` do R, que desconta os parâmetros do modelo, nenhuma decisão muda. Testes de várias restrições ao mesmo tempo usam a correção de Korn-Graubard. O Vigitel não divulga estrato nem UPA: a variância usa só o peso.
- Estimativas brutas e ajustadas aparecem lado a lado.

## 5. Resultados

### 5.1 O índice de insônia do Vigitel mede uma coisa só (spec 002)

**Insônia no Vigitel.** As três perguntas de insônia, respondidas de "nunca" a "sempre" (0 a 4), formam uma única dimensão. A análise paralela retém {{fatores_insonia3_vigitel}} componente, que explica {{var_pc1_insonia3_vigitel}} da variância (α de Cronbach = {{alfa_insonia3_vigitel}}; KMO = {{kmo_insonia3_vigitel}}). A soma dos três itens, de 0 a 12, correlaciona {{r_soma_pc1_insonia3_vigitel}} com a primeira componente, o que justifica usar o índice 0–12 nas etapas seguintes.

| Pergunta | Média (0–4) | Carga na PCA | Carga na AF | α sem o item |
|---|---|---|---|---|
| {{vig_item1_rotulo}} (`{{vig_item1_variavel_vigitel}}`) | {{vig_item1_media}} | {{vig_item1_carga_pc1}} | {{vig_item1_carga_af1_ml}} | {{vig_item1_alfa_sem_item}} |
| {{vig_item2_rotulo}} (`{{vig_item2_variavel_vigitel}}`) | {{vig_item2_media}} | {{vig_item2_carga_pc1}} | {{vig_item2_carga_af1_ml}} | {{vig_item2_alfa_sem_item}} |
| {{vig_item3_rotulo}} (`{{vig_item3_variavel_vigitel}}`) | {{vig_item3_media}} | {{vig_item3_carga_pc1}} | {{vig_item3_carga_af1_ml}} | {{vig_item3_alfa_sem_item}} |

**PHQ-9 na PNS.** O questionário de depressão tem {{fatores_phq9_pns}} fator (α = {{alfa_phq9_pns}}; KMO = {{kmo_phq9_pns}}; {{var_pc1_phq9_pns}} da variância na primeira componente). Numa solução exploratória de 2 fatores, o item de sono fica com o cansaço (fator somático), separado do humor deprimido.

**Escalas dos outros países:**

- doomscrolling (Turquia) e insônia de Atenas (Japão): unidimensionais;
- uso problemático de smartphone (China), procrastinação do sono (Turquia) e procrastinação do sono (Japão): 2 dimensões. No Japão, a segunda é a dos itens de redação invertida.

Os escores da PCA e da análise fatorial ordenam as pessoas quase igual: correlação de {{r_pc1_af_min}} a {{r_pc1_af_max}}.

![Cargas do fator de insônia no Vigitel](../resultados/002/figuras/cargas_insonia_vigitel.png)

### 5.2 Brasil: tela e sono nas duas pesquisas nacionais (spec 003)

Desfecho: dificuldade para adormecer "quase sempre" ou "sempre" no Vigitel e problema de sono em mais da metade dos dias na PNS. Exposição: tela ≥ 3 h contra < 1 h por dia. Ajuste: faixa etária, sexo e escolaridade.

**Como ler um teste de hipótese.** Na H3.1, H0 diz que a razão de prevalências é 1 (a tela não muda a prevalência de problema de sono). Se H0 fosse verdadeira, a estatística z seguiria a curva da figura, e só 5% das vezes cairia além de ±1,96 (α = 0,05, bilateral). O z observado no Vigitel é {{rp_digital_vigitel2024_est}}, muito além do limite: p {{rp_digital_vigitel2024_p}}, e p Holm {{rp_digital_vigitel2024_pholm}} depois da correção. Rejeita-se H0.

![Um teste de hipótese desenhado: H3.1 no Vigitel](../resultados/006/figuras/teste_explicado.png)

**Família 1: a associação em cada pesquisa** (H0: RP = 1; α = 0,05 bilateral; Holm por exposição)

| H | Base | Exposição | RP ajustada (IC 95%) | Estatística | p | p Holm | Decisão |
|---|---|---|---|---|---|---|---|
| H3.1 | Vigitel 2024 | tela digital | {{rp_digital_vigitel2024}} ({{rp_digital_vigitel2024_ic}}) | z = {{rp_digital_vigitel2024_est}} | {{rp_digital_vigitel2024_p}} | {{rp_digital_vigitel2024_pholm}} | {{rp_digital_vigitel2024_decisao}} |
| H3.2 | PNS 2019 | tela digital | {{rp_digital_pns2019}} ({{rp_digital_pns2019_ic}}) | t({{pns_gl}}) = {{rp_digital_pns2019_est}} | {{rp_digital_pns2019_p}} | {{rp_digital_pns2019_pholm}} | {{rp_digital_pns2019_decisao}} |
| H3.1 | Vigitel 2024 | TV | {{rp_tv_vigitel2024}} ({{rp_tv_vigitel2024_ic}}) | z = {{rp_tv_vigitel2024_est}} | {{rp_tv_vigitel2024_p}} | {{rp_tv_vigitel2024_pholm}} | {{rp_tv_vigitel2024_decisao}} |
| H3.2 | PNS 2019 | TV | {{rp_tv_pns2019}} ({{rp_tv_pns2019_ic}}) | t({{pns_gl}}) = {{rp_tv_pns2019_est}} | {{rp_tv_pns2019_p}} | {{rp_tv_pns2019_pholm}} | {{rp_tv_pns2019_decisao}} |

![RP nas duas pesquisas brasileiras](../resultados/003/figuras/rp_por_pais.png)

- **Dose-resposta (H3.4).** O teste de tendência nas 3 faixas rejeita H0 em {{h34_rejeita}} combinações de pesquisa e exposição. A faixa de 1 a 3 h, porém, fica perto da de < 1 h: o excesso aparece em ≥ 3 h, e a relação não é uma reta.
- **Família 2: as duas pesquisas concordam?** {{fam2_rejeita}} hipóteses rejeitam H0 depois de Holm.
  - **PNS × Vigitel (H3.9).** H0: as duas RP são iguais. A razão Vigitel ÷ PNS é {{h39_razao}} (IC 95% {{h39_ic}}); z = {{h39_z}}, p = {{h39_p}}, p Holm {{h39_pholm}}: {{h39_decisao}}. Não foi detectada diferença entre as pesquisas. Isso não prova que sejam iguais: elas usam perguntas de sono diferentes, e o intervalo é largo.
  - **Faixa etária (H3.7)** e **TV × tela digital (H3.8):** não foi detectada diferença (menores p Holm {{h37_pholm_min}} e {{h38_pholm_min}}).

**Confundimento por idade.** Na PNS, a RP bruta da tela digital é {{rp_bruta_digital_pns2019}} ({{rp_bruta_digital_pns2019_ic}}): sem ajuste, quem usa mais tela relata *menos* problema de sono. A figura mostra o motivo. Entre os adultos de 18 a 29 anos, {{pns_tela3h_18_29}} usam tela digital 3 h ou mais e {{pns_sono_18_29}} relatam problema de sono; aos 60 ou mais, {{pns_tela3h_60mais}} e {{pns_sono_60mais}}. A idade anda junto com as duas variáveis, em sentidos opostos. Ajustada por idade, sexo e escolaridade, a RP vai a {{rp_ajustada_digital_pns2019}} ({{rp_ajustada_digital_pns2019_ic}}). No Vigitel a mudança é pequena: {{rp_bruta_digital_vigitel2024}} bruta e {{rp_ajustada_digital_vigitel2024}} ajustada.

![Confundimento por idade na PNS 2019](../resultados/006/figuras/confundimento_idade.png)

### 5.3 Regressão linear múltipla, ANOVA e teste t (spec 005)

Mesmo formato do exercício da disciplina (SUMMARY OUTPUT do Excel), com dummies de tela (referência < 1 h) e covariáveis. Em cada hipótese, H0 diz que o coeficiente da tela é zero (ou que as médias das faixas são iguais); α = 0,05 bilateral, com Holm dentro de cada família (R1: H5.1, H5.3 a H5.6; R2: H5.7 e H5.9).

Cada hipótese aparece com duas estatísticas. A **sem peso** é a que o Excel calcula, no formato da aula. A **com peso** usa o desenho amostral e é a que decide no Vigitel. Nas bases de repositório não há desenho, e as duas coincidem.

| H | Base | Teste | Coeficiente com peso (IC 95%) | Sem peso (Excel) | Com peso (decisão) | p | p Holm | Decisão |
|---|---|---|---|---|---|---|---|---|
| H5.1 | Vigitel | t da tela ≥ 3 h; Y = índice de insônia | {{H51_b}} ({{H51_ic}}) | {{H51_sp}} | {{H51_cp}} | {{H51_p}} | {{H51_pholm}} | {{H51_decisao}} |
| H5.3 | Xuzhou | t do SAS-SV; Y = PSQI | {{H53_b}} por ponto ({{H53_ic}}) | {{H53_sp}} | {{H53_cp}} | {{H53_p}} | {{H53_pholm}} | {{H53_decisao}} |
| H5.4 | Argentina | t da tela antes de dormir; Y = latência (min) | {{H54_b}} min por hora ({{H54_ic}}) | {{H54_sp}} | {{H54_cp}} | {{H54_p}} | {{H54_pholm}} | {{H54_decisao}} |
| H5.5 | Turquia | t do doomscrolling; Y = latência (min) | {{H55_b}} min por ponto ({{H55_ic}}) | {{H55_sp}} | {{H55_cp}} | {{H55_p}} | {{H55_pholm}} | {{H55_decisao}} |
| H5.6 | Japão | t do celular antes de dormir; Y = AIS | {{H56_b}} ponto por hora ({{H56_ic}}) | {{H56_sp}} | {{H56_cp}} | {{H56_p}} | {{H56_pholm}} | {{H56_decisao}} |
| H5.7 | Vigitel | ANOVA de um fator, 3 faixas | — | {{H57_sp}} | {{H57_cp}} (Wald) | {{H57_p}} | {{H57_pholm}} | {{H57_decisao}} |
| H5.9 | Vigitel | t de Welch, ≥ 3 h × < 1 h | diferença {{H59_b}} ({{H59_ic}}) | {{H59_sp}} (Welch) | {{H59_cp}} (média ponderada) | {{H59_p}} | {{H59_pholm}} | {{H59_decisao}} |

H5.2, H5.8, H5.10 e H5.11 usavam o NHANES e foram retiradas com os EUA.

**Pontos de leitura:**

- **Significativo não quer dizer grande.** No Vigitel, a tela acrescenta {{H51_dr2}} ao R² e a diferença de médias tem d de Cohen = {{H59_efeito}}. Em Xuzhou, o uso problemático acrescenta {{H53_dr2}}.
- **Dois resultados são frágeis:**
  - Na Argentina, o sinal é o contrário do esperado (mais tela, menos latência) e some quando a série escolar substitui a idade (p = {{H54_p_serie}}).
  - Na Turquia, a associação some sem as observações influentes (p = {{H55_p_seminfl}}).
- **Conferência dos p-valores.** A ferramenta Análise de Dados do Excel foi executada de verdade, por automação. Cada número (coeficiente, erro padrão, t, p, F, R²) foi comparado por três caminhos: saída do Excel, fórmula no Excel e script. Foram {{conf_n}} comparações: {{conf_dentro}} dentro da tolerância (diferença relativa < 1e-8) e {{conf_excecoes}} exceções documentadas. Entre fórmula e script, a maior diferença relativa foi {{conf_max_B}}, e entre Excel e script, {{conf_max_A}}. A exceção (diferença {{conf_max_A_exc}}) vem do teste t de Welch: o Excel arredonda o grau de liberdade para inteiro, e o relatório usa o fracionário.

**Quanto a tela explica do sono.** A decomposição do R² mede quanto o R² da regressão ponderada cai quando cada fator sai do modelo (a parte que só ele explica).

| Fator | Vigitel 2024 (índice de insônia 0–12) | PNS 2019 (problema de sono 0–3) |
|---|---|---|
| tempo de tela | {{r2u_vigitel2024_tela}} | {{r2u_pns2019_tela}} |
| idade | {{r2u_vigitel2024_idade}} | {{r2u_pns2019_idade}} |
| sexo | {{r2u_vigitel2024_sexo}} | {{r2u_pns2019_sexo}} |
| escolaridade | {{r2u_vigitel2024_escolaridade}} | {{r2u_pns2019_escolaridade}} |
| modelo completo (R²) | {{r2c_vigitel2024}} | {{r2c_pns2019}} |

A tela explica pouco: menos que o sexo nas duas pesquisas e, na PNS, menos que a idade. O modelo inteiro explica {{r2c_vigitel2024}} da variação do sono no Vigitel e {{r2c_pns2019}} na PNS: quase tudo o que faz alguém dormir mal está fora destas quatro variáveis.

![Decomposição do R²](../resultados/006/figuras/decomposicao_r2.png)

![Efeitos padronizados](../resultados/005/figuras/efeitos_padronizados.png)

### 5.4 O Brasil no mundo (spec 004)

Correlação de Spearman entre exposição e escore de sono em cada base (positivo = mais tela, pior sono):

| Base | Tipo de exposição | ρ (IC 95%) |
|---|---|---|
| PNS 2019 | tempo total | {{rho_pns2019}} ({{rho_pns2019_ic}}) |
| Vigitel 2024 | tempo total | {{rho_vigitel2024}} ({{rho_vigitel2024_ic}}) |
| Argentina | tempo total | {{rho_argentina}} ({{rho_argentina_ic}}) |
| Japão | celular antes de dormir | {{rho_japao}} ({{rho_japao_ic}}) |
| China (Xuzhou) | uso problemático | {{rho_xuzhou}} ({{rho_xuzhou_ic}}) |
| Turquia | uso problemático (doomscrolling) | {{rho_turquia}} ({{rho_turquia_ic}}) |

Meta-análise de efeitos aleatórios das {{meta_k}} bases. O IC de DerSimonian-Laird usa a distribuição normal; o de Hartung-Knapp reescala o erro padrão pela dispersão entre as bases e usa t com k − 1 gl, o que é mais honesto com tão poucas bases.

- **Estimativa global:** ρ = {{meta_rho}}. Pelo IC de DerSimonian-Laird ({{meta_rho_ic}}; p = {{meta_p_dl}}) fica acima de zero; pelo de Hartung-Knapp ({{meta_rho_ic_hk}}; p = {{meta_p_hk}}) não se distingue de zero.
- **H4.1, heterogeneidade** (H0: a associação é igual em todas as bases): Q = {{meta_Q}}, gl = {{meta_glQ}}, p {{meta_pQ}}, p Holm {{H41_pholm}}; I² = {{meta_I2}}. Decisão: {{H41_decisao}}; a associação varia muito de uma base para outra.
- **H4.2, tipo de exposição** (H0: sem diferença entre tempo total, pré-sono e uso problemático): a ordem é a da literatura, tempo total {{meta_rho_total}} < pré-sono {{meta_rho_presono}} < uso problemático {{meta_rho_problematico}}. Q = {{H42_Q}}, p = {{H42_p}}, p Holm {{H42_pholm}}: {{H42_decisao}}, com só 1 a 3 bases por subgrupo.
- **H4.3, Brasil × outros países com tempo total:** o Brasil (PNS + Vigitel) tem ρ = {{meta_rho_brasil}} e o outro lado, só a Argentina (adolescentes), {{meta_rho_outros}}. z = {{H43_z}}, p Holm {{H43_pholm}}: {{H43_decisao}}. O teste compara o Brasil com uma única base.
- **H4.4, comparação com a meta-análise de referência** (H0: o ρ de tempo total está fora do intervalo 0,21–0,35 de Han, Zhou e Liu, 2024): o tempo total combinado ({{meta_rho_total}}) fica abaixo do intervalo, e o teste de equivalência não rejeita H0 (p Holm {{H44_pholm}}). Nos nossos dados, a associação com tempo total é muito menor que a da literatura.

**Brasil × resto do mundo (exploratório).** Pedida pelo grupo depois de ver os resultados e fora da família de Holm, esta comparação junta as duas pesquisas brasileiras de um lado e as quatro bases dos outros países do outro, misturando os tipos de exposição.

| Grupo | k | ρ | IC 95% DerSimonian-Laird | IC 95% Hartung-Knapp |
|---|---|---|---|---|
| Brasil (PNS + Vigitel) | 2 | {{meta_rho_brasil}} | {{meta_rho_brasil_ic}} | — (k = 2: 1 gl) |
| Resto do mundo (Argentina, Japão, China, Turquia) | 4 | {{meta_rho_resto}} | {{meta_rho_resto_ic}} | {{meta_rho_resto_ic_hk}} |

A diferença, na escala z de Fisher, é {{brasil_resto_dif_z}} (IC 95% {{brasil_resto_dif_ic}}); z = {{brasil_resto_z}}, p = {{brasil_resto_p}}. Não foi detectada diferença. O resto do mundo fica mais alto porque reúne as escalas de uso problemático e de celular antes de dormir; com tempo total, a Argentina ({{rho_argentina}}) fica perto do Brasil.

![O Brasil no mundo](../resultados/006/figuras/brasil_no_mundo.png)

- **Desenho amostral (deff):** as correlações das pesquisas brasileiras foram calculadas sem o desenho amostral. Multiplicando a variância pelo deff de Kish (PNS {{deff_pns2019}}, Vigitel {{deff_vigitel2024}}), a estimativa global fica {{meta_deff_rho}} ({{meta_deff_ic}}) e o I², {{meta_deff_I2}}. Nenhuma decisão muda.
- **Ajuste por idade:** a PNS passa de {{rho_pns2019}} para {{rho_aj_pns2019}} ({{rho_aj_pns2019_ic}}); o Brasil combinado, de {{meta_rho_brasil}} para {{rho_aj_brasil}} ({{rho_aj_brasil_ic}}); e o tempo total combinado, de {{meta_rho_total}} para {{rho_aj_total}} ({{rho_aj_total_ic}}).

![Gráfico de floresta](../resultados/004/figuras/floresta.png)

## 6. Discussão

**Tamanho.** A associação entre tela e problema de sono aparece nas duas pesquisas brasileiras e na maioria das bases, mas é pequena. Com dezenas de milhares de entrevistados, as pesquisas detectam com folga associações sem importância prática. Esse é o padrão descrito por Przybylski (2019): associações consistentes, que explicam poucos por cento da variação. As razões de prevalência entre {{rp_digital_min}} e {{rp_digital_max}} descrevem um grupo extremo (≥ 3 h) contra o de baixo uso. Na decomposição do R², a tela explica menos da variação do sono que o sexo, e na PNS menos que a idade.

**As duas pesquisas concordam.** PNS e Vigitel usam perguntas de sono diferentes, cobrem populações diferentes (o país todo e as capitais) e foram feitas com cinco anos de distância. Mesmo assim, não foi detectada diferença entre as razões de prevalência (IC da razão {{h39_ic}}). Ausência de diferença detectada não é prova de igualdade, mas a concordância dá mais confiança de que a associação não é artefato de uma pesquisa só.

**O Brasil no mundo e na literatura.** A correlação brasileira com tempo total ({{meta_rho_brasil}}) é parecida com a da Argentina e fica muito abaixo do r = 0,28 de Han, Zhou e Liu (2024). Parte da distância vem da medida: nas pesquisas, a exposição é em faixas de horas e o sono é um item só, o que atenua a correlação. Parte vem da população: a literatura é quase toda de crianças, adolescentes e universitários, e as pesquisas brasileiras cobrem adultos de todas as idades.

**O que importa é o tipo de uso.** As maiores correlações vieram do uso problemático (China) e do celular nas horas antes de dormir (Japão), não do tempo total. Isso concorda com Han, Zhou e Liu (2024), com Levenson et al. (2017) e com Hjetland et al. (2025). Mas cada subgrupo tem uma a três bases, e o teste não confirma a diferença.

**Confundimento.** A inversão do sinal na PNS mostra que a idade confunde a relação: jovens usam mais tela e relatam menos problema de sono. Uma comparação sem ajuste chegaria à conclusão oposta.

**Por que os EUA saíram.** A única base dos EUA (NHANES 2005-06) media computador e videogame antes do smartphone. Comparar Brasil 2019–2024 com EUA 2005 misturaria país e época, e nenhuma conclusão sobre "o Brasil frente aos EUA" seria separável da mudança tecnológica. O grupo retirou a base em 2026-11-27, depois de ver os resultados; isso fica registrado nas specs e nesta seção.

## 7. Limitações

- **Dados transversais.** Não dá para separar "tela piora o sono" de "quem dorme mal usa mais tela" (BAUDUCCO et al., 2024).
- **Mudança de escopo depois dos resultados.** A retirada dos EUA e a comparação Brasil × resto do mundo foram decididas depois de ver os números. A primeira está justificada pela época da base; a segunda é exploratória e fica fora da correção de Holm.
- **O item de sono da PNS é outro.** É o do PHQ-9 (inclui dormir demais), enquanto o Vigitel pergunta sobre dificuldade para adormecer. A comparação PNS × Vigitel (H3.9) mistura pesquisa e item.
- **O Vigitel cobre só as capitais** e não divulga estrato e UPA: a variância usa só o peso.
- **Medidas autorrelatadas e em faixas.** Isso atenua as correlações.
- **Comparação internacional limitada.** As quatro bases dos outros países são amostras de conveniência de jovens, com escalas diferentes. Em H4.3, o lado "outros países com tempo total" tem uma base só (Argentina, adolescentes), e a heterogeneidade é extrema (I² = {{meta_I2}}).
- **Bases de repositório sem desenho amostral.**
  - Sexo sem rótulo em Xuzhou e no Japão.
  - Rótulo da escala da Turquia inferido, sem dicionário.
  - {{n_arg_sem_idade}} adolescentes argentinos sem idade.
- **Renda não entrou** nos modelos (ausente no Vigitel e não harmonizada na PNS).

## 8. Conclusões

1. Em adultos brasileiros, usar tela digital no lazer 3 h ou mais por dia se associa a uma prevalência de problema de sono {{rp_br_pct_min}} a {{rp_br_pct_max}} maior, depois de ajustar por idade, sexo e escolaridade.
2. As duas pesquisas nacionais concordam: não foi detectada diferença entre a PNS 2019 e o Vigitel 2024 (razão {{h39_razao}}, IC 95% {{h39_ic}}).
3. O efeito é pequeno. A tela explica {{r2u_vigitel2024_tela}} da variação do índice de insônia no Vigitel e {{r2u_pns2019_tela}} na PNS: menos que o sexo nas duas pesquisas e, na PNS, menos que a idade.
4. Sem ajuste por idade, a conclusão se inverte na PNS. Comparações entre grupos de uso de tela precisam sempre de ajuste.
5. Frente ao resto do mundo, não foi detectada diferença (Brasil ρ = {{meta_rho_brasil}}, outros quatro países ρ = {{meta_rho_resto}}; exploratório). Com tempo total, o Brasil fica bem abaixo da literatura (r = 0,28). Uso problemático e uso antes de dormir se associam mais ao sono, como diz a literatura, mas com tão poucas bases a diferença não foi confirmada.
6. Os dados são transversais. O resultado é uma associação; mostrar causa exigiria estudo longitudinal ou experimental.

## 9. Como conferir

```bash
export STAT4_BRUTOS=/caminho/para/pesquisa/dados
python -m analise.rodar_tudo
python -m pytest
```

Cada etapa tem:

- uma spec com as hipóteses (`specs/00N-*/spec.md`) e, no Histórico, a retirada dos EUA;
- um notebook executado (`analise/notebooks/`);
- um resumo (`resultados/00N/RESUMO.md`);
- uma explicação didática (`docs/explicacoes/`).

As figuras-síntese da apresentação (teste desenhado, decomposição do R², confundimento por idade, Brasil no mundo) ficam em `resultados/006/` e são geradas por `python -m analise.relatorio.figuras_apresentacao`.

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

PRZYBYLSKI, A. K. Digital Screen Time and Pediatric Sleep: Evidence from a Preregistered Cohort Study. **The Journal of Pediatrics**, v. 205, p. 218-223.e1, 2019. DOI: https://doi.org/10.1016/j.jpeds.2018.09.054.
