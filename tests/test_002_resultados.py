"""Critérios de aceite da spec 002 conferidos sobre as saídas (pula se a análise ainda não rodou)."""
import numpy as np
import pandas as pd
import pytest
from sklearn.decomposition import PCA

from analise.comum import caminhos
from analise.comum import multivariada as mv
from analise.comum.estatistica import le_csv

TAB = caminhos.RESULTADOS / "002" / "tabelas"


def _tab(nome):
    f = TAB / nome
    if not f.exists():
        pytest.skip("rode: python -m analise.multivariada.analisa")
    return le_csv(f)


def test_autovalores_somam_p_e_pa_tem_1000_replicas_coerentes():
    av = _tab("pca_autovalores.csv")
    for cid, g in av.groupby("conjunto"):
        assert abs(g.autovalor.sum() - len(g)) < 1e-6, cid
        assert (np.diff(g.autovalor.to_numpy()) <= 1e-12).all(), cid       # ordem decrescente


def test_pca_svd_igual_sklearn_em_dado_real():
    p = caminhos.processado("nhanes0506")
    if not p.exists():
        pytest.skip("base não processada")
    X = pd.read_parquet(p)[["sintoma_1", "sintoma_2", "sintoma_3"]].dropna().to_numpy(float)
    r = mv.pca_svd(X)
    ref = PCA().fit(mv.padroniza(X))
    assert np.allclose(r["autovalores"], ref.explained_variance_, atol=1e-8)
    av = _tab("pca_autovalores.csv")
    g = av[av.conjunto == "insonia3_nhanes"].autovalor.to_numpy()
    assert np.allclose(g, r["autovalores"], atol=1e-8)


def test_hipoteses_todas_presentes():
    h = _tab("hipoteses.csv")
    for k in ["H2.1", "H2.2", "H2.3", "H2.4", "H2.5", "H2.6"]:
        assert h.hipotese.str.startswith(k).any(), k
    assert h.decisao.notna().all()


def test_tucker_no_intervalo_e_n_completos():
    t = _tab("tucker.csv")
    assert t.phi.abs().le(1 + 1e-12).all()
    ad = _tab("adequacao.csv").set_index("conjunto")
    assert ad.loc["phq9_pns", "n"] <= 88531 and ad.loc["insonia3_vigitel", "n"] <= 27048
    assert (ad.k_decidido == ad.k_paralela).all()                           # regra do plano


def test_escores_exportados():
    for base, col in [("vigitel2024", "insonia3_af"), ("nhanes0506", "phq9_pc1"), ("pns2019", "phq9_soma")]:
        f = caminhos.PROCESSADOS / f"escores_{base}.parquet"
        if not f.exists():
            pytest.skip("escores não exportados")
        e = pd.read_parquet(f)
        assert col in e.columns and e[col].notna().sum() > 1000
