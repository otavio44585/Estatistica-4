"""T085–T086 — Roda a Análise de Dados do Excel (caminho A) em cada pasta de trabalho.

Uma instância do Excel por arquivo (abrir o segundo arquivo na mesma instância derrubou o Excel com
"servidor RPC não disponível"). Cada chamada tem teto de tempo (princípio 15).
Uso: python -m analise.regressao.roda_excel [base ...]
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from analise.comum import caminhos

PASTA = caminhos.DADOS / "excel"
PS1 = caminhos.RAIZ / "analise" / "regressao" / "excel_toolpak.ps1"


def main(filtro=None):
    plano = json.loads((PASTA / "plano_toolpak.json").read_text(encoding="utf-8"))
    ok = True
    for pasta in plano["pastas"]:
        nome = Path(pasta["arquivo"].replace("\\", "/")).name
        if filtro and not any(f in nome for f in filtro):
            continue
        # o plano salvo guarda só o nome do arquivo (sem caminho local); o caminho absoluto que o Excel exige
        # vai num JSON temporário fora do repositório, apagado logo depois
        exec_pasta = {**pasta, "arquivo": str((PASTA / nome).resolve())}
        fd, tmp = tempfile.mkstemp(prefix="stat4_plano_", suffix=".json")
        um = Path(tmp)
        with open(fd, "w", encoding="utf-8") as f:
            json.dump({"pastas": [exec_pasta]}, f, ensure_ascii=False)
        try:
            r = subprocess.run(["pwsh", "-NoProfile", "-File", str(PS1), "-Plano", str(um), "-LimiteSeg", "600"],
                               capture_output=True, text=True, timeout=700, encoding="utf-8", errors="replace")
            saida = (r.stdout + r.stderr).strip().splitlines()
            falhou = r.returncode != 0 or any("Exception" in s or "erro" in s.lower() or "RPC" in s for s in saida)
        except subprocess.TimeoutExpired:
            saida, falhou = ["tempo esgotado"], True
        print(f"{'FALHOU' if falhou else 'ok'}  {nome}  ({sum('OK ' in s for s in saida)} saídas)")
        if falhou:
            ok = False
            print("\n".join(saida[-5:]))
        um.unlink(missing_ok=True)
    return ok


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:] or None) else 1)
