"""T060 — Pares exposição × desfecho da spec 004 (fixados no plano em 2026-11-27, antes do cálculo).

Sinal padronizado: positivo = mais tela, pior sono. `inverte=True` troca o sinal quando o desfecho
é "quanto maior, melhor" (duração, qualidade).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Par:
    base: str
    tipo: str            # "tempo total" | "pré-sono" | "uso problemático"
    exposicao: str
    desfecho: str
    inverte: bool
    rot_exposicao: str
    rot_desfecho: str
    equivalencia: str
    principal: bool = True
    peso: str | None = None


TIPOS = ["tempo total", "pré-sono", "uso problemático"]

PRINCIPAIS = [
    Par("pns2019", "tempo total", "tela_digital_ord", "problema_sono_ord", False,
        "computador/tablet/celular no lazer (6 faixas)", "problema no sono nas últimas 2 semanas (0-3)",
        "aproximada: item do PHQ-9 inclui despertar e dormir demais", peso="peso"),
    Par("vigitel2024", "tempo total", "tela_digital_ord", "insonia_idx", False,
        "computador/tablet/celular no tempo livre (8 faixas)", "índice de insônia, 3 sintomas (0-12)",
        "equivalente ao NHANES no desfecho; exposição aproximada", peso="peso"),
    Par("nhanes0506", "tempo total", "tela_digital_ord", "insonia_idx", False,
        "computador/games fora do trabalho (7 faixas)", "índice de insônia, 3 sintomas (0-12)",
        "equivalente ao Vigitel no desfecho; exposição de 2005, antes do smartphone", peso="peso"),
    Par("argentina", "tempo total", "tela_total_h", "latencia_min", False,
        "horas de tela por dia", "latência do sono (min)", "aproximada: adolescentes"),
    Par("japao", "pré-sono", "tela_presono_h", "escore_sono_escala", False,
        "horas de celular nas 3 h antes de dormir", "Escala de Insônia de Atenas (8-32)", "aproximada"),
    Par("xuzhou", "uso problemático", "uso_problematico", "escore_sono_escala", False,
        "SAS-SV, dependência de smartphone (10-60)", "PSQI (0-21)", "aproximada"),
    Par("turquia", "uso problemático", "uso_problematico", "escore_sono_escala", False,
        "escala de doomscrolling (15-105)", "PSQI turco (0-21)", "aproximada: rótulo da escala inferido"),
]

SENSIBILIDADE = [
    Par("argentina", "pré-sono", "tela_presono_h", "latencia_min", False,
        "horas de tela antes de dormir", "latência do sono (min)", "aproximada", principal=False),
    Par("argentina", "tempo total", "tela_total_h", "sono_horas", True,
        "horas de tela por dia", "duração do sono em dia de semana (h, invertida)", "aproximada", principal=False),
    Par("argentina", "pré-sono", "tela_presono_h", "sono_horas", True,
        "horas de tela antes de dormir", "duração do sono em dia de semana (h, invertida)", "aproximada", principal=False),
    Par("japao", "pré-sono", "tela_presono_h", "sono_horas", True,
        "horas de celular nas 3 h antes de dormir", "duração do sono em dia de semana (h, invertida)", "aproximada",
        principal=False),
    Par("turquia", "uso problemático", "uso_problematico", "latencia_min", False,
        "escala de doomscrolling (15-105)", "latência do sono (min)", "aproximada", principal=False),
]
