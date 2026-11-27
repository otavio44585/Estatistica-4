# EXPLORATÓRIO (2026-11-27). Ponto de partida da spec 001; não é análise confirmatória.
# Uso: defina STAT4_BRUTOS (pasta dos microdados brutos) e, opcionalmente, STAT4_SAIDA.
import os, pandas as pd, numpy as np, re, zipfile, pyreadstat, warnings
from scipy import stats
warnings.filterwarnings("ignore")
D = os.environ["STAT4_BRUTOS"]
OUT = os.environ.get("STAT4_SAIDA", ".")
L = []

def analisa(base, expo, desf, df, x, y, w, idade, alto, baixo, freq):
    d = df[[x, y, w] + ([idade] if idade else [])].dropna()
    d = d[d[x].isin(alto + baixo)]
    g = d[x].isin(alto); f = d[y].isin(freq)
    a, na, b, nb = f[g].sum(), g.sum(), f[~g].sum(), (~g).sum()
    rp = (a / na) / (b / nb); se = np.sqrt(1/a - 1/na + 1/b - 1/nb)
    pw = lambda m: np.average(f[m], weights=d.loc[m, w]) * 100
    r = dict(base=base, exposicao=expo, desfecho=desf, n_alto=int(na), n_baixo=int(nb),
             pct_alto=round(a/na*100, 1), pct_baixo=round(b/nb*100, 1),
             pct_alto_pond=round(pw(g), 1), pct_baixo_pond=round(pw(~g), 1),
             RP_bruta=round(rp, 2), IC95_bruta=f"{np.exp(np.log(rp)-1.96*se):.2f}-{np.exp(np.log(rp)+1.96*se):.2f}")
    if idade:
        d["fx"] = pd.cut(d[idade], [17, 29, 44, 59, 200], labels=["18-29", "30-44", "45-59", "60+"])
        num = den = vn = 0; faixas = []
        for k, s in d.groupby("fx", observed=True):
            gg = s[x].isin(alto); ff = s[y].isin(freq)
            a1, n1, b0, n0 = ff[gg].sum(), gg.sum(), ff[~gg].sum(), (~gg).sum(); N = n1 + n0
            if n1 == 0 or n0 == 0 or b0 == 0: continue
            num += a1*n0/N; den += b0*n1/N; vn += (n1*n0*(a1+b0) - a1*b0*N) / N**2
            faixas.append(f"{k}: {(a1/n1)/(b0/n0):.2f}")
        rr = num / den; sr = np.sqrt(vn / (num*den))
        r.update(RP_idade=round(rr, 2), IC95_idade=f"{np.exp(np.log(rr)-1.96*sr):.2f}-{np.exp(np.log(rr)+1.96*sr):.2f}",
                 RP_por_faixa=" | ".join(faixas), pct_alto_18_29=round(d.loc[g, "fx"].eq("18-29").mean()*100, 1),
                 pct_baixo_18_29=round(d.loc[~g, "fx"].eq("18-29").mean()*100, 1))
    L.append(r)

# PNS 2019
inp = open(rf"{D}\pns_2019\extraido\Dicionario_e_input_20220530\input_PNS_2019.txt", encoding="latin-1").read()
pos = {m[1]: (int(m[0]), int(m[2])) for m in re.findall(r"@(\d+)\s+(\w+)\s+\$?(\d+)\.", inp)}
vs = ["M001", "C008", "V00291", "N010", "P04501", "P04502"]
pns = pd.read_fwf(rf"{D}\pns_2019\extraido\PNS_2019_20220525\PNS_2019.txt",
                  colspecs=[(pos[v][0]-1, pos[v][0]-1+pos[v][1]) for v in vs], names=vs, dtype=str)
pns = pns[pns.M001 == "1"].apply(pd.to_numeric, errors="coerce"); pns = pns[pns.C008 >= 18]
for x, nome in [("P04502", "computador/tablet/celular"), ("P04501", "TV")]:
    analisa("PNS 2019 (BR)", nome, "problema de sono >metade dos dias", pns, x, "N010", "V00291", "C008", [4, 5], [6, 1], [3, 4])

# Vigitel 2024
z = zipfile.ZipFile(rf"{D}\vigitel_2006_2024\vigitel-2006-2024-peso-rake-csv.zip")
cols = ["ano", "q6", "pesorake2025", "r703", "q59a", "q59b", "q59c"]
vg = pd.concat(ch[ch.ano == 2024] for ch in pd.read_csv(z.open(z.namelist()[0]), usecols=cols, encoding="latin-1", chunksize=200000, low_memory=False))
vg = vg.apply(pd.to_numeric, errors="coerce"); vg = vg[vg.q6 >= 18]
vg["q59c2"] = np.where(vg.q59b == 2, 0, vg.q59c)
analisa("Vigitel 2024 (BR capitais)", "computador/tablet/celular", "dificuldade p/ adormecer quase sempre/sempre", vg, "q59c2", "r703", "pesorake2025", "q6", [4, 5, 6, 7], [0, 1], [4, 5])
analisa("Vigitel 2024 (BR capitais)", "TV", "dificuldade p/ adormecer quase sempre/sempre", vg, "q59a", "r703", "pesorake2025", "q6", [4, 5, 6, 7], [8, 1], [4, 5])

# NHANES 2005-06
sl, _ = pyreadstat.read_xport(rf"{D}\nhanes_2005_2006\SLQ_D.xpt")
pa, _ = pyreadstat.read_xport(rf"{D}\nhanes_2005_2006\PAQ_D.xpt")
de, _ = pyreadstat.read_xport(rf"{D}\nhanes_2005_2006\DEMO_D.xpt")
nh = sl.merge(pa[["SEQN", "PAD590", "PAD600"]], on="SEQN").merge(de[["SEQN", "RIDAGEYR", "WTINT2YR"]], on="SEQN")
nh = nh[nh.RIDAGEYR >= 18]; nh["SLQ080"] = nh.SLQ080.where(nh.SLQ080 <= 4)
for x, nome in [("PAD600", "computador/games"), ("PAD590", "TV")]:
    analisa("NHANES 2005-06 (EUA)", nome, "dificuldade p/ adormecer often/almost always", nh, x, "SLQ080", "WTINT2YR", "RIDAGEYR", [3, 4, 5], [6, 0], [3, 4])

out = pd.DataFrame(L)
pd.set_option("display.width", 250)
print(out[["base", "exposicao", "n_alto", "n_baixo", "pct_alto", "pct_baixo", "RP_bruta", "IC95_bruta", "RP_idade", "IC95_idade", "pct_alto_18_29", "pct_baixo_18_29"]].to_string(index=False))
print(); print(out[["base", "exposicao", "RP_por_faixa"]].to_string(index=False))
out.to_csv(rf"{OUT}\comparativo_preliminar.csv", sep=";", index=False, decimal=",")
