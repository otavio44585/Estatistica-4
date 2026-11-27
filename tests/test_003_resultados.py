"""Confere a tabela de hipóteses da spec 003 (cobertura das hipóteses e Holm por família)."""
import numpy as np
import pytest

from analise.comum import caminhos
from analise.comum.estatistica import le_csv, holm

ARQ = caminhos.RESULTADOS / "003" / "tabelas" / "hipoteses.csv"


@pytest.fixture(scope="module")
def H():
    if not ARQ.exists():
        pytest.skip("rode python -m analise.brasil_eua.executa")
    return le_csv(ARQ)


def test_todas_as_hipoteses_da_spec_estao_na_tabela(H):
    assert set(H.hipotese) == {"H3.1", "H3.2", "H3.4", "H3.7", "H3.8", "H3.9"}
    assert not ({"H3.3", "H3.6"} & set(H.hipotese))   # retiradas em 2026-11-27 (EUA fora do trabalho)
    assert "nhanes0506" not in set(H.base)
    assert "H3.5" not in set(H.hipotese)        # transferida para a spec 005


def test_holm_recalculado_por_familia(H):
    for _, g in H.groupby("familia"):
        assert np.allclose(g.p_holm.values, holm(g.p.values))
        assert (g.p_holm >= g.p - 1e-12).all()


def test_decisao_coerente_com_p_holm(H):
    assert ((H.p_holm < 0.05) == (H.decisao == "rejeita H0")).all()


def test_ic_da_rp_contem_a_estimativa(H):
    h = H[H.estimativa.notna()]
    assert ((h.ic_inf <= h.estimativa) & (h.estimativa <= h.ic_sup)).all()


def test_sem_nhanes_nas_tabelas_da_003():
    for nome in ["rp_bruta_ajustada", "prevalencias", "rp_por_faixa_etaria", "sensibilidade", "comparacao_variancia"]:
        t = le_csv(caminhos.RESULTADOS / "003" / "tabelas" / f"{nome}.csv")
        assert "nhanes0506" not in set(t.base), nome
    c = le_csv(caminhos.RESULTADOS / "003" / "tabelas" / "comparacoes_entre_bases.csv")
    assert set(c.hipotese) == {"H3.9"}


def test_familias_de_holm_sem_eua(H):
    f2 = H[H.familia == "2"]
    assert len(f2) == 5 and set(f2.hipotese) == {"H3.7", "H3.8", "H3.9"}
