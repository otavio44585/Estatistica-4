"""Conjuntos de itens analisados na spec 002.

2026-11-27: os EUA (NHANES 2005-06) saíram do trabalho inteiro; os conjuntos do NHANES e as comparações
Brasil × EUA (Tucker, H2.2–H2.4) foram retirados. Ver o Histórico de specs/002-estrutura-latente/spec.md.
"""
from analise.harmonizacao.recodes import PHQ_ROTULOS

INSONIA_ROTULOS = ["dificuldade para adormecer", "dificuldade para voltar a dormir", "acordar cedo demais"]
# Vigitel 2024: variável original e rótulo do dicionário (dicionario-vigitel-2006-2024.xlsx); respostas 1 nunca .. 5 sempre
INSONIA_VIGITEL_ORIGEM = {"sintoma_1": ("r703", "dificuldade para dormir"),
                          "sintoma_2": ("r704", "acordou e teve dificuldade pra dormir de novo"),
                          "sintoma_3": ("r705", "acordou antes da hora desejada e não conseguiu dormir de novo")}
SAS_ROTULOS = ["perde planos por causa do celular", "perde eficiência", "dor no punho/pescoço",
               "não suporta ficar sem", "impaciente sem o celular", "inquieto sem o celular",
               "não desiste apesar dos efeitos", "checa o tempo todo", "usa mais que o previsto",
               "outros dizem que usa demais"]
AIS_ROTULOS = ["indução do sono", "despertares noturnos", "despertar precoce", "duração total",
               "qualidade", "bem-estar diurno", "funcionamento diurno", "sonolência diurna"]

CONJUNTOS = [
    dict(id="insonia3_vigitel", base="vigitel2024", instrumento="insonia3", nome="3 sintomas de insônia",
         itens=["sintoma_1", "sintoma_2", "sintoma_3"], rotulos=INSONIA_ROTULOS, ordinal=True, peso=True),
    dict(id="phq9_pns", base="pns2019", instrumento="phq9", nome="PHQ-9",
         itens=[f"phq{i}" for i in range(1, 10)], rotulos=PHQ_ROTULOS, ordinal=True, peso=True),
    dict(id="sassv_xuzhou", base="xuzhou", instrumento="sassv", nome="SAS-SV (uso problemático)",
         itens=[f"sas{i}" for i in range(1, 11)], rotulos=SAS_ROTULOS, ordinal=False, peso=False),
    dict(id="doomscrolling_turquia", base="turquia", instrumento="doomscrolling", nome="Doomscrolling (FK)",
         itens=[f"fk{i}" for i in range(1, 16)], rotulos=[f"FK{i}" for i in range(1, 16)], ordinal=False, peso=False),
    dict(id="procrastinacao_turquia", base="turquia", instrumento="procrastinacao", nome="Procrastinação do sono (UE)",
         itens=[f"ue{i}" for i in range(1, 10)], rotulos=[f"UE{i}" for i in range(1, 10)], ordinal=False, peso=False),
    dict(id="ais_japao", base="japao", instrumento="ais", nome="AIS (insônia de Atenas)",
         itens=[f"ais{i}" for i in range(1, 9)], rotulos=AIS_ROTULOS, ordinal=True, peso=False),
    dict(id="bps_japao", base="japao", instrumento="bps", nome="BPS (procrastinação do sono)",
         itens=[f"bps{i}" for i in range(1, 10)], rotulos=[f"BPS{i}" for i in range(1, 10)], ordinal=False, peso=False),
]
POR_ID = {c["id"]: c for c in CONJUNTOS}

# Conjuntos com robustez por correlação policórica (spec: "pelo menos 3 sintomas e PHQ-9")
POLICORICA = ["insonia3_vigitel", "phq9_pns", "ais_japao"]

# Pares para a congruência de Tucker entre países: vazio desde 2026-11-27 (H2.2 e H2.3 retiradas, EUA fora)
PARES_TUCKER = []
RETIRADAS = {"H2.2": "cargas do fator de insônia equivalentes entre Brasil e EUA (Tucker)",
             "H2.3": "PHQ-9 com a mesma estrutura na PNS e no NHANES (Tucker)",
             "H2.4": "item de sono do PHQ-9 no mesmo fator nos dois países"}
NOTA_RETIRADA = "retirada em 2026-11-27 (EUA fora do trabalho)"
