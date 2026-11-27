"""T050 — Constrói e executa analise/notebooks/04_testes_brasil_eua.ipynb (nbformat + nbclient).

Uso: python -m analise.brasil_eua.notebook
"""
import nbformat as nbf
from nbclient import NotebookClient

from analise.comum import caminhos

md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

CELULAS = [
    md("""# 04 — Brasil: razão de prevalências e testes de hipótese na PNS 2019 e no Vigitel 2024 (spec 003)

**Pergunta.** Em adultos brasileiros, o tempo de tela no lazer se associa a problemas de sono nas duas pesquisas nacionais, e a associação tem o mesmo tamanho nas duas, entre faixas etárias e entre TV e tela digital?

**Os EUA saíram do trabalho em 27/11/2026.** A única base dos EUA (NHANES) é de 2005, antes do smartphone, e o tempo de tela daquela época não é comparável com o de 2019–2024. H3.3 e H3.6 foram retiradas; a decisão veio depois de os resultados com o NHANES já terem sido estimados e está registrada na spec.

**Transparência.** As hipóteses H3.1–H3.9 foram escritas depois da análise exploratória de 27/11/2026. O modelo, as covariáveis e os pesos foram fixados no plano antes desta execução. Na família 2, a exposição digital foi fixada como principal antes de rodar; a TV aparece como complementar.

Este notebook **mostra as técnicas** passo a passo e lê os resultados gerados por `python -m analise.brasil_eua.executa` (todos os números vêm de `resultados/003/tabelas/`)."""),
    code("""import sys, pathlib
raiz = pathlib.Path.cwd()
sys.path.insert(0, str(raiz))
import numpy as np, pandas as pd, patsy, statsmodels.api as sm
from scipy import stats
from IPython.display import Image, display, Markdown
from analise.comum import caminhos
from analise.comum.estatistica import le_csv, formata_p
from analise.brasil_eua.survey import poisson_desenho
pd.set_option("display.width", 160); pd.set_option("display.max_columns", 20)
T = caminhos.RESULTADOS / "003" / "tabelas"; F = caminhos.RESULTADOS / "003" / "figuras"
vig = pd.read_parquet(caminhos.processado("vigitel2024"))
pns = pd.read_parquet(caminhos.processado("pns2019"))
print(len(vig), len(pns))"""),
    md("""## 1. Razão de prevalências (RP)

Para um desfecho binário Y (problema de sono frequente) e exposição alta × baixa:

$$RP = \\frac{P(Y=1 \\mid \\text{tela} \\geq 3\\,h)}{P(Y=1 \\mid \\text{tela} < 1\\,h)}$$

Num modelo de Poisson com ligação log, $\\log E[Y \\mid x] = \\beta_0 + \\beta_1 x + \\dots$, o coeficiente da exposição dá $RP = e^{\\beta_1}$ ajustada pelas outras variáveis. Por que Poisson e não logística: com desfecho comum (15–25%), a razão de chances exageraria a RP.

**Teste de Wald.** $H_0: \\beta_1 = 0$ (RP = 1). Estatística $t = \\hat\\beta_1 / EP(\\hat\\beta_1)$; IC 95% da RP: $\\exp(\\hat\\beta_1 \\pm q_{0,975}\\, EP)$, com $q$ da t com os graus de liberdade do desenho (UPAs − estratos) ou da normal."""),
    md("### 1a. Conferência à mão: RP bruta sem peso no Vigitel = tabela 2×2 = Poisson"),
    code("""d = vig.dropna(subset=["dif_adormecer_freq", "tela_digital_cat"])
d = d[d.tela_digital_cat.isin([0, 2])].copy()
d["alta"] = (d.tela_digital_cat == 2).astype(float)
tab = pd.crosstab(d.alta, d.dif_adormecer_freq, margins=True); display(tab)
p_alta = tab.loc[1.0, 1.0] / tab.loc[1.0, "All"]; p_baixa = tab.loc[0.0, 1.0] / tab.loc[0.0, "All"]
rp_mao = p_alta / p_baixa
aj = poisson_desenho(d.reset_index(drop=True), "dif_adormecer_freq ~ alta")
print(f"prevalência alta {p_alta:.4f}, baixa {p_baixa:.4f}; RP à mão = {rp_mao:.4f}; RP Poisson = {np.exp(aj.beta[1]):.4f}")"""),
    md("""## 2. Variância com desenho amostral (linearização de Taylor)

Peso muda a estimativa; **estrato e UPA mudam o erro padrão**. A variância usada é a do `svyglm` do R:

$$A = \\sum_i w_i \\mu_i x_i x_i^T, \\qquad u_i = w_i x_i (y_i - \\mu_i), \\qquad z_{hj} = \\sum_{i \\in \\text{UPA } j,\\, \\text{estrato } h} u_i$$

$$B = \\sum_h \\frac{n_h}{n_h - 1} \\sum_j (z_{hj} - \\bar z_h)(z_{hj} - \\bar z_h)^T, \\qquad V(\\hat\\beta) = A^{-1} B A^{-1}$$

Abaixo, o cálculo passo a passo na PNS 2019 (8.027 UPAs em 574 estratos) e a comparação com a função do projeto.

**Graus de liberdade.** Regra única do projeto: d = UPAs − estratos. Sensibilidade: regra do `svyglm` do R, d − p + 1 (p = nº de parâmetros); na PNS, com milhares de UPAs, as duas regras dão o mesmo resultado prático. **Wald com q > 1 restrições:** correção de Korn-Graubard, $F = \\frac{d - q + 1}{d\\,q} W \\sim F(q,\\, d - q + 1)$."""),
    code("""dd = pns.dropna(subset=["problema_sono_freq", "tela_digital_cat", "faixa_etaria", "sexo", "escolaridade3"]).reset_index(drop=True)
dd["expo"] = dd.tela_digital_cat.astype(int)
y, X = patsy.dmatrices("problema_sono_freq ~ C(expo) + C(faixa_etaria) + sexo + C(escolaridade3)", dd, return_type="dataframe")
w = dd.peso.values
fit = sm.GLM(y.iloc[:, 0], X, family=sm.families.Poisson(), var_weights=w).fit()
mu = fit.mu; Xv = X.values
A = (Xv * (w * mu)[:, None]).T @ Xv
U = pd.DataFrame(Xv * (w * (y.iloc[:, 0].values - mu))[:, None])
upa = dd.estrato.astype(int).astype(str) + "_" + dd.upa.astype(int).astype(str)
Z = U.groupby(upa.values).sum(); est = dd.estrato.groupby(upa.values).first().reindex(Z.index)
B = sum(len(g) / (len(g) - 1) * (g - g.mean()).T.values @ (g - g.mean()).values for _, g in Z.groupby(est.values))
V = np.linalg.inv(A) @ B @ np.linalg.inv(A)
i = list(X.columns).index("C(expo)[T.2]")
ep_mao = np.sqrt(V[i, i])
aj = poisson_desenho(dd, "problema_sono_freq ~ C(expo) + C(faixa_etaria) + sexo + C(escolaridade3)", peso="peso", estrato="estrato", upa="upa")
gl = Z.shape[0] - est.nunique()
t = fit.params.iloc[i] / ep_mao
print(f"UPAs {Z.shape[0]}, estratos {est.nunique()}, gl do desenho = {gl}")
ingenuo = sm.GLM(y.iloc[:, 0], X, family=sm.families.Poisson(), var_weights=w / w.mean()).fit()  # peso normalizado (média 1), sem estrato/UPA
print(f"EP à mão = {ep_mao:.5f} | função do projeto = {aj.ep()[i]:.5f} | Poisson ponderado sem desenho = {ingenuo.bse.iloc[i]:.5f}")
print(f"RP = {np.exp(fit.params.iloc[i]):.3f}; t({gl}) = {t:.2f}; p = {2*stats.t.sf(abs(t), gl):.4f}")"""),
    md("Comparação dos erros padrão (T040): linearização (usada), cluster do `statsmodels`, Poisson ponderado sem desenho e robusto sem peso."),
    code("""display(le_csv(T / "comparacao_variancia.csv").round(4))"""),
    md("""## 3. Família 1 — associação em cada pesquisa brasileira

| H | H0 | H1 |
|---|---|---|
| H3.1 Vigitel | RP = 1 | RP ≠ 1 (esperado > 1) |
| H3.2 PNS | RP = 1 | RP ≠ 1 |
| H3.4 dose-resposta (Vigitel e PNS) | β do escore 0/1/2 = 0 | β ≠ 0 |

(H3.3, NHANES, retirada em 27/11/2026.)

Correção de Holm dentro da família, separada por exposição (digital e TV). α = 0,05."""),
    code("""H = le_csv(T / "hipoteses.csv")
cols = ["familia", "hipotese", "base", "exposicao", "estimativa", "ic_inf", "ic_sup", "estatistica", "tipo_estat", "gl2", "p", "p_holm", "decisao"]
display(H[H.familia.str.startswith("1")][cols].round(4))"""),
    code("""display(Image(filename=str(F / "rp_por_pais.png")))"""),
    md("""**Sensibilidade à regra de gl.** Mesmo teste com a regra do `svyglm` (d − p + 1) e Holm refeito por família. Só a PNS tem estrato e UPA; com milhares de UPAs, a regra não muda nenhuma decisão."""),
    code("""display(H[H.gl_desenho.notna()][["familia", "hipotese", "base", "exposicao", "gl2", "p_holm", "gl2_svyglm", "p_holm_svyglm", "decisao_svyglm"]].round(4))"""),
    md("""**Bruta × ajustada.** Na PNS, a RP bruta da tela digital fica abaixo de 1 e passa para acima de 1 quando a idade entra no modelo: quem usa mais tela é mais jovem, e os jovens relatam menos problema de sono (confundimento). Por isso o princípio 11 exige as duas lado a lado."""),
    code("""R = le_csv(T / "rp_bruta_ajustada.csv")
display(R[R.comparacao == "2 vs 0"].pivot_table(index=["base", "exposicao"], columns="modelo", values="rp").round(3))"""),
    md("**Forma da relação.** A faixa intermediária (1 a 3 h) não fica no meio do caminho: o excesso aparece em ≥ 3 h. O teste de desvio da linearidade é exploratório (não estava na spec)."),
    code("""display(Image(filename=str(F / "prevalencia_por_faixa_tela.png")))
display(le_csv(T / "desvio_linearidade_exploratorio.csv")[["base", "exposicao", "rp_1_vs_0", "rp_2_vs_0", "estatistica", "tipo", "p"]].round(4))"""),
    md("""## 4. Família 2 — comparações (Vigitel e PNS)

| H | Pergunta | Teste |
|---|---|---|
| H3.7 | A RP difere por faixa etária? | Wald conjunto das 6 interações idade × tela (F de Korn-Graubard com gl do desenho) |
| H3.8 | A RP da TV difere da RP digital na mesma pesquisa? | contraste β_TV − β_digital no mesmo modelo |
| H3.9 | A RP difere entre PNS e Vigitel? | z da diferença dos log-RP (amostras independentes) |

Para comparar duas RP de amostras independentes: $z = \\dfrac{\\log RP_2 - \\log RP_1}{\\sqrt{EP_1^2 + EP_2^2}}$.

(H3.6, Brasil × EUA, retirada em 27/11/2026.)"""),
    code("""display(H[H.familia == "2"][cols].round(4))
C = le_csv(T / "comparacoes_entre_bases.csv")
display(C[["hipotese", "exposicao", "metodo", "razao", "ic_inf", "ic_sup", "estatistica", "p"]].round(4))"""),
    md("""**Leitura.** Não foi detectada diferença entre faixas etárias, entre TV e tela digital, nem entre PNS e Vigitel; os IC são largos o bastante para que isso não seja prova de igualdade, e PNS e Vigitel usam perguntas de sono diferentes. As RP por faixa etária (figura abaixo) são estimadas por domínio: a variância usa o desenho inteiro."""),
    code("""display(Image(filename=str(F / "rp_por_faixa_etaria.png")))"""),
    md("## 5. Sensibilidades"),
    code("""S = le_csv(T / "sensibilidade.csv")
display(S[["base", "exposicao", "modelo", "comparacao", "rp", "ic_inf", "ic_sup", "p", "n"]].round(3))"""),
    md("""## 6. Conclusão e limitações

- Nas duas pesquisas brasileiras, tela digital ≥ 3 h/dia se associa a mais problema de sono frequente, com ajuste por idade, sexo e escolaridade, e com o desenho amostral no erro padrão. **Associação, não efeito**: os dados são transversais.
- Não foi detectada diferença de magnitude entre PNS e Vigitel, entre faixas etárias, nem entre TV e tela digital (IC largos: não é prova de igualdade). A forma é de limiar (≥ 3 h), não linear.
- Limitações: o item da PNS é diferente do do Vigitel; o Vigitel só cobre capitais e não divulga estrato/UPA; renda não entrou; sem comparação internacional nesta spec (os EUA saíram do trabalho; a comparação com outros países está na spec 004).

O resumo completo, com todas as tabelas, está em `resultados/003/RESUMO.md`."""),
]


def main():
    nb = nbf.v4.new_notebook()
    nb.cells = CELULAS
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    NotebookClient(nb, timeout=600, kernel_name="python3",
                   resources={"metadata": {"path": str(caminhos.RAIZ)}}).execute()
    caminhos.NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    destino = caminhos.NOTEBOOKS / "04_testes_brasil_eua.ipynb"
    nbf.write(nb, destino)
    print("ok:", destino)


if __name__ == "__main__":
    main()
