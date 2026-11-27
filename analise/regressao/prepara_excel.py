"""T083 — Gera as planilhas para a Análise de Dados do Excel e o plano de execução do ToolPak.

Para cada base: analise/dados/excel/<base>_resultados.xlsx (fora do git: tem microdados) com
  dados        Y na coluna A, tela e covariáveis contíguas (só casos completos, tudo numérico)
  anova        Y em 3 colunas, uma por faixa de tela (Vigitel)
  teste_t      Y em 2 colunas: ≥ 3 h e < 1 h (Vigitel)
  dummy_2grupos Y e a dummy ≥ 3 h, só nesses dois grupos (mostra que t com variâncias iguais = t da dummy)
  log          n antes e depois de remover faltantes
(NHANES e base empilhada retirados em 2026-11-27: EUA fora do trabalho). Também escreve analise/dados/excel/plano_toolpak.json,
que o excel_toolpak.ps1 executa, com as fórmulas do caminho B (p recalculado pela estatística e pelos gl).
"""
import json

import openpyxl
import pandas as pd
from openpyxl.utils import get_column_letter as L

from analise.comum import caminhos
from analise.regressao import dados as D

PASTA = caminhos.DADOS / "excel"


def _escreve(ws, df: pd.DataFrame):
    ws.append(list(df.columns))
    for row in df.itertuples(index=False):
        ws.append([None if pd.isna(v) else float(v) for v in row])


def _formulas_regressao(n_coefs: int) -> list:
    """Caminho B ao lado da saída da Regressão: p de cada coeficiente e F de significação."""
    f = [{"celula": "G11", "formula": "F de significação conferido (fórmula)"},
         {"celula": "G12", "formula": "=F.DIST.RT(E12,B12,B13)"},
         {"celula": "H16", "formula": "p conferido (fórmula)"}]
    for r in range(17, 17 + n_coefs):
        f.append({"celula": f"H{r}", "formula": f"=T.DIST.2T(ABS(D{r}),$B$13)"})
    return f


def _f_parcial(completo: str, restrito: str, q: int) -> list:
    return [
        {"celula": "A1", "formula": f"F parcial: {completo} × {restrito}"},
        {"celula": "A2", "formula": "q (restrições)"}, {"celula": "B2", "formula": str(q)},
        {"celula": "A3", "formula": "F"},
        {"celula": "B3", "formula": f"=(({restrito}!C13-{completo}!C13)/B2)/({completo}!C13/{completo}!B13)"},
        {"celula": "A4", "formula": "gl1"}, {"celula": "B4", "formula": "=B2"},
        {"celula": "A5", "formula": "gl2"}, {"celula": "B5", "formula": f"={completo}!B13"},
        {"celula": "A6", "formula": "p"}, {"celula": "B6", "formula": "=F.DIST.RT(B3,B4,B5)"},
        {"celula": "A7", "formula": "ΔR²"}, {"celula": "B7", "formula": f"={completo}!B5-{restrito}!B5"},
        {"celula": "A8", "formula": "f²"}, {"celula": "B8", "formula": f"=B7/(1-{completo}!B5)"},
    ]


def _tarefa_reg(aba_saida, aba, n, c0, c1, n_coefs):
    return {"ferramenta": "Regress", "aba_dados": aba, "aba_saida": aba_saida,
            "y": f"A1:A{n + 1}", "x": f"{L(c0)}1:{L(c1)}{n + 1}", "formulas": _formulas_regressao(n_coefs)}


def prepara_base(base: str) -> dict:
    m = D.POR_BASE[base]
    df, info = D.matriz(base)
    n, nt, nc = len(df), len(info["tela"]), len(info["cov"])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "dados"
    _escreve(ws, df)
    tarefas = [
        _tarefa_reg("reg_completo", "dados", n, 2, 1 + nt + nc, 1 + nt + nc),
        _tarefa_reg("reg_simples", "dados", n, 2, 1 + nt, 1 + nt),
        _tarefa_reg("reg_covariaveis", "dados", n, 2 + nt, 1 + nt + nc, 1 + nc),
        {"ferramenta": "Formulas", "aba_dados": "dados", "aba_saida": "f_parcial",
         "formulas": _f_parcial("reg_completo", "reg_covariaveis", nt)},
    ]
    if info["tela_cat"] is not None:
        g, _ = D.grupos_tela(base)
        an = pd.concat([s.reset_index(drop=True).rename(k) for k, s in g.items()], axis=1)
        _escreve(wb.create_sheet("anova"), an)
        nmax = an.notna().sum().max()
        tarefas.append({"ferramenta": "Anova1", "aba_dados": "anova", "aba_saida": "anova_saida",
                        "entrada": f"A1:C{nmax + 1}",
                        "formulas": [{"celula": "H11", "formula": "p conferido (fórmula)"},
                                     {"celula": "H12", "formula": "=F.DIST.RT(E12,C12,C13)"}]})
        tt = pd.concat([g["≥ 3 h"].reset_index(drop=True).rename("tela_3h_mais"),
                        g["< 1 h"].reset_index(drop=True).rename("tela_menos_1h")], axis=1)
        _escreve(wb.create_sheet("teste_t"), tt)
        n1, n2 = len(g["≥ 3 h"]), len(g["< 1 h"])
        tarefas.append({"ferramenta": "Pttestv", "aba_dados": "teste_t", "aba_saida": "teste_t_welch",
                        "entrada1": f"A1:A{n1 + 1}", "entrada2": f"B1:B{n2 + 1}",
                        "formulas": [{"celula": "D11", "formula": "p conferido (fórmula, gl inteiro do Excel)"},
                                     {"celula": "D12", "formula": "=T.DIST.2T(ABS(B9),B8)"}]})
        tarefas.append({"ferramenta": "Ttestm", "aba_dados": "teste_t", "aba_saida": "teste_t_igual",
                        "entrada1": f"A1:A{n1 + 1}", "entrada2": f"B1:B{n2 + 1}",
                        "formulas": [{"celula": "D12", "formula": "p conferido (fórmula)"},
                                     {"celula": "D13", "formula": "=T.DIST.2T(ABS(B10),B9)"}]})
        y2 = pd.concat([g["≥ 3 h"], g["< 1 h"]])
        d2 = pd.DataFrame({m.y: y2.to_numpy(), "tela_3h_mais": [1.0] * n1 + [0.0] * n2})
        _escreve(wb.create_sheet("dummy_2grupos"), d2)
        tarefas.append(_tarefa_reg("reg_dummy_2grupos", "dummy_2grupos", n1 + n2, 2, 2, 2))
    lg = wb.create_sheet("log")
    lg.append(["etapa", "n"])
    lg.append(["base processada (spec 001)", info["n_partida"]])
    lg.append(["casos completos do modelo", n])
    PASTA.mkdir(parents=True, exist_ok=True)
    arq = PASTA / f"{base}_resultados.xlsx"
    wb.save(arq)
    print(f"{base}: {n} casos completos de {info['n_partida']} -> {arq.name}")
    return {"arquivo": arq.name, "tarefas": tarefas}


def main():
    for velho in ("nhanes0506_resultados.xlsx", "empilhada_resultados.xlsx"):   # EUA fora do trabalho
        (PASTA / velho).unlink(missing_ok=True)
    pastas = [prepara_base(m.base) for m in D.MODELOS]
    (PASTA / "plano_toolpak.json").write_text(json.dumps({"pastas": pastas}, ensure_ascii=False, indent=1),
                                              encoding="utf-8")


if __name__ == "__main__":
    main()
