"""Exporta site/apresentacao.html para site/apresentacao.pdf com o Chrome (ou Edge) sem janela.

Uso: python -m analise.relatorio.exporta_pdf
Um slide por página (1280×720), pelo CSS @page do próprio deck. Precisa de Chrome ou Edge instalado;
sem navegador, avisa e não falha o pipeline.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from analise.comum import caminhos

CANDIDATOS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "google-chrome", "chromium", "chromium-browser", "msedge",
]


def navegador():
    for c in CANDIDATOS:
        if Path(c).exists() or shutil.which(c):
            return c
    return None


def main():
    html = caminhos.RAIZ / "site" / "apresentacao.html"
    pdf = caminhos.RAIZ / "site" / "apresentacao.pdf"
    nav = navegador()
    if nav is None:
        print("aviso: Chrome/Edge não encontrado; PDF não gerado")
        return 0
    with tempfile.TemporaryDirectory(prefix="stat4_chrome_") as perfil:   # perfil isolado, apagado no fim
        cmd = [nav, "--headless=new", "--disable-gpu", f"--user-data-dir={perfil}", "--no-pdf-header-footer",
               "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000",
               f"--print-to-pdf={pdf}", html.resolve().as_uri()]
        subprocess.run(cmd, capture_output=True, timeout=180)
    if not pdf.exists() or pdf.stat().st_size < 10_000:
        print("falhou: PDF não gerado")
        return 1
    paginas = pdf.read_bytes().count(b"/Type /Page") - pdf.read_bytes().count(b"/Type /Pages")
    print(f"{pdf.relative_to(caminhos.RAIZ).as_posix()}: {paginas} páginas, {pdf.stat().st_size / 1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
