"""Códigos especiais por base (princípio 5): recusa, não sabe, ignorado, pulo.

Cada base mapeia variável original -> códigos que viram NaN. Os códigos saem dos dicionários
oficiais (PNS 2019: dicionario_PNS_microdados_2019.xls; Vigitel: dicionario-vigitel-2006-2024.xlsx;
NHANES: páginas .htm de cada arquivo; repositórios: inventário em docs/inventario-dados.md).
"""
import numpy as np
import pandas as pd

_PHQ_PNS = {f"N0{i}": [9] for i in range(10, 19)}
_SLQ = {f"SLQ{i:03d}": [7, 9] for i in range(80, 150, 10)}
_DPQ = {f"DPQ0{i}0": [7, 9] for i in range(1, 10)}

CODIGOS = {
    "pns2019": {"C006": [9], "VDD004A": [9], "P04501": [9], "P04502": [9], **_PHQ_PNS},
    "vigitel2024": {v: [777, 888] for v in ["q59a", "q59b", "q59c", "r205", "fesc", "r703", "r704", "r705", "r701_hh", "r701_mm"]},
    "nhanes0506": {**_SLQ, **_DPQ, "SLD010H": [77, 99], "SLD020M": [77, 99], "PAD590": [77, 99],
                   "PAD600": [77, 99], "DMDEDUC2": [7, 9], "DMDEDUC3": [77, 99]},
    "argentina": {"latencia": [999]},
    "xuzhou": {},
    "turquia": {},
    "japao": {},
}


def troca_por_nan(df: pd.DataFrame, base: str) -> pd.DataFrame:
    """Devolve cópia com os códigos especiais da base trocados por NaN."""
    df = df.copy()
    for var, cods in CODIGOS[base].items():
        if var in df.columns:
            df[var] = df[var].where(~df[var].isin(cods), np.nan)
    return df


def recodifica(serie: pd.Series, mapa: dict) -> pd.Series:
    """Mapeia códigos para novos valores; o que não está no mapa vira NaN."""
    return serie.map(mapa).astype("float")
