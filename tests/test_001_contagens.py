"""Contagens da spec 001 (critério de aceite): os n conferem com o inventário."""
import json

import pandas as pd
import pytest

from analise.comum import caminhos

ESPERADO = {
    "pns2019": {"morador selecionado com entrevista (M001 = 1)": 90846, "18 anos ou mais": 88531},
    "vigitel2024": {"edição 2024": 27048},
    "xuzhou": {"linhas no arquivo": 2317},
    "argentina": {"completos do artigo (excluFINAL = 0)": 864},
    "turquia": {"linhas no arquivo": 1216},
    "japao": {"linhas no arquivo": 381},
}


@pytest.mark.parametrize("base", list(ESPERADO))
def test_contagens(base):
    f = caminhos.LOGS / f"{base}.json"
    if not f.exists():
        pytest.skip(f"{base} sem log (rode analise.harmonizacao)")
    log = json.loads(f.read_text(encoding="utf-8"))
    for etapa, n in ESPERADO[base].items():
        assert log[etapa] == n, f"{base} / {etapa}: {log[etapa]} != {n}"


FINAL = {"pns2019": 88531, "vigitel2024": 27048, "xuzhou": 2317,
         "argentina": 864, "turquia": 1216, "japao": 381}


@pytest.mark.parametrize("base", list(FINAL))
def test_contagem_no_proprio_parquet(base):
    """Confere o n nos dados processados, não só no log."""
    p = caminhos.processado(base)
    if not p.exists():
        pytest.skip(f"{base} não processada")
    assert len(pd.read_parquet(p, columns=["base"])) == FINAL[base]
