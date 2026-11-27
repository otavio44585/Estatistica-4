"""T087, T089, T091 — Todos os modelos da spec 005 no script (caminho C), sem peso e com peso.

Saídas em resultados/005/tabelas/:
  summary_<base>_<modelo>.csv       layout do SUMMARY OUTPUT (sem peso = o que o Excel calcula)
  summary_<base>_completo_ponderado.csv   Vigitel com peso amostral
  hipoteses.csv                     H5.1, H5.3–H5.7 e H5.9: estatística, gl, p, p Holm, decisão, efeito, IC
                                    (H5.2, H5.8, H5.10 e H5.11 retiradas em 2026-11-27: EUA fora do trabalho)
  bruta_ajustada.csv                coeficiente da tela na regressão simples × múltipla, sem e com peso
  anova_t.csv                       ANOVA de um fator e testes t (sem peso e com peso), médias por faixa
  equivalencias.csv                 checagens de consistência da spec (ANOVA = regressão nas dummies etc.)
"""
import numpy as np
import pandas as pd
from scipy import stats

from analise.comum import caminhos
from analise.comum.estatistica import holm, decisao, salva_csv
from analise.regressao import dados as D
from analise.regressao.ols import mqo, mqp, f_parcial, summary_output, wald_bloco

OUT = caminhos.saida("005")
T = OUT / "tabelas"


def _desenho(base, info):
    """Peso e, se a base tiver, estrato e UPA. O Vigitel só divulga o peso (cada pessoa é a sua UPA)."""
    des = info["desenho"]
    return des.peso, (des["estrato"] if "estrato" in des else None), (des["upa"] if "upa" in des else None)


def _efeito_padronizado(df, m, b, ep, nome):
    """Efeito em DP de Y: dummy -> b/DP(Y); contínuo -> b·DP(X)/DP(Y) (β padronizado)."""
    sy = df[m.y].std()
    fator = (1 / sy) if nome.startswith("tela_") else df[nome].std() / sy
    return b * fator, ep * fator


def d_cohen(y: pd.Series, alto: pd.Series, w: pd.Series | None = None) -> float:
    """d de Cohen com a MESMA definição sem e com peso: diferença de médias / DP combinado dentro dos grupos.
    s² = Σ_g Σ_i w*_i (y_i − ȳ_g)² / (n − 2), com w* = w · n / Σw (pesos normalizados para somar n).
    Com w = 1 é o d clássico, (ȳ₁ − ȳ₀) / s_combinado com n₁ + n₀ − 2 gl."""
    yv = y.to_numpy(float)
    g = alto.to_numpy(bool)
    wv = np.ones(len(yv)) if w is None else w.to_numpy(float)
    wv = wv * len(yv) / wv.sum()
    m1, m0 = np.average(yv[g], weights=wv[g]), np.average(yv[~g], weights=wv[~g])
    sq = (wv[g] * (yv[g] - m1) ** 2).sum() + (wv[~g] * (yv[~g] - m0) ** 2).sum()
    return (m1 - m0) / np.sqrt(sq / (len(yv) - 2))


def regressoes():
    linhas_r1, bruta, resumo = [], [], {}
    for m in D.MODELOS:
        df, info = D.matriz(m.base)
        y = df[m.y]
        Xc, Xs, Xv = df[info["tela"] + info["cov"]], df[info["tela"]], df[info["cov"]]
        a_c, a_s, a_v = mqo(y, Xc), mqo(y, Xs), mqo(y, Xv)
        fp = f_parcial(a_c, a_v)
        for nome, a in (("completo", a_c), ("simples", a_s), ("covariaveis", a_v)):
            salva_csv(summary_output(a), T / f"summary_{m.base}_{nome}.csv")
        c, cs = a_c.coef(m.tela_teste), a_s.coef(m.tela_teste)
        ez, ez_ep = _efeito_padronizado(df, m, c["b"], c["ep"], m.tela_teste)
        linha = dict(hipotese=m.hipotese, familia="R1", base=m.base, rotulo=m.rotulo, y=m.y_rotulo,
                     teste=f"t do coeficiente '{m.tela_teste}' (com covariáveis)", n=a_c.n,
                     b_sem_peso=c["b"], ep_sem_peso=c["ep"], t_sem_peso=c["t"], gl_sem_peso=c["gl"], p_sem_peso=c["p"],
                     ic_inf_sem_peso=c["ic_inf"], ic_sup_sem_peso=c["ic_sup"],
                     delta_r2_sem_peso=fp["delta_r2"], f2_sem_peso=fp["f2"], f_parcial_sem_peso=fp["f"],
                     p_f_parcial_sem_peso=fp["p"], r2_completo_sem_peso=a_c.r2, r2_aj_completo_sem_peso=a_c.r2_aj,
                     f_global_sem_peso=a_c.f, p_f_global_sem_peso=a_c.p_f, efeito_padronizado=ez,
                     efeito_padronizado_ep=ez_ep)
        bruta.append(dict(base=m.base, coeficiente=m.tela_teste, versao="sem peso", b_bruta=cs["b"],
                          ic_bruta=f"{cs['ic_inf']:.3f} a {cs['ic_sup']:.3f}", p_bruta=cs["p"], b_ajustada=c["b"],
                          ic_ajustada=f"{c['ic_inf']:.3f} a {c['ic_sup']:.3f}", p_ajustada=c["p"], n=a_c.n))
        if m.peso:
            w, est, upa = _desenho(m.base, info)
            p_c, p_s, p_v = mqp(y, Xc, w, est, upa), mqp(y, Xs, w, est, upa), mqp(y, Xv, w, est, upa)
            salva_csv(summary_output(p_c), T / f"summary_{m.base}_completo_ponderado.csv")
            cp, csp = p_c.coef(m.tela_teste), p_s.coef(m.tela_teste)
            wb = wald_bloco(p_c, info["tela"])
            d_r2 = p_c.r2 - p_v.r2
            linha.update(versao_decisao="com peso (" + p_c.tipo_ep + ")", regra_gl="UPAs − estratos",
                         gl_svyglm=p_c.extra["gl_svyglm"], b=cp["b"], ep=cp["ep"], estatistica=cp["t"],
                         gl1=np.nan, gl2=cp["gl"], p=cp["p"], ic_inf=cp["ic_inf"], ic_sup=cp["ic_sup"],
                         efeito_nome="ΔR² ponderado do bloco de tela (f²)", efeito=d_r2, f2=d_r2 / (1 - p_c.r2),
                         wald_bloco_tela_f=wb["f"], wald_bloco_tela_p=wb["p"])
            bruta.append(dict(base=m.base, coeficiente=m.tela_teste, versao=f"com peso ({p_c.tipo_ep})",
                              b_bruta=csp["b"], ic_bruta=f"{csp['ic_inf']:.3f} a {csp['ic_sup']:.3f}", p_bruta=csp["p"],
                              b_ajustada=cp["b"], ic_ajustada=f"{cp['ic_inf']:.3f} a {cp['ic_sup']:.3f}",
                              p_ajustada=cp["p"], n=p_c.n))
        else:
            linha.update(versao_decisao="sem peso (não há desenho complexo)", b=c["b"], ep=c["ep"], estatistica=c["t"],
                         gl1=np.nan, gl2=c["gl"], p=c["p"], ic_inf=c["ic_inf"], ic_sup=c["ic_sup"],
                         efeito_nome="ΔR² do bloco de tela (f²)", efeito=fp["delta_r2"], f2=fp["f2"])
        linhas_r1.append(linha)
        resumo[m.base] = (df, info, a_c)
    return linhas_r1, bruta, resumo


def anova_t():
    linhas, tab, equiv = [], [], []
    # H5.8 e H5.10 (NHANES) retiradas em 2026-11-27: EUA fora do trabalho.
    for h_an, h_t, base in (("H5.7", "H5.9", "vigitel2024"),):
        m = D.POR_BASE[base]
        g, info = D.grupos_tela(base)
        df, _ = D.matriz(base)
        y = df[m.y]
        w, est, upa = _desenho(base, info)
        # ANOVA de um fator, sem peso (o que o Excel faz)
        f, p = stats.f_oneway(*g.values())
        sq_tot = ((y - y.mean()) ** 2).sum()
        sq_ent = sum(len(s) * (s.mean() - y.mean()) ** 2 for s in g.values())
        eta2 = sq_ent / sq_tot
        reg = mqo(y, df[info["tela"]])
        equiv.append(dict(base=base, checagem="F da ANOVA de um fator = F global da regressão nas 2 dummies",
                          valor_1=f, valor_2=reg.f, dif_relativa=abs(f - reg.f) / f))
        # ANOVA com peso: regressão ponderada nas 2 dummies, F de Wald do bloco
        pr = mqp(y, df[info["tela"]], w, est, upa)
        wa = wald_bloco(pr, info["tela"])
        linhas.append(dict(hipotese=h_an, familia="R2", base=base, rotulo=m.rotulo, y=m.y_rotulo,
                           teste="ANOVA de um fator (3 faixas de tela)", n=len(y),
                           f_sem_peso=f, gl1_sem_peso=2, gl2_sem_peso=len(y) - 3, p_sem_peso=p, eta2_sem_peso=eta2,
                           versao_decisao=f"com peso (F de Wald com correção de Korn-Graubard, {pr.tipo_ep})",
                           regra_gl="UPAs − estratos", estatistica=wa["f"], gl1=wa["gl1"],
                           gl2=wa["gl2"], p=wa["p"], efeito_nome="η² ponderado (R² da regressão nas dummies)",
                           efeito=pr.r2, b=np.nan, ep=np.nan, ic_inf=np.nan, ic_sup=np.nan))
        # médias por faixa (sem e com peso)
        cat = info["tela_cat"]
        for k, (nome, s) in enumerate(g.items()):
            mask = (cat == k).to_numpy()
            ww = w.to_numpy()[mask]
            mp = np.average(y.to_numpy()[mask], weights=ww)
            tab.append(dict(base=base, faixa=nome, n=len(s), media=s.mean(), dp=s.std(), media_ponderada=mp))
        # teste t de Welch (sem peso) e equivalências
        a, b0 = g["≥ 3 h"], g["< 1 h"]
        tw = stats.ttest_ind(a, b0, equal_var=False)
        v1, v2 = a.var() / len(a), b0.var() / len(b0)
        gl_w = (v1 + v2) ** 2 / (v1 ** 2 / (len(a) - 1) + v2 ** 2 / (len(b0) - 1))
        p_gl_excel = 2 * stats.t.sf(abs(tw.statistic), round(gl_w))
        ti = stats.ttest_ind(a, b0, equal_var=True)
        sp = np.sqrt(((len(a) - 1) * a.var() + (len(b0) - 1) * b0.var()) / (len(a) + len(b0) - 2))
        dif = a.mean() - b0.mean()
        tc = stats.t.ppf(0.975, gl_w)
        y2 = pd.concat([a, b0]).reset_index(drop=True)
        dmy = pd.DataFrame({"tela_3h_mais": [1.0] * len(a) + [0.0] * len(b0)})
        r2g = mqo(y2, dmy)
        equiv.append(dict(base=base, checagem="t com variâncias iguais = t da dummy na regressão simples (2 grupos)",
                          valor_1=ti.statistic, valor_2=r2g.t[1], dif_relativa=abs(ti.statistic - r2g.t[1]) / abs(ti.statistic)))
        equiv.append(dict(base=base, checagem="t de Welch × t com variâncias iguais (diferem; registrado)",
                          valor_1=tw.statistic, valor_2=ti.statistic,
                          dif_relativa=abs(tw.statistic - ti.statistic) / abs(ti.statistic)))
        equiv.append(dict(base=base, checagem="p de Welch: gl fracionário (script) × gl inteiro (Excel)",
                          valor_1=tw.pvalue, valor_2=p_gl_excel, dif_relativa=abs(tw.pvalue - p_gl_excel) / max(tw.pvalue, 1e-300)))
        # t com peso: regressão ponderada de Y na dummy ≥ 3 h, só nos dois grupos
        cat = info["tela_cat"]
        sub = (cat.isin([0, 2])).to_numpy()
        ys = y[sub].reset_index(drop=True)
        xs = pd.DataFrame({"tela_3h_mais": (cat[sub] == 2).astype(float).reset_index(drop=True)})
        ws_ = w[sub].reset_index(drop=True)
        es_ = None if est is None else est[sub].reset_index(drop=True)
        us_ = None if upa is None else upa[sub].reset_index(drop=True)
        pt = mqp(ys, xs, ws_, es_, us_)
        cpt = pt.coef("tela_3h_mais")
        linhas.append(dict(hipotese=h_t, familia="R2", base=base, rotulo=m.rotulo, y=m.y_rotulo,
                           teste="t de Welch: ≥ 3 h × < 1 h", n=len(a) + len(b0),
                           f_sem_peso=np.nan, t_sem_peso=tw.statistic, gl_sem_peso=gl_w, p_sem_peso=tw.pvalue,
                           p_sem_peso_gl_excel=p_gl_excel, dif_sem_peso=dif,
                           ic_inf_sem_peso=dif - tc * np.sqrt(v1 + v2), ic_sup_sem_peso=dif + tc * np.sqrt(v1 + v2),
                           d_cohen_sem_peso=d_cohen(ys, xs.tela_3h_mais == 1),
                           versao_decisao=f"com peso (diferença de médias ponderada, {pt.tipo_ep})", regra_gl="UPAs − estratos",
                           estatistica=cpt["t"], gl1=np.nan, gl2=cpt["gl"], p=cpt["p"], b=cpt["b"], ep=cpt["ep"],
                           ic_inf=cpt["ic_inf"], ic_sup=cpt["ic_sup"],
                           efeito_nome="d de Cohen ponderado (DP combinado dentro dos grupos)",
                           efeito=d_cohen(ys, xs.tela_3h_mais == 1, ws_)))
        equiv.append(dict(base=base, checagem="d de Cohen da função = (ȳ₁ − ȳ₀)/s combinado clássico (sem peso)",
                          valor_1=d_cohen(ys, xs.tela_3h_mais == 1), valor_2=dif / sp,
                          dif_relativa=abs(d_cohen(ys, xs.tela_3h_mais == 1) - dif / sp) / abs(dif / sp)))
    return linhas, tab, equiv


def main():
    r1, bruta, _ = regressoes()
    r2, tab, equiv = anova_t()
    h = pd.DataFrame(r1 + r2)
    h["p_holm"] = np.nan
    for fam in ("R1", "R2"):
        msk = h.familia == fam
        h.loc[msk, "p_holm"] = holm(h.loc[msk, "p"].to_numpy())
    h["decisao"] = [decisao(p) for p in h.p_holm]
    salva_csv(h, T / "hipoteses.csv")
    salva_csv(pd.DataFrame(bruta), T / "bruta_ajustada.csv")
    salva_csv(pd.DataFrame(tab), T / "medias_por_faixa.csv")
    salva_csv(pd.DataFrame(equiv), T / "equivalencias.csv")
    cols = ["hipotese", "base", "b", "estatistica", "gl2", "p", "p_holm", "decisao", "efeito"]
    print(h[cols].to_string())


if __name__ == "__main__":
    main()
