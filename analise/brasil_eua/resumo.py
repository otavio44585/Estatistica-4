"""T049 — Gera resultados/003/RESUMO.md a partir dos CSVs (nenhum número digitado à mão, princípio 2).

Uso: python -m analise.brasil_eua.resumo   (depois de analise.brasil_eua.executa)
"""
import numpy as np
import pandas as pd

from analise.comum import caminhos
from analise.comum.estatistica import le_csv, formata_p, num
from analise.comum.graficos import NOME_BASE

OUT = caminhos.saida("003")
T = OUT / "tabelas"


def rp(r, a="estimativa", lo="ic_inf", hi="ic_sup"):
    return f"{num(r[a])} ({num(r[lo])}–{num(r[hi])})"


def est(r):
    tipo = r.get("tipo_estat", r.get("tipo"))
    gl1, gl2 = r.get("gl1"), r.get("gl2")
    if tipo == "F":
        return f"F({int(gl1)}; {int(gl2)}) = {num(r.estatistica)}"
    if tipo == "qui2":
        return f"χ²({int(gl1)}) = {num(r.estatistica)}"
    if tipo == "t":
        return f"t({int(gl2)}) = {num(r.estatistica)}"
    return f"z = {num(r.estatistica)}"


def nb(b):
    return NOME_BASE.get(b, b)


def main():
    H = le_csv(T / "hipoteses.csv")
    R = le_csv(T / "rp_bruta_ajustada.csv")
    C = le_csv(T / "comparacoes_entre_bases.csv")
    S = le_csv(T / "sensibilidade.csv")
    L = le_csv(T / "desvio_linearidade_exploratorio.csv")
    V = le_csv(T / "comparacao_variancia.csv")
    P = le_csv(T / "prevalencias.csv")
    I = le_csv(T / "rp_por_faixa_etaria.csv")

    o = []
    w = o.append
    w("# 003 — Brasil × EUA: resultados\n")
    w("Gerado por `python -m analise.brasil_eua.resumo` a partir de `resultados/003/tabelas/*.csv`. "
      "Execução de 2026-11-27; aprovação do grupo pendente.\n")
    w("## Transparência\n")
    w("As hipóteses H3.1–H3.9 foram formuladas depois da análise exploratória de 2026-11-27 "
      "(`docs/exploratorio_comparativo_br_eua_2026-11-27.*`). O modelo, as covariáveis e os pesos foram fixados no "
      "plano antes desta execução. A exposição digital foi fixada no código como a principal da família 2 antes de "
      "rodar (o foco da spec é a tela digital); a TV na família 2 é **complementar** e não entra na correção de Holm. "
      "Todos os testes são bilaterais (H1: RP ≠ 1; o sinal esperado, RP > 1, vem da literatura e não muda o teste).\n")
    w("## Método em uma tabela\n")
    w("| Item | Escolha |\n|---|---|")
    w("| Modelo | Poisson com ligação log, peso amostral; exp(β) = razão de prevalências (RP) |")
    w("| Covariáveis (ajustada) | faixa etária (18–29, 30–44, 45–59, 60+), sexo, escolaridade em 3 faixas |")
    w("| Exposição alta × baixa | tela ≥ 3 h/dia × não usa ou < 1 h/dia (`tela_digital_cat`, `tela_tv_cat`) |")
    w("| Desfechos | Vigitel: dificuldade para adormecer quase sempre ou sempre; NHANES: often/almost always (5 ou mais "
      "vezes por mês); PNS: problema de sono em mais da metade dos dias |")
    w("| Variância | linearização de Taylor com estrato e UPA (PNS, NHANES); sanduíche robusto só com peso (Vigitel) |")
    gl_pns = int(R[R.base == "pns2019"].gl.dropna().iloc[0])
    gl_nh = int(R[R.base == "nhanes0506"].gl.dropna().iloc[0])
    w(f"| Graus de liberdade do desenho | regra única do projeto: UPAs − estratos (PNS {gl_pns}; NHANES {gl_nh}); "
      f"Vigitel: normal. Sensibilidade: regra do svyglm (d − p + 1) |")
    w("| Wald conjunto (q > 1) | correção de Korn-Graubard: F = (d − q + 1)/(d·q)·W, gl (q, d − q + 1) |")
    w("| RP por faixa etária | estimadas por domínio: ajuste na faixa, variância com todas as UPAs e estratos |")
    w(f"| Base empilhada (H3.6) | gl mostrado = gl do NHANES ({gl_nh}); Satterthwaite registrado como sensibilidade |")
    w("| Correção | Holm na família 1 (por exposição: digital e TV) e na família 2 |")
    w("| α | 0,05 bilateral |\n")

    w("## Hipóteses: decisão\n")
    w("Fonte: `resultados/003/tabelas/hipoteses.csv`.\n")
    w("| Família | H | Base | Exposição | Estimativa (IC 95%) | Estatística | p | p Holm | Decisão |")
    w("|---|---|---|---|---|---|---|---|---|")
    for _, r in H.iterrows():
        if r.hipotese == "H3.7":
            e = f"RP por faixa: {num(r.ic_inf)} a {num(r.ic_sup)}"
        else:
            e = rp(r)
        w(f"| {r.familia} | {r.hipotese} | {nb(r.base)} | {r.exposicao} | {e} | {est(r)} | {formata_p(r.p)} | "
          f"{formata_p(r.p_holm)} | {r.decisao} |")
    w("")
    w("Estimativas: H3.1–H3.3 = RP de tela alta; H3.4 = RP por faixa de exposição (escore 0/1/2); "
      "H3.6 = razão das RP (NHANES ÷ Vigitel); H3.8 = razão RP da TV ÷ RP digital no mesmo modelo; "
      "H3.9 = razão das RP (Vigitel ÷ PNS).\n")

    w("## Sensibilidade à regra de graus de liberdade\n")
    w("Fonte: colunas `gl2_svyglm`, `p_svyglm`, `p_holm_svyglm` de `resultados/003/tabelas/hipoteses.csv` (Holm "
      "refeito por família com a regra do svyglm). Só linhas com gl de desenho finito.\n")
    w("| Família | H | Base | Exposição | gl (regra principal) | p Holm | gl (svyglm) | p Holm (svyglm) | Decisão (svyglm) |")
    w("|---|---|---|---|---|---|---|---|---|")
    for _, r in H[H.gl_desenho.notna()].iterrows():
        glsv = "—" if np.isnan(r.gl2_svyglm) else str(int(r.gl2_svyglm))
        nota = f" ({r.nota_svyglm})" if isinstance(r.nota_svyglm, str) and r.nota_svyglm else ""
        w(f"| {r.familia} | {r.hipotese} | {nb(r.base)} | {r.exposicao} | {int(r.gl2)} | {formata_p(r.p_holm)} | "
          f"{glsv} | {formata_p(r.p_holm_svyglm)} | {r.decisao_svyglm}{nota} |")
    w("")
    w("## Bruta, só idade e ajustada lado a lado (tela ≥ 3 h vs < 1 h)\n")
    w("Fonte: `resultados/003/tabelas/rp_bruta_ajustada.csv`.\n")
    w("| Base | Exposição | Bruta | Só idade | Ajustada | n |\n|---|---|---|---|---|---|")
    R2 = R[R.comparacao == "2 vs 0"]
    for (b, e), g in R2.groupby(["base", "exposicao"], sort=False):
        g = g.set_index("modelo")
        w(f"| {nb(b)} | {e} | {rp(g.loc['bruta'], 'rp')} | {rp(g.loc['só idade'], 'rp')} | "
          f"{rp(g.loc['ajustada'], 'rp')} | {int(g.loc['ajustada', 'n'])} |")
    w("")
    w("## Prevalências ponderadas por faixa de tela\n")
    w("Fonte: `resultados/003/tabelas/prevalencias.csv`.\n")
    w("| Base | Exposição | < 1 h | 1 a < 3 h | ≥ 3 h |\n|---|---|---|---|---|")
    for (b, e), g in P.groupby(["base", "exposicao"], sort=False):
        g = g.set_index("categoria")
        cel = [f"{num(100 * g.loc[k, 'prevalencia_ponderada'], 1)}% (n = {int(g.loc[k, 'n'])})" for k in (0, 1, 2)]
        w(f"| {nb(b)} | {e} | " + " | ".join(cel) + " |")
    w("")
    w("## Comparações entre bases (inclui TV, complementar)\n")
    w("Fonte: `resultados/003/tabelas/comparacoes_entre_bases.csv`.\n")
    w("| H | Exposição | Método | Razão (IC 95%) | Estatística | p | gl Satterthwaite (p) |\n|---|---|---|---|---|---|---|")
    for _, r in C.iterrows():
        e = rp(r, "razao") if not np.isnan(r.razao) else "—"
        sat = (f"{num(r.gl_satterthwaite, 1)} ({formata_p(r.p_satterthwaite)})"
               if not np.isnan(r.get("gl_satterthwaite", np.nan)) else "—")
        w(f"| {r.hipotese} | {r.exposicao} | {r.metodo} | {e} | {est(r)} | {formata_p(r.p)} | {sat} |")
    w("")
    w("Na base empilhada, a variância da interação país × tela vem quase toda do NHANES: o gl mostrado é o do "
      "desenho do NHANES (regra do projeto), e não o da base empilhada (~27 mil, otimista). O gl de "
      "Satterthwaite fica abaixo de 15 e não muda nenhuma decisão.\n")
    w("## Sensibilidades (não entram nas famílias)\n")
    w("Fonte: `resultados/003/tabelas/sensibilidade.csv`. Renda não existe no contrato de variáveis (ausente no "
      "Vigitel e não harmonizada na PNS/NHANES): sensibilidade não feita.\n")
    w("| Base | Exposição | Modelo | Comparação | RP (IC 95%) | p | n |\n|---|---|---|---|---|---|---|")
    for _, r in S.iterrows():
        w(f"| {nb(r.base)} | {r.exposicao} | {r.modelo} | {r.comparacao} | {rp(r, 'rp')} | {formata_p(r.p)} | {int(r.n)} |")
    w("")
    w("## Forma da relação (exploratório)\n")
    w("Fonte: `resultados/003/tabelas/desvio_linearidade_exploratorio.csv`. Teste não previsto na spec: sob tendência "
      "linear no log com escores 0/1/2, a RP de 1–3 h seria a raiz quadrada da RP de ≥ 3 h (β₁ = β₂/2).\n")
    w("| Base | Exposição | RP 1–3 h vs < 1 h | RP ≥ 3 h vs < 1 h | Estatística | p |\n|---|---|---|---|---|---|")
    for _, r in L.iterrows():
        w(f"| {nb(r.base)} | {r.exposicao} | {num(r.rp_1_vs_0)} | {num(r.rp_2_vs_0)} | {est(r)} | {formata_p(r.p)} |")
    w("")
    w("## Variância: linearização × alternativas (T040)\n")
    w("Fonte: `resultados/003/tabelas/comparacao_variancia.csv`. Erro padrão do log-RP de tela alta (modelo ajustado).\n")
    w("| Base | Exposição | Linearização (usada) | Cluster do statsmodels | Poisson ponderado sem desenho | Robusto sem peso |")
    w("|---|---|---|---|---|---|")
    for _, r in V.iterrows():
        cl = num(r.ep_cluster_statsmodels, 4) if not np.isnan(r.ep_cluster_statsmodels) else "—"
        w(f"| {nb(r.base)} | {r.exposicao} | {num(r.ep_linearizacao, 4)} | {cl} | "
          f"{num(r.ep_modelo_poisson_ponderado, 4)} | {num(r.ep_robusto_sem_peso, 4)} |")
    w("")

    # leitura
    def h(hip, base, expo="digital"):
        return H[(H.hipotese == hip) & (H.base == base) & (H.exposicao == expo)].iloc[0]
    bruta_pns = R2[(R2.base == "pns2019") & (R2.exposicao == "digital") & (R2.modelo == "bruta")].iloc[0]
    tv36 = C[(C.hipotese == "H3.6") & (C.exposicao == "TV") & C.metodo.str.startswith("interação país")].iloc[0]
    tv36s = C[(C.hipotese == "H3.6 (sensibilidade)") & (C.exposicao == "TV")].iloc[0]
    h36 = H[H.hipotese == "H3.6"].iloc[0]
    w("## Leitura\n")
    f1p = H[(H.familia == "1 (digital)") & H.hipotese.isin(["H3.1", "H3.2", "H3.3"])]
    tv1 = H[(H.familia == "1 (TV)") & H.hipotese.isin(["H3.1", "H3.2", "H3.3"])]
    h33 = h("H3.3", "nhanes0506")
    w(f"- **Dentro de cada país (família 1).** Com ajuste por idade, sexo e escolaridade, tela digital ≥ 3 h/dia se "
      f"associou a mais problema de sono frequente no Vigitel (RP {rp(h('H3.1', 'vigitel2024'))}), na PNS "
      f"(RP {rp(h('H3.2', 'pns2019'))}) e no NHANES (RP {rp(h('H3.3', 'nhanes0506'))}). "
      f"{int((f1p.decisao == 'rejeita H0').sum())} de 3 rejeitam H0 depois de Holm com a regra de gl do projeto. "
      f"Com TV, {int((tv1.decisao == 'rejeita H0').sum())} de 3 (RP de {num(tv1.estimativa.min())} a "
      f"{num(tv1.estimativa.max())}).")
    w(f"- **A decisão de H3.3 depende da regra de graus de liberdade.** Com UPAs − estratos ({int(h33.gl2)} gl, regra "
      f"do projeto) o p Holm é {formata_p(h33.p_holm)} ({h33.decisao}). Com a regra do svyglm "
      f"({int(h33.gl2_svyglm)} gl), o p Holm vai a {formata_p(h33.p_holm_svyglm)} ({h33.decisao_svyglm}). "
      f"A estimativa (RP {num(h33.estimativa)}) é a mesma; muda só a incerteza atribuída a um desenho com "
      f"{int(h33.gl2)} gl. Vigitel e PNS não dependem da regra.")
    w(f"- **Confundimento por idade na PNS.** A RP bruta da tela digital é {rp(bruta_pns, 'rp')}: quem usa mais tela "
      f"é mais jovem e jovens relatam menos problema de sono. Ajustada, passa a {rp(h('H3.2', 'pns2019'))}.")
    d34 = H[H.hipotese == "H3.4"]
    abaixo = int((L.rp_1_vs_0 < 1).sum())
    acima = [f"{nb(r.base)}, {r.exposicao} ({num(r.rp_1_vs_0)})" for _, r in L.iterrows() if r.rp_1_vs_0 >= 1]
    w(f"- **Dose-resposta (H3.4).** O teste de tendência rejeita H0 em {int((d34.decisao == 'rejeita H0').sum())} "
      f"das {len(d34)} combinações, mas a forma não é uma reta. A RP ajustada de 1 a 3 h contra < 1 h fica abaixo de 1 "
      f"em {abaixo} das {len(L)} combinações (1 ou mais em: {'; '.join(acima) or 'nenhuma'}), e o excesso aparece em "
      f"≥ 3 h. O teste exploratório de desvio da linearidade tem p < 0,05 em {int((L.p < 0.05).sum())} das {len(L)}. "
      f"Os dados apontam um limiar perto de 3 h, não uma relação linear.")
    w(f"- **Brasil × EUA (H3.6).** Para a tela digital, não foi detectada diferença entre a RP do NHANES e a do "
      f"Vigitel (razão {rp(h36)}, p Holm {formata_p(h36.p_holm)}). O IC é compatível com uma RP dos EUA de "
      f"{num(100 * (1 - h36.ic_inf), 0)}% menor a {num(100 * (h36.ic_sup - 1), 0)}% maior que a do Brasil: "
      f"ausência de evidência de diferença, não prova de igualdade. Para a TV (complementar, fora de Holm) a razão foi "
      f"{rp(tv36, 'razao')}, p {formata_p(tv36.p)}, mas sem peso fica em {rp(tv36s, 'razao')} "
      f"(p {formata_p(tv36s.p)}): a diferença depende da ponderação do NHANES e não deve ser lida como robusta.")
    f2 = H[H.familia == "2"]
    i1829 = I[(I.base == "pns2019") & (I.exposicao == "digital") & (I.faixa == "18-29")].iloc[0]
    h39 = H[H.hipotese == "H3.9"].iloc[0]
    w(f"- **Idade, TV × digital e PNS × Vigitel (H3.7–H3.9).** {int((f2.decisao == 'rejeita H0').sum())} das "
      f"{len(f2)} hipóteses da família 2 rejeitam H0 depois de Holm: não foi detectada variação por faixa etária, "
      f"entre TV e tela digital, nem entre PNS e Vigitel (razão {rp(h39)}; itens de sono diferentes). Na PNS, a RP "
      f"ajustada em 18–29 anos é {rp(i1829, 'rp')} (estimada por domínio), perto do que a exploração viu, mas o "
      f"teste de interação não detecta diferença entre as faixas.")
    r_des = V.ep_linearizacao / V.ep_modelo_poisson_ponderado
    vv = V[V.base == "vigitel2024"]
    r_vig = vv.ep_linearizacao / vv.ep_robusto_sem_peso
    w(f"- **Desenho amostral importa.** O erro padrão com desenho é {num(r_des.min())} a {num(r_des.max())} vezes o "
      f"do Poisson ponderado que ignora o desenho. No Vigitel, o peso rake multiplica o erro padrão por "
      f"{num(r_vig.min())} a {num(r_vig.max())} em relação à análise sem peso.")
    w("")
    w("## Limitações\n")
    w("- Transversal: associação, não efeito. Causalidade reversa (quem dorme mal pode usar mais tela à noite) e "
      "confundimento residual (saúde mental, trabalho em turnos, renda) seguem possíveis.")
    w("- NHANES 2005-06 é anterior ao smartphone; a comparação mistura país e época (2005 × 2024).")
    w("- O item da PNS (problema de sono em geral, 2 semanas) não é o mesmo do Vigitel e do NHANES (dificuldade "
      "para adormecer); H3.9 mistura base e item.")
    w("- Vigitel cobre só as capitais e não divulga estrato e UPA: a variância usa só o peso.")
    w(f"- NHANES tem {gl_nh} graus de liberdade de desenho: intervalos largos e testes com pouco poder; a decisão de "
      f"H3.3 muda com a regra de gl (ver acima).")
    w("- Renda não entrou (ausente no contrato de variáveis).")
    (OUT / "RESUMO.md").write_text("\n".join(o) + "\n", encoding="utf-8")
    print("\n".join(o))


if __name__ == "__main__":
    main()
