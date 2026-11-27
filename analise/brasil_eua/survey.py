"""T040/T041 — Regressão de Poisson com peso amostral e variância por linearização de Taylor.

Decisão da T040 (2026-11-27): Python. R não está instalado na máquina de referência.

Modelo: log E[y | x] = xᵀβ, ajustado por pseudo-máxima verossimilhança ponderada
    U(β) = Σᵢ wᵢ xᵢ (yᵢ − μᵢ) = 0,   μᵢ = exp(xᵢᵀβ).
exp(βⱼ) é a razão de prevalências (RP) do termo j.

Variância (a mesma do svyglm do pacote survey do R, com UPA e estrato):
    A = Σᵢ wᵢ μᵢ xᵢ xᵢᵀ                        ("pão")
    uᵢ = wᵢ xᵢ (yᵢ − μᵢ)                       (escore de cada pessoa)
    z_hj = Σ_{i ∈ UPA j do estrato h} uᵢ        (total do escore por UPA)
    B = Σ_h n_h/(n_h − 1) Σ_j (z_hj − z̄_h)(z_hj − z̄_h)ᵀ   ("recheio")
    V(β̂) = A⁻¹ B A⁻¹
Sem UPA (Vigitel), cada pessoa é a própria UPA num estrato único: V vira o sanduíche robusto
com fator n/(n − 1). Estrato com uma só UPA: centrado na média geral das UPAs, fator 1
(equivale a survey.lonely.psu = "adjust"); o número desses estratos fica registrado.

Graus de liberdade do desenho: d = nº de UPAs − nº de estratos (orientação do NCHS para o NHANES).
É a regra ÚNICA do projeto (specs 003 e 005). Testes de coeficiente usam t com d gl; sem UPA, normal (z).
Sensibilidade: regra do svyglm (gl residual d − p + 1, p = nº de parâmetros), em gl_svyglm().

Wald conjunto com q > 1 restrições e d finito: correção de Korn-Graubard,
    F = (d − q + 1)/(d·q) · W  ~  F(q, d − q + 1);
com q = 1 coincide com t². Sem gl de desenho (Vigitel), W ~ χ²(q), equivalente a F = W/q com (q, ∞).

Domínio (subpopulação): poisson_desenho(..., dominio="coluna booleana") ajusta o modelo só nas linhas
do domínio, mas calcula a variância com TODAS as UPAs e estratos do desenho (escores zero fora do
domínio), como svyglm(design = subset(desenho, ...)). Assim gl e UPAs por estrato são os do desenho completo.
"""
from dataclasses import dataclass, field, replace

import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm
from scipy import stats


@dataclass
class Ajuste:
    nomes: list
    beta: np.ndarray
    cov: np.ndarray
    gl: float | None          # gl do desenho (None = normal)
    n: int
    n_upas: int
    n_estratos: int
    estratos_1upa: int
    metodo: str
    cov_cluster_sm: np.ndarray | None = None
    dados: pd.DataFrame | None = field(default=None, repr=False)
    Ainv: np.ndarray | None = field(default=None, repr=False)
    meat_estratos: list | None = field(default=None, repr=False)   # [(B_h, n_h)] por estrato

    @property
    def n_param(self) -> int:
        return len(self.nomes)

    def gl_svyglm(self):
        """gl residual do svyglm do R: d − p + 1 (sensibilidade; None sem desenho)."""
        return (self.gl - self.n_param + 1) if self.gl else None

    def com_gl(self, gl):
        """Cópia com outro gl de desenho (ex.: base empilhada mostra o gl do NHANES; sensibilidade svyglm)."""
        return replace(self, gl=gl)

    def satterthwaite(self, termo: str | None = None, contraste: np.ndarray | None = None) -> float:
        """gl de Satterthwaite para a variância de cᵀβ: (Σ v_h)² / Σ v_h²/(n_h − 1), v_h = cᵀA⁻¹B_hA⁻¹c."""
        c = contraste if contraste is not None else np.eye(len(self.nomes))[self.nomes.index(termo)]
        g = self.Ainv @ c
        v = [(float(g @ Bh @ g), nh) for Bh, nh in self.meat_estratos if nh > 1]
        return sum(x for x, _ in v) ** 2 / sum(x ** 2 / (nh - 1) for x, nh in v)

    def ep(self):
        return np.sqrt(np.diag(self.cov))

    def tabela(self) -> pd.DataFrame:
        ep = self.ep()
        est = self.beta / ep
        q = stats.t.ppf(0.975, self.gl) if self.gl else stats.norm.ppf(0.975)
        p = 2 * (stats.t.sf(np.abs(est), self.gl) if self.gl else stats.norm.sf(np.abs(est)))
        return pd.DataFrame({"termo": self.nomes, "beta": self.beta, "ep": ep, "estatistica": est, "p": p,
                             "rp": np.exp(self.beta), "ic_inf": np.exp(self.beta - q * ep),
                             "ic_sup": np.exp(self.beta + q * ep)})

    def termo(self, nome: str) -> dict:
        t = self.tabela().set_index("termo").loc[nome]
        return {**t.to_dict(), "gl": self.gl, "n": self.n}

    def wald(self, termos: list[str] | None = None, contraste: np.ndarray | None = None) -> dict:
        """Wald conjunto H0: Lβ = 0. Com gl d do desenho: Korn-Graubard F = (d−q+1)/(d·q)·W ~ F(q, d−q+1).
        Sem gl de desenho: W ~ χ²(q)."""
        if contraste is None:
            idx = [self.nomes.index(t) for t in termos]
            L = np.zeros((len(idx), len(self.nomes)))
            L[np.arange(len(idx)), idx] = 1
        else:
            L = np.atleast_2d(contraste)
        lb = L @ self.beta
        W = float(lb @ np.linalg.solve(L @ self.cov @ L.T, lb))
        q = L.shape[0]
        if self.gl:
            d = self.gl
            gl2 = d - q + 1
            if gl2 < 1:
                raise ValueError(f"Korn-Graubard: q = {q} restrições com só {d} gl de desenho")
            F = (d - q + 1) / (d * q) * W
            return {"estatistica": F, "gl1": q, "gl2": gl2, "p": float(stats.f.sf(F, q, gl2)), "tipo": "F",
                    "wald_W": W}
        return {"estatistica": W, "gl1": q, "gl2": None, "p": float(stats.chi2.sf(W, q)), "tipo": "qui2", "wald_W": W}


def _meat(U: pd.DataFrame, upa: pd.Series, estrato: pd.Series):
    Z = U.groupby(upa.values).sum()
    est_da_upa = estrato.groupby(upa.values).first().reindex(Z.index)
    grand = Z.mean(axis=0).values
    B = np.zeros((U.shape[1], U.shape[1]))
    solo, partes = 0, []
    for h, g in Z.groupby(est_da_upa.values):
        nh = len(g)
        if nh == 1:
            solo += 1
            c = g.values - grand
            Bh = c.T @ c
        else:
            c = g.values - g.values.mean(axis=0)
            Bh = nh / (nh - 1) * (c.T @ c)
        B += Bh
        partes.append((Bh, nh))
    return B, len(Z), est_da_upa.nunique(), solo, partes


def poisson_desenho(df: pd.DataFrame, formula: str, peso: str | None = None, estrato: str | None = None,
                    upa: str | None = None, compara_cluster: bool = False, dominio: str | None = None) -> Ajuste:
    """Poisson log-linear com peso; variância por linearização (estrato + UPA) ou sanduíche robusto.

    dominio: nome de coluna booleana. O ajuste usa só as linhas do domínio; a variância usa o desenho
    inteiro (escores zero fora do domínio)."""
    y, X = patsy.dmatrices(formula, df, return_type="dataframe", NA_action="drop")
    d = df.loc[X.index]
    cols = [c for c in (peso, estrato, upa) if c]
    ok = d[cols].notna().all(axis=1) if cols else pd.Series(True, index=d.index)
    y, X, d = y[ok], X[ok], d[ok]
    w = d[peso].astype(float).values if peso else np.ones(len(d))
    dom = d[dominio].astype(bool).values if dominio else np.ones(len(d), dtype=bool)
    yv, Xv = y.iloc[:, 0].values, X.values
    res = sm.GLM(yv[dom], Xv[dom], family=sm.families.Poisson(), var_weights=w[dom]).fit(tol=1e-12)
    beta = np.asarray(res.params)
    mu = np.exp(Xv @ beta)
    wd = w * dom                                     # peso zero fora do domínio: escore e pão zerados
    A = (Xv * (wd * mu)[:, None]).T @ Xv
    U = pd.DataFrame(Xv * (wd * (yv - mu))[:, None])
    if upa:
        g_upa = (d[estrato].astype(str) + "_" + d[upa].astype(str)) if estrato else d[upa].astype(str)
        g_est = d[estrato] if estrato else pd.Series(0, index=d.index)
        metodo = "linearização (estrato + UPA)" if estrato else "linearização (UPA)"
    else:
        g_upa = pd.Series(np.arange(len(d)), index=d.index)
        g_est = pd.Series(0, index=d.index)
        metodo = "sanduíche robusto (cada pessoa = UPA, estrato único)"
    if dominio:
        metodo += ", domínio"
    B, n_upas, n_est, solo, partes = _meat(U, g_upa.reset_index(drop=True), g_est.reset_index(drop=True))
    Ainv = np.linalg.inv(A)
    cov = Ainv @ B @ Ainv
    gl = (n_upas - n_est) if upa else None
    cov_cl = None
    if compara_cluster and upa and not dominio:
        codes = pd.factorize(g_upa)[0]
        r2 = sm.GLM(yv, Xv, family=sm.families.Poisson(), var_weights=w).fit(
            cov_type="cluster", cov_kwds={"groups": codes}, tol=1e-12)
        cov_cl = np.asarray(r2.cov_params())
    return Ajuste(list(X.columns), beta, cov, gl, int(dom.sum()), n_upas, n_est, solo, metodo, cov_cl,
                  d[dom], Ainv, partes)


def mantel_haenszel(y: pd.Series, expo_alta: pd.Series, estrato: pd.Series) -> tuple[float, float]:
    """RP de Mantel-Haenszel por estrato e EP do log (Greenland-Robins), como na exploração de 27/11."""
    num = den = vn = 0.0
    for _, idx in estrato.groupby(estrato).groups.items():
        yy, gg = y.loc[idx].astype(bool), expo_alta.loc[idx].astype(bool)
        a1, n1, b0, n0 = (yy & gg).sum(), gg.sum(), (yy & ~gg).sum(), (~gg).sum()
        N = n1 + n0
        if n1 == 0 or n0 == 0 or b0 == 0:
            continue
        num += a1 * n0 / N
        den += b0 * n1 / N
        vn += (n1 * n0 * (a1 + b0) - a1 * b0 * N) / N ** 2
    rr = num / den
    return rr, np.sqrt(vn / (num * den))
