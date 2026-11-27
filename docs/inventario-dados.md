# Inventário de fontes de dados — "insônia digital" (tela/dispositivo × sono)

Levantamento de 2026-11-13. Critério: microdado em nível de indivíduo com variável de tela/dispositivo **e** variável de sono no mesmo arquivo (ou em arquivos ligáveis pelo ID do indivíduo). Todo código de variável abaixo foi conferido no dicionário/codebook oficial (URL citada) e, nas fontes baixadas, também no próprio arquivo. "Não verificado" indica o que não foi possível confirmar em documento oficial.

Pastas: `<STAT4_BRUTOS>/<fonte>/` (fora do git; ver `specs/001-dados-harmonizados/plan.md`). Scripts de inspeção (só leitura) ficaram fora das pastas de dados.

Totais: **28 conjuntos baixados** em 28 pastas (mais 2 pastas só com documentação de fontes descartadas: `pense_2019`, `pense_2024`); **17 não baixados**; descartados na seção 4. Volume baixado: 535,6 MB (561.627.878 B; maior arquivo: 226,8 MB). Em disco, incluindo `extraido\`: 1.685,7 MB.

## 1. Tabela-resumo

Legenda de tipo: **C** contínua · **O** ordinal · **B** binária. "Aberto" = download direto, sem cadastro.

| Fonte | País/ano | n | Y de sono (códigos, tipo) | X de tela (códigos, tipo) | Covariáveis-chave | Acesso | Real/sintético | Status |
|---|---|---|---|---|---|---|---|---|
| NHANES 2005-2006 | EUA, 2005-06 | 6.139 (≥16 anos) | `SLD020M` latência min (C, topo 60), `SLD010H` h sono (C), `SLQ080`–`SLQ100` sintomas de insônia e `SLQ110`–`SLQ140` não descansado/sonolência/sono insuficiente/remédio (O 0–4), `SLQ050`/`SLQ060` (B), `DPQ030` (O 0–3) | `PAD590` TV h/dia, `PAD600` computador/games h/dia (O 0–5, 6 = nenhuma) | `RIDAGEYR`, `RIAGENDR`, `INDFMPIR`, `DMDEDUC2`, `RIDRETH1`, `DR1TCAFF` cafeína, `BMXBMI`, PHQ-9, pesos/desenho | Aberto (public-use, domínio público) | Real | BAIXADO em `nhanes_2005_2006` |
| NHANES 2011-2012 | EUA, 2011-12 | 6.175 | `SLD010H` (C), `SLQ050`/`SLQ060` (B), `DPQ030` (O) | `PAQ710` TV, `PAQ715` computador (O 0–5, 8 = não usa) | idem | Aberto | Real | BAIXADO em `nhanes_2011_2012` |
| NHANES 2013-2014 | EUA, 2013-14 | 6.464 | idem 2011-12 | `PAQ710`, `PAQ715` (O) | idem | Aberto | Real | BAIXADO em `nhanes_2013_2014` |
| NHANES 2015-2016 | EUA, 2015-16 | 6.327 | `SLD012` h sono (C), `SLQ300`/`SLQ310` horários (HH:MM), `SLQ050` (B), `SLQ120` sonolência (O 0–4), `DPQ030` (O) | `PAQ710`, `PAQ715` (O) | idem | Aberto | Real | BAIXADO em `nhanes_2015_2016` |
| NSCH 2025 | EUA, 2025 | 45.139 crianças 0–17 | `HOURSLEEP` (O 1–7), `HOURSLEEP05` (O), `BEDTIME` regularidade (O 1–5) | `SCREENTIME` (O 1–5) | `SC_AGE_YEARS`, `SC_SEX`, `SC_RACER`, `HIGRADE`, `FPL_I1-6`, `PHYSACTIV`, `K2Q32A`, `K2Q33A`; `FWC` | Aberto (domínio público) | Real | BAIXADO em `nsch_2025` |
| NSCH 2017 | EUA, 2017 | 21.599 | idem 2025 | `K7Q60_R` TV (O 1–6), `K7Q91_R` dispositivos (O 1–6) | idem | Aberto | Real | BAIXADO em `nsch_2017` |
| YRBS 2021 | EUA, 2021 | 17.232 (9º–12º ano) | `Q86` h sono (O 1–7), `QN86` ≥8 h (B) | `Q78` screen time (O 1–6), `QN78` ≥3 h (B) | `Q1` idade, `Q2` sexo, `Q3` série, `RACEETH`, `Q25`, `Q85`, `Q77`, `BMIPCT`; sem renda | Aberto | Real | BAIXADO em `yrbs_2021` |
| YRBS 2025 | EUA, 2025 | 10.710 | `Q83` h sono (O 1–7), `QN83` (B) | `Q77` freq. redes sociais (O 1–8); sem horas de tela | `Q1`, `Q2`, `Q3`, `RACEETH`, `Q73`, `Q81`, `Q105` | Aberto | Real | BAIXADO em `yrbs_2025` |
| ABES 2021 | EUA, jan–jun 2021 | 7.705 | `Q86`, `QN86` | `Q78`, `QN78` | idem YRBS + `Q100`–`Q111` (COVID) | Aberto | Real | BAIXADO em `abes_2021` |
| ATUS 2025 | EUA, 2025 | 6.146 (15–85 anos; 114.151 episódios) | `t010101` sono, `t010102` insônia/acordado (C, min/dia) | `t120303` TV, `t120308` computador lazer, `t120307` jogos (C, min/dia); sequência de episódios permite "tela antes de dormir" | `TEAGE`, `TESEX`, `PEEDUCA`, `PTDTRACE`, `TELFS`, `TRCHILDNUM`, `HEFAMINC`; `TUFINLWGT` | Aberto (domínio público) | Real | BAIXADO em `atus_2025` |
| PNS 2019 | Brasil, 2019 | 90.846 (≥15 anos) | `N010` problemas no sono, 2 sem (O 1–4); `Q132` remédio para dormir (B) | `P04501` TV (O 1–5, 6 = não assiste), `P04502` computador/tablet/celular lazer (O 1–5, 6 = não usa) | `C006`, `C008`, `C009`, `VDD004A`, `VDF003`, `J001`, `P034`, `P050`, `Q092`; `V00291` | Aberto (FTP IBGE) | Real | BAIXADO em `pns_2019` |
| PNS 2013 | Brasil, 2013 | 60.202 (≥18 anos) | `N010` (O 1–4), `Q132` (B) | `P045` TV (O 1–7, 8 = não assiste); sem computador/celular | `C006`, `C008`, `VDD004A`, `VDF003`; `V00291` | Aberto | Real | BAIXADO em `pns_2013` |
| PeNSE 2015 (Amostras 1 e 2) | Brasil, 2015 | 102.072 (9º ano) + 16.556 (13–17 anos) | `VB12002` não dormiu por preocupação, 12 m (O 1–5) | `VB03009A` TV h/dia (O 1–10), `VB03010A` tempo sentado com telas e outras atividades (O 1–9) | `VB01001`, `VB01002`, `VB01003`, `VB01008A`, `VB01014`–`VB01016`, `VB03011A`; `PESO` | Aberto | Real | BAIXADO em `pense_2015` |
| Vigitel 2006–2024 (sono só em 2024) | Brasil, 27 capitais, 2024 | 27.048 (2024) de 833.217 | `r701_hh`+`r701_mm` duração (C), `r702` sono desejado (C), `r703`–`r705` sintomas de insônia (O 1–5), `r706` ronco, `r707` apneia; `insonia` (B) | `q59a` TV (O 1–7, 8 = não assiste), `q59b` usa computador/tablet/celular (B), `q59c` horas desse uso (O 1–7) | `q6` idade, `q7` sexo, `fesc`, `q69` cor, `civil`, `imc`, `fumante`, `alcabu`, `r205` depressão; `pesorake2025` | Aberto (licença não declarada) | Real | BAIXADO em `vigitel_2006_2024` |
| R1 Siebers 2024 (digital nightlife) | Holanda, 2020 | 155 × 21 dias (1.806 noites) | `sleep_qual` (O 1–7) | `prebed_use`, `postbed_use`, `daytime_use` (C, logging por app) | nenhuma | Aberto, CC BY 4.0 | Real | BAIXADO em `repo_figshare_siebers2024_nightlife` |
| R2 Xuzhou SAS-SV × PSQI | China, 2025 | 2.317 | `PSQI` total (C; 0–18 observado), componentes (O) | `SAS` SAS-SV (C 10–60), itens (O), `time` (O, sem rótulo) | sexo, série, região, renda, IMC, `Pss` | Aberto, CC BY 4.0 | Real | BAIXADO em `repo_figshare_xuzhou_sassv_psqi_china` |
| R3 Rede SA × sono | China, s/ano | 1.842 | `PSQI1`–`PSQI7` (O 0–3) | `SA1`–`SA10` (O 1–6) | nenhuma | Aberto, CC BY 4.0 | Real (declarado) | BAIXADO em `repo_figshare_network_sassv_psqi_china` |
| R4 Redes sociais × PSQI (MBBS/BDS) | Paquistão, 2023-24 | 364 | `PSQI_Global_Score` (C), `Q27` latência min (C), `Q29` h sono (C) | `Q13` uso diário (O), `Q21` última hora antes de dormir (O), `Q23` celular ao dormir (O), `Q24` checa ao acordar (O) | idade, sexo, ano, alojamento, nota | Aberto, CC BY 4.0 | Declarado real; padrões atípicos no arquivo | BAIXADO em `repo_figshare_socialmedia_psqi_paquistao` |
| R5 Dependência × procrastinação do sono (3 ondas) | China, s/ano | 376 | `T*Average score for BPS` (C) — procrastinação, não sono | `T*Average score for MPA` (C) | atividade física; `Q1`–`Q4` sem rótulo | Aberto, CC BY 4.0 | Real | BAIXADO em `repo_figshare_mpa_bedtimeproc_adolesc_china` |
| R6 Smartphone × insônia, medicina | Peru, 2020 | 370 | `insomnia_nosi` (B, do ISI) | `addiction_dependence` (O 0–2) | idade, sexo, depressão (B), ansiedade (B), IMC | Aberto, CC BY 4.0 | Real | BAIXADO em `repo_figshare_smartphone_isi_medicina_peru` |
| R7 Pérez-Chada (tela e sono adolescentes) | Argentina, 2019 | 4.115 brutos; 864 completos | latência min (C), duração semana/fds (C), PDSS (C), `somno01pdss` (B) | tela antes de dormir h (C), tela total h/dia (C), por atividade (C), TV/computador na hora de dormir (B) | idade, sexo, escolaridade dos pais, IMC, domicílio | Aberto, CC BY 4.0 | Real | BAIXADO em `repo_mendeley_screen_sleep_adolesc_argentina` |
| R8 Ibadan (sono e tela adolescentes) | Nigéria, s/ano | 270 | `GLOBALPSQI` (C), `hwlngdoutofallslp` latência min (C), `hrsofslp` (C), `sleepquality` (B) | `smartweekday_hrspt`, `tvweekday_hrspt`, `laptopweekday_hrspt`, `totalhrspent_screen` (C, em **minutos**), uso noturno | local, idade, sexo, escolaridade/ocupação dos pais | Aberto, CC BY 4.0 | Real | BAIXADO em `repo_mendeley_sleep_screen_adolesc_nigeria` |
| R9 Doomscrolling × sono | Turquia, s/ano | 1.216 | `puki_toplam` PSQI (C), `sleep_latency_numeric` (C), `sleep_duration_numeric` (C) | `FK_TOPLAM` (C, provável Doomscrolling Scale; sem codebook) | `S1` idade; ansiedade/depressão | Aberto, CC BY 4.0 | Real (declarado) | BAIXADO em `repo_mendeley_doomscrolling_sleep_turquia` |
| R10 Student Insomnia (DIU) | Bangladesh, 2024 | 996 (v2) / 791 (v1) | 4 itens ordinais em texto | item 11 dispositivos antes de dormir (O 5) | ano, sexo, cafeína, atividade física, estresse | Aberto, CC BY 4.0 | Declarado real; indícios de preenchimento automatizado | BAIXADO em `repo_mendeley_student_insomnia_bangladesh` |
| R11 Sleep Patterns of College Students | não informado, 2026 | 2.722 + 1.222 | h sono, horário, qualidade (O) | celular antes de dormir (O 5) | faixa etária, ano, estudo noturno | Aberto, CC BY 4.0 | Procedência não documentada | BAIXADO em `repo_mendeley_sleep_patterns_college` |
| R12 Okajima (procrastinação × celular) | Japão, s/ano | 381 | `AIStotal` Athens Insomnia (C 8–32), `SDI_wd`/`SDI_we` h sono (C) | `mphone` h de celular nas 3 h antes de dormir (C 0–3) | idade, sexo, cronotipo, bem-estar | Aberto, CC BY 4.0 | Real | BAIXADO em `repo_zenodo_okajima_bedtime_procrastination_japao` |
| R13 Safaria (sono × smartphone) | Indonésia, s/ano | 672 | `Sleep` escore (C 9–36) | `Smartphone` (C), `Nomo` (C) | sexo, idade (categ.), relação com pais | Aberto, CC BY 4.0 | Real | BAIXADO em `repo_zenodo_safaria_sleep_smartphone_indonesia` |
| R14 Digital Screen Exposure (universitários) | Indonésia, 2026 | 105 | 2 itens Likert (O 1–5) | 9 itens Likert de uso antes de dormir/na cama (O) | faixa etária, curso, semestre | Aberto, CC BY 4.0 | Real (Google Forms) | BAIXADO em `repo_zenodo_screen_sleep_univ_indonesia` |
| Add Health (Wave I public-use) | EUA, 1994-95 | 6.504 | `H1GH51` h sono (C), `H1GH52` (B), `H1GH18` dificuldade para dormir (O 0–4) | `H1DA8` TV, `H1DA9` vídeo, `H1DA10` games/computador h/semana (C) | `BIO_SEX`, idade, raça, CES-D; pesos à parte | Termo de uso / conta gratuita | Real | NÃO BAIXADO |
| ABCD Study | EUA, 2016– | 11.880 (9–10 anos na entrada) | `ph_p_sds` (SDSC), `ph_y_mctq` (C) | `nt_y_stq__screen__wkdy__hr_001__01` etc. (C); EARS | amplas | DUA institucional (NBDC) | Real | NÃO BAIXADO |
| NSRR — SHINE / STAGES / FFCWS | EUA | 433 / ~1.500–1.881 / 923 | actigrafia, `isi_score`, latência | `devicebeforebed_mom` etc. (O 1–4); `bthbts_0300` (O 0–3); diário de mídia | — | DAUA (conta + comitê) | Real | NÃO BAIXADO |
| ERICA | Brasil, 2013-14 | ~85.000 (12–17) | horários de dormir/acordar (códigos não verificados) | horas de tela (não verificado) | dieta, antropometria, AF | Sem arquivo público | Real | NÃO BAIXADO |
| ELSA-Brasil | Brasil, 2008–2014 | 15.105 (35–74) | duração, insônia, actigrafia (não verificados) | tela no lazer/trabalho, onda 2 (não verificado) | amplas | Proposta aprovada | Real | NÃO BAIXADO |
| Coortes de Pelotas (2004, 1993) | Brasil | 1.851 (2004, 15 anos) | MCTQ duração, qualidade (não verificados) | TV, computador, tablet/celular, console h/dia (não verificado) | amplas | Aplicação aos pesquisadores | Real | NÃO BAIXADO |
| UK Biobank | Reino Unido, 2006– | ~501 mil | campo 1160 duração (C), 1200 insônia (O) | 1070 TV, 1080 computador h/dia (C) | amplas | Pago + aplicação | Real | NÃO BAIXADO |
| HBSC | ~40 países, 2001/02–2017/18 | não verificado | `sleepdifficulty` (O 1–5) | `tvwd`/`tvwe`, `playgamewd`/`we`, `compusewd` (O) | — | Pedido por formulário | Real | NÃO BAIXADO |
| SHoT 2018/2022 | Noruega | 49.051 / ~45.202 | insônia DSM-5 (B), duração, latência (C) | mídia após deitar min/noite (C) | idade, sexo | Ética + pedido ao NIPH | Real | NÃO BAIXADO |
| Millennium Cohort Study (MCS6) | Reino Unido, 2015 | 11.872 (14 anos) | horários, latência (códigos não verificados) | TV, internet, games, redes sociais; diário de tempo | pesos | Cadastro gratuito + licença (UKDS) | Real | NÃO BAIXADO |
| openICPSR E193588 | provável China (não verificado) | 508 | PSQI | uso de smartphone | — | Login gratuito openICPSR | Real | NÃO BAIXADO |
| Gamers Wave 1–3 (Harvard Dataverse) | Austrália | não verificado | actigrafia Fitbit | uso problemático smartphone/games; AWARE | — | DUA | Real | NÃO BAIXADO |
| Kaggle "Sleep Pattern" | Índia, 2021 | 46 | sono | h de celular, filtro de luz azul | — | Login Kaggle | Real (survey) | NÃO BAIXADO |
| Kaggle "StudentLife" | EUA (Dartmouth) | 48 | EMA de sono | sensoriamento do celular | — | Login + 3,04 GB | Real | NÃO BAIXADO |
| IEEE DataPort "Sleep Schedule…" | não informado | 3.000 | qualidade do sono | celular antes de dormir | — | Login/assinatura | Procedência não documentada | NÃO BAIXADO |
| ETRI Lifelog 2024 | Coreia do Sul | 10 ou 50 | sensor de sono + autorrelato | smartphone/smartwatch | — | License Agreement | Real | NÃO BAIXADO |
| YRBS 2023 | EUA, 2023 | não verificado | `Q85` h sono (O) | `Q80` redes sociais (O) | idem YRBS | Aberto | Real | NÃO BAIXADO (aberto; mesmo desenho de 2025) |

---

## 2. Fichas das fontes baixadas

### 2.1 NHANES (CDC/NCHS, EUA) — 4 ciclos

Fonte: https://wwwn.cdc.gov/nchs/nhanes/ · codebooks por arquivo em `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/<ano>/DataFiles/<ARQ>_<sufixo>.htm` (cópia `.htm` baixada junto de cada `.xpt`). Acesso aberto, sem cadastro; arquivos public-use (uso sujeito às restrições do NCHS contra reidentificação). Real. Unidade: pessoa; arquivos ligados por `SEQN`.

**Mapa de ciclos (conferido nos codebooks):**

| Ciclo | Sono (SLQ, ≥16 anos) | Tela (PAQ) | Sobreposição tela × sono em ≥16 anos |
|---|---|---|---|
| 2005-2006 (D) | completo: `SLD010H`, **`SLD020M` (latência, min)**, `SLQ050`, `SLQ060`, `SLQ070A-D`, `SLQ080`–`SLQ160`, `SLQ170`–`SLQ240` | `PAD590` (TV/vídeo h/dia), `PAD600` (computador/games h/dia), **2–150 anos** | **sim** |
| 2007-2008 (E) | completo (igual ao D, inclui `SLD020M`) | `PAD590`/`PAD600` só **2–11 anos**; ≥12 só `PAD680` (min sentado) | não (descartado) |
| 2009-2010 (F) | curto: `SLD010H`, `SLQ050`, `SLQ060` | `PAD590`/`PAD600` só 2–11 anos | não (descartado) |
| 2011-2012 (G) | curto: `SLD010H`, `SLQ050`, `SLQ060` | `PAQ710` (TV), `PAQ715` (computador), 2–150 anos | **sim** |
| 2013-2014 (H) | curto: `SLD010H`, `SLQ050`, `SLQ060` | `PAQ710`, `PAQ715`, 2–150 anos | **sim** |
| 2015-2016 (I) | `SLQ300`/`SLQ310` (hora de dormir/acordar, HH:MM), `SLD012` (h sono dia útil), `SLQ030`, `SLQ040`, `SLQ050`, `SLQ120` (sonolência diurna) | `PAQ710`, `PAQ715`, 2–150 anos | **sim** |
| 2017-2018 (J) | `SLQ300`–`SLQ330`, `SLD012`, `SLD013`, `SLQ030`, `SLQ040`, `SLQ050`, `SLQ120` | só `PAD680` (min sentado; TV/computador citados como exemplo) | não (descartado) |
| 2021-2023 (L) | — | só `PAD680` (PAQ_L) | não (descartado) |

Em todos os ciclos D–I há também `DPQ030` (PHQ-9: "dificuldade para pegar no sono ou permanecer dormindo, ou dormir demais", 0–3, ≥18 anos).

Codebooks usados: SLQ_D, SLQ_E, SLQ_F, SLQ_G, SLQ_H, SLQ_I, SLQ_J; PAQ_D, PAQ_E, PAQ_F, PAQ_G, PAQ_H, PAQ_I, PAQ_J, PAQ_L; DPQ_D (todos em `.../Public/<ano>/DataFiles/<arq>.htm`).

**Arquivos baixados (cada pasta: DEMO, SLQ, PAQ, DPQ, DR1TOT, BMX em `.xpt` + `.htm`):**

| Pasta | Tamanho | SLQ (linhas×col) | PAQ | DEMO | DPQ | DR1TOT | BMX | SLQ∩PAQ (≥16) | n com Y e X válidos |
|---|---|---|---|---|---|---|---|---|---|
| `nhanes_2005_2006` | 21,9 MB | 6.139×28 | 9.424×20 | 10.348×43 | 5.334×11 | 9.950×160 | 9.950×27 | 6.139 (16–85 anos) | 6.091 (`SLD020M`+`PAD590`+`PAD600`) |
| `nhanes_2011_2012` | 20,2 MB | 6.175×4 | 9.107×21 | 9.756×48 | 5.615×11 | 9.338×166 | 9.338×26 | 6.175 (16–80) | 6.152 (`SLD010H`+`PAQ710`+`PAQ715`) |
| `nhanes_2013_2014` | 26,8 MB | 6.464×4 | 9.484×96 | 10.175×47 | 5.924×11 | 9.813×168 | 9.813×26 | 6.464 (16–80) | 6.451 (`SLD010H`+`PAQ710`+`PAQ715`) |
| `nhanes_2015_2016` | 26,2 MB | 6.327×8 | 9.255×94 | 9.971×47 | 5.735×11 | 9.544×168 | 9.544×26 | 6.327 (16–80) | 6.280 (`SLD012`+`PAQ710`+`PAQ715`) |

**Variáveis confirmadas presentes no arquivo:** as de sono e tela da tabela de ciclos; em DEMO `RIDAGEYR` (idade), `RIAGENDR` (sexo), `INDFMPIR` (razão renda/pobreza), `DMDEDUC2` (escolaridade ≥20 anos), `RIDRETH1` (raça/etnia), pesos `WTINT2YR`/`WTMEC2YR`, desenho `SDMVPSU`/`SDMVSTRA`; `DR1TCAFF` (cafeína, mg, recordatório 24h) em DR1TOT; `BMXBMI` em BMX; `DPQ010`–`DPQ090` (PHQ-9) em DPQ.

**Tipos e códigos (conferidos):**
- `SLD020M` (2005-06): minutos 0–59, **60 = 60 ou mais** (topo censurado), 77 recusa, 99 não sabe. Distribuição concentrada em 5/10/15/30/60 (arredondamento de resposta). Contínua censurada.
- `SLD010H`: horas inteiras 1(ou 2)–11, **12 = 12 ou mais**, 77/99. `SLD012` (2015-16): horas em passos de 0,5 (2–14,5), sem 77/99.
- `SLQ080`–`SLQ160`, `SLQ120`: ordinal 0 Nunca … 4 Quase sempre (16–30×/mês); 7/9. `SLQ050`/`SLQ060`: binária 1 sim / 2 não; 7/9.
- `SLQ300`/`SLQ310` (2015-16): texto "HH:MM" (lido como bytes pelo pandas); 77777/99999 recusa/não sabe.
- `PAD590`/`PAD600` (2005-06): **0 = menos de 1 h**, 1…4 h, **5 = 5 h ou mais**, **6 = nenhuma**, 77/99. `PAQ710`/`PAQ715` (2011-16): 0 = <1 h, 1…4, 5 = ≥5 h, **8 = não assiste/não usa**, 77/99. Ordinal; o código "nenhuma" (6 ou 8) fica fora da ordem numérica e precisa ser recodificado antes de qualquer uso como número.
- `DPQ030`: 0–3; 7/9.

**Observações:**
- O pandas `read_sas` devolve o valor 0 como `5.397605346934028e-79` (artefato do formato XPT); arredondar.
- Pesos: questionário domiciliar (SLQ/PAQ/DPQ) usa `WTINT2YR`; dieta (DR1TOT) usa `WTDRD1`; desenho complexo com `SDMVPSU` + `SDMVSTRA`.
- `PAQ715` mede computador/games "fora da escola"; não há pergunta de uso na cama/antes de dormir em nenhum ciclo.
- `DPQ` só ≥18 anos e só quando a entrevista foi feita com a própria pessoa (`DPQ001`).

### 2.2 PNS 2019 — Pesquisa Nacional de Saúde (IBGE, Brasil)

Fonte: https://ftp.ibge.gov.br/PNS/2019/Microdados/ ("Todos os arquivos aqui disponíveis são públicos"). Acesso aberto, sem cadastro. Real. Unidade: morador; módulos N e P só para o **morador selecionado (≥15 anos)**.

- Arquivos (`pns_2019\`): `PNS_2019_20220525.zip` (29.512.476 B), `Dicionario_e_input_20220530.zip` (172.422 B), `Chaves_PNS_2019.pdf`, `historico_de_atualizacoes_20220525.txt`. Extraído em `extraido\`: `PNS_2019.txt` (455.275.300 B, largura fixa, LRECL 1548), `dicionario_PNS_microdados_2019.xls`, `input_PNS_2019.sas`/`.txt` (posições).
- Conferido no arquivo: **293.726 linhas** (todos os moradores) × **1.088 variáveis** no layout. `M001 = 1` (entrevista do morador selecionado realizada): **90.846**, idade 15–107. Todos os 90.846 têm `N010`, `P04501` e `P04502` preenchidos e ≠ 9.
- **Y:** `N010` (pos. 564) — "Nas duas últimas semanas, com que frequência o(a) Sr(a) teve problemas no sono, como dificuldade para adormecer, acordar frequentemente à noite ou dormir mais do que de costume?" 1 Nenhum dia / 2 Menos da metade dos dias / 3 Mais da metade / 4 Quase todos os dias / 9 Ignorado. Ordinal (item 3 do PHQ-9). Distribuição: 58.090 / 16.039 / 5.773 / 10.944. Relacionados: `N011` (cansaço/sem energia, mesma escala), `Q132` (usou medicamento para dormir nas 2 últimas semanas, 1 sim/2 não), `Q133` (dias de uso).
- **X:** `P04501` (pos. 705) — horas/dia assistindo TV: 1 <1 h, 2 1–<2 h, 3 2–<3 h, 4 3–<6 h, 5 ≥6 h, **6 não assiste**, 9 ignorado. `P04502` (pos. 706) — horas do tempo livre usando **computador, tablet ou celular para lazer** (redes sociais, notícias, vídeos, jogos): mesmas faixas, **6 não costuma usar**. Ordinais com faixas desiguais.
- **Covariáveis confirmadas:** `C006` sexo, `C008` idade, `C009` cor/raça, `VDD004A` escolaridade (7 níveis), `VDF003` renda domiciliar per capita (R$), `V0026` urbano/rural, `V0001` UF, `J001` autoavaliação de saúde, `P034` exercício nos últimos 3 meses, `P050` tabagismo, `P027` álcool, `Q092` diagnóstico de depressão.
- Desenho: peso `V00291` (morador selecionado, calibrado), estrato `V0024`, UPA `UPA_PNS`. Branco = não aplicável; 9 = ignorado.
- Não há pergunta de uso de tela na cama/antes de dormir, nem duração/latência do sono.

### 2.3 PNS 2013 (IBGE, Brasil)

Fonte: https://ftp.ibge.gov.br/PNS/2013/Microdados/. Aberto, sem cadastro. Real. Morador selecionado **≥18 anos**.

- Arquivos (`pns_2013\`): `PNS_2013.zip` (20.519.716 B), `Dicionario_e_input_20200930.zip` (139.560 B), `Questionario_PNS_2013.pdf`, `Chaves_PNS_2013.pdf`, `historico_atualizacao_microdados_PNS_2013_20200825.txt`. Extraído: `PNS_2013.txt` (330.464.110 B, LRECL 1484), dicionário `.xls`, input SAS.
- Conferido: **222.385 linhas** × **1.000 variáveis** no layout; `M001 = 1`: **60.202** (18–101 anos), todos com `N010` e `P045` preenchidos.
- **Y:** `N010` (pos. 560), mesma pergunta e escala de 2019 (sem código 9 observado). `N011`, `Q132` também presentes.
- **X:** só TV — `P045` (pos. 709): 1 <1 h, 2 1–<2, 3 2–<3, 4 3–<4, 5 4–<5, 6 5–<6, 7 ≥6 h, **8 não assiste**. **Não há** pergunta de computador/tablet/celular em 2013.
- Covariáveis: `C006`, `C008`, `VDD004A`, `VDF003` confirmadas; peso `V00291`, estrato `V0024`, UPA `UPA_PNS`.

### 2.4 PeNSE 2015 — Pesquisa Nacional de Saúde do Escolar (IBGE, Brasil)

Fonte: https://ftp.ibge.gov.br/pense/2015/microdados/. Aberto, sem cadastro. Real. Unidade: aluno (questionário autoaplicado).

- Arquivos (`pense_2015\`): `PeNSE_2015_AMOSTRA1.zip` (226.818.475 B), `PeNSE_2015_AMOSTRA2.zip` (39.081.033 B), `atualizacoes_20180525.txt`, `Nota_metodologica_01_utilizacao_microdados_20180514.pdf`. Extraído: Amostra 2 completa em `extraido\AMOSTRA2\` (CSV, SAS7BDAT, XLSX, dicionário); da Amostra 1 só os 3 CSV + dicionário em `extraido\AMOSTRA1\` (os SAS/XLSX somam ~770 MB e são cópias do mesmo conteúdo).
- **Amostra 1** (alunos do 9º ano do EF): `PENSE_AMOSTRA1_ALUNO.CSV` **102.072 × 174**; idade 11–19 (moda 14). n com Y e os dois X válidos: **101.089**.
- **Amostra 2** (alunos de 13–17 anos, 6º ano EF ao 3º EM): `PENSE_AMOSTRA2_ALUNO.CSV` **16.556 × 181**; idade 11–19. n válido: **16.407**.
- **Y:** `VB12002` — "NOS ÚLTIMOS 12 MESES, com que frequência você não conseguiu dormir à noite porque algo o(a) preocupava muito?" 1 Nunca … 5 Sempre; 99 não informado. Ordinal. É a única variável de sono da PeNSE 2015 (não há duração nem latência).
- **X:** `VB03009A` — horas/dia de TV em dia de semana: 1 não assiste, 2 até 1 h, 3 >1–2 h … 9 >7–8 h, 10 >8 h; 99. `VB03010A` — tempo sentado em dia de semana assistindo TV, usando computador, videogame, conversando ou outras atividades sentado (exclui escola): 1 até 1 h … 9 >8 h; 99. Ordinais. `VB03010A` mistura tela com outras atividades sentado.
- Covariáveis confirmadas: `VB01001` sexo, `VB01002` cor/raça, `VB01003` idade, `VB01008A` escolaridade da mãe, `VB01010A` pessoas no domicílio, `VB01014` tem celular, `VB01015A` computador em casa, `VB01016` internet em casa, `VB03011A` dias com ≥60 min de atividade física; módulos de álcool, tabaco, drogas, saúde mental (`VB12xxx`).
- Desenho: `PESO` (decimal com vírgula), `ESTRATO_EXP`, `ESTRATOGEOREG`, `escola`, `turma`. Separador `;`, encoding latin-1. 99 = não informado; −1 = pulo.

### 2.4b Vigitel 2006–2024 (Ministério da Saúde, Brasil) — módulo de sono só em 2024

Fonte: https://svs.aids.gov.br/daent/cgdnt/vigitel/ · dicionário `dicionario-vigitel-2006-2024.xlsx` (mesma página). Aberto, sem login; licença não declarada na página. Real. Inquérito telefônico, adultos ≥18 anos das 27 capitais. Unidade: entrevistado.

- Arquivos (`vigitel_2006_2024\`): `vigitel-2006-2024-peso-rake-csv.zip` (87.121.523 B) contendo `vigitel-2006-2024-peso-rake_slabel.csv` (577.433.824 B descompactado; **não extraído** — lido direto do zip em blocos); `dicionario-vigitel-2006-2024.xlsx` (93.263 B).
- Conferido no arquivo: **833.217 linhas × 486 colunas** (todas as edições 2006–2024 empilhadas, variável `ano`). **2024: 27.048 linhas**; as variáveis `r70x` só existem em 2024. Em 2024: `r701_hh` não nulo em 26.939; `r703`/`r704`/`r705` em 27.048; `r703` e `q59a` juntos em 27.048; `r703` e `q59c` juntos em 21.250 (`q59c` é pulada quando `q59b` = 2).
- **Y:** `r701_hh` + `r701_mm` (duração habitual do sono; duração = `r701_hh + r701_mm/60`; `r701_hh` 0–15, 109 NaN) (C); `r702_hh`/`r702_mm` sono desejado (C); `r703` dificuldade para dormir, `r704` acordou e teve dificuldade de voltar a dormir, `r705` acordou antes da hora e não voltou a dormir (O 1 nunca … 5 sempre; distribuição de `r703` em 2024: 8.641 / 6.517 / 5.798 / 2.963 / 3.129); `r706` ronco; `r707` apneia observada; derivada `insonia` (B; fórmula do dicionário: `r703>=4 | r704>=4 | r705>=4`).
- **X:** `q59a` horas/dia de TV (O 1–7, **8 = não assiste**; desde 2010); `q59b` usa computador/tablet/celular no tempo livre (1 sim / 2 não / 777 não sabe; desde 2016); `q59c` horas/dia desse uso (O 1–7; desde 2016); `tempo_tela_total` (B, ≥3 h/dia).
- Covariáveis: `q6` idade, `q7` sexo, `fesc` escolaridade (3 faixas), `q69` cor, `civil`, `cidade`, `imc`, `fumante`, `alcabu`, `r205` diagnóstico de depressão. Peso: `pesorake2025`.
- Observações: não resposta 777 (não sabe) e 888 (não quis responder) em `q59b`, `q69`, `civil`, `r205`; em 2024 `r703`–`r705` só têm 1–5. `sono_curto` consta no dicionário mas não existe no CSV. O dicionário dá a `tempo_tela_stv` e `tempo_tela_total` a mesma fórmula de `tv_d_3` (aparente erro de cópia). `atilaz` vazio em 2024. CSV separado por vírgula, latin-1.

### 2.5 NSCH 2025 e NSCH 2017 — National Survey of Children's Health (HRSA/Census, EUA)

Fonte: https://www.census.gov/programs-surveys/nsch/data/datasets.html · dicionário: https://www.census.gov/data-tools/demo/uccb/nschdict e Variable List 2025 (https://www2.census.gov/programs-surveys/nsch/technical-documentation/codebook/2025-NSCH-Topical-Variable-List.pdf). Aberto, sem cadastro, domínio público. Real. Unidade: criança 0–17 anos, relato do responsável. Microdados existem de 2016 a 2025.

**NSCH 2025** (`nsch_2025\`)
- Arquivos: `nsch_2025_topical_Stata.zip` (5.507.296 B) → `extraido\nsch_2025e_topical.dta` (22.791.468 B) + `nsch_2025_topical.do`; PDFs Variable List (1.690.346 B), Frequencies (3.140.301 B), FAQs (682.685 B).
- Conferido: **45.139 × 458**. FORMTYPE T1 = 12.100, T2 = 13.348, T3 = 19.691. Válidos: `SCREENTIME` 44.305; `HOURSLEEP` 32.644; `HOURSLEEP05` 11.967; `BEDTIME` 44.564.
- **Y:** `HOURSLEEP` (6–17 anos, horas em noite de semana; 1 = <6 h … 7 = 11 h+; ordinal); `HOURSLEEP05` (0–5 anos, horas/dia incluindo cochilos; 1 = <7 h … 7 = 12 h+); `BEDTIME` (vai para a cama no mesmo horário; 1 Always … 5 Never; ordinal).
- **X:** `SCREENTIME` (TV, computador, celular etc. em dia de semana, exceto escola; 1 = <1 h, 2 = 1 h, 3 = 2 h, 4 = 3 h, 5 = 4 h+; ordinal). Não há item de dispositivo no quarto ou na hora de dormir (busca por "device", "phone", "electronic", "bedroom" no Variable List).
- Covariáveis: `SC_AGE_YEARS`, `SC_SEX`, `SC_RACER`, `HIGRADE` (escolaridade do adulto), `FPL_I1`–`FPL_I6` (razão de pobreza, 6 imputações), `PHYSACTIV` (6–17), `K2Q32A` (depressão), `K2Q33A` (ansiedade).
- Desenho: peso `FWC`; estrato `FIPSST` × `STRATUM` (valores '1'/'2A'; o FAQ orienta recodificar 2A→2); PSU `HHID`. Não resposta como missing especial do Stata (.m, .n, .l, .d) → NaN no pandas. Renda em 6 imputações.

**NSCH 2017** (`nsch_2017\`) — ano com TV separada de dispositivos
- Arquivos: `nsch_2017_topical_Stata.zip` (2.715.174 B) → `extraido\nsch_2017e_topical.dta` (10.365.207 B) + `.do`; Variable List (2.826.634 B); FAQs (530.657 B).
- Conferido: **21.599 × 436**. Válidos: `K7Q60_R` 21.399; `K7Q91_R` 21.402; `HOURSLEEP` 15.253.
- **Y:** `HOURSLEEP`, `HOURSLEEP05`, `BEDTIME` (mesmas escalas de 2025).
- **X:** `K7Q60_R` (TV/vídeos/videogame na TV) e `K7Q91_R` (computador, celular, videogame portátil e outros dispositivos, exceto escola); ambos 1 = None, 2 = <1 h, 3 = 1 h, 4 = 2 h, 5 = 3 h, 6 = 4 h+.
- Não verificado: em que ano entre 2018 e 2024 os dois itens foram fundidos em `SCREENTIME`.

### 2.6 YRBS nacional 2021 e 2025 + ABES 2021 (CDC, EUA)

Fonte: https://www.cdc.gov/yrbs/data/index.html e https://www.cdc.gov/healthyyouth/data/abes/data.htm · codebook: Data User's Guide de cada ano (ex.: https://www.cdc.gov/yrbs/files/2021/pdf/2021_YRBS_Data_Users_Guide_508.pdf) + programas SAS de input/formats (posições). Aberto, sem cadastro, domínio público. Real. Unidade: estudante do 9º ao 12º ano. Arquivo `.dat` ASCII de largura fixa, lido com `pandas.read_fwf` pelas posições do SAS input. Observação de acesso: www.cdc.gov e www.bls.gov respondem 403 a `curl` com UA simples; o download funcionou com UA completo de navegador e cabeçalhos `Accept`/`Sec-Fetch-*`.

**YRBS 2021** (`yrbs_2021\`; coleta no outono de 2021)
- Arquivos: `XXH2021_YRBS_Data.dat` (7.289.136 B), `2021XXH-SAS-Input-Program.sas` (17.031 B), `2021XXH-Formats-Program.sas` (17.121 B), User's Guide (2.215.399 B).
- Conferido: **17.232 × 237**. Válidos: `Q78` 16.496; `Q86` 13.615.
- **Y:** `Q86` horas de sono em noite de escola (1 = ≤4 h, 2 = 5 h, 3 = 6 h, 4 = 7 h, 5 = 8 h, 6 = 9 h, 7 = 10 h+; ordinal); `QN86` = 8 h ou mais (binária 1 sim / 2 não).
- **X:** `Q78` "screen time" em dia de escola (TV, computador, smartphone, outro dispositivo; exclui escola; 1 = <1 h … 6 = 5 h+; ordinal); `QN78` = 3 h ou mais (binária).
- Covariáveis: `Q1` idade, `Q2` sexo (1 F, 2 M), `Q3` série, `RACEETH`, `Q25` tristeza/desesperança, `Q85` saúde mental atual, `Q77` dias de atividade física, `BMIPCT`, substâncias, refrigerante. Sem renda.
- Desenho: `WEIGHT` (escalado para somar n), `STRATUM` (16), `PSU` (57). Missing = campo em branco (sem códigos 7/9).

**YRBS 2025** (`yrbs_2025\`)
- Arquivos: `XXH2025_YRBS_Data.dat` (4.594.590 B), SAS Input (18.876 B), Formats (18.092 B), User's Guide (802.320 B).
- Conferido: **10.710 × 251**. Válidos: `Q77` 9.860; `Q83` 8.725. `STRATUM` 14, `PSU` 55. Missing em branco.
- **Y:** `Q83` horas de sono em noite de escola (escala 1–7 como 2021); `QN83` ≥8 h.
- **X:** `Q77` frequência de uso de redes sociais (1 não usa … 6 várias vezes/dia, 7 ~1×/hora, 8 >1×/hora; ordinal); `QN77`. **Não há mais item de horas de tela.**
- Covariáveis: `Q1`, `Q2`, `Q3`, `RACEETH` (9 categorias, novo esquema), `Q73` atividade física, `Q81` saúde mental, `Q105` dificuldade de concentração, bebidas.
- YRBS 2023: não baixado (mesmo desenho de conteúdo de 2025; SAS input tem `Q80` redes sociais e `Q85` sono). n de 2023 não verificado.

**ABES 2021** (`abes_2021\`; Adolescent Behaviors and Experiences Survey, online, jan–jun 2021)
- Arquivos: `ABEH2021_5_RECRUIT.dat` (3.374.790 B), `2021ABEH-SAS-Input-Program-w-5-recruit-variables.sas` (20.486 B), Formats (19.855 B), `2021_ABES_Data_Users_Guide.pdf` (3.677.012 B).
- Conferido: **7.705 × 275**. Válidos: `Q78` 7.210; `Q86` 7.074.
- Y/X: `Q86`/`QN86` e `Q78`/`QN78`, como no YRBS 2021. Covariáveis extras: `Q100`–`Q111` (COVID: saúde mental, perda de emprego dos pais, insegurança alimentar, "virtual connectedness"), `Q85`, `Q115`.
- Desenho: `WEIGHT`, `STRATUM` (16), `PSU` (70). Nas variáveis QN o missing vem como "." (não em branco).

### 2.7 ATUS 2025 — American Time Use Survey (BLS, EUA)

Fonte: https://www.bls.gov/tus/data/datafiles-2025.htm · dicionários https://www.bls.gov/tus/dictionaries/atusintcodebk25.pdf e `atuscpscodebk25.pdf` · lexicon https://www.bls.gov/tus/lexicons/lexiconwex2025.xls. Aberto, domínio público. Real. Unidade: respondente 15–85 anos, um diário de 24 h (4h–4h).

- Arquivos (`atus_2025\`, bytes): `atusresp-2025.zip` 429.058; `atusact-2025.zip` 1.882.541; `atussum-2025.zip` 383.733; `atusrost-2025.zip` 78.890; `atuscps-2025.zip` 5.637.745; dicionários PDF, `lexiconnoex2025.pdf`, `lexiconwex2025.xls`. Extraídos em `extraido\<zip>\`: `.dat` em CSV com cabeçalho (+ programas .do/.sas/.sps, não executados).
- Conferido: Summary **6.146 × 377**; Respondent 6.146 × 175; Activity **114.151 episódios × 30**; Roster 15.052 × 8; CPS 62.891 × 385 (inclui domicílios não respondentes).
- **Y (contínuas, min/dia):** `t010101` Sleeping (média 541,7); `t010102` Sleeplessness ("insomnia, lying awake, tossing and turning"; 5,2% com valor > 0); `t010199` Sleeping n.e.c.
- **X (contínuas, min/dia):** `t120303` TV e filmes (média 185,1); `t120304` TV religiosa; `t120307` Playing games (inclui jogos de tabuleiro/cartas — não é só tela); `t120308` Computer use for leisure (inclui internet e redes sociais).
- Sequência de episódios no Activity (`TUACTIVITY_N`, `TUSTARTTIM`, `TUSTOPTIME`, `TUACTDUR24`, `TRCODE`) permite derivar tela imediatamente antes de dormir: 2.794 de 6.146 pessoas têm episódio 1203xx seguido de 010101; 320 pessoas têm episódio 010102.
- Covariáveis: `TEAGE`, `TESEX`, `PEEDUCA` (31–46), `PTDTRACE`, `TELFS`, `TRCHILDNUM`, `TUDIARYDAY`, `TRHOLIDAY`, `TRERNWA`, `TEHRUSLT`; `HEFAMINC` (renda familiar) no arquivo CPS.
- Observações: `TUFINLWGT` em escala pessoa-dia (1,48e6 a 2,70e8); pesos replicados (`atuswgts`, 7,4 MB) não baixados. Não resposta: −1 blank, −2 don't know, −3 refused. Só a atividade primária é codificada (uso de celular simultâneo não aparece). Sem módulo de saúde/bem-estar em 2025.

### 2.8 Repositórios abertos (Figshare, Mendeley Data, Zenodo) — 14 datasets

Todos com licença **CC BY 4.0**, download direto sem login. Cada pasta tem `_<repo>_metadata.json` com o JSON da API do repositório (licença, descrição). Observação de acesso: Figshare e Zenodo devolveram 403 com `-A "Mozilla/5.0"`; o download funcionou com o user agent padrão do curl. Os `.sav` foram lidos com `pyreadstat` (instalado com `pip --user` durante a tarefa).

**R1. Siebers et al. 2024 — "Adolescents' digital nightlife"** (`repo_figshare_siebers2024_nightlife\`)
- Dataset https://doi.org/10.21942/uva.26395903.v2 (UvA Figshare) · artigo 10.1177/00936502241276793 (Communication Research). Holanda, 2020. Real.
- 155 adolescentes × 21 dias (1.806 noites válidas). Painel longo (`user_id` × `study_day`).
- Arquivos (bytes): `phone.csv` 138.369 (3.255×6), `social.csv` 132.177 (3.255×6), `video.csv` 112.959 (3.255×6), `game.csv` 84.916 (2.814×6; 134 usuários), `timeframes.csv` 231.880 (1.859×9: hora de deitar/acordar, `sleep_qual`).
- Y: `sleep_qual` (1–7, item único diário, ordinal). X: `daytime_use`, `prebed_use` (horas na hora antes de deitar; máx. 1,0), `postbed_use` (horas após deitar) — **registrados por app (logging), não autorrelato**; contínuas; por tipo (celular, redes sociais, vídeo, games).
- Sem covariáveis (sem idade/sexo). Faltante = **−999**; valores 88/99 que aparecem são IDs de usuário.

**R2. Xuzhou Medical University — SAS-SV + PSQI** (`repo_figshare_xuzhou_sassv_psqi_china\`)
- https://doi.org/10.1371/journal.pone.0340852.s001 · artigo 10.1371/journal.pone.0340852. China, mar/2025. Real.
- `pone.0340852.s001.xlsx` (607.604 B): **2.317 × 59**, sem NaN.
- Y: `PSQI` total (0–18 observado, contínua), `PSQI classification` (1/2), itens/componentes do PSQI (`@2...minutes...falling asleep` é **componente 0–2, não minutos**; `@3Actual sleep time` componente 0–3; hora de deitar em 4 categorias).
- X: `SAS` (SAS-SV, 10–60, contínua), `SAS_AV` (1/2), itens SAS 1–10; `time` (1–5, sem rótulo no arquivo; tempo de uso do celular — não verificado); `aoye` (0/1, sem rótulo).
- Covariáveis: gender, grade, region, child, economic, profess, altura, peso, IMC, `Pss` (estresse percebido). O HPLP-II citado no artigo não está no arquivo.

**R3. Rede SA × sono, universitários chineses** (`repo_figshare_network_sassv_psqi_china\`)
- https://doi.org/10.6084/m9.figshare.32109184.v1 · artigo não indicado. China, ano não informado. Real (declarado).
- `Original_data.xlsx` (140.656 B): **1.842 × 17**, sem NaN.
- Y: `PSQI1`–`PSQI7` (componentes 0–3; o total precisa ser somado). X: `SA1`–`SA10` (itens SAS-SV, 1–6). Sem covariáveis.

**R4. Redes sociais, checagem noturna e PSQI — estudantes MBBS/BDS** (`repo_figshare_socialmedia_psqi_paquistao\`)
- https://doi.org/10.6084/m9.figshare.32521821.v1 · artigo provável do mesmo estudo 10.3389/fpubh.2026.1968305 (n = 364, Khyber Pakhtunkhwa). Paquistão, out/2023–abr/2024.
- `Social_Media_Article_Complete_Data.xlsx` (168.540 B): **364 × 94**, sem NaN.
- Y: `PSQI_Global_Score` (3–15), `PSQI_Category`, `Q27_Sleep_latency_minutes` (5–70, contínua), `Q29_Actual_sleep_hours` (3,6–7,9), itens Q30–Q34.
- X: `Q13_Daily_social_media_use_6band`, `Q21_SM_last_hour_before_sleep` (4 faixas), `Derived_Screen_duration_before_sleep_3band`, `Q23_Phone_while_sleep`, `Q24_Check_SM_if_wake_at_night` (ordinais em texto).
- Covariáveis: idade, sexo, ano, programa, tipo de instituição, alojamento, nota de prova.
- Declarado real, com **padrões atípicos no arquivo**: idade = 26 em 112/364; latências fora do arredondamento típico de autorrelato (31, 35, 38, 42…); horas de sono em passos de 0,1 h; separação perfeita do PSQI entre grupos (mínimo 9 em "Time Pass", máximo 9 em "Academic"); prevalência PSQI > 5 de 79,1% no arquivo vs 85,7% no artigo da Frontiers.

**R5. Dependência de celular × procrastinação do sono, 3 ondas** (`repo_figshare_mpa_bedtimeproc_adolesc_china\`)
- https://doi.org/10.1371/journal.pone.0331340.s001 · artigo 10.1371/journal.pone.0331340. China ("S Province"), 3 ondas com 3 meses de intervalo. Real.
- `pone.0331340.s001.xlsx` (189.157 B): **376 × 115** (alunos do ensino médio).
- Y: `T0/T1/T2Average score for BPS` (Bedtime Procrastination Scale, média 1–5) — **mede procrastinação de ir dormir, não sono**. X: `T0/T1/T2Average score for MPA` (Mobile Phone Addiction, itens `T*SA1-22`).
- Covariáveis: `T*Average score for PAB` (atividade física); `Q1`–`Q4` sem rótulo (Q1 binária, provável sexo; Q4 de 5 dígitos, provável ID — não verificado).

**R6. Dependência de smartphone e insônia em estudantes de medicina** (`repo_figshare_smartphone_isi_medicina_peru\`)
- https://doi.org/10.1371/journal.pone.0329495.s001 · artigo 10.1371/journal.pone.0329495. Peru (Piura), 2020. Real.
- `pone.0329495.s001.dta` (26.613 B): **370 × 12**.
- Y: `insomnia_nosi` (binária, recodificada do ISI; escore ISI não está no arquivo). X: `addiction_dependence` (0/1/2, ordinal).
- Covariáveis: age, sex, `depression_nosi` (PHQ, binária), `anxiety_nosi` (GAD-7, binária), `dx_nutritional` (IMC), `fmortcovid`, `single`. Só versões recodificadas.

**R7. Pérez-Chada et al. — tela e sono em adolescentes** (`repo_mendeley_screen_sleep_adolesc_argentina\`)
- https://doi.org/10.17632/pj9hzmp7ym.1 · artigo 10.1371/journal.pone.0281379. Argentina, 2019. Real.
- `repositorio.xlsx` (4.682.126 B): **4.115 × 123** linhas brutas, 35.326 células NaN; 1.257 com nota (`aplazos` não nulo); 864 completos no artigo (`excluFINAL == 0`). Usar as flags `excluidos`, `excluFINAL`, `datoscompleto*`.
- Y: `¿Cuánto tiempo en Minutos tardas en dormirte?` (**latência em minutos**, contínua; **999** = faltante); `tposueñosemTRIMMED` e `tposueñofsemTRIMMED` (duração em horas, semana/fim de semana); `difonsetsueño`; `Resultado` (escore PDSS 2–32, sonolência); `somno01pdss` (binária).
- X: `¿Cuánto tiempo de pantalla… antes de dormirte…?` (horas de tela antes de dormir); `tpopantallatotalhstrimmed` (horas/dia); por atividade `tpovideojuegoshs`, `tpojuegotabletcelhs`, `tporedeshs`, `tpotvonlinehs`; `WATCHTVbedtime7D01`, `COMPUbedtime1D01`/`2D01` (binárias, uso na hora de dormir).
- Covariáveis: `edad`, `sexonum`, `niveducpadresRECOD`, cômodos/pessoas no domicílio, altura, peso, IMC/z-escores, deslocamento, sesta, hora do jantar, notas escolares.

**R8. Sono e tela em adolescentes escolares de Ibadan** (`repo_mendeley_sleep_screen_adolesc_nigeria\`)
- https://doi.org/10.17632/yhk2y9ygm2.1 · artigo não indicado. Nigéria, ano não informado (publicado em 2025). Real.
- `Sleep_n_screen_time_Ibadan.sav` (101.658 B): **270 × 176**, com rótulos de valor.
- Y: `GLOBALPSQI` (0–15; 70 NaN), `NEWGLOBALPSQI` (63 NaN), `component1`–`component7`, `hwlngdoutofallslp` (latência em minutos; 4 NaN), `hrsofslp` (horas), `sleepquality` (binária).
- X: `smartweekday_hrspt`, `tvweekday_hrspt`, `laptopweekday_hrspt`, `totalhrspent_screen` e equivalentes de fim de semana — **o sufixo "hrs" contém minutos** (valores até 2.460); `hoursspentoninternetphoneinnit` (uso noturno); `screenaccessible*`.
- Covariáveis: `loc` (rural/urbano), `age`, `gen`, `edumum`/`edudad`, `occmum`/`occdad`, `famtype`, religião, pessoas por quarto.

**R9. Doomscrolling, procrastinação do sono e problemas de sono (18–40 anos)** (`repo_mendeley_doomscrolling_sleep_turquia\`)
- https://doi.org/10.17632/tjbkb6f25x.1 · artigo não indicado. Turquia, ano não informado (publicado em 2026). Real (declarado).
- `Doomscrolling.csv` (336.646 B): **1.216 × 117**, separador diferente de vírgula; brancos `' '` = pulo/faltante (S4, S17, S20, S21).
- Y: `puki_toplam` (PSQI turco, 0–15 observado), `sleep_latency_numeric` (minutos), `sleep_duration_numeric` (texto com vírgula decimal), `bedtime`, `wake_time`.
- X: `FK_TOPLAM` (15–105; 15 itens de 7 pontos, provável Doomscrolling Scale — **sem codebook**), `FK1`–`FK15`; `DB_TOPLAM` (provável dependência de IA generativa), `UE_TOPLAM` (provável procrastinação do sono, 9 itens) — rótulos não verificados.
- Covariáveis: `S1` idade; `S2`–`S24` sem rótulo; `HS_TOPLAM` + `anxiety_subscale` + `depression_subscale`.

**R10. Student Insomnia and Educational Outcomes** (`repo_mendeley_student_insomnia_bangladesh\`)
- https://doi.org/10.17632/5mvrx4v62z.3 · sem artigo. Bangladesh (Daffodil Int. Univ.), out–dez/2024. Declarado real (Google Forms).
- `..._v1.csv` (186.316 B; 791 × 16) e `..._version-2.csv` (234.871 B; 996 × 16); a descrição do depósito cita 785 e 985.
- Y: 4 itens ordinais em texto (dificuldade para adormecer, horas de sono em faixas, despertares, qualidade). X: item 11 "frequência de uso de dispositivos antes de dormir" (5 níveis).
- Covariáveis: ano de estudo, sexo, cafeína, atividade física, estresse, desempenho.
- **Indícios de preenchimento automatizado no arquivo:** mediana de 22 s entre envios, 82,6% dos intervalos < 60 s; 88% com dificuldade para adormecer "toda noite/frequente" e 90% dormindo ≥ 7 h.

**R11. Sleep Patterns of College Students (2 depósitos do mesmo autor)** (`repo_mendeley_sleep_patterns_college\`)
- https://doi.org/10.17632/vpmfsbpt89.1 e https://doi.org/10.17632/h75rzz3y6n.1 · sem artigo, sem instituição, país não informado, 2026. **Procedência não documentada.**
- `vpmfsbpt89_..._2721.csv` (288.204 B; 2.722 × 10, sem timestamp) e `h75rzz3y6n_..._1222.csv` (155.215 B; 1.222 × 11; envios de 21 a 24/ago/2026). O de 1.222 não é subconjunto do de 2.722.
- Y: horas de sono, horário de dormir e qualidade em faixas ordinais. X: "tempo no celular antes de dormir" (5 faixas). Covariáveis: faixa etária, ano de estudo, estudo noturno, motivo de dormir tarde.
- Padrões no arquivo: (2.722) 55% dormem < 5 h e 24% deitam depois das 4h, mas 45% "nunca" se sentem cansados; (1.222) 43% dos intervalos entre envios < 60 s.

**R12. Okajima — procrastinação do sono × uso de celular** (`repo_zenodo_okajima_bedtime_procrastination_japao\`)
- https://zenodo.org/records/20743494 · artigo não localizado. Japão, ano não informado (publicado em 2026). Real.
- `BPS_study.csv` (66.749 B): **381 × 76** (18–29 anos). Algumas colunas com nome em japonês.
- Y: `AIStotal` (Athens Insomnia Scale, 8–32; itens `AIS1`–`AIS8` codificados 1–4, não 0–3); `SDI_wd`, `SDI_we`, `SDI_ist` (horas de sono semana/fim de semana/ideal), `SDItotal`. Horas de sono = 0 em 9 casos (provável faltante).
- X: `mphone` (horas de celular nas 3 h antes de dormir, 0–3, contínua); `BPStotal`; `CVCtotal` (itens `voyage1-15`, rótulo ausente).
- Covariáveis: `age`, `gender`, `CIRENStotal` (cronotipo), `SWB1`–`16`, `day_satisfy`, `day_behav`.

**R13. Safaria et al. — problemas de sono × uso problemático de smartphone** (`repo_zenodo_safaria_sleep_smartphone_indonesia\`)
- https://zenodo.org/records/13831484 · artigo Safaria, Arini, Saputra, Suyono, J. Technol. Behav. Sci. 2025 (DOI não localizado; PDF https://eprints.uad.ac.id/84773/1/Interplay_of_nomophobia_to_sleep_problems.pdf). Indonésia (Yogyakarta). Real.
- `DATA_RISET_JOGJA.sav` (11.281 B): **672 × 7** (15–19 anos). Só escores totais.
- Y: `Sleep` ("poor sleep habit", 9–36). X: `Smartphone` (uso problemático, 8–37), `Nomo` (nomofobia, 8–32). Covariáveis: `Gender`, `Age` (códigos 1–5 = 16/17/18/19/15 anos), `Father`, `Mother`.

**R14. Digital Screen Exposure, Sleep Quality and Learning Focus** (`repo_zenodo_screen_sleep_univ_indonesia\`)
- https://zenodo.org/records/21152421 · artigo não indicado. Indonésia, 2026. Real (Google Forms).
- `Research_M_Project_Responses.xlsx` (16.899 B): **105 × 18**.
- Y: 2 itens Likert 1–5 de sono com causa atribuída pelo próprio respondente ("o uso antes de dormir dificulta adormecer", "dormir mais tarde"). X: 9 itens Likert de uso de gadget antes de dormir e na cama. Covariáveis: faixa etária, curso, semestre.

---

## 3. Não baixados

Todas reais. Códigos marcados "não verificado" não foram confirmados em documento oficial acessível sem login.

| Fonte | Link direto | O que é exigido | Passos para obter |
|---|---|---|---|
| **Add Health** (Wave I public-use, n = 6.504; Waves II–VI até 3.937) | https://addhealth.cpc.unc.edu/data/public-use-data-sets/ · codebook público: https://adata.site.wesleyan.edu/files/2017/08/AddHealth-Wave_1_Questionnaire-and-Codebook.pdf | Aceite de termo de uso + conta gratuita | Uma de três rotas: (a) Add Health Dataverse https://dataverse.unc.edu/dataverse/addhealth — assinar "Dataset Terms form"; (b) ICPSR 21600 https://www.icpsr.umich.edu/web/ICPSR/studies/21600 — conta MyData gratuita (pesos em "Public Use Grand Sample Weights", DS4); (c) ARDA, aceitando os termos. A amostra completa (restrita) exige contrato via CPC Data Portal e vínculo de pesquisa com doutorado. Tamanho/formato dos arquivos: não verificado. Códigos conferidos no codebook: `H1GH51` (1–20; 96/98), `H1GH52` (0/1; 6/8), `H1GH18` (0–4; 6/8), `H1DA8`/`H1DA9`/`H1DA10` (0–99; 996/998). |
| **ABCD Study** | https://abcdstudy.org/about/ · docs https://docs.abcdstudy.org/v/6_1_0/documentation/non_imaging/nt.html | DUA institucional (NBDC Data Use Certification) | https://docs.abcdstudy.org/latest/usage/access.html e https://www.nbdc-datahub.org/data-access-process: instituição reconhecida pelo NIH, assinatura do signing official, e-mails institucionais, conformidade NIST SP 800-171. Não há subconjunto aberto. Itens de tela no horário de dormir em ondas posteriores: códigos não verificados. |
| **NSRR** — SHINE, STAGES, FFCWS | https://sleepdata.org/datasets (variáveis em `sleepdata.org/datasets/<slug>/variables?search=`) | DAUA: conta + pedido em 6 etapas revisado pelo NSRR Review Committee; válido 3 anos; uso não comercial; IRB "preferred, not required" (https://sleepdata.org/replies/439) | SHINE (bebês 1–24 meses, n = 433): `devicebeforebed_mom`, `devicebed_mom`, `devicesleep_mom`, `tvsleep_mom` (O 1–4), `tvbabyslp_mom` (B), `computer_mom`/`phone_mom` (O 0–6; de quem é o tempo: não verificado); Y por actigrafia, `troublefallaslp_mom`. STAGES (pacientes de clínica do sono): `bthbts_0300` "quanto tempo antes de deitar usa computador/TV pela última vez" (O 0–3); `isi_score`, `sched_2200`. FFCWS ano 15 (n = 923 com actigrafia): diário com mídia/tela, códigos não verificados. |
| **ERICA** | https://pmc.ncbi.nlm.nih.gov/articles/PMC4334602/ · https://microdata.fao.org/index.php/catalog/2060 | Sem arquivo público com sono/tela | Pedido à coordenação (IESC-UFRJ). O único microdado distribuído (FAO, formulário + declaração de confidencialidade) é o componente de dieta, sem sono nem tela. |
| **ELSA-Brasil** | https://periodicos.usp.br/rsp/article/download/76734/80570/105027 | Proposta aprovada pelo comitê de publicações | Submeter proposta no sistema publiELSA; aprovada, pedir variáveis ao Data Center. Política atual: não verificada. |
| **Coortes de Pelotas** | https://epidemio-ufpel.org.br/cohort-2004/ · https://pmc.ncbi.nlm.nih.gov/articles/PMC4190519 | Formulário de aplicação + contato com pesquisadores | Contato ppgepi@ufpel.edu.br. 2004 aos 15 anos (2019-20): tela por dispositivo e MCTQ, n = 1.851 (https://pmc.ncbi.nlm.nih.gov/articles/PMC10251069); 1993: sono aos 11 e 22 anos, tela aos 11 (https://pmc.ncbi.nlm.nih.gov/articles/PMC4807077). 1982 e 2015: não verificados. |
| **UK Biobank** | https://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=1070 (também 1080, 1160, 1200) | Cadastro + aplicação aprovada + taxa + análise só na plataforma RAP (custo de computação) | Valor da taxa: não verificado (página oficial deu 403; busca indica £500/3 anos na tarifa estudante/LMIC). Códigos especiais (−10/−1/−3): não verificados. |
| **HBSC** | https://www4.uib.no/en/research/research-infrastructure/hbsc-data-management-centre/open-access · questionário 2009/10: https://www.uib.no/sites/w3.uib.no/files/attachments/2009_mandatory_questionnaire_0.pdf | Pedido por formulário | "Request data" → formulário em svar.uib.no; contato dmc@hbsc.org. Dados abertos só 3 anos após o fim da rodada; pacotes opcionais e rodadas anteriores a 2001/02 não liberados. Códigos de 2013/14 e 2017/18: não verificados. |
| **SHoT** (Noruega) | https://frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2025.1548273/full | Aprovação ética (REK Vest) + pedido ao NIPH | Contato Børge Sivertsen; GDPR restringe compartilhamento. Códigos: não verificados. n de 2022 inconsistente no artigo (45.202 / 46.202 / 45.654). |
| **Millennium Cohort Study (MCS6)** | UKDS SN 8156 · https://cls.ucl.ac.uk/wp-content/uploads/2020/09/MCS6_User_Guide_ed2_2020-08-10.pdf | Cadastro gratuito no UK Data Service + End User Licence ("safeguarded") | Cadastrar, aceitar a licença e baixar SN 8156. Códigos `FC*` de sono e tela: não verificados. |
| **openICPSR E193588** (smartphone × PSQI, COVID-19) | https://doi.org/10.3886/E193588V3 | Login gratuito no openICPSR (página devolveu 403 ao acesso automatizado) | Criar conta em openicpsr.org e baixar pela página do projeto. País: não verificado. |
| **Gamers Wave 1–3** (Victoria University) | https://doi.org/10.7910/DVN/YOJLLQ | DUA ("Request Access" no Harvard Dataverse) | Pedir acesso e aceitar o DUA da Victoria University. Arquivos de 2 KB a 2,3 MB. |
| **Kaggle "Sleep Pattern"** | https://www.kaggle.com/datasets/krupa1999/sleep-pattern | Login Kaggle | Entrar e baixar (2.909 B; licença "Unknown"; n = 46 segundo arXiv 2411.02388). |
| **Kaggle "StudentLife"** | https://www.kaggle.com/datasets/dartweichen/student-life | Login Kaggle + 3,04 GB | Entrar e baixar; o site oficial studentlife.cs.dartmouth.edu não respondeu em 13/11/2026. |
| **IEEE DataPort "Sleep Schedule and Sleeping Habits Survey"** | https://doi.org/10.21227/qrhh-9887 | Login/assinatura IEEE DataPort | Entrar e baixar (xlsx 126,9 KB; CC BY 4.0). Sem país nem método documentados. |
| **ETRI Lifelog Dataset 2024** | https://nanum.etri.re.kr/share/human/ETRILifelogDataset2024 | License Agreement no portal Nanum (só uso acadêmico) | Cadastro e aceite da licença. n: 10 (arXiv 2508.03698) ou 50 (portal). |
| **YRBS 2023** | https://www.cdc.gov/yrbs/data/index.html | Nada (aberto) | Não baixado por ter o mesmo desenho de conteúdo do YRBS 2025 já baixado (sem horas de tela; `Q80` redes sociais, `Q85` sono). |

Também abertos e não baixados, por redundância: NSCH 2016 e 2018–2024 (https://www.census.gov/programs-surveys/nsch/data/datasets.html); pesos replicados do ATUS 2025 (`atuswgts`, 7,4 MB).

---

## 4. Descartados (verificados: sem tela + sono juntos, sintéticos declarados ou sem microdado)

| Fonte | Motivo verificado | URL |
|---|---|---|
| PeNSE 2019 (IBGE) | Dicionário tem TV (`B03009b`) e tempo sentado com telas (`B03010b`), mas **nenhuma** variável de sono; o módulo B12 (saúde mental) vai de `B12003` a `B12009` e não inclui o item de sono de 2015. Só a documentação foi baixada (`pense_2019\Documentacao.zip`, 52.901 B); `Dados.zip` (117 MB) não foi baixado. | https://ftp.ibge.gov.br/pense/2019/microdados/ |
| PeNSE 2024 (IBGE) | Dicionário tem `B03009C` (TV/streaming) e `B03010C` (tempo sentado com telas), sem variável de sono. Só documentação baixada (`pense_2024\Documentacao.zip`, 49.093 B); `Dados.zip` (150 MB) não baixado. | https://ftp.ibge.gov.br/pense/2024/microdados/ |
| NHANES 2007-2008, 2009-2010 | Tela (`PAD590`/`PAD600`) só para 2–11 anos; sono (SLQ) só ≥16 anos — sem sobreposição. | codebooks PAQ_E, PAQ_F |
| NHANES 2017-2018, 2017–mar/2020, 2021-2023 | Sem variável de tela; só `PAD680` (minutos sentado, total). | codebooks PAQ_J, PAQ_L |
| NSRR — CFS, MrOS, SHHS, PATS, HEARTBEAT, CCSHS | Os itens com "TV"/"video" (FOSQ `ftv`, `fvideo`, `fosotv`; `watv02`/`sh319b`; `ytv`) são da escala de sonolência do tipo "cochila/tem dificuldade vendo TV", não exposição a tela. | https://sleepdata.org/datasets |
| NSRR — SNAPSHOT | 323 universitários (2013–16); nenhuma variável de tela nos dados compartilhados; exige pré-aprovação do PI. | https://sleepdata.org/datasets |
| Kaggle `uom190346a/sleep-health-and-lifestyle-dataset` | **Sintético** declarado pelo autor ("synthetic and created by me for illustrative purposes"); também sem variável de tela. | https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset |
| Kaggle `govindaramsriram/sleep-time-prediction` | **Sintético** declarado ("Generated synthetically using a Python script"). | kaggle.com/datasets/govindaramsriram/sleep-time-prediction |
| Kaggle `jayjoshi37/sleep-screen-time-and-stress-analysis` | **Sintético** declarado (15.000 registros). | kaggle.com/datasets/jayjoshi37/sleep-screen-time-and-stress-analysis |
| Kaggle `jayjoshi37/smartphone-usage-and-addiction-prediction` | **Sintético** declarado. | kaggle.com/datasets/jayjoshi37/smartphone-usage-and-addiction-prediction |
| Kaggle `samartalwar/sleep-debt-and-screen-time-late-night-phone-habits` | **Sintético** declarado ("generated via a simulation"). | kaggle.com/datasets/samartalwar/sleep-debt-and-screen-time-late-night-phone-habits |
| Kaggle `sureshbeekhani/teen-social-media-usage-and-mental-health`, `arsalanjamal002/student-sleep-patterns`, `ankushpanday2/indian-kids-screentime-2025`, `neurocipher/digital-distraction-vs-academic-performance`, `khushikyad001/global-mobile-phone-addiction-dataset`, `amanshah2002/stress-screen-time-analysis-synthetic-data` | **Sintéticos** declarados na descrição do autor (lida via API pública). | kaggle.com/datasets/<id> |
| Kaggle `zahranusratt/…` e `jimarahman/smartphone-usage-and-addiction-analysis-dataset` | Sem procedência; tamanho listado (182.295 B) idêntico ao do sintético `jayjoshi37`. | kaggle.com/datasets/<id> |
| Kaggle `amartiwari13/screen-time-sleep-and-stress-analysis-dataset` (50.000 registros), `prince7489/mental-health-and-social-media-balance-dataset` | Nenhum método descrito; não verificado se sintéticos. | kaggle.com/datasets/<id> |
| Zenodo 15171250 "Group Health Dataset (Sleep and Screen Time)" | Só 4 usuários (Mi Band, TU Eindhoven). | https://zenodo.org/records/15171250 |
| DANS 10.17026/DANS-ZMV-3MHA "The influence of screen time on sleep quality" | n = 5 e arquivos restritos. | https://doi.org/10.17026/DANS-ZMV-3MHA |
| DataverseNL 10.34894/U7NPHZ (Borger, Huber & Ghosh 2019) | Só `.mat` agregados; usa o toque na tela como estimador do sono, não como exposição. | https://doi.org/10.34894/U7NPHZ |
| Zenodo 16665655 "Screen Time Survey" | 38 crianças; único item de sono é "sonolência na escola por gadget". | https://zenodo.org/records/16665655 |
| Zenodo/Dryad 4934490 (Taiwan, transições de dependência de smartphone) | 1.943 × 21, sem variável de sono. | https://zenodo.org/records/4934490 |
| Zenodo 6742700 "Smartphone_data" | EEG/memória de trabalho, sem sono. | https://zenodo.org/records/6742700 |
| Mendeley mrcthr8nxf (procrastinação do sono + PSQI, Chongqing) | Sem variável de tela. | https://data.mendeley.com/datasets/mrcthr8nxf |
| Harvard Dataverse L139VP (phantom vibration × sleep disorder) | Só PDF, sem microdado. | https://doi.org/10.7910/DVN/L139VP |
| Figshare 34009308 e 34478340 (Frontiers) | Suplementos `.docx`, não microdados. | https://figshare.com |

Não verificado: microdados do estudo Open Play no OSF (osf.io/kxw2h); o OSF de Siebers (osf.io/tpj98) tem sintaxe/pré-registro.

---

## 5. Notas de procedimento

- Scripts de inspeção (somente leitura) ficaram fora do repositório. Nenhum arquivo baixado foi executado nem alterado.
- `pyreadstat` foi instalado com `pip --user` para ler `.sav`.
- PeNSE 2015 Amostra 1: só os CSV e o dicionário foram extraídos; SAS7BDAT/XLSX (mesmo conteúdo) ficaram no zip. Vigitel não foi extraído (lido do zip).
