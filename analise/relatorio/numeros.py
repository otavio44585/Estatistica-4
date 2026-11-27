"""Números do relatório, lidos dos CSVs em resultados/ (princípio 2: nada digitado à mão).

carrega() devolve {chave: texto formatado}. Os modelos em docs/modelos/*.md usam {{chave}};
analise.relatorio.relatorio substitui e falha se alguma chave não existir.
"""
import pandas as pd

from analise.comum import caminhos
from analise.comum.estatistica import formata_p

R = caminhos.RESULTADOS


def _csv(spec, nome):
    return pd.read_csv(R / spec / "tabelas" / f"{nome}.csv", sep=";", decimal=",", encoding="utf-8-sig")


def n2(x, casas=2):
    return f"{x:.{casas}f}".replace(".", ",").replace("-", "−")


def milhar(x):
    return f"{int(round(x)):,}".replace(",", ".")


def pct(x, casas=1):
    return n2(x, casas) + "%"


def ic(a, b, casas=2):
    return f"{n2(a, casas)} a {n2(b, casas)}"


def _linha(df, **filtro):
    m = pd.Series(True, index=df.index)
    for k, v in filtro.items():
        m &= df[k].astype(str) == str(v)
    sub = df[m]
    if len(sub) != 1:
        raise KeyError(f"filtro {filtro} achou {len(sub)} linhas")
    return sub.iloc[0]


def numeros_001(N):
    ns = pd.read_csv(R / "001" / "tabelas" / "n_por_base.csv", sep=";", encoding="utf-8-sig")
    for r in ns[ns.etapa.str.startswith("salvo")].itertuples():
        N[f"n_{r.base}"] = milhar(r.n)
    N["n_total"] = milhar(ns[ns.etapa.str.startswith("salvo")].n.sum())
    N["n_arg_sem_idade"] = milhar(pd.read_parquet(caminhos.processado("argentina"), columns=["idade"]).idade.isna().sum())
    pv = _csv("001", "prevalencias")
    for b in ["pns2019", "vigitel2024", "nhanes0506"]:
        N[f"tela3h_{b}"] = pct(_linha(pv, base=b, variavel="tela_digital_cat", categoria="≥ 3 h").pct_com_peso, 0)
    N["prev_adormecer_vigitel2024"] = pct(_linha(pv, base="vigitel2024", variavel="dif_adormecer_freq").pct_com_peso, 0)
    N["prev_adormecer_nhanes0506"] = pct(_linha(pv, base="nhanes0506", variavel="dif_adormecer_freq").pct_com_peso, 0)
    N["prev_sono_pns2019"] = pct(_linha(pv, base="pns2019", variavel="problema_sono_freq").pct_com_peso, 0)


def numeros_002(N):
    t = _csv("002", "tucker")
    N["tucker_insonia"] = n2(_linha(t, hipotese="H2.2", solucao="AF ML 1 fator (Pearson)").phi, 3)
    N["tucker_phq9"] = n2(_linha(t, hipotese="H2.3", solucao="AF ML 1 fator (Pearson)").phi, 3)
    a = _csv("002", "adequacao").set_index("conjunto")
    for c in a.index:
        N[f"var_pc1_{c}"] = pct(100 * a.loc[c, "var_pc1"], 0)
        N[f"alfa_{c}"] = n2(a.loc[c, "alfa"], 2)
        N[f"kmo_{c}"] = n2(a.loc[c, "kmo"], 2)
        N[f"fatores_{c}"] = str(int(a.loc[c, "k_decidido"]))
    e = _csv("002", "escores_correlacao").set_index("conjunto")
    N["r_soma_pc1_min"] = n2(e.r_pc1_soma.min(), 3)
    for c in e.index:
        N[f"r_soma_pc1_{c}"] = n2(e.loc[c, "r_pc1_soma"], 4)
    N["r_pc1_af_min"] = n2(e.r_pc1_af.min(), 3)
    N["r_pc1_af_max"] = n2(e.r_pc1_af.max(), 3)


def numeros_003(N):
    h = _csv("003", "hipoteses")
    for hip, base in [("H3.1", "vigitel2024"), ("H3.2", "pns2019"), ("H3.3", "nhanes0506")]:
        for exp in ["digital", "TV"]:
            r = _linha(h, hipotese=hip, base=base, exposicao=exp)
            k = f"rp_{exp.lower()}_{base}"
            N[k] = n2(r.estimativa)
            N[k + "_ic"] = ic(r.ic_inf, r.ic_sup)
            N[k + "_pholm"] = formata_p(r.p_holm)
    rb = _csv("003", "rp_bruta_ajustada")
    for base in ["pns2019", "vigitel2024", "nhanes0506"]:
        for mod in ["bruta", "ajustada"]:
            r = _linha(rb, base=base, exposicao="digital", modelo=mod, comparacao="2 vs 0")
            N[f"rp_{mod}_digital_{base}"] = n2(r.rp)
    c = _csv("003", "comparacoes_entre_bases")
    r = c[(c.hipotese == "H3.6") & (c.exposicao == "digital") & c.metodo.str.startswith("interação país × tela na base")].iloc[0]
    N["h36_razao"], N["h36_ic"], N["h36_p"] = n2(r.razao), ic(r.ic_inf, r.ic_sup), formata_p(r.p)
    N["h36_pholm"] = formata_p(_linha(h, hipotese="H3.6", exposicao="digital").p_holm)
    r = c[(c.hipotese == "H3.9") & (c.exposicao == "digital")].iloc[0]
    N["h39_razao"], N["h39_ic"] = n2(r.razao), ic(r.ic_inf, r.ic_sup)
    N["h39_pholm"] = formata_p(_linha(h, hipotese="H3.9", exposicao="digital").p_holm)
    r = c[(c.hipotese == "H3.6") & (c.exposicao == "TV") & c.metodo.str.startswith("interação país × tela na base")].iloc[0]
    N["h36_tv_razao"], N["h36_tv_p"] = n2(r.razao), formata_p(r.p)
    r = c[(c.hipotese == "H3.6 (sensibilidade)") & (c.exposicao == "digital")].iloc[0]
    N["h36_semPeso_razao"], N["h36_semPeso_p"] = n2(r.razao), formata_p(r.p)
    tv = c[(c.hipotese.str.contains("sensibilidade")) & (c.exposicao == "TV")]
    if len(tv):
        N["h36_tv_semPeso_razao"], N["h36_tv_semPeso_p"] = n2(tv.iloc[0].razao), formata_p(tv.iloc[0].p)
    N["h36_ic_pct_inf"] = pct(100 * (1 - c[(c.hipotese == "H3.6") & (c.exposicao == "digital")].ic_inf.iloc[0]), 0)
    N["h36_ic_pct_sup"] = pct(100 * (c[(c.hipotese == "H3.6") & (c.exposicao == "digital")].ic_sup.iloc[0] - 1), 0)
    rps = [h[(h.hipotese == k) & (h.exposicao == "digital")].estimativa.iloc[0] for k in ("H3.1", "H3.2", "H3.3")]
    N["rp_digital_min"], N["rp_digital_max"] = n2(min(rps)), n2(max(rps))
    br = [h[(h.hipotese == k) & (h.exposicao == "digital")].estimativa.iloc[0] for k in ("H3.1", "H3.2")]
    N["rp_br_pct_min"], N["rp_br_pct_max"] = pct(100 * (min(br) - 1), 0), pct(100 * (max(br) - 1), 0)
    nh = pd.read_parquet(caminhos.processado("nhanes0506"), columns=["estrato", "upa"])
    N["nhanes_estratos"] = str(nh.estrato.nunique())
    N["nhanes_upas"] = str(nh.groupby("estrato").upa.nunique().sum())
    r33 = _linha(h, hipotese="H3.3", base="nhanes0506", exposicao="digital")
    N["h33_pholm_svyglm"], N["h33_gl_svyglm"] = formata_p(r33.p_holm_svyglm), str(int(r33.gl2_svyglm))
    N["nhanes_gl"] = str(int(r33.gl2))
    h34 = h[(h.hipotese == "H3.4")]
    N["h34_rejeita"] = f"{int((h34.decisao == 'rejeita H0').sum())} de {len(h34)}"
    h37 = h[h.hipotese == "H3.7"]
    N["h37_pholm_min"] = formata_p(h37.p_holm.min())


def numeros_004(N):
    e = _csv("004", "efeitos_por_base").set_index("base")
    for b in e.index:
        N[f"rho_{b}"] = n2(e.loc[b, "rho"], 3)
        N[f"rho_{b}_ic"] = ic(e.loc[b, "rho_ic_inf"], e.loc[b, "rho_ic_sup"], 3)
    m = _csv("004", "meta_analise").set_index("analise")
    g = m.loc["global (7 bases)"]
    N["meta_rho"], N["meta_rho_ic"] = n2(g.rho, 3), ic(g.rho_ic_inf, g.rho_ic_sup, 3)
    N["meta_rho_ic_hk"], N["meta_p_hk"] = ic(g.rho_ic_inf_hk, g.rho_ic_sup_hk, 3), formata_p(g.p_efeito_hk)
    N["meta_p_dl"] = formata_p(g.p_efeito)
    N["meta_Q"], N["meta_glQ"], N["meta_pQ"] = n2(g.Q, 1), str(int(g.gl_Q)), formata_p(g.p_Q)
    N["meta_I2"], N["meta_tau2"] = pct(100 * g.I2, 1), n2(g.tau2, 4)
    for nome, chave in [("subgrupo: tempo total", "total"), ("subgrupo: pré-sono", "presono"),
                        ("subgrupo: uso problemático", "problematico")]:
        N[f"meta_rho_{chave}"] = n2(m.loc[nome, "rho"], 3)
        N[f"meta_rho_{chave}_ic"] = ic(m.loc[nome, "rho_ic_inf"], m.loc[nome, "rho_ic_sup"], 3)
    br = m.loc["Brasil (PNS + Vigitel)"]
    N["meta_rho_brasil"], N["meta_rho_brasil_ic"] = n2(br.rho, 3), ic(br.rho_ic_inf, br.rho_ic_sup, 3)
    ot = [i for i in m.index if i.startswith("outros países")][0]
    N["meta_rho_outros"] = n2(m.loc[ot, "rho"], 3)
    h = _csv("004", "hipoteses").set_index("hipotese")
    for k in ["H4.1", "H4.2", "H4.3", "H4.4"]:
        N[f"{k.replace('.', '')}_p"] = formata_p(h.loc[k, "p"])
        N[f"{k.replace('.', '')}_pholm"] = formata_p(h.loc[k, "p_holm"])
        N[f"{k.replace('.', '')}_decisao"] = h.loc[k, "decisao"]
    N["H42_Q"] = n2(h.loc["H4.2", "estatistica"], 2)
    sen = _csv("004", "sensibilidade").set_index("analise")
    for chave, nome in [("rho_aj_pns2019", "PNS 2019 (Brasil): ρ parcial ajustado por idade"),
                        ("rho_aj_vigitel2024", "Vigitel 2024 (Brasil): ρ parcial ajustado por idade"),
                        ("rho_aj_total", "subgrupo tempo total com ρ ajustado por idade"),
                        ("rho_aj_brasil", "Brasil (PNS + Vigitel) com ρ ajustado por idade")]:
        N[chave] = n2(sen.loc[nome, "rho"], 3)
        N[chave + "_ic"] = ic(sen.loc[nome, "ic_inf"], sen.loc[nome, "ic_sup"], 3)
    dg = sen.loc["global com variância × deff de Kish nos inquéritos"]
    N["meta_deff_rho"], N["meta_deff_ic"], N["meta_deff_I2"] = n2(dg.rho, 3), ic(dg.ic_inf, dg.ic_sup, 3), pct(100 * dg.I2, 1)
    for b, nome in [("pns2019", "PNS 2019 (Brasil)"), ("vigitel2024", "Vigitel 2024 (Brasil)"), ("nhanes0506", "NHANES 2005-06 (EUA)")]:
        N[f"deff_{b}"] = n2(sen.loc[f"{nome}: EP × √deff de Kish", "deff"], 2)
    hol = [i for i in sen.index if i.startswith("[contraponto, intrapessoal] Holanda")][0]
    N["rho_holanda"], N["rho_holanda_ic"] = n2(sen.loc[hol, "rho"], 3), ic(sen.loc[hol, "ic_inf"], sen.loc[hol, "ic_sup"], 3)
    N["H43_z"] = n2(h.loc["H4.3", "estatistica"], 2)


def numeros_005(N):
    h = _csv("005", "hipoteses").set_index("hipotese")
    for k in h.index:
        r, c = h.loc[k], k.replace(".", "")
        N[f"{c}_b"] = n2(r.b, 2) if pd.notna(r.b) else "—"
        N[f"{c}_ic"] = ic(r.ic_inf, r.ic_sup, 2) if pd.notna(r.ic_inf) else "—"
        N[f"{c}_est"] = n2(r.estatistica, 2)
        N[f"{c}_gl"] = milhar(r.gl2) if pd.notna(r.gl2) else "—"
        N[f"{c}_p"], N[f"{c}_pholm"], N[f"{c}_decisao"] = formata_p(r.p), formata_p(r.p_holm), r.decisao
        N[f"{c}_efeito"] = n2(r.efeito, 3)
        N[f"{c}_n"] = milhar(r.n)
        if pd.notna(r.p_sem_peso):
            N[f"{c}_p_sempeso"] = formata_p(r.p_sem_peso)
        if pd.notna(r.b_sem_peso):
            N[f"{c}_b_sempeso"] = n2(r.b_sem_peso, 2)
    N["H51_dr2"] = n2(h.loc["H5.1", "efeito"], 4)
    N["H51_dr2_pct"] = pct(100 * h.loc["H5.1", "efeito"], 1)
    N["H53_dr2"] = n2(h.loc["H5.3", "efeito"], 3)
    c = pd.read_csv(R / "005" / "conferencia.csv", sep=";", decimal=",", encoding="utf-8-sig")
    ok = c.ok.astype(str).str.strip().str.lower()
    exc = ok.eq("informativo") if "excecao_documentada" not in c else c.excecao_documentada.astype(str).str.lower().eq("true")
    dentro = ok.eq("true") & ~exc if "dentro_tolerancia" not in c else c.dentro_tolerancia.astype(str).str.lower().eq("true") & ~exc
    falhas = len(c) - int(dentro.sum()) - int(exc.sum())
    if falhas:
        raise AssertionError(f"conferencia.csv tem {falhas} comparações fora da tolerância sem exceção documentada")
    N["conf_n"], N["conf_dentro"], N["conf_excecoes"] = milhar(len(c)), milhar(dentro.sum()), milhar(exc.sum())
    N["conf_max_B"] = f"{c.dif_rel_B_C.max():.1e}".replace(".", ",")
    N["conf_max_A"] = f"{c.loc[dentro, 'dif_rel_A_C'].max():.1e}".replace(".", ",")
    N["conf_max_A_exc"] = f"{c.loc[exc, 'dif_rel_A_C'].max():.1e}".replace(".", ",") if exc.any() else "—"

    def gl(x):
        return "∞" if pd.isna(x) else (milhar(x) if abs(x - round(x)) < 1e-9 else n2(x, 1))

    for k in h.index:
        r, cc = h.loc[k], k.replace(".", "")
        if pd.notna(r.get("t_sem_peso")):
            N[f"{cc}_sp"] = f"t({gl(r.gl_sem_peso)}) = {n2(r.t_sem_peso)}"
        elif pd.notna(r.get("f_sem_peso")):
            N[f"{cc}_sp"] = f"F({gl(r.gl1_sem_peso)}; {gl(r.gl2_sem_peso)}) = {n2(r.f_sem_peso)}"
        else:
            N[f"{cc}_sp"] = "—"
        if str(r.versao_decisao).startswith("sem peso"):
            N[f"{cc}_cp"] = "igual (sem desenho amostral)"
        elif pd.notna(r.gl1):
            N[f"{cc}_cp"] = f"F({gl(r.gl1)}; {gl(r.gl2)}) = {n2(r.estatistica)}"
        else:
            N[f"{cc}_cp"] = f"t({gl(r.gl2)}) = {n2(r.estatistica)}"
    N["H57_f_sempeso"] = n2(h.loc["H5.7", "f_sem_peso"])
    s = _csv("005", "sensibilidade")
    r = s[(s.hipotese == "H5.2") & s.analise.str.startswith("regra do svyglm")].iloc[0]
    N["H52_p_svyglm"] = formata_p(r.p)
    pega = lambda hip, ini: s[(s.hipotese == hip) & s.analise.str.startswith(ini)].iloc[0]
    N["H54_p_serie"] = formata_p(pega("H5.4", "série escolar").p)
    N["H55_p_seminfl"] = formata_p(pega("H5.5", "sem observações influentes").p)
    N["H52_p_seminfl"] = formata_p(pega("H5.2", "sem observações influentes").p)


def carrega() -> dict:
    N = {}
    for f in (numeros_001, numeros_002, numeros_003, numeros_004, numeros_005):
        f(N)
    return N


if __name__ == "__main__":
    for k, v in carrega().items():
        print(f"{k} = {v}")
