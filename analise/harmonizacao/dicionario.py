"""T011 — Dicionário harmonizado, tabela de equivalência e descritiva das bases processadas.

Gera:
  analise/dados/dicionario_harmonizado.csv   uma linha por (base, variável)
  resultados/001/tabelas/equivalencia.csv     variável × base, com o grau de equivalência
  resultados/001/tabelas/descritiva.csv       n válido, média, DP, mínimo, máximo por (base, variável)
  resultados/001/tabelas/n_por_base.csv       n de cada etapa de filtro (dos logs)
"""
import json

import pandas as pd

from analise.comum import caminhos


BASES = ["pns2019", "vigitel2024", "xuzhou", "argentina", "turquia", "japao"]

# (variável, base, origem, recodificação, faltantes, equivalência)
D = [
    ("sintoma_1", "vigitel2024", "r703", "1..5 -> 0..4", "777/888", "equivalente"),
    ("sintoma_2", "vigitel2024", "r704", "1..5 -> 0..4", "777/888", "equivalente"),
    ("sintoma_3", "vigitel2024", "r705", "1..5 -> 0..4", "777/888", "equivalente"),
    ("insonia_idx", "vigitel2024", "r703+r704+r705", "soma 0-12, só com os 3 itens", "-", "equivalente"),
    ("dif_adormecer_freq", "vigitel2024", "r703", "4 quase sempre, 5 sempre -> 1", "777/888", "equivalente (âncoras diferentes)"),
    ("problema_sono_freq", "pns2019", "N010", "3 mais da metade, 4 quase todos -> 1", "9", "aproximada: inclui despertar e dormir demais; 2 semanas"),
    ("problema_sono_ord", "pns2019", "N010", "1..4 -> 0..3", "9", "aproximada"),
    ("sono_horas", "vigitel2024", "r701_hh + r701_mm/60", "horas; 0 h -> faltante", "777/888", "aproximada: período de referência varia"),
    ("sono_horas", "argentina", "tposueñosemTRIMMED", "horas em dia de semana", "-", "aproximada"),
    ("sono_horas", "turquia", "sleep_duration_numeric", "texto com vírgula -> número", "branco", "aproximada"),
    ("sono_horas", "japao", "SDI_wd", "horas em dia de semana; 0 -> faltante", "0", "aproximada"),
    ("latencia_min", "argentina", "¿Cuánto tiempo en Minutos tardas en dormirte?", "minutos", "999", "equivalente"),
    ("latencia_min", "turquia", "sleep_latency_numeric", "minutos", "branco", "equivalente"),
    ("escore_sono_escala", "xuzhou", "PSQI", "0-21 (maior = pior)", "-", "não comparável entre escalas"),
    ("escore_sono_escala", "argentina", "Resultado (PDSS)", "0-32 (maior = mais sonolência)", "-", "não comparável entre escalas"),
    ("escore_sono_escala", "turquia", "puki_toplam (PSQI turco)", "0-21", "branco", "não comparável entre escalas"),
    ("escore_sono_escala", "japao", "AIStotal (Atenas)", "8-32 (itens 1-4)", "-", "não comparável entre escalas"),
    ("tela_digital_cat", "pns2019", "P04502", "6,1 -> 0; 2,3 -> 1; 4,5 -> 2", "9", "aproximada"),
    ("tela_digital_cat", "vigitel2024", "q59b/q59c", "q59b=2 ou q59c=1 -> 0; 2,3 -> 1; 4-7 -> 2", "777/888", "aproximada"),
    ("tela_tv_cat", "pns2019", "P04501", "6,1 -> 0; 2,3 -> 1; 4,5 -> 2", "9", "aproximada"),
    ("tela_tv_cat", "vigitel2024", "q59a", "8,1 -> 0; 2,3 -> 1; 4-7 -> 2", "777/888", "aproximada"),
    ("tela_digital_ord", "pns2019", "P04502", "não usa = 0, depois as 5 faixas em ordem", "9", "ordinal, faixas próprias"),
    ("tela_digital_ord", "vigitel2024", "q59b/q59c", "não usa = 0, depois as 7 faixas", "777/888", "ordinal, faixas próprias"),
    ("tela_presono_h", "argentina", "tela antes de dormir em dia de semana (h)", "horas", "-", "aproximada: janelas diferentes"),
    ("tela_presono_h", "japao", "mphone", "horas de celular nas 3 h antes de dormir (0-3)", "-", "aproximada: janelas diferentes"),
    ("tela_total_h", "argentina", "tpopantallatotalhstrimmed", "horas/dia", "-", "aproximada"),
    ("uso_problematico", "xuzhou", "SAS", "SAS-SV 10-60", "-", "não comparável entre escalas"),
    ("uso_problematico", "turquia", "FK_TOPLAM", "doomscrolling 15-105 (rótulo inferido, ver spec 005 T080)", "branco", "não comparável entre escalas"),
    ("idade", "pns2019", "C008", "anos", "-", "equivalente"),
    ("idade", "vigitel2024", "q6", "anos", "-", "equivalente"),
    ("idade", "argentina", "edad", "anos; 163 faltantes", "-", "equivalente"),
    ("idade", "turquia", "S1", "anos", "-", "equivalente"),
    ("idade", "japao", "age", "anos", "-", "equivalente"),
    ("sexo", "pns2019", "C006", "2 mulher -> 1", "9", "equivalente"),
    ("sexo", "vigitel2024", "q7", "2 feminino -> 1", "-", "equivalente"),
    ("sexo", "argentina", "sexonum", "0 Femenino -> 1", "-", "equivalente"),
    ("sexo", "xuzhou", "gender", "código 2 -> 1 (rótulo não documentado)", "-", "rótulo desconhecido"),
    ("sexo", "japao", "gender", "código 2 -> 1 (rótulo não documentado)", "-", "rótulo desconhecido"),
    ("escolaridade3", "pns2019", "VDD004A", "1-4 -> 0; 5 -> 1; 6,7 -> 2", "-", "aproximada: médio incompleto = 0 (no Vigitel, 9-11 anos de estudo = 1)"),
    ("escolaridade3", "vigitel2024", "fesc", "0-8 anos -> 0; 9-11 -> 1; 12+ -> 2", "-", "aproximada: 9-11 anos inclui médio incompleto, que na PNS fica em 0"),
    ("depressao_phq9", "pns2019", "N010-N018", "soma 0-27 (ordem PHQ-9)", "9", "equivalente"),
    ("depressao_diag", "vigitel2024", "r205", "1 sim -> 1", "777/888", "aproximada: diagnóstico referido"),
    ("peso", "pns2019", "V00291", "-", "-", "-"), ("estrato", "pns2019", "V0024", "-", "-", "-"), ("upa", "pns2019", "UPA_PNS", "-", "-", "-"),
    ("peso", "vigitel2024", "pesorake2025", "-", "-", "-"),
]
CONTRATO = ["dif_adormecer_freq", "problema_sono_freq", "sintoma_1", "sintoma_2", "sintoma_3", "insonia_idx",
            "sono_horas", "latencia_min", "escore_sono_escala", "tela_digital_cat", "tela_tv_cat", "tela_presono_h",
            "uso_problematico", "idade", "faixa_etaria", "sexo", "escolaridade3", "depressao_phq9", "depressao_diag",
            "peso", "estrato", "upa"]


def main():
    dic = pd.DataFrame(D, columns=["variavel", "base", "origem", "recodificacao", "faltantes", "equivalencia"])
    dados = {b: pd.read_parquet(caminhos.processado(b)) for b in BASES}
    # toda variável do dicionário existe na base processada
    falta = [(r.base, r.variavel) for r in dic.itertuples() if r.variavel not in dados[r.base].columns]
    assert not falta, f"variáveis do dicionário ausentes no processado: {falta}"
    dic["n_validos"] = [int(dados[r.base][r.variavel].notna().sum()) for r in dic.itertuples()]
    dic.to_csv(caminhos.DADOS / "dicionario_harmonizado.csv", sep=";", index=False, encoding="utf-8-sig")

    out = caminhos.saida("001")
    eq = pd.DataFrame(index=CONTRATO, columns=BASES, dtype=object)
    for v in CONTRATO:
        for b in BASES:
            linha = dic[(dic.variavel == v) & (dic.base == b)]
            if len(linha):
                eq.loc[v, b] = linha.equivalencia.iloc[0]
            elif v in dados[b].columns and dados[b][v].notna().any():
                eq.loc[v, b] = "derivada"
            else:
                eq.loc[v, b] = "ausente"
    eq.index.name = "variavel"
    eq.to_csv(out / "tabelas" / "equivalencia.csv", sep=";", encoding="utf-8-sig")

    linhas = []
    for b, df in dados.items():
        for v in df.columns:
            s = pd.to_numeric(df[v], errors="coerce")
            if s.notna().sum() == 0 or v in ("id",):
                continue
            linhas.append(dict(base=b, variavel=v, n_validos=int(s.notna().sum()), n_total=len(df),
                               media=s.mean(), dp=s.std(), minimo=s.min(), maximo=s.max()))
    pd.DataFrame(linhas).round(4).to_csv(out / "tabelas" / "descritiva.csv", sep=";", index=False,
                                         decimal=",", encoding="utf-8-sig")
    ns = []
    for b in BASES:
        for etapa, n in json.loads((caminhos.LOGS / f"{b}.json").read_text(encoding="utf-8")).items():
            ns.append(dict(base=b, etapa=etapa, n=n))
    pd.DataFrame(ns).to_csv(out / "tabelas" / "n_por_base.csv", sep=";", index=False, encoding="utf-8-sig")
    print(eq.to_string())


if __name__ == "__main__":
    main()
