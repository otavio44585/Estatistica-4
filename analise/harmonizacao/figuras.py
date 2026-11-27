"""Descritiva da spec 001: distribuição da exposição e dos desfechos, com peso amostral nos inquéritos.

Gera resultados/001/tabelas/prevalencias.csv e as figuras de resultados/001/figuras/.
"""
import numpy as np
import pandas as pd

from analise.comum import caminhos
from analise.comum.estatistica import salva_csv
from analise.comum.graficos import COR_PAIS, NOME_BASE, PAIS_BASE, estilo, salva, plt

INQ = ["pns2019", "vigitel2024", "nhanes0506"]
ROT_TELA = {0: "não usa ou < 1 h", 1: "1 a < 3 h", 2: "≥ 3 h"}


def prop_ponderada(s: pd.Series, w: pd.Series) -> pd.Series:
    ok = s.notna() & w.notna()
    return (w[ok].groupby(s[ok]).sum() / w[ok].sum()).sort_index()


def main():
    estilo()
    out = caminhos.saida("001")
    dados = {b: pd.read_parquet(caminhos.processado(b)) for b in INQ}
    linhas = []
    for b, df in dados.items():
        for var in ["tela_digital_cat", "tela_tv_cat"]:
            pp, pb = prop_ponderada(df[var], df.peso), df[var].value_counts(normalize=True).sort_index()
            for k in pp.index:
                linhas.append(dict(base=b, variavel=var, categoria=ROT_TELA[int(k)], n=int((df[var] == k).sum()),
                                   pct_sem_peso=100 * pb[k], pct_com_peso=100 * pp[k]))
        for var in ["dif_adormecer_freq", "problema_sono_freq"]:
            if var in df:
                ok = df[var].notna()
                linhas.append(dict(base=b, variavel=var, categoria="sim", n=int(df.loc[ok, var].sum()),
                                   pct_sem_peso=100 * df.loc[ok, var].mean(),
                                   pct_com_peso=100 * np.average(df.loc[ok, var], weights=df.loc[ok, "peso"])))
    prev = pd.DataFrame(linhas).round(2)
    salva_csv(prev, out / "tabelas" / "prevalencias.csv")

    # Figura 1: distribuição ponderada da tela digital nas três bases de inquérito
    fig, ax = plt.subplots(figsize=(7, 3.2))
    sub = prev[prev.variavel == "tela_digital_cat"]
    esquerda = np.zeros(len(INQ))
    tons = ["#CFE8DF", "#6FC2A6", "#00694C"]
    for cat, cor in zip(ROT_TELA.values(), tons):
        v = [sub[(sub.base == b) & (sub.categoria == cat)].pct_com_peso.sum() for b in INQ]
        ax.barh([NOME_BASE[b] for b in INQ], v, left=esquerda, color=cor, label=cat, edgecolor="white")
        for i, (x0, w) in enumerate(zip(esquerda, v)):
            if w > 6:
                ax.text(x0 + w / 2, i, f"{w:.0f}%", ha="center", va="center", fontsize=9,
                        color="white" if cor == tons[2] else "black")
        esquerda += v
    ax.set_xlim(0, 100); ax.set_xlabel("% da população adulta (com peso amostral)")
    ax.set_title("Tempo diário de computador, tablet ou celular no lazer")
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.28)); ax.grid(axis="y", visible=False)
    ax.invert_yaxis()
    salva(fig, out / "figuras" / "exposicao_tela_digital.png")

    # Figura 2: índice de insônia (0-12) no Vigitel e no NHANES, distribuição ponderada
    fig, ax = plt.subplots(figsize=(7, 3.2))
    for b, desloc in [("vigitel2024", -0.2), ("nhanes0506", 0.2)]:
        df = dados[b]
        p = prop_ponderada(df.insonia_idx, df.peso) * 100
        ax.bar(p.index + desloc, p.values, width=0.4, color=COR_PAIS[PAIS_BASE[b]], label=NOME_BASE[b])
    ax.set_xticks(range(13)); ax.set_xlabel("índice de insônia (soma dos 3 sintomas, 0 = nunca, 12 = sempre)")
    ax.set_ylabel("% (com peso)"); ax.set_title("Distribuição do índice de insônia"); ax.legend()
    salva(fig, out / "figuras" / "indice_insonia.png")
    escreve_resumo(out, prev)
    print(prev.to_string())


def escreve_resumo(out, prev):
    """resultados/001/RESUMO.md gerado a partir das tabelas (nenhum número digitado)."""
    ns = pd.read_csv(out / "tabelas" / "n_por_base.csv", sep=";", encoding="utf-8-sig")
    final = ns[ns.etapa.str.startswith("salvo")].set_index("base").n
    pt = lambda x: f"{x:.1f}".replace(".", ",")
    milhar = lambda x: f"{int(x):,}".replace(",", ".")
    L = ["# 001 — Resumo dos dados harmonizados", "",
         "Gerado por `analise/harmonizacao/figuras.py` a partir de `resultados/001/tabelas/`.", "",
         "## n final por base", "", "| Base | n |", "|---|---|"]
    L += [f"| {NOME_BASE[b]} | {milhar(n)} |" for b, n in final.items()]
    L += ["", "## Exposição e desfechos nos inquéritos (% com peso amostral)", "",
          "| Base | Variável | Categoria | n | % sem peso | % com peso |", "|---|---|---|---|---|---|"]
    for r in prev.itertuples():
        L.append(f"| {NOME_BASE[r.base]} | `{r.variavel}` | {r.categoria} | {milhar(r.n)} | {pt(r.pct_sem_peso)} | {pt(r.pct_com_peso)} |")
    L += ["", "![Tela digital por base](figuras/exposicao_tela_digital.png)", "",
          "![Índice de insônia](figuras/indice_insonia.png)", "",
          "Equivalência de cada variável entre as bases: `resultados/001/tabelas/equivalencia.csv`. "
          "Descritiva completa (média, DP, mínimo, máximo): `resultados/001/tabelas/descritiva.csv`."]
    (out / "RESUMO.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
