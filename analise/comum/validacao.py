"""Validação das bases processadas: faixa de valores de cada variável do contrato (spec 001).

Um código especial (7, 9, 77, 99, 777, 888, 999) que sobreviva como número cai fora da faixa
válida da variável e faz a validação falhar.
"""
import json
import math

import numpy as np
import pandas as pd

from analise.comum import caminhos

INF = math.inf
FAIXAS = {
    "sintoma_1": (0, 4), "sintoma_2": (0, 4), "sintoma_3": (0, 4),
    "insonia_idx": (0, 12),
    "dif_adormecer_freq": (0, 1), "problema_sono_freq": (0, 1), "problema_sono_ord": (0, 3),
    "tela_digital_cat": (0, 2), "tela_tv_cat": (0, 2),
    "tela_digital_ord": (0, 7), "tela_tv_ord": (0, 7),
    "sono_horas": (0.5, 24), "latencia_min": (0, 240),
    "tela_presono_h": (0, 24), "tela_total_h": (0, 24),
    "idade": (10, 120), "sexo": (0, 1), "escolaridade3": (0, 2),
    "depressao_phq9": (0, 27), "depressao_diag": (0, 1),
    **{f"phq{i}": (0, 3) for i in range(1, 10)},
    "peso": (0, INF),
}


def valida(df: pd.DataFrame, extra: dict | None = None) -> None:
    """Levanta AssertionError listando toda variável com valor fora da faixa."""
    faixas = {**FAIXAS, **(extra or {})}
    erros = []
    for var, (lo, hi) in faixas.items():
        if var not in df.columns:
            continue
        v = pd.to_numeric(df[var], errors="coerce").dropna()
        fora = v[(v < lo) | (v > hi)]
        if len(fora):
            erros.append(f"{var}: {len(fora)} valores fora de [{lo}, {hi}] (ex.: {sorted(fora.unique())[:5]})")
        if var not in ("peso",) and np.isinf(v).any():
            erros.append(f"{var}: valor infinito")
    if erros:
        raise AssertionError("Validação falhou:\n" + "\n".join(erros))


class Log:
    """Registra o n depois de cada filtro e salva em logs/<base>.log e .json."""

    def __init__(self, base: str):
        self.base, self.etapas = base, []

    def __call__(self, etapa: str, n: int):
        self.etapas.append((etapa, int(n)))
        print(f"[{self.base}] {etapa}: {n:,}".replace(",", "."))

    def salva(self):
        caminhos.LOGS.mkdir(parents=True, exist_ok=True)
        txt = "\n".join(f"{e}: {n}" for e, n in self.etapas)
        (caminhos.LOGS / f"{self.base}.log").write_text(txt + "\n", encoding="utf-8")
        (caminhos.LOGS / f"{self.base}.json").write_text(
            json.dumps(dict(self.etapas), ensure_ascii=False, indent=1), encoding="utf-8")


def faixa_etaria(idade: pd.Series) -> pd.Series:
    return pd.cut(idade, [17, 29, 44, 59, 200], labels=["18-29", "30-44", "45-59", "60+"]).astype("string")


def salva_base(df: pd.DataFrame, base: str, log: Log, extra: dict | None = None) -> pd.DataFrame:
    valida(df, extra)
    caminhos.PROCESSADOS.mkdir(parents=True, exist_ok=True)
    df.to_parquet(caminhos.processado(base), index=False)
    log("salvo (após validação)", len(df))
    log.salva()
    return df
