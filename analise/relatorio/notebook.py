"""Monta um notebook a partir de uma lista de células e o executa com nbclient (saídas salvas no arquivo)."""
import nbformat
from nbclient import NotebookClient

from analise.comum import caminhos

CABECALHO = """import os, sys
from pathlib import Path
raiz = Path.cwd()
while not (raiz / "pytest.ini").exists() and raiz != raiz.parent:
    raiz = raiz.parent
sys.path.insert(0, str(raiz)); os.chdir(raiz)
import pandas as pd, numpy as np
pd.set_option("display.width", 160); pd.set_option("display.max_columns", 30)"""


def monta_e_executa(celulas, nome: str, timeout: int = 600):
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.cells.append(nbformat.v4.new_code_cell(CABECALHO))
    for tipo, texto in celulas:
        f = nbformat.v4.new_markdown_cell if tipo == "md" else nbformat.v4.new_code_cell
        nb.cells.append(f(texto.strip("\n")))
    NotebookClient(nb, timeout=timeout, kernel_name="python3",
                   resources={"metadata": {"path": str(caminhos.RAIZ)}}).execute()
    destino = caminhos.NOTEBOOKS / nome
    destino.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, destino)
    return destino
