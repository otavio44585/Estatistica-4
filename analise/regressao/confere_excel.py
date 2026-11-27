"""T088 — Conferência dos p-valores e demais números por três caminhos.

  A = saída da Análise de Dados do Excel (ToolPak), lida das abas de saída
  B = fórmula nativa do Excel ao lado da saída (T.DIST.2T, F.DIST.RT), recalculada pelo próprio Excel
  C = script (analise/regressao/ols.py e scipy), recalculado a partir dos dados processados

Tolerância: diferença relativa < 1e-8; dois valores < 1e-15 contam como iguais.
Saídas: resultados/005/conferencia.csv e resultados/005/excel_saidas/<base>__<aba>.csv.

Clone limpo: as pastas de trabalho (analise/dados/excel/) têm microdados e ficam fora do git. Sem elas, o
caminho A é lido das abas exportadas em resultados/005/excel_saidas/ (mesma grade de células), e a conferência
roda igual em qualquer sistema, sem Excel.

Colunas de conferencia.csv: `ok` (True/False, ou "informativo" na linha que compara o p de Welch com gl inteiro
do Excel × gl fracionário do script), `dentro_tolerancia` (booleana) e `excecao_documentada` (booleana).

O layout da saída da ToolPak é fixo (posições conferidas no teste com o exercício da aula); os rótulos
podem vir em inglês ou em português, conforme o idioma do Excel.
"""
import numpy as np
import openpyxl
import pandas as pd
from openpyxl.utils.cell import column_index_from_string, coordinate_from_string
from scipy import stats

from analise.comum import caminhos
from analise.comum.estatistica import salva_csv
from analise.regressao import dados as D
from analise.regressao.ols import mqo, f_parcial

PASTA = caminhos.DADOS / "excel"
OUT = caminhos.saida("005")
TOL = 1e-8
TITULOS_REG = {"SUMMARY OUTPUT", "RESUMO DOS RESULTADOS"}
ROT_ENTRE = {"Between Groups", "Entre grupos"}


def iguais(a, b) -> tuple[bool, float]:
    if a is None or b is None or (isinstance(a, float) and np.isnan(a)) or (isinstance(b, float) and np.isnan(b)):
        return False, np.nan
    a, b = float(a), float(b)
    if abs(a) < 1e-15 and abs(b) < 1e-15:
        return True, 0.0
    d = abs(a - b) / max(abs(a), abs(b))
    return d < TOL, d


class Conferencia:
    def __init__(self):
        self.linhas = []

    def add(self, base, aba, item, A, C, B=None):
        okAC, dAC = iguais(A, C)
        linha = dict(base=base, aba=aba, item=item, A_toolpak=A, B_formula=B, C_script=C, dif_rel_A_C=dAC,
                     dif_rel_B_C=np.nan, ok=okAC)
        if B is not None:
            okBC, dBC = iguais(B, C)
            linha.update(dif_rel_B_C=dBC, ok=okAC and okBC)
        self.linhas.append(linha)


class _Celula:
    def __init__(self, valor):
        self.value = valor


class _AbaCSV:
    """Aba exportada (CSV sem cabeçalho) com acesso ws["B4"].value, como no openpyxl."""

    def __init__(self, caminho):
        self.grade = pd.read_csv(caminho, sep=";", header=None, dtype=str, encoding="utf-8-sig",
                                 keep_default_na=False).to_numpy()

    def __getitem__(self, coord):
        col, lin = coordinate_from_string(coord)
        i, j = lin - 1, column_index_from_string(col) - 1
        if i >= self.grade.shape[0] or j >= self.grade.shape[1]:
            return _Celula(None)
        v = self.grade[i, j]
        if v == "":
            return _Celula(None)
        try:
            return _Celula(float(v))
        except ValueError:
            return _Celula(v)


class _PastaCSV:
    def __init__(self, base):
        self.base = base

    def __getitem__(self, aba):
        return _AbaCSV(OUT / "excel_saidas" / f"{self.base}__{aba}.csv")


def abre(base):
    """Pasta de trabalho salva pelo Excel; sem ela (clone limpo), as abas exportadas em CSV."""
    arq = PASTA / f"{base}_resultados.xlsx"
    if arq.exists():
        return openpyxl.load_workbook(arq, data_only=True), True
    if not (OUT / "excel_saidas" / f"{base}__reg_completo.csv").exists():
        raise FileNotFoundError(f"nem {arq} nem resultados/005/excel_saidas/{base}__*.csv")
    return _PastaCSV(base), False


EXPORTA = True


def exporta_aba(ws, base, aba):
    if not EXPORTA or isinstance(ws, _AbaCSV):
        return
    grade = [[c.value for c in row] for row in ws.iter_rows()]
    pd.DataFrame(grade).to_csv(OUT / "excel_saidas" / f"{base}__{aba}.csv", sep=";", index=False, header=False,
                               encoding="utf-8-sig")


def confere_regressao(cf, ws, base, aba, a, nomes):
    assert ws["A1"].value in TITULOS_REG, f"{base}/{aba}: saída da Regressão não encontrada"
    v = lambda c: ws[c].value
    cf.add(base, aba, "R múltiplo", v("B4"), a.r_multiplo)
    cf.add(base, aba, "R²", v("B5"), a.r2)
    cf.add(base, aba, "R² ajustado", v("B6"), a.r2_aj)
    cf.add(base, aba, "erro padrão", v("B7"), a.erro_padrao)
    cf.add(base, aba, "observações", v("B8"), a.n)
    cf.add(base, aba, "gl regressão", v("B12"), a.k)
    cf.add(base, aba, "SQ regressão", v("C12"), a.sq_reg)
    cf.add(base, aba, "F", v("E12"), a.f)
    cf.add(base, aba, "F de significação", v("F12"), a.p_f, B=v("G12"))
    cf.add(base, aba, "gl resíduo", v("B13"), a.gl_res)
    cf.add(base, aba, "SQ resíduo", v("C13"), a.sq_res)
    for j, nome in enumerate(nomes):
        r = 17 + j
        cf.add(base, aba, f"{nome}: coeficiente", v(f"B{r}"), a.b[j])
        cf.add(base, aba, f"{nome}: erro padrão", v(f"C{r}"), a.ep[j])
        cf.add(base, aba, f"{nome}: t", v(f"D{r}"), a.t[j])
        cf.add(base, aba, f"{nome}: p", v(f"E{r}"), a.p[j], B=v(f"H{r}"))
        cf.add(base, aba, f"{nome}: IC inferior", v(f"F{r}"), a.ic_inf[j])
        cf.add(base, aba, f"{nome}: IC superior", v(f"G{r}"), a.ic_sup[j])


def confere_f_parcial(cf, ws, base, fp):
    cf.add(base, "f_parcial", "F parcial", ws["B3"].value, fp["f"])
    cf.add(base, "f_parcial", "p do F parcial", ws["B6"].value, fp["p"])
    cf.add(base, "f_parcial", "ΔR²", ws["B7"].value, fp["delta_r2"])
    cf.add(base, "f_parcial", "f²", ws["B8"].value, fp["f2"])


def confere_base(cf, base):
    wb, _ = abre(base)
    (OUT / "excel_saidas").mkdir(exist_ok=True)
    df, info = D.matriz(base)
    m = D.POR_BASE[base]
    y = df[m.y]
    nt = info["tela"]
    modelos = {"reg_completo": nt + info["cov"], "reg_simples": nt, "reg_covariaveis": info["cov"]}
    aj = {}
    for aba, cols in modelos.items():
        aj[aba] = mqo(y, df[cols])
        confere_regressao(cf, wb[aba], base, aba, aj[aba], ["Intercepto"] + cols)
        exporta_aba(wb[aba], base, aba)
    confere_f_parcial(cf, wb["f_parcial"], base, f_parcial(aj["reg_completo"], aj["reg_covariaveis"]))
    exporta_aba(wb["f_parcial"], base, "f_parcial")
    if info["tela_cat"] is not None:
        g, _ = D.grupos_tela(base)
        ws = wb["anova_saida"]
        assert ws["A12"].value in ROT_ENTRE, f"{base}: layout da ANOVA inesperado ({ws['A12'].value})"
        f, p = stats.f_oneway(*g.values())
        sq_ent = sum(len(s) * (s.mean() - y.mean()) ** 2 for s in g.values())
        sq_dent = sum(((s - s.mean()) ** 2).sum() for s in g.values())
        for r, (nome, s) in zip((5, 6, 7), g.items()):
            cf.add(base, "anova_saida", f"{nome}: n", ws[f"B{r}"].value, len(s))
            cf.add(base, "anova_saida", f"{nome}: média", ws[f"D{r}"].value, s.mean())
            cf.add(base, "anova_saida", f"{nome}: variância", ws[f"E{r}"].value, s.var())
        cf.add(base, "anova_saida", "SQ entre", ws["B12"].value, sq_ent)
        cf.add(base, "anova_saida", "SQ dentro", ws["B13"].value, sq_dent)
        cf.add(base, "anova_saida", "gl entre", ws["C12"].value, 2)
        cf.add(base, "anova_saida", "gl dentro", ws["C13"].value, len(y) - 3)
        cf.add(base, "anova_saida", "F", ws["E12"].value, f)
        cf.add(base, "anova_saida", "p", ws["F12"].value, p, B=ws["H12"].value)
        cf.add(base, "anova_saida", "F (ANOVA) = F global da regressão nas dummies", ws["E12"].value,
               aj["reg_simples"].f)
        exporta_aba(ws, base, "anova_saida")
        a, b0 = g["≥ 3 h"], g["< 1 h"]
        ws = wb["teste_t_welch"]
        tw = stats.ttest_ind(a, b0, equal_var=False)
        v1, v2 = a.var() / len(a), b0.var() / len(b0)
        gl_w = (v1 + v2) ** 2 / (v1 ** 2 / (len(a) - 1) + v2 ** 2 / (len(b0) - 1))
        cf.add(base, "teste_t_welch", "média ≥ 3 h", ws["B4"].value, a.mean())
        cf.add(base, "teste_t_welch", "média < 1 h", ws["C4"].value, b0.mean())
        cf.add(base, "teste_t_welch", "gl (Excel arredonda o gl de Welch)", ws["B8"].value, round(gl_w))
        cf.add(base, "teste_t_welch", "t", ws["B9"].value, tw.statistic)
        cf.add(base, "teste_t_welch", "p bicaudal (C com gl inteiro, como o Excel)", ws["B12"].value,
               2 * stats.t.sf(abs(tw.statistic), round(gl_w)), B=ws["D12"].value)
        linha = dict(base=base, aba="teste_t_welch", item="p bicaudal: gl inteiro (Excel) × gl fracionário (script)",
                     A_toolpak=ws["B12"].value, B_formula=None, C_script=tw.pvalue,
                     dif_rel_A_C=abs(ws["B12"].value - tw.pvalue) / tw.pvalue, dif_rel_B_C=np.nan,
                     ok="informativo")
        cf.linhas.append(linha)
        exporta_aba(ws, base, "teste_t_welch")
        ws = wb["teste_t_igual"]
        ti = stats.ttest_ind(a, b0, equal_var=True)
        cf.add(base, "teste_t_igual", "gl", ws["B9"].value, len(a) + len(b0) - 2)
        cf.add(base, "teste_t_igual", "t", ws["B10"].value, ti.statistic)
        cf.add(base, "teste_t_igual", "p bicaudal", ws["B13"].value, ti.pvalue, B=ws["D13"].value)
        exporta_aba(ws, base, "teste_t_igual")
        y2 = pd.concat([a, b0]).reset_index(drop=True)
        r2g = mqo(y2, pd.DataFrame({"tela_3h_mais": [1.0] * len(a) + [0.0] * len(b0)}))
        confere_regressao(cf, wb["reg_dummy_2grupos"], base, "reg_dummy_2grupos", r2g, ["Intercepto", "tela_3h_mais"])
        cf.add(base, "reg_dummy_2grupos", "t da dummy = t do teste t com variâncias iguais",
               wb["reg_dummy_2grupos"]["D18"].value, ti.statistic)
        exporta_aba(wb["reg_dummy_2grupos"], base, "reg_dummy_2grupos")


def confere_empilhada(cf):
    wb, _ = abre("empilhada")
    df, _ = D.empilhada()
    y = df["insonia_idx"]
    X = df.drop(columns="insonia_idx")
    Xr = X.drop(columns=["eua_x_tela_1a3h", "eua_x_tela_3h_mais"])
    a_c, a_r = mqo(y, X), mqo(y, Xr)
    confere_regressao(cf, wb["reg_completo"], "empilhada", "reg_completo", a_c, a_c.nomes)
    confere_regressao(cf, wb["reg_restrito"], "empilhada", "reg_restrito", a_r, a_r.nomes)
    confere_f_parcial(cf, wb["f_parcial"], "empilhada", f_parcial(a_c, a_r))
    for aba in ("reg_completo", "reg_restrito", "f_parcial"):
        exporta_aba(wb[aba], "empilhada", aba)


def main():
    cf = Conferencia()
    for m in D.MODELOS:
        confere_base(cf, m.base)
    confere_empilhada(cf)
    out = pd.DataFrame(cf.linhas)
    out["excecao_documentada"] = out.ok.astype(str) == "informativo"
    out["dentro_tolerancia"] = (~out.excecao_documentada) & (out.ok.astype(str) == "True")
    salva_csv(out, OUT / "conferencia.csv")
    av = out[~out.excecao_documentada]
    falhas = av[~av.dentro_tolerancia]
    print(f"{len(av)} números conferidos; {int(av.dentro_tolerancia.sum())} dentro da tolerância; "
          f"{int(out.excecao_documentada.sum())} exceções documentadas; {len(falhas)} divergências acima de {TOL}")
    print(f"maior diferença relativa A×C: {av.dif_rel_A_C.max():.2e}; B×C: {av.dif_rel_B_C.max():.2e}")
    if len(falhas):
        print(falhas[["base", "aba", "item", "A_toolpak", "B_formula", "C_script", "dif_rel_A_C", "dif_rel_B_C"]].to_string())
    return len(falhas) == 0


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
