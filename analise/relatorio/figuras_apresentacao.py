"""Figuras da apresentação (spec 006), geradas a partir dos dados e dos CSVs de resultados/.

resultados/006/figuras/teste_explicado.png   um teste de hipótese desenhado: curva sob H0, α = 0,05, regiões de
                                              rejeição e a estatística observada (H3.1, Vigitel)
resultados/006/figuras/testes_painel.png     a mesma leitura para cada teste t/z das famílias confirmatórias
resultados/006/figuras/confundimento_idade.png  PNS 2019: por faixa etária, % com tela ≥ 3 h e % com problema de sono
resultados/006/tabelas/testes_apresentacao.csv   os testes desenhados (estatística, gl, p, p Holm, decisão)

Uso: python -m analise.relatorio.figuras_apresentacao
"""
import numpy as np
import pandas as pd
from scipy import stats

from analise.comum import caminhos
from analise.comum.estatistica import formata_p, salva_csv
from analise.comum.graficos import COR_NEUTRA, estilo, plt, salva

R = caminhos.RESULTADOS
ALFA = 0.05
MARINHO, TURQUESA, AMBAR = "#08223D", "#00A1B8", "#F1B634"


def _csv(spec, nome):
    return pd.read_csv(R / spec / "tabelas" / f"{nome}.csv", sep=";", decimal=",", encoding="utf-8-sig")


def testes() -> pd.DataFrame:
    """Testes t/z confirmatórios das specs 003 e 005, com a versão que decide."""
    L = []
    h3 = _csv("003", "hipoteses")
    for r in h3.itertuples():
        if str(r.tipo_estat) not in ("z", "t") or pd.isna(r.estatistica):
            continue
        if str(getattr(r, "exposicao", "")) not in ("digital", "TV × digital"):
            continue
        gl = np.inf if str(r.tipo_estat) == "z" or pd.isna(r.gl2) else float(r.gl2)
        L.append(dict(spec="003", hipotese=r.hipotese, base=r.base, teste=f"RP ({r.exposicao})", tipo=r.tipo_estat,
                      estatistica=float(r.estatistica), gl=gl, p=float(r.p), p_holm=float(r.p_holm), decisao=r.decisao))
    h5 = _csv("005", "hipoteses")
    for r in h5.itertuples():
        if pd.notna(r.gl1) or pd.isna(r.estatistica):          # F (ANOVA) fica fora do painel t/z
            continue
        L.append(dict(spec="005", hipotese=r.hipotese, base=r.base, teste=str(r.teste), tipo="t",
                      estatistica=float(r.estatistica), gl=float(r.gl2) if pd.notna(r.gl2) else np.inf,
                      p=float(r.p), p_holm=float(r.p_holm), decisao=r.decisao))
    return pd.DataFrame(L)


def _dist(gl):
    return stats.norm if not np.isfinite(gl) or gl > 1000 else stats.t(gl)


def desenha(ax, est, gl, titulo, detalhe=True, lim=5.0):
    d = _dist(gl)
    crit = d.ppf(1 - ALFA / 2)
    x = np.linspace(-lim, lim, 600)
    y = d.pdf(x)
    ax.plot(x, y, color=MARINHO, lw=1.8)
    ax.fill_between(x, y, where=x <= -crit, color=AMBAR, alpha=.85, lw=0)
    ax.fill_between(x, y, where=x >= crit, color=AMBAR, alpha=.85, lw=0)
    ax.fill_between(x, y, where=(x > -crit) & (x < crit), color=TURQUESA, alpha=.12, lw=0)
    for c in (-crit, crit):
        ax.axvline(c, color=AMBAR, lw=1, ls="--")
    fora = abs(est) > lim
    xe = np.sign(est) * (lim * 0.97) if fora else est
    ax.annotate("", xy=(xe, 0), xytext=(xe, d.pdf(0) * 0.62),
                arrowprops=dict(arrowstyle="-|>", color=MARINHO, lw=2))
    rot = f"observado {est:.2f}".replace(".", ",") + (" →" if fora and est > 0 else "")
    ax.text(xe, d.pdf(0) * 0.66, rot, ha="right" if xe > 0 else "left", va="bottom", fontsize=9 if not detalhe else 11,
            color=MARINHO, fontweight="bold")
    ax.set_title(titulo, fontsize=10 if not detalhe else 12, color=MARINHO, loc="left")
    ax.set_yticks([]); ax.set_ylim(0, d.pdf(0) * 1.18); ax.set_xlim(-lim, lim)
    ax.spines["left"].set_visible(False); ax.grid(False)
    if detalhe:
        ax.text(-crit, d.pdf(0) * 1.06, f"−{crit:.2f}".replace(".", ","), ha="center", fontsize=10, color="#8a5a00")
        ax.text(crit, d.pdf(0) * 1.06, f"+{crit:.2f}".replace(".", ","), ha="center", fontsize=10, color="#8a5a00")
        ax.text(0, d.pdf(0) * 0.35, "não rejeita H0\n95% da área", ha="center", fontsize=11, color=MARINHO)
        ax.text(-crit - 0.9, d.pdf(0) * 0.22, "rejeita H0\nα/2 = 2,5%", ha="center", fontsize=10, color="#8a5a00")
        ax.text(crit + 0.9, d.pdf(0) * 0.22, "rejeita H0\nα/2 = 2,5%", ha="center", fontsize=10, color="#8a5a00")
        ax.set_xlabel("estatística do teste, se H0 fosse verdadeira (z)")


ROT_BASE = {"vigitel2024": "Vigitel 2024", "pns2019": "PNS 2019", "xuzhou": "China", "argentina": "Argentina",
            "turquia": "Turquia", "japao": "Japão", "pns2019 + vigitel2024": "PNS × Vigitel", "pns2019 × vigitel2024": "PNS × Vigitel"}


def main():
    estilo()
    out = caminhos.saida("006")
    T = testes()
    salva_csv(T.round(6), out / "tabelas" / "testes_apresentacao.csv")

    # 1. um teste explicado: H3.1, Vigitel, tela digital
    r = T[(T.hipotese == "H3.1")].iloc[0]
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    desenha(ax, r.estatistica, r.gl, f"H3.1 · Vigitel 2024 · H0: RP = 1 · α = 0,05 bilateral · p Holm {formata_p(r.p_holm)}")
    salva(fig, out / "figuras" / "teste_explicado.png")

    # 2. painel: um mini-gráfico por teste t/z confirmatório
    n = len(T)
    cols = 4
    linhas = int(np.ceil(n / cols))
    fig, axs = plt.subplots(linhas, cols, figsize=(12, 2.35 * linhas))
    for ax, r in zip(np.ravel(axs), T.itertuples()):
        base = ROT_BASE.get(str(r.base), str(r.base))
        cor = "rejeita" if r.decisao == "rejeita H0" else "não rejeita"
        desenha(ax, r.estatistica, r.gl, f"{r.hipotese} · {base}\n{cor} H0 · p Holm {formata_p(r.p_holm)}", detalhe=False)
        ax.set_xticks([-4, -2, 0, 2, 4]); ax.tick_params(labelsize=8)
    for ax in np.ravel(axs)[n:]:
        ax.axis("off")
    fig.tight_layout()
    salva(fig, out / "figuras" / "testes_painel.png")

    # 3. confundimento por idade na PNS: % tela ≥ 3 h e % problema de sono, por faixa etária (com peso)
    pns = pd.read_parquet(caminhos.processado("pns2019"),
                          columns=["faixa_etaria", "tela_digital_cat", "problema_sono_freq", "peso"]).dropna()
    fx = ["18-29", "30-44", "45-59", "60+"]
    g = pns.groupby("faixa_etaria")
    tela = [100 * np.average(g.get_group(f).tela_digital_cat.eq(2), weights=g.get_group(f).peso) for f in fx]
    sono = [100 * np.average(g.get_group(f).problema_sono_freq, weights=g.get_group(f).peso) for f in fx]
    salva_csv(pd.DataFrame({"faixa_etaria": fx, "pct_tela_3h": tela, "pct_problema_sono": sono}).round(2),
              out / "tabelas" / "confundimento_idade_pns.csv")
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    ax.plot(fx, tela, marker="o", lw=2.4, color=TURQUESA, label="usa tela digital 3 h ou mais por dia")
    ax.plot(fx, sono, marker="s", lw=2.4, color=AMBAR, label="problema de sono em mais da metade dos dias")
    for xs, ys, cor in ((fx, tela, TURQUESA), (fx, sono, "#8a5a00")):
        for xi, yi in zip(xs, ys):
            ax.text(xi, yi + 1.4, f"{yi:.0f}%", ha="center", fontsize=10, color=cor, fontweight="bold")
    ax.set_ylabel("% dos adultos (com peso amostral)"); ax.set_xlabel("faixa etária (anos)")
    ax.set_ylim(0, max(tela + sono) * 1.25)
    ax.set_title("PNS 2019: quem usa mais tela é mais jovem, e os jovens relatam menos problema de sono",
                 fontsize=11, color=MARINHO, loc="left")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2)
    salva(fig, out / "figuras" / "confundimento_idade.png")
    # 4. quanto cada fator explica do sono: R² único (quanto o R² cai se o fator sai do modelo), com peso
    dec = decomposicao_r2()
    salva_csv(dec.round(6), out / "tabelas" / "decomposicao_r2.csv")
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2), sharey=False)
    for ax, (base, sub) in zip(axs, dec.groupby("base", sort=False)):
        sub = sub.sort_values("r2_unico_pct")
        cores = [AMBAR if f == "tela" else MARINHO for f in sub.fator]
        ax.barh(sub.rotulo, sub.r2_unico_pct, color=cores)
        for y, v in enumerate(sub.r2_unico_pct):
            ax.text(v, y, f" {v:.2f}%".replace(".", ","), va="center", fontsize=10, color=MARINHO)
        ax.set_title(f"{ROT_BASE[base]} · {sub.desfecho.iloc[0]}", fontsize=11, color=MARINHO, loc="left")
        ax.set_xlabel("% da variação do sono explicada só por este fator")
        ax.set_xlim(0, sub.r2_unico_pct.max() * 1.35); ax.grid(axis="y", visible=False)
    fig.tight_layout()
    salva(fig, out / "figuras" / "decomposicao_r2.png")
    # 5. Brasil no mundo: correlação por base, Brasil em destaque, eixo até +1, combinados em negrito (sem losango)
    brasil_no_mundo(out)
    print(T[["hipotese", "base", "tipo", "estatistica", "gl", "p_holm", "decisao"]].to_string())
    print(dec.to_string())


def brasil_no_mundo(out):
    e = _csv("004", "efeitos_por_base")
    m = _csv("004", "meta_analise").set_index("analise")
    nome = {"pns2019": "PNS 2019", "vigitel2024": "Vigitel 2024", "argentina": "Argentina · tela por dia",
            "japao": "Japão · celular antes de dormir", "xuzhou": "China · uso problemático",
            "turquia": "Turquia · doomscrolling"}
    linhas = []
    for b in ["pns2019", "vigitel2024"]:
        r = e[e.base == b].iloc[0]
        linhas.append(("Brasil", nome[b], r.rho, r.rho_ic_inf, r.rho_ic_sup, False))
    br = m.loc["Brasil (PNS + Vigitel)"]
    linhas.append(("Brasil", "Brasil combinado", br.rho, br.rho_ic_inf, br.rho_ic_sup, True))
    for b in ["argentina", "japao", "xuzhou", "turquia"]:
        r = e[e.base == b].iloc[0]
        linhas.append(("mundo", nome[b], r.rho, r.rho_ic_inf, r.rho_ic_sup, False))
    rm = m.loc["resto do mundo (4 bases)"]
    linhas.append(("mundo", "Resto do mundo combinado", rm.rho, rm.rho_ic_inf, rm.rho_ic_sup, True))
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ys = np.arange(len(linhas))[::-1]
    for y, (grupo, rot, rho, lo, hi, comb) in zip(ys, linhas):
        cor = AMBAR if grupo == "Brasil" else MARINHO
        ax.plot([lo, hi], [y, y], color=cor, lw=3.2 if comb else 2, solid_capstyle="round")
        ax.plot(rho, y, marker="s" if comb else "o", ms=10 if comb else 8, color=cor,
                markeredgecolor=MARINHO if comb else cor, markeredgewidth=1.4)
        ax.text(max(hi, 0) + 0.02, y, f"{rho:.2f}".replace(".", ",").replace("-", "−"), va="center", fontsize=11 if comb else 10,
                color=MARINHO, fontweight="bold" if comb else "normal")
    ax.set_yticks(ys, [l[1] for l in linhas])
    for t, l in zip(ax.get_yticklabels(), linhas):
        t.set_fontweight("bold" if l[5] else "normal")
    ax.axvline(0, color=COR_NEUTRA, lw=1)
    ax.axvspan(0.5, 1.0, color="#E5E6E7", alpha=.5, lw=0)
    ax.text(0.75, ys.max() + 0.3, "correlação forte\n(nenhuma base chega aqui)", ha="center", va="top", fontsize=9.5, color=COR_NEUTRA)
    ax.set_xlim(-0.15, 1.0)
    ax.set_xlabel("correlação de Spearman (0 = nenhuma relação, +1 = relação perfeita); positivo = mais tela, pior sono")
    ax.grid(axis="y", visible=False)
    salva(fig, out / "figuras" / "brasil_no_mundo.png")


FATORES = {"tela": ["tela_1", "tela_2"], "idade": ["idade"], "sexo": ["sexo"], "escolaridade": ["esc_1", "esc_2"]}
ROT_FATOR = {"tela": "tempo de tela", "idade": "idade", "sexo": "sexo", "escolaridade": "escolaridade"}


def _r2_ponderado(y, X, w):
    X1 = np.column_stack([np.ones(len(y)), X]) if X.size else np.ones((len(y), 1))
    sw = np.sqrt(w)
    b, *_ = np.linalg.lstsq(X1 * sw[:, None], y * sw, rcond=None)
    res = y - X1 @ b
    ybar = np.average(y, weights=w)
    return 1 - np.sum(w * res ** 2) / np.sum(w * (y - ybar) ** 2)


def decomposicao_r2() -> pd.DataFrame:
    """R² completo e R² único de cada fator (R²_completo − R²_sem o fator), regressão linear ponderada."""
    L = []
    for base, y_nome, rot in [("vigitel2024", "insonia_idx", "índice de insônia (0–12)"),
                              ("pns2019", "problema_sono_ord", "problema de sono (0–3)")]:
        d = pd.read_parquet(caminhos.processado(base),
                            columns=[y_nome, "tela_digital_cat", "idade", "sexo", "escolaridade3", "peso"]).dropna()
        d["tela_1"], d["tela_2"] = (d.tela_digital_cat == 1).astype(float), (d.tela_digital_cat == 2).astype(float)
        d["esc_1"], d["esc_2"] = (d.escolaridade3 == 1).astype(float), (d.escolaridade3 == 2).astype(float)
        y, w = d[y_nome].to_numpy(float), (d.peso / d.peso.mean()).to_numpy(float)
        todas = [c for cols in FATORES.values() for c in cols]
        r2c = _r2_ponderado(y, d[todas].to_numpy(float), w)
        for f, cols in FATORES.items():
            resto = [c for c in todas if c not in cols]
            r2u = r2c - _r2_ponderado(y, d[resto].to_numpy(float), w)
            r2s = _r2_ponderado(y, d[cols].to_numpy(float), w)
            L.append(dict(base=base, desfecho=rot, n=len(d), fator=f, rotulo=ROT_FATOR[f], r2_completo=r2c,
                          r2_unico=r2u, r2_unico_pct=100 * r2u, r2_sozinho=r2s, r2_sozinho_pct=100 * r2s))
    return pd.DataFrame(L)


if __name__ == "__main__":
    main()
