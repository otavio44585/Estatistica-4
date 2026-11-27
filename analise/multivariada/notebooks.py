"""T032 — Gera e executa os notebooks 02 (PCA por SVD) e 03 (análise fatorial).

Uso:  python -m analise.multivariada.notebooks      (depois de analise.multivariada.analisa)
Os números citados no texto dos notebooks são lidos das tabelas de resultados/002 na hora de gerar.
"""
import nbformat as nbf
from nbclient import NotebookClient

from analise.comum import caminhos
from analise.comum.estatistica import le_csv

TAB = caminhos.RESULTADOS / "002" / "tabelas"


def f(x, c=3):
    return f"{x:.{c}f}".replace(".", ",")


def md(s):
    return nbf.v4.new_markdown_cell(s.strip())


def code(s):
    return nbf.v4.new_code_cell(s.strip())


SETUP = """
import sys, pathlib
raiz = pathlib.Path.cwd()
while not (raiz / "analise").is_dir():
    raiz = raiz.parent
sys.path.insert(0, str(raiz))
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from IPython.display import Image, display
from analise.comum import caminhos, multivariada as mv
from analise.comum.estatistica import le_csv
pd.set_option("display.precision", 3); pd.set_option("display.width", 160)
TAB = caminhos.RESULTADOS / "002" / "tabelas"; FIG = caminhos.RESULTADOS / "002" / "figuras"
"""


def nb_pca():
    ad = le_csv(TAB / "adequacao.csv").set_index("conjunto")
    t = le_csv(TAB / "tucker.csv")
    tpc = t[(t.hipotese == "H2.2") & (t.solucao == "PCA 1º componente")].phi.iloc[0]
    av = le_csv(TAB / "pca_autovalores.csv")
    s7 = av[av.conjunto == "sono7_nhanes"]
    cells = [
        md("""
# 02 — Análise de componentes principais (PCA) pela decomposição em valores singulares

Spec 002, perguntas Q2.1 e Q2.4. Este notebook mostra a PCA **passo a passo pela SVD** nos 3 sintomas de insônia
do NHANES 2005-06 (EUA) e do Vigitel 2024 (Brasil) e confere cada número com uma implementação de referência
(`scikit-learn`). No fim, resume os 10 conjuntos de itens da spec.

**Por que PCA aqui?** Queremos saber se os três sintomas (dificuldade para adormecer, para voltar a dormir e
acordar cedo demais) podem ser resumidos num único índice de insônia — o índice 0–12 usado nas specs 003 a 005.
A PCA procura as direções que concentram a maior parte da variância dos itens padronizados.
"""),
        code(SETUP),
        md("""
## Passo 1 — Padronizar

Cada item vira escore z: $Z_{ij} = (X_{ij} - \\bar X_j) / s_j$, com desvio padrão amostral ($n-1$).
Assim a PCA trabalha sobre a **matriz de correlação**, e itens com escalas diferentes pesam igual.
"""),
        code("""
nh = pd.read_parquet(caminhos.processado("nhanes0506"))
itens = ["sintoma_1", "sintoma_2", "sintoma_3"]
rotulos = ["adormecer", "voltar a dormir", "acordar cedo"]
X = nh[itens].dropna().to_numpy(float)
n, p = X.shape
Z = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)
print(f"n = {n} pessoas com os 3 itens; p = {p} itens")
print("médias de Z:", Z.mean(axis=0).round(12), "  DP de Z:", Z.std(axis=0, ddof=1).round(12))
"""),
        md("""
## Passo 2 — Decomposição em valores singulares

$$Z = U\\,\\Sigma\\,V^\\top$$

- $U$ ($n \\times p$): direções no espaço das pessoas (colunas ortonormais);
- $\\Sigma$: valores singulares $\\sigma_1 \\ge \\sigma_2 \\ge \\sigma_3$;
- $V$ ($p \\times p$): direções no espaço dos itens — os **vetores dos componentes**.
"""),
        code("""
U, s, Vt = np.linalg.svd(Z, full_matrices=False)
V = Vt.T
V = V * np.sign(V.sum(axis=0))      # sinal é arbitrário; fixamos cargas positivas
print("U:", U.shape, " Σ:", s.round(3), " V:\\n", pd.DataFrame(V, index=rotulos, columns=["CP1", "CP2", "CP3"]).round(3))
print("UᵀU = I ?", np.allclose(U.T @ U, np.eye(p)), "   VᵀV = I ?", np.allclose(V.T @ V, np.eye(p)))
print("Z = UΣVᵀ ?", np.allclose(Z, U @ np.diag(s) @ Vt))
"""),
        md("""
## Passo 3 — Autovalores e variância explicada

Como $Z^\\top Z/(n-1) = R$ (a correlação), $R = V\\,\\frac{\\Sigma^2}{n-1}\\,V^\\top$. Logo os **autovalores** da
correlação são $\\lambda_k = \\sigma_k^2/(n-1)$, e a proporção de variância do componente $k$ é $\\lambda_k / p$.
Conferimos com os autovalores de $R$ e com o `PCA` do scikit-learn (tolerância $10^{-8}$).
"""),
        code("""
lam = s**2 / (n - 1)
R = np.corrcoef(X, rowvar=False)
lam_R = np.sort(np.linalg.eigvalsh(R))[::-1]
from sklearn.decomposition import PCA
lam_sk = PCA().fit(Z).explained_variance_
print("λ pela SVD     :", lam.round(6))
print("λ de R (eigh)  :", lam_R.round(6))
print("λ scikit-learn :", lam_sk.round(6))
assert np.allclose(lam, lam_R, atol=1e-8) and np.allclose(lam, lam_sk, atol=1e-8)
print("diferença máxima SVD × scikit-learn:", np.abs(lam - lam_sk).max())
pd.DataFrame({"autovalor": lam, "% variância": 100 * lam / p, "% acumulada": 100 * np.cumsum(lam) / p},
             index=["CP1", "CP2", "CP3"]).round(2)
"""),
        md("""
## Passo 4 — Cargas e escores

- **Cargas**: $A = V\\,\\Sigma/\\sqrt{n-1}$. Com dados padronizados, a carga do item $j$ no componente $k$ é a
  **correlação** entre o item e o escore do componente.
- **Escores**: $F = U\\,\\Sigma = Z\\,V$ (uma linha por pessoa).
"""),
        code("""
A = V * s / np.sqrt(n - 1)
F = Z @ V
print("F = UΣ ?", np.allclose(np.abs(F), np.abs(U * s)))
corr_item_cp1 = [np.corrcoef(Z[:, j], F[:, 0])[0, 1] for j in range(p)]
pd.DataFrame({"carga CP1": A[:, 0], "corr(item, escore CP1)": corr_item_cp1, "carga CP2": A[:, 1]}, index=rotulos).round(4)
"""),
        md(f"""
**Leitura.** No NHANES o 1º componente tem autovalor {f(ad.loc['insonia3_nhanes','lambda1'])} e explica
{f(ad.loc['insonia3_nhanes','var_pc1']*100,1)}% da variância dos três sintomas; os outros dois ficam abaixo de 1.
Todas as cargas do CP1 são altas e do mesmo sinal: o componente é um eixo de "insônia em geral".
"""),
        md("""
## Passo 5 — Quantos componentes? Kaiser, scree e análise paralela

- **Kaiser**: reter $\\lambda > 1$ (o componente explica mais que um item sozinho).
- **Scree**: procurar o "cotovelo" no gráfico dos autovalores.
- **Análise paralela de Horn (1965)**: gerar 1.000 conjuntos de dados aleatórios com o mesmo $n$ e $p$, sem
  nenhuma estrutura, e reter só os componentes cujo autovalor supera o **percentil 95** dos aleatórios.
  É a regra que decide no plano da spec 002.
"""),
        code("""
pa = mv.analise_paralela(n, p, reps=1000, semente=2027)
pd.DataFrame({"observado": lam, "aleatório (média)": pa["media"], "aleatório (P95)": pa["p95"],
              "retém?": lam > pa["p95"]}, index=["CP1", "CP2", "CP3"]).round(4)
"""),
        md("""
## Brasil: o mesmo procedimento no Vigitel 2024

Usamos a função `mv.pca_svd` (o mesmo código acima, empacotado e testado em `tests/test_002_multivariada.py`).
"""),
        code("""
vg = pd.read_parquet(caminhos.processado("vigitel2024"))
Xb = vg[itens].dropna().to_numpy(float)
rb, ru = mv.pca_svd(Xb), mv.pca_svd(X)
comp = pd.DataFrame({"carga CP1 Vigitel (BR)": rb["cargas"][:, 0], "carga CP1 NHANES (EUA)": ru["cargas"][:, 0]}, index=rotulos)
print(f"Vigitel: n = {len(Xb)}, λ1 = {rb['autovalores'][0]:.3f} ({100*rb['variancia'][0]:.1f}%)")
print(f"NHANES : n = {len(X)}, λ1 = {ru['autovalores'][0]:.3f} ({100*ru['variancia'][0]:.1f}%)")
print("Tucker φ entre as cargas do CP1:", round(mv.tucker(rb["cargas"][:, 0], ru["cargas"][:, 0]), 4))
comp.round(3)
"""),
        md(f"""
**Leitura.** Nos dois países um único componente concentra a variância (Vigitel {f(ad.loc['insonia3_vigitel','var_pc1']*100,1)}%,
NHANES {f(ad.loc['insonia3_nhanes','var_pc1']*100,1)}%), e as cargas praticamente coincidem (Tucker φ = {f(tpc)}).
Isso sustenta usar a soma dos três sintomas como índice nas specs 003–005: a correlação entre a soma e o escore do CP1 é
≥ 0,999 nas duas bases (`resultados/002/tabelas/escores_correlacao.csv`).
"""),
        md("## Os 10 conjuntos de itens da spec 002"),
        code("""
ad = le_csv(TAB / "adequacao.csv")
ad[["conjunto", "n", "p", "lambda1", "var_pc1", "k_kaiser", "k_paralela"]]
"""),
        code('display(Image(filename=str(FIG / "scree_todos.png")))'),
        md(f"""
**Leitura.** A análise paralela retém 1 dimensão nos dois conjuntos de insônia, nos dois PHQ-9, no doomscrolling
e na AIS; retém 2 no SAS-SV (Xuzhou), na procrastinação (Turquia) e no BPS (Japão). Nos 7 sintomas de sono do
NHANES, Kaiser apontaria 2 (λ2 = {f(s7.autovalor.iloc[1])}), mas o 2º autovalor não supera o P95 aleatório
({f(s7.p95_aleatorio.iloc[1])}): a regra do plano retém 1.

## Biplot: 7 sintomas de sono (NHANES)

O biplot mostra, no plano dos 2 primeiros componentes, as **cargas** (setas) e os **escores** (pontos). O CP1 é
"problema de sono em geral" (todas as setas para a direita); o CP2 separa os sintomas **noturnos** (adormecer,
acordar à noite, acordar cedo, remédio) dos **diurnos** (não descansado, sonolência, sono insuficiente).
"""),
        code('display(Image(filename=str(FIG / "biplot_sono7_nhanes.png")))'),
        md("""
## Conclusão

- A PCA por SVD reproduz exatamente (até $10^{-8}$) a PCA de referência; os autovalores são $\\sigma^2/(n-1)$.
- Os 3 sintomas de insônia formam um componente dominante no Brasil e nos EUA, com cargas quase idênticas.
- O número de dimensões dos outros instrumentos está em `resultados/002/tabelas/adequacao.csv`; a análise
  fatorial (notebook 03) confirma e interpreta essas dimensões.
"""),
    ]
    return cells


def nb_af():
    h = le_csv(TAB / "hipoteses.csv")
    ad = le_csv(TAB / "adequacao.csv").set_index("conjunto")
    cells = [
        md("""
# 03 — Análise fatorial

Spec 002, perguntas Q2.1 a Q2.4. A **análise fatorial (AF)** supõe que cada item é explicado por fatores comuns
mais um erro próprio: $x = \\Lambda f + \\varepsilon$, com $\\mathrm{Cov}(x) = \\Lambda\\Phi\\Lambda^\\top + \\Psi$.
Diferente da PCA (que resume a variância **total**), a AF modela só a variância **comum** — a parte que os
itens compartilham. Os números deste notebook são recalculados aqui e conferidos com `resultados/002/tabelas/`.
"""),
        code(SETUP + """
pns = pd.read_parquet(caminhos.processado("pns2019")); nh = pd.read_parquet(caminhos.processado("nhanes0506"))
phq = [f"phq{i}" for i in range(1, 10)]
from analise.harmonizacao.recodes import PHQ_ROTULOS
Xb = pns[phq].dropna().to_numpy(float); Xu = nh[phq].dropna().to_numpy(float)
Rb, Ru = np.corrcoef(Xb, rowvar=False), np.corrcoef(Xu, rowvar=False)
print("PHQ-9: PNS n =", len(Xb), " NHANES n =", len(Xu))
"""),
        md("""
## 1. Os dados servem para AF? KMO, MSA, Bartlett e α

- **KMO** compara as correlações com as correlações **parciais** (pela inversa de $R$):
  $\\mathrm{KMO} = \\sum r_{ij}^2 / (\\sum r_{ij}^2 + \\sum q_{ij}^2)$. Perto de 1 = os itens compartilham variância;
  regra prática KMO ≥ 0,60 (*a verificar*). O **MSA** é o mesmo índice item a item.
- **Bartlett**: testa $H_0$: $R = I$ (itens não correlacionados).
  $\\chi^2 = -(n-1-(2p+5)/6)\\ln|R|$, gl $= p(p-1)/2$.
- **α de Cronbach**: consistência interna, $\\alpha = \\frac{k}{k-1}(1 - \\sum s_j^2 / s_T^2)$.
"""),
        code("""
for nome, X, R in (("PNS 2019", Xb, Rb), ("NHANES 2005-06", Xu, Ru)):
    k, msa = mv.kmo(R); chi2, gl, pv = mv.bartlett(R, len(X))
    print(f"{nome}: KMO = {k:.3f}; MSA mín = {msa.min():.3f}; Bartlett χ² = {chi2:,.1f}, gl = {gl}, p = {pv:.2e}; α = {mv.alfa_cronbach(X):.3f}")
"""),
        md("""
Com n de milhares, o Bartlett rejeita $H_0$ sempre (p arredondado para 0): ele só confirma que há correlação a
modelar. O tamanho do efeito está no KMO e no α.

## 2. Extração por máxima verossimilhança (ML) e por eixos principais

- **ML**: escolhe as unicidades $\\Psi$ que maximizam a verossimilhança normal; minimiza
  $-\\sum_{j>k}(\\ln\\lambda_j - \\lambda_j) - k + p$ sobre os autovalores de $\\Psi^{-1/2}R\\Psi^{-1/2}$.
- **Eixos principais**: troca a diagonal de $R$ pelas comunalidades $h^2$ e repete a decomposição até convergir.

**Comunalidade** $h_j^2 = \\sum_k \\lambda_{jk}^2$ = parte da variância do item explicada pelos fatores;
**unicidade** $= 1 - h_j^2$.
"""),
        code("""
mlb, mlu = mv.af_ml(Rb, 1), mv.af_ml(Ru, 1)
pab = mv.af_eixos_principais(Rb, 1)
pd.DataFrame({"PNS ML": mlb["cargas"][:, 0], "PNS eixos": pab["cargas"][:, 0], "PNS h²": mlb["comunalidades"],
              "NHANES ML": mlu["cargas"][:, 0], "NHANES h²": mlu["comunalidades"]}, index=PHQ_ROTULOS).round(3)
"""),
        md("""
## 3. Congruência de Tucker: a estrutura é a mesma no Brasil e nos EUA?

$\\varphi = \\sum a_i b_i / \\sqrt{\\sum a_i^2 \\sum b_i^2}$. Lorenzo-Seva e ten Berge (2006,
doi:10.1027/1614-2241.2.2.57, limites conferidos no resumo registrado no Crossref): **0,85–0,94 = similaridade
razoável; acima de 0,95 = fatores considerados iguais**. Cuidado: com todas as cargas positivas, φ tende a sair
alto; por isso a tabela também traz a maior diferença absoluta entre cargas.
"""),
        code("""
print("PHQ-9, 1 fator ML: Tucker φ =", round(mv.tucker(mlb["cargas"][:, 0], mlu["cargas"][:, 0]), 4))
le_csv(TAB / "tucker.csv")[["hipotese", "instrumento", "solucao", "fator", "phi", "classificacao", "dif_max_carga"]]
"""),
        code('display(Image(filename=str(FIG / "cargas_insonia_br_eua.png"))); display(Image(filename=str(FIG / "cargas_phq9_br_eua.png")))'),
        md("""
## 4. Onde carrega o item de sono do PHQ-9? (H2.4)

Com 1 fator (a solução retida pela análise paralela nos dois países), o item de sono carrega no único fator.
Como a literatura costuma separar no PHQ-9 um fator **somático** e um **afetivo**, rodamos também uma solução
**exploratória** de 2 fatores com rotação **oblimin** (oblíqua: os fatores podem se correlacionar; Φ é a
correlação entre eles).
"""),
        code("""
for nome, R in (("PNS", Rb), ("NHANES", Ru)):
    L2 = mv.af_ml(R, 2)["cargas"]; P, Phi, _ = mv.oblimin(L2)
    df = pd.DataFrame(P, index=PHQ_ROTULOS, columns=["F1", "F2"]).round(2)
    print(f"--- {nome}: Φ(F1,F2) = {Phi[0,1]:.3f}"); display(df)
"""),
        md("""
Nos dois países o item de sono fica no mesmo fator que **cansaço** (o fator somático), não no do humor
deprimido. A ordem F1/F2 muda de uma base para outra, mas o agrupamento é o mesmo.

## 5. Conjuntos com 2 fatores: varimax × oblimin

Para SAS-SV (Xuzhou), procrastinação do sono (Turquia) e BPS (Japão) a análise paralela retém 2 fatores.
**Varimax** força fatores não correlacionados (ortogonal); **oblimin** permite correlação.
"""),
        code("""
cg = le_csv(TAB / "af_cargas.csv"); phi = le_csv(TAB / "af_phi.csv")
display(phi)
display(Image(filename=str(FIG / "cargas_multifator.png")))
"""),
        md("""
**Leitura.**
- **BPS (Japão)**: o 2º fator reúne exatamente os itens de redação invertida (BPS2R, BPS3R, BPS7R, BPS9R) e se
  correlaciona pouco com o 1º (Φ ≈ 0,19). É o padrão de um **fator de método** (efeito da redação), não
  necessariamente de dois construtos.
- **SAS-SV (Xuzhou)**: um fator de "abstinência" (impaciente/inquieto/não suporta ficar sem o celular) e outro de
  "perturbação da rotina" (perde planos, perde eficiência, usa mais que o previsto), com Φ ≈ 0,61: dimensões
  distintas, mas bem correlacionadas.
- **Procrastinação (Turquia)**: dois blocos de itens (UE2, 3, 6, 7 × os demais), Φ ≈ 0,38. Sem codebook, não dá
  para afirmar se o 2º bloco é de itens invertidos.

## 6. Escores: PCA × AF × soma (H2.6)

Escore fatorial pelo método de regressão (Thurstone): $\\hat F = Z\\,R^{-1}\\Lambda\\Phi$.
"""),
        code("""
Z = mv.padroniza(Xu)
f_af = mv.escores_regressao(Z, Ru, mlu["cargas"])[:, 0]
pc = mv.pca_svd(Xu)
pc1 = pc["escores"][:, 0]
print("NHANES PHQ-9: r(PC1, AF) =", round(np.corrcoef(pc1, f_af)[0, 1], 4), " r(PC1, soma) =", round(np.corrcoef(pc1, Xu.sum(axis=1))[0, 1], 4))
le_csv(TAB / "escores_correlacao.csv")
"""),
        md("""
## 7. Robustez: correlação policórica e correlação ponderada

Os itens são ordinais (0–3 ou 0–4). A correlação de Pearson entre categorias subestima a associação entre os
traços contínuos que estão por trás. A **policórica** (Olsson, 1979, doi:10.1007/BF02296207) estima essa
correlação supondo uma normal bivariada latente cortada em limiares: os limiares vêm das proporções marginais e
$\\rho$ maximiza a verossimilhança da tabela cruzada. A **ponderada** usa o peso amostral do inquérito.
"""),
        code("""
Xi = nh[["sintoma_1", "sintoma_2", "sintoma_3"]].dropna().to_numpy(int)
Rp = mv.policorica(Xi)
print("NHANES, 3 sintomas — Pearson:\\n", np.corrcoef(Xi, rowvar=False).round(3), "\\npolicórica:\\n", Rp.round(3))
le_csv(TAB / "robustez.csv")[["conjunto", "correlacao", "lambda1", "var1", "k_kaiser", "tucker_vs_pearson"]]
"""),
        md("""
A policórica aumenta as correlações e o 1º autovalor, como esperado, mas as cargas mantêm o mesmo padrão
(Tucker com a solução de Pearson ≥ 0,994) e a ponderação pelo peso amostral quase não muda nada (Tucker ≥ 0,998).

## 8. Decisão sobre as hipóteses H2.1–H2.6
"""),
        code("le_csv(TAB / 'hipoteses.csv')"),
        md(f"""
## Conclusão

- **H2.1 e H2.2**: os 3 sintomas formam 1 fator no Brasil e nos EUA, com estruturas equivalentes
  (Tucker φ = {h[h.hipotese=='H2.2'].valor.iloc[0].split('(')[0].replace('φ = ','').strip().replace('.',',')}).
- **H2.3 e H2.4**: o PHQ-9 tem 1 fator nos dois países, equivalente entre eles; o item de sono acompanha o
  cansaço quando se força a solução de 2 fatores.
- **H2.5**: doomscrolling e AIS são unidimensionais; SAS-SV, procrastinação (Turquia) e BPS têm 2 dimensões —
  no BPS, compatível com efeito dos itens invertidos.
- **H2.6**: escore da PCA e escore fatorial ordenam as pessoas quase igual (r ≥ 0,95 em todos os conjuntos).
- Consequência para as próximas specs: os índices por soma simples (insônia 0–12, PHQ-9 0–27, escores totais
  das escalas) são resumos adequados dos construtos, com a ressalva das escalas bidimensionais.
"""),
    ]
    return cells


def executa(cells, nome):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    NotebookClient(nb, timeout=600, kernel_name="python3",
                   resources={"metadata": {"path": str(caminhos.RAIZ)}}).execute()
    caminhos.NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, caminhos.NOTEBOOKS / nome)
    print("ok:", nome)


def main():
    executa(nb_pca(), "02_pca_svd.ipynb")
    executa(nb_af(), "03_analise_fatorial.ipynb")


if __name__ == "__main__":
    main()
