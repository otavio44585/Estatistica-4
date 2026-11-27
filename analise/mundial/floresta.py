"""T067 — Gráfico de floresta (ρ de Spearman, IC 95%), Brasil em destaque."""
import numpy as np
import matplotlib.pyplot as plt

from analise.comum.graficos import estilo, salva, COR_PAIS, COR_NEUTRA
from analise.mundial.pares import TIPOS


def _diamante(ax, y, c, lo, hi, cor, alt=0.28):
    ax.fill([lo, c, hi, c], [y, y + alt, y, y - alt], color=cor, zorder=3)


def bruta_ajustada(aj, caminho):
    """ρ bruto × ρ parcial ajustado por idade, por base."""
    estilo()
    fig, ax = plt.subplots(figsize=(7.6, 0.5 * len(aj) + 1.2))
    for i, r in enumerate(aj.itertuples()):
        y = len(aj) - i
        cor = COR_PAIS.get(r.pais, COR_NEUTRA)
        ax.plot([r.ic_inf_bruto, r.ic_sup_bruto], [y + 0.13] * 2, color=cor, lw=1.4, alpha=0.55)
        ax.scatter([r.rho_bruto], [y + 0.13], marker="o", facecolor="white", edgecolor=cor, s=36, zorder=3,
                   label="bruto" if i == 0 else None)
        ax.plot([r.ic_inf_ajustado, r.ic_sup_ajustado], [y - 0.13] * 2, color=cor, lw=1.6)
        ax.scatter([r.rho_ajustado_idade], [y - 0.13], marker="o", color=cor, s=36, zorder=3,
                   label="ajustado por idade" if i == 0 else None)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_yticks([len(aj) - i for i in range(len(aj))])
    ax.set_yticklabels(aj.nome)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("ρ de Spearman (positivo = mais tela, pior sono)")
    ax.set_title("Bruto × ajustado por idade (ρ parcial), IC 95%", loc="left")
    ax.legend(loc="lower right", fontsize=8)
    salva(fig, caminho)


def desenha(ef, meta, caminho, han=None):
    estilo()
    linhas = []   # (rótulo, tipo de linha, dados)
    for t in TIPOS:
        d = ef[ef.tipo == t]
        if not len(d):
            continue
        linhas.append((t.capitalize(), "cabecalho", None))
        for r in d.itertuples():
            linhas.append((f"{r.nome}  (n = {r.n:,})".replace(",", "."), "base", r))
        m = meta[meta.analise == f"subgrupo: {t}"].iloc[0]
        linhas.append((f"Combinado: {t} (k = {int(m.k)})", "sub", m))
    g = meta[meta.analise.str.startswith("global")].iloc[0]
    linhas.append(("", "branco", None))
    linhas.append((f"Combinado global, efeitos aleatórios (k = {int(g.k)})", "global", g))

    fig, ax = plt.subplots(figsize=(8.6, 0.36 * len(linhas) + 1.4))
    n = len(linhas)
    if han:
        ax.axvspan(han[1], han[2], color=COR_NEUTRA, alpha=0.12, lw=0,
                   label="IC 95% da referência: Han, Zhou e Liu (2024), uso geral, r = 0,28")
    ax.axvline(0, color="black", lw=0.8)
    pesos = ef.peso_aleatorio_pct
    for i, (rot, tipo, r) in enumerate(linhas):
        y = n - i
        if tipo == "base":
            cor = COR_PAIS.get(r.pais, COR_NEUTRA)
            ax.plot([r.rho_ic_inf, r.rho_ic_sup], [y, y], color=cor, lw=1.6)
            ax.scatter([r.rho], [y], s=20 + 3 * r.peso_aleatorio_pct, marker="s", color=cor, zorder=3,
                       edgecolor="black" if r.pais == "Brasil" else "none", linewidth=1.2)
            ax.text(1.02, y, f"{r.rho:.3f} [{r.rho_ic_inf:.3f}; {r.rho_ic_sup:.3f}]".replace(".", ","),
                    transform=ax.get_yaxis_transform(), va="center", fontsize=8.5)
        elif tipo in ("sub", "global"):
            cor = "#444444" if tipo == "sub" else COR_PAIS["Combinado"]
            _diamante(ax, y, r.rho, r.rho_ic_inf, r.rho_ic_sup, cor)
            hk_i, hk_s = getattr(r, "rho_ic_inf_hk", None), getattr(r, "rho_ic_sup_hk", None)
            if tipo == "global" and hk_i is not None and hk_i == hk_i:
                ax.plot([hk_i, hk_s], [y - 0.42, y - 0.42], color=cor, lw=1.0, ls=(0, (3, 2)),
                        label=f"IC 95% de Hartung-Knapp do global: {hk_i:.3f} a {hk_s:.3f}".replace(".", ","))
            ax.text(1.02, y, f"{r.rho:.3f} [{r.rho_ic_inf:.3f}; {r.rho_ic_sup:.3f}]".replace(".", ","),
                    transform=ax.get_yaxis_transform(), va="center", fontsize=8.5, fontweight="bold")
    ax.set_yticks([n - i for i in range(n)])
    ax.set_yticklabels([r for r, _, _ in linhas])
    for lab, (_, tipo, _) in zip(ax.get_yticklabels(), linhas):
        if tipo in ("cabecalho", "global"):
            lab.set_fontweight("bold")
        if tipo == "base" and "Brasil" in lab.get_text():
            lab.set_color(COR_PAIS["Brasil"])
            lab.set_fontweight("bold")
    ax.set_ylim(0.3, n + 0.7)
    ax.set_xlabel("ρ de Spearman (positivo = mais tela, pior sono)")
    ax.grid(axis="y", visible=False)
    ax.set_title("Associação entre uso de tela e sono por base (IC 95%)", loc="left")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, -0.075), fontsize=8)
    salva(fig, caminho)
