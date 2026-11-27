"""Funções estatísticas compartilhadas pelas specs 002–005 (princípio 7)."""
import numpy as np
import pandas as pd

ALFA = 0.05


def holm(p) -> np.ndarray:
    """p ajustado por Holm (step-down): ordena crescente, p(i)·(m − i + 1), máximo acumulado, teto 1."""
    p = np.asarray(p, dtype=float)
    m = len(p)
    ordem = np.argsort(p)
    aj = np.empty(m)
    acum = 0.0
    for k, i in enumerate(ordem):
        acum = max(acum, (m - k) * p[i])
        aj[i] = min(1.0, acum)
    return aj


def formata_p(p: float) -> str:
    """Regra do relatório: 3 casas; abaixo de 0,001 escreve '< 0,001'. Nunca '0,000'."""
    if p is None or (isinstance(p, float) and np.isnan(p)):
        return "—"
    return "< 0,001" if p < 0.001 else f"{p:.3f}".replace(".", ",")


def decisao(p_ajustado: float, alfa: float = ALFA) -> str:
    return "rejeita H0" if p_ajustado < alfa else "não rejeita H0"


def num(x: float, casas: int = 2) -> str:
    """Número no padrão brasileiro (vírgula decimal)."""
    return f"{x:.{casas}f}".replace(".", ",")


def salva_csv(df: pd.DataFrame, caminho) -> None:
    """Padrão do projeto: separador ';', decimal ',', UTF-8 com BOM (abre direto no Excel em português)."""
    df.to_csv(caminho, sep=";", decimal=",", index=False, encoding="utf-8-sig")


def le_csv(caminho) -> pd.DataFrame:
    return pd.read_csv(caminho, sep=";", decimal=",", encoding="utf-8-sig")
