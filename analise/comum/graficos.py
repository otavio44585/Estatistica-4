"""Estilo único dos gráficos (todas as specs usam as mesmas cores por país)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Paleta Okabe-Ito (segura para daltonismo). Brasil sempre em destaque.
COR_PAIS = {
    "Brasil": "#009E73",
    "EUA": "#0072B2",
    "China": "#D55E00",
    "Argentina": "#56B4E9",
    "Turquia": "#CC79A7",
    "Japão": "#E69F00",
    "Combinado": "#000000",
}
COR_NEUTRA = "#7F7F7F"
NOME_BASE = {
    "pns2019": "PNS 2019 (Brasil)",
    "vigitel2024": "Vigitel 2024 (Brasil)",
    "nhanes0506": "NHANES 2005-06 (EUA)",
    "xuzhou": "Xuzhou (China)",
    "argentina": "Pérez-Chada (Argentina)",
    "turquia": "Doomscrolling (Turquia)",
    "japao": "Okajima (Japão)",
}
PAIS_BASE = {"pns2019": "Brasil", "vigitel2024": "Brasil", "nhanes0506": "EUA", "xuzhou": "China",
             "argentina": "Argentina", "turquia": "Turquia", "japao": "Japão"}


def estilo():
    plt.rcParams.update({
        "figure.dpi": 110, "savefig.dpi": 150, "savefig.bbox": "tight",
        "font.size": 10, "axes.titlesize": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25, "legend.frameon": False,
    })


def salva(fig, caminho):
    fig.savefig(caminho)
    plt.close(fig)
