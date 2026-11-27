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
    assert set(H.hipotese) == {"H3.1", "H3.2", "H3.3", "H3.4", "H3.6", "H3.7", "H3.8", "H3.9"}
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
