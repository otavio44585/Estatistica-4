"""Conjuntos de itens analisados na spec 002."""
from analise.harmonizacao.recodes import PHQ_ROTULOS

SLQ = [f"slq{i:03d}" for i in range(80, 150, 10)]
SLQ_ROTULOS = ["adormecer", "acordar à noite", "acordar cedo", "não descansado", "sonolência diurna",
               "sono insuficiente", "remédio para dormir"]
INSONIA_ROTULOS = ["dificuldade para adormecer", "dificuldade para voltar a dormir", "acordar cedo demais"]
SAS_ROTULOS = ["perde planos por causa do celular", "perde eficiência", "dor no punho/pescoço",
               "não suporta ficar sem", "impaciente sem o celular", "inquieto sem o celular",
               "não desiste apesar dos efeitos", "checa o tempo todo", "usa mais que o previsto",
               "outros dizem que usa demais"]
AIS_ROTULOS = ["indução do sono", "despertares noturnos", "despertar precoce", "duração total",
               "qualidade", "bem-estar diurno", "funcionamento diurno", "sonolência diurna"]

CONJUNTOS = [
    dict(id="insonia3_vigitel", base="vigitel2024", instrumento="insonia3", nome="3 sintomas de insônia",
         itens=["sintoma_1", "sintoma_2", "sintoma_3"], rotulos=INSONIA_ROTULOS, ordinal=True, peso=True),
    dict(id="insonia3_nhanes", base="nhanes0506", instrumento="insonia3", nome="3 sintomas de insônia",
         itens=["sintoma_1", "sintoma_2", "sintoma_3"], rotulos=INSONIA_ROTULOS, ordinal=True, peso=True),
    dict(id="sono7_nhanes", base="nhanes0506", instrumento="sono7", nome="7 sintomas de sono",
         itens=SLQ, rotulos=SLQ_ROTULOS, ordinal=True, peso=True),
    dict(id="phq9_pns", base="pns2019", instrumento="phq9", nome="PHQ-9",
         itens=[f"phq{i}" for i in range(1, 10)], rotulos=PHQ_ROTULOS, ordinal=True, peso=True),
    dict(id="phq9_nhanes", base="nhanes0506", instrumento="phq9", nome="PHQ-9",
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
POLICORICA = ["insonia3_vigitel", "insonia3_nhanes", "phq9_pns", "phq9_nhanes", "sono7_nhanes", "ais_japao"]

# Pares com o mesmo instrumento para a congruência de Tucker (H2.2 e H2.3)
PARES_TUCKER = [("insonia3_vigitel", "insonia3_nhanes", "H2.2"), ("phq9_pns", "phq9_nhanes", "H2.3")]
