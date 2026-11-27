"""Critérios de aceite da spec 002 conferidos sobre as saídas (pula se a análise ainda não rodou).

2026-11-27: EUA (NHANES 2005-06) fora do trabalho; H2.2–H2.4 retiradas.
"""
import numpy as np
import pandas as pd
import pytest
from sklearn.decomposition import PCA

from analise.comum import caminhos
from analise.comum import multivariada as mv
from analise.comum.estatistica import le_csv

TAB = caminhos.RESULTADOS / "002" / "tabelas"
FIG = caminhos.RESULTADOS / "002" / "figuras"


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
    p = caminhos.processado("vigitel2024")
    if not p.exists():
        pytest.skip("base não processada")
    X = pd.read_parquet(p)[["sintoma_1", "sintoma_2", "sintoma_3"]].dropna().to_numpy(float)
    r = mv.pca_svd(X)
    ref = PCA().fit(mv.padroniza(X))
    assert np.allclose(r["autovalores"], ref.explained_variance_, atol=1e-8)
    av = _tab("pca_autovalores.csv")
    g = av[av.conjunto == "insonia3_vigitel"].autovalor.to_numpy()
    assert np.allclose(g, r["autovalores"], atol=1e-8)


def test_hipoteses_todas_presentes_e_eua_retiradas():
    h = _tab("hipoteses.csv")
    for k in ["H2.1", "H2.2", "H2.3", "H2.4", "H2.5", "H2.6"]:
        assert h.hipotese.str.startswith(k).any(), k
    assert h.decisao.notna().all()
    ret = h[h.hipotese.isin(["H2.2", "H2.3", "H2.4"])]
    assert len(ret) == 3 and ret.decisao.str.startswith("retirada em 2026-11-27").all()
    assert (h[h.hipotese == "H2.1"].conjunto == "insonia3_vigitel").all()


def test_sem_nhanes_em_nenhuma_saida():
    ad = _tab("adequacao.csv")
    assert not ad.base.eq("nhanes0506").any()
    assert not any("nhanes" in f.name for f in TAB.glob("*.csv"))
    assert not any("nhanes" in f.name or "br_eua" in f.name for f in FIG.glob("*.png"))
    assert _tab("tucker.csv").empty                                        # sem comparação entre países


def test_n_completos_e_regra_do_plano():
    ad = _tab("adequacao.csv").set_index("conjunto")
    assert ad.loc["phq9_pns", "n"] <= 88531 and ad.loc["insonia3_vigitel", "n"] <= 27048
    assert (ad.k_decidido == ad.k_paralela).all()                           # regra do plano


def test_tabela_do_indice_do_vigitel():
    v = _tab("vigitel_indice.csv")
    assert v.variavel_vigitel.tolist() == ["r703", "r704", "r705"]
    assert v.carga_pc1.between(0.5, 1).all() and v.carga_af1_ml.between(0.5, 1).all()
    r = _tab("vigitel_indice_resumo.csv").iloc[0]
    ad = _tab("adequacao.csv").set_index("conjunto").loc["insonia3_vigitel"]
    assert abs(r.alfa - ad.alfa) < 1e-12 and abs(r.kmo - ad.kmo) < 1e-12 and r.fatores_retidos == 1
    assert r.autovalor_1 > r.p95_aleatorio_1 and r.autovalor_2 < r.p95_aleatorio_2      # análise paralela retém 1


def test_escores_exportados():
    for base, col in [("vigitel2024", "insonia3_af"), ("pns2019", "phq9_soma")]:
        f = caminhos.PROCESSADOS / f"escores_{base}.parquet"
        if not f.exists():
            pytest.skip("escores não exportados")
        e = pd.read_parquet(f)
        assert col in e.columns and e[col].notna().sum() > 1000
