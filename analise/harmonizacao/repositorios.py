"""T007–T010 — Harmoniza as quatro bases de repositório (CC BY 4.0, sem desenho amostral complexo).

Xuzhou (China), Pérez-Chada (Argentina), Doomscrolling (Turquia), Okajima (Japão).
"""
import numpy as np
import pandas as pd

from analise.comum import caminhos
from analise.comum.faltantes import troca_por_nan
from analise.comum.validacao import Log, salva_base


def xuzhou() -> pd.DataFrame:
    base, log = "xuzhou", Log("xuzhou")
    df = pd.read_excel(caminhos.brutos() / "repo_figshare_xuzhou_sassv_psqi_china" / "pone.0340852.s001.xlsx")
    log("linhas no arquivo", len(df))
    sas = [c for c in df.columns[:df.columns.get_loc("SAS_AV（2 represent addiction）")] if str(c).startswith("@")]
    assert len(sas) == 10 and (df[sas].sum(axis=1) == df.SAS).all(), "itens do SAS-SV não somam o total"
    o = pd.DataFrame({"base": base, "pais": "China", "id": df["order number"]})
    o["sexo"] = (df.gender == 2).astype(float)          # rótulo 1/2 não documentado no depósito
    o["serie"], o["renda"], o["regiao"] = df.grade, df.economic, df.region
    for i, c in enumerate(sas, 1):
        o[f"sas{i}"] = df[c]
    o["uso_problematico"], o["uso_problematico_nome"] = df.SAS, "SAS-SV (10-60)"
    o["escore_sono_escala"], o["escore_sono_nome"] = df.PSQI, "PSQI (0-21)"
    return salva_base(o, base, log, extra={"escore_sono_escala": (0, 21), "uso_problematico": (10, 60),
                                           **{f"sas{i}": (1, 6) for i in range(1, 11)}})


def argentina() -> pd.DataFrame:
    base, log = "argentina", Log("argentina")
    df = pd.read_excel(caminhos.brutos() / "repo_mendeley_screen_sleep_adolesc_argentina" / "repositorio.xlsx")
    log("linhas brutas", len(df))
    df = df[df.excluFINAL == 0].reset_index(drop=True); log("completos do artigo (excluFINAL = 0)", len(df))
    df = df.rename(columns={
        "¿Cuánto tiempo en Minutos tardas en dormirte?": "latencia",
        "¿Cuánto tiempo de pantalla (dispositivos electrónicos) utilizas antes de dormirte los días de semana?": "presono"})
    df = troca_por_nan(df, base)
    o = pd.DataFrame({"base": base, "pais": "Argentina", "id": df["Código"]})
    o["idade"] = df.edad                                   # 163 sem idade (sem data de nascimento)
    o["serie"] = df.grado
    o["sexo"] = 1 - df.sexonum                             # sexonum: 0 = Femenino, 1 = Masculino
    o["escolaridade_pais"] = df.niveducpadresRECOD
    o["latencia_min"] = df.latencia
    o["tela_presono_h"] = df.presono
    o["tela_total_h"] = df.tpopantallatotalhstrimmed
    o["sono_horas"] = df["tposueñosemTRIMMED"]
    o["escore_sono_escala"], o["escore_sono_nome"] = df.Resultado, "PDSS sonolência diurna (0-32)"
    return salva_base(o, base, log, extra={"escore_sono_escala": (0, 32), "idade": (10, 25)})


def turquia() -> pd.DataFrame:
    base, log = "turquia", Log("turquia")
    df = pd.read_csv(caminhos.brutos() / "repo_mendeley_doomscrolling_sleep_turquia" / "Doomscrolling.csv",
                     sep=None, engine="python", encoding="utf-8-sig")
    log("linhas no arquivo", len(df))
    df = df.replace(r"^\s*$", np.nan, regex=True)
    fk, ue = [f"FK{i}" for i in range(1, 16)], [f"UE{i}" for i in range(1, 10)]
    for c in fk + ue + ["S1", "puki_toplam", "FK_TOPLAM", "UE_TOPLAM", "sleep_latency_numeric"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    assert (df[fk].sum(axis=1) == df.FK_TOPLAM).all(), "itens FK não somam FK_TOPLAM"
    o = pd.DataFrame({"base": base, "pais": "Turquia", "id": df.anket_no})
    o["idade"] = df.S1                                     # sexo sem rótulo no depósito: não usado
    for i, c in enumerate(fk, 1):
        o[f"fk{i}"] = df[c]
    for i, c in enumerate(ue, 1):
        o[f"ue{i}"] = df[c]
    o["uso_problematico"], o["uso_problematico_nome"] = df.FK_TOPLAM, "Doomscrolling (FK, 15-105)"
    o["procrastinacao"] = df.UE_TOPLAM
    o["latencia_min"] = df.sleep_latency_numeric
    o["sono_horas"] = pd.to_numeric(df.sleep_duration_numeric.astype(str).str.replace(",", "."), errors="coerce")
    o["escore_sono_escala"], o["escore_sono_nome"] = df.puki_toplam, "PSQI turco (0-21)"
    return salva_base(o, base, log, extra={"escore_sono_escala": (0, 21), "uso_problematico": (15, 105),
                                           **{f"fk{i}": (1, 7) for i in range(1, 16)}})


def japao() -> pd.DataFrame:
    base, log = "japao", Log("japao")
    df = pd.read_csv(caminhos.brutos() / "repo_zenodo_okajima_bedtime_procrastination_japao" / "BPS_study.csv")
    log("linhas no arquivo", len(df))
    ais = [f"AIS{i}" for i in range(1, 9)]
    bps = ["BPS1", "BPS2R", "BPS3R", "BPS4", "BPS5", "BPS6", "BPS7R", "BPS8", "BPS9R"]
    assert (df[ais].sum(axis=1) == df.AIStotal).all() and (df[bps].sum(axis=1) == df.BPStotal).all()
    o = pd.DataFrame({"base": base, "pais": "Japão", "id": df.No})
    o["idade"] = df.age
    o["sexo"] = (df.gender == 2).astype(float)            # rótulo 1/2 não documentado no depósito
    for i, c in enumerate(ais, 1):
        o[f"ais{i}"] = df[c]
    for i, c in enumerate(bps, 1):
        o[f"bps{i}"] = df[c]
    o["procrastinacao"] = df.BPStotal
    o["tela_presono_h"] = df.mphone
    o["sono_horas"] = df.SDI_wd.where(df.SDI_wd > 0)       # 0 h em 9 casos = faltante
    o["escore_sono_escala"], o["escore_sono_nome"] = df.AIStotal, "AIS Atenas (8-32)"
    return salva_base(o, base, log, extra={"escore_sono_escala": (8, 32), **{f"ais{i}": (1, 4) for i in range(1, 9)}})


if __name__ == "__main__":
    for f in (xuzhou, argentina, turquia, japao):
        f()
