"""Gera resultados/005/RESUMO.md a partir dos CSVs (nenhum número digitado à mão, princípio 2)."""
import pandas as pd

from analise.comum import caminhos
from analise.comum.estatistica import formata_p, le_csv, num
from analise.regressao import dados as D

OUT = caminhos.saida("005")
T = OUT / "tabelas"


def _sci(x):
    return f"{x:.1e}".replace(".", ",")


def _p(p):
    """'p < 0,001' ou 'p = 0,158'."""
    t = formata_p(p)
    return f"p {t}" if t.startswith("<") else f"p = {t}"


def _ic(lo, hi, c=2):
    return f"{num(lo, c)} a {num(hi, c)}"


def main():
    h = le_csv(T / "hipoteses.csv")
    cf = le_csv(OUT / "conferencia.csv")
    ba = le_csv(T / "bruta_ajustada.csv")
    mf = le_csv(T / "medias_por_faixa.csv")
    dg = le_csv(T / "diagnostico.csv")
    se = le_csv(T / "sensibilidade.csv")
    eq = le_csv(T / "equivalencias.csv")
    H = h.set_index("hipotese")
    exc = cf.excecao_documentada.astype(str) == "True"
    av = cf[~exc]
    n_ok = int((av.dentro_tolerancia.astype(str) == "True").sum())
    welch = cf[exc]
    dn = D.matriz("nhanes0506")[1]["desenho"]
    nh_est, nh_upa = dn.estrato.nunique(), int(dn.groupby("estrato").upa.nunique().sum())

    L = ["# 005 — Resumo dos resultados: regressão linear múltipla, ANOVA e teste t", "",
         "Gerado por `python -m analise.regressao.resumo` a partir de `resultados/005/tabelas/*.csv` e "
         "`resultados/005/conferencia.csv`. α = 0,05 bilateral; Holm dentro de cada família. "
         "Associação observacional, sem interpretação causal.", "",
         "## Conferência dos p-valores (três caminhos)", "",
         f"- **Caminho A:** ferramenta Análise de Dados do Excel (Analysis ToolPak), executada por automação COM "
         f"(`analise/regressao/excel_toolpak.ps1`, chamado por `roda_excel.py`): Regressão, Anova: fator único e "
         f"Teste-t (variâncias diferentes e iguais), em 7 pastas de trabalho.",
         "- **Caminho B:** fórmulas nativas do Excel ao lado de cada saída (`T.DIST.2T`, `F.DIST.RT`), recalculadas pelo próprio Excel.",
         "- **Caminho C:** script (`analise/regressao/ols.py`, álgebra matricial, e `scipy`).",
         f"- **Resultado:** {n_ok} de {len(av)} números dentro da tolerância (1e-8), mais {len(welch)} exceções documentadas "
         f"(abaixo); maior diferença relativa A × C = {_sci(av.dif_rel_A_C.max())}, B × C = {_sci(av.dif_rel_B_C.max())}. "
         "Arquivo: `resultados/005/conferencia.csv` (colunas `dentro_tolerancia` e `excecao_documentada`).",
         f"- **Exceções documentadas ({len(welch)}, uma por base com teste t):** o teste t de Welch do Excel arredonda os "
         f"graus de liberdade para inteiro. O p do Excel difere do p com gl fracionário em até {_sci(welch.dif_rel_A_C.max())} "
         "(relativo), acima da tolerância. "
         "O relatório usa o gl fracionário (caminho C); o Excel bate com o script quando o script usa o mesmo gl inteiro.",
         "- **Equivalências verificadas** (`tabelas/equivalencias.csv`): F da ANOVA = F global da regressão nas 2 dummies "
         f"(diferença {_sci(eq.dif_relativa.iloc[0])}); t com variâncias iguais = t da dummy (diferença {_sci(eq.dif_relativa.iloc[1])}); "
         f"t de Welch difere do t com variâncias iguais em {num(100 * eq.dif_relativa.iloc[2], 1)}% (Vigitel).", "",
         "**Graus de liberdade com peso (regra única do projeto, igual à da spec 003):** gl = nº de UPAs − nº de estratos "
         f"(NHANES: {nh_upa} − {nh_est} = {nh_upa - nh_est}). Wald de mais de um coeficiente (ANOVA ponderada, F global, H5.11) com a correção de "
         "Korn-Graubard: F = (d − q + 1)/(d·q)·W, gl (q, d − q + 1). A regra do `svyglm` (d − p + 1) entra como sensibilidade.", "",
         "## Família R1 — coeficiente da tela na regressão múltipla", "",
         "| H | Base | Y | Tela (coeficiente testado) | b (IC 95%) | t | gl | p | p Holm | Decisão | ΔR² do bloco de tela | Versão que decide |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in h[h.familia == "R1"].iterrows():
        L.append(f"| {r.hipotese} | {r.rotulo} | {r.y} | {r.teste.split(chr(39))[1]} | {num(r.b, 3)} ({_ic(r.ic_inf, r.ic_sup, 3)}) | "
                 f"{num(r.estatistica)} | {int(r.gl2)} | {formata_p(r.p)} | {formata_p(r.p_holm)} | {r.decisao} | "
                 f"{num(r.efeito, 4)} (f² {num(r.f2, 4)}) | {r.versao_decisao} |")
    L += ["", "Leitura (um coeficiente por base, unidades do desfecho, demais variáveis fixas):", ""]
    a = H.loc["H5.1"]
    L.append(f"- **Vigitel (H5.1):** quem usa tela digital ≥ 3 h/dia tem índice de insônia {num(a.b)} ponto maior "
             f"(IC {_ic(a.ic_inf, a.ic_sup)}) que quem usa < 1 h, com idade, sexo e escolaridade fixos. O bloco de tela "
             f"acrescenta {num(100 * a.efeito, 2)}% de R² (ponderado).")
    a = H.loc["H5.2"]
    L.append(f"- **NHANES (H5.2):** diferença de {num(a.b)} ponto (IC {_ic(a.ic_inf, a.ic_sup)}), {_p(a.p)} com o desenho "
             f"amostral (gl = {int(a.gl2)}). Sem peso, o mesmo modelo dá b = {num(a.b_sem_peso)} e {_p(a.p_sem_peso)}: "
             "a conclusão depende do desenho, e o princípio 8 manda usar a versão com peso. Também é frágil sem peso: "
             f"sem as observações influentes, {_p(se[(se.hipotese == 'H5.2') & se.analise.str.startswith('sem observações')].p.iloc[0])}.")
    a = H.loc["H5.3"]
    L.append(f"- **Xuzhou (H5.3):** cada ponto a mais no SAS-SV se associa a {num(a.b, 3)} ponto a mais no PSQI "
             f"(IC {_ic(a.ic_inf, a.ic_sup, 3)}); 10 pontos de SAS-SV ≈ {num(10 * a.b)} ponto de PSQI. Maior tamanho de efeito da família "
             f"(ΔR² = {num(a.efeito, 3)}).")
    a = H.loc["H5.4"]
    L.append(f"- **Argentina (H5.4):** cada hora de tela antes de dormir se associa a {num(a.b)} min de latência "
             f"(IC {_ic(a.ic_inf, a.ic_sup)}). **O sinal é o contrário do esperado** (menos latência com mais tela). "
             "Com a série escolar no lugar da idade (mais casos completos), o p fica acima de 0,05 (ver sensibilidade).")
    a = H.loc["H5.5"]
    L.append(f"- **Turquia (H5.5):** cada ponto de doomscrolling se associa a {num(a.b, 3)} min de latência "
             f"(IC {_ic(a.ic_inf, a.ic_sup, 3)}); 10 pontos ≈ {num(10 * a.b)} min. Rótulo da escala confirmado por evidência "
             "indireta, sem codebook (T080).")
    a = H.loc["H5.6"]
    L.append(f"- **Japão (H5.6):** cada hora de celular nas 3 h antes de dormir se associa a {num(a.b)} ponto a mais na AIS "
             f"(IC {_ic(a.ic_inf, a.ic_sup)}).")
    L += ["", "**Testes do modelo, fora das famílias** (o que o SUMMARY OUTPUT mostra; sem peso, como no Excel):", "",
          "| Base | n | R² | R² ajustado | F global (gl) | p do F global | F parcial da tela (gl) | p | ΔR² |",
          "|---|---|---|---|---|---|---|---|---|"]
    for _, r in h[h.familia == "R1"].iterrows():
        k = int(r.n - 1 - r.gl_sem_peso)
        q = 2 if r.base in ("vigitel2024", "nhanes0506") else 1
        L.append(f"| {r.rotulo} | {int(r.n)} | {num(r.r2_completo_sem_peso, 4)} | {num(r.r2_aj_completo_sem_peso, 4)} | "
                 f"{num(r.f_global_sem_peso)} ({k}; {int(r.gl_sem_peso)}) | {formata_p(r.p_f_global_sem_peso)} | "
                 f"{num(r.f_parcial_sem_peso)} ({q}; {int(r.gl_sem_peso)}) | {formata_p(r.p_f_parcial_sem_peso)} | "
                 f"{num(r.delta_r2_sem_peso, 4)} |")
    sj = le_csv(T / "summary_japao_completo.csv").set_index("item")
    L += ["", f"No Japão o F global não é significativo (p = {formata_p(H.loc['H5.6'].p_f_global_sem_peso)}), mas o coeficiente "
              f"da tela é: idade (p = {formata_p(sj.loc['idade'].valor_p)}) e sexo (p = {formata_p(sj.loc['sexo_cod2'].valor_p)}) "
              "diluem o F, que testa os três coeficientes juntos. O F global não substitui o teste da hipótese.", "",
          "## Família R2 — ANOVA, teste t e Brasil × EUA", "",
          "| H | Base | Teste | Estatística (com peso) | gl | p | p Holm | Decisão | Efeito | Sem peso (Excel) |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in h[h.familia == "R2"].iterrows():
        gl = f"{int(r.gl1)}; {int(r.gl2)}" if pd.notna(r.gl1) else f"{int(r.gl2)}"
        if pd.notna(r.get("t_sem_peso")):
            sp = f"t = {num(r.t_sem_peso)}, gl = {num(r.gl_sem_peso, 1)}, {_p(r.p_sem_peso)}, d = {num(r.d_cohen_sem_peso, 3)}"
        else:
            sp = f"F = {num(r.f_sem_peso)}, gl = {int(r.gl1_sem_peso)}; {int(r.gl2_sem_peso)}, {_p(r.p_sem_peso)}"
            if pd.notna(r.get("eta2_sem_peso")):
                sp += f", η² = {num(r.eta2_sem_peso, 4)}"
        L.append(f"| {r.hipotese} | {r.rotulo} | {r.teste} | {num(r.estatistica)} | {gl} | {formata_p(r.p)} | "
                 f"{formata_p(r.p_holm)} | {r.decisao} | {r.efeito_nome}: {num(r.efeito, 4)} | {sp} |")
    a = H.loc["H5.11"]
    L += ["", f"- **H5.11 (Brasil × EUA):** na base empilhada, não foi detectada diferença entre os países na interação "
              f"país × tela (F({int(a.gl1)}; {int(a.gl2)}) = {num(a.estatistica)}, {_p(a.p)}; gl de desenho do NHANES, "
              f"porque a variância da interação vem quase toda dele). A diferença entre os coeficientes de ≥ 3 h dos dois "
              f"países é {num(a.b)} ponto (IC {_ic(a.ic_inf, a.ic_sup)}). Não rejeitar H0 não prova que os efeitos são "
              "iguais: o IC é largo, sobretudo pelo NHANES.",
          "- **d de Cohen:** a mesma definição sem e com peso: diferença de médias dividida pelo DP combinado dentro "
          "dos grupos (com peso, pesos normalizados para somar n).", "",
          "## Médias do índice de insônia por faixa de tela (`tabelas/medias_por_faixa.csv`)", "",
          "| Base | Faixa | n | Média | DP | Média com peso |", "|---|---|---|---|---|---|"]
    for _, r in mf.iterrows():
        L.append(f"| {r.base} | {r.faixa} | {r.n} | {num(r.media)} | {num(r.dp)} | {num(r.media_ponderada)} |")
    da, _ = D.matriz("argentina")
    ds, _ = D.matriz("argentina", sens_serie=True)
    L += ["", "## Bruta × ajustada (`tabelas/bruta_ajustada.csv`)", "",
          "| Base | Versão | b simples (só tela) | p | b múltipla | p |", "|---|---|---|---|---|---|"]
    for _, r in ba.iterrows():
        L.append(f"| {r.base} | {r.versao} | {num(r.b_bruta, 3)} ({r.ic_bruta.replace('.', ',')}) | {formata_p(r.p_bruta)} | "
                 f"{num(r.b_ajustada, 3)} ({r.ic_ajustada.replace('.', ',')}) | {formata_p(r.p_ajustada)} |")
    idades = {}
    for b in ("vigitel2024", "nhanes0506"):
        dfb, ib = D.matriz(b)
        idades[b] = dfb.groupby(ib["tela_cat"]).idade.mean()
    L += ["", "No Vigitel e no NHANES o coeficiente da tela cresce ao ajustar (confundimento negativo pelas covariáveis em "
              f"conjunto). Quem usa ≥ 3 h é mais jovem: idade média {num(idades['vigitel2024'][2], 1)} × "
              f"{num(idades['vigitel2024'][0], 1)} anos (< 1 h) no Vigitel e {num(idades['nhanes0506'][2], 1)} × "
              f"{num(idades['nhanes0506'][0], 1)} no NHANES. Mesmo sentido do confundimento por idade visto na exploração da PNS.", "",
          "## Pressupostos (`tabelas/diagnostico.csv`)", "",
          "| Base | n | Breusch-Pagan p | Jarque-Bera p | VIF da tela | VIF máximo (regressor) | Influentes (Cook > 4/n) |",
          "|---|---|---|---|---|---|---|"]
    for _, r in dg.iterrows():
        L.append(f"| {r.base} | {r.n} | {formata_p(r.breusch_pagan_p)} | {formata_p(r.jarque_bera_p)} | {num(r.vif_tela)} | "
                 f"{num(r.vif_maximo)} ({r.regressor_vif_maximo}) | {r.influentes_cook_4n} ({num(r.pct_influentes, 1)}%) |")
    L += ["", "- Resíduos não normais em todas as bases (desfechos discretos e assimétricos). Com n de centenas ou mais, t e F "
              "seguem aproximadamente válidos; os QQ-plots estão em `figuras/diagnostico_<base>.png`.",
          "- Heterocedasticidade em Vigitel, NHANES e Xuzhou: a sensibilidade com EP robusto HC3 não muda nenhuma decisão das bases sem peso.",
          f"- VIF da tela ≤ {num(dg.vif_tela.max(), 1)} e VIF máximo ≤ {num(dg.vif_maximo.max(), 1)} em todas as bases. A categoria "
          "de referência das dummies é a mais frequente; com a menor como referência (renda 1 em Xuzhou, escolaridade dos "
          "pais 1 na Argentina) o VIF dessas dummies passava de 10, sem mudar o coeficiente da tela.", "",
          "## Sensibilidade (`tabelas/sensibilidade.csv`)", "",
          "| H | Análise | b | p | Muda a decisão a 5%? |", "|---|---|---|---|---|"]
    for _, r in se.iterrows():
        rot = " (exploratória)" if str(r.exploratoria) == "True" else ""
        muda = "—" if rot else ("sim" if str(r.muda_em_relacao_ao_principal) == "True" else "não")
        L.append(f"| {r.hipotese} | {r.analise}{rot} | {num(r.b, 3)} | {formata_p(r.p)} | {muda} |")
    L += ["", "Pontos de atenção da sensibilidade:",
          "- **H5.2 (NHANES):** sem peso ou com HC3 o coeficiente é significativo; com o desenho amostral não é. "
          "Com a regra do `svyglm` (gl = 9) a decisão se mantém. Sem as observações influentes, também não é significativo.",
          f"- **H5.4 (Argentina):** depende de quem entra na amostra: com a série escolar no lugar da idade ({len(ds) - len(da)} casos a mais), p > 0,05.",
          "- **H5.5 (Turquia):** sem as observações influentes, p > 0,05; com log(1 + latência), mantém.", "",
          "## Limitações", "",
          "- Dados transversais: associação, não efeito.",
          "- NHANES 2005-06 é anterior ao smartphone; Vigitel cobre só as capitais. H5.11 mistura país e época.",
          "- Os desfechos são escalas diferentes em cada base; os coeficientes só são comparáveis dentro da base "
          "(a comparação padronizada entre países é a spec 004).",
          "- Latência da Argentina e da Turquia concentrada em valores redondos (5, 10, 15, 30, 60 min).",
          "- Turquia: rótulo da escala de doomscrolling inferido sem codebook; sexo sem rótulo, fora do modelo.",
          "- Xuzhou e Japão: sexo entra como código 1/2 sem rótulo documentado.",
          f"- Argentina: adolescentes sem idade (163) ou sem escolaridade dos pais ficam fora do modelo principal ({len(da)} de 864).",
          ]
    (OUT / "RESUMO.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:40]))


if __name__ == "__main__":
    main()
