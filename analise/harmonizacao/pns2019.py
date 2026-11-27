"""T004 — Harmoniza a PNS 2019 (IBGE). Adultos selecionados (M001 = 1) com 18 anos ou mais."""
import re

import numpy as np
import pandas as pd

from analise.comum import caminhos
from analise.comum.faltantes import troca_por_nan, recodifica
from analise.comum.validacao import Log, faixa_etaria, salva_base
from analise.harmonizacao import recodes as R

BASE = "pns2019"
VARS = ["V0024", "UPA_PNS", "M001", "C006", "C008", "VDD004A", "V00291", "P04501", "P04502"] + \
       [f"N0{i}" for i in range(10, 19)]


def le_bruto() -> pd.DataFrame:
    d = caminhos.brutos() / "pns_2019" / "extraido"
    inp = (d / "Dicionario_e_input_20220530" / "input_PNS_2019.txt").read_text(encoding="latin-1")
    pos = {m[1]: (int(m[0]), int(m[2])) for m in re.findall(r"@(\d+)\s+(\w+)\s+\$?(\d+)\.", inp)}
    specs = [(pos[v][0] - 1, pos[v][0] - 1 + pos[v][1]) for v in VARS]
    df = pd.read_fwf(d / "PNS_2019_20220525" / "PNS_2019.txt", colspecs=specs, names=VARS, dtype=str)
    return df.apply(lambda s: pd.to_numeric(s.str.strip(), errors="coerce"))


def harmoniza() -> pd.DataFrame:
    log = Log(BASE)
    df = le_bruto(); log("linhas no arquivo (moradores)", len(df))
    df = df[df.M001 == 1]; log("morador selecionado com entrevista (M001 = 1)", len(df))
    df = df[df.C008 >= 18]; log("18 anos ou mais", len(df))
    df = troca_por_nan(df, BASE)
    o = pd.DataFrame({"base": BASE, "pais": "Brasil", "id": np.arange(len(df))})
    df = df.reset_index(drop=True)
    o["peso"], o["estrato"], o["upa"] = df.V00291, df.V0024, df.UPA_PNS
    o["idade"] = df.C008
    o["faixa_etaria"] = faixa_etaria(df.C008)
    o["sexo"] = recodifica(df.C006, {1: 0, 2: 1})                     # 1 = feminino
    o["escolaridade3"] = recodifica(df.VDD004A, R.PNS_ESC)
    o["tela_digital_cat"] = recodifica(df.P04502, R.PNS_CAT)
    o["tela_digital_ord"] = recodifica(df.P04502, R.PNS_ORD)
    o["tela_tv_cat"] = recodifica(df.P04501, R.PNS_CAT)
    o["tela_tv_ord"] = recodifica(df.P04501, R.PNS_ORD)
    for i, v in enumerate(R.PHQ_PNS, 1):
        o[f"phq{i}"] = df[v] - 1                                       # 1..4 -> 0..3
    o["depressao_phq9"] = o[[f"phq{i}" for i in range(1, 10)]].sum(axis=1, min_count=9)
    o["problema_sono_ord"] = df.N010 - 1
    o["problema_sono_freq"] = np.where(df.N010.isna(), np.nan, df.N010.isin([3, 4]).astype(float))
    return salva_base(o, BASE, log)


if __name__ == "__main__":
    harmoniza()
