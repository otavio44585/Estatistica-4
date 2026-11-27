"""Métodos da spec 004: correlação na escala z de Fisher e meta-análise de efeitos aleatórios.

Referências (DOI conferido no Crossref em 2026-11-27):
- Fieller, Hartley e Pearson (1957), Biometrika 44(3-4):470-481, doi:10.1093/biomet/44.3-4.470 —
  variância de atanh(ρ de Spearman) ≈ 1,06/(n − 3).
- DerSimonian e Laird (1986), Controlled Clinical Trials 7(3):177-188, doi:10.1016/0197-2456(86)90046-2.
- Higgins e Thompson (2002), Statistics in Medicine 21(11):1539-1558, doi:10.1002/sim.1186 — I² e IC por H.
- Bakdash e Marusich (2017), Frontiers in Psychology 8:456, doi:10.3389/fpsyg.2017.00456 — correlação de
  medidas repetidas.
- Hartung e Knapp (2001), Statistics in Medicine 20(24):3875-3889, doi:10.1002/sim.1009 — IC da média
  aleatória com t(k − 1) e variância reescalada (Hartung-Knapp-Sidik-Jonkman), acrescentado após a
  verificação independente de 2026-11-27.
- Kish (1965), efeito do desenho por pesos desiguais: deff = 1 + CV² dos pesos = n·Σw²/(Σw)².
  Fórmula padrão; referência sem DOI, citada só como fórmula.
"""
import numpy as np
import pandas as pd
from scipy import stats

Z975 = stats.norm.ppf(0.975)


# ---------------------------------------------------------------- correlação por base
def postos_ponderados(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Posto médio ponderado: ponto médio do peso acumulado de cada valor (empates recebem o mesmo posto)."""
    ordem = np.argsort(x, kind="mergesort")
    xs, ws = x[ordem], w[ordem]
    valores, inicio = np.unique(xs, return_index=True)
    soma = np.add.reduceat(ws, inicio)
    acum = np.cumsum(soma)
    meio = acum - soma / 2
    return meio[np.searchsorted(valores, x)]


def pearson_ponderado(x, y, w) -> float:
    w = w / w.sum()
    mx, my = (w * x).sum(), (w * y).sum()
    cov = (w * (x - mx) * (y - my)).sum()
    return float(cov / np.sqrt((w * (x - mx) ** 2).sum() * (w * (y - my) ** 2).sum()))


def spearman_ponderado(x, y, w) -> float:
    """Sensibilidade (não padrão): Pearson ponderado dos postos ponderados."""
    return pearson_ponderado(postos_ponderados(x, w), postos_ponderados(y, w), w)


def ep_fhp(n: int) -> float:
    """EP de atanh(ρ de Spearman) por Fieller, Hartley e Pearson (1957)."""
    return float(np.sqrt(1.06 / (n - 3)))


def ep_bootstrap(x, y, B=1000, semente=2026) -> float:
    """EP de atanh(ρ) por bootstrap não paramétrico (reamostragem de pessoas)."""
    rng = np.random.default_rng(semente)
    n = len(x)
    z = np.empty(B)
    for b in range(B):
        i = rng.integers(0, n, n)
        r = stats.spearmanr(x[i], y[i]).statistic
        z[b] = np.arctanh(np.clip(r, -0.999999, 0.999999))
    return float(z.std(ddof=1))


def efeito(x, y, inverte=False) -> dict:
    """ρ de Spearman (principal) e r de Pearson (conferência), com z de Fisher e IC 95%."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    n = len(x)
    s = -1 if inverte else 1
    rho = s * stats.spearmanr(x, y).statistic
    r = s * stats.pearsonr(x, y).statistic
    z, ep = np.arctanh(rho), ep_fhp(n)
    return dict(n=n, rho=rho, r_pearson=r, z=z, ep_fhp=ep,
                rho_ic_inf=np.tanh(z - Z975 * ep), rho_ic_sup=np.tanh(z + Z975 * ep),
                p_rho=float(2 * stats.norm.sf(abs(z / ep))))


def spearman_parcial(x, y, c, inverte=False) -> dict:
    """ρ de Spearman parcial (postos de x e y controlados pelo posto de c, uma covariável).

    EP aproximado por √(1,06/(n − 4)): a fórmula de Fieller, Hartley e Pearson com um grau a menos.
    """
    x, y, c = (np.asarray(a, float) for a in (x, y, c))
    ok = ~(np.isnan(x) | np.isnan(y) | np.isnan(c))
    rx, ry, rc = (stats.rankdata(a[ok]) for a in (x, y, c))
    rxy, rxc, ryc = (np.corrcoef(a, b)[0, 1] for a, b in ((rx, ry), (rx, rc), (ry, rc)))
    rp = (-1 if inverte else 1) * (rxy - rxc * ryc) / np.sqrt((1 - rxc ** 2) * (1 - ryc ** 2))
    n = int(ok.sum())
    z, ep = np.arctanh(rp), float(np.sqrt(1.06 / (n - 4)))
    return dict(n=n, rho=float(rp), z=float(z), ep=ep,
                ic_inf=float(np.tanh(z - Z975 * ep)), ic_sup=float(np.tanh(z + Z975 * ep)))


def rmcorr(df: pd.DataFrame, sujeito: str, x: str, y: str) -> dict:
    """Correlação de medidas repetidas: Pearson entre x e y centrados na média de cada pessoa; gl = N − k − 1."""
    d = df[[sujeito, x, y]].dropna()
    d = d[d.groupby(sujeito)[x].transform("size") >= 2]
    xc = d[x] - d.groupby(sujeito)[x].transform("mean")
    yc = d[y] - d.groupby(sujeito)[y].transform("mean")
    r = float(np.sum(xc * yc) / np.sqrt(np.sum(xc ** 2) * np.sum(yc ** 2)))
    k, N = d[sujeito].nunique(), len(d)
    gl = N - k - 1
    t = r * np.sqrt(gl / (1 - r ** 2))
    ep = 1 / np.sqrt(gl - 1)
    z = np.arctanh(r)
    return dict(n=N, sujeitos=k, gl=gl, r=r, p=float(2 * stats.t.sf(abs(t), gl)),
                ic_inf=float(np.tanh(z - Z975 * ep)), ic_sup=float(np.tanh(z + Z975 * ep)))


# ---------------------------------------------------------------- meta-análise
def dersimonian_laird(y, v) -> dict:
    """Efeitos aleatórios de DerSimonian e Laird sobre efeitos y com variâncias v (escala z de Fisher)."""
    y, v = np.asarray(y, float), np.asarray(v, float)
    k = len(y)
    w = 1 / v
    mu_fixo = np.sum(w * y) / np.sum(w)
    Q = float(np.sum(w * (y - mu_fixo) ** 2))
    gl = k - 1
    C = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - gl) / C) if k > 1 else 0.0
    ws = 1 / (v + tau2)
    mu = float(np.sum(ws * y) / np.sum(ws))
    ep = float(np.sqrt(1 / np.sum(ws)))
    I2 = max(0.0, (Q - gl) / Q) if Q > 0 and k > 1 else 0.0
    return dict(k=k, mu=mu, ep=ep, ic_inf=mu - Z975 * ep, ic_sup=mu + Z975 * ep,
                z=mu / ep, p=float(2 * stats.norm.sf(abs(mu / ep))),
                mu_fixo=float(mu_fixo), ep_fixo=float(np.sqrt(1 / np.sum(w))),
                Q=Q, gl=gl, p_Q=float(stats.chi2.sf(Q, gl)) if k > 1 else np.nan,
                tau2=float(tau2), I2=float(I2), **ic_i2(Q, k),
                peso_fixo=w / w.sum(), peso_aleatorio=ws / ws.sum())


def hartung_knapp(y, v, tau2: float) -> dict:
    """IC de Hartung-Knapp-Sidik-Jonkman para a média aleatória (pesos 1/(v + τ²) do DerSimonian-Laird).

    q = Σ wᵢ*(yᵢ − μ)² / (k − 1);  EP_HK = √(q / Σ wᵢ*);  IC = μ ± t(0,975; k − 1)·EP_HK.
    Sem truncamento de q em 1 (forma original, igual à do statsmodels `sd_eff_w_re_hksj`).
    """
    y, v = np.asarray(y, float), np.asarray(v, float)
    k = len(y)
    if k < 2:
        return dict(ep_hk=np.nan, ic_inf_hk=np.nan, ic_sup_hk=np.nan, p_hk=np.nan, gl_hk=np.nan, q_hk=np.nan)
    ws = 1 / (v + tau2)
    mu = np.sum(ws * y) / np.sum(ws)
    q = float(np.sum(ws * (y - mu) ** 2) / (k - 1))
    ep = float(np.sqrt(q / np.sum(ws)))
    tc = stats.t.ppf(0.975, k - 1)
    return dict(ep_hk=ep, ic_inf_hk=float(mu - tc * ep), ic_sup_hk=float(mu + tc * ep),
                p_hk=float(2 * stats.t.sf(abs(mu / ep), k - 1)), gl_hk=k - 1, q_hk=q)


def deff_kish(w) -> float:
    """Efeito do desenho devido só aos pesos desiguais (Kish): 1 + CV² = n·Σw² / (Σw)²."""
    w = np.asarray(w, float)
    w = w[~np.isnan(w)]
    return float(len(w) * np.sum(w ** 2) / np.sum(w) ** 2)


def tendencia_ordenada(mu, ep, escore) -> dict:
    """Inclinação de uma meta-regressão ponderada (pesos 1/EP²) das médias de subgrupo sobre um escore ordinal.

    Usada só como análise EXPLORATÓRIA da ordem prevista em H4.2 (a spec registrou uma hipótese ordenada).
    """
    mu, ep, x = (np.asarray(a, float) for a in (mu, ep, escore))
    w = 1 / ep ** 2
    xb = np.sum(w * x) / np.sum(w)
    yb = np.sum(w * mu) / np.sum(w)
    sxx = np.sum(w * (x - xb) ** 2)
    b = float(np.sum(w * (x - xb) * (mu - yb)) / sxx)
    se = float(np.sqrt(1 / sxx))
    return dict(inclinacao=b, ep=se, z=b / se, p=float(2 * stats.norm.sf(abs(b / se))),
                p_unilateral=float(stats.norm.sf(b / se)))


def ic_i2(Q: float, k: int) -> dict:
    """IC 95% de I² pelo IC de H (Higgins e Thompson, 2002, método baseado no teste)."""
    if k < 3:
        return dict(I2_ic_inf=np.nan, I2_ic_sup=np.nan)
    H = np.sqrt(max(Q, 1e-12) / (k - 1))
    if Q > k:
        ep_lnH = 0.5 * (np.log(Q) - np.log(k - 1)) / (np.sqrt(2 * Q) - np.sqrt(2 * k - 3))
    else:
        ep_lnH = np.sqrt(1 / (2 * (k - 2)) * (1 - 1 / (3 * (k - 2) ** 2)))
    lo, hi = np.exp(np.log(H) - Z975 * ep_lnH), np.exp(np.log(H) + Z975 * ep_lnH)
    f = lambda h: max(0.0, (h ** 2 - 1) / h ** 2)
    return dict(I2_ic_inf=f(max(lo, 1.0)) if lo > 1 else 0.0, I2_ic_sup=f(hi))


def subgrupos(df: pd.DataFrame, grupo: str = "tipo") -> tuple[pd.DataFrame, dict]:
    """τ² separado por subgrupo; Q entre = Q das estimativas combinadas (gl = G − 1)."""
    linhas = []
    for g, d in df.groupby(grupo, sort=False):
        m = dersimonian_laird(d.z, d.ep ** 2)
        linhas.append(dict(subgrupo=g, **{k: v for k, v in m.items() if not k.startswith("peso")}))
    t = pd.DataFrame(linhas)
    w = 1 / t.ep ** 2
    mu = np.sum(w * t.mu) / np.sum(w)
    Qb = float(np.sum(w * (t.mu - mu) ** 2))
    gl = len(t) - 1
    return t, dict(Q_entre=Qb, gl=gl, p=float(stats.chi2.sf(Qb, gl)))


def compara_z(z1, ep1, z2, ep2) -> dict:
    d = z1 - z2
    ep = np.sqrt(ep1 ** 2 + ep2 ** 2)
    return dict(diferenca_z=d, ep=ep, z=d / ep, p=float(2 * stats.norm.sf(abs(d / ep))))


def tost_equivalencia(z, ep, r_inf, r_sup) -> dict:
    """Dois testes unilaterais sobre z de Fisher: H0 fora de [r_inf, r_sup]; H1 dentro."""
    zi, zs = np.arctanh(r_inf), np.arctanh(r_sup)
    t_inf, t_sup = (z - zi) / ep, (z - zs) / ep
    p_inf, p_sup = float(stats.norm.sf(t_inf)), float(stats.norm.cdf(t_sup))
    return dict(z_inf=float(t_inf), z_sup=float(t_sup), p_inf=p_inf, p_sup=p_sup, p=max(p_inf, p_sup))


def ep_de_ic(r_inf, r_sup) -> float:
    """EP na escala z a partir de um IC 95% publicado em r."""
    return float((np.arctanh(r_sup) - np.arctanh(r_inf)) / (2 * Z975))
