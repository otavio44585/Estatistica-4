"""T003 — Nenhum código especial sobrevive como número (spec 001, critério de aceite)."""
import numpy as np
import pandas as pd
import pytest

from analise.comum import caminhos
from analise.comum.faltantes import troca_por_nan, recodifica
from analise.comum.validacao import valida
from analise.harmonizacao import recodes as R

BASES = ["pns2019", "vigitel2024", "xuzhou", "argentina", "turquia", "japao"]


def test_validacao_falha_com_codigo_especial():
    sujo = pd.DataFrame({"sintoma_1": [0, 2, 9], "idade": [30, 40, 50]})   # 9 = ignorado na PNS
    with pytest.raises(AssertionError, match="sintoma_1"):
        valida(sujo)


def test_validacao_passa_com_dado_limpo():
    valida(pd.DataFrame({"sintoma_1": [0, 2, np.nan], "insonia_idx": [0, 12, 5], "tela_digital_cat": [0, 1, 2]}))


def test_troca_por_nan_pns_e_vigitel():
    pns = troca_por_nan(pd.DataFrame({"N010": [1, 4, 9], "P04502": [2, 6, 9]}), "pns2019")
    assert pns.N010.isna().tolist() == [False, False, True] and pns.P04502.isna().tolist() == [False, False, True]
    vig = troca_por_nan(pd.DataFrame({"q59b": [1, 2, 777, 888], "r703": [1, 5, 777, 888]}), "vigitel2024")
    assert vig.q59b.isna().tolist() == [False, False, True, True] and vig.r703.isna().tolist() == [False, False, True, True]


def test_recodificacao_exposicao_bate_com_o_plano():
    # plano 001: PNS P04502 6,1 -> 0; 2,3 -> 1; 4,5 -> 2 ; Vigitel q59c (0 = não usa) 0,1 -> 0; 2,3 -> 1; 4-7 -> 2
    assert recodifica(pd.Series([6, 1, 2, 3, 4, 5, 9]), R.PNS_CAT).tolist()[:6] == [0, 0, 1, 1, 2, 2]
    assert np.isnan(recodifica(pd.Series([9]), R.PNS_CAT).iloc[0])
    assert recodifica(pd.Series([0, 1, 2, 3, 4, 5, 6, 7]), R.VIG_CAT).tolist() == [0, 0, 1, 1, 2, 2, 2, 2]


def test_ordem_phq9_pns():
    # o item de sono do PHQ-9 (3º na ordem do instrumento) é a pergunta N010 da PNS
    assert R.PHQ_PNS[2] == "N010"


@pytest.mark.parametrize("base", BASES)
def test_bases_processadas_validas(base):
    p = caminhos.processado(base)
    if not p.exists():
        pytest.skip(f"{base} ainda não processada (rode analise.harmonizacao)")
    df = pd.read_parquet(p)
    extra = {"escore_sono_escala": (0, 32), "idade": (10, 120)}
    valida(df, extra)
