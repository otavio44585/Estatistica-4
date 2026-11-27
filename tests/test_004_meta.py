"""Spec 004 — métodos da comparação mundial (correlação na escala z e meta-análise)."""
import numpy as np
import pandas as pd
import pytest
from scipy import stats
from statsmodels.stats.meta_analysis import combine_effects

from analise.comum import caminhos
from analise.comum.estatistica import le_csv
from analise.mundial import metodos as M

Y = np.array([0.10, 0.25, 0.05, 0.30, 0.18])     # efeitos de teste (escala z), não são dados do trabalho
V = np.array([0.004, 0.010, 0.002, 0.020, 0.006])


def test_dersimonian_laird_igual_statsmodels():
    m = M.dersimonian_laird(Y, V)
    sm = combine_effects(Y, V, method_re="dl")
    assert np.isclose(m["mu"], sm.mean_effect_re, atol=1e-12)
    assert np.isclose(m["ep"], sm.sd_eff_w_re, atol=1e-12)
    assert np.isclose(m["Q"], sm.q, atol=1e-12)
    assert np.isclose(m["tau2"], sm.tau2, atol=1e-12)
    assert np.isclose(m["I2"], sm.i2, atol=1e-12)


def test_sem_heterogeneidade_aleatorio_igual_fixo():
    m = M.dersimonian_laird(np.full(4, 0.2), np.array([0.01, 0.02, 0.03, 0.04]))
    assert m["tau2"] == 0 and np.isclose(m["mu"], m["mu_fixo"]) and m["I2"] == 0


def test_ic_i2_contem_estimativa():
    m = M.dersimonian_laird(Y, V)
    assert m["I2_ic_inf"] <= m["I2"] <= m["I2_ic_sup"]


def test_postos_ponderados_com_peso_igual_reproduzem_spearman():
    rng = np.random.default_rng(1)
    x, y = rng.integers(0, 5, 300).astype(float), rng.normal(size=300)
    assert np.isclose(M.spearman_ponderado(x, y, np.ones(300)), stats.spearmanr(x, y).statistic, atol=1e-12)


def test_efeito_inverte_sinal_e_ep_fhp():
    rng = np.random.default_rng(2)
    x = rng.normal(size=200)
    y = x + rng.normal(size=200)
    a, b = M.efeito(x, y), M.efeito(x, y, inverte=True)
    assert np.isclose(a["rho"], -b["rho"]) and np.isclose(a["ep_fhp"], np.sqrt(1.06 / 197))


def test_spearman_parcial_igual_correlacao_dos_residuos():
    rng = np.random.default_rng(3)
    c = rng.normal(size=500)
    x, y = c + rng.normal(size=500), c + rng.normal(size=500)
    e = M.spearman_parcial(x, y, c)
    rx, ry, rc = (stats.rankdata(a) for a in (x, y, c))
    res = lambda a: a - np.polyval(np.polyfit(rc, a, 1), rc)
    assert np.isclose(e["rho"], np.corrcoef(res(rx), res(ry))[0, 1], atol=1e-10)


def test_tost():
    dentro = M.tost_equivalencia(np.arctanh(0.28), 0.01, 0.21, 0.35)
    fora = M.tost_equivalencia(np.arctanh(0.02), 0.01, 0.21, 0.35)
    assert dentro["p"] < 0.05 and fora["p"] > 0.5


def test_subgrupos_iguais_dao_q_entre_zero():
    df = pd.DataFrame({"tipo": ["a", "a", "b", "b"], "z": [0.1, 0.2, 0.1, 0.2], "ep": [0.05] * 4, "base": list("wxyz")})
    _, qb = M.subgrupos(df)
    assert np.isclose(qb["Q_entre"], 0)


def test_rmcorr_igual_pearson_centrado():
    df = pd.DataFrame({"s": np.repeat([1, 2, 3], 4), "x": [1, 2, 3, 4, 5, 7, 6, 8, 2, 2, 3, 5.0],
                       "y": [2, 1, 4, 3, 9, 8, 7, 9, 1, 3, 2, 4.0]})
    r = M.rmcorr(df, "s", "x", "y")
    xc = df.x - df.groupby("s").x.transform("mean")
    yc = df.y - df.groupby("s").y.transform("mean")
    assert np.isclose(r["r"], np.corrcoef(xc, yc)[0, 1]) and r["gl"] == 12 - 3 - 1


def test_resultados_da_004_consistentes():
    tab = caminhos.RESULTADOS / "004" / "tabelas"
    if not (tab / "hipoteses.csv").exists():
        pytest.skip("rode python -m analise.mundial.rodar")
    h = le_csv(tab / "hipoteses.csv")
    assert list(h.hipotese) == ["H4.1", "H4.2", "H4.3", "H4.4"]
    assert (h.p_holm >= h.p - 1e-12).all()
    assert le_csv(tab / "conferencia_statsmodels.csv").diferenca_abs.max() < 1e-10
    ef = le_csv(tab / "efeitos_por_base.csv")
    assert len(ef) == 6 and "nhanes0506" not in set(ef.base) and ef.ep_usado.nunique() == 1


# ---- correções da verificação independente (2026-11-27)
def test_hartung_knapp_igual_statsmodels():
    m = M.dersimonian_laird(Y, V)
    hk = M.hartung_knapp(Y, V, m["tau2"])
    sm = combine_effects(Y, V, method_re="dl")
    assert np.isclose(hk["ep_hk"], sm.sd_eff_w_re_hksj, atol=1e-12)
    # IC manual: μ ± t(0,975; k − 1)·EP_HK
    tc = stats.t.ppf(0.975, len(Y) - 1)
    assert np.isclose(hk["ic_inf_hk"], m["mu"] - tc * hk["ep_hk"]) and np.isclose(hk["ic_sup_hk"], m["mu"] + tc * hk["ep_hk"])


def test_hartung_knapp_k1_sem_ic():
    assert np.isnan(M.hartung_knapp([0.1], [0.01], 0.0)["ic_inf_hk"])


def test_deff_kish():
    assert np.isclose(M.deff_kish(np.ones(10)), 1.0)
    assert np.isclose(M.deff_kish([1.0, 3.0]), 2 * 10 / 16)      # n·Σw²/(Σw)²


def test_tendencia_ordenada_inclinacao_conhecida():
    t = M.tendencia_ordenada([0.0, 0.1, 0.2], [0.05, 0.05, 0.05], [0, 1, 2])
    assert np.isclose(t["inclinacao"], 0.1) and t["p"] < 1


def test_meta_global_hk_bate_com_verificacao_independente():
    f = caminhos.RESULTADOS / "004" / "tabelas" / "meta_analise.csv"
    if not f.exists():
        pytest.skip("rode analise.mundial.rodar")
    g = le_csv(f).iloc[0]
    assert g.analise == "global (6 bases)"
    # HK recalculado a partir dos efeitos por base (o verificador conferiu a mesma fórmula com 7 bases)
    ef = le_csv(f.parent / "efeitos_por_base.csv")
    m = M.dersimonian_laird(ef.z, ef.ep ** 2)
    hk = M.hartung_knapp(ef.z, ef.ep ** 2, m["tau2"])
    assert np.isclose(g.rho_ic_inf_hk, np.tanh(hk["ic_inf_hk"])) and np.isclose(g.rho_ic_sup_hk, np.tanh(hk["ic_sup_hk"]))
    assert g.rho_ic_inf_hk < g.rho_ic_inf and g.rho_ic_sup_hk > g.rho_ic_sup   # HK é mais largo aqui


def test_sem_nhanes_e_brasil_x_resto_exploratorio():
    """Decisão do grupo (2026-11-27): NHANES fora; Brasil × resto do mundo só como exploratório, fora de Holm."""
    tab = caminhos.RESULTADOS / "004" / "tabelas"
    if not (tab / "meta_analise.csv").exists():
        pytest.skip("rode analise.mundial.rodar")
    meta = le_csv(tab / "meta_analise.csv")
    assert not meta.bases.str.contains("nhanes0506").any()
    resto = meta[meta.analise == "resto do mundo (4 bases)"].iloc[0]
    assert resto.papel == "exploratório" and set(resto.bases.split(", ")) == {"argentina", "japao", "xuzhou", "turquia"}
    outros = meta[meta.analise == "outros países, tempo total (Argentina)"].iloc[0]
    assert outros.k == 1
    assert "resto do mundo" not in " ".join(le_csv(tab / "hipoteses.csv").hipotese)
    ex = le_csv(tab / "exploratorio_referencia.csv")
    assert ex.analise.str.startswith("EXPLORATÓRIO: Brasil (PNS + Vigitel) × resto do mundo").sum() == 1
    sens = le_csv(tab / "sensibilidade.csv")
    assert not sens.analise.str.contains("NHANES").any()
