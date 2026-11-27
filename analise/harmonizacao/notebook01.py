"""Gera e executa analise/notebooks/01_dados_harmonizados.ipynb (narrativa da spec 001)."""
from analise.relatorio.notebook import monta_e_executa

C = [
    ("md", """
# 01 — Dados harmonizados (spec 001)

**Pergunta:** dá para medir tela e sono de forma comparável entre as bases?

Este notebook não recalcula a harmonização: ela roda pelos scripts `analise/harmonizacao/*.py`, que gravam
`analise/dados/processados/<base>.parquet` e um log com o n depois de cada filtro. Aqui se lê o resultado
e se mostra o que cada base tem.

| Base | País | Desenho | Script |
|---|---|---|---|
| PNS 2019 | Brasil | inquérito domiciliar com peso, estrato e UPA | `pns2019.py` |
| Vigitel 2024 | Brasil (27 capitais) | inquérito telefônico com peso | `vigitel2024.py` |
| NHANES 2005-06 | EUA | inquérito com peso, estrato e UPA | `nhanes0506.py` |
| Xuzhou, Pérez-Chada, Doomscrolling, Okajima | China, Argentina, Turquia, Japão | amostras de conveniência (repositórios CC BY 4.0) | `repositorios.py` |
"""),
    ("md", "## 1. Quantas pessoas sobram em cada filtro\n\nOs números conferem com o inventário (`tests/test_001_contagens.py`)."),
    ("code", """from analise.comum.estatistica import le_csv
n = pd.read_csv("resultados/001/tabelas/n_por_base.csv", sep=";", encoding="utf-8-sig")
n"""),
    ("md", """## 2. Recodificação da exposição

As faixas de horas são diferentes em cada questionário. O ponto comum é cortar em **1 h** e **3 h**:
0 = não usa ou < 1 h; 1 = 1 a < 3 h; 2 = ≥ 3 h. As tabelas abaixo são as que o código usa (`recodes.py`)."""),
    ("code", """from analise.harmonizacao import recodes as R
pd.DataFrame({"PNS P04502 (código → faixa)": R.PNS_CAT, "NHANES PAD600": pd.Series(R.NH_CAT)}).rename_axis("código original")"""),
    ("md", """## 3. Equivalência entre bases

`equivalente` = mesma pergunta; `aproximada` = pergunta ou faixa diferente (a comparação diz o quê);
`não comparável` = escalas diferentes, que só se comparam por métrica padronizada (spec 004)."""),
    ("code", """eq = pd.read_csv("resultados/001/tabelas/equivalencia.csv", sep=";", encoding="utf-8-sig", index_col=0)
eq.loc[["insonia_idx", "dif_adormecer_freq", "problema_sono_freq", "latencia_min", "tela_digital_cat", "escolaridade3"]]"""),
    ("md", "## 4. Distribuição da exposição e dos desfechos (com peso amostral)"),
    ("code", """prev = pd.read_csv("resultados/001/tabelas/prevalencias.csv", sep=";", decimal=",", encoding="utf-8-sig")
prev"""),
    ("code", """from IPython.display import Image, display
display(Image("resultados/001/figuras/exposicao_tela_digital.png"))
display(Image("resultados/001/figuras/indice_insonia.png"))"""),
    ("md", """## 5. Leitura

- Em 2019, 22% dos adultos brasileiros (PNS) usavam computador, tablet ou celular no lazer 3 h ou mais por dia;
  no Vigitel 2024 (capitais) eram 27%. No NHANES 2005-06, antes do smartphone, eram 7%.
- O NHANES de 2005 mede outra época: a comparação Brasil × EUA mistura país e período (limitação declarada na 003 e na 005).
- Os três sintomas de insônia do Vigitel e do NHANES são a mesma pergunta, com âncoras de frequência diferentes.
  O item de sono da PNS é o do PHQ-9 e inclui dormir demais: só é comparável de forma aproximada.

Os percentuais deste texto vêm de `resultados/001/tabelas/prevalencias.csv`, impresso acima."""),
]

if __name__ == "__main__":
    print(monta_e_executa(C, "01_dados_harmonizados.ipynb"))
