"""Funções multivariadas da spec 002 (plano, seção "Técnicas e como cada uma é mostrada").

Implementação própria, conferida em tests/test_002_multivariada.py contra scikit-learn e factor_analyzer.
O `FactorAnalyzer.fit` do factor_analyzer 0.5.1 não roda com o scikit-learn 1.9 (argumento
`force_all_finite` removido do `check_array`); por isso a análise fatorial está escrita aqui.

Referências (DOI conferido no Crossref em 2026-11-27):
- Cronbach (1951), Psychometrika 16(3):297-334, doi:10.1007/BF02310555 — alfa.
- Kaiser e Rice (1974), Educ. Psychol. Meas. 34:111-117, doi:10.1177/001316447403400115 — KMO.
- Bartlett (1950), Br. J. Stat. Psychol. 3(2):77-85, doi:10.1111/j.2044-8317.1950.tb00285.x — esfericidade.
- Horn (1965), Psychometrika 30(2):179-185, doi:10.1007/BF02289447 — análise paralela.
- Kaiser (1958), Psychometrika 23(3):187-200, doi:10.1007/BF02289233 — varimax.
- Jennrich (2002), Psychometrika 67(1):7-19, doi:10.1007/BF02294706 — rotação oblíqua por gradiente projetado.
- Olsson (1979), Psychometrika 44(4):443-460, doi:10.1007/BF02296207 — correlação policórica (dois passos).
- Lorenzo-Seva e ten Berge (2006), Methodology 2(2):57-64, doi:10.1027/1614-2241.2.2.57 — limites de Tucker.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import optimize, stats


# ---------------------------------------------------------------- confiabilidade e adequação
def alfa_cronbach(X) -> float:
    """α = k/(k−1) · (1 − Σ var(itens) / var(total)), variâncias com ddof = 1."""
    X = np.asarray(X, float)
    k = X.shape[1]
    return k / (k - 1) * (1 - X.var(axis=0, ddof=1).sum() / X.sum(axis=1).var(ddof=1))


def alfa_sem_item(X) -> np.ndarray:
    X = np.asarray(X, float)
    return np.array([alfa_cronbach(np.delete(X, j, axis=1)) for j in range(X.shape[1])])


def correlacao_item_total(X) -> np.ndarray:
    """Correlação de cada item com a soma dos outros (item-total corrigida)."""
    X = np.asarray(X, float)
    tot = X.sum(axis=1)
    return np.array([np.corrcoef(X[:, j], tot - X[:, j])[0, 1] for j in range(X.shape[1])])


def kmo(R) -> tuple[float, np.ndarray]:
    """KMO global e MSA por item a partir da correlação parcial (inversa de R).

    parcial_ij = −Rinv_ij / √(Rinv_ii · Rinv_jj);  KMO = Σr² / (Σr² + Σparcial²) fora da diagonal.
    """
    R = np.asarray(R, float)
    Ri = np.linalg.inv(R)
    d = np.sqrt(np.diag(Ri))
    P = -Ri / np.outer(d, d)
    np.fill_diagonal(P, 0)
    R0 = R.copy()
    np.fill_diagonal(R0, 0)
    r2, p2 = R0 ** 2, P ** 2
    msa = r2.sum(axis=0) / (r2.sum(axis=0) + p2.sum(axis=0))
    return float(r2.sum() / (r2.sum() + p2.sum())), msa


def bartlett(R, n: int) -> tuple[float, int, float]:
    """χ² = −(n − 1 − (2p + 5)/6) · ln det R, gl = p(p − 1)/2."""
    R = np.asarray(R, float)
    p = R.shape[0]
    chi2 = -(n - 1 - (2 * p + 5) / 6) * np.log(np.linalg.det(R))
    gl = p * (p - 1) // 2
    return float(chi2), int(gl), float(stats.chi2.sf(chi2, gl))


# ---------------------------------------------------------------- PCA por SVD
def padroniza(X) -> np.ndarray:
    X = np.asarray(X, float)
    return (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)


def pca_svd(X) -> dict:
    """PCA pela decomposição em valores singulares da matriz padronizada.

    Z = U Σ Vᵀ;  autovalores λ = σ² / (n − 1);  cargas = V Σ / √(n − 1);  escores = U Σ.
    O sinal de cada componente é fixado para que a soma das cargas seja positiva.
    """
    Z = padroniza(X)
    n = Z.shape[0]
    U, s, Vt = np.linalg.svd(Z, full_matrices=False)
    V = Vt.T
    sinal = np.sign(V.sum(axis=0))
    sinal[sinal == 0] = 1
    U, V = U * sinal, V * sinal
    lam = s ** 2 / (n - 1)
    return dict(Z=Z, U=U, sigma=s, V=V, autovalores=lam, variancia=lam / lam.sum(),
                cargas=V * s / np.sqrt(n - 1), escores=U * s)


def analise_paralela(n: int, p: int, reps: int = 1000, percentil: float = 95, semente: int = 2026,
                     bloco: int = 50) -> dict:
    """Horn (1965): autovalores da correlação de dados normais independentes com o mesmo n e p."""
    rng = np.random.default_rng(semente)
    lams = np.empty((reps, p))
    for i in range(reps):
        Xr = rng.standard_normal((n, p))
        lams[i] = np.sort(np.linalg.eigvalsh(np.corrcoef(Xr, rowvar=False)))[::-1]
    return dict(media=lams.mean(axis=0), p95=np.percentile(lams, percentil, axis=0))


def n_retidos(autovalores, referencia) -> int:
    """Quantos autovalores consecutivos, a partir do primeiro, ficam acima da referência."""
    k = 0
    for a, r in zip(autovalores, referencia):
        if a > r:
            k += 1
        else:
            break
    return max(k, 1)


# ---------------------------------------------------------------- análise fatorial
def _smc(R):
    return 1 - 1 / np.diag(np.linalg.inv(R))


def _cargas_ml(psi, R, k):
    sc = 1 / np.sqrt(psi)
    S = R * np.outer(sc, sc)
    w, v = np.linalg.eigh(S)
    w, v = w[::-1][:k], v[:, ::-1][:, :k]
    return (v * np.sqrt(np.maximum(w - 1, 0))) * np.sqrt(psi)[:, None]


def af_ml(R, k: int) -> dict:
    """Máxima verossimilhança (Jöreskog): minimiza −Σ_{j>k}(ln λ_j − λ_j) − k + p sobre as unicidades."""
    R = np.asarray(R, float)
    p = R.shape[0]

    def obj(psi):
        sc = 1 / np.sqrt(psi)
        w = np.linalg.eigvalsh(R * np.outer(sc, sc))[::-1][k:]
        return -(np.sum(np.log(w) - w) - k + p)

    ini = (1 - 0.5 * k / p) / np.diag(np.linalg.inv(R))
    res = optimize.minimize(obj, ini, method="L-BFGS-B", bounds=[(0.005, 1)] * p)
    L = _cargas_ml(res.x, R, k)
    L = _sinal(L)
    return dict(cargas=L, comunalidades=(L ** 2).sum(axis=1), unicidades=1 - (L ** 2).sum(axis=1),
                convergiu=bool(res.success), objetivo=float(res.fun))


def af_eixos_principais(R, k: int, max_iter: int = 500, tol: float = 1e-8) -> dict:
    """Eixos principais iterados: diagonal de R trocada pelas comunalidades até convergir (início = SMC)."""
    R = np.asarray(R, float)
    h2 = _smc(R)
    for it in range(max_iter):
        Rr = R.copy()
        np.fill_diagonal(Rr, h2)
        w, v = np.linalg.eigh(Rr)
        w, v = w[::-1][:k], v[:, ::-1][:, :k]
        L = v * np.sqrt(np.maximum(w, 0))
        novo = (L ** 2).sum(axis=1)
        if np.max(np.abs(novo - h2)) < tol:
            h2 = novo
            break
        h2 = novo
    L = _sinal(L)
    return dict(cargas=L, comunalidades=(L ** 2).sum(axis=1), unicidades=1 - (L ** 2).sum(axis=1),
                convergiu=it < max_iter - 1, iteracoes=it + 1)


def _sinal(L):
    s = np.sign(L.sum(axis=0))
    s[s == 0] = 1
    return L * s


def varimax(L, normaliza: bool = True, max_iter: int = 1000, tol: float = 1e-10) -> tuple[np.ndarray, np.ndarray]:
    """Varimax (Kaiser, 1958) com normalização de Kaiser. Devolve (cargas rotacionadas, matriz T)."""
    L = np.asarray(L, float)
    p, k = L.shape
    h = np.sqrt((L ** 2).sum(axis=1)) if normaliza else np.ones(p)
    A = L / h[:, None]
    T = np.eye(k)
    d = 0
    for _ in range(max_iter):
        B = A @ T
        u, s, vt = np.linalg.svd(A.T @ (B ** 3 - B @ np.diag((B ** 2).sum(axis=0)) / p))
        T = u @ vt
        d_novo = s.sum()
        if d_novo < d * (1 + tol):
            break
        d = d_novo
    return _sinal((A @ T) * h[:, None]), T


def oblimin(L, gamma: float = 0.0, normaliza: bool = True, max_iter: int = 1000, tol: float = 1e-6):
    """Oblimin direto por gradiente projetado (Jennrich, 2002). Devolve (padrão, Φ, T)."""
    L = np.asarray(L, float)
    p, k = L.shape
    h = np.sqrt((L ** 2).sum(axis=1)) if normaliza else np.ones(p)
    A = L / h[:, None]
    N = np.ones((k, k)) - np.eye(k)
    C = np.ones((p, p)) / p if gamma else np.zeros((p, p))

    def crit(Lam):
        L2 = Lam ** 2
        X = (np.eye(p) - gamma * C) @ L2 @ N
        return np.sum(L2 * X) / 4, Lam * X

    T = np.eye(k)
    Lam = A @ np.linalg.inv(T).T
    f, Gq = crit(Lam)
    G = -(Lam.T @ Gq @ np.linalg.inv(T)).T
    al = 1.0
    for _ in range(max_iter):
        Gp = G - T @ np.diag(np.sum(T * G, axis=0))
        s = np.linalg.norm(Gp)
        if s < tol:
            break
        al *= 2
        for _ in range(11):
            X = T - al * Gp
            Tt = X / np.sqrt((X ** 2).sum(axis=0))
            Lamt = A @ np.linalg.inv(Tt).T
            ft, Gqt = crit(Lamt)
            if ft < f - 0.5 * s ** 2 * al:
                break
            al /= 2
        T, f, Gq, Lam = Tt, ft, Gqt, Lamt
        G = -(Lam.T @ Gq @ np.linalg.inv(T)).T
    padrao = Lam * h[:, None]
    Phi = T.T @ T
    s = np.sign(padrao.sum(axis=0))
    s[s == 0] = 1
    return padrao * s, Phi * np.outer(s, s), T


def escores_regressao(Z, R, cargas, Phi=None) -> np.ndarray:
    """Escores de Thurstone (regressão): F = Z · R⁻¹ · Λ · Φ (Φ = I na solução ortogonal)."""
    k = cargas.shape[1]
    Phi = np.eye(k) if Phi is None else Phi
    W = np.linalg.solve(R, cargas @ Phi)
    return Z @ W


def tucker(a, b) -> float:
    """Coeficiente de congruência φ = Σ aᵢbᵢ / √(Σaᵢ² · Σbᵢ²)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float(a @ b / np.sqrt((a @ a) * (b @ b)))


# ---------------------------------------------------------------- correlações alternativas
def correlacao_ponderada(X, w) -> np.ndarray:
    X, w = np.asarray(X, float), np.asarray(w, float)
    w = w / w.sum()
    m = w @ X
    D = X - m
    C = (D * w[:, None]).T @ D
    d = np.sqrt(np.diag(C))
    return C / np.outer(d, d)


def _limiares(x):
    cats = np.sort(np.unique(x))
    acum = np.cumsum([np.mean(x == c) for c in cats])[:-1]
    return cats, stats.norm.ppf(acum)


def policorica_par(x, y) -> float:
    """Policórica em dois passos (Olsson, 1979): limiares pelas marginais, depois ρ por máxima verossimilhança."""
    x, y = np.asarray(x), np.asarray(y)
    cx, ax = _limiares(x)
    cy, ay = _limiares(y)
    tab = pd.crosstab(pd.Categorical(x, cx), pd.Categorical(y, cy), dropna=False).to_numpy()
    BIG = 10.0
    ax_ = np.r_[-BIG, ax, BIG]
    ay_ = np.r_[-BIG, ay, BIG]
    A, B = np.meshgrid(ax_, ay_, indexing="ij")
    pts = np.column_stack([A.ravel(), B.ravel()])

    def nll(rho):
        F = stats.multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]]).cdf(pts).reshape(A.shape)
        P = F[1:, 1:] - F[:-1, 1:] - F[1:, :-1] + F[:-1, :-1]
        return -np.sum(tab * np.log(np.clip(P, 1e-300, None)))

    r = optimize.minimize_scalar(nll, bounds=(-0.995, 0.995), method="bounded", options={"xatol": 1e-6})
    return float(r.x)


def policorica(X) -> np.ndarray:
    X = np.asarray(X)
    p = X.shape[1]
    R = np.eye(p)
    for i in range(p):
        for j in range(i + 1, p):
            R[i, j] = R[j, i] = policorica_par(X[:, i], X[:, j])
    return torna_pd(R)


def torna_pd(R, eps: float = 1e-6) -> np.ndarray:
    """Se R não for positiva definida, corta autovalores em eps e reescala a diagonal para 1."""
    w, v = np.linalg.eigh(R)
    if w.min() > eps:
        return R
    R2 = (v * np.maximum(w, eps)) @ v.T
    d = np.sqrt(np.diag(R2))
    return R2 / np.outer(d, d)
