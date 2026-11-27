"""T005 — Harmoniza o Vigitel 2024 (Ministério da Saúde). Lido direto do zip, em blocos."""
import zipfile

import numpy as np
import pandas as pd

from analise.comum import caminhos
from analise.comum.faltantes import troca_por_nan, recodifica
from analise.comum.validacao import Log, faixa_etaria, salva_base
from analise.harmonizacao import recodes as R

BASE = "vigitel2024"
COLS = ["ano", "cidade", "q6", "q7", "fesc", "pesorake2025", "r701_hh", "r701_mm",
        "r703", "r704", "r705", "q59a", "q59b", "q59c", "r205"]


def le_bruto() -> pd.DataFrame:
    z = zipfile.ZipFile(caminhos.brutos() / "vigitel_2006_2024" / "vigitel-2006-2024-peso-rake-csv.zip")
    blocos = pd.read_csv(z.open(z.namelist()[0]), usecols=COLS, encoding="latin-1",
                         chunksize=200_000, low_memory=False)
    df = pd.concat(b[pd.to_numeric(b.ano, errors="coerce") == 2024] for b in blocos)
    return df.apply(pd.to_numeric, errors="coerce").reset_index(drop=True)


def harmoniza() -> pd.DataFrame:
    log = Log(BASE)
    df = le_bruto(); log("edição 2024", len(df))
    df = df[df.q6 >= 18].reset_index(drop=True); log("18 anos ou mais", len(df))
    df = troca_por_nan(df, BASE)
    o = pd.DataFrame({"base": BASE, "pais": "Brasil", "id": np.arange(len(df))})
    o["peso"], o["cidade"] = df.pesorake2025, df.cidade
    o["idade"] = df.q6
    o["faixa_etaria"] = faixa_etaria(df.q6)
    o["sexo"] = recodifica(df.q7, {1: 0, 2: 1})
    o["escolaridade3"] = recodifica(df.fesc, R.VIG_ESC)
    for i, v in enumerate(["r703", "r704", "r705"], 1):
        o[f"sintoma_{i}"] = df[v] - 1                                  # 1 nunca .. 5 sempre -> 0..4
    o["insonia_idx"] = o[["sintoma_1", "sintoma_2", "sintoma_3"]].sum(axis=1, min_count=3)
    o["dif_adormecer_freq"] = np.where(df.r703.isna(), np.nan, df.r703.isin([4, 5]).astype(float))
    o["sono_horas"] = df.r701_hh + df.r701_mm.fillna(0) / 60
    o.loc[o.sono_horas < 0.5, "sono_horas"] = np.nan                   # 0 h = resposta inválida
    # computador/tablet/celular: q59b = 2 (não usa) vira 0; q59c pulada nesse caso
    dig = np.where(df.q59b == 2, 0, np.where(df.q59b == 1, df.q59c, np.nan))
    dig = pd.Series(dig)
    o["tela_digital_cat"] = recodifica(dig, R.VIG_CAT)
    o["tela_digital_ord"] = recodifica(dig, R.VIG_ORD)
    tv = df.q59a.where(df.q59a != 8, 0)                                # 8 = não assiste
    o["tela_tv_cat"] = recodifica(tv, R.VIG_CAT)
    o["tela_tv_ord"] = recodifica(tv, R.VIG_ORD)
    o["depressao_diag"] = recodifica(df.r205, {1: 1, 2: 0})
    return salva_base(o, BASE, log)


if __name__ == "__main__":
    harmoniza()
