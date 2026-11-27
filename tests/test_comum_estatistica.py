import numpy as np

from analise.comum.estatistica import holm, formata_p


def test_holm_exemplo_conhecido():
    # m = 4: p ordenados 0,01 0,02 0,03 0,04 -> 0,04 0,06 0,06 0,06
    aj = holm([0.04, 0.01, 0.03, 0.02])
    assert np.allclose(aj, [0.06, 0.04, 0.06, 0.06])


def test_holm_nunca_menor_que_p_bruto_e_teto_1():
    p = np.array([0.5, 0.001, 0.2, 0.9])
    aj = holm(p)
    assert (aj >= p).all() and (aj <= 1).all()


def test_formato_p():
    assert formata_p(5.07e-18) == "< 0,001"
    assert formata_p(0.0234) == "0,023"
    assert formata_p(0.001) == "0,001"
