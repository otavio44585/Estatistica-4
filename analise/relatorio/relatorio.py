"""Preenche os modelos docs/modelos/*.md com os números de resultados/ (analise.relatorio.numeros).

docs/modelos/relatorio.md            -> docs/relatorio.md
docs/modelos/roteiro_apresentacao.md -> docs/roteiro_apresentacao.md

Falha se algum {{marcador}} não tiver valor (princípio 2: nenhum número digitado à mão).
"""
import datetime as dt
import re

from analise.comum import caminhos
from analise.relatorio.numeros import carrega

MODELOS = {"relatorio.md": "relatorio.md", "roteiro_apresentacao.md": "roteiro_apresentacao.md"}
MARCADOR = re.compile(r"\{\{\s*([\w]+)\s*\}\}")


def preenche(texto: str, N: dict) -> str:
    faltam = sorted({m for m in MARCADOR.findall(texto) if m not in N})
    if faltam:
        raise KeyError(f"marcadores sem valor: {faltam}")
    return MARCADOR.sub(lambda m: N[m.group(1)], texto)


def apresentadores(N: dict) -> None:
    """Nomes de docs/modelos/integrantes.csv; sem nome preenchido, usa o papel do bloco."""
    import csv
    f = caminhos.RAIZ / "docs" / "modelos" / "integrantes.csv"
    with open(f, encoding="utf-8-sig", newline="") as h:
        for linha in csv.DictReader(h, delimiter=";"):
            nome = (linha.get("nome") or "").strip()
            N[f"apresentador_{linha['bloco'].strip()}"] = nome or linha["papel"].strip()


def main():
    N = carrega()
    N["data"] = dt.date.today().strftime("%d/%m/%Y")
    apresentadores(N)
    docs = caminhos.RAIZ / "docs"
    aviso = "<!-- Arquivo GERADO por analise/relatorio/relatorio.py a partir de docs/modelos/{}. Edite o modelo, não este arquivo. -->\n\n"
    for origem, destino in MODELOS.items():
        texto = (docs / "modelos" / origem).read_text(encoding="utf-8")
        (docs / destino).write_text(aviso.format(origem) + preenche(texto, N), encoding="utf-8")
        print("docs/" + destino)


if __name__ == "__main__":
    main()
