"""T090 — Diagnóstico de pressupostos, sensibilidades e figuras da spec 005.

Saídas:
  resultados/005/tabelas/diagnostico.csv     Breusch-Pagan, Jarque-Bera, VIF da tela e VIF máximo, nº de influentes (Cook > 4/n)
      A categoria de referência das dummies é a mais frequente (dados.py): com a referência pequena (renda 1 em
      Xuzhou, n = 33; escolaridade dos pais 1 na Argentina, n = 11) o VIF passava de 10 por colinearidade entre as
      próprias dummies. O coeficiente da tela não depende da referência.
  resultados/005/tabelas/sensibilidade.csv   coeficiente da tela sob cada variação, e se a decisão mudaria
  resultados/005/figuras/diagnostico_<base>.png   resíduo × ajustado e QQ-plot
  resultados/005/figuras/efeitos_padronizados.png coeficiente da tela em DP do desfecho, por base (família R1)
  resultados/005/figuras/medias_por_faixa.png     índice de insônia por faixa de tela, Vigitel × NHANES
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import OLSInfluence, variance_inflation_factor

from analise.comum import caminhos
from analise.comum.estatistica import ALFA, le_csv, salva_csv
from analise.comum.graficos import COR_PAIS, COR_NEUTRA, PAIS_BASE, estilo, salva
from analise.regressao import dados as D
from analise.regressao.ols import mqo, mqp

import matplotlib.pyplot as plt  # noqa: E402  (backend definido em analise.comum.graficos)

OUT = caminhos.saida("005")
T, F = OUT / "tabelas", OUT / "figuras"


def _sm(df, y, cols):
    return sm.OLS(df[y], sm.add_constant(df[cols].astype(float))).fit()


def diagnostico():
    estilo()
    linhas = []
    for m in D.MODELOS:
        df, info = D.matriz(m.base)
        cols = info["tela"] + info["cov"]
        fit = _sm(df, m.y, cols)
        bp = het_breuschpagan(fit.resid, fit.model.exog)
        jb = stats.jarque_bera(fit.resid)
        ex = fit.model.exog
        vif = [variance_inflation_factor(ex, j) for j in range(1, ex.shape[1])]
        cook = OLSInfluence(fit).cooks_distance[0]
        n_inf = int((cook > 4 / len(df)).sum())
        linhas.append(dict(base=m.base, n=len(df), breusch_pagan_lm=bp[0], breusch_pagan_p=bp[1],
                           jarque_bera=jb.statistic, jarque_bera_p=jb.pvalue, assimetria_residuos=stats.skew(fit.resid),
                           vif_tela=vif[cols.index(m.tela_teste)],
                           vif_maximo=max(vif), regressor_vif_maximo=cols[int(np.argmax(vif))],
                           influentes_cook_4n=n_inf, pct_influentes=100 * n_inf / len(df)))
        fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
        cor = COR_PAIS[PAIS_BASE[m.base]]
        ax[0].scatter(fit.fittedvalues, fit.resid, s=4, alpha=0.25, color=cor)
        ax[0].axhline(0, color=COR_NEUTRA, lw=1)
        ax[0].set(xlabel="valor ajustado", ylabel="resíduo", title=f"{m.rotulo}: resíduo × ajustado")
        (osm, osr), (sl, ic, _) = stats.probplot(fit.resid, dist="norm")
        ax[1].scatter(osm, osr, s=4, alpha=0.3, color=cor)
        ax[1].plot(osm, sl * osm + ic, color=COR_NEUTRA, lw=1)
        ax[1].set(xlabel="quantil teórico (normal)", ylabel="quantil dos resíduos", title="QQ-plot dos resíduos")
        salva(fig, F / f"diagnostico_{m.base}.png")
    salva_csv(pd.DataFrame(linhas), T / "diagnostico.csv")
    return pd.DataFrame(linhas)


def sensibilidade():
    h = le_csv(T / "hipoteses.csv").set_index("hipotese")
    linhas = []

    def add(m, analise, b, ep, p, n, exploratoria=False):
        p0 = h.loc[m.hipotese, "p"]
        linhas.append(dict(hipotese=m.hipotese, base=m.base, analise=analise, b=b, ep=ep, p=p, n=n,
                           decisao_bruta_alfa=("rejeita H0" if p < ALFA else "não rejeita H0"),
                           muda_em_relacao_ao_principal=(p < ALFA) != (p0 < ALFA),
                           exploratoria=exploratoria))

    for m in D.MODELOS:
        df, info = D.matriz(m.base)
        cols = info["tela"] + info["cov"]
        j = cols.index(m.tela_teste) + 1
        hc3 = _sm(df, m.y, cols).get_robustcov_results(cov_type="HC3")
        add(m, "EP robusto HC3 (sem peso)", hc3.params[j], hc3.bse[j], hc3.pvalues[j], len(df))
        fit = _sm(df, m.y, cols)
        cook = OLSInfluence(fit).cooks_distance[0]
        sem = df[cook <= 4 / len(df)].reset_index(drop=True)
        a = mqo(sem[m.y], sem[cols]).coef(m.tela_teste)
        add(m, "sem observações influentes (Cook > 4/n)", a["b"], a["ep"], a["p"], len(sem))
        if m.y == "latencia_min":
            dl = df.copy()
            dl[m.y] = np.log1p(dl[m.y])
            a = mqo(dl[m.y], dl[cols]).coef(m.tela_teste)
            add(m, "log(1 + latência)", a["b"], a["ep"], a["p"], len(dl))
        if m.base == "argentina":
            ds, inf2 = D.matriz(m.base, sens_serie=True)
            c2 = inf2["tela"] + inf2["cov"]
            a = mqo(ds[m.y], ds[c2]).coef(m.tela_teste)
            add(m, "série escolar no lugar da idade (mais casos completos)", a["b"], a["ep"], a["p"], len(ds))
        if m.base == "nhanes0506":
            des = info["desenho"]
            pc = mqp(df[m.y], df[cols], des.peso, des.estrato, des.upa, regra_gl="svyglm")
            c = pc.coef(m.tela_teste)
            add(m, f"regra do svyglm, gl = d − p + 1 = {pc.gl_res} (com peso)", c["b"], c["ep"], c["p"], len(df))
            a = mqo(df[m.y], df[cols]).coef(m.tela_teste)
            add(m, "sem peso (o que o Excel calcula)", a["b"], a["ep"], a["p"], len(df))
        if m.base == "vigitel2024":
            a = mqo(df[m.y], df[cols]).coef(m.tela_teste)
            add(m, "sem peso (o que o Excel calcula)", a["b"], a["ep"], a["p"], len(df))
        # desfechos secundários (exploratórios, fora das famílias)
        alt = {"vigitel2024": ["sono_horas"], "nhanes0506": ["sono_horas", "latencia_min"], "argentina": ["sono_horas"],
               "turquia": ["sono_horas"], "japao": ["sono_horas"]}.get(m.base, [])
        for yc in alt:
            da, ia = D.matriz(m.base, y_col=yc)
            ca = ia["tela"] + ia["cov"]
            if m.peso:
                des = ia["desenho"]
                est = des.estrato if m.base == "nhanes0506" else None
                upa = des.upa if m.base == "nhanes0506" else None
                a = mqp(da[yc], da[ca], des.peso, est, upa).coef(m.tela_teste)
            else:
                a = mqo(da[yc], da[ca]).coef(m.tela_teste)
            add(m, f"desfecho secundário: {yc}" + (" (com peso)" if m.peso else ""), a["b"], a["ep"], a["p"],
                len(da), exploratoria=True)
    out = pd.DataFrame(linhas)
    salva_csv(out, T / "sensibilidade.csv")
    return out


def figuras():
    estilo()
    h = le_csv(T / "hipoteses.csv")
    r1 = h[h.familia == "R1"].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    for i, r in r1.iterrows():
        fator = r.efeito_padronizado / r.b_sem_peso
        est, lo, hi = r.b * fator, r.ic_inf * fator, r.ic_sup * fator
        cor = COR_PAIS[PAIS_BASE[r.base]]
        ax.errorbar(est, i, xerr=[[est - lo], [hi - est]], fmt="o", color=cor, capsize=3)
        ax.text(max(hi, 0) + 0.02, i, f"{r.rotulo}: {r.y}", va="center", fontsize=8)
    ax.axvline(0, color=COR_NEUTRA, lw=1)
    ax.set_yticks([])
    ax.set_xlim(-0.3, 0.75)
    ax.set_xlabel("efeito da tela em desvios-padrão do desfecho (IC 95%)\n"
                  "Vigitel e NHANES: ≥ 3 h × < 1 h, b/DP(Y); demais: β padronizado (1 DP a mais de exposição)", fontsize=8.5)
    ax.set_title("Família R1: tela × sono com covariáveis (versão que decide a hipótese)")
    ax.invert_yaxis()
    salva(fig, F / "efeitos_padronizados.png")

    mf = le_csv(T / "medias_por_faixa.csv")
    fig, ax = plt.subplots(figsize=(6, 3.6))
    for base, pais in (("vigitel2024", "Brasil"), ("nhanes0506", "EUA")):
        s = mf[mf.base == base]
        ax.plot(s.faixa, s.media_ponderada, "o-", color=COR_PAIS[pais], label=f"{D.POR_BASE[base].rotulo} (com peso)")
        ax.plot(s.faixa, s.media, "o--", color=COR_PAIS[pais], alpha=0.5, label=f"{D.POR_BASE[base].rotulo} (sem peso)")
    ax.set(xlabel="tempo de tela digital no lazer", ylabel="índice de insônia médio (0-12)",
           title="Índice de insônia por faixa de tela")
    ax.legend(fontsize=8)
    salva(fig, F / "medias_por_faixa.png")


def main():
    d = diagnostico()
    s = sensibilidade()
    figuras()
    print(d[["base", "breusch_pagan_p", "jarque_bera_p", "vif_tela", "vif_maximo", "regressor_vif_maximo", "influentes_cook_4n"]].to_string())
    print(s[["hipotese", "analise", "b", "p", "muda_em_relacao_ao_principal"]].to_string())


if __name__ == "__main__":
    main()
