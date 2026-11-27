"""T003 — Nenhum código especial sobrevive como número (spec 001, critério de aceite)."""
import numpy as np
import pandas as pd
import pytest

from analise.comum import caminhos
from analise.comum.faltantes import troca_por_nan, recodifica
from analise.comum.validacao import valida
from analise.harmonizacao import recodes as R

BASES = ["pns2019", "vigitel2024", "nhanes0506", "xuzhou", "argentina", "turquia", "japao"]


def test_validacao_falha_com_codigo_especial():
    sujo = pd.DataFrame({"sintoma_1": [0, 2, 9], "idade": [30, 40, 50]})   # 9 = não sabe no NHANES
    with pytest.raises(AssertionError, match="sintoma_1"):
        valida(sujo)


def test_validacao_passa_com_dado_limpo():
    valida(pd.DataFrame({"sintoma_1": [0, 2, np.nan], "insonia_idx": [0, 12, 5], "tela_digital_cat": [0, 1, 2]}))


def test_troca_por_nan_nhanes():
    df = pd.DataFrame({"SLQ080": [0, 4, 7, 9], "SLD020M": [15, 60, 77, 99]})
    out = troca_por_nan(df, "nhanes0506")
    assert out.SLQ080.isna().tolist() == [False, False, True, True]
    assert out.SLD020M.isna().tolist() == [False, False, True, True]


def test_recodificacao_exposicao_bate_com_o_plano():
    # plano 001: PNS P04502 6,1 -> 0; 2,3 -> 1; 4,5 -> 2 ; NHANES PAD600 6,0 -> 0; 1,2 -> 1; 3-5 -> 2
    assert recodifica(pd.Series([6, 1, 2, 3, 4, 5, 9]), R.PNS_CAT).tolist()[:6] == [0, 0, 1, 1, 2, 2]
    assert np.isnan(recodifica(pd.Series([9]), R.PNS_CAT).iloc[0])
    assert recodifica(pd.Series([6, 0, 1, 2, 3, 4, 5]), R.NH_CAT).tolist() == [0, 0, 1, 1, 2, 2, 2]
    assert recodifica(pd.Series([0, 1, 2, 3, 4, 5, 6, 7]), R.VIG_CAT).tolist() == [0, 0, 1, 1, 2, 2, 2, 2]


def test_ordem_phq9_pns():
    # o item de sono do PHQ-9 (3º) é a pergunta N010 da PNS e a DPQ030 do NHANES
    assert R.PHQ_PNS[2] == "N010" and R.PHQ_NH[2] == "DPQ030"


@pytest.mark.parametrize("base", BASES)
def test_bases_processadas_validas(base):
    p = caminhos.processado(base)
    if not p.exists():
        pytest.skip(f"{base} ainda não processada (rode analise.harmonizacao)")
    df = pd.read_parquet(p)
    extra = {"escore_sono_escala": (0, 32), "idade": (10, 120)}
    valida(df, extra)
