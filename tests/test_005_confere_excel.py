"""T082 — Teste de referência: o script reproduz o SUMMARY OUTPUT do Excel no exercício 2 da aula.

A planilha da aula não é copiada para o repositório (material da disciplina). O teste lê o arquivo pela
variável de ambiente STAT4_AULA; sem ela, procura '../Estatistica 4 - regressao linear .xlsx' ao lado do
repositório; sem o arquivo, o teste é pulado.
"""
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from analise.comum import caminhos
from analise.regressao.confere_excel import iguais
from analise.regressao.ols import mqo

AULA = Path(os.environ.get("STAT4_AULA", caminhos.RAIZ.parent / "Estatistica 4 - regressao linear .xlsx"))


@pytest.fixture(scope="module")
def aula():
    if not AULA.exists():
        pytest.skip("planilha da aula ausente (defina STAT4_AULA)")
    openpyxl = pytest.importorskip("openpyxl")
    ws = openpyxl.load_workbook(AULA, data_only=True)["exerc2"]
    dados = pd.DataFrame([[ws.cell(r, c).value for c in range(1, 5)] for r in range(2, 22)],
                         columns=["salario", "sexo", "qualificado", "tempo"]).astype(float)
    excel = {k: ws[c].value for k, c in [("r2", "G15"), ("r2_aj", "G16"), ("ep", "G17"), ("n", "G18"),
                                         ("gl_reg", "G22"), ("sq_reg", "H22"), ("f", "J22"), ("p_f", "K22"),
                                         ("gl_res", "G23"), ("sq_res", "H23")]}
    excel["coef"] = [[ws.cell(r, c).value for c in range(7, 13)] for r in range(27, 31)]
    return dados, excel


def test_reproduz_summary_output_da_aula(aula):
    dados, ex = aula
    a = mqo(dados.salario, dados[["sexo", "qualificado", "tempo"]])
    for nome, valor in [("r2", a.r2), ("r2_aj", a.r2_aj), ("ep", a.erro_padrao), ("n", a.n), ("gl_reg", a.k),
                        ("sq_reg", a.sq_reg), ("f", a.f), ("p_f", a.p_f), ("gl_res", a.gl_res), ("sq_res", a.sq_res)]:
        assert abs(valor - ex[nome]) <= 1e-9 * max(abs(ex[nome]), 1e-300), nome
    for j, (b, ep, t, p, lo, hi) in enumerate(ex["coef"]):
        for meu, deles in zip((a.b[j], a.ep[j], a.t[j], a.p[j], a.ic_inf[j], a.ic_sup[j]), (b, ep, t, p, lo, hi)):
            assert abs(meu - deles) <= 1e-9 * abs(deles)


def test_conferencia_detecta_p_alterado():
    assert iguais(0.0123456789, 0.0123456789)[0]
    assert not iguais(0.0123456789, 0.0123456789 * (1 + 1e-6))[0]   # p alterado de propósito
    assert iguais(1e-300, 0.0)[0]                                     # os dois < 1e-15 contam como iguais


def test_conferencia_salva_sem_divergencia():
    f = caminhos.RESULTADOS / "005" / "conferencia.csv"
    if not f.exists():
        pytest.skip("rode analise.regressao.confere_excel")
    from analise.comum.estatistica import le_csv
    c = le_csv(f)
    av = c[c.ok.astype(str) != "informativo"]
    assert len(av) > 500 and av.ok.astype(str).eq("True").all()
    assert np.nanmax(av.dif_rel_A_C) < 1e-8
    # colunas booleanas usadas pelo relatório para contar certo
    assert c.dentro_tolerancia.astype(str).eq("True").sum() == len(av)
    assert c.excecao_documentada.astype(str).eq("True").sum() == (c.ok.astype(str) == "informativo").sum()


def test_conferencia_funciona_em_clone_limpo(monkeypatch):
    """Sem as pastas de trabalho (fora do git), o caminho A vem de resultados/005/excel_saidas/."""
    import analise.regressao.confere_excel as ce
    if not (ce.OUT / "excel_saidas" / "japao__reg_completo.csv").exists() or not caminhos.processado("japao").exists():
        pytest.skip("saídas exportadas ou dados processados ausentes")
    monkeypatch.setattr(ce, "PASTA", caminhos.RAIZ / "pasta_que_nao_existe")
    monkeypatch.setattr(ce, "EXPORTA", False)
    cf = ce.Conferencia()
    ce.confere_base(cf, "japao")
    assert len(cf.linhas) > 50 and all(l["ok"] is True for l in cf.linhas)
