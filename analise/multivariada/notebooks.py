"""T032 — Gera e executa os notebooks 02 (PCA por SVD) e 03 (análise fatorial).

Uso:  python -m analise.multivariada.notebooks      (depois de analise.multivariada.analisa)
Os números citados no texto dos notebooks são lidos das tabelas de resultados/002 na hora de gerar.
2026-11-27: EUA (NHANES 2005-06) fora do trabalho; o passo a passo usa o Vigitel 2024 e a PNS 2019.
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
    rs = le_csv(TAB / "vigitel_indice_resumo.csv").iloc[0]
    cells = [
        md("""
# 02 — Análise de componentes principais (PCA) pela decomposição em valores singulares

Spec 002, perguntas Q2.1 e Q2.4. Este notebook mostra a PCA **passo a passo pela SVD** nos 3 sintomas de insônia
do **Vigitel 2024** e confere cada número com uma implementação de referência (`scikit-learn`). No fim, resume os
conjuntos de itens da spec.

**Que itens juntamos?** As três perguntas de insônia do Vigitel 2024, respondidas de 1 (nunca) a 5 (sempre) e
recodificadas para 0 a 4:

| Item | Pergunta no Vigitel (dicionário) |
|---|---|
| `sintoma_1` (r703) | dificuldade para dormir |
| `sintoma_2` (r704) | acordou e teve dificuldade pra dormir de novo |
| `sintoma_3` (r705) | acordou antes da hora desejada e não conseguiu dormir de novo |

**Por que PCA aqui?** Queremos saber se essas três perguntas podem ser resumidas num único **índice de insônia**
(a soma, de 0 a 12) usado nas specs 003 a 005. A PCA procura as direções que concentram a maior parte da variância
dos itens padronizados. Os EUA (NHANES 2005-06) saíram do trabalho em 2026-11-27.
"""),
        code(SETUP),
        md("""
## Passo 1 — Padronizar

Cada item vira escore z: $Z_{ij} = (X_{ij} - \\bar X_j) / s_j$, com desvio padrão amostral ($n-1$).
Assim a PCA trabalha sobre a **matriz de correlação**, e itens com escalas diferentes pesam igual.
"""),
        code("""
vg = pd.read_parquet(caminhos.processado("vigitel2024"))
itens = ["sintoma_1", "sintoma_2", "sintoma_3"]
rotulos = ["adormecer (r703)", "voltar a dormir (r704)", "acordar cedo (r705)"]
X = vg[itens].dropna().to_numpy(float)
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
**Leitura.** No Vigitel o 1º componente tem autovalor {f(rs.autovalor_1)} e explica
{f(rs.var_pc1*100,1)}% da variância das três perguntas; os outros dois ficam abaixo de 1
({f(rs.autovalor_2)} e {f(rs.autovalor_3)}). Todas as cargas do CP1 são altas e do mesmo sinal: o componente é um
eixo de "insônia em geral". A soma simples dos 3 itens correlaciona {f(rs.r_pc1_soma,4)} com o escore do CP1, o que
justifica usar a soma (0–12) como índice.
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
## O índice de insônia do Vigitel, item a item

Tabela pronta em `resultados/002/tabelas/vigitel_indice.csv` (cargas na PCA e na análise fatorial, comunalidade,
MSA, α sem o item) e figura das cargas.
"""),
        code("""
display(le_csv(TAB / "vigitel_indice.csv")[["variavel_vigitel", "pergunta_dicionario", "carga_pc1", "carga_af1_ml",
                                            "comunalidade_af1", "msa", "alfa_sem_item"]])
display(Image(filename=str(FIG / "cargas_insonia_vigitel.png")))
"""),
        md("## Os conjuntos de itens da spec 002"),
        code("""
ad = le_csv(TAB / "adequacao.csv")
ad[["conjunto", "n", "p", "lambda1", "var_pc1", "k_kaiser", "k_paralela"]]
"""),
        code('display(Image(filename=str(FIG / "scree_todos.png")))'),
        md(f"""
**Leitura.** A análise paralela retém 1 dimensão no índice de insônia do Vigitel, no PHQ-9 da PNS, no doomscrolling
(Turquia) e na AIS (Japão); retém 2 no SAS-SV (China), na procrastinação (Turquia) e no BPS (Japão).

## Biplot: PHQ-9 da PNS 2019

O biplot mostra, no plano dos 2 primeiros componentes, as **cargas** (setas) e os **escores** (pontos). O CP1 é
"sofrimento em geral" (todas as setas para a direita, {f(ad.loc['phq9_pns','var_pc1']*100,0)}% da variância); o CP2
separa os itens somáticos (sono, cansaço, apetite) dos afetivos (humor, fracasso, autolesão).
"""),
        code('display(Image(filename=str(FIG / "biplot_phq9_pns.png")))'),
        md("""
## Conclusão

- A PCA por SVD reproduz exatamente (até $10^{-8}$) a PCA de referência; os autovalores são $\\sigma^2/(n-1)$.
- As 3 perguntas de insônia do Vigitel 2024 formam um componente dominante; a soma delas é o índice de insônia.
- O número de dimensões dos outros instrumentos está em `resultados/002/tabelas/adequacao.csv`; a análise
  fatorial (notebook 03) confirma e interpreta essas dimensões.
"""),
    ]
    return cells


def nb_af():
    ad = le_csv(TAB / "adequacao.csv").set_index("conjunto")
    rs = le_csv(TAB / "vigitel_indice_resumo.csv").iloc[0]
    cells = [
        md("""
# 03 — Análise fatorial

Spec 002, perguntas Q2.1 a Q2.4. A **análise fatorial (AF)** supõe que cada item é explicado por fatores comuns
mais um erro próprio: $x = \\Lambda f + \\varepsilon$, com $\\mathrm{Cov}(x) = \\Lambda\\Phi\\Lambda^\\top + \\Psi$.
Diferente da PCA (que resume a variância **total**), a AF modela só a variância **comum** — a parte que os
itens compartilham. Os números deste notebook são recalculados aqui e conferidos com `resultados/002/tabelas/`.

Desde 2026-11-27 os EUA (NHANES 2005-06) estão fora do trabalho; as hipóteses H2.2–H2.4, que comparavam
Brasil e EUA, foram retiradas. O exemplo principal é o PHQ-9 da PNS 2019.
"""),
        code(SETUP + """
pns = pd.read_parquet(caminhos.processado("pns2019"))
phq = [f"phq{i}" for i in range(1, 10)]
from analise.harmonizacao.recodes import PHQ_ROTULOS
Xb = pns[phq].dropna().to_numpy(float)
Rb = np.corrcoef(Xb, rowvar=False)
print("PHQ-9: PNS n =", len(Xb))
"""),
        md(f"""
## 1. Os dados servem para AF? KMO, MSA, Bartlett e α

- **α de Cronbach** mede a **consistência interna**: se os itens "andam juntos" a ponto de a soma ser um bom
  resumo. $\\alpha = \\frac{{k}}{{k-1}}(1 - \\sum s_j^2 / s_T^2)$; vai de 0 a 1. No índice de insônia do Vigitel,
  α = {f(rs.alfa, 2)}.
- **KMO** (Kaiser-Meyer-Olkin) mede se as correlações entre os itens são explicadas por algo **em comum** a todos,
  e não só por pares de itens: compara as correlações com as correlações **parciais** (pela inversa de $R$),
  $\\mathrm{{KMO}} = \\sum r_{{ij}}^2 / (\\sum r_{{ij}}^2 + \\sum q_{{ij}}^2)$. Vai de 0 a 1; perto de 1 = vale fazer AF;
  regra prática KMO ≥ 0,60 (*a verificar*). O **MSA** é o mesmo índice item a item. No Vigitel, KMO = {f(rs.kmo, 2)}.
- **Bartlett**: testa $H_0$: $R = I$ (itens não correlacionados).
  $\\chi^2 = -(n-1-(2p+5)/6)\\ln|R|$, gl $= p(p-1)/2$.
"""),
        code("""
k, msa = mv.kmo(Rb); chi2, gl, pv = mv.bartlett(Rb, len(Xb))
print(f"PNS 2019, PHQ-9: KMO = {k:.3f}; MSA mín = {msa.min():.3f}; Bartlett χ² = {chi2:,.1f}, gl = {gl}, p = {pv:.2e}; α = {mv.alfa_cronbach(Xb):.3f}")
le_csv(TAB / "adequacao.csv")[["conjunto", "n", "p", "alfa", "kmo", "bartlett_chi2", "bartlett_gl", "k_paralela"]]
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
mlb = mv.af_ml(Rb, 1)
pab = mv.af_eixos_principais(Rb, 1)
pd.DataFrame({"ML": mlb["cargas"][:, 0], "eixos principais": pab["cargas"][:, 0], "h² (ML)": mlb["comunalidades"],
              "unicidade": 1 - mlb["comunalidades"]}, index=PHQ_ROTULOS).round(3)
"""),
        md("""
## 3. Onde carrega o item de sono do PHQ-9?

Com 1 fator (a solução retida pela análise paralela), o item de sono carrega no único fator. Como a literatura
costuma separar no PHQ-9 um fator **somático** e um **afetivo**, rodamos também uma solução **exploratória** de 2
fatores com rotação **oblimin** (oblíqua: os fatores podem se correlacionar; Φ é a correlação entre eles).
"""),
        code("""
L2 = mv.af_ml(Rb, 2)["cargas"]; P, Phi, _ = mv.oblimin(L2)
print(f"PNS: Φ(F1,F2) = {Phi[0,1]:.3f}")
display(pd.DataFrame(P, index=PHQ_ROTULOS, columns=["F1", "F2"]).round(2))
le_csv(TAB / "phq9_item_sono.csv")
"""),
        md("""
Na solução exploratória de 2 fatores, o item de sono fica no mesmo fator que **cansaço** (o fator somático), não
no do humor deprimido.

## 4. Conjuntos com 2 fatores: varimax × oblimin

Para SAS-SV (China), procrastinação do sono (Turquia) e BPS (Japão) a análise paralela retém 2 fatores.
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
- **SAS-SV (China)**: um fator de "abstinência" (impaciente/inquieto/não suporta ficar sem o celular) e outro de
  "perturbação da rotina" (perde planos, perde eficiência, usa mais que o previsto), com Φ ≈ 0,61: dimensões
  distintas, mas bem correlacionadas.
- **Procrastinação (Turquia)**: dois blocos de itens (UE2, 3, 6, 7 × os demais), Φ ≈ 0,38. Sem codebook, não dá
  para afirmar se o 2º bloco é de itens invertidos.

## 5. Escores: PCA × AF × soma (H2.6)

Escore fatorial pelo método de regressão (Thurstone): $\\hat F = Z\\,R^{-1}\\Lambda\\Phi$.
"""),
        code("""
Z = mv.padroniza(Xb)
f_af = mv.escores_regressao(Z, Rb, mlb["cargas"])[:, 0]
pc = mv.pca_svd(Xb)
pc1 = pc["escores"][:, 0]
print("PNS PHQ-9: r(PC1, AF) =", round(abs(np.corrcoef(pc1, f_af)[0, 1]), 4), " r(PC1, soma) =", round(abs(np.corrcoef(pc1, Xb.sum(axis=1))[0, 1]), 4))
le_csv(TAB / "escores_correlacao.csv")
"""),
        md("""
## 6. Robustez: correlação policórica e correlação ponderada

Os itens são ordinais (0–3 ou 0–4). A correlação de Pearson entre categorias subestima a associação entre os
traços contínuos que estão por trás. A **policórica** (Olsson, 1979, doi:10.1007/BF02296207) estima essa
correlação supondo uma normal bivariada latente cortada em limiares: os limiares vêm das proporções marginais e
$\\rho$ maximiza a verossimilhança da tabela cruzada. A **ponderada** usa o peso amostral do inquérito. O
coeficiente de Tucker aqui compara as cargas de cada solução com as da solução de Pearson **na mesma base**.
"""),
        code("""
vg = pd.read_parquet(caminhos.processado("vigitel2024"))
Xi = vg[["sintoma_1", "sintoma_2", "sintoma_3"]].dropna().to_numpy(int)
Rp = mv.policorica(Xi)
print("Vigitel 2024, 3 sintomas — Pearson:\\n", np.corrcoef(Xi, rowvar=False).round(3), "\\npolicórica:\\n", Rp.round(3))
le_csv(TAB / "robustez.csv")[["conjunto", "correlacao", "lambda1", "var1", "k_kaiser", "tucker_vs_pearson"]]
"""),
        md("""
A policórica aumenta as correlações e o 1º autovalor, como esperado, mas as cargas mantêm o mesmo padrão, e a
ponderação pelo peso amostral quase não muda nada (coluna `tucker_vs_pearson`).

## 7. Decisão sobre as hipóteses
"""),
        code("le_csv(TAB / 'hipoteses.csv')"),
        md(f"""
## Conclusão

- **H2.1**: as 3 perguntas de insônia do Vigitel 2024 formam 1 fator (α = {f(rs.alfa, 2)}, KMO = {f(rs.kmo, 2)},
  {f(rs.var_pc1*100, 0)}% da variância no 1º componente). A soma delas é o índice de insônia.
- **H2.2–H2.4**: retiradas em 2026-11-27, com a saída dos EUA do trabalho. Fica o descritivo da PNS: o PHQ-9 tem
  1 fator, e o item de sono acompanha o cansaço quando se força a solução de 2 fatores.
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
