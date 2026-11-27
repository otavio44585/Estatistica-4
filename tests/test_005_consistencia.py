"""T082 — Checagens de consistência da spec 005 e conferência do MQO contra o statsmodels."""
import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm
from scipy import stats

from analise.comum import caminhos
from analise.comum.estatistica import le_csv
from analise.regressao.ols import korn_graubard, mqo, mqp, f_parcial, wald_bloco


def _gera(n=400, semente=7):
    """Dados construídos só para testar a álgebra (não são amostra de nada)."""
    r = np.random.default_rng(semente)
    X = pd.DataFrame({"x1": r.normal(size=n), "x2": r.integers(0, 2, n).astype(float), "x3": r.normal(size=n)})
    y = pd.Series(1 + 0.3 * X.x1 - 0.5 * X.x2 + r.normal(size=n))
    return y, X


def ic_p_consistentes(b, lo, hi, p, alfa=0.05) -> bool:
    """p < α se e somente se o IC (1 − α) não contém 0."""
    return (p < alfa) == (lo > 0 or hi < 0)


def test_mqo_igual_statsmodels():
    y, X = _gera()
    a = mqo(y, X)
    s = sm.OLS(y, sm.add_constant(X)).fit()
    assert np.allclose(a.b, s.params, rtol=1e-12) and np.allclose(a.ep, s.bse, rtol=1e-10)
    assert np.allclose(a.p, s.pvalues, rtol=1e-8) and np.isclose(a.f, s.fvalue) and np.isclose(a.r2_aj, s.rsquared_adj)


def test_p_e_ic_consistentes_e_falha_com_p_alterado():
    y, X = _gera()
    a = mqo(y, X)
    for j in range(len(a.b)):
        assert ic_p_consistentes(a.b[j], a.ic_inf[j], a.ic_sup[j], a.p[j])
    j = int(np.argmin(a.p))                        # coeficiente claramente significativo
    assert not ic_p_consistentes(a.b[j], a.ic_inf[j], a.ic_sup[j], 0.20)   # p alterado de propósito


def test_f_parcial_com_uma_restricao_igual_t_ao_quadrado():
    y, X = _gera()
    c, r = mqo(y, X), mqo(y, X[["x2", "x3"]])
    assert np.isclose(f_parcial(c, r)["f"], c.t[1] ** 2, rtol=1e-10)


def test_anova_igual_regressao_nas_dummies_e_t_igual_dummy():
    r = np.random.default_rng(3)
    g = r.integers(0, 3, 600)
    y = pd.Series(r.normal(size=600) + 0.2 * g)
    f, _ = stats.f_oneway(*[y[g == k] for k in range(3)])
    reg = mqo(y, pd.DataFrame({"d1": (g == 1) * 1.0, "d2": (g == 2) * 1.0}))
    assert np.isclose(f, reg.f, rtol=1e-10)
    m = g != 1
    t = stats.ttest_ind(y[g == 2], y[g == 0], equal_var=True).statistic
    r2 = mqo(y[m].reset_index(drop=True), pd.DataFrame({"d": (g[m] == 2) * 1.0}))
    assert np.isclose(t, r2.t[1], rtol=1e-10)


def test_mqp_sem_desenho_igual_hc0_corrigido():
    y, X = _gera()
    a = mqp(y, X, pd.Series(np.ones(len(y))))
    s = sm.OLS(y, sm.add_constant(X)).fit(cov_type="HC0")
    n = len(y)
    assert np.allclose(a.b, s.params) and np.allclose(a.ep, s.bse * np.sqrt(n / (n - 1)), rtol=1e-10)


def test_mqp_um_estrato_igual_cluster_do_statsmodels():
    y, X = _gera()
    upa = pd.Series(np.repeat(np.arange(40), 10))
    a = mqp(y, X, pd.Series(np.ones(len(y))), pd.Series(np.zeros(len(y))), upa)
    s = sm.OLS(y, sm.add_constant(X)).fit(cov_type="cluster", cov_kwds={"groups": upa, "use_correction": False})
    G = 40
    assert np.allclose(a.ep, s.bse * np.sqrt(G / (G - 1)), rtol=1e-8)
    assert a.gl_res == 40 - 1                                   # regra do projeto: UPAs − estratos
    assert a.extra["gl_svyglm"] == (40 - 1) + 1 - 4             # sensibilidade: regra do svyglm
    b = mqp(y, X, pd.Series(np.ones(len(y))), pd.Series(np.zeros(len(y))), upa, regra_gl="svyglm")
    assert b.gl_res == 36 and np.allclose(a.ep, b.ep)


def test_korn_graubard():
    # F = (d − q + 1)/(d·q)·W com gl (q, d − q + 1); com d grande tende a W/q
    kg = korn_graubard(12.0, 2, 15)
    assert np.isclose(kg["f"], 14 / 30 * 12.0) and kg["gl1"] == 2 and kg["gl2"] == 14
    assert np.isclose(kg["p"], stats.f.sf(14 / 30 * 12.0, 2, 14))
    assert np.isclose(korn_graubard(12.0, 2, 1e9)["f"], 6.0, rtol=1e-6)
    y, X = _gera()
    upa = pd.Series(np.repeat(np.arange(40), 10))
    est = pd.Series(np.repeat(np.arange(20), 20))
    a = mqp(y, X, pd.Series(np.ones(len(y))), est, upa)
    wb = wald_bloco(a, ["x1", "x2"])
    assert wb["gl2"] == a.gl_res - 2 + 1 and wb["gl1"] == 2


def test_mqp_estrato_com_uma_upa_igual_a_regra_da_003():
    """Estrato com 1 UPA: centrado na média geral das UPAs, fator 1 (como analise/brasil_eua/survey.py)."""
    y, X = _gera()
    upa = pd.Series(np.repeat(np.arange(40), 10))
    est = pd.Series(np.where(np.arange(400) < 10, 99, np.repeat(np.arange(20), 20)))   # estratos 99 e 0 ficam com 1 UPA cada
    a = mqp(y, X, pd.Series(np.ones(len(y))), est, upa)
    assert a.extra["estratos_1upa"] == 2
    Xm = np.column_stack([np.ones(400), X.to_numpy()])
    A = np.linalg.inv(Xm.T @ Xm)
    e = y.to_numpy() - Xm @ (A @ Xm.T @ y.to_numpy())
    U = pd.DataFrame(Xm * e[:, None]).groupby(upa.to_numpy()).sum().to_numpy()
    eu = pd.Series(est.to_numpy()).groupby(upa.to_numpy()).first().to_numpy()
    G = np.zeros((4, 4))
    for h in np.unique(eu):
        Uh = U[eu == h]
        c = Uh - (U.mean(axis=0) if len(Uh) == 1 else Uh.mean(axis=0))
        G += (1 if len(Uh) == 1 else len(Uh) / (len(Uh) - 1)) * c.T @ c
    assert np.allclose(a.ep, np.sqrt(np.diag(A @ G @ A)), rtol=1e-10)


def test_d_cohen_mesma_definicao_com_e_sem_peso():
    from analise.regressao.modelos import d_cohen
    r = np.random.default_rng(5)
    y = pd.Series(r.normal(size=300))
    g = pd.Series(r.integers(0, 2, 300) == 1)
    a, b = y[g], y[~g]
    sp = np.sqrt(((len(a) - 1) * a.var() + (len(b) - 1) * b.var()) / (len(y) - 2))
    assert np.isclose(d_cohen(y, g), (a.mean() - b.mean()) / sp, rtol=1e-12)
    assert np.isclose(d_cohen(y, g, pd.Series(np.full(300, 7.0))), d_cohen(y, g), rtol=1e-12)


def test_resultados_salvos_consistentes():
    f = caminhos.RESULTADOS / "005" / "tabelas" / "hipoteses.csv"
    if not f.exists():
        pytest.skip("rode analise.regressao.modelos")
    h = le_csv(f)
    assert (h.p_holm >= h.p - 1e-15).all() and (h.p_holm <= 1).all()
    # H5.2, H5.8, H5.10 e H5.11 retiradas em 2026-11-27 (EUA fora do trabalho)
    assert set(h.hipotese) == {"H5.1", "H5.3", "H5.4", "H5.5", "H5.6", "H5.7", "H5.9"}
    assert not h.base.astype(str).str.contains("nhanes").any()
    assert set(h[h.familia == "R1"].hipotese) == {"H5.1", "H5.3", "H5.4", "H5.5", "H5.6"}
    assert set(h[h.familia == "R2"].hipotese) == {"H5.7", "H5.9"}
    for _, r in h.dropna(subset=["ic_inf"]).iterrows():
        assert ic_p_consistentes(r.b, r.ic_inf, r.ic_sup, r.p), r.hipotese
    eq = le_csv(caminhos.RESULTADOS / "005" / "tabelas" / "equivalencias.csv")
    exatas = eq[eq.checagem.str.contains(" = ")]
    assert (exatas.dif_relativa < 1e-9).all()
