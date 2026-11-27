"""Caminhos do projeto. Os brutos vêm da variável de ambiente STAT4_BRUTOS (princípio 14)."""
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DADOS = RAIZ / "analise" / "dados"
PROCESSADOS = DADOS / "processados"
LOGS = DADOS / "logs"
RESULTADOS = RAIZ / "resultados"
NOTEBOOKS = RAIZ / "analise" / "notebooks"


def brutos() -> Path:
    """Pasta dos microdados brutos. Sem STAT4_BRUTOS, tenta ../pesquisa/dados (irmã do repositório)."""
    valor = os.environ.get("STAT4_BRUTOS")
    p = Path(valor) if valor else RAIZ.parent / "pesquisa" / "dados"
    if not p.is_dir():
        raise RuntimeError(
            "Pasta dos brutos não encontrada. Defina STAT4_BRUTOS com o caminho da pasta "
            "que contém pns_2019/, vigitel_2006_2024/ e as pastas dos repositórios"
        )
    return p


def saida(spec: str) -> Path:
    """resultados/<spec>/ com subpastas tabelas/ e figuras/."""
    p = RESULTADOS / spec
    (p / "tabelas").mkdir(parents=True, exist_ok=True)
    (p / "figuras").mkdir(parents=True, exist_ok=True)
    return p


def processado(base: str) -> Path:
    return PROCESSADOS / f"{base}.parquet"
