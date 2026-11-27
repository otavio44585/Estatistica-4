# Etapa 1 — Estado da arte e fontes de dados: Insônia Digital

Estatística 4 — ESEG · Levantamento concluído em 13/11/2026

## 1. Objeto e método do levantamento

**Objeto.** "Insônia digital" não é categoria diagnóstica (o transtorno de insônia é definido no DSM-5 e na ICSD-3). Neste trabalho o termo designa o conjunto de prejuízos ao sono associados ao uso de telas e dispositivos eletrônicos, sobretudo à noite e na cama: maior latência para adormecer, sintomas de insônia, menor duração, pior qualidade e atraso do horário de dormir.

**Busca.** Três frentes executadas em 13/11/2026:

| Frente | Fontes consultadas | Resultado |
|---|---|---|
| Literatura internacional | OpenAlex, Crossref, Europe PMC, PMC | 30 trabalhos: 13 revisões/meta-análises/consenso, 4 experimentos, 13 observacionais |
| Literatura Brasil e América Latina | SciELO, LILACS/BVS, OpenAlex (afiliação BR e países latino-americanos), Europe PMC, Redalyc | 22 trabalhos: 15 na tabela principal + 7 complementares |
| Fontes de dados | portais oficiais (CDC, IBGE, Ministério da Saúde, BLS, HRSA), Figshare, Mendeley Data, Zenodo, Harvard Dataverse, ICPSR, Kaggle | 28 bases baixadas, 17 de acesso restrito, ~35 descartadas |

**Critérios de verificação.** Toda referência teve o DOI resolvido no Crossref e no OpenAlex; achados, tamanhos amostrais e desenhos foram extraídos do resumo ou do texto integral, nunca de memória. Nas bases baixadas, cada variável citada foi conferida no dicionário oficial e no próprio arquivo. Detalhamento completo em `_inventario_papers_internacional.md`, `_inventario_papers_brasil.md` e `_inventario_dados.md`.

**Acervo local.** 42 PDFs (23 internacionais, 19 brasileiros/latino-americanos); 10 trabalhos sem PDF (seção 8).

## 2. O que a literatura estabelece

### 2.1 Associação consistente

A revisão sistemática seminal reuniu 67 estudos com crianças e adolescentes e encontrou associação adversa entre tempo de tela e sono em 90% deles, principalmente menor duração e horário mais tardio (HALE; GUAN, 2015). A meta-análise de Carter et al. (2016), com 20 estudos e 125.198 participantes de 6 a 19 anos, estimou que o uso de dispositivo portátil na hora de dormir se associa a sono insuficiente (OR 2,17; IC95% 1,42–3,32), má qualidade (OR 1,46) e sonolência diurna (OR 2,72). O simples acesso ao aparelho no quarto, sem uso, também se associou a sono insuficiente (OR 1,79).

Revisões posteriores confirmam a direção. Em jovens de 16 a 25 anos, celular, computador, internet e redes sociais se associaram a menor duração e pior qualidade; TV, console e tablet, não (BRAUTSCH et al., 2023). Em 55 artigos de 2018 a 2023, o uso geral de mídia eletrônica se correlacionou com pior qualidade do sono (r = 0,28) e o uso problemático, com mais problemas de sono (r = 0,33), com efeitos maiores em culturas orientais (HAN; ZHOU; LIU, 2024). O consenso da National Sleep Foundation concluiu que o uso de tela prejudica o sono de crianças e adolescentes, mas não emitiu conclusão sobre adultos nem sobre o efeito da luz (HARTSTEIN et al., 2024).

### 2.2 Efeito pequeno quando medido em minutos

As medidas contínuas mostram magnitudes modestas:

| Estudo | Desenho | Efeito |
|---|---|---|
| Przybylski (2019) | NSCH 2016, n = 50.212, regressão hierárquica pré-registrada | −3 a −8 min de sono por hora de tela; tela explica < 1,9% da variância |
| Orben; Przybylski (2020) | Millennium Cohort, n = 11.884, curva de especificação | −9 min/h em dia de semana, −3 min/h no fim de semana; tela nos 30 min antes de dormir ≈ −1 min |
| He et al. (2025) | MA de 21 coortes, n = 548.338 | −3 a −5 min de sono e +13,2 min no horário de deitar por hora de tela/dia; dificuldade de iniciar o sono OR 3,05 |
| Hjetland et al. (2025) | SHoT 2022, ~45 mil universitários | cada hora de tela **na cama**: −24 min de sono e OR 1,59 para sintomas de insônia |
| Castro-Santos et al. (2023) | SONAR-Brasil, n = 2.050 adultos | tela ≥ 2 h antes de deitar: **latência +16,98 min** (IC95% 13,14–20,82); +0,10 min por minuto de tela |
| Echevarria et al. (2023) | Coorte de Pelotas 2004, 15 anos | tela ≥ 9 h/dia vs < 2 h: −0,54 h (≈ −32 min) de sono |
| Chang et al. (2015) | experimento cruzado, n = 12, PSG | e-book emissor de luz por 4 h: latência 25,7 vs 15,8 min no livro impresso |

As medidas binárias produzem razões de chance grandes (Carter: OR 2,17; Hjetland: OR 1,59), enquanto as contínuas mostram poucos minutos por hora de exposição. Os dois tipos de resultado convivem na mesma literatura e dependem da forma como o desfecho é medido.

### 2.3 O momento do uso pesa mais que o total

Checar redes sociais nos 30 minutos antes de dormir se associou a perturbação do sono (aOR 1,62) independentemente do uso total diário, em amostra nacional de 1.763 adultos jovens dos EUA (LEVENSON et al., 2017). Medidas objetivas apontam na mesma direção: logs de aplicativo em 653 adultos associaram o uso perto da hora de deitar a menor eficiência e maior latência (CHRISTENSEN et al., 2016), e em adolescentes com Fitbit o uso noturno (20h–6h), mas não o diurno, atrasou o início do sono (BURNELL et al., 2024). Na meta-análise intrapessoal de 25 estudos, a tela usada depois de deitar teve correlação mais negativa com a qualidade (r = −0,092) que a tela diária (−0,026) ou noturna (−0,005) (BOURKE et al., 2026).

### 2.4 Mecanismos

- **Deslocamento de tempo.** É o achado mais robusto. Comparando a mesma pessoa em dias diferentes, o único efeito significativo da tela é atrasar o início do sono (r = 0,079); duração, latência, eficiência e qualidade não mudam (BOURKE et al., 2026). O deslocamento ocorre em dois passos: deitar mais tarde e, já na cama, adiar a tentativa de dormir, com intervalo médio de 39 min (EXELMANS; VAN DEN BULCK, 2017). A procrastinação da hora de dormir se correlaciona com menor duração (z = −0,31) e pior qualidade (z = −0,35) (HILL et al., 2022).
- **Luz e melatonina.** Demonstrado em laboratório: o e-book emissor de luz suprimiu a melatonina em 55% e atrasou o relógio circadiano em mais de 1,5 h (CHANG et al., 2015); o efeito sobre latência e melatonina segue dose-resposta com a irradiância melanópica da tela (SCHÖLLHORN et al., 2023).
- **Excitação pelo conteúdo.** Evidência mista. Trinta minutos de redes sociais antes de dormir não aumentaram a excitação nem pioraram o sono medido por polissonografia em 32 jovens (COMBERTALDI et al., 2021). Entre universitários noruegueses, a associação da tela na cama com insônia não diferiu por tipo de atividade (HJETLAND et al., 2025).
- **Direção inversa.** O problema de sono também leva ao uso: a tela funciona como "passatempo" enquanto o sono não vem e como estratégia de regulação emocional (BAUDUCCO et al., 2024).

## 3. Questões metodológicas levantadas pela literatura

| Questão | Evidência |
|---|---|
| **Confundimento** | A correlação bruta entre tela e duração do sono (r = −0,35) caiu para r semiparcial = −0,14 após controles de criança, família e vizinhança; segundo o autor, cinco sextos da correlação bruta estavam ligados aos controles (PRZYBYLSKI, 2019) |
| **Viés do autorrelato** | Uso autorrelatado e uso registrado em log se correlacionam só moderadamente; escalas de "uso problemático" ainda menos (PARRY et al., 2021). As associações negativas vêm sobretudo das medidas retrospectivas, não do diário de uso do tempo (ORBEN; PRZYBYLSKI, 2020) |
| **Causalidade reversa** | Problemas de sono previram mais TV e redes sociais anos depois, e não o contrário (TAVERNIER; WILLOUGHBY, 2014). Associação bidirecional em coorte de 3.396 estudantes (LIU et al., 2019). Na MA de estudos longitudinais, o sono pior prevê mais uso disfuncional de mídia (PAGANO; BACARO; CROCETTI, 2023) |
| **Entre pessoas × dentro da pessoa** | Num diário de 14 dias com log, nas noites com mais smartphone que o habitual os adolescentes dormiram mais cedo e por mais tempo, com efeito fraco (TKACZYK et al., 2023). As associações entre pessoas (transversais, coortes) são mais fortes que as intrapessoais (BOURKE et al., 2026) |
| **Heterogeneidade** | Efeitos maiores em culturas orientais (HAN; ZHOU; LIU, 2024); moderação por região, desenho, idade e sexo (AHMED et al., 2024) |
| **Desenho dos estudos** | Predominam estudos transversais com desfecho binário e regressão logística. Dos 15 estudos brasileiros/latino-americanos principais, só três usam regressão linear ou GLM com desfecho contínuo (ECHEVARRIA et al., 2023; CASTRO-SANTOS et al., 2023; OLIVARES-GUIDO et al., 2024); um quarto usa equações estruturais (PÉREZ-CHADA et al., 2023) |

## 4. Estudos que usaram regressão linear

Referência direta para comparar coeficientes e escolher covariáveis.

| Estudo | Y | X | Modelo | Coeficiente | Covariáveis |
|---|---|---|---|---|---|
| Castro-Santos et al. (2023) | latência (min) | tela ≥ 2 h antes de deitar; minutos de tela | linear múltipla + splines | β = +16,98 min; +0,10 min por minuto | idade, sexo, região, estado civil, escolaridade, dieta noturna, IMC |
| Echevarria et al. (2023) | duração (h) | tela de lazer em 5 faixas | linear, seleção backward (p < 0,20) | β = −0,54 h (≥ 9 h vs < 2 h) | sexo, renda, escolaridade materna, trabalho, sintomas psicológicos, álcool |
| Przybylski (2019) | duração; consistência | horas de tela/dia | linear hierárquica pré-registrada | b = −0,040 a −0,049 | idade, sexo, raça, estressores, apoio social, saúde; escolaridade do cuidador, finanças, segurança alimentar, auxílio; vizinhança |
| Exelmans; Van den Bulck (2016) | PSQI, insônia, fadiga | uso do celular na cama / após apagar a luz | linear hierárquica: bloco 1 controles, bloco 2 exposição | — (ver texto) | sexo, idade, escolaridade em dummies |
| Exelmans; Van den Bulck (2017) | latência deitar → tentar dormir | razão mídia pré-deitar / atividades pré-deitar | hierárquica | b = 0,202 (p < 0,01) | controles + hora de deitar |
| Christensen et al. (2016) | componentes do PSQI | minutos de tela por log | linear múltipla | — (ver texto) | idade, sexo, apneia do sono + preditores significativos |
| Hjetland et al. (2025) | duração | minutos de tela na cama | linear múltipla | −24 min por hora | idade, sexo |
| Orben; Przybylski (2020) | duração, horário | tecnologia (retrospectiva e diário) | curva de especificação (muitas regressões lineares) | β mediano −0,06 (semana) | sexo, idade, etnia materna, renda, irmãos, escolaridade e depressão materna, entre outras |
| Olivares-Guido et al. (2024) | PSQI contínuo | uso problemático de smartphone (MREQ) | GLM robusto | B = 0,29 ponto de PSQI por ponto | turno escolar, esporte, escolaridade paterna, percepção de prejuízo |

## 5. Evidência brasileira e latino-americana

- **Adultos.** SONAR-Brasil (CASTRO-SANTOS et al., 2023) é o único estudo nacional que mede latência em minutos com regressão linear múltipla. No ConVid, survey com 45.161 adultos na quarentena de 2020, a incidência de computador/tablet ≥ 4 h/dia se associou a piora do sono (OR 1,91) (WERNECK et al., 2020).
- **Adolescentes.** Na coorte de Pelotas 2004, tela ≥ 9 h/dia reduziu o sono em cerca de 32 min (ECHEVARRIA et al., 2023). Em colégios militares de Fortaleza, usar o celular antes de dormir se associou a sonolência excessiva (OR 4,30) (SOUZA; PINTO; ALVES, 2020). Em Presidente Prudente, o tempo de tela se associou a pior sono só entre os insuficientemente ativos (SANTOS et al., 2024). Em Caruaru, TV ≥ 2 h/dia se associou a percepção negativa do sono (SILVA et al., 2017), e computador e videogame, só no grupo com risco de ansiedade (SANTIAGO et al., 2022). Em Porto Alegre, a associação desapareceu após o ajuste (CAUMO et al., 2020).
- **Universitários.** Em Alfenas-MG, uso noturno de internet se associou à proporção de maus dormidores (MESQUITA; REIMÃO, 2010). Estudantes de medicina sem celular 1 h antes de dormir por 15 dias tiveram PSQI de 8,2 para 6,4, em estudo antes-depois sem grupo controle (FREITAS et al., 2017).
- **América Latina.** Peru: dependência de Facebook e má qualidade do sono (RP 1,31) (WOLNICZAK et al., 2013). Argentina: videogame associado a menor duração (coef. padronizado −0,22) (PÉREZ-CHADA et al., 2023) — base pública. México: cada ponto de uso problemático de smartphone soma 0,29 ponto de PSQI (OLIVARES-GUIDO et al., 2024).
- **Revisão nacional.** Silva et al. (2022), em *Cadernos de Saúde Pública*, reuniram 23 estudos com adolescentes, sem meta-análise; nenhum foi classificado como de boa qualidade pela escala Newcastle-Ottawa.

## 6. Lacunas identificadas

- Adultos e universitários sub-representados: a maioria dos estudos é com crianças e adolescentes (BRAUTSCH et al., 2023).
- Evidência experimental escassa: 35 estudos experimentais ou de intervenção entre 522 empíricos avaliados pelo consenso da NSF (HARTSTEIN et al., 2024).
- Causalidade não confirmada e erro de medida da exposição já eram as limitações centrais na revisão seminal (HALE; GUAN, 2015) e persistem (PARRY et al., 2021).
- No Brasil, a busca não encontrou estudo de tela × sono com PeNSE, PNS, Vigitel ou ELSA-Brasil, embora PNS, PeNSE 2015 e Vigitel 2024 tenham as duas variáveis (seção 7). A ausência na busca não prova inexistência.

## 7. Fontes de dados disponíveis

Detalhe, códigos de variáveis e caminhos em `README.md` e `_inventario_dados.md`. C = contínua, O = ordinal.

| Grupo | Bases baixadas | Y de sono | X de tela | Observação |
|---|---|---|---|---|
| Inquéritos nacionais brasileiros | PNS 2019 (n = 90.846), PNS 2013, PeNSE 2015, Vigitel 2024 | problemas no sono (O); Vigitel: duração (C) e sintomas de insônia (O) | horas de TV e de computador/celular em faixas (O) | pesos amostrais; nenhum mede latência |
| Inquéritos nacionais dos EUA | NHANES 2005-06 a 2015-16, NSCH 2017/2025, YRBS 2021, ABES 2021 | NHANES 2005-06: **latência em min (C, máx. 60)**; demais: horas de sono | horas de TV/computador (O) | pesos amostrais; códigos 77/99 |
| Diário de uso do tempo | ATUS 2025 (n = 6.146) | minutos de sono e de insônia (C) | minutos de TV/computador (C) | sequência permite tela antes de dormir |
| Repositórios de estudos publicados | 14 bases (Argentina, Nigéria, Japão, Holanda, Turquia, China, Peru, Indonésia, Paquistão, Bangladesh) | latência em min (C) em Argentina, Nigéria, Turquia, Paquistão; AIS, PSQI, ISI | tela antes de dormir (C) em Argentina e Japão; log de app na Holanda | 3 bases com procedência questionável marcadas no inventário |

Bases com desenho amostral complexo (PNS, PeNSE, Vigitel, NHANES, NSCH, YRBS, ATUS) trazem pesos que a ferramenta de Regressão do Excel não aplica.

## 8. Pendências da etapa

**Com versão aberta, abrir no navegador:** Bauducco et al. 2024 (https://oru.diva-portal.org/smash/get/diva2:1852117/FULLTEXT01) · Bourke et al. 2026 (https://pmc.ncbi.nlm.nih.gov/articles/PMC12954599/) · Levenson et al. 2017 (https://pmc.ncbi.nlm.nih.gov/articles/PMC8205627/) · Tkaczyk et al. 2023 (https://doi.org/10.1016/j.chb.2023.107946).

**Pagos, sem versão aberta:** Tavernier; Willoughby 2014 · Bhat et al. 2018 · Liu et al. 2019 · Caumo et al. 2020 · Oliveira et al. 2020 · Wells et al. 2008 (DOIs nas referências).

Os 10 já estão descritos nos inventários a partir do resumo ou do texto do PMC; a ausência do PDF não bloqueia a próxima etapa.

## Referências

Lista completa do acervo (52 trabalhos), em ordem alfabética, gerada a partir dos metadados do Crossref. Inclui trabalhos que estão nos inventários e não são citados neste texto; na versão final do relatório, manter só os citados.

AHMED, O. et al. Social media use, mental health and sleep: A systematic review with meta-analyses. **Journal of Affective Disorders**, v. 367, p. 701-712, 2024. DOI: https://doi.org/10.1016/j.jad.2024.08.193.

BAUDUCCO, S. et al. A bidirectional model of sleep and technology use: A theoretical review of How much, for whom, and which mechanisms. **Sleep Medicine Reviews**, v. 76, p. 101933, 2024. DOI: https://doi.org/10.1016/j.smrv.2024.101933.

BHAT, S. et al. "To sleep, perchance to tweet": in-bed electronic social media use and its associations with insomnia, daytime sleepiness, mood, and sleep duration in adults. **Sleep Health**, v. 4, n. 2, p. 166-173, 2018. DOI: https://doi.org/10.1016/j.sleh.2017.12.004.

BOURKE, M. et al. Within-Person Association Between Daily Screen Use and Sleep in Youth: A Systematic Review and Meta-Analysis. **JAMA Pediatrics**, v. 180, n. 5, p. 500, 2026. DOI: https://doi.org/10.1001/jamapediatrics.2025.6490.

BRAUTSCH, L. A. et al. Digital media use and sleep in late adolescence and young adulthood: A systematic review. **Sleep Medicine Reviews**, v. 68, p. 101742, 2023. DOI: https://doi.org/10.1016/j.smrv.2022.101742.

BURNELL, K. et al. Daily links between objective smartphone use and sleep among adolescents. **Journal of Adolescence**, v. 96, n. 6, p. 1171-1181, 2024. DOI: https://doi.org/10.1002/jad.12326.

CARTER, B. et al. Association Between Portable Screen-Based Media Device Access or Use and Sleep Outcomes: A Systematic Review and Meta-analysis. **JAMA Pediatrics**, v. 170, n. 12, p. 1202, 2016. DOI: https://doi.org/10.1001/jamapediatrics.2016.2341.

CASTRO-SANTOS, L. et al. Sleep and circadian hygiene practices association with sleep quality among Brazilian adults. **Sleep Medicine: X**, v. 6, p. 100088, 2023. DOI: https://doi.org/10.1016/j.sleepx.2023.100088.

CAUMO, G. H. et al. Exposure to electronic devices and sleep quality in adolescents: a matter of type, duration, and timing. **Sleep Health**, v. 6, n. 2, p. 172-178, 2020. DOI: https://doi.org/10.1016/j.sleh.2019.12.004.

CHANG, A. M. et al. Evening use of light-emitting eReaders negatively affects sleep, circadian timing, and next-morning alertness. **Proceedings of the National Academy of Sciences**, v. 112, n. 4, p. 1232-1237, 2015. DOI: https://doi.org/10.1073/pnas.1418490112.

CHRISTENSEN, M. A. et al. Direct Measurements of Smartphone Screen-Time: Relationships with Demographics and Sleep. **PLOS ONE**, v. 11, n. 11, p. e0165331, 2016. DOI: https://doi.org/10.1371/journal.pone.0165331.

COMBERTALDI, S. L. et al. Pre-sleep social media use does not strongly disturb sleep: a sleep laboratory study in healthy young participants. **Sleep Medicine**, v. 87, p. 191-202, 2021. DOI: https://doi.org/10.1016/j.sleep.2021.09.009.

ECHEVARRIA, P. et al. Screen use and sleep duration and quality at 15 years old: Cohort study. **Sleep Medicine: X**, v. 5, p. 100073, 2023. DOI: https://doi.org/10.1016/j.sleepx.2023.100073.

EXELMANS, L.; VAN DEN BULCK, J. Bedtime mobile phone use and sleep in adults. **Social Science & Medicine**, v. 148, p. 93-101, 2016. DOI: https://doi.org/10.1016/j.socscimed.2015.11.037.

EXELMANS, L.; VAN DEN BULCK, J. Bedtime, shuteye time and electronic media: sleep displacement is a two-step process. **Journal of Sleep Research**, v. 26, n. 3, p. 364-370, 2017. DOI: https://doi.org/10.1111/jsr.12510.

FREITAS, C. C. M. et al. Relação entre uso do telefone celular antes de dormir, qualidade do sono e sonolência diurna. **Revista de Medicina**, v. 96, n. 1, p. 14-20, 2017. DOI: https://doi.org/10.11606/issn.1679-9836.v96i1p14-20.

HALE, L.; GUAN, S. Screen time and sleep among school-aged children and adolescents: A systematic literature review. **Sleep Medicine Reviews**, v. 21, p. 50-58, 2015. DOI: https://doi.org/10.1016/j.smrv.2014.07.007.

HAN, X.; ZHOU, E.; LIU, D. Electronic Media Use and Sleep Quality: Updated Systematic Review and Meta-Analysis. **Journal of Medical Internet Research**, v. 26, p. e48356, 2024. DOI: https://doi.org/10.2196/48356.

HARTSTEIN, L. E. et al. The impact of screen use on sleep health across the lifespan: A National Sleep Foundation consensus statement. **Sleep Health**, v. 10, n. 4, p. 373-384, 2024. DOI: https://doi.org/10.1016/j.sleh.2024.05.001.

HE, X. et al. The association of screen time and the risk of sleep outcomes: a systematic review and meta-analysis. **Frontiers in Psychiatry**, v. 16, 1640263, 2025. DOI: https://doi.org/10.3389/fpsyt.2025.1640263.

HILL, V. M. et al. Go to bed! A systematic review and meta-analysis of bedtime procrastination correlates and sleep outcomes. **Sleep Medicine Reviews**, v. 66, p. 101697, 2022. DOI: https://doi.org/10.1016/j.smrv.2022.101697.

HJETLAND, G. J. et al. How and when screens are used: comparing different screen activities and sleep in Norwegian university students. **Frontiers in Psychiatry**, v. 16, 1548273, 2025. DOI: https://doi.org/10.3389/fpsyt.2025.1548273.

HYSING, M. et al. Sleep and use of electronic devices in adolescence: results from a large population-based study. **BMJ Open**, v. 5, n. 1, p. e006748, 2015. DOI: https://doi.org/10.1136/bmjopen-2014-006748.

LEVENSON, J. C. et al. Social Media Use Before Bed and Sleep Disturbance Among Young Adults in the United States: A Nationally Representative Study. **Sleep**, v. 40, n. 9, zsx113, 2017. DOI: https://doi.org/10.1093/sleep/zsx113.

LIMA, D. V. G. et al. Quality of sleep and use of computers and cell-phones among university students. **Revista da Associação Médica Brasileira**, v. 65, n. 12, p. 1454-1458, 2019. DOI: https://doi.org/10.1590/1806-9282.65.12.1454.

LIU, S. et al. The associations of long-time mobile phone use with sleep disturbances and mental distress in technical college students: a prospective cohort study. **Sleep**, v. 42, n. 2, zsy213, 2019. DOI: https://doi.org/10.1093/sleep/zsy213.

LUND, L. et al. Electronic media use and sleep in children and adolescents in western countries: a systematic review. **BMC Public Health**, v. 21, n. 1, 1598, 2021. DOI: https://doi.org/10.1186/s12889-021-11640-9.

MARIN, M. G. et al. Internet addiction, sleeping habits and psychological distress in Brazilian adolescents and young adults. **Psicologia: Reflexão e Crítica**, v. 37, n. 1, 37, 2024. DOI: https://doi.org/10.1186/s41155-024-00323-0.

MESQUITA, G.; REIMÃO, R. Nightly use of computer by adolescents: its effect on quality of sleep. **Arquivos de Neuro-Psiquiatria**, v. 65, n. 2b, p. 428-432, 2007. DOI: https://doi.org/10.1590/S0004-282X2007000300012.

MESQUITA, G.; REIMÃO, R. Quality of sleep among university students: effects of nighttime computer and television use. **Arquivos de Neuro-Psiquiatria**, v. 68, n. 5, p. 720-725, 2010. DOI: https://doi.org/10.1590/S0004-282X2010000500009.

OLIVARES-GUIDO, C. M. et al. Problematic Use of Smartphones and Social Media on Sleep Quality of High School Students in Mexico City. **International Journal of Environmental Research and Public Health**, v. 21, n. 9, p. 1177, 2024. DOI: https://doi.org/10.3390/ijerph21091177.

OLIVEIRA, M. L. C. de et al. Impact of Electronic Device Usage Before Bedtime on Sleep and Attention in Adolescents. **Mind, Brain, and Education**, v. 14, n. 4, p. 376-386, 2020. DOI: https://doi.org/10.1111/mbe.12260.

OLIVEIRA, T. et al. Children's behavioral problems, screen time, and sleep problems' association with negative and positive parenting strategies during the COVID-19 outbreak in Brazil. **Child Abuse & Neglect**, v. 130, p. 105345, 2022. DOI: https://doi.org/10.1016/j.chiabu.2021.105345.

ORBEN, A.; PRZYBYLSKI, A. K. Teenage sleep and technology engagement across the week. **PeerJ**, v. 8, p. e8427, 2020. DOI: https://doi.org/10.7717/peerj.8427.

PAGANO, M.; BACARO, V.; CROCETTI, E. "Using digital media or sleeping … that is the question". A meta-analysis on digital media use and unhealthy sleep in adolescence. **Computers in Human Behavior**, v. 146, p. 107813, 2023. DOI: https://doi.org/10.1016/j.chb.2023.107813.

PARRY, D. A. et al. A systematic review and meta-analysis of discrepancies between logged and self-reported digital media use. **Nature Human Behaviour**, v. 5, n. 11, p. 1535-1547, 2021. DOI: https://doi.org/10.1038/s41562-021-01117-5.

PAUL, V. C. G. de et al. Association of smartphone addiction with pain, sleep, anxiety, and depression in university students. **Fisioterapia em Movimento**, v. 36, e36110, 2023. DOI: https://doi.org/10.1590/fm.2023.36110.

PÉREZ-CHADA, D. et al. Screen use, sleep duration, daytime somnolence, and academic failure in school-aged adolescents. **PLOS ONE**, v. 18, n. 2, p. e0281379, 2023. DOI: https://doi.org/10.1371/journal.pone.0281379.

PERRAULT, A. A. et al. Reducing the use of screen electronic devices in the evening is associated with improved sleep and daytime vigilance in adolescents. **Sleep**, v. 42, n. 9, zsz125, 2019. DOI: https://doi.org/10.1093/sleep/zsz125.

PRADO, I. M. et al. Possible sleep bruxism, smartphone addiction and sleep quality among Brazilian university students during COVID-19 pandemic. **Sleep Science**, v. 15, n. 2, p. 158-167, 2022. DOI: https://doi.org/10.5935/1984-0063.20220036.

PRZYBYLSKI, A. K. Digital Screen Time and Pediatric Sleep: Evidence from a Preregistered Cohort Study. **The Journal of Pediatrics**, v. 205, p. 218-223.e1, 2019. DOI: https://doi.org/10.1016/j.jpeds.2018.09.054.

SANTIAGO, F. L. et al. Association between screen time exposure, anxiety, and sleep quality in adolescents. **Salud Mental**, v. 45, n. 3, p. 125-133, 2022. DOI: https://doi.org/10.17711/sm.0185-3325.2022.017.

SANTOS, A. B. dos et al. Screen time is negatively associated with sleep quality and duration only in insufficiently active adolescents: A Brazilian cross-sectional school-based study. **Preventive Medicine Reports**, v. 37, p. 102579, 2024. DOI: https://doi.org/10.1016/j.pmedr.2023.102579.

SCHÖLLHORN, I. et al. Melanopic irradiance defines the impact of evening display light on sleep latency, melatonin and alertness. **Communications Biology**, v. 6, n. 1, 228, 2023. DOI: https://doi.org/10.1038/s42003-023-04598-4.

SILVA, A. O. da et al. Tempo de tela, percepção da qualidade de sono e episódios de parassonia em adolescentes. **Revista Brasileira de Medicina do Esporte**, v. 23, n. 5, p. 375-379, 2017. DOI: https://doi.org/10.1590/1517-869220172305163582.

SILVA, S. S. da et al. Use of digital screens by adolescents and association on sleep quality: a systematic review. **Cadernos de Saúde Pública**, v. 38, n. 10, e00300721, 2022. DOI: https://doi.org/10.1590/0102-311XEN300721.

SOUZA, E. A. de; PINTO, J. C. B. L. de; ALVES, F. R. Uso do celular antes de dormir: um fator com maior risco para sonolência excessiva em adolescentes de escolas militares. **Jornal Brasileiro de Psiquiatria**, v. 69, n. 2, p. 111-116, 2020. DOI: https://doi.org/10.1590/0047-2085000000265.

TAVERNIER, R.; WILLOUGHBY, T. Sleep problems: predictor or outcome of media use among emerging adults at university? **Journal of Sleep Research**, v. 23, n. 4, p. 389-396, 2014. DOI: https://doi.org/10.1111/jsr.12132.

TKACZYK, M. et al. Are smartphones detrimental to adolescent sleep? An electronic diary study of evening smartphone use and sleep. **Computers in Human Behavior**, v. 149, p. 107946, 2023. DOI: https://doi.org/10.1016/j.chb.2023.107946.

WELLS, J. C. K. et al. Sleep patterns and television viewing in relation to obesity and blood pressure: evidence from an adolescent Brazilian birth cohort. **International Journal of Obesity**, v. 32, n. 7, p. 1042-1049, 2008. DOI: https://doi.org/10.1038/ijo.2008.37.

WERNECK, A. O. et al. The mediation role of sleep quality in the association between the incidence of unhealthy movement behaviors during the COVID-19 quarantine and mental health. **Sleep Medicine**, v. 76, p. 10-15, 2020. DOI: https://doi.org/10.1016/j.sleep.2020.09.021.

WOLNICZAK, I. et al. Association between Facebook Dependence and Poor Sleep Quality: A Study in a Sample of Undergraduate Students in Peru. **PLoS ONE**, v. 8, n. 3, p. e59087, 2013. DOI: https://doi.org/10.1371/journal.pone.0059087.
