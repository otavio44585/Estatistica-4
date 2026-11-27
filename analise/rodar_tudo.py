"""Roda o trabalho inteiro, na ordem das specs, a partir dos microdados brutos (STAT4_BRUTOS).

Uso:
  python -m analise.rodar_tudo               tudo (harmonização leva alguns minutos: PNS tem 455 MB)
  python -m analise.rodar_tudo --sem-brutos  pula a 001 e usa os processados já existentes
  python -m analise.rodar_tudo --sem-excel   pula a automação do Excel (caminho A da 005);
                                             a conferência usa as planilhas já salvas
Cada passo roda como processo separado; o primeiro erro interrompe tudo.
"""
import subprocess
import sys
import time

HARMONIZACAO = ["analise.harmonizacao.pns2019", "analise.harmonizacao.vigitel2024",
                "analise.harmonizacao.repositorios",
                "analise.harmonizacao.dicionario"]
PASSOS = [
    ("001", ["analise.harmonizacao.figuras", "analise.harmonizacao.notebook01"]),
    ("002", ["analise.multivariada.analisa", "analise.multivariada.notebooks"]),
    ("003", ["analise.brasil_eua.executa", "analise.brasil_eua.resumo", "analise.brasil_eua.notebook"]),
    ("004", ["analise.mundial.rodar", "analise.mundial.notebook"]),
    ("005", ["analise.regressao.prepara_excel", "analise.regressao.roda_excel", "analise.regressao.modelos",
             "analise.regressao.confere_excel", "analise.regressao.diagnostico", "analise.regressao.resumo",
             "analise.regressao.notebook"]),
    ("006", ["analise.relatorio.figuras_apresentacao", "analise.relatorio.relatorio", "analise.relatorio.gerar_site",
             "analise.relatorio.exporta_pdf"]),
]


def roda(modulo: str):
    t0 = time.time()
    print(f"→ {modulo}", flush=True)
    r = subprocess.run([sys.executable, "-m", modulo])
    if r.returncode != 0:
        sys.exit(f"falhou: {modulo} (código {r.returncode})")
    print(f"  ok em {time.time() - t0:.0f} s", flush=True)


def main(args):
    if "--sem-brutos" not in args:
        for m in HARMONIZACAO:
            roda(m)
    for spec, modulos in PASSOS:
        for m in modulos:
            if m == "analise.regressao.roda_excel" and "--sem-excel" in args:
                print(f"→ {m} pulado (--sem-excel)")
                continue
            roda(m)
    roda("pytest")


if __name__ == "__main__":
    main(sys.argv[1:])
