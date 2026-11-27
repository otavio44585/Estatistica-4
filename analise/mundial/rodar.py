"""Spec 004 — executa T061–T067 e grava resultados/004/.

Uso: python -m analise.mundial.rodar
"""
import time

import numpy as np
import pandas as pd
from statsmodels.stats.meta_analysis import combine_effects

from analise.comum import caminhos
from analise.comum.estatistica import holm, decisao, salva_csv, formata_p
from analise.comum.graficos import PAIS_BASE, NOME_BASE
from analise.mundial import metodos as M
from analise.mundial.pares import PRINCIPAIS, SENSIBILIDADE, TIPOS
from analise.mundial import questionaveis as Q

LIMIAR_DIVERGENCIA = 0.10   # regra T061 fixada no plano
B_BOOT, SEMENTE = 1000, 2026
HAN_GERAL = (0.28, 0.21, 0.35)        # Han, Zhou e Liu (2024): uso geral × qualidade, k = 20
HAN_PROBLEMATICO = (0.33, 0.28, 0.38)  # uso problemático × problemas de sono, k = 36


def carrega():
    return {b: pd.read_parquet(caminhos.processado(b)) for b in sorted({p.base for p in PRINCIPAIS})}


def efeitos_principais(dados, bootstrap=True):
    linhas = []
    for p in PRINCIPAIS:
        d = dados[p.base][[p.exposicao, p.desfecho]].dropna()
        e = M.efeito(d[p.exposicao], d[p.desfecho], p.inverte)
        t0 = time.time()
        ep_b = M.ep_bootstrap(d[p.exposicao].to_numpy(float), d[p.desfecho].to_numpy(float), B_BOOT, SEMENTE) \
            if bootstrap else np.nan
        linhas.append(dict(base=p.base, nome=NOME_BASE[p.base], pais=PAIS_BASE[p.base], tipo=p.tipo,
                           exposicao=p.exposicao, rot_exposicao=p.rot_exposicao, desfecho=p.desfecho,
                           rot_desfecho=p.rot_desfecho, inverte=p.inverte, equivalencia=p.equivalencia,
                           **e, ep_bootstrap=ep_b, divergencia_rel=(ep_b - e["ep_fhp"]) / e["ep_fhp"],
                           seg_bootstrap=round(time.time() - t0, 1)))
        print(f"  {p.base}: n={e['n']} rho={e['rho']:.3f} ep_fhp={e['ep_fhp']:.5f} ep_boot={ep_b:.5f}")
    return pd.DataFrame(linhas)


def meta_linha(nome, d, papel):
    m = M.dersimonian_laird(d.z, d.ep ** 2)
    hk = M.hartung_knapp(d.z, d.ep ** 2, m["tau2"])     # verificação independente, 2026-11-27
    return dict(analise=nome, papel=papel, k=m["k"], bases=", ".join(d.base),
                rho=np.tanh(m["mu"]), rho_ic_inf=np.tanh(m["ic_inf"]), rho_ic_sup=np.tanh(m["ic_sup"]),
                z=m["mu"], ep=m["ep"], z_teste=m["z"], p_efeito=m["p"],
                rho_fixo=np.tanh(m["mu_fixo"]), Q=m["Q"], gl_Q=m["gl"], p_Q=m["p_Q"],
                tau2=m["tau2"], I2=m["I2"], I2_ic_inf=m["I2_ic_inf"], I2_ic_sup=m["I2_ic_sup"],
                ep_hk=hk["ep_hk"], gl_hk=hk["gl_hk"], rho_ic_inf_hk=np.tanh(hk["ic_inf_hk"]),
                rho_ic_sup_hk=np.tanh(hk["ic_sup_hk"]), p_efeito_hk=hk["p_hk"],
                nota="k = 1: sem τ² nem IC de Hartung-Knapp (uma base só)" if m["k"] == 1 else "")


def main():
    out = caminhos.saida("004")
    tab = out / "tabelas"
    dados = carrega()

    # ---- T062 + T061: efeito por base e verificação do EP de Spearman
    print("T061/T062: efeitos por base e bootstrap")
    ef = efeitos_principais(dados)
    usa_boot = bool((ef.divergencia_rel.abs() > LIMIAR_DIVERGENCIA).any())
    ef["ep"] = ef.ep_bootstrap if usa_boot else ef.ep_fhp
    ef["ep_usado"] = "bootstrap" if usa_boot else "Fieller-Hartley-Pearson"
    # deff de Kish dos pesos nos inquéritos (casos completos do par principal); verificação de 2026-11-27
    ef["deff_kish"] = np.nan
    for p in PRINCIPAIS:
        if p.peso:
            w = dados[p.base][[p.exposicao, p.desfecho, p.peso]].dropna()[p.peso]
            ef.loc[ef.base == p.base, "deff_kish"] = M.deff_kish(w)
    ef["rho_ic_inf"], ef["rho_ic_sup"] = np.tanh(ef.z - M.Z975 * ef.ep), np.tanh(ef.z + M.Z975 * ef.ep)
    print(f"  regra T061: divergência máxima {ef.divergencia_rel.abs().max():.1%} -> EP usado: {ef.ep_usado.iloc[0]}")

    # ---- T063: meta-análise global (H4.1), conferida com statsmodels
    glob = M.dersimonian_laird(ef.z, ef.ep ** 2)
    hk_glob = M.hartung_knapp(ef.z, ef.ep ** 2, glob["tau2"])
    sm = combine_effects(ef.z.to_numpy(), (ef.ep ** 2).to_numpy(), method_re="dl")
    conf = pd.DataFrame([
        dict(quantidade="média aleatória (z)", manual=glob["mu"], statsmodels=sm.mean_effect_re),
        dict(quantidade="EP aleatório", manual=glob["ep"], statsmodels=sm.sd_eff_w_re),
        dict(quantidade="média fixa (z)", manual=glob["mu_fixo"], statsmodels=sm.mean_effect_fe),
        dict(quantidade="Q", manual=glob["Q"], statsmodels=sm.q),
        dict(quantidade="tau2", manual=glob["tau2"], statsmodels=sm.tau2),
        dict(quantidade="I2", manual=glob["I2"], statsmodels=sm.i2),
        dict(quantidade="EP Hartung-Knapp", manual=M.hartung_knapp(ef.z, ef.ep ** 2, glob["tau2"])["ep_hk"],
             statsmodels=sm.sd_eff_w_re_hksj),
    ])
    conf["diferenca_abs"] = (conf.manual - conf.statsmodels).abs()
    assert conf.diferenca_abs.max() < 1e-10, conf
    salva_csv(conf, tab / "conferencia_statsmodels.csv")
    ef["peso_aleatorio_pct"] = glob["peso_aleatorio"] * 100
    ef["peso_fixo_pct"] = glob["peso_fixo"] * 100

    metas = [meta_linha("global (7 bases)", ef, "H4.1")]
    # ---- T064: subgrupos (H4.2)
    sub, qb = M.subgrupos(ef, "tipo")
    for t in TIPOS:
        metas.append(meta_linha(f"subgrupo: {t}", ef[ef.tipo == t], "H4.2"))
    # ---- T065: Brasil × outros com tempo total (H4.3) e referência (H4.4)
    br = ef[ef.pais == "Brasil"]
    outros_tt = ef[(ef.tipo == "tempo total") & (ef.pais != "Brasil")]
    metas.append(meta_linha("Brasil (PNS + Vigitel)", br, "H4.3"))
    metas.append(meta_linha("outros países, tempo total (NHANES + Argentina)", outros_tt, "H4.3"))
    meta = pd.DataFrame(metas)
    salva_csv(meta, tab / "meta_analise.csv")

    mbr, mout = M.dersimonian_laird(br.z, br.ep ** 2), M.dersimonian_laird(outros_tt.z, outros_tt.ep ** 2)
    h43 = M.compara_z(mbr["mu"], mbr["ep"], mout["mu"], mout["ep"])
    tt = M.dersimonian_laird(ef[ef.tipo == "tempo total"].z, ef[ef.tipo == "tempo total"].ep ** 2)
    h44 = M.tost_equivalencia(tt["mu"], tt["ep"], HAN_GERAL[1], HAN_GERAL[2])
    dif_han = M.compara_z(tt["mu"], tt["ep"], np.arctanh(HAN_GERAL[0]), M.ep_de_ic(*HAN_GERAL[1:]))
    up = M.dersimonian_laird(ef[ef.tipo == "uso problemático"].z, ef[ef.tipo == "uso problemático"].ep ** 2)
    dif_han_up = M.compara_z(up["mu"], up["ep"], np.arctanh(HAN_PROBLEMATICO[0]), M.ep_de_ic(*HAN_PROBLEMATICO[1:]))

    hip = pd.DataFrame([
        dict(hipotese="H4.1", h0="efeito comum a todas as bases", teste="Q de Cochran",
             estatistica=glob["Q"], gl=glob["gl"], p=glob["p_Q"],
             efeito=f"I² = {glob['I2']:.1%} (IC {glob['I2_ic_inf']:.1%} a {glob['I2_ic_sup']:.1%}); τ² = {glob['tau2']:.4f}",
             estimativa=np.tanh(glob["mu"]), ic_inf=np.tanh(glob["ic_inf"]), ic_sup=np.tanh(glob["ic_sup"]),
             ic_inf_hk=np.tanh(hk_glob["ic_inf_hk"]), ic_sup_hk=np.tanh(hk_glob["ic_sup_hk"])),
        dict(hipotese="H4.2", h0="sem diferença entre os tipos de exposição", teste="Q entre subgrupos",
             estatistica=qb["Q_entre"], gl=qb["gl"], p=qb["p"],
             efeito="; ".join(f"{r.subgrupo}: ρ = {np.tanh(r.mu):.3f} (k = {r.k})" for r in sub.itertuples())
                    + ". Registrada como hipótese ordenada; testada como omnibus (Q entre subgrupos não usa a ordem)",
             estimativa=np.nan, ic_inf=np.nan, ic_sup=np.nan),
        dict(hipotese="H4.3", h0="Brasil = outros países com tempo total", teste="z da diferença (escala z de Fisher)",
             estatistica=h43["z"], gl=np.nan, p=h43["p"],
             efeito=f"ρ Brasil = {np.tanh(mbr['mu']):.3f}; ρ outros = {np.tanh(mout['mu']):.3f}",
             estimativa=h43["diferenca_z"], ic_inf=h43["diferenca_z"] - M.Z975 * h43["ep"],
             ic_sup=h43["diferenca_z"] + M.Z975 * h43["ep"]),
        dict(hipotese="H4.4", h0="estimativa de tempo total fora de [0,21; 0,35] (Han, Zhou e Liu, 2024)",
             teste="equivalência por dois testes unilaterais (TOST)",
             estatistica=min(h44["z_inf"], -h44["z_sup"]), gl=np.nan, p=h44["p"],
             efeito=f"ρ tempo total = {np.tanh(tt['mu']):.3f} (IC {np.tanh(tt['ic_inf']):.3f} a {np.tanh(tt['ic_sup']):.3f}); "
                    f"diferença para r = 0,28: z = {dif_han['z']:.2f}, p = {formata_p(dif_han['p'])}",
             estimativa=np.tanh(tt["mu"]), ic_inf=np.tanh(tt["ic_inf"]), ic_sup=np.tanh(tt["ic_sup"])),
    ])
    hip["p_holm"] = holm(hip.p)
    hip["decisao"] = [decisao(p) for p in hip.p_holm]
    hip["p_txt"], hip["p_holm_txt"] = hip.p.map(formata_p), hip.p_holm.map(formata_p)
    salva_csv(hip, tab / "hipoteses.csv")

    expl = pd.DataFrame([
        dict(analise="exploratório: uso problemático × Han, Zhou e Liu (2024) r = 0,33 (IC 0,28–0,38)",
             rho=np.tanh(up["mu"]), ic_inf=np.tanh(up["ic_inf"]), ic_sup=np.tanh(up["ic_sup"]),
             z=dif_han_up["z"], p=dif_han_up["p"]),
        dict(analise="complemento de H4.4: diferença tempo total × r = 0,28", rho=np.tanh(tt["mu"]),
             ic_inf=np.tanh(tt["ic_inf"]), ic_sup=np.tanh(tt["ic_sup"]), z=dif_han["z"], p=dif_han["p"]),
    ])
    # exploratório: a ordem prevista em H4.2 (tempo total < pré-sono < uso problemático), por meta-regressão
    ordem = {"tempo total": 0, "pré-sono": 1, "uso problemático": 2}
    sub_o = sub.assign(escore=sub.subgrupo.map(ordem)).dropna(subset=["escore"])
    td = M.tendencia_ordenada(sub_o.mu, sub_o.ep, sub_o.escore)
    expl = pd.concat([expl, pd.DataFrame([dict(
        analise="EXPLORATÓRIO: tendência ordenada de H4.2 (escore 0 tempo total, 1 pré-sono, 2 uso problemático; "
                "meta-regressão das médias de subgrupo, pesos 1/EP²)",
        rho=np.nan, ic_inf=np.nan, ic_sup=np.nan, z=td["z"], p=td["p"],
        inclinacao_z=td["inclinacao"], ep_inclinacao=td["ep"], p_unilateral=td["p_unilateral"])])], ignore_index=True)
    salva_csv(expl, tab / "exploratorio_referencia.csv")

    # ---- T066: sensibilidades
    sens = []
    for b in ef.base:                                   # deixar uma de fora
        d = ef[ef.base != b]
        m = M.dersimonian_laird(d.z, d.ep ** 2)
        sens.append(dict(analise=f"sem {NOME_BASE[b]}", grupo="deixar uma de fora", k=m["k"],
                         rho=np.tanh(m["mu"]), ic_inf=np.tanh(m["ic_inf"]), ic_sup=np.tanh(m["ic_sup"]),
                         Q=m["Q"], p_Q=m["p_Q"], I2=m["I2"], n=np.nan))
    ef_w = ef.copy()                                    # correlação ponderada nos inquéritos
    for p in PRINCIPAIS:
        if p.peso:
            d = dados[p.base][[p.exposicao, p.desfecho, p.peso]].dropna()
            rw = M.spearman_ponderado(d[p.exposicao].to_numpy(float), d[p.desfecho].to_numpy(float),
                                      d[p.peso].to_numpy(float))
            i = ef_w.index[ef_w.base == p.base][0]
            ef_w.loc[i, "z"] = np.arctanh(rw)
            sens.append(dict(analise=f"{NOME_BASE[p.base]}: ρ ponderado pelo peso amostral", grupo="ponderada",
                             k=1, rho=rw, ic_inf=np.nan, ic_sup=np.nan, Q=np.nan, p_Q=np.nan, I2=np.nan, n=len(d)))
    # efeito do desenho: variância × deff de Kish nos 3 inquéritos (verificação independente, 2026-11-27)
    ef_d = ef.copy()
    infl = ef_d.deff_kish.fillna(1.0)
    ef_d["ep"] = ef_d.ep * np.sqrt(infl)
    for r in ef_d[ef_d.deff_kish.notna()].itertuples():
        sens.append(dict(analise=f"{r.nome}: EP × √deff de Kish", grupo="efeito do desenho (deff)", k=1,
                         rho=r.rho, ic_inf=np.tanh(r.z - M.Z975 * r.ep), ic_sup=np.tanh(r.z + M.Z975 * r.ep),
                         Q=np.nan, p_Q=np.nan, I2=np.nan, n=r.n, deff=r.deff_kish))
    for nome, d in [("global com variância × deff de Kish nos inquéritos", ef_d),
                    ("subgrupo tempo total com variância × deff de Kish", ef_d[ef_d.tipo == "tempo total"])]:
        m = M.dersimonian_laird(d.z, d.ep ** 2)
        hk = M.hartung_knapp(d.z, d.ep ** 2, m["tau2"])
        sens.append(dict(analise=nome, grupo="efeito do desenho (deff)", k=m["k"], rho=np.tanh(m["mu"]),
                         ic_inf=np.tanh(m["ic_inf"]), ic_sup=np.tanh(m["ic_sup"]), Q=m["Q"], p_Q=m["p_Q"],
                         I2=m["I2"], n=np.nan, tau2=m["tau2"], ic_inf_hk=np.tanh(hk["ic_inf_hk"]),
                         ic_sup_hk=np.tanh(hk["ic_sup_hk"])))
    bd, od = ef_d[ef_d.pais == "Brasil"], ef_d[(ef_d.tipo == "tempo total") & (ef_d.pais != "Brasil")]
    mb, mo = M.dersimonian_laird(bd.z, bd.ep ** 2), M.dersimonian_laird(od.z, od.ep ** 2)
    c = M.compara_z(mb["mu"], mb["ep"], mo["mu"], mo["ep"])
    sens.append(dict(analise="H4.3 com variância × deff de Kish (Brasil − outros, escala z)", grupo="efeito do desenho (deff)",
                     k=4, rho=np.tanh(mb["mu"]), ic_inf=c["diferenca_z"] - M.Z975 * c["ep"],
                     ic_sup=c["diferenca_z"] + M.Z975 * c["ep"], Q=np.nan, p_Q=np.nan, I2=np.nan, n=np.nan,
                     z_teste=c["z"], p=c["p"], rho_outros=np.tanh(mo["mu"])))
    m = M.dersimonian_laird(ef_w.z, ef_w.ep ** 2)
    sens.append(dict(analise="global com ρ ponderado nos 3 inquéritos", grupo="ponderada", k=m["k"],
                     rho=np.tanh(m["mu"]), ic_inf=np.tanh(m["ic_inf"]), ic_sup=np.tanh(m["ic_sup"]),
                     Q=m["Q"], p_Q=m["p_Q"], I2=m["I2"], n=np.nan))
    # bruta × ajustada por idade (princípio 11); Xuzhou não tem idade e entra bruta
    ef_aj, aj = ef.copy(), []
    for p in PRINCIPAIS:
        if "idade" in dados[p.base].columns:
            d = dados[p.base][[p.exposicao, p.desfecho, "idade"]].dropna()
            e = M.spearman_parcial(d[p.exposicao], d[p.desfecho], d.idade, p.inverte)
            i = ef_aj.index[ef_aj.base == p.base][0]
            ef_aj.loc[i, ["z", "ep"]] = [e["z"], e["ep"]]
            bruto = ef.loc[ef.base == p.base].iloc[0]
            aj.append(dict(base=p.base, nome=NOME_BASE[p.base], pais=PAIS_BASE[p.base], tipo=p.tipo,
                           rho_bruto=bruto.rho, ic_inf_bruto=bruto.rho_ic_inf, ic_sup_bruto=bruto.rho_ic_sup,
                           n_bruto=bruto.n, rho_ajustado_idade=e["rho"], ic_inf_ajustado=e["ic_inf"],
                           ic_sup_ajustado=e["ic_sup"], n_ajustado=e["n"]))
            sens.append(dict(analise=f"{NOME_BASE[p.base]}: ρ parcial ajustado por idade", grupo="ajustada por idade",
                             k=1, rho=e["rho"], ic_inf=e["ic_inf"], ic_sup=e["ic_sup"], Q=np.nan, p_Q=np.nan,
                             I2=np.nan, n=e["n"]))
    salva_csv(pd.DataFrame(aj), tab / "bruta_ajustada_idade.csv")
    m = M.dersimonian_laird(ef_aj.z, ef_aj.ep ** 2)
    sens.append(dict(analise="global com ρ ajustado por idade (Xuzhou bruto, sem idade)", grupo="ajustada por idade",
                     k=m["k"], rho=np.tanh(m["mu"]), ic_inf=np.tanh(m["ic_inf"]), ic_sup=np.tanh(m["ic_sup"]),
                     Q=m["Q"], p_Q=m["p_Q"], I2=m["I2"], n=np.nan))
    tt_aj = ef_aj[ef_aj.tipo == "tempo total"]
    m = M.dersimonian_laird(tt_aj.z, tt_aj.ep ** 2)
    sens.append(dict(analise="subgrupo tempo total com ρ ajustado por idade", grupo="ajustada por idade",
                     k=m["k"], rho=np.tanh(m["mu"]), ic_inf=np.tanh(m["ic_inf"]), ic_sup=np.tanh(m["ic_sup"]),
                     Q=m["Q"], p_Q=m["p_Q"], I2=m["I2"], n=np.nan))
    br_aj = ef_aj[ef_aj.pais == "Brasil"]
    m = M.dersimonian_laird(br_aj.z, br_aj.ep ** 2)
    sens.append(dict(analise="Brasil (PNS + Vigitel) com ρ ajustado por idade", grupo="ajustada por idade",
                     k=m["k"], rho=np.tanh(m["mu"]), ic_inf=np.tanh(m["ic_inf"]), ic_sup=np.tanh(m["ic_sup"]),
                     Q=m["Q"], p_Q=m["p_Q"], I2=m["I2"], n=np.nan))
    for p in SENSIBILIDADE:                             # pares alternativos
        d = dados[p.base][[p.exposicao, p.desfecho]].dropna()
        e = M.efeito(d[p.exposicao], d[p.desfecho], p.inverte)
        sens.append(dict(analise=f"{NOME_BASE[p.base]}: {p.rot_exposicao} × {p.rot_desfecho}", grupo="par alternativo",
                         k=1, rho=e["rho"], ic_inf=e["rho_ic_inf"], ic_sup=e["rho_ic_sup"], Q=np.nan, p_Q=np.nan,
                         I2=np.nan, n=e["n"]))
    quest = []
    for rot, tipo, f, inv, rx, ry in Q.QUESTIONAVEIS:  # procedência questionável
        d = f().dropna()
        e = M.efeito(d.x, d.y, inv)
        quest.append(dict(base=rot, tipo=tipo, z=e["z"], ep=e["ep_fhp"]))
        sens.append(dict(analise=f"[procedência questionável] {rot}", grupo="procedência questionável", k=1,
                         rho=e["rho"], ic_inf=e["rho_ic_inf"], ic_sup=e["rho_ic_sup"], Q=np.nan, p_Q=np.nan,
                         I2=np.nan, n=e["n"]))
    qd = pd.concat([ef[["base", "tipo", "z", "ep"]], pd.DataFrame(quest)], ignore_index=True)
    m = M.dersimonian_laird(qd.z, qd.ep ** 2)
    sens.append(dict(analise="global incluindo as 4 bases de procedência questionável", grupo="procedência questionável",
                     k=m["k"], rho=np.tanh(m["mu"]), ic_inf=np.tanh(m["ic_inf"]), ic_sup=np.tanh(m["ic_sup"]),
                     Q=m["Q"], p_Q=m["p_Q"], I2=m["I2"], n=np.nan))
    hol = M.rmcorr(Q.holanda(), "user_id", "prebed_use", "sleep_qual_inv")   # contraponto intrapessoal
    sens.append(dict(analise="[contraponto, intrapessoal] Holanda, Siebers: celular na hora antes de deitar × "
                             "qualidade da noite (invertida)", grupo="contraponto intrapessoal", k=1, rho=hol["r"],
                     ic_inf=hol["ic_inf"], ic_sup=hol["ic_sup"], Q=np.nan, p_Q=hol["p"], I2=np.nan, n=hol["n"]))
    sens_df = pd.DataFrame(sens)
    salva_csv(sens_df, tab / "sensibilidade.csv")
    salva_csv(ef, tab / "efeitos_por_base.csv")

    from analise.mundial.floresta import desenha, bruta_ajustada
    desenha(ef, meta, out / "figuras" / "floresta.png", HAN_GERAL)
    bruta_ajustada(pd.DataFrame(aj), out / "figuras" / "bruta_ajustada_idade.png")
    print(hip[["hipotese", "estatistica", "gl", "p_txt", "p_holm_txt", "decisao"]].to_string(index=False))
    print(meta[["analise", "k", "rho", "rho_ic_inf", "rho_ic_sup", "Q", "p_Q", "I2", "tau2"]].round(4).to_string(index=False))
    print(sens_df[["analise", "rho", "ic_inf", "ic_sup", "n"]].round(3).to_string(index=False))
    return ef, meta, hip, sens_df


if __name__ == "__main__":
    main()
