# 005 — Plano: regressão linear múltipla, ANOVA e teste t

Status: executado (2026-11-27).

## Modelos

Vigitel e NHANES, k = 6 regressores:

```text
Y = β0 + β1·D(1 a <3 h) + β2·D(≥3 h) + β3·idade + β4·feminino + β5·D(médio) + β6·D(superior) + ε
```

Bases de repositório: `Y = β0 + β1·X + covariáveis + ε`, com X contínuo.

Dummies: k − 1 por variável categórica (a categoria de referência fica fora, para evitar a armadilha das dummies). Referências: tela < 1 h, sexo masculino, escolaridade abaixo do ensino médio.

| Hipótese | Modelo ou teste | Estatística | Ferramenta do Excel | Script |
|---|---|---|---|---|
| H5.1–H5.6 | MQO: Y ~ tela + covariáveis | t = b / EP, gl = n − k − 1 | Regressão (*Regression*) | `statsmodels` OLS (sem peso) e WLS (com peso) |
| H5.7–H5.8 | ANOVA de um fator, 3 grupos | F = MQ entre / MQ dentro, gl (2, n − 3) | Anova: fator único (*Anova: Single Factor*) | `scipy.stats.f_oneway` e regressão nas 2 dummies |
| H5.9–H5.10 | t de Welch, ≥ 3 h × < 1 h | t; gl de Welch–Satterthwaite | Teste-t: duas amostras presumindo variâncias diferentes (*t-Test: Two-Sample Assuming Unequal Variances*) | `scipy.stats.ttest_ind(equal_var=False)` |
| H5.11 | base empilhada: Y ~ tela + covariáveis + país + país × tela | F parcial, q = 2 | duas Regressões (com e sem as interações) e fórmula do F parcial | comparação de modelos aninhados |

## Técnica mostrada passo a passo

O notebook calcula cada número por álgebra matricial em `numpy` e compara com `statsmodels` e com o Excel:

| Quantidade | Fórmula |
|---|---|
| Coeficientes | b = (XᵀX)⁻¹ Xᵀy |
| Variância residual | s² = SQRes / (n − k − 1) |
| Erro padrão | EP(bⱼ) = √(s² · [(XᵀX)⁻¹]ⱼⱼ) |
| t e p | tⱼ = bⱼ / EP(bⱼ); p = 2 · P(T(n − k − 1) > \|tⱼ\|) |
| IC 95% | bⱼ ± t(0,975; n − k − 1) · EP(bⱼ) |
| F global | F = (SQReg / k) / (SQRes / (n − k − 1)); p = P(F(k, n − k − 1) > F) |
| R² e R² ajustado | R² = SQReg / SQTot; R² aj = 1 − (1 − R²)(n − 1) / (n − k − 1) |
| F parcial | F = [(SQRes_r − SQRes_c) / q] / [SQRes_c / (n − k_c − 1)] |
| f² de Cohen | f² = (R²_c − R²_r) / (1 − R²_c) |
| η² | SQ entre / SQ total |
| d de Cohen | (ȳ₁ − ȳ₂) / s combinado |
| gl de Welch | (s₁²/n₁ + s₂²/n₂)² / [(s₁²/n₁)²/(n₁ − 1) + (s₂²/n₂)²/(n₂ − 1)] |
| Holm | ordenar p crescente; p(i) · (m − i + 1); máximo acumulado; teto 1 |

## Verificação dos p-valores

| Caminho | Como | Onde |
|---|---|---|
| A. Ferramenta do Excel | saída de Regressão, ANOVA e Teste-t | `<base>_resultados.xlsx`, abas de saída |
| B. Fórmula no Excel | `=T.DIST.2T(ABS(t), gl)` e `=F.DIST.RT(F, gl1, gl2)` (em português: `DIST.T.BC` e `DIST.F.CD`, separador `;`), numa coluna "p conferido" ao lado da saída | mesma planilha |
| C. Script | `statsmodels`/`scipy` e a álgebra matricial acima | `analise/regressao/modelos.py` |

`analise/regressao/confere_excel.py` lê a planilha salva (openpyxl, `data_only=True`), localiza as tabelas pelos rótulos em inglês ou em português e compara A, B e C célula a célula. Tolerância: diferença relativa < 1e-8. Quando os dois valores são < 1e-15, contam como iguais, porque o Excel arredonda p muito pequeno para 0. A saída é `resultados/005/conferencia.csv`, com uma linha por número, a diferença e ok/falha.

**Teste de referência, conferido em 2026-11-27.** No exercício 2 da aula (salário ~ sexo + qualificado + tempo de serviço, n = 20), `statsmodels` reproduz o SUMMARY OUTPUT do Excel:

| Número | Diferença relativa máxima |
|---|---|
| p-valores dos coeficientes | 7,9e-14 |
| F de significação (5,0715e-18) | 7,9e-15 |

Esse caso vira o teste automatizado `tests/test_confere_excel.py`. Fixture: os 20 valores do exercício e a saída do Excel. O grupo decide se esse material da aula pode ficar num repositório público; se não puder, o teste lê o arquivo por variável de ambiente.

`tests/test_consistencia.py` cobre as checagens da spec:

- p < 0,05 ⇔ IC exclui 0;
- F parcial com q = 1 é igual a t²;
- ANOVA de um fator = regressão nas dummies;
- t com variâncias iguais = t da dummy;
- Holm ≥ p bruto.

**Princípio 2.** O número que vai para o relatório sai do caminho C. O Excel é a técnica mostrada e é conferido por script, então nada no relatório é digitado à mão.

## Peso amostral

A ferramenta Regressão do Excel não aceita peso.

| Base | Excel | Script |
|---|---|---|
| Vigitel 2024 | sem peso: demonstração da técnica e sensibilidade | WLS com `pesorake2025`, erro padrão robusto. Este é o resultado que decide a hipótese |
| NHANES 2005-06 | sem peso: demonstração e sensibilidade | WLS com `WTINT2YR` e erro padrão por UPA. A ferramenta segue a decisão da T040 (spec 003). É o resultado que decide |
| Repositórios | análise principal (não há desenho complexo) | reproduz o Excel |

Base empilhada (H5.11): pesos reescalados para somar o n de cada base, como na spec 003.

## Pressupostos e o que fazer quando falham

| Pressuposto | Verificação | Se falhar |
|---|---|---|
| Linearidade | resíduo × ajustado; resíduo × X contínuo | termo quadrático ou faixas de X, como sensibilidade |
| Normalidade dos resíduos | QQ-plot e histograma; Jarque-Bera (com n grande rejeita por desvio pequeno, então vale o gráfico) | com n de centenas ou mais, t e F seguem aproximadamente válidos; registrar |
| Homocedasticidade | Breusch-Pagan; resíduo × ajustado | erro padrão robusto HC3 como sensibilidade (o Excel não calcula); registrar se a decisão muda |
| Multicolinearidade | VIF de cada regressor | VIF > 10: revisar covariáveis |
| Observações influentes | distância de Cook > 4/n; resíduo studentizado | reestimar sem elas, como sensibilidade |
| Independência | conglomerado (UPA) no NHANES | erro padrão por cluster na versão com peso |

Problemas conhecidos de Y:

- **Latência:** concentrada em 5/10/15/30/60 min, com cauda longa. No NHANES o topo é censurado em 60, por isso lá a latência é só desfecho secundário. Sensibilidade com log(1 + latência).
- **`insonia_idx`:** discreto e limitado a 0–12. Em 2024, 8.641 dos 27.048 entrevistados do Vigitel responderam "nunca" no primeiro sintoma. MQO estima bem a diferença de médias, mas o IC do valor previsto pode sair de 0–12.

## Poder

Tamanho mínimo detectável para um coeficiente, com poder de 80% e α = 0,05:

| Base | n | f² | Correlação parcial |
|---|---|---|---|
| Japão | 381 | 0,021 | 0,14 |
| Argentina | 864 | 0,009 | 0,10 |
| Turquia | 1.216 | 0,007 | 0,08 |
| Xuzhou | 2.317 | 0,003 | 0,06 |
| NHANES | 5.563 | 0,001 | 0,04 |
| Vigitel | 27.048 | 0,0003 | 0,02 |

No Vigitel, um efeito sem importância prática já sai significativo. Por isso o relatório discute o tamanho do efeito (ganho de R², f² e IC), não só o p.

## Preparação para o Excel

`analise/regressao/prepara_excel.py` gera, por base, `<base>_dados.xlsx` com:

| Aba | Conteúdo |
|---|---|
| `dados` | Y na coluna A e os X contíguos a seguir, já numéricos, com as dummies criadas e só casos completos (a ferramenta não aceita célula vazia no intervalo); rótulos na linha 1 |
| `anova` | Y em 3 colunas, uma por faixa de tela (layout que a ferramenta de ANOVA exige) |
| `teste_t` | Y em 2 colunas (≥ 3 h e < 1 h) |
| `log` | n antes e depois de cada filtro |

A maior base (Vigitel, 27.048 linhas) cabe no limite do Excel (1.048.576 linhas).

**Licença.** As planilhas das bases CC BY 4.0 (Xuzhou, Argentina, Turquia, Japão) e de domínio público (NHANES) podem entrar no git com atribuição. A do Vigitel segue a pergunta 3 da spec 001. Sem decisão, a planilha fica em `STAT4_SAIDA`, fora do git, e só as abas de resultado entram, exportadas em CSV.

## Protocolo do Excel

`analise/regressao/PROTOCOLO_EXCEL.md` descreve o passo a passo:

- O caminho: Dados → Análise de Dados → Regressão. Intervalo Y, intervalo X, Rótulos, Nível de confiança 95%, Resíduos e Plotagem de resíduos.
- O nome fixo de cada aba de saída: `reg_completo`, `reg_simples`, `reg_covariaveis`, `anova_saida`, `teste_t_saida`. O script de conferência lê essas abas.
- As fórmulas de conferência (caminho B).
- Os nomes das ferramentas e funções em português e em inglês. A planilha da aula foi gerada com o Excel em inglês ("SUMMARY OUTPUT", "Significance F").

Quem executa salva `<base>_resultados.xlsx`.

## Saídas

- `resultados/005/tabelas/summary_<base>_<modelo>.csv` — formato SUMMARY OUTPUT.
- `resultados/005/tabelas/hipoteses.csv` — hipótese, estatística, gl, p, p Holm, decisão, efeito e IC.
- `resultados/005/conferencia.csv` — A × B × C.
- `resultados/005/figuras/diagnostico_<base>.png`.
- `analise/notebooks/06_regressao_linear.ipynb`.

## Riscos

| Risco | Efeito | Mitigação |
|---|---|---|
| n grande no Vigitel e no NHANES | quase todo coeficiente com p < 0,001 | decisão acompanhada de tamanho de efeito e IC; o texto discute relevância |
| Turquia sem codebook | X com rótulo errado | T080 confirma no depósito ou no artigo; sem confirmação, H5.5 vira exploratória |
| Excel em português ou em inglês | nomes de ferramenta, função e rótulo mudam | protocolo com os dois idiomas; a conferência reconhece os dois conjuntos de rótulos |
| Planilha editada à mão depois da saída | número diverge do script | a conferência falha e aponta a célula |
| NHANES de 2005, antes do smartphone; Vigitel só nas capitais | H5.11 mistura época e país | mesma limitação declarada na spec 003 |

## Histórico

- 2026-11-27: executado. Módulos em `analise/regressao/`: `dados.py` (matrizes), `ols.py` (MQO matricial e WLS com linearização), `prepara_excel.py`, `excel_toolpak.ps1` + `roda_excel.py` (caminho A), `modelos.py` (caminho C), `confere_excel.py` (A × B × C), `diagnostico.py`, `resumo.py`, `notebook.py`.
- Caminho A: a Análise de Dados foi automatizada por COM. Em automação o Excel não carrega o suplemento sozinho: é preciso registrar o `ANALYS32.XLL` e abrir o `ATPVBAEN.XLAM`. Nomes internos conferidos pela saída: `Pttestv` = variâncias diferentes (Welch), `Ttestm` = variâncias iguais. Abrir o segundo arquivo na mesma instância derrubou o Excel ("servidor RPC não disponível"); por isso há uma instância por arquivo, com teto de tempo e encerramento só da instância criada.
- Planilhas: um arquivo `<base>_resultados.xlsx` por base, com dados e saídas (fora do git); as abas de saída vão em CSV para `resultados/005/excel_saidas/`.
- Tolerância cumprida: maior diferença relativa A × C e B × C = 4,5e-10 (< 1e-8). Exceção documentada: p do Welch com gl inteiro (Excel) × fracionário (script), diferença relativa até 1,5e-5, linha "informativo" em `conferencia.csv`.
- Graus de liberdade da versão com peso: regra do `svyglm` (gl do desenho + 1 − nº de parâmetros). Diferente da spec 003 (gl do desenho); sensibilidade registrada. **Substituído na correção abaixo.**
- Teste de referência (`tests/test_005_confere_excel.py`) lê a planilha da aula por `STAT4_AULA`, sem copiar o material para o repositório.
- Notebook numerado 06 (o 05 é da spec 004).
- 2026-11-27, correções da verificação independente: gl com peso = UPAs − estratos (regra única, igual à 003; `svyglm` vira sensibilidade); Korn-Graubard nos Wald com q > 1 (`ols.korn_graubard`); H5.11 com o gl de desenho do NHANES; estrato com 1 UPA alinhado a `survey.py`; d de Cohen com DP combinado nas duas versões; referência das dummies = categoria mais frequente (VIF ≤ 2,0); conferência com colunas `dentro_tolerancia`/`excecao_documentada` e leitura de `excel_saidas/` em clone limpo. Testes novos em `tests/test_005_consistencia.py` (Korn-Graubard, estrato com 1 UPA, d de Cohen) e `tests/test_005_confere_excel.py` (clone limpo). Nenhuma decisão mudou.
