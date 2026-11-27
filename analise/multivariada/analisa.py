"""T022–T031 — PCA por SVD e análise fatorial dos conjuntos de itens (spec 002).

2026-11-27: EUA (NHANES 2005-06) fora do trabalho; H2.2–H2.4 retiradas (sem comparação entre países).

Uso:  python -m analise.multivariada.analisa
Saídas: resultados/002/tabelas/*.csv, resultados/002/figuras/*.png, analise/dados/processados/escores_<base>.parquet

Regra do número de fatores (plano 002): decide a análise paralela de Horn (autovalor observado acima do
percentil 95 de 1.000 matrizes aleatórias de mesmo n e p, contando a partir do primeiro); Kaiser (λ > 1)
e o scree entram como apoio e a divergência é registrada.
"""
from __future__ import annotations

import time

import numpy as np
import pandas as pd

from analise.comum import caminhos
from analise.comum import multivariada as mv
from analise.comum.estatistica import salva_csv
from analise.comum.graficos import COR_PAIS, NOME_BASE, PAIS_BASE, estilo, salva
from analise.multivariada.conjuntos import (CONJUNTOS, INSONIA_VIGITEL_ORIGEM, NOTA_RETIRADA, PARES_TUCKER,
                                            POLICORICA, POR_ID, RETIRADAS)

import matplotlib.pyplot as plt

OUT = caminhos.saida("002")
TAB, FIG = OUT / "tabelas", OUT / "figuras"
SEMENTE = 2026
REPS = 1000


def classifica_tucker(phi: float) -> str:
    """Lorenzo-Seva e ten Berge (2006): > 0,95 iguais; 0,85–0,94 similaridade razoável."""
    a = abs(phi)
    return "equivalente (≥ 0,95)" if a >= 0.95 else ("similar (0,85–0,94)" if a >= 0.85 else "diferente (< 0,85)")


def analisa_conjunto(c: dict, i: int, dados: dict) -> dict:
    t0 = time.time()
    df = dados[c["base"]]
    cols = c["itens"] + (["peso"] if c["peso"] else [])
    d = df[["id"] + cols].dropna()
    X = d[c["itens"]].to_numpy(float)
    n, p = X.shape
    R = np.corrcoef(X, rowvar=False)
    pca = mv.pca_svd(X)
    pa = mv.analise_paralela(n, p, reps=REPS, semente=SEMENTE + i)
    k_kaiser = int((pca["autovalores"] > 1).sum())
    k_pa = mv.n_retidos(pca["autovalores"], pa["p95"])
    k = k_pa
    kmo_g, msa = mv.kmo(R)
    chi2, gl, pb = mv.bartlett(R, n)
    alfa = mv.alfa_cronbach(X)

    ml1 = mv.af_ml(R, 1)
    pa1 = mv.af_eixos_principais(R, 1)
    solucoes = [("ml", "nenhuma", 1, ml1["cargas"], None), ("eixos principais", "nenhuma", 1, pa1["cargas"], None)]
    phis = []
    if k >= 2:
        for nome, f in (("ml", mv.af_ml), ("eixos principais", mv.af_eixos_principais)):
            Lk = f(R, k)["cargas"]
            solucoes.append((nome, "nenhuma", k, Lk, None))
            v, _ = mv.varimax(Lk)
            solucoes.append((nome, "varimax", k, v, None))
            o, Phi, _ = mv.oblimin(Lk)
            solucoes.append((nome, "oblimin", k, o, Phi))
            for a in range(k):
                for b in range(a + 1, k):
                    phis.append(dict(conjunto=c["id"], metodo=nome, k=k, fator_a=f"F{a+1}", fator_b=f"F{b+1}", phi=Phi[a, b]))
    # H2.4: solução exploratória de 2 fatores para o PHQ-9 mesmo se a análise paralela retiver 1
    if c["instrumento"] == "phq9" and k < 2:
        L2 = mv.af_ml(R, 2)["cargas"]
        o, Phi, _ = mv.oblimin(L2)
        solucoes.append(("ml", "oblimin (exploratória, 2 fatores)", 2, o, Phi))
        phis.append(dict(conjunto=c["id"], metodo="ml (exploratória)", k=2, fator_a="F1", fator_b="F2", phi=Phi[0, 1]))

    # escores: 1º componente, fator único (regressão de Thurstone), soma simples
    Z = pca["Z"]
    pc1 = pca["escores"][:, 0] / np.sqrt(pca["autovalores"][0])
    af1 = mv.escores_regressao(Z, R, ml1["cargas"])[:, 0]
    soma = X.sum(axis=1)
    r = lambda a, b: float(np.corrcoef(a, b)[0, 1])

    # robustez: policórica e ponderada
    rob = [dict(conjunto=c["id"], correlacao="Pearson", n=n, lambda1=pca["autovalores"][0],
                var1=pca["variancia"][0], k_kaiser=k_kaiser, alfa=alfa,
                **{f"carga_{j+1}": ml1["cargas"][j, 0] for j in range(p)}, tucker_vs_pearson=1.0)]
    cargas_alt = {}
    if c["id"] in POLICORICA:
        Rp = mv.policorica(X.astype(int))
        lp = np.sort(np.linalg.eigvalsh(Rp))[::-1]
        mlp = mv.af_ml(Rp, 1)["cargas"][:, 0]
        cargas_alt["policórica"] = mlp
        rob.append(dict(conjunto=c["id"], correlacao="policórica", n=n, lambda1=lp[0], var1=lp[0] / p,
                        k_kaiser=int((lp > 1).sum()), alfa=np.nan,
                        **{f"carga_{j+1}": mlp[j] for j in range(p)}, tucker_vs_pearson=mv.tucker(mlp, ml1["cargas"][:, 0])))
        salva_csv(pd.DataFrame(Rp, index=c["itens"], columns=c["itens"]).reset_index(names="item"),
                  TAB / f"correlacao_policorica_{c['id']}.csv")
    if c["peso"]:
        Rw = mv.correlacao_ponderada(X, d["peso"].to_numpy(float))
        lw = np.sort(np.linalg.eigvalsh(Rw))[::-1]
        mlw = mv.af_ml(Rw, 1)["cargas"][:, 0]
        cargas_alt["ponderada"] = mlw
        rob.append(dict(conjunto=c["id"], correlacao="ponderada pelo peso amostral", n=n, lambda1=lw[0], var1=lw[0] / p,
                        k_kaiser=int((lw > 1).sum()), alfa=np.nan,
                        **{f"carga_{j+1}": mlw[j] for j in range(p)}, tucker_vs_pearson=mv.tucker(mlw, ml1["cargas"][:, 0])))

    Lk_ml = next(s[3] for s in solucoes if s[0] == "ml" and s[2] == k and s[1] == "nenhuma")
    var_comum_k = float((Lk_ml ** 2).sum() / p)
    print(f"  {c['id']}: n={n} p={p} λ1={pca['autovalores'][0]:.3f} k_PA={k_pa} k_Kaiser={k_kaiser} "
          f"KMO={kmo_g:.3f} α={alfa:.3f} ({time.time()-t0:.1f}s)")
    return dict(c=c, d=d, X=X, n=n, p=p, R=R, pca=pca, pa=pa, k=k, k_kaiser=k_kaiser, k_pa=k_pa, kmo=kmo_g, msa=msa,
                bartlett=(chi2, gl, pb), alfa=alfa, alfa_sem=mv.alfa_sem_item(X), item_total=mv.correlacao_item_total(X),
                ml1=ml1, solucoes=solucoes, phis=phis, var_comum_k=var_comum_k,
                escores=dict(pc1=pc1, af=af1, soma=soma),
                r=dict(pc1_af=r(pc1, af1), pc1_soma=r(pc1, soma), af_soma=r(af1, soma)),
                robustez=rob, cargas_alt=cargas_alt)


def tabelas(res: list[dict]):
    ad, it, av, cg, ph, es, rb = [], [], [], [], [], [], []
    for z in res:
        c = z["c"]
        chi2, gl, pb = z["bartlett"]
        ad.append(dict(conjunto=c["id"], base=c["base"], instrumento=c["nome"], n=z["n"], p=z["p"], alfa=z["alfa"],
                       kmo=z["kmo"], bartlett_chi2=chi2, bartlett_gl=gl, bartlett_p=pb,
                       lambda1=z["pca"]["autovalores"][0], var_pc1=z["pca"]["variancia"][0],
                       k_kaiser=z["k_kaiser"], k_paralela=z["k_pa"], k_decidido=z["k"],
                       var_comum_af=z["var_comum_k"], var_comum_af1=float((z["ml1"]["cargas"] ** 2).sum() / z["p"])))
        desc = z["d"][c["itens"]]
        for j, (item, rot) in enumerate(zip(c["itens"], c["rotulos"])):
            it.append(dict(conjunto=c["id"], item=item, rotulo=rot, n=z["n"], media=desc[item].mean(), dp=desc[item].std(),
                           minimo=desc[item].min(), maximo=desc[item].max(), msa=z["msa"][j],
                           alfa_sem_item=z["alfa_sem"][j], r_item_total=z["item_total"][j],
                           carga_pc1=z["pca"]["cargas"][j, 0], carga_af1_ml=z["ml1"]["cargas"][j, 0],
                           comunalidade_af1=z["ml1"]["comunalidades"][j]))
        acum = np.cumsum(z["pca"]["variancia"])
        for j in range(z["p"]):
            av.append(dict(conjunto=c["id"], componente=j + 1, valor_singular=z["pca"]["sigma"][j],
                           autovalor=z["pca"]["autovalores"][j], variancia=z["pca"]["variancia"][j], variancia_acum=acum[j],
                           p95_aleatorio=z["pa"]["p95"][j], media_aleatoria=z["pa"]["media"][j]))
        for metodo, rot, k, L, Phi in z["solucoes"]:
            h2 = (L @ (Phi if Phi is not None else np.eye(k)) * L).sum(axis=1)
            for j, (item, rotl) in enumerate(zip(c["itens"], c["rotulos"])):
                cg.append(dict(conjunto=c["id"], metodo=metodo, rotacao=rot, k=k, item=item, rotulo=rotl,
                               **{f"F{f+1}": L[j, f] for f in range(k)}, comunalidade=h2[j], unicidade=1 - h2[j]))
        ph += z["phis"]
        es.append(dict(conjunto=c["id"], n=z["n"], r_pc1_af=z["r"]["pc1_af"], r_pc1_soma=z["r"]["pc1_soma"],
                       r_af_soma=z["r"]["af_soma"]))
        rb += z["robustez"]
        salva_csv(pd.DataFrame(z["R"], index=c["itens"], columns=c["itens"]).reset_index(names="item"),
                  TAB / f"correlacao_{c['id']}.csv")
    salva_csv(pd.DataFrame(ad), TAB / "adequacao.csv")
    salva_csv(pd.DataFrame(it), TAB / "itens.csv")
    salva_csv(pd.DataFrame(av), TAB / "pca_autovalores.csv")
    salva_csv(pd.DataFrame(cg), TAB / "af_cargas.csv")
    salva_csv(pd.DataFrame(ph), TAB / "af_phi.csv")
    salva_csv(pd.DataFrame(es), TAB / "escores_correlacao.csv")
    salva_csv(pd.DataFrame(rb), TAB / "robustez.csv")
    return pd.DataFrame(ad), pd.DataFrame(es)


def tucker_e_h24(por_id: dict) -> pd.DataFrame:
    linhas = []
    for a, b, h in PARES_TUCKER:
        za, zb = por_id[a], por_id[b]
        sols = [("AF ML 1 fator (Pearson)", za["ml1"]["cargas"][:, 0], zb["ml1"]["cargas"][:, 0]),
                ("PCA 1º componente", za["pca"]["cargas"][:, 0], zb["pca"]["cargas"][:, 0])]
        for alt in ("policórica", "ponderada"):
            if alt in za["cargas_alt"] and alt in zb["cargas_alt"]:
                sols.append((f"AF ML 1 fator ({alt})", za["cargas_alt"][alt], zb["cargas_alt"][alt]))
        for nome, la, lb in sols:
            phi = mv.tucker(la, lb)
            linhas.append(dict(hipotese=h, instrumento=za["c"]["nome"], base_a=za["c"]["base"], base_b=zb["c"]["base"],
                               solucao=nome, fator="F1", phi=phi, classificacao=classifica_tucker(phi),
                               dif_max_carga=float(np.max(np.abs(la - lb)))))
        # soluções de 2 fatores (retidas ou exploratórias): casar fatores pela maior congruência
        s2a = [s for s in za["solucoes"] if s[2] == 2 and "oblimin" in s[1] and s[0] == "ml"]
        s2b = [s for s in zb["solucoes"] if s[2] == 2 and "oblimin" in s[1] and s[0] == "ml"]
        if s2a and s2b:
            La, Lb = s2a[0][3], s2b[0][3]
            direto = mv.tucker(La[:, 0], Lb[:, 0]) + mv.tucker(La[:, 1], Lb[:, 1])
            cruzado = mv.tucker(La[:, 0], Lb[:, 1]) + mv.tucker(La[:, 1], Lb[:, 0])
            casa = [(0, 0), (1, 1)] if direto >= cruzado else [(0, 1), (1, 0)]
            for fa, fb in casa:
                phi = mv.tucker(La[:, fa], Lb[:, fb])
                linhas.append(dict(hipotese=f"{h} (exploratória)", instrumento=za["c"]["nome"], base_a=za["c"]["base"],
                                   base_b=zb["c"]["base"], solucao=f"AF ML 2 fatores oblimin ({s2a[0][1]})",
                                   fator=f"{za['c']['base']} F{fa+1} × {zb['c']['base']} F{fb+1}", phi=phi,
                                   classificacao=classifica_tucker(phi),
                                   dif_max_carga=float(np.max(np.abs(La[:, fa] - Lb[:, fb])))))
    colunas = ["hipotese", "instrumento", "base_a", "base_b", "solucao", "fator", "phi", "classificacao", "dif_max_carga"]
    t = pd.DataFrame(linhas, columns=colunas)          # vazio desde 2026-11-27 (sem pares entre países)
    salva_csv(t, TAB / "tucker.csv")
    return t


def h24(por_id: dict) -> list[dict]:
    """Em que fator carrega o item de sono (phq3) do PHQ-9, na solução retida e na de 2 fatores."""
    out = []
    for cid in ("phq9_pns",):
        z = por_id[cid]
        for metodo, rot, k, L, Phi in z["solucoes"]:
            if metodo != "ml" or (k == 1 and rot != "nenhuma") or (k >= 2 and "oblimin" not in rot):
                continue
            j = z["c"]["itens"].index("phq3")
            f = int(np.argmax(np.abs(L[j])))
            # fator "somático" = o que concentra cansaço (phq4) e apetite (phq5)
            out.append(dict(conjunto=cid, solucao=f"ML {k} fator(es) {rot}", k=k,
                            fator_do_sono=f"F{f+1}", carga_sono=L[j, f],
                            fator_do_cansaco=f"F{int(np.argmax(np.abs(L[3])))+1}",
                            fator_do_humor=f"F{int(np.argmax(np.abs(L[1])))+1}"))
    salva_csv(pd.DataFrame(out), TAB / "phq9_item_sono.csv")
    return out


def exporta_escores(res: list[dict], dados: dict):
    por_base = {}
    for z in res:
        c = z["c"]
        e = pd.DataFrame({"id": z["d"]["id"].to_numpy(), f"{c['instrumento']}_pc1": z["escores"]["pc1"],
                          f"{c['instrumento']}_af": z["escores"]["af"], f"{c['instrumento']}_soma": z["escores"]["soma"]})
        por_base.setdefault(c["base"], []).append(e)
    for base, lista in por_base.items():
        out = dados[base][["id"]].copy()
        for e in lista:
            out = out.merge(e, on="id", how="left")
        out.to_parquet(caminhos.PROCESSADOS / f"escores_{base}.parquet", index=False)
        print(f"  escores_{base}.parquet: {len(out)} linhas, colunas {list(out.columns[1:])}")


def figuras(res: list[dict], por_id: dict, tucker: pd.DataFrame):
    estilo()
    # scree + análise paralela, todos os conjuntos
    ncol = 4
    nlin = int(np.ceil(len(res) / ncol))
    fig, axs = plt.subplots(nlin, ncol, figsize=(4.2 * ncol, 3.3 * nlin))
    axs = np.atleast_2d(axs)
    for ax in axs.ravel()[len(res):]:
        ax.set_visible(False)
    for ax, z in zip(axs.ravel(), res):
        c = z["c"]
        x = np.arange(1, z["p"] + 1)
        cor = COR_PAIS.get(PAIS_BASE[c["base"]], "#333")
        ax.plot(x, z["pca"]["autovalores"], "o-", color=cor, label="observado")
        ax.plot(x, z["pa"]["p95"], "s--", color="#7F7F7F", ms=3, label="aleatório P95 (Horn)")
        ax.axhline(1, color="#BBBBBB", lw=1, label="Kaiser λ = 1")
        ax.set_title(f"{c['nome']}\n{NOME_BASE[c['base']]} — retém {z['k']}", fontsize=9)
        ax.set_xticks(x)
        ax.set_xlabel("componente")
    for lin in range(nlin):
        axs[lin, 0].set_ylabel("autovalor")
    axs[0, 0].legend(fontsize=7)
    fig.suptitle("Scree e análise paralela: número de dimensões de cada conjunto de itens", y=1.0)
    fig.tight_layout()
    salva(fig, FIG / "scree_todos.png")

    # índice de insônia do Vigitel 2024: cargas na PCA e na AF, item a item
    z = por_id["insonia3_vigitel"]
    import textwrap
    rot = [textwrap.fill(r, 16) + f"\n({INSONIA_VIGITEL_ORIGEM[i][0]})" for i, r in zip(z["c"]["itens"], z["c"]["rotulos"])]
    x = np.arange(len(rot))
    br = lambda v: f"{v:.2f}".replace(".", ",")
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.bar(x - 0.2, z["pca"]["cargas"][:, 0], 0.4, color=COR_PAIS["Brasil"], label="PCA: carga no 1º componente")
    ax.bar(x + 0.2, z["ml1"]["cargas"][:, 0], 0.4, color="#56B4E9", label="Análise fatorial (ML): carga no fator")
    for j in range(len(rot)):
        ax.text(x[j] - 0.2, z["pca"]["cargas"][j, 0] + 0.02, br(z["pca"]["cargas"][j, 0]), ha="center", fontsize=8)
        ax.text(x[j] + 0.2, z["ml1"]["cargas"][j, 0] + 0.02, br(z["ml1"]["cargas"][j, 0]), ha="center", fontsize=8)
    ax.set_xticks(x, rot)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("carga (correlação item × fator)")
    v = z["pca"]["variancia"][0] * 100
    ax.set_title(f"Índice de insônia, Vigitel 2024: 1 fator explica {v:.0f}% da variância")
    n_txt = f"{z['n']:,}".replace(",", ".")
    ax.text(0.5, 0.985, f"α de Cronbach = {br(z['alfa'])} · KMO = {br(z['kmo'])} · n = {n_txt}",
            transform=ax.transAxes, ha="center", va="top", fontsize=8, color="#555555")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=2, fontsize=8)
    salva(fig, FIG / "cargas_insonia_vigitel.png")

    # biplot do PHQ-9 (PNS 2019): cargas nos 2 primeiros componentes
    z = por_id["phq9_pns"]
    L = z["pca"]["cargas"]
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    rng = np.random.default_rng(1)
    idx = rng.choice(z["n"], size=min(800, z["n"]), replace=False)
    sc = z["pca"]["escores"][idx, :2] / np.sqrt(z["pca"]["autovalores"][:2])
    ax.scatter(sc[:, 0] / np.abs(sc).max(), sc[:, 1] / np.abs(sc).max(), s=4, color="#BBBBBB", alpha=0.5,
               label="pessoas (amostra de 800, escores reescalados)")
    pos = [[L[j, 0] * 1.06, L[j, 1] * 1.06] for j in range(len(z["c"]["rotulos"]))]
    ordem = sorted(range(len(pos)), key=lambda j: pos[j][1])
    for a_, b_ in zip(ordem, ordem[1:]):
        if abs(pos[b_][0] - pos[a_][0]) < 0.35 and pos[b_][1] - pos[a_][1] < 0.07:
            pos[b_][1] = pos[a_][1] + 0.07
    for j, rotl in enumerate(z["c"]["rotulos"]):
        ax.arrow(0, 0, L[j, 0], L[j, 1], color=COR_PAIS["Brasil"], head_width=0.02, length_includes_head=True)
        ax.text(pos[j][0], pos[j][1], rotl, fontsize=8, va="center")
    ax.set_xlim(right=1.2)
    v = z["pca"]["variancia"]
    ax.set_xlabel(f"componente 1 ({v[0]*100:.0f}% da variância)")
    ax.set_ylabel(f"componente 2 ({v[1]*100:.0f}%)")
    ax.axhline(0, color="#999", lw=0.6)
    ax.axvline(0, color="#999", lw=0.6)
    ax.set_title("Biplot: PHQ-9, PNS 2019")
    ax.legend(fontsize=7, loc="lower left")
    salva(fig, FIG / "biplot_phq9_pns.png")

    # mapa de cargas das soluções com 2+ fatores (oblimin, ML)
    multi = [(zz, s) for zz in res for s in zz["solucoes"] if s[0] == "ml" and s[2] >= 2 and "oblimin" in s[1]]
    if multi:
        fig, axs = plt.subplots(1, len(multi), figsize=(4.4 * len(multi), 4.8), gridspec_kw={"wspace": 1.05})
        axs = np.atleast_1d(axs)
        for ax, (zz, s) in zip(axs, multi):
            L = s[3]
            im = ax.imshow(L, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
            ax.set_yticks(range(len(zz["c"]["rotulos"])), [r if len(r) <= 20 else r[:19] + "…" for r in zz["c"]["rotulos"]], fontsize=7)
            ax.set_xticks(range(L.shape[1]), [f"F{f+1}" for f in range(L.shape[1])])
            for (ii, jj), val in np.ndenumerate(L):
                ax.text(jj, ii, f"{val:.2f}".replace(".", ","), ha="center", va="center", fontsize=6.5)
            expl = " (exploratória)" if "explorat" in s[1] else ""
            ax.set_title(f"{zz['c']['nome']}{expl}\n{NOME_BASE[zz['c']['base']]}", fontsize=8)
            ax.grid(False)
        fig.colorbar(im, ax=axs, shrink=0.6, label="carga (padrão oblimin)")
        fig.suptitle("Soluções com 2 fatores (AF por ML, rotação oblimin)", y=1.02)
        salva(fig, FIG / "cargas_multifator.png")


def hipoteses(ad: pd.DataFrame, es: pd.DataFrame, tucker: pd.DataFrame, h24l: list, por_id: dict) -> pd.DataFrame:
    H = []
    a = ad.set_index("conjunto")
    cid = "insonia3_vigitel"
    z = por_id[cid]
    mincarga = float(z["ml1"]["cargas"][:, 0].min())
    ok = a.loc[cid, "k_paralela"] == 1 and mincarga >= 0.50
    H.append(dict(hipotese="H2.1", conjunto=cid, criterio="análise paralela retém 1 e cargas ≥ 0,50",
                  valor=f"retém {a.loc[cid,'k_paralela']}; menor carga {mincarga:.3f}; λ1 = {a.loc[cid,'lambda1']:.3f} ({a.loc[cid,'var_pc1']*100:.1f}%)",
                  decisao="critério atendido: 1 dimensão" if ok else "critério não atendido"))
    sono = {x["k"]: x for x in h24l if x["conjunto"] == "phq9_pns"}
    for h, crit in RETIRADAS.items():
        valor = "—"
        if h == "H2.4" and 1 in sono:
            valor = (f"descritivo, só PNS: na solução retida de 1 fator o item de sono carrega no único fator "
                     f"(carga {sono[1]['carga_sono']:.3f})")
        H.append(dict(hipotese=h, conjunto="—", criterio=crit, valor=valor, decisao=NOTA_RETIRADA))
    for cid in ("sassv_xuzhou", "doomscrolling_turquia", "procrastinacao_turquia", "ais_japao", "bps_japao"):
        r = a.loc[cid]
        H.append(dict(hipotese="H2.5", conjunto=cid, criterio="análise paralela retém 1",
                      valor=f"retém {r.k_paralela} (Kaiser {r.k_kaiser}); λ1 = {r.lambda1:.3f} ({r.var_pc1*100:.1f}%)",
                      decisao="critério atendido: unidimensional" if r.k_paralela == 1 else f"critério não atendido: {r.k_paralela} dimensões"))
    for r in es.itertuples():
        H.append(dict(hipotese="H2.6", conjunto=r.conjunto, criterio="r(PC1, escore fatorial) ≥ 0,95",
                      valor=f"r = {r.r_pc1_af:.4f}", decisao="critério atendido" if r.r_pc1_af >= 0.95 else "critério não atendido"))
    h = pd.DataFrame(H)
    salva_csv(h, TAB / "hipoteses.csv")
    return h


def vigitel_indice(por_id: dict):
    """Tabelas do índice de insônia do Vigitel 2024 para a apresentação: item a item e resumo."""
    z = por_id["insonia3_vigitel"]
    c = z["c"]
    desc = z["d"][c["itens"]]
    linhas = []
    for j, (item, rot) in enumerate(zip(c["itens"], c["rotulos"])):
        var, pergunta = INSONIA_VIGITEL_ORIGEM[item]
        linhas.append(dict(item=item, variavel_vigitel=var, pergunta_dicionario=pergunta, rotulo=rot,
                           escala="0 nunca, 1 raramente, 2 às vezes, 3 quase sempre, 4 sempre (r70x − 1)",
                           media=desc[item].mean(), dp=desc[item].std(),
                           carga_pc1=z["pca"]["cargas"][j, 0], carga_af1_ml=z["ml1"]["cargas"][j, 0],
                           comunalidade_af1=z["ml1"]["comunalidades"][j], msa=z["msa"][j],
                           alfa_sem_item=z["alfa_sem"][j], r_item_total=z["item_total"][j]))
    salva_csv(pd.DataFrame(linhas), TAB / "vigitel_indice.csv")
    chi2, gl, pb = z["bartlett"]
    av, p95 = z["pca"]["autovalores"], z["pa"]["p95"]
    resumo = dict(conjunto=c["id"], base=c["base"], indice="índice de insônia (soma dos 3 itens, 0-12)", n=z["n"], p=z["p"],
                  alfa=z["alfa"], kmo=z["kmo"], bartlett_chi2=chi2, bartlett_gl=gl, bartlett_p=pb,
                  autovalor_1=av[0], autovalor_2=av[1], autovalor_3=av[2], p95_aleatorio_1=p95[0], p95_aleatorio_2=p95[1],
                  var_pc1=z["pca"]["variancia"][0], var_comum_af1=float((z["ml1"]["cargas"] ** 2).sum() / z["p"]),
                  fatores_retidos=z["k"], r_pc1_soma=z["r"]["pc1_soma"], r_pc1_af=z["r"]["pc1_af"])
    salva_csv(pd.DataFrame([resumo]), TAB / "vigitel_indice_resumo.csv")


def limpa_obsoletos():
    """Remove saídas de conjuntos e comparações retirados em 2026-11-27 (EUA fora do trabalho)."""
    for f in [FIG / "cargas_insonia_br_eua.png", FIG / "cargas_phq9_br_eua.png", FIG / "biplot_sono7_nhanes.png",
              caminhos.PROCESSADOS / "escores_nhanes0506.parquet", *TAB.glob("correlacao_*nhanes*.csv")]:
        if f.exists():
            f.unlink()
            print("  removido:", f.name)


def main():
    t0 = time.time()
    bases = sorted({c["base"] for c in CONJUNTOS})
    dados = {b: pd.read_parquet(caminhos.processado(b)) for b in bases}
    res = [analisa_conjunto(c, i, dados) for i, c in enumerate(CONJUNTOS)]
    por_id = {z["c"]["id"]: z for z in res}
    ad, es = tabelas(res)
    t = tucker_e_h24(por_id)
    h24l = h24(por_id)
    figuras(res, por_id, t)
    h = hipoteses(ad, es, t, h24l, por_id)
    vigitel_indice(por_id)
    exporta_escores(res, dados)
    limpa_obsoletos()
    import pandas as _pd
    _pd.set_option("display.width", 250)
    _pd.set_option("display.max_colwidth", 120)
    print(h.to_string(index=False))
    print(t.to_string(index=False))
    print(f"tempo total {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
