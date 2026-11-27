"""T068 — Gera e executa analise/notebooks/05_comparacao_mundial.ipynb (nbformat + nbclient).

Uso: python -m analise.mundial.notebook
"""
import nbformat as nbf
from nbclient import NotebookClient

from analise.comum import caminhos

md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

CELULAS = [
    md("""# 05 — Comparação mundial: correlação comum e meta-análise (spec 004)

**Pergunta:** como a associação entre uso de tela e sono no Brasil se posiciona frente a outros países e à literatura?

As bases usam escalas diferentes (índice de insônia, PSQI, AIS, latência em minutos), então a razão de prevalências da spec 003 não serve para todas. A métrica comum é a **correlação de Spearman (ρ)** entre exposição e desfecho, com sinal padronizado: **positivo = mais tela, pior sono**. As correlações das 6 bases são combinadas por **meta-análise de efeitos aleatórios (DerSimonian e Laird, 1986)**.

Os pares exposição × desfecho, a família de testes (H4.1–H4.4, com Holm) e as regras de decisão foram fixados no plano antes do cálculo (`specs/004-comparacao-mundial/plan.md`)."""),
    code("""import sys, os
sys.path.insert(0, os.getcwd())
import numpy as np, pandas as pd
from scipy import stats
from IPython.display import Image, display
from statsmodels.stats.meta_analysis import combine_effects
from analise.comum import caminhos
from analise.comum.estatistica import le_csv, holm, formata_p
from analise.mundial import metodos as M, rodar
from analise.mundial.pares import PRINCIPAIS
pd.set_option("display.width", 200); pd.set_option("display.max_colwidth", 80)
TAB = caminhos.RESULTADOS / "004" / "tabelas"; FIG = caminhos.RESULTADOS / "004" / "figuras"
pd.DataFrame([dict(base=p.base, tipo=p.tipo, exposicao=p.rot_exposicao, desfecho=p.rot_desfecho, inverte=p.inverte)
              for p in PRINCIPAIS])"""),
    md("""## 1. Rodar a análise completa

`rodar.main()` calcula os efeitos por base (com bootstrap), a meta-análise, os testes, as sensibilidades e as figuras, e grava tudo em `resultados/004/`. As seções seguintes refazem cada passo à mão para mostrar a técnica."""),
    code("""ef, meta, hip, sens = rodar.main()"""),
    md("""## 2. Uma correlação passo a passo (Vigitel 2024)

1. ρ de Spearman = correlação de Pearson entre os **postos** de x e de y (empates recebem o posto médio).
2. Transformação z de Fisher: z = atanh(ρ). Na escala z a distribuição é aproximadamente normal.
3. Erro padrão de z para Spearman (Fieller, Hartley e Pearson, 1957): EP ≈ √(1,06 / (n − 3)). Para Pearson seria √(1 / (n − 3)).
4. IC 95%: z ± 1,96·EP, e volta para ρ com tanh()."""),
    code("""v = pd.read_parquet(caminhos.processado("vigitel2024"))[["tela_digital_ord", "insonia_idx"]].dropna()
rx, ry = stats.rankdata(v.tela_digital_ord), stats.rankdata(v.insonia_idx)
rho = np.corrcoef(rx, ry)[0, 1]
n = len(v); z = np.arctanh(rho); ep = np.sqrt(1.06 / (n - 3))
print(f"n = {n}; ρ (postos) = {rho:.4f}; scipy = {stats.spearmanr(v.tela_digital_ord, v.insonia_idx).statistic:.4f}")
print(f"z = {z:.4f}; EP = {ep:.5f}; IC 95% de ρ = [{np.tanh(z - 1.96*ep):.4f}; {np.tanh(z + 1.96*ep):.4f}]")"""),
    md("""### Conferência do erro padrão (T061)

A fórmula de Fieller, Hartley e Pearson foi derivada para dados contínuos sem empates; aqui a exposição tem poucas faixas. A regra fixada no plano: se o EP por **bootstrap** (1.000 reamostragens, semente 2026) divergir mais de 10% da fórmula em alguma base, usa-se o bootstrap em todas."""),
    code("""ef[["nome", "n", "rho", "r_pearson", "ep_fhp", "ep_bootstrap", "divergencia_rel", "ep_usado"]].round(4)"""),
    md("""## 3. Meta-análise de efeitos aleatórios, à mão (DerSimonian e Laird)

Com efeitos yᵢ = zᵢ e variâncias vᵢ = EPᵢ²:

| Passo | Fórmula |
|---|---|
| pesos de efeito fixo | wᵢ = 1 / vᵢ |
| média de efeito fixo | μ_F = Σ wᵢ yᵢ / Σ wᵢ |
| heterogeneidade | Q = Σ wᵢ (yᵢ − μ_F)², gl = k − 1 |
| variância entre estudos | τ² = max(0, (Q − gl) / C), C = Σ wᵢ − Σ wᵢ² / Σ wᵢ |
| pesos aleatórios | wᵢ* = 1 / (vᵢ + τ²) |
| média aleatória e EP | μ = Σ wᵢ* yᵢ / Σ wᵢ*, EP = √(1 / Σ wᵢ*) |
| I² (Higgins e Thompson, 2002) | I² = max(0, (Q − gl) / Q) |"""),
    code("""y, vv = ef.z.to_numpy(), (ef.ep ** 2).to_numpy()
w = 1 / vv; muF = (w * y).sum() / w.sum()
Q = (w * (y - muF) ** 2).sum(); gl = len(y) - 1
C = w.sum() - (w ** 2).sum() / w.sum(); tau2 = max(0, (Q - gl) / C)
ws = 1 / (vv + tau2); mu = (ws * y).sum() / ws.sum(); epm = np.sqrt(1 / ws.sum())
I2 = max(0, (Q - gl) / Q)
print(f"μ_F = {muF:.5f} (ρ = {np.tanh(muF):.4f});  Q = {Q:.2f}, gl = {gl}, p = {stats.chi2.sf(Q, gl):.2e}")
print(f"τ² = {tau2:.5f};  μ = {mu:.5f} -> ρ = {np.tanh(mu):.4f}, IC [{np.tanh(mu-1.96*epm):.4f}; {np.tanh(mu+1.96*epm):.4f}];  I² = {I2:.1%}")
sm = combine_effects(y, vv, method_re="dl", row_names=list(ef.nome))
print(f"statsmodels: μ = {sm.mean_effect_re:.5f}, τ² = {sm.tau2:.5f}, Q = {sm.q:.2f}, I² = {sm.i2:.1%}")
pd.DataFrame({"base": ef.nome, "peso fixo %": 100 * w / w.sum(), "peso aleatório %": 100 * ws / ws.sum()}).round(1)"""),
    md("""**Leitura:** com τ² > 0 os pesos aleatórios ficam quase iguais entre as bases. No efeito fixo, a PNS (n = 88 mil, ρ negativo) domina a média; no aleatório, cada base pesa em torno de 1/6. Por isso as duas médias divergem, e a escolha do modelo aleatório (fixada no plano) importa."""),
    code("""le_csv(TAB / "conferencia_statsmodels.csv")"""),
    md("""### IC de Hartung-Knapp (acrescentado na verificação independente)

Com poucas bases (k = 6), o IC normal do DerSimonian-Laird é estreito demais. O método de Hartung e Knapp (2001) reescala a variância pela dispersão observada e usa t com k − 1 gl:

q = Σ wᵢ*(yᵢ − μ)² / (k − 1);  EP_HK = √(q / Σ wᵢ*);  IC = μ ± t(0,975; k − 1)·EP_HK.

Os dois intervalos aparecem lado a lado. Os testes H4.1–H4.4 não usam esse IC, então nenhuma decisão muda."""),
    code("""hk = M.hartung_knapp(y, vv, tau2); tc = stats.t.ppf(0.975, len(y) - 1)
print(f"EP_HK = {hk['ep_hk']:.5f} (statsmodels {sm.sd_eff_w_re_hksj:.5f}); q = {hk['q_hk']:.2f}")
print(f"DL: ρ IC [{np.tanh(mu-1.96*epm):.3f}; {np.tanh(mu+1.96*epm):.3f}]  |  HK: ρ IC [{np.tanh(hk['ic_inf_hk']):.3f}; {np.tanh(hk['ic_sup_hk']):.3f}], p = {hk['p_hk']:.3f}")
le_csv(TAB / "meta_analise.csv")[["analise", "k", "rho", "rho_ic_inf", "rho_ic_sup", "rho_ic_inf_hk", "rho_ic_sup_hk", "p_efeito", "p_efeito_hk", "nota"]].round(3)"""),
    md("""### Efeito do desenho nos inquéritos

Os EP das correlações de PNS e Vigitel supõem amostra aleatória simples. Pesos desiguais aumentam a variância por um fator de pelo menos deff = 1 + CV² dos pesos (Kish). Estrato e conglomerado não entram nessa conta. A sensibilidade multiplica a variância desses dois inquéritos pelo deff e refaz a meta-análise: Q e I² caem, mas continuam enormes."""),
    code("""print(ef[["nome", "deff_kish"]].dropna().round(2).to_string(index=False))
s_ = le_csv(TAB / "sensibilidade.csv")
s_[s_.grupo == "efeito do desenho (deff)"][["analise", "k", "rho", "ic_inf", "ic_sup", "Q", "I2", "tau2", "z_teste", "p"]].round(4)"""),
    md("""## 4. Testes de hipótese (família H4.1–H4.4, Holm)

- **H4.1** heterogeneidade: Q de Cochran ~ χ²(k − 1).
- **H4.2** tipo de exposição: τ² separado por subgrupo; Q entre subgrupos = Q das três médias combinadas, gl = 2.
- **H4.3** Brasil (PNS + Vigitel, efeitos aleatórios) × outros países com tempo total: z = (z_BR − z_outros) / √(EP_BR² + EP_outros²). Sem o NHANES (retirado do trabalho em 2026-11-27, decisão do grupo), o lado "outros" é só a Argentina (k = 1, adolescentes).
- **H4.4** equivalência com a referência (Han, Zhou e Liu, 2024: uso geral × qualidade, r = 0,28, IC 0,21–0,35) por dois testes unilaterais (TOST): H0 = estimativa de tempo total fora de [0,21; 0,35]. p = maior dos dois p unilaterais."""),
    code("""h = le_csv(TAB / "hipoteses.csv")
h[["hipotese", "h0", "teste", "estatistica", "gl", "p_txt", "p_holm_txt", "decisao", "efeito"]]"""),
    md("""**H4.2: hipótese ordenada, teste omnibus.** A spec registrou uma ordem (tempo total < pré-sono < uso problemático), mas o teste fixado no plano é o Q entre subgrupos, que não usa a ordem. Uma meta-regressão das médias de subgrupo sobre o escore 0/1/2 entra como **exploratória** (fora da família de Holm). O subgrupo pré-sono tem k = 1 (só o Japão), então ele não tem τ² próprio."""),
    code("""le_csv(TAB / "exploratorio_referencia.csv")"""),
    md("""### EXPLORATÓRIO: Brasil × resto do mundo

Pedido do grupo depois de ver os resultados, por isso fora da família de Holm. Junta as duas bases brasileiras de um lado e as quatro do resto do mundo (Argentina, Japão, China, Turquia) do outro, **misturando os tipos de exposição** (tempo total, pré-sono, uso problemático). Não substitui H4.3, que compara só bases com o mesmo tipo de exposição."""),
    code("""display(Image(filename=str(FIG / "brasil_vs_resto.png")))
le_csv(TAB / "meta_analise.csv").query("analise == 'Brasil (PNS + Vigitel)' or analise.str.startswith('resto do mundo')", engine="python")[["analise", "k", "rho", "rho_ic_inf", "rho_ic_sup", "rho_ic_inf_hk", "rho_ic_sup_hk", "I2"]].round(3)"""),
    code("""print("Holm conferido:", np.allclose(holm(h.p), h.p_holm))
le_csv(TAB / "meta_analise.csv")[["analise", "k", "rho", "rho_ic_inf", "rho_ic_sup", "Q", "gl_Q", "p_Q", "tau2", "I2"]].round(4)"""),
    md("""## 5. Gráfico de floresta

Cada quadrado é o ρ de uma base (tamanho proporcional ao peso aleatório), com IC 95%. Os losangos são as estimativas combinadas. A faixa cinza é o IC 95% da meta-análise de referência para uso geral × qualidade do sono."""),
    code("""display(Image(filename=str(FIG / "floresta.png")))"""),
    md("""## 6. Sensibilidades

- **Bruta × ajustada por idade** (princípio 11): ρ parcial de Spearman controlando a idade. Na PNS o sinal muda: o ρ bruto negativo reflete confundimento por idade (jovens usam mais tela e relatam menos problema de sono), o mesmo padrão da exploração de 27/11 (RP bruta 0,90 → ajustada 1,17).
- Deixar uma base de fora; ρ ponderado pelo peso amostral nos inquéritos; pares alternativos; bases de procedência questionável (só aqui, rotuladas); contraponto intrapessoal da Holanda."""),
    code("""display(Image(filename=str(FIG / "bruta_ajustada_idade.png")))
le_csv(TAB / "bruta_ajustada_idade.csv").round(3)"""),
    code("""le_csv(TAB / "sensibilidade.csv")[["grupo", "analise", "k", "n", "rho", "ic_inf", "ic_sup", "I2"]].round(3)"""),
    md("""## 7. O que isto permite dizer (e o que não permite)

- A associação entre tela e sono é **pequena e positiva** na maior parte das bases, mas **varia muito entre elas** (H4.1). A estimativa combinada global resume bases heterogêneas e deve ser lida com cuidado.
- Com só 1 a 4 bases por subgrupo, o Q entre subgrupos tem pouco poder: "não rejeitar H0" em H4.2 **não** mostra que os tipos de exposição têm o mesmo efeito.
- Não foi detectada diferença entre o Brasil e os outros países com tempo total (H4.3, que agora compara com uma base só, a Argentina), nem, de forma exploratória, entre o Brasil e o resto do mundo. As duas bases brasileiras discordam entre si: PNS bruta negativa, Vigitel positiva. Ajustadas por idade, ambas ficam positivas.
- As nossas reanálises de tempo total ficam **abaixo** do intervalo da meta-análise de referência (H4.4). A referência mede uso geral × qualidade do sono, majoritariamente em jovens; nossos desfechos são insônia, problema de sono e latência em populações gerais. A diferença pode ser de população, de medida ou de seleção de estudos publicados.
- São dados transversais: o resultado é associação, não mostra causa."""),
]


def main():
    nb = nbf.v4.new_notebook()
    nb.cells = CELULAS
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    NotebookClient(nb, timeout=600, kernel_name="python3",
                   resources={"metadata": {"path": str(caminhos.RAIZ)}}).execute()
    caminhos.NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    destino = caminhos.NOTEBOOKS / "05_comparacao_mundial.ipynb"
    nbf.write(nb, destino)
    print("notebook executado e salvo em", destino)


if __name__ == "__main__":
    main()
