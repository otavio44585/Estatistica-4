"""T081 — Mínimos quadrados ordinários por álgebra matricial (caminho C da conferência).

Tudo o que a ferramenta Regressão do Excel mostra no SUMMARY OUTPUT sai daqui:
    b = (XᵀX)⁻¹ Xᵀy                         coeficientes
    s² = SQRes / (n − k − 1)                 variância residual (k = nº de regressores, sem o intercepto)
    EP(bⱼ) = √(s² · [(XᵀX)⁻¹]ⱼⱼ)             erro padrão
    tⱼ = bⱼ / EP(bⱼ);  p = 2·P(T(n−k−1) > |tⱼ|)
    IC 95%: bⱼ ± t(0,975; n−k−1) · EP(bⱼ)
    F = (SQReg / k) / (SQRes / (n − k − 1));  p = P(F(k, n−k−1) > F)   ("F de significação")
    R² = SQReg / SQTot;  R² ajustado = 1 − (1 − R²)(n − 1)/(n − k − 1)

Também tem a versão ponderada (WLS) com erro padrão de desenho amostral por linearização
(estrato e UPA), no mesmo espírito do pacote `survey` do R, usada para Vigitel e NHANES.
"""
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy import stats


@dataclass
class Ajuste:
    nomes: list
    b: np.ndarray
    ep: np.ndarray
    t: np.ndarray
    p: np.ndarray
    ic_inf: np.ndarray
    ic_sup: np.ndarray
    n: int
    k: int
    gl_res: float
    sq_reg: float
    sq_res: float
    sq_tot: float
    f: float
    p_f: float
    r2: float
    r2_aj: float
    erro_padrao: float
    tipo_ep: str = "clássico (Excel)"
    extra: dict = field(default_factory=dict)

    @property
    def r_multiplo(self) -> float:
        return float(np.sqrt(self.r2))

    def coef(self, nome: str) -> dict:
        j = self.nomes.index(nome)
        return dict(b=self.b[j], ep=self.ep[j], t=self.t[j], p=self.p[j], ic_inf=self.ic_inf[j],
                    ic_sup=self.ic_sup[j], gl=self.gl_res)


def _matriz(X: pd.DataFrame) -> tuple[np.ndarray, list]:
    nomes = ["Intercepto"] + list(X.columns)
    return np.column_stack([np.ones(len(X)), X.to_numpy(float)]), nomes


def mqo(y: pd.Series, X: pd.DataFrame) -> Ajuste:
    """MQO clássico, exatamente o que a Regressão do Excel calcula."""
    Xm, nomes = _matriz(X)
    yv = y.to_numpy(float)
    n, kp1 = Xm.shape
    k = kp1 - 1
    XtX_inv = np.linalg.inv(Xm.T @ Xm)
    b = XtX_inv @ Xm.T @ yv
    e = yv - Xm @ b
    sq_res = float(e @ e)
    sq_tot = float(((yv - yv.mean()) ** 2).sum())
    sq_reg = sq_tot - sq_res
    gl = n - k - 1
    s2 = sq_res / gl
    ep = np.sqrt(s2 * np.diag(XtX_inv))
    t = b / ep
    p = 2 * stats.t.sf(np.abs(t), gl)
    tc = stats.t.ppf(0.975, gl)
    f = (sq_reg / k) / s2 if k > 0 else np.nan
    p_f = stats.f.sf(f, k, gl) if k > 0 else np.nan
    r2 = sq_reg / sq_tot
    return Ajuste(nomes, b, ep, t, p, b - tc * ep, b + tc * ep, n, k, gl, sq_reg, sq_res, sq_tot,
                  f, p_f, r2, 1 - (1 - r2) * (n - 1) / gl, float(np.sqrt(s2)))


def f_parcial(completo: Ajuste, restrito: Ajuste) -> dict:
    """F de modelos aninhados: [(SQRes_r − SQRes_c)/q] / [SQRes_c/(n − k_c − 1)]; f² = ΔR²/(1 − R²_c)."""
    q = completo.k - restrito.k
    f = ((restrito.sq_res - completo.sq_res) / q) / (completo.sq_res / completo.gl_res)
    d_r2 = completo.r2 - restrito.r2
    return dict(f=f, gl1=q, gl2=completo.gl_res, p=stats.f.sf(f, q, completo.gl_res),
                delta_r2=d_r2, f2=d_r2 / (1 - completo.r2))


def summary_output(a: Ajuste) -> pd.DataFrame:
    """Tabela no layout do SUMMARY OUTPUT do Excel (uma linha por célula preenchida)."""
    lin = [
        ("Estatística de regressão", "R múltiplo", a.r_multiplo), ("Estatística de regressão", "R-quadrado", a.r2),
        ("Estatística de regressão", "R-quadrado ajustado", a.r2_aj),
        ("Estatística de regressão", "Erro padrão", a.erro_padrao), ("Estatística de regressão", "Observações", a.n),
        ("ANOVA", "Regressão gl", a.k), ("ANOVA", "Regressão SQ", a.sq_reg), ("ANOVA", "Regressão MQ", a.sq_reg / a.k),
        ("ANOVA", "F", a.f), ("ANOVA", "F de significação", a.p_f),
        ("ANOVA", "Resíduo gl", a.gl_res), ("ANOVA", "Resíduo SQ", a.sq_res), ("ANOVA", "Resíduo MQ", a.sq_res / a.gl_res),
        ("ANOVA", "Total gl", a.n - 1), ("ANOVA", "Total SQ", a.sq_tot),
    ]
    df = pd.DataFrame(lin, columns=["bloco", "item", "valor"])
    coefs = pd.DataFrame({"bloco": "Coeficientes", "item": a.nomes, "coeficiente": a.b, "erro_padrao": a.ep,
                          "stat_t": a.t, "valor_p": a.p, "inferior_95": a.ic_inf, "superior_95": a.ic_sup})
    return pd.concat([df, coefs], ignore_index=True)


# ---------------------------------------------------------------- ponderado (desenho amostral)

def korn_graubard(W: float, q: int, d: float) -> dict:
    """Wald conjunto com gl de desenho finito (correção de Korn e Graubard, a mesma do svyglm do R):
    F = (d − q + 1)/(d·q) · W, com gl (q, d − q + 1). Para d grande, F → W/q."""
    gl2 = d - q + 1
    if not np.isfinite(d) or gl2 <= 0:
        return dict(f=np.nan, gl1=q, gl2=gl2, p=np.nan, wald=W)
    f = (d - q + 1) / (d * q) * W
    return dict(f=f, gl1=q, gl2=gl2, p=float(stats.f.sf(f, q, gl2)), wald=W)


def mqp(y: pd.Series, X: pd.DataFrame, peso: pd.Series, estrato: pd.Series | None = None,
        upa: pd.Series | None = None, regra_gl: str = "desenho") -> Ajuste:
    """WLS com peso amostral e erro padrão por linearização de Taylor.

    V(b) = (XᵀWX)⁻¹ G (XᵀWX)⁻¹, com G = Σ_h n_h/(n_h − 1) Σ_i (u_hi − ū_h)(u_hi − ū_h)ᵀ,
    u_hi = Σ_{j ∈ UPA i do estrato h} w_j x_j e_j.
    Sem UPA, cada pessoa é a sua UPA (equivale ao EP robusto HC0 com correção n/(n − 1) por estrato).
    Estrato com uma só UPA: centrado na média geral das UPAs, fator 1 — mesma regra de
    analise/brasil_eua/survey.py (survey.lonely.psu = "adjust"); o número desses estratos fica em extra.

    Graus de liberdade (regra única do projeto, a mesma da spec 003 e a orientação do NCHS para o NHANES):
        regra_gl="desenho": gl = nº de UPAs − nº de estratos   (principal)
        regra_gl="svyglm":  gl = UPAs − estratos + 1 − nº de parâmetros   (sensibilidade)
    O F global (todos os coeficientes menos o intercepto) usa a correção de Korn-Graubard.
    """
    Xm, nomes = _matriz(X)
    yv, w = y.to_numpy(float), peso.to_numpy(float)
    n, kp1 = Xm.shape
    k = kp1 - 1
    A = np.linalg.inv(Xm.T @ (Xm * w[:, None]))
    b = A @ Xm.T @ (w * yv)
    e = yv - Xm @ b
    est = np.zeros(n, int) if estrato is None else pd.factorize(estrato.to_numpy())[0]
    psu = np.arange(n) if upa is None else pd.factorize(pd.Series(list(zip(est, upa.to_numpy()))))[0]
    score = Xm * (w * e)[:, None]
    U = pd.DataFrame(score).groupby(psu).sum()
    est_psu = pd.Series(est).groupby(psu).first().loc[U.index].to_numpy()
    Uv = U.to_numpy()
    media_geral = Uv.mean(axis=0)
    G = np.zeros((kp1, kp1))
    solo = 0
    for h in np.unique(est_psu):
        Uh = Uv[est_psu == h]
        nh = len(Uh)
        if nh == 1:
            solo += 1
            c = Uh - media_geral
            G += c.T @ c
        else:
            c = Uh - Uh.mean(axis=0)
            G += nh / (nh - 1) * c.T @ c
    V = A @ G @ A
    ep = np.sqrt(np.diag(V))
    gl_desenho = len(Uv) - len(np.unique(est_psu))
    gl_svyglm = gl_desenho + 1 - kp1
    if regra_gl not in ("desenho", "svyglm"):
        raise ValueError(regra_gl)
    gl = gl_desenho if regra_gl == "desenho" else gl_svyglm
    t = b / ep
    p = 2 * stats.t.sf(np.abs(t), gl)
    tc = stats.t.ppf(0.975, gl)
    ybar = np.average(yv, weights=w)
    sq_tot = float((w * (yv - ybar) ** 2).sum())
    sq_res = float((w * e ** 2).sum())
    r2 = 1 - sq_res / sq_tot
    R = np.eye(kp1)[1:]
    W = float(b[1:] @ np.linalg.solve(R @ V @ R.T, b[1:]))
    kg = korn_graubard(W, k, gl)
    tipo = "linearização (estrato + UPA)" if upa is not None else "robusto (cada pessoa é a sua UPA)"
    return Ajuste(nomes, b, ep, t, p, b - tc * ep, b + tc * ep, n, k, gl, sq_tot - sq_res, sq_res, sq_tot,
                  kg["f"], kg["p"], r2, 1 - (1 - r2) * (n - 1) / (n - k - 1), float(np.sqrt(sq_res / w.sum())),
                  tipo_ep=tipo, extra=dict(V=V, gl_desenho=gl_desenho, gl_svyglm=gl_svyglm, regra_gl=regra_gl,
                                           estratos_1upa=solo, f_global_gl2=kg["gl2"]))


def coef_com_gl(a: Ajuste, nome: str, gl: float) -> dict:
    """Coeficiente de um ajuste ponderado com outro gl (ex.: gl de desenho do NHANES na base empilhada)."""
    j = a.nomes.index(nome)
    t = a.b[j] / a.ep[j]
    tc = stats.t.ppf(0.975, gl)
    return dict(b=a.b[j], ep=a.ep[j], t=t, p=float(2 * stats.t.sf(abs(t), gl)),
                ic_inf=a.b[j] - tc * a.ep[j], ic_sup=a.b[j] + tc * a.ep[j], gl=gl)


def wald_bloco(a: Ajuste, nomes: list, gl: float | None = None) -> dict:
    """F de Wald para um bloco de coeficientes (ex.: as 2 dummies de tela) no modelo ponderado,
    com a correção de Korn-Graubard: F = (d − q + 1)/(d·q)·W, gl (q, d − q + 1).
    d = gl do ajuste (UPAs − estratos), ou o gl informado (base empilhada: gl de desenho do NHANES)."""
    V = a.extra["V"]
    j = [a.nomes.index(n) for n in nomes]
    bj = a.b[j]
    W = float(bj @ np.linalg.solve(V[np.ix_(j, j)], bj))
    return korn_graubard(W, len(j), a.gl_res if gl is None else gl)
