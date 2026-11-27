# Verificação independente (2026-11-27)

Depois da execução das specs 001–006, um agente verificador independente (modelo Fable 5.2) revisou o código, os dados, as specs e a entrega. Ele não editou nada; só leu, refez estimativas por conta própria e listou problemas. Esta página registra cada item e o que foi feito.

> **Atualização de 2026-11-27: os EUA saíram do trabalho.** A verificação foi feita quando o trabalho ainda incluía o NHANES 2005-06 (EUA). Depois dela, o grupo retirou a base, porque é de antes do smartphone. Os itens 1, 6 e 9 e três sugestões dependiam do NHANES: o que ainda vale deles está nas tabelas abaixo, e o que deixou de existir está em "Itens superados pela retirada dos EUA (2026-11-27)", no fim da página. Os números desta página que citam o NHANES descrevem a versão verificada.

**O que o verificador refez sozinho e bateu (versão com os EUA):**

- recodificações conferidas contra os brutos e os dicionários (PNS, Vigitel, NHANES);
- os n das bases;
- RP ajustadas: NHANES 1,405, PNS 1,187, Vigitel 1,316;
- 1º autovalor do Vigitel: 2,261;
- meta-análise DerSimonian-Laird: ρ 0,0815, Q 382,19, I² 98,43%;
- MQO e WLS do Vigitel;
- 6 DOIs no Crossref.

## Erros confirmados

| # | Severidade | Problema | O que foi feito | Onde conferir |
|---|---|---|---|---|
| 1 | crítica | A regra de graus de liberdade (gl) do NHANES mudava a decisão de H3.3, e o texto só mostrava o lado que não muda | Regra única no projeto: gl = UPAs − estratos. A regra do `svyglm` virou sensibilidade. **Hoje:** a regra vale na PNS (8.027 UPAs − 574 estratos = 7.453 gl), a única base com estrato e UPA; pela regra do `svyglm`, nenhuma decisão muda. A H3.3 saiu com os EUA | `resultados/003/tabelas/hipoteses.csv` (colunas `*_svyglm`); relatório §4 |
| 2 | crítica | O roteiro citava o F de Wald ponderado (9,61) como se fosse o F da ANOVA do Excel | O roteiro usa o F do Excel (34,91), que é igual ao da regressão nas dummies, e cita o de Wald como o que decide | `docs/roteiro_apresentacao.md`, bloco 6 |
| 3 | importante | A tabela de regressão, ANOVA e t trazia estatísticas ponderadas com rótulo de ANOVA e de t de Welch, sem gl | A tabela mostra duas colunas, "sem peso (Excel)" e "com peso (decisão)", com os gl | relatório §5.3 |
| 4 | importante | "922 comparações, todas passaram" era falso: a coluna `ok` era texto | A conferência separa 920 dentro da tolerância e 2 exceções documentadas (gl de Welch arredondado pelo Excel). O script falha se aparecer divergência não documentada | `resultados/005/conferencia.csv` (`dentro_tolerancia`, `excecao_documentada`); `analise/relatorio/numeros.py` |
| 5 | importante | Ausência de evidência escrita como igualdade ("Brasil e EUA não diferem") | O texto diz "não foi detectada diferença" e dá o IC. A discussão explica por que a comparabilidade é só parcial | relatório (Resumo, §5.2, §6, §8); roteiro; explicações 003, 004 e 005 |
| 6 | importante | Os testes de Wald com várias restrições e poucos gl não tinham correção | Correção de Korn-Graubard: F = (d − q + 1)/(d·q)·W. Em H3.7 no NHANES, p passou de 0,050 para 0,183; a decisão não muda. **Hoje:** a correção continua no código e se aplica à H3.7 da PNS, F(6; 7.448) com d = 7.453; com tantos gl ela quase não muda o F | `analise/brasil_eua/survey.py`, `analise/regressao/ols.py`; testes novos |
| 7 | importante | A frase "nenhum número digitado" valia também para números da literatura e constantes | A frase ficou restrita aos resultados próprios. Os n, a contagem de casos sem idade e os gl agora vêm dos dados | `docs/modelos/*.md` |
| 8 | importante | O teste de linguagem causal tinha brecha ("leva ao", "efeito da") | A regex foi ampliada e as frases foram reescritas ("se associa a", "precede") | `tests/test_006_entrega.py` |
| 9 | menor | As bases empilhadas mostravam gl ≈ 27 mil, mas a variância da interação vem do NHANES | O gl da interação passou a ser o do desenho do NHANES (15). Por Satterthwaite daria 8,9, com a mesma decisão (p 0,617 contra 0,622). **Hoje:** não há base empilhada; a comparação PNS × Vigitel (H3.9) usa a diferença dos log-RP de modelos separados | `resultados/003/tabelas/comparacoes_entre_bases.csv` |
| 10 | menor | Detalhes de método: redação da análise paralela; estrato com 1 UPA tratado de jeitos diferentes; d de Cohen com DP diferente com e sem peso; RP por faixa etária com variância só do subconjunto | Corrigidos: redação da §5.1; mesmo tratamento de estrato com 1 UPA nas duas specs; DP combinado nas duas versões; RP por faixa etária estimada por domínio, com todo o desenho na variância | specs 003 e 005, Histórico |
| 11 | menor | A conferência falhava num clone sem Excel; os testes viravam `skip` sem aviso; a contagem conferia o log, não os dados | Sem `analise/dados/excel/`, a conferência lê `resultados/005/excel_saidas/`. O README explica os `skip`. Um teste novo confere o n no próprio parquet | `analise/regressao/confere_excel.py`; `tests/test_001_contagens.py`; `README.md` |

## Sugestões

| Sugestão | O que foi feito |
|---|---|
| IC de Hartung-Knapp na meta-análise (k = 7 na versão verificada; k = 6 sem os EUA) | Reportado ao lado do DerSimonian-Laird. O IC global de Hartung-Knapp inclui o zero nas duas versões, e o relatório diz isso. Também é usado na comparação exploratória Brasil × resto do mundo |
| Os EP das correlações ignoram o desenho amostral | Sensibilidade com a variância multiplicada pelo deff de Kish (hoje só PNS 3,21 e Vigitel 3,74). Nenhuma decisão muda |
| Pré-sono com uma base só; H4.2 registrada como ordenada e testada como omnibus | Declarado no Histórico da 004. Teste de tendência acrescentado como exploratório, fora de Holm |
| Fragilidade de H5.2 sem observações influentes | Citada no relatório e no RESUMO da 005 enquanto a H5.2 existiu. Superada: a H5.2 (NHANES) saiu com os EUA. As fragilidades de H5.4 (Argentina) e H5.5 (Turquia) continuam no relatório |
| VIF de 18,1 e 11,4 nas dummies de Xuzhou e da Argentina | A referência passou a ser a categoria mais frequente: VIF ≤ 2,0, e o coeficiente da tela não muda |
| Escolaridade: "médio incompleto" em faixas diferentes entre as bases | Anotado em `resultados/001/tabelas/equivalencia.csv` |
| H3.1–H3.3 escritas como unilaterais e testadas como bilaterais | A spec agora diz "RP ≠ 1 (sinal esperado > 1)" |
| Cabeçalhos crus nas páginas | Rótulos legíveis e uma legenda de leitura em cada tabela |
| "Pessoa 1–4" no roteiro | Os nomes vêm de `docs/modelos/integrantes.csv`. Enquanto o grupo não preenche, o roteiro mostra o papel de cada bloco. Não sobra nenhum "Pessoa N" |
| Nome de pessoa nas specs de um repositório público | Trocado por "a pedido de um integrante" |
| Caminho local em `analise/dados/excel/plano_toolpak.json` | O plano guarda só o nome de cada arquivo. O caminho absoluto que o Excel exige vai num JSON temporário fora do repositório, apagado depois de cada execução. O Excel foi rodado de novo assim, com as 7 pastas e 920 números conferidos |
| Holm "em 5%" | Corrigido para "em no máximo 5%" |

## Como conferir que cada correção está aplicada

`tests/test_verificacao_independente.py` confere cada item nos arquivos gerados. Se alguém desfizer uma correção, o teste aponta qual item.

| Item | Teste |
|---|---|
| 1 | `test_item01_regra_unica_de_gl_e_svyglm_como_sensibilidade` (gl da PNS = UPAs − estratos = 7.453; `svyglm` só como sensibilidade, sem mudar decisão) |
| 2 | `test_item02_roteiro_usa_o_F_do_excel_na_equivalencia` |
| 3 | `test_item03_tabela_53_separa_sem_peso_e_com_peso_com_gl` |
| 4 | `test_item04_conferencia_conta_excecoes_separadas` |
| 5 | `test_item05_sem_igualdade_afirmada` (relatório, roteiro e explicações 003–005) |
| 5 e 8 | `test_item05_item08_sem_linguagem_causal_em_explicacoes_e_resumos`, que varre todas as explicações e todos os `RESUMO.md`, inclusive os da 002 |
| 6 | `test_item06_korn_graubard_na_pns` (H3.7 da PNS: F(q; d − q + 1) com q = 6 e d = 7.453), além dos testes unitários `test_korn_graubard_wald` (003) e `test_korn_graubard` (005) |
| 7 | `test_item07_frase_de_rastreabilidade_restrita_a_resultados_proprios` |
| 8 | `test_item08_regex_causal_ampliada` e `test_006_entrega.py::test_sem_linguagem_causal_afirmativa` |
| 9 | `test_item09_nenhuma_base_empilhada_nem_nhanes` (nenhuma base empilhada, nenhuma linha do NHANES nem hipótese retirada nas tabelas de 001, 003, 004 e 005) |
| 10 | `test_item10_rp_por_faixa_estimada_por_dominio` (PNS: 8.027 UPAs, 7.453 gl, nenhum estrato com 1 UPA), mais `test_dominio_usa_desenho_inteiro`, `test_mqp_estrato_com_uma_upa_igual_a_regra_da_003` e `test_d_cohen_mesma_definicao_com_e_sem_peso` |
| 11 | `test_item11_clone_limpo_e_contagem_no_parquet`, mais `test_conferencia_funciona_em_clone_limpo` e `test_contagem_no_proprio_parquet` |
| Sugestões | `test_sug_hartung_knapp_e_deff`, `test_sug_h42_omnibus_declarado`, `test_sug_vif_abaixo_de_10`, `test_sug_escolaridade_anotada`, `test_sug_h1_bilateral_na_spec_003`, `test_sug_cabecalhos_legiveis_no_site`, `test_sug_sem_nome_pessoal_nas_specs`, `test_sug_holm_no_maximo_5pct` |

Também confirmam as duas últimas sugestões: `test_sug_plano_do_excel_sem_caminho_local`, `test_sug_roteiro_com_apresentadores_configuraveis` e `test_006_entrega.py::test_roteiro_sem_marcador_de_pessoa`. Todas as sugestões do verificador foram aplicadas.

## Itens superados pela retirada dos EUA (2026-11-27)

O grupo retirou o NHANES 2005-06 depois da verificação e depois de ver os resultados (Histórico das specs 001 a 005). Parte do que o verificador apontou dependia dessa base:

| Item | O que dependia do NHANES | O que ainda vale | Teste hoje |
|---|---|---|---|
| 1 | A H3.3 (NHANES) mudava de decisão conforme a regra de gl (15 gl na regra do projeto, 7 na do `svyglm`) | A regra única gl = UPAs − estratos, aplicada na PNS (7.453 gl), com a regra do `svyglm` como sensibilidade. Na PNS a diferença entre as regras é de poucos gl e nenhuma decisão muda. Nenhuma decisão do trabalho é hoje sensível à regra de gl | `test_item01_regra_unica_de_gl_e_svyglm_como_sensibilidade` |
| 6 | A correção de Korn-Graubard fazia diferença no NHANES (d = 15): H3.7 passava de p 0,050 para 0,183 | A correção continua no código e é aplicada na H3.7 da PNS (d = 7.453, q = 6). Com tantos gl ela quase não muda o F, mas a regra é a mesma | `test_item06_korn_graubard_na_pns` |
| 9 | O gl da interação país × tela na base empilhada Vigitel + NHANES (H3.6, H5.11) | Nada: não há base empilhada. A comparação entre as duas pesquisas brasileiras (H3.9) usa a diferença dos log-RP de modelos separados | `test_item09_nenhuma_base_empilhada_nem_nhanes` |
| Sugestão: deff de Kish | Deff do NHANES (1,61) | Deff da PNS e do Vigitel | `test_sug_hartung_knapp_e_deff` |
| Sugestão: Hartung-Knapp | k = 7 com o NHANES | k = 6; o IC global continua incluindo o zero | `test_sug_hartung_knapp_e_deff` |
| Sugestão: fragilidade de H5.2 | H5.2 era a regressão do NHANES | Retirada com H5.8, H5.10 e H5.11 | — |
| Itens 3 e 5 | A coluna "com peso" e o texto "não foi detectada diferença" se aplicavam também ao NHANES e à comparação Brasil × EUA | Continuam no relatório, agora no Vigitel (com peso) e nas comparações PNS × Vigitel e Brasil × resto do mundo | `test_item03_tabela_53_separa_sem_peso_e_com_peso_com_gl`, `test_item05_sem_igualdade_afirmada` |

As hipóteses retiradas mantêm a numeração original (H2.2–H2.4, H3.3, H3.6, H5.2, H5.8, H5.10, H5.11), para que a verificação continue rastreável no histórico do git.

## Depois das correções

- O pipeline completo (`python -m analise.rodar_tudo`) foi rodado de novo do zero, com a automação do Excel e sem deixar nenhuma instância aberta.
- Na versão verificada, a suíte de testes passava inteira e nenhuma decisão de hipótese mudou pela regra principal; a única decisão sensível a uma escolha de método era H3.3 (NHANES).
- Depois da retirada dos EUA, os testes desta página foram adaptados ao que ainda vale (seção acima). Nenhuma decisão restante depende da regra de graus de liberdade.
