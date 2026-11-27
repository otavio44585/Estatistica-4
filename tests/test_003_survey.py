"""T041 — Testes da RP por Poisson com desenho amostral (spec 003).

Os três primeiros usam dados simulados só para conferir o código contra o statsmodels
(nada aqui é apresentado como dado real). O último usa as bases processadas.
"""
import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

from analise.brasil_eua.survey import poisson_desenho, mantel_haenszel
from analise.comum import caminhos


def _simula(n=3000, semente=1):
    rng = np.random.default_rng(semente)
    x = rng.integers(0, 3, n)
    z = rng.integers(0, 2, n)
    p = 0.15 * np.exp(0.2 * x + 0.1 * z)
    y = (rng.random(n) < p).astype(float)
    upa = rng.integers(0, 60, n)
    return pd.DataFrame({"y": y, "x": x, "z": z, "w": rng.uniform(0.5, 3, n),
                         "upa": upa, "estrato": upa // 2})


def test_sem_upa_igual_sanduiche_robusto_hc0_vezes_n_sobre_n_menos_1():
    d = _simula()
    a = poisson_desenho(d, "y ~ C(x) + z")
    X = sm.add_constant(pd.get_dummies(d.x, prefix="x", drop_first=True).astype(float).join(d.z))
    r = sm.GLM(d.y, X, family=sm.families.Poisson()).fit(cov_type="HC0")
    n = len(d)
    assert np.allclose(a.beta, r.params.values, atol=1e-8)
    assert np.allclose(a.cov, np.asarray(r.cov_params()) * n / (n - 1), rtol=1e-6)


def test_um_estrato_com_upa_igual_cluster_do_statsmodels_sem_correcao_vezes_g_sobre_g_menos_1():
    d = _simula()
    d["um"] = 0
    a = poisson_desenho(d, "y ~ C(x) + z", peso="w", estrato="um", upa="upa")
    X = patsy_X = sm.add_constant(pd.get_dummies(d.x, prefix="x", drop_first=True).astype(float).join(d.z))
    r = sm.GLM(d.y, patsy_X, family=sm.families.Poisson(), var_weights=d.w).fit(
        cov_type="cluster", cov_kwds={"groups": d.upa.values, "use_correction": False})
    G = d.upa.nunique()
    assert np.allclose(a.cov, np.asarray(r.cov_params()) * G / (G - 1), rtol=1e-6)


def test_invariante_a_escala_do_peso():
    d = _simula()
    a = poisson_desenho(d, "y ~ C(x) + z", peso="w", estrato="estrato", upa="upa")
    d["w2"] = d.w * 1234.5
    b = poisson_desenho(d, "y ~ C(x) + z", peso="w2", estrato="estrato", upa="upa")
    assert np.allclose(a.beta, b.beta) and np.allclose(a.cov, b.cov, rtol=1e-8)
    assert a.gl == d.assign(k=d.estrato.astype(str) + "_" + d.upa.astype(str)).k.nunique() - d.estrato.nunique()


# T041: RP ajustada só por faixa etária (Poisson, sem peso) × Mantel-Haenszel da exploração de 27/11
CASOS = [  # base, desfecho, exposição, RP de MH na exploração (docs/exploratorio_*.csv)
    ("pns2019", "problema_sono_freq", "tela_digital_cat", 1.17),
    ("pns2019", "problema_sono_freq", "tela_tv_cat", 1.18),
    ("vigitel2024", "dif_adormecer_freq", "tela_digital_cat", 1.23),
    ("vigitel2024", "dif_adormecer_freq", "tela_tv_cat", 1.24),
    # NHANES retirado em 2026-11-27 (EUA fora do trabalho)
]


@pytest.mark.parametrize("base,y,x,rp_explo", CASOS)
def test_t041_poisson_bate_com_mantel_haenszel(base, y, x, rp_explo):
    p = caminhos.processado(base)
    if not p.exists():
        pytest.skip("base não processada")
    d = pd.read_parquet(p)
    d = d[d[x].isin([0, 2])].dropna(subset=[y, x, "faixa_etaria"]).reset_index(drop=True)
    d["alta"] = (d[x] == 2).astype(float)
    a = poisson_desenho(d, f"{y} ~ alta + C(faixa_etaria)")
    rp_poisson = float(np.exp(a.beta[a.nomes.index("alta")]))
    rp_mh, _ = mantel_haenszel(d[y], d.alta, d.faixa_etaria)
    assert abs(rp_mh - rp_explo) < 0.006, f"MH recalculado {rp_mh:.3f} ≠ exploração {rp_explo}"
    assert abs(rp_poisson - rp_mh) < 0.01, f"Poisson {rp_poisson:.4f} × MH {rp_mh:.4f}"


# ---- correções da verificação independente (2026-11-27) ----
from scipy import stats as _st  # noqa: E402


def test_korn_graubard_wald():
    """F = (d − q + 1)/(d·q)·W com gl (q, d − q + 1); com q = 1 coincide com t²."""
    d = _simula()
    a = poisson_desenho(d, "y ~ C(x) + z", peso="w", estrato="estrato", upa="upa")
    termos = ["C(x)[T.1]", "C(x)[T.2]"]
    idx = [a.nomes.index(t) for t in termos]
    b, V = a.beta[idx], a.cov[np.ix_(idx, idx)]
    W = float(b @ np.linalg.solve(V, b))
    q, gl = 2, a.gl
    r = a.wald(termos)
    assert r["gl1"] == q and r["gl2"] == gl - q + 1
    assert np.isclose(r["estatistica"], (gl - q + 1) / (gl * q) * W)
    assert np.isclose(r["p"], _st.f.sf(r["estatistica"], q, gl - q + 1))
    r1 = a.wald(["z"])
    assert np.isclose(r1["estatistica"], a.termo("z")["estatistica"] ** 2) and r1["gl2"] == gl
    assert np.isclose(r1["p"], a.termo("z")["p"])
    sem = poisson_desenho(d, "y ~ C(x) + z", peso="w")
    r2 = sem.wald(termos)
    assert r2["tipo"] == "qui2" and r2["gl2"] is None


def test_dominio_usa_desenho_inteiro():
    """Ajuste só no domínio; variância com todas as UPAs (escores zero fora) = A⁻¹BA⁻¹ montado à mão."""
    d = _simula(n=4000, semente=7)
    d["dom"] = d.z == 1
    a = poisson_desenho(d, "y ~ C(x)", peso="w", estrato="estrato", upa="upa", dominio="dom")
    sub = d[d.dom].reset_index(drop=True)
    b = poisson_desenho(sub, "y ~ C(x)", peso="w", estrato="estrato", upa="upa")
    assert np.allclose(a.beta, b.beta, atol=1e-8)                 # mesma estimativa pontual
    k = d.estrato.astype(str) + "_" + d.upa.astype(str)
    assert a.n_upas == k.nunique() and a.gl == k.nunique() - d.estrato.nunique()
    assert a.n == int(d.dom.sum())
    # variância à mão: escores zero fora do domínio, centrados por estrato com todas as UPAs
    import patsy
    yy, X = patsy.dmatrices("y ~ C(x)", d, return_type="dataframe")
    Xv, yv, w = X.values, yy.iloc[:, 0].values, d.w.values * d.dom.values
    mu = np.exp(Xv @ a.beta)
    A = (Xv * (w * mu)[:, None]).T @ Xv
    U = pd.DataFrame(Xv * (w * (yv - mu))[:, None])
    Z = U.groupby(k.values).sum()
    est = d.estrato.groupby(k.values).first().reindex(Z.index)
    B = sum(len(g) / (len(g) - 1) * (g - g.mean()).T.values @ (g - g.mean()).values for _, g in Z.groupby(est.values))
    V = np.linalg.inv(A) @ B @ np.linalg.inv(A)
    assert np.allclose(a.cov, V, rtol=1e-8)
    # domínio = todos coincide com o ajuste comum
    d["todos"] = True
    c = poisson_desenho(d, "y ~ C(x)", peso="w", estrato="estrato", upa="upa", dominio="todos")
    e = poisson_desenho(d, "y ~ C(x)", peso="w", estrato="estrato", upa="upa")
    assert np.allclose(c.cov, e.cov) and np.allclose(c.beta, e.beta)


def test_regra_gl_svyglm_e_satterthwaite():
    d = _simula()
    a = poisson_desenho(d, "y ~ C(x) + z", peso="w", estrato="estrato", upa="upa")
    assert a.gl_svyglm() == a.gl - a.n_param + 1
    gs = a.satterthwaite("z")
    assert 1 <= gs <= a.gl + 1e-9          # Satterthwaite nunca passa do total de gl dos estratos
    assert a.com_gl(5).gl == 5 and a.gl != 5
