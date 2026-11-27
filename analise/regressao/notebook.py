"""T092 — Gera e executa analise/notebooks/06_regressao_linear.ipynb (nbformat + nbclient)."""
import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell as C, new_markdown_cell as M, new_notebook

from analise.comum import caminhos

CELULAS = [
    M("""# 06 — Regressão linear múltipla, ANOVA e teste t (spec 005)

Este notebook mostra **como** cada número da spec 005 é calculado e **como** ele foi conferido.
A ordem é a da aula: álgebra matricial → saída no formato do Excel → Excel de verdade → conferência → decisão.

- Spec: `specs/005-regressao-linear/spec.md` (hipóteses fixadas antes de rodar).
- Scripts: `analise/regressao/` (`ols.py`, `dados.py`, `modelos.py`, `confere_excel.py`, `diagnostico.py`).
- Resumo dos resultados: `resultados/005/RESUMO.md`.
- **EUA fora do trabalho (decisão do grupo, 2026-11-27):** H5.2, H5.8, H5.10 e H5.11 (NHANES 2005-06 e base
  empilhada) foram retiradas; a numeração original das hipóteses é mantida.

Regenerar tudo, a partir da raiz do repositório:

```text
python -m analise.regressao.prepara_excel   # planilhas para o Excel
python -m analise.regressao.roda_excel      # Análise de Dados do Excel (caminho A)
python -m analise.regressao.modelos         # script (caminho C) e hipóteses
python -m analise.regressao.confere_excel   # A × B × C
python -m analise.regressao.diagnostico     # pressupostos, sensibilidade e figuras
python -m analise.regressao.resumo          # RESUMO.md
python -m analise.regressao.notebook        # este notebook
```"""),
    C("""import sys, pathlib
raiz = pathlib.Path.cwd()
while not (raiz / "specs").exists():
    raiz = raiz.parent
sys.path.insert(0, str(raiz))
import numpy as np, pandas as pd
from scipy import stats
from IPython.display import Image, Markdown, display
from analise.comum import caminhos
from analise.comum.estatistica import le_csv, formata_p
from analise.regressao import dados as D
from analise.regressao.ols import mqo, summary_output
pd.set_option("display.width", 200); pd.set_option("display.max_columns", 30)
T = caminhos.RESULTADOS / "005" / "tabelas"; F = caminhos.RESULTADOS / "005" / "figuras\""""),
    M("""## 1. A regressão por álgebra matricial

Exemplo com a menor base, Okajima (Japão, n = 381): AIS (escala de insônia de Atenas, 8–32) explicada pelas horas de
celular nas 3 horas antes de dormir, com idade e sexo fixos (H5.6).

Fórmulas, com k = número de regressores sem o intercepto:

- coeficientes: **b = (XᵀX)⁻¹ Xᵀy**
- variância residual: s² = SQRes / (n − k − 1)
- erro padrão: EP(bⱼ) = √(s² · [(XᵀX)⁻¹]ⱼⱼ)
- estatística t: tⱼ = bⱼ / EP(bⱼ), com p = 2 · P(T(n − k − 1) > |tⱼ|)
- IC 95%: bⱼ ± t(0,975; n − k − 1) · EP(bⱼ)
- ANOVA da regressão: F = (SQReg / k) / (SQRes / (n − k − 1)), p = P(F(k, n − k − 1) > F)
- R² = SQReg / SQTot; R² ajustado = 1 − (1 − R²)(n − 1)/(n − k − 1)"""),
    C("""df, info = D.matriz("japao")
cols = info["tela"] + info["cov"]
y = df["ais"].to_numpy()
X = np.column_stack([np.ones(len(df)), df[cols].to_numpy()])
n, k = X.shape[0], X.shape[1] - 1
XtX_inv = np.linalg.inv(X.T @ X)
b = XtX_inv @ X.T @ y
e = y - X @ b
sq_res = e @ e; sq_tot = ((y - y.mean())**2).sum(); sq_reg = sq_tot - sq_res
gl = n - k - 1; s2 = sq_res / gl
ep = np.sqrt(s2 * np.diag(XtX_inv)); t = b / ep
p = 2 * stats.t.sf(np.abs(t), gl)
F_ = (sq_reg / k) / s2; pF = stats.f.sf(F_, k, gl)
print(f"n = {n}, k = {k}, gl do resíduo = {gl}")
print(f"R² = {sq_reg/sq_tot:.6f}   R² ajustado = {1-(1-sq_reg/sq_tot)*(n-1)/gl:.6f}   F = {F_:.4f}   p(F) = {pF:.3e}")
pd.DataFrame({"b": b, "EP": ep, "t": t, "p": p}, index=["Intercepto"] + cols)"""),
    M("""A mesma conta pela função do projeto (`analise/regressao/ols.py`) e pelo `statsmodels` dá o mesmo resultado.
A função devolve a tabela no layout do **SUMMARY OUTPUT** do Excel:"""),
    C("""a = mqo(df["ais"], df[cols])
import statsmodels.api as sm
s = sm.OLS(df["ais"], sm.add_constant(df[cols])).fit()
print("maior diferença de coeficiente (manual × função × statsmodels):", np.abs(a.b - b).max(), np.abs(s.params.to_numpy() - b).max())
summary_output(a)"""),
    M("""## 2. O Excel de verdade (caminho A) e a conferência

A ferramenta **Análise de Dados** do Excel (Analysis ToolPak) foi executada por automação COM
(`analise/regressao/excel_toolpak.ps1`), em uma instância própria do Excel. Ao lado de cada saída, a planilha recebe
fórmulas nativas que recalculam o p a partir da estatística e dos graus de liberdade (caminho B):
`=T.DIST.2T(ABS(t); gl)` para os coeficientes e `=F.DIST.RT(F; gl1; gl2)` para o F (em português: `DIST.T.BC` e `DIST.F.CD`).

Abaixo, a saída da Regressão do Excel para o Japão, exportada para CSV (`resultados/005/excel_saidas/`):"""),
    C("""saida = caminhos.RESULTADOS / "005" / "excel_saidas" / "japao__reg_completo.csv"
pd.read_csv(saida, sep=";", header=None, encoding="utf-8-sig").fillna("")"""),
    C("""cf = le_csv(caminhos.RESULTADOS / "005" / "conferencia.csv")
exc = cf.excecao_documentada.astype(str) == "True"
av = cf[~exc]
print(f"{len(av)} números conferidos; dentro da tolerância: {(av.dentro_tolerancia.astype(str) == 'True').sum()}; "
      f"exceções documentadas: {exc.sum()}")
print(f"maior diferença relativa A×C = {av.dif_rel_A_C.max():.2e};  B×C = {av.dif_rel_B_C.max():.2e}")
cf[cf.item.str.contains(": p|F de significação|p bicaudal", regex=True)][["base", "aba", "item", "A_toolpak", "B_formula", "C_script", "dif_rel_A_C"]].head(15)"""),
    M("""**Achado da conferência:** no teste t de duas amostras com variâncias diferentes (Welch), o Excel **arredonda os graus
de liberdade para inteiro** antes de calcular o p. O script usa o gl fracionário de Welch–Satterthwaite. A diferença é
pequena, mas só aparece porque o p foi conferido por mais de um caminho:"""),
    C("""cf[cf.excecao_documentada.astype(str) == "True"][["base", "item", "A_toolpak", "C_script", "dif_rel_A_C"]]"""),
    M("""## 3. Família R1 — o coeficiente da tela em cada base

Cinco testes t (um por base), corrigidos por Holm. No Vigitel decide a versão **com peso amostral** (princípio 8);
nas bases de repositório, a do Excel (não há desenho complexo).

**Erro padrão com peso:** o Vigitel só divulga o peso (sem estrato nem UPA), então cada pessoa é a sua UPA e o
gl é n − 1. Quando o Wald testa mais de um coeficiente (q > 1), usa a correção de Korn-Graubard,
F = (d − q + 1)/(d·q)·W, que com d tão grande coincide com W/q."""),
    C("""h = le_csv(T / "hipoteses.csv")
r1 = h[h.familia == "R1"].copy()
r1["p"] = r1.p.map(formata_p); r1["p_holm"] = r1.p_holm.map(formata_p)
r1[["hipotese", "rotulo", "y", "b", "ic_inf", "ic_sup", "estatistica", "gl2", "p", "p_holm", "decisao", "efeito", "versao_decisao"]].round(4)"""),
    C("""display(Image(filename=str(F / "efeitos_padronizados.png")))"""),
    M("""Leitura: no Vigitel, tela digital ≥ 3 h/dia se associa a um índice de insônia cerca de 0,6 ponto maior (escala 0–12)
que < 1 h, com idade, sexo e escolaridade fixos. O ganho de R² do bloco de tela é pequeno (menos de 1%): a associação
existe, mas explica pouco da variação entre pessoas. Na Argentina o sinal é o contrário do esperado."""),
    M("""## 4. Família R2 — ANOVA de um fator e teste t (Vigitel)

- **ANOVA de um fator:** compara as médias das 3 faixas de tela. O F é idêntico ao F global da regressão de Y nas 2 dummies.
- **Teste t:** ≥ 3 h × < 1 h. Com variâncias iguais, o t é idêntico ao t da dummy numa regressão simples."""),
    C("""r2 = h[h.familia == "R2"].copy()
for c in ("p", "p_holm", "p_sem_peso"): r2[c] = r2[c].map(formata_p)
r2[["hipotese", "rotulo", "teste", "estatistica", "gl1", "gl2", "p", "p_holm", "decisao", "efeito_nome", "efeito", "p_sem_peso"]].round(4)"""),
    C("""display(le_csv(T / "equivalencias.csv"))
display(Image(filename=str(F / "medias_por_faixa.png")))"""),
    M("""## 5. Bruta × ajustada e sem peso × com peso"""),
    C("""le_csv(T / "bruta_ajustada.csv").round(4)"""),
    M("""## 6. Pressupostos

Resíduo × ajustado (linearidade e variância constante), QQ-plot (normalidade), Breusch-Pagan (heterocedasticidade),
VIF (multicolinearidade) e distância de Cook (observações influentes). Com n grande, o Jarque-Bera rejeita normalidade
por desvios pequenos; o gráfico importa mais."""),
    C("""display(le_csv(T / "diagnostico.csv").round(4))
display(Image(filename=str(F / "diagnostico_vigitel2024.png")))"""),
    C("""s = le_csv(T / "sensibilidade.csv"); s["p"] = s.p.map(formata_p)
s[["hipotese", "analise", "b", "p", "muda_em_relacao_ao_principal", "exploratoria"]].round(4)"""),
    M("""## 7. Decisão

A tabela final, com p ajustado por Holm dentro de cada família, está em `resultados/005/tabelas/hipoteses.csv`, e a
leitura de cada hipótese em `resultados/005/RESUMO.md`. Lembrete: os dados são transversais, então os resultados
descrevem associação, não efeito do uso de tela."""),
    C("""display(Markdown((caminhos.RESULTADOS / "005" / "RESUMO.md").read_text(encoding="utf-8").split("## Família R2")[0].split("## Família R1")[1]))"""),
]


def main():
    nb = new_notebook(cells=CELULAS, metadata={"kernelspec": {"name": "python3", "display_name": "Python 3"},
                                               "language_info": {"name": "python"}})
    NotebookClient(nb, timeout=600, kernel_name="python3",
                   resources={"metadata": {"path": str(caminhos.RAIZ)}}).execute()
    caminhos.NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    destino = caminhos.NOTEBOOKS / "06_regressao_linear.ipynb"
    nbformat.write(nb, destino)
    print("executado e salvo:", destino)


if __name__ == "__main__":
    main()
