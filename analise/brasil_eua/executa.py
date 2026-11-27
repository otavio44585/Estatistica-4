"""T042–T049 — Executa as hipóteses H3.1–H3.4 e H3.6–H3.9 da spec 003 e as sensibilidades.

Uso: python -m analise.brasil_eua.executa
Saídas em resultados/003/tabelas e resultados/003/figuras.

Correções da verificação independente (2026-11-27):
- gl do desenho = UPAs − estratos é a regra única; a regra do svyglm (d − p + 1) entra como sensibilidade
  (colunas *_svyglm em hipoteses.csv e linhas em sensibilidade.csv);
- Wald conjunto com correção de Korn-Graubard (survey.Ajuste.wald);
- base empilhada Vigitel + NHANES: o gl mostrado é o do NHANES (15), conservador; Satterthwaite registrado;
- RP por faixa etária estimada por domínio (variância com o desenho inteiro).
"""
import numpy as np
import pandas as pd
from scipy import stats

from analise.brasil_eua.survey import poisson_desenho
from analise.comum import caminhos
from analise.comum.estatistica import holm, decisao, salva_csv
from analise.comum import graficos as G

OUT = caminhos.saida("003")
T, F = OUT / "tabelas", OUT / "figuras"

BASES = {
    "vigitel2024": dict(y="dif_adormecer_freq", desenho=dict(peso="peso"),
                        desfecho="dificuldade para adormecer quase sempre ou sempre"),
    "pns2019": dict(y="problema_sono_freq", desenho=dict(peso="peso", estrato="estrato", upa="upa"),
                    desfecho="problema de sono em mais da metade dos dias (2 semanas)"),
    "nhanes0506": dict(y="dif_adormecer_freq", desenho=dict(peso="peso", estrato="estrato", upa="upa"),
                       desfecho="dificuldade para adormecer often/almost always (5 ou mais vezes por mês)"),
}
EXPOS = {"tela_digital_cat": "digital", "tela_tv_cat": "TV"}
ORD = {"tela_digital_cat": "tela_digital_ord", "tela_tv_cat": "tela_tv_ord"}
COV = "C(faixa_etaria) + sexo + C(escolaridade3)"
COVARS = ["faixa_etaria", "sexo", "escolaridade3"]
FAIXAS = ["18-29", "30-44", "45-59", "60+"]
# corte alternativo de exposição alta (sensibilidade): valores de tela_*_ord
CORTE_ALT = {"vigitel2024": (5, "≥ 4 h"), "nhanes0506": (5, "≥ 4 h"), "pns2019": (5, "≥ 6 h (a PNS não separa 4 h)")}


def carrega(base):
    return pd.read_parquet(caminhos.processado(base))


def amostra(df, y, x, extra=()):
    cols = [y, x, *COVARS, *extra, *[c for c in ("peso", "estrato", "upa") if c in df.columns]]
    d = df.dropna(subset=cols).reset_index(drop=True)
    d["expo"] = d[x].astype(int)
    return d


def linha_rp(aj, termo, **info):
    t = aj.termo(termo)
    return dict(**info, termo=termo, rp=t["rp"], ic_inf=t["ic_inf"], ic_sup=t["ic_sup"], beta=t["beta"], ep=t["ep"],
                estatistica=t["estatistica"], tipo_estat="t" if aj.gl else "z", gl=aj.gl, p=t["p"], n=aj.n,
                n_upas=aj.n_upas, n_estratos=aj.n_estratos, estratos_1upa=aj.estratos_1upa, variancia=aj.metodo,
                n_param=aj.n_param, gl_svyglm=aj.gl_svyglm())


def p_svyglm(estatistica, tipo, gl1, gl_desenho, n_param):
    """p com a regra do svyglm: d' = d − p + 1 no lugar de d (t; F de Korn-Graubard recalculado)."""
    if not gl_desenho or pd.isna(gl_desenho):
        return np.nan, np.nan
    d2 = gl_desenho - n_param + 1
    if tipo == "t":
        return 2 * stats.t.sf(abs(estatistica), d2), d2
    if tipo == "F":
        q = int(gl1)
        if d2 - q + 1 < 1:                                             # gl insuficientes para q restrições
            return np.nan, d2
        W = estatistica * gl_desenho * q / (gl_desenho - q + 1)       # desfaz Korn-Graubard com d
        F2 = (d2 - q + 1) / (d2 * q) * W
        return stats.f.sf(F2, q, d2 - q + 1), d2
    return np.nan, np.nan


def prevalencias(base, d, y, x, peso):
    out = []
    for k, g in d.groupby("expo"):
        w = g[peso] if peso else np.ones(len(g))
        out.append(dict(base=base, exposicao=EXPOS[x], categoria=int(k), n=len(g), casos=int(g[y].sum()),
                        prevalencia_amostral=g[y].mean(), prevalencia_ponderada=np.average(g[y], weights=w)))
    return out


def main():
    G.estilo()
    dados = {b: carrega(b) for b in BASES}
    rps, prev, dose, varcomp, sens, idade_rows, h37, h38 = [], [], [], [], [], [], [], []
    ajustados = {}   # (base, x) -> Ajuste do modelo ajustado

    for b, cfg in BASES.items():
        y, des = cfg["y"], cfg["desenho"]
        for x in EXPOS:
            d = amostra(dados[b], y, x)
            prev += prevalencias(b, d, y, x, des.get("peso"))
            info = dict(base=b, exposicao=EXPOS[x], desfecho=y)
            for nome, form in [("bruta", f"{y} ~ C(expo)"), ("só idade", f"{y} ~ C(expo) + C(faixa_etaria)"),
                               ("ajustada", f"{y} ~ C(expo) + {COV}")]:
                aj = poisson_desenho(d, form, **des, compara_cluster=(nome == "ajustada"))
                for cat in (1, 2):
                    rps.append(linha_rp(aj, f"C(expo)[T.{cat}]", **info, modelo=nome, comparacao=f"{cat} vs 0"))
                if nome == "ajustada":
                    ajustados[(b, x)] = aj
                    # T040: comparação com o EP de cluster do statsmodels e com o EP do modelo (sem desenho)
                    i = aj.nomes.index("C(expo)[T.2]")
                    ingenuo = poisson_desenho(d, form)  # sem peso, sem desenho, sanduíche individual
                    import statsmodels.api as sm, patsy
                    yy, XX = patsy.dmatrices(form, d, return_type="dataframe")
                    w = d[des["peso"]].values
                    mb = sm.GLM(yy.iloc[:, 0], XX, family=sm.families.Poisson(), var_weights=w / w.mean()).fit()
                    varcomp.append(dict(base=b, exposicao=EXPOS[x], termo="C(expo)[T.2]",
                                        ep_linearizacao=aj.ep()[i],
                                        ep_cluster_statsmodels=(np.sqrt(np.diag(aj.cov_cluster_sm))[i]
                                                                if aj.cov_cluster_sm is not None else np.nan),
                                        ep_modelo_poisson_ponderado=float(mb.bse.iloc[i]),
                                        ep_robusto_sem_peso=ingenuo.ep()[i], variancia=aj.metodo,
                                        gl_desenho=aj.gl))
            # H3.4 dose-resposta: escore 0/1/2 como termo linear
            aj = poisson_desenho(d, f"{y} ~ expo + {COV}", **des)
            dose.append(linha_rp(aj, "expo", **info, modelo="ajustada, escore 0/1/2", comparacao="por faixa"))
            # sensibilidades
            dep = "dep" if b != "vigitel2024" else "depressao_diag"
            d2 = dados[b].copy()
            if b != "vigitel2024":
                d2["dep"] = (d2.depressao_phq9 >= 10).astype(float).where(d2.depressao_phq9.notna())
            dd = amostra(d2, y, x, extra=(dep,))
            aj = poisson_desenho(dd, f"{y} ~ C(expo) + {COV} + {dep}", **des)
            sens.append(linha_rp(aj, "C(expo)[T.2]", **info, modelo="ajustada + depressão",
                                 comparacao="2 vs 0", nota="PHQ-9 ≥ 10" if dep == "dep" else "diagnóstico referido"))
            aj = poisson_desenho(d, f"{y} ~ C(expo) + {COV}",
                                 **({"estrato": des["estrato"], "upa": des["upa"]} if "upa" in des else {}))
            sens.append(linha_rp(aj, "C(expo)[T.2]", **info, modelo="ajustada sem peso", comparacao="2 vs 0", nota=""))
            corte, rot = CORTE_ALT[b]
            dc = dados[b].dropna(subset=[ORD[x]]).copy()
            dc = dc[(dc[ORD[x]] >= corte) | (dc[ORD[x]] <= 1)]
            dc["alta"] = (dc[ORD[x]] >= corte).astype(float)
            dc = dc.dropna(subset=[y, *COVARS]).reset_index(drop=True)
            aj = poisson_desenho(dc, f"{y} ~ alta + {COV}", **des)
            sens.append(linha_rp(aj, "alta", **info, modelo="ajustada, corte alternativo",
                                 comparacao=f"{rot} vs não usa ou < 1 h", nota=rot))
            # H3.7 interação faixa etária × tela (só para a exposição digital entra na família 2)
            aj = poisson_desenho(d, f"{y} ~ C(expo) * C(faixa_etaria) + sexo + C(escolaridade3)", **des)
            termos = [t for t in aj.nomes if ":" in t]
            w = aj.wald(termos)
            h37.append(dict(base=b, exposicao=EXPOS[x], **w, n=aj.n, n_param=aj.n_param, gl_desenho=aj.gl))
            for fx in FAIXAS:
                # domínio: ajusta na faixa, variância com todas as UPAs e estratos do desenho
                ajf = poisson_desenho(d.assign(dom=(d.faixa_etaria == fx)), f"{y} ~ C(expo) + sexo + C(escolaridade3)",
                                      **des, dominio="dom")
                idade_rows.append(linha_rp(ajf, "C(expo)[T.2]", **info, modelo=f"ajustada, faixa {fx} (domínio)",
                                           comparacao="2 vs 0", faixa=fx))
        # H3.8: TV e digital no mesmo modelo, contraste β_TV(2) − β_digital(2)
        d = dados[b].dropna(subset=[y, "tela_digital_cat", "tela_tv_cat", *COVARS]).reset_index(drop=True)
        d["dig"], d["tv"] = d.tela_digital_cat.astype(int), d.tela_tv_cat.astype(int)
        aj = poisson_desenho(d, f"{y} ~ C(dig) + C(tv) + {COV}", **des)
        L = np.zeros(len(aj.nomes))
        L[aj.nomes.index("C(tv)[T.2]")], L[aj.nomes.index("C(dig)[T.2]")] = 1, -1
        w = aj.wald(contraste=L)
        dif = float(L @ aj.beta)
        ep = float(np.sqrt(L @ aj.cov @ L))
        q = stats.t.ppf(0.975, aj.gl) if aj.gl else 1.959964
        h38.append(dict(base=b, rp_tv=np.exp(aj.beta[aj.nomes.index("C(tv)[T.2]")]),
                        rp_digital=np.exp(aj.beta[aj.nomes.index("C(dig)[T.2]")]),
                        razao_tv_digital=np.exp(dif), ic_inf=np.exp(dif - q * ep), ic_sup=np.exp(dif + q * ep),
                        **w, n=aj.n, n_param=aj.n_param, gl_desenho=aj.gl))

    rps, prev, dose, sens = map(pd.DataFrame, (rps, prev, dose, sens))
    idade_df, h37, h38, varcomp = map(pd.DataFrame, (idade_rows, h37, h38, varcomp))

    # H3.6 e H3.9: comparações entre bases
    comp = []
    def ztest(b1, b2, x):
        a1, a2 = ajustados[(b1, x)], ajustados[(b2, x)]
        i1, i2 = a1.nomes.index("C(expo)[T.2]"), a2.nomes.index("C(expo)[T.2]")
        dif = a2.beta[i2] - a1.beta[i1]
        ep = np.sqrt(a1.cov[i1, i1] + a2.cov[i2, i2])
        z = dif / ep
        return dict(razao=np.exp(dif), ic_inf=np.exp(dif - 1.959964 * ep), ic_sup=np.exp(dif + 1.959964 * ep),
                    estatistica=z, p=2 * stats.norm.sf(abs(z)), tipo="z", gl1=None, gl2=None)
    for x in EXPOS:
        # base empilhada Vigitel + NHANES, pesos reescalados para somar o n de cada base
        partes = []
        for b, eua in (("vigitel2024", 0), ("nhanes0506", 1)):
            d = amostra(dados[b], BASES[b]["y"], x)
            d["peso_r"] = d.peso * len(d) / d.peso.sum()
            d["eua"] = eua
            if eua:
                d["est_e"] = "N" + d.estrato.astype(int).astype(str)
                d["upa_e"] = d.est_e + "_" + d.upa.astype(int).astype(str)
            else:
                d["est_e"] = "V"
                d["upa_e"] = "V_" + d.index.astype(str)
            partes.append(d[["dif_adormecer_freq", "expo", *COVARS, "peso_r", "eua", "est_e", "upa_e"]])
        st = pd.concat(partes, ignore_index=True)
        aj0 = poisson_desenho(st, f"dif_adormecer_freq ~ C(expo) + {COV} + eua + eua:C(expo)",
                              peso="peso_r", estrato="est_e", upa="upa_e")
        # gl mostrado = gl de desenho do NHANES (UPAs − estratos = 15): a variância da interação vem quase
        # toda do NHANES; o gl total da base empilhada (~27 mil) seria otimista. Satterthwaite registrado.
        gl_nh = ajustados[("nhanes0506", x)].gl
        gl_satt = aj0.satterthwaite("eua:C(expo)[T.2]")
        aj = aj0.com_gl(gl_nh)
        t2 = aj.termo("eua:C(expo)[T.2]")
        p_satt = float(2 * stats.t.sf(abs(t2["estatistica"]), gl_satt))
        conj = aj.wald([t for t in aj.nomes if t.startswith("eua:")])
        zt = ztest("vigitel2024", "nhanes0506", x)
        comp.append(dict(hipotese="H3.6", exposicao=EXPOS[x], comparacao="NHANES ÷ Vigitel (RP de tela alta)",
                         metodo="interação país × tela na base empilhada (1 gl, categoria 2)",
                         razao=t2["rp"], ic_inf=t2["ic_inf"], ic_sup=t2["ic_sup"], estatistica=t2["estatistica"],
                         tipo="t", gl1=1, gl2=aj.gl, p=t2["p"], n=aj.n, n_param=aj.n_param,
                         gl_satterthwaite=gl_satt, p_satterthwaite=p_satt, gl_base_empilhada=aj0.gl))
        comp.append(dict(hipotese="H3.6", exposicao=EXPOS[x], comparacao="NHANES ÷ Vigitel",
                         metodo="interação conjunta (2 gl)", razao=np.nan, ic_inf=np.nan, ic_sup=np.nan,
                         estatistica=conj["estatistica"], tipo=conj["tipo"], gl1=conj["gl1"], gl2=conj["gl2"],
                         p=conj["p"], n=aj.n, n_param=aj.n_param, gl_satterthwaite=np.nan, gl_base_empilhada=aj0.gl))
        comp.append(dict(hipotese="H3.6", exposicao=EXPOS[x], comparacao="NHANES ÷ Vigitel",
                         metodo="z da diferença dos log-RP (modelos separados)", **zt, n=np.nan))
        comp.append(dict(hipotese="H3.9", exposicao=EXPOS[x], comparacao="Vigitel ÷ PNS (RP de tela alta)",
                         metodo="z da diferença dos log-RP (modelos separados)", **ztest("pns2019", "vigitel2024", x),
                         n=np.nan))
        # sensibilidade: H3.6 com os modelos ajustados sem peso
        sv = sens[(sens.modelo == "ajustada sem peso") & (sens.exposicao == EXPOS[x])].set_index("base")
        dif = sv.loc["nhanes0506", "beta"] - sv.loc["vigitel2024", "beta"]
        ep = np.sqrt(sv.loc["nhanes0506", "ep"] ** 2 + sv.loc["vigitel2024", "ep"] ** 2)
        comp.append(dict(hipotese="H3.6 (sensibilidade)", exposicao=EXPOS[x], comparacao="NHANES ÷ Vigitel",
                         metodo="z da diferença dos log-RP, modelos ajustados SEM peso", razao=np.exp(dif),
                         ic_inf=np.exp(dif - 1.959964 * ep), ic_sup=np.exp(dif + 1.959964 * ep),
                         estatistica=dif / ep, p=2 * stats.norm.sf(abs(dif / ep)), tipo="z", gl1=None, gl2=None,
                         n=np.nan))
    comp = pd.DataFrame(comp)

    # exploratório: desvio da linearidade no log (β1 = β2/2 sob tendência linear com escores 0/1/2)
    lin = []
    for (b, x), aj in ajustados.items():
        L = np.zeros(len(aj.nomes))
        L[aj.nomes.index("C(expo)[T.1]")], L[aj.nomes.index("C(expo)[T.2]")] = 1, -0.5
        w = aj.wald(contraste=L)
        lin.append(dict(base=b, exposicao=EXPOS[x], teste="desvio da linearidade (β1 − β2/2 = 0) — exploratório",
                        rp_1_vs_0=np.exp(aj.beta[aj.nomes.index("C(expo)[T.1]")]),
                        rp_2_vs_0=np.exp(aj.beta[aj.nomes.index("C(expo)[T.2]")]), **w, n=aj.n))
    lin = pd.DataFrame(lin)

    # ---------- tabela de hipóteses com Holm ----------
    nome_h = {"vigitel2024": "H3.1", "pns2019": "H3.2", "nhanes0506": "H3.3"}
    H = []
    for x, rot in EXPOS.items():
        fam = f"1 ({rot})"
        for b in BASES:
            r = rps[(rps.base == b) & (rps.exposicao == rot) & (rps.modelo == "ajustada") & (rps.comparacao == "2 vs 0")].iloc[0]
            H.append(dict(familia=fam, hipotese=nome_h[b], base=b, exposicao=rot,
                          descricao=f"RP de {BASES[b]['desfecho']}, tela {rot} ≥ 3 h vs < 1 h, ajustada",
                          h0="RP = 1", estimativa=r.rp, ic_inf=r.ic_inf, ic_sup=r.ic_sup, estatistica=r.estatistica,
                          tipo_estat=r.tipo_estat, gl1=None, gl2=r.gl, p=r.p, n=r.n,
                          n_param=r.n_param, gl_desenho=r.gl))
        for b in BASES:
            r = dose[(dose.base == b) & (dose.exposicao == rot)].iloc[0]
            H.append(dict(familia=fam, hipotese="H3.4", base=b, exposicao=rot,
                          descricao="tendência dose-resposta: RP por faixa de exposição (escore 0/1/2), ajustada",
                          h0="sem tendência (β = 0)", estimativa=r.rp, ic_inf=r.ic_inf, ic_sup=r.ic_sup,
                          estatistica=r.estatistica, tipo_estat=r.tipo_estat, gl1=None, gl2=r.gl, p=r.p, n=r.n,
                          n_param=r.n_param, gl_desenho=r.gl))
    r = comp[(comp.hipotese == "H3.6") & (comp.exposicao == "digital") & comp.metodo.str.startswith("interação país")].iloc[0]
    H.append(dict(familia="2", hipotese="H3.6", base="vigitel2024 + nhanes0506", exposicao="digital",
                  descricao="RP de tela digital alta difere entre EUA e Brasil (razão NHANES ÷ Vigitel)",
                  h0="RP_BR = RP_EUA", estimativa=r.razao, ic_inf=r.ic_inf, ic_sup=r.ic_sup,
                  estatistica=r.estatistica, tipo_estat="t", gl1=1, gl2=r.gl2, p=r.p, n=r.n,
                  n_param=r.n_param, gl_desenho=r.gl2))
    for b in BASES:
        r = h37[(h37.base == b) & (h37.exposicao == "digital")].iloc[0]
        rr = idade_df[(idade_df.base == b) & (idade_df.exposicao == "digital")]
        H.append(dict(familia="2", hipotese="H3.7", base=b, exposicao="digital",
                      descricao="RP de tela digital alta difere entre faixas etárias (interação idade × tela)",
                      h0="sem interação", estimativa=np.nan, ic_inf=rr.rp.min(), ic_sup=rr.rp.max(),
                      estatistica=r.estatistica, tipo_estat=r.tipo, gl1=r.gl1, gl2=r.gl2, p=r.p, n=r.n,
                      n_param=r.n_param, gl_desenho=r.gl_desenho))
    for b in BASES:
        r = h38[h38.base == b].iloc[0]
        H.append(dict(familia="2", hipotese="H3.8", base=b, exposicao="TV × digital",
                      descricao="RP da TV alta difere da RP da tela digital alta (mesmo modelo; razão TV ÷ digital)",
                      h0="RP_TV = RP_digital", estimativa=r.razao_tv_digital, ic_inf=r.ic_inf, ic_sup=r.ic_sup,
                      estatistica=r.estatistica, tipo_estat=r.tipo, gl1=r.gl1, gl2=r.gl2, p=r.p, n=r.n,
                      n_param=r.n_param, gl_desenho=r.gl_desenho))
    r = comp[(comp.hipotese == "H3.9") & (comp.exposicao == "digital")].iloc[0]
    H.append(dict(familia="2", hipotese="H3.9", base="pns2019 × vigitel2024", exposicao="digital",
                  descricao="RP de tela digital alta difere entre PNS e Vigitel (razão Vigitel ÷ PNS)",
                  h0="RP_PNS = RP_Vigitel", estimativa=r.razao, ic_inf=r.ic_inf, ic_sup=r.ic_sup,
                  estatistica=r.estatistica, tipo_estat="z", gl1=None, gl2=None, p=r.p, n=np.nan))
    H = pd.DataFrame(H)
    H["p_holm"] = np.nan
    for fam, idx in H.groupby("familia").groups.items():
        H.loc[idx, "p_holm"] = holm(H.loc[idx, "p"].values)
    H["decisao"] = H.p_holm.apply(decisao)
    H["nota"] = np.where(H.hipotese.isin(["H3.7"]), "ic_inf/ic_sup = menor e maior RP entre as faixas etárias", "")
    # sensibilidade: regra de gl do svyglm (d − p + 1) no lugar de UPAs − estratos, Holm refeito por família
    ps = [p_svyglm(r.estatistica, r.tipo_estat, r.gl1, r.gl_desenho, r.n_param) for r in H.itertuples()]
    H["p_svyglm"] = [a if not pd.isna(a) else r.p for a, r in zip((x[0] for x in ps), H.itertuples())]
    H["gl2_svyglm"] = [x[1] for x in ps]
    H["nota_svyglm"] = [("não calculável: d − p + 1 < q; Holm usa o p da regra principal"
                         if (pd.isna(a) and not pd.isna(g)) else "") for (a, g) in ps]
    H["p_holm_svyglm"] = np.nan
    for fam, idx in H.groupby("familia").groups.items():
        H.loc[idx, "p_holm_svyglm"] = holm(H.loc[idx, "p_svyglm"].values)
    H["decisao_svyglm"] = H.p_holm_svyglm.apply(decisao)
    linhas_gl = H[H.hipotese.isin(["H3.1", "H3.2", "H3.3"]) & H.gl_desenho.notna()]
    extra = [dict(base=r.base, exposicao=r.exposicao, desfecho=BASES[r.base]["y"],
                  modelo="ajustada, gl pela regra do svyglm (d − p + 1)", comparacao="2 vs 0",
                  termo="C(expo)[T.2]", rp=r.estimativa, ic_inf=np.nan, ic_sup=np.nan, estatistica=r.estatistica,
                  tipo_estat="t", gl=r.gl2_svyglm, p=r.p_svyglm, n=r.n, hipotese=r.hipotese,
                  p_holm_familia=r.p_holm_svyglm, decisao_familia=r.decisao_svyglm,
                  nota=f"regra principal: gl = {int(r.gl_desenho)}, p Holm {r.p_holm:.4f}")
             for r in linhas_gl.itertuples()]
    sens = pd.concat([sens, pd.DataFrame(extra)], ignore_index=True)

    salva_csv(H, T / "hipoteses.csv")
    salva_csv(rps, T / "rp_bruta_ajustada.csv")
    salva_csv(prev, T / "prevalencias.csv")
    salva_csv(dose, T / "dose_resposta.csv")
    salva_csv(lin, T / "desvio_linearidade_exploratorio.csv")
    salva_csv(sens, T / "sensibilidade.csv")
    salva_csv(idade_df, T / "rp_por_faixa_etaria.csv")
    salva_csv(h37, T / "interacao_idade.csv")
    salva_csv(h38, T / "tv_vs_digital.csv")
    salva_csv(comp, T / "comparacoes_entre_bases.csv")
    salva_csv(varcomp, T / "comparacao_variancia.csv")
    figuras(rps, idade_df, prev)
    print(H[["familia", "hipotese", "base", "exposicao", "estimativa", "ic_inf", "ic_sup", "p", "p_holm", "decisao"]]
          .round(4).to_string())


def figuras(rps, idade_df, prev):
    import matplotlib.pyplot as plt
    # 1. RP bruta e ajustada por base e exposição
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ordem = [(b, e) for b in BASES for e in ("digital", "TV")]
    for i, (b, e) in enumerate(ordem):
        cor = G.COR_PAIS[G.PAIS_BASE[b]]
        for modelo, desloc, mk, fc in (("bruta", 0.18, "o", "white"), ("ajustada", -0.18, "o", cor)):
            r = rps[(rps.base == b) & (rps.exposicao == e) & (rps.modelo == modelo) & (rps.comparacao == "2 vs 0")].iloc[0]
            y = len(ordem) - 1 - i + desloc
            ax.plot([r.ic_inf, r.ic_sup], [y, y], color=cor, lw=1.6)
            ax.plot(r.rp, y, mk, mfc=fc, mec=cor, ms=7, mew=1.6)
            if modelo == "ajustada":
                ax.text(r.ic_sup * 1.02, y, f"{r.rp:.2f} ({r.ic_inf:.2f}–{r.ic_sup:.2f})".replace(".", ","),
                        va="center", fontsize=8)
    ax.axvline(1, color=G.COR_NEUTRA, lw=1, ls="--")
    ax.set_yticks(range(len(ordem)))
    ax.set_yticklabels([f"{G.NOME_BASE[b]} — {e}" for b, e in ordem][::-1])
    ax.set_xscale("log")
    ax.set_xticks([0.8, 1, 1.25, 1.5, 2])
    ax.set_xticklabels(["0,8", "1", "1,25", "1,5", "2"])
    ax.set_xlim(0.75, 2.9)
    ax.set_xlabel("Razão de prevalências, tela ≥ 3 h vs < 1 h (escala log; IC 95% com desenho amostral)")
    ax.plot([], [], "o", mfc="white", mec="k", label="bruta")
    ax.plot([], [], "o", mfc="k", mec="k", label="ajustada (idade, sexo, escolaridade)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, fontsize=8)
    ax.set_title("Problema de sono frequente com tela alta: Brasil × EUA")
    G.salva(fig, F / "rp_por_pais.png")

    # 2. RP por faixa etária (tela digital)
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for j, b in enumerate(BASES):
        r = idade_df[(idade_df.base == b) & (idade_df.exposicao == "digital")].set_index("faixa").loc[FAIXAS]
        xs = np.arange(4) + (j - 1) * 0.12
        cor = G.COR_PAIS[G.PAIS_BASE[b]]
        ls = "-" if b != "pns2019" else ":"
        ax.errorbar(xs, r.rp, yerr=[r.rp - r.ic_inf, r.ic_sup - r.rp], fmt="o", ls=ls, color=cor, capsize=3,
                    label=G.NOME_BASE[b], mfc=cor if b != "pns2019" else "white")
    ax.axhline(1, color=G.COR_NEUTRA, lw=1, ls="--")
    ax.set_xticks(range(4))
    ax.set_xticklabels(FAIXAS)
    ax.set_yscale("log")
    ax.set_yticks([0.5, 0.75, 1, 1.5, 2, 3])
    ax.set_yticklabels(["0,5", "0,75", "1", "1,5", "2", "3"])
    ax.minorticks_off()
    ax.set_xlabel("Faixa etária (anos)")
    ax.set_ylabel("RP tela digital ≥ 3 h vs < 1 h")
    ax.legend(fontsize=8)
    ax.set_title("A associação por faixa etária (H3.7)")
    G.salva(fig, F / "rp_por_faixa_etaria.png")

    # 3. prevalência ponderada por faixa de tela
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.4), sharey=True)
    for ax, e in zip(axes, ("digital", "TV")):
        for j, b in enumerate(BASES):
            r = prev[(prev.base == b) & (prev.exposicao == e)].sort_values("categoria")
            ax.bar(r.categoria + (j - 1) * 0.27, r.prevalencia_ponderada * 100, width=0.26,
                   color=G.COR_PAIS[G.PAIS_BASE[b]], alpha=1 if b != "pns2019" else 0.55, label=G.NOME_BASE[b])
        ax.set_xticks([0, 1, 2])
        ax.set_xticklabels(["< 1 h", "1 a < 3 h", "≥ 3 h"])
        ax.set_title(f"Tela {e}")
    axes[0].set_ylabel("Prevalência ponderada (%)")
    axes[1].legend(fontsize=7)
    fig.suptitle("Problema de sono frequente por tempo de tela (desfechos diferem entre bases)", fontsize=10)
    G.salva(fig, F / "prevalencia_por_faixa_tela.png")


if __name__ == "__main__":
    main()
