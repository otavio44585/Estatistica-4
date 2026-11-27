"""T066 — Bases de procedência questionável (só sensibilidade, princípio 1) e contraponto da Holanda.

Lidas direto dos brutos; nada daqui entra na estimativa principal.
"""
import numpy as np
import pandas as pd

from analise.comum import caminhos

ORD_PAQ_Q13 = {"Less than 30 minutes": 0, "30 minutes – 1 hour": 1, "1–2 hours": 2, "2–3 hours": 3,
               "3–5 hours": 4, "More than 5 hours": 5}
ORD_FREQ_BGD = {"Never": 0, "Rarely (1-2 times a week)": 1, "Sometimes (3-4 times a week)": 2,
                "Often (5-6 times a week)": 3, "Every night": 4}
ORD_CEL_SP = {"Less than 15 minutes": 0, "15–30 minutes": 1, "30–60 minutes": 2, "1–2 hours": 3,
              "More than 2 hours": 4}
ORD_QUAL_SP = {"Very Poor": 0, "Poor": 1, "Average": 2, "Good": 3, "Very Good": 4}   # maior = melhor -> inverter


def paquistao() -> pd.DataFrame:
    d = pd.read_excel(caminhos.brutos() / "repo_figshare_socialmedia_psqi_paquistao" / "Social_Media_Article_Complete_Data.xlsx")
    return pd.DataFrame({"x": d["Q13_Daily_social_media_use_6band"].map(ORD_PAQ_Q13),
                         "y": pd.to_numeric(d["PSQI_Global_Score"], errors="coerce")})


def bangladesh() -> pd.DataFrame:
    d = pd.read_csv(caminhos.brutos() / "repo_mendeley_student_insomnia_bangladesh" /
                    "Student_Insomnia_Educational_Outcomes_version-2.csv")
    cx = [c for c in d.columns if c.startswith("11.")][0]
    cy = [c for c in d.columns if c.startswith("3.")][0]
    return pd.DataFrame({"x": d[cx].map(ORD_FREQ_BGD), "y": d[cy].map(ORD_FREQ_BGD)})


def sleep_patterns(arquivo: str) -> pd.DataFrame:
    d = pd.read_csv(caminhos.brutos() / "repo_mendeley_sleep_patterns_college" / arquivo)
    cx = [c for c in d.columns if c.startswith("5.")][0]
    cy = [c for c in d.columns if c.startswith("6.")][0]
    return pd.DataFrame({"x": d[cx].map(ORD_CEL_SP), "y": d[cy].map(ORD_QUAL_SP)})


QUESTIONAVEIS = [
    # (rótulo, tipo, função, inverte, exposição, desfecho)
    ("Paquistão (redes sociais × PSQI)", "tempo total", paquistao, False,
     "uso diário de redes sociais (6 faixas)", "PSQI global"),
    ("Bangladesh v2 (dispositivo antes de dormir × dificuldade para adormecer)", "pré-sono", bangladesh, False,
     "frequência de uso de dispositivo antes de dormir (5 níveis)", "frequência de dificuldade para adormecer (5 níveis)"),
    ("Sleep Patterns 2.722 (celular antes de dormir × qualidade)", "pré-sono",
     lambda: sleep_patterns("vpmfsbpt89_Sleep_Patterns_Responses_2721.csv"), True,
     "tempo no celular antes de dormir (5 faixas)", "qualidade do sono (invertida)"),
    ("Sleep Patterns 1.222 (celular antes de dormir × qualidade)", "pré-sono",
     lambda: sleep_patterns("h75rzz3y6n_Sleep_Patterns_Responses_1222.csv"), True,
     "tempo no celular antes de dormir (5 faixas)", "qualidade do sono (invertida)"),
]


def holanda() -> pd.DataFrame:
    """Siebers et al. (2024): celular na hora antes de deitar (log de app) e qualidade do sono, por noite."""
    d = pd.read_csv(caminhos.brutos() / "repo_figshare_siebers2024_nightlife" / "phone.csv")
    d = d.replace(-999, np.nan)
    d["sleep_qual_inv"] = -d["sleep_qual"]          # maior qualidade = melhor; invertido para o sinal padrão
    return d
