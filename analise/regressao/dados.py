"""Matrizes dos modelos da spec 005: Y na 1ª coluna, depois os regressores da tela, depois as covariáveis.

A ordem Y | tela | covariáveis deixa os três modelos com X contíguo, como a Regressão do Excel exige:
  completo     = tela + covariáveis   (colunas B até a última)
  simples      = só tela              (bruta, princípio 11)
  covariaveis  = só covariáveis       (modelo restrito do F parcial)
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd

from analise.comum import caminhos


@dataclass(frozen=True)
class Modelo:
    hipotese: str
    base: str
    rotulo: str
    y: str
    y_rotulo: str
    tela: tuple          # colunas de tela na matriz
    tela_teste: str      # coeficiente testado na família R1
    peso: bool           # inquérito com peso amostral


MODELOS = [
    Modelo("H5.1", "vigitel2024", "Vigitel 2024", "insonia_idx", "índice de insônia (0-12)",
           ("tela_1a3h", "tela_3h_mais"), "tela_3h_mais", True),
    Modelo("H5.2", "nhanes0506", "NHANES 2005-06", "insonia_idx", "índice de insônia (0-12)",
           ("tela_1a3h", "tela_3h_mais"), "tela_3h_mais", True),
    Modelo("H5.3", "xuzhou", "Xuzhou", "psqi", "PSQI (0-21)", ("sas_sv",), "sas_sv", False),
    Modelo("H5.4", "argentina", "Argentina", "latencia_min", "latência (min)", ("tela_presono_h",), "tela_presono_h", False),
    Modelo("H5.5", "turquia", "Turquia", "latencia_min", "latência (min)", ("doomscrolling",), "doomscrolling", False),
    Modelo("H5.6", "japao", "Japão", "ais", "AIS (8-32)", ("celular_presono_h",), "celular_presono_h", False),
]
POR_BASE = {m.base: m for m in MODELOS}


def _dummies(s: pd.Series, prefixo: str, ref="moda") -> pd.DataFrame:
    """k − 1 dummies; referência = categoria mais frequente (evita VIF alto quando a categoria de
    referência é pequena; o coeficiente da tela não depende da referência)."""
    if ref == "moda":
        ref = s.dropna().value_counts().sort_index().idxmax()
    cats = sorted(c for c in s.dropna().unique() if c != ref)
    return pd.DataFrame({f"{prefixo}_{int(c)}": (s == c).astype(float).where(s.notna()) for c in cats})


def matriz(base: str, sens_serie: bool = False, y_col: str | None = None) -> tuple[pd.DataFrame, dict]:
    """Devolve (dados do modelo, informações): só casos completos, tudo numérico.

    informações: n de partida, n final, colunas de tela, colunas de covariáveis, peso/estrato/upa alinhados.
    sens_serie: só Argentina — troca a idade pela série escolar (sensibilidade da spec).
    y_col: troca o desfecho por outra coluna da base processada (desfechos secundários, exploratórios).
    """
    m = POR_BASE[base]
    d = pd.read_parquet(caminhos.processado(base))
    n0 = len(d)
    cov = pd.DataFrame(index=d.index)
    tela = pd.DataFrame(index=d.index)
    if base in ("vigitel2024", "nhanes0506"):
        y = d.insonia_idx
        tela["tela_1a3h"] = (d.tela_digital_cat == 1).astype(float).where(d.tela_digital_cat.notna())
        tela["tela_3h_mais"] = (d.tela_digital_cat == 2).astype(float).where(d.tela_digital_cat.notna())
        cov["idade"] = d.idade
        cov["feminino"] = d.sexo
        cov["esc_medio"] = (d.escolaridade3 == 1).astype(float).where(d.escolaridade3.notna())
        cov["esc_superior"] = (d.escolaridade3 == 2).astype(float).where(d.escolaridade3.notna())
    elif base == "xuzhou":
        y = d.escore_sono_escala
        tela["sas_sv"] = d.uso_problematico
        cov["sexo_cod2"] = d.sexo
        cov = cov.join(_dummies(d.serie, "serie")).join(_dummies(d.renda, "renda"))
    elif base == "argentina":
        y = d.latencia_min
        tela["tela_presono_h"] = d.tela_presono_h
        if sens_serie:
            cov = cov.join(_dummies(d.serie, "serie"))
        else:
            cov["idade"] = d.idade
        cov["feminino"] = d.sexo
        cov = cov.join(_dummies(d.escolaridade_pais, "esc_pais"))
    elif base == "turquia":
        y = d.latencia_min
        tela["doomscrolling"] = d.uso_problematico
        cov["idade"] = d.idade
    elif base == "japao":
        y = d.escore_sono_escala
        tela["celular_presono_h"] = d.tela_presono_h
        cov["idade"] = d.idade
        cov["sexo_cod2"] = d.sexo
    else:
        raise KeyError(base)
    if y_col is not None:
        y = d[y_col]
    df = pd.concat([y.rename(m.y if y_col is None else y_col), tela, cov], axis=1)
    desenho = pd.DataFrame(index=d.index)
    if "peso" in d:
        desenho["peso"] = d.peso
    for c in ("estrato", "upa"):
        if c in d:
            desenho[c] = d[c]
    ok = df.notna().all(axis=1) & desenho.notna().all(axis=1)
    info = dict(n_partida=n0, n_final=int(ok.sum()), tela=list(tela.columns), cov=list(cov.columns),
                desenho=desenho[ok].reset_index(drop=True), tela_cat=None)
    if base in ("vigitel2024", "nhanes0506"):
        info["tela_cat"] = d.tela_digital_cat[ok].reset_index(drop=True)
    return df[ok].reset_index(drop=True), info


def empilhada() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Base Vigitel + NHANES para H5.11: + país (EUA = 1) + país × tela. Pesos reescalados para somar o n de cada base."""
    partes, desenhos = [], []
    for base, eua in (("vigitel2024", 0.0), ("nhanes0506", 1.0)):
        df, info = matriz(base)
        df["eua"] = eua
        df["eua_x_tela_1a3h"] = eua * df.tela_1a3h
        df["eua_x_tela_3h_mais"] = eua * df.tela_3h_mais
        des = info["desenho"].copy()
        des["peso"] = des.peso * len(des) / des.peso.sum()
        des["estrato"] = des.get("estrato", pd.Series(-1, index=des.index)).astype(float) + (1000 if eua else 0)
        if "upa" not in des:
            des["upa"] = np.arange(len(des), dtype=float)             # Vigitel: cada pessoa é a sua UPA
            des["estrato"] = -1.0
        partes.append(df)
        desenhos.append(des[["peso", "estrato", "upa"]])
    return pd.concat(partes, ignore_index=True), pd.concat(desenhos, ignore_index=True)


def grupos_tela(base: str) -> dict:
    """Y por faixa de tela (sem covariáveis), para ANOVA de um fator e teste t."""
    df, info = matriz(base)
    cat = info["tela_cat"]
    return {"< 1 h": df[POR_BASE[base].y][cat == 0], "1 a < 3 h": df[POR_BASE[base].y][cat == 1],
            "≥ 3 h": df[POR_BASE[base].y][cat == 2]}, info
