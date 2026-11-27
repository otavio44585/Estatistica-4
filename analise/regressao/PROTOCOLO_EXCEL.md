# Protocolo do Excel — spec 005 (T084)

Como reproduzir **à mão**, no Excel, o que `roda_excel.py` faz por automação. O resultado tem de bater com o script: a
conferência (`python -m analise.regressao.confere_excel`) lê as mesmas abas e compara célula a célula.

## 0. Preparar

1. Gere as planilhas: `python -m analise.regressao.prepara_excel`. Elas ficam em `analise/dados/excel/<base>_resultados.xlsx`
   (fora do git, porque têm microdados).
2. No Excel: **Arquivo → Opções → Suplementos → Gerenciar: Suplementos do Excel → Ir… → marcar "Ferramentas de Análise"**
   (em inglês, *Analysis ToolPak*). O botão **Análise de Dados** aparece na guia **Dados**.

## 1. Regressão (três modelos por base)

Na aba `dados`, a coluna A é o Y e as colunas seguintes estão nesta ordem: tela, depois covariáveis. Os três modelos usam
intervalos contíguos:

| Aba de saída (nome exato) | Intervalo Y | Intervalo X |
|---|---|---|
| `reg_completo` | A1:A(n+1) | da coluna B até a última |
| `reg_simples` | A1:A(n+1) | só as colunas de tela (B, ou B:C no Vigitel) |
| `reg_covariaveis` | A1:A(n+1) | só as covariáveis (da primeira depois da tela até a última) |

Passos: **Dados → Análise de Dados → Regressão (*Regression*) → OK**. Preencher Intervalo Y e Intervalo X; marcar
**Rótulos**; deixar **Constante é zero** desmarcado; **Nível de confiança** 95%; **Opções de saída → Nova planilha** com o
nome da tabela acima (ou intervalo de saída na célula A1 de uma aba vazia com esse nome). Resíduos são opcionais; a
conferência não usa.

O NHANES e a base empilhada Vigitel + NHANES saíram do trabalho em 2026-11-27 (EUA fora do trabalho).

## 2. Fórmulas de conferência (caminho B)

Na saída da Regressão (layout fixo: ANOVA nas linhas 12–14, coeficientes a partir da linha 17):

| Célula | Fórmula (Excel em inglês) | Excel em português |
|---|---|---|
| G12 | `=F.DIST.RT(E12,B12,B13)` | `=DIST.F.CD(E12;B12;B13)` |
| H17, H18, … | `=T.DIST.2T(ABS(D17),$B$13)` | `=DIST.T.BC(ABS(D17);$B$13)` |

G12 tem de repetir o "F de significação" (F12) e a coluna H tem de repetir o "valor-P" (coluna E).

Aba `f_parcial` (F parcial do bloco de tela = completo × só covariáveis):

| Célula | Conteúdo |
|---|---|
| B2 | número de restrições q (2 no Vigitel; 1 nas outras) |
| B3 | `=((reg_covariaveis!C13-reg_completo!C13)/B2)/(reg_completo!C13/reg_completo!B13)` |
| B5 | `=reg_completo!B13` |
| B6 | `=F.DIST.RT(B3,B2,B5)` |
| B7 | `=reg_completo!B5-reg_covariaveis!B5` (ΔR²) |
| B8 | `=B7/(1-reg_completo!B5)` (f²) |

## 3. ANOVA de um fator (Vigitel)

**Dados → Análise de Dados → Anova: fator único (*Anova: Single Factor*)**. Intervalo de entrada: aba `anova`, colunas
A:C (uma por faixa de tela, com rótulos na linha 1). Agrupado por **Colunas**; **Rótulos na primeira linha**; α = 0,05.
Saída na aba `anova_saida`, célula A1. Conferência: `H12 = F.DIST.RT(E12,C12,C13)`.

O F desta ANOVA tem de ser igual ao F global da aba `reg_simples` (regressão de Y nas 2 dummies de tela).

## 4. Testes t (Vigitel)

Aba `teste_t`: coluna A = ≥ 3 h, coluna B = < 1 h.

| Ferramenta | Aba de saída | Conferência |
|---|---|---|
| Teste-t: duas amostras presumindo variâncias diferentes (*t-Test: Two-Sample Assuming Unequal Variances*) | `teste_t_welch` | `D12 = T.DIST.2T(ABS(B9),B8)` |
| Teste-t: duas amostras presumindo variâncias equivalentes (*t-Test: Two-Sample Assuming Equal Variances*) | `teste_t_igual` | `D13 = T.DIST.2T(ABS(B10),B9)` |

Diferença média hipotética = 0; Rótulos marcado; α = 0,05.

**Atenção:** no teste de variâncias diferentes o Excel **arredonda o gl de Welch para inteiro** (célula B8). O script usa o gl
fracionário; por isso o p do Excel difere do p do relatório na 5ª ou 6ª casa (registrado em `resultados/005/conferencia.csv`).

Aba `dummy_2grupos` → Regressão com saída em `reg_dummy_2grupos`: o t da dummy (D18) é igual, em módulo, ao t do teste
com variâncias iguais.

## 5. Salvar e conferir

Salvar como `<base>_resultados.xlsx` na mesma pasta e rodar `python -m analise.regressao.confere_excel`. A conferência
reconhece os rótulos em inglês e em português, mas lê os números pela posição: não insira linhas nem mova as tabelas de saída.

## O que a automação faz de diferente

`excel_toolpak.ps1` chama as mesmas ferramentas pelo suplemento VBA (`ATPVBAEN.XLAM`): `Regress`, `Anova1`, `Pttestv`
(variâncias diferentes) e `Ttestm` (variâncias iguais). Em automação, o Excel não carrega os suplementos sozinho: o script
registra o `ANALYS32.XLL`, abre o `ATPVBAEN.XLAM`, usa uma instância própria do Excel por arquivo e a encerra no fim, sem
tocar em Excel que o usuário tenha aberto.
