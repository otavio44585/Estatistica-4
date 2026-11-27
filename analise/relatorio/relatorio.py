"""Preenche os modelos de docs/modelos/ com os números de resultados/ (analise.relatorio.numeros).

docs/modelos/relatorio.md            -> docs/relatorio.md
docs/modelos/roteiro_apresentacao.md -> docs/roteiro_apresentacao.md
docs/modelos/README.md               -> README.md                (se o modelo existir)
docs/modelos/apresentacao.html       -> site/apresentacao.html   (se o modelo existir; imagens embutidas)

Falha se algum {{marcador}} não tiver valor (princípio 2: nenhum resultado digitado à mão).
Nos destinos .html, todo src="<caminho>.png|.svg|.jpg" relativo à raiz do repositório vira data URI,
para a página funcionar sozinha (sem internet e no GitHub Pages).
"""
import base64
import datetime as dt
import mimetypes
import re

from analise.comum import caminhos
from analise.relatorio.numeros import carrega

RAIZ = caminhos.RAIZ
MODELOS = {
    "relatorio.md": RAIZ / "docs" / "relatorio.md",
    "roteiro_apresentacao.md": RAIZ / "docs" / "roteiro_apresentacao.md",
    "README.md": RAIZ / "README.md",
    "apresentacao.html": RAIZ / "site" / "apresentacao.html",
}
OPCIONAIS = {"README.md", "apresentacao.html"}
MARCADOR = re.compile(r"\{\{\s*([\w]+)\s*\}\}")
IMAGEM = re.compile(r'src="(?!data:|https?:)([^"]+\.(?:png|svg|jpg|jpeg))"')


def preenche(texto: str, N: dict) -> str:
    faltam = sorted({m for m in MARCADOR.findall(texto) if m not in N})
    if faltam:
        raise KeyError(f"marcadores sem valor: {faltam}")
    return MARCADOR.sub(lambda m: N[m.group(1)], texto)


def embute_imagens(html: str) -> str:
    """Troca src de imagem (caminho relativo à raiz do repositório) por data URI."""
    def troca(m):
        f = RAIZ / m.group(1)
        if not f.is_file():
            raise FileNotFoundError(f"imagem do modelo não encontrada: {m.group(1)}")
        tipo = mimetypes.guess_type(f.name)[0] or "image/png"
        if f.suffix == ".svg":
            tipo = "image/svg+xml"
        return f'src="data:{tipo};base64,{base64.b64encode(f.read_bytes()).decode()}"'
    return IMAGEM.sub(troca, html)


def apresentadores(N: dict) -> None:
    """Nomes de docs/modelos/integrantes.csv; sem nome preenchido, usa o papel do bloco."""
    import csv
    f = RAIZ / "docs" / "modelos" / "integrantes.csv"
    with open(f, encoding="utf-8-sig", newline="") as h:
        for linha in csv.DictReader(h, delimiter=";"):
            nome = (linha.get("nome") or "").strip()
            N[f"apresentador_{linha['bloco'].strip()}"] = nome or linha["papel"].strip()


def main():
    N = carrega()
    N["data"] = dt.date.today().strftime("%d/%m/%Y")
    apresentadores(N)
    erros = []
    for origem, destino in MODELOS.items():
        modelo = RAIZ / "docs" / "modelos" / origem
        if not modelo.exists():
            if origem in OPCIONAIS:
                continue
            raise FileNotFoundError(modelo)
        try:
            texto = preenche(modelo.read_text(encoding="utf-8"), N)
        except KeyError as e:                       # um modelo com chave faltando não impede os outros
            erros.append(f"{origem}: {e}")
            continue
        if destino.suffix == ".html":
            aviso = f"<!-- GERADO por analise/relatorio/relatorio.py a partir de docs/modelos/{origem}. Edite o modelo. -->\n"
            texto = embute_imagens(texto)
            texto = texto.replace("<!doctype html>", "<!doctype html>\n" + aviso, 1) if texto.lower().startswith("<!doctype html>") else aviso + texto
        else:
            texto = f"<!-- Arquivo GERADO por analise/relatorio/relatorio.py a partir de docs/modelos/{origem}. Edite o modelo, não este arquivo. -->\n\n" + texto
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8")
        print(destino.relative_to(RAIZ).as_posix())
    if erros:
        raise KeyError("modelos com marcadores sem valor:\n" + "\n".join(erros))


if __name__ == "__main__":
    main()
