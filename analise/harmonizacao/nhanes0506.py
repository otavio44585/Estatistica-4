"""T006 — Harmoniza o NHANES 2005-06 (CDC/NCHS). Questionário de sono + atividade + demografia + PHQ-9."""
import numpy as np
import pandas as pd
import pyreadstat

from analise.comum import caminhos
from analise.comum.faltantes import troca_por_nan, recodifica
from analise.comum.validacao import Log, faixa_etaria, salva_base
from analise.harmonizacao import recodes as R

BASE = "nhanes0506"
SLQ = [f"SLQ{i:03d}" for i in range(80, 150, 10)]


def le_bruto() -> pd.DataFrame:
    d = caminhos.brutos() / "nhanes_2005_2006"
    le = lambda f: pyreadstat.read_xport(str(d / f))[0]
    sl = le("SLQ_D.xpt")[["SEQN", "SLD010H", "SLD020M"] + SLQ]
    pa = le("PAQ_D.xpt")[["SEQN", "PAD590", "PAD600"]]
    de = le("DEMO_D.xpt")[["SEQN", "RIDAGEYR", "RIAGENDR", "DMDEDUC2", "DMDEDUC3", "WTINT2YR", "SDMVSTRA", "SDMVPSU"]]
    dp = le("DPQ_D.xpt")[["SEQN"] + R.PHQ_NH]
    return sl.merge(pa, on="SEQN", how="left").merge(de, on="SEQN", how="left").merge(dp, on="SEQN", how="left")


def harmoniza() -> pd.DataFrame:
    log = Log(BASE)
    df = le_bruto(); log("participantes do questionário de sono (SLQ_D)", len(df))
    df = df[df.RIDAGEYR >= 18].reset_index(drop=True); log("18 anos ou mais", len(df))
    df = troca_por_nan(df, BASE)
    o = pd.DataFrame({"base": BASE, "pais": "EUA", "id": df.SEQN.astype(int)})
    o["peso"], o["estrato"], o["upa"] = df.WTINT2YR, df.SDMVSTRA, df.SDMVPSU
    o["idade"] = df.RIDAGEYR
    o["faixa_etaria"] = faixa_etaria(df.RIDAGEYR)
    o["sexo"] = recodifica(df.RIAGENDR, {1: 0, 2: 1})
    esc = np.where(df.RIDAGEYR >= 20, recodifica(df.DMDEDUC2, R.NH_ESC2), recodifica(df.DMDEDUC3, R.NH_ESC3))
    o["escolaridade3"] = esc
    for i, v in enumerate(["SLQ080", "SLQ090", "SLQ100"], 1):
        o[f"sintoma_{i}"] = df[v]                                      # 0 never .. 4 almost always
    o["insonia_idx"] = o[["sintoma_1", "sintoma_2", "sintoma_3"]].sum(axis=1, min_count=3)
    o["dif_adormecer_freq"] = np.where(df.SLQ080.isna(), np.nan, df.SLQ080.isin([3, 4]).astype(float))
    for v in SLQ:
        o[v.lower()] = df[v]                                           # 7 sintomas de sono (spec 002)
    o["sono_horas"] = df.SLD010H
    o["latencia_min"] = df.SLD020M
    o["latencia_censurada"] = (df.SLD020M == 60).astype(float).where(df.SLD020M.notna())
    o["tela_digital_cat"] = recodifica(df.PAD600, R.NH_CAT)
    o["tela_digital_ord"] = recodifica(df.PAD600, R.NH_ORD)
    o["tela_tv_cat"] = recodifica(df.PAD590, R.NH_CAT)
    o["tela_tv_ord"] = recodifica(df.PAD590, R.NH_ORD)
    for i, v in enumerate(R.PHQ_NH, 1):
        o[f"phq{i}"] = df[v]
    o["depressao_phq9"] = o[[f"phq{i}" for i in range(1, 10)]].sum(axis=1, min_count=9)
    return salva_base(o, BASE, log)


if __name__ == "__main__":
    harmoniza()
