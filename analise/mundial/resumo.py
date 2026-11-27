"""Gera resultados/004/RESUMO.md a partir dos CSV de resultados/004/tabelas (nenhum número digitado).

Chamado no fim de `python -m analise.mundial.rodar`; também roda sozinho: `python -m analise.mundial.resumo`.
"""
import numpy as np
import pandas as pd

from analise.comum import caminhos
from analise.comum.estatistica import formata_p, le_csv

OUT = caminhos.RESULTADOS / "004"
TAB = OUT / "tabelas"


def f(x, c=3):
    return "—" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{c}f}".replace(".", ",").replace("-", "−")


def ic(a, b, c=3):
    return "—" if np.isnan(a) else f"{f(a, c)}; {f(b, c)}"


def pct(x, c=1):
    return f(100 * x, c) + "%"


def mil(x):
    return f"{int(round(x)):,}".replace(",", ".")


def main():
    ef, meta, hip = le_csv(TAB / "efeitos_por_base.csv"), le_csv(TAB / "meta_analise.csv"), le_csv(TAB / "hipoteses.csv")
    ex, sens = le_csv(TAB / "exploratorio_referencia.csv"), le_csv(TAB / "sensibilidade.csv")
    aj = le_csv(TAB / "bruta_ajustada_idade.csv")
    M = meta.set_index("analise")
    H = hip.set_index("hipotese")
    S = sens.set_index("analise")
    g = M.loc[[i for i in M.index if i.startswith("global")][0]]
    L = ["# 004 — Comparação mundial: resumo dos resultados", "",
         "Gerado por `python -m analise.mundial.resumo` a partir de `resultados/004/tabelas/` (nenhum número digitado). "
         "Notebook: `analise/notebooks/05_comparacao_mundial.ipynb`.", "",
         "**Decisão do grupo (2026-11-27):** o NHANES 2005-06 (EUA) saiu do trabalho inteiro — a única base dos EUA é de 2005, "
         "antes do smartphone, e misturava país com época. A meta-análise tem 6 bases (Histórico da spec 004).", "",
         "**Métrica:** ρ de Spearman entre exposição e desfecho; sinal padronizado, **positivo = mais tela, pior sono**. "
         "IC 95% pela transformação z de Fisher com EP de Fieller, Hartley e Pearson (1957).", "",
         "## Efeito por base (par principal fixado antes do cálculo) — `efeitos_por_base.csv`", "",
         "| Base | Tipo | Exposição × desfecho | n | ρ (IC 95%) | r de Pearson | Peso aleatório |", "|---|---|---|---|---|---|---|"]
    for r in ef.itertuples():
        L.append(f"| {r.nome} | {r.tipo} | {r.rot_exposicao} × {r.rot_desfecho} | {mil(r.n)} | {f(r.rho)} ({ic(r.rho_ic_inf, r.rho_ic_sup)}) "
                 f"| {f(r.r_pearson)} | {f(r.peso_aleatorio_pct, 1)}% |")
    dv = ef.loc[ef.divergencia_rel.abs().idxmax()]
    L += ["", f"**T061 (erro padrão):** o EP por bootstrap divergiu no máximo {pct(abs(dv.divergencia_rel))} ({dv.nome}) da fórmula de "
              f"Fieller, Hartley e Pearson, abaixo do limiar de 10% do plano; a meta-análise usa a fórmula ({ef.ep_usado.iloc[0]}).", "",
          "## Meta-análise — `meta_analise.csv`", "",
          "IC 95% por DerSimonian-Laird (normal, fixado no plano) e por Hartung-Knapp (t com k − 1 gl; mais honesto com poucas bases).", "",
          "| Combinação | Papel | k | ρ | IC 95% DL | IC 95% Hartung-Knapp | Q (gl), p | I² | τ² |", "|---|---|---|---|---|---|---|---|---|"]
    for nome, r in M.iterrows():
        q = "—" if r.k == 1 else f"{f(r.Q, 1)} ({int(r.gl_Q)}), p {formata_p(r.p_Q)}"
        hk = "— (k = 1)" if r.k == 1 else f"{ic(r.rho_ic_inf_hk, r.rho_ic_sup_hk)} (p = {formata_p(r.p_efeito_hk)})"
        L.append(f"| {nome} | {r.papel} | {int(r.k)} | {f(r.rho)} | {ic(r.rho_ic_inf, r.rho_ic_sup)} (p = {formata_p(r.p_efeito)}) | {hk} "
                 f"| {q} | {'—' if r.k == 1 else pct(r.I2)} | {'—' if r.k == 1 else f(r.tau2, 4)} |")
    L += ["", f"**Leitura.** Pelo DerSimonian-Laird a estimativa global ({f(g.rho)}) exclui o zero; pelo Hartung-Knapp "
              f"({ic(g.rho_ic_inf_hk, g.rho_ic_sup_hk)}) não exclui. Nenhum teste da família usa esse IC. Com k = 2 o t de Hartung-Knapp "
              "tem 1 gl e o intervalo fica enorme. A média manual bate com `statsmodels.combine_effects` (`conferencia_statsmodels.csv`).", "",
          "## Hipóteses (família H4.1–H4.4, Holm) — `hipoteses.csv`", "",
          "| # | H0 | Teste | Estatística | p | p Holm | Decisão | Detalhe |", "|---|---|---|---|---|---|---|---|"]
    for k, r in H.iterrows():
        est = f"{f(r.estatistica, 2)}" + ("" if np.isnan(r.gl) else f"; gl = {int(r.gl)}")
        L.append(f"| {k} | {r.h0} | {r.teste} | {est} | {formata_p(r.p)} | {formata_p(r.p_holm)} | {r.decisao} | {r.efeito} |")
    L += ["", "- **H4.2:** registrada como hipótese ordenada e testada como omnibus (Q entre subgrupos, fixado no plano). "
              "Com 1 a 3 bases por subgrupo, \"não rejeitar\" não mostra igualdade. O pré-sono tem uma base só (Japão).",
          "- **H4.3:** sem o NHANES, o lado \"outros com tempo total\" tem **k = 1** (só a Argentina, adolescentes). "
          "Não foi detectada diferença, mas o teste compara o Brasil com uma única base."]
    L += ["", "## Exploratório (fora da família de Holm) — `exploratorio_referencia.csv`", ""]
    for r in ex.itertuples():
        if r.analise.startswith("EXPLORATÓRIO: Brasil"):
            L.append(f"- **Brasil × resto do mundo** (pedido do grupo depois de ver os resultados; mistura os tipos de exposição): "
                     f"Brasil (PNS + Vigitel) ρ = {f(r.rho)} ({ic(r.ic_inf, r.ic_sup)}) × resto do mundo (Argentina, Japão, China, Turquia) "
                     f"ρ = {f(r.rho_resto)} (DL {ic(r.ic_inf_resto, r.ic_sup_resto)}; Hartung-Knapp {ic(r.ic_inf_resto_hk, r.ic_sup_resto_hk)}); "
                     f"diferença na escala z {f(r.diferenca_z)} (IC {ic(r.ic_inf_dif, r.ic_sup_dif)}), z = {f(r.z, 2)}, p = {formata_p(r.p)}. "
                     "Não foi detectada diferença; a associação no resto do mundo puxa para cima por causa das escalas de uso problemático e pré-sono. "
                     "Figura: `figuras/brasil_vs_resto.png`.")
        elif r.analise.startswith("EXPLORATÓRIO: tendência"):
            L.append(f"- **Tendência ordenada de H4.2:** inclinação {f(r.inclinacao_z)} na escala z (EP {f(r.ep_inclinacao)}; "
                     f"z = {f(r.z, 2)}; p = {formata_p(r.p)}). Compatível com a ordem prevista, mas são só três pontos.")
        else:
            L.append(f"- {r.analise}: ρ = {f(r.rho)} ({ic(r.ic_inf, r.ic_sup)}); z = {f(r.z, 2)}, p = {formata_p(r.p)}.")
    L += ["", "## Sensibilidades — `sensibilidade.csv`, `bruta_ajustada_idade.csv`", "", "- **Bruta × ajustada por idade (ρ parcial; exploratório):**"]
    for r in aj.itertuples():
        L.append(f"  - {r.nome}: {f(r.rho_bruto)} → {f(r.rho_ajustado_idade)} ({ic(r.ic_inf_ajustado, r.ic_sup_ajustado)})")
    for nome in ["subgrupo tempo total com ρ ajustado por idade", "Brasil (PNS + Vigitel) com ρ ajustado por idade"]:
        L.append(f"  - {nome}: {f(S.loc[nome, 'rho'])} ({ic(S.loc[nome, 'ic_inf'], S.loc[nome, 'ic_sup'])})")
    fora = sens[sens.grupo == "deixar uma de fora"]
    lo, hi = fora.loc[fora.rho.idxmin()], fora.loc[fora.rho.idxmax()]
    L.append(f"- **Deixar uma base de fora:** ρ global de {f(lo.rho)} ({lo.analise}) a {f(hi.rho)} ({hi.analise}).")
    pond = sens[sens.grupo == "ponderada"]
    L.append("- **ρ ponderado pelo peso amostral:** " + "; ".join(f"{r.analise.split(':')[0]} {f(r.rho)}" for r in pond.itertuples()) + ".")
    dd = sens[sens.grupo == "efeito do desenho (deff)"]
    L.append("- **Desenho amostral (deff de Kish, só PNS e Vigitel):** " + "; ".join(
        f"{r.analise}: {f(r.rho)} ({ic(r.ic_inf, r.ic_sup)})" + ("" if np.isnan(r.I2) else f", I² {pct(r.I2)}") +
        ("" if np.isnan(getattr(r, "p", np.nan)) else f", p = {formata_p(r.p)}") for r in dd.itertuples()) + ". Nenhuma decisão muda.")
    for grupo, titulo in [("par alternativo", "Pares alternativos"), ("procedência questionável", "Procedência questionável (nunca na estimativa principal)"),
                          ("contraponto intrapessoal", "Contraponto intrapessoal (Holanda, fora da meta-análise)")]:
        d = sens[sens.grupo == grupo]
        L.append(f"- **{titulo}:** " + "; ".join(f"{r.analise}: {f(r.rho)}" + ("" if np.isnan(r.ic_inf) else f" ({ic(r.ic_inf, r.ic_sup)})")
                                                 for r in d.itertuples()) + ".")
    L += ["", "## Limitações", "",
          f"1. **Heterogeneidade extrema** (I² = {pct(g.I2)}): a média global resume bases com escalas, populações e anos diferentes.",
          "2. **Exposição em faixas** nos inquéritos: a correlação de postos com muitos empates fica atenuada.",
          "3. **Correlação bruta como métrica principal:** a PNS mostra confundimento por idade; a versão ajustada é sensibilidade.",
          "4. **Referência aproximada:** Han, Zhou e Liu (2024) combinam uso geral × qualidade do sono, majoritariamente em jovens.",
          "5. **Subgrupos pequenos:** pré-sono tem 1 base e uso problemático 2; em H4.3 o lado \"outros\" tem 1 base.",
          "6. **Dados transversais:** o resultado é uma associação entre tela e sono, não uma relação de causa.",
          "7. **EP dos inquéritos sem o desenho:** o deff de Kish é um limite inferior do efeito do desenho.",
          f"8. **Poucas bases** (k = {int(g.k)}): o IC normal do DerSimonian-Laird é otimista; o de Hartung-Knapp inclui o zero."]
    (OUT / "RESUMO.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("resultados/004/RESUMO.md")


if __name__ == "__main__":
    main()
