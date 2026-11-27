"""Confere, item a item, que cada correção pedida pela verificação independente (docs/verificacao_independente.md)
está presente nos arquivos gerados. Se alguém regredir uma correção, o teste aponta qual item.

Os itens 1, 6 e 9 nasceram no NHANES (EUA), que saiu do trabalho em 2026-11-27. Os testes conferem o que
ainda vale deles: a regra de gl na PNS, a correção de Korn-Graubard na H3.7 da PNS e a ausência de base empilhada
(seção "Itens superados pela retirada dos EUA" do documento)."""
import re

import pandas as pd
import pytest

from analise.comum import caminhos

R, RAIZ = caminhos.RESULTADOS, caminhos.RAIZ


def csv(spec, nome):
    p = R / spec / "tabelas" / f"{nome}.csv"
    if not p.exists():
        pytest.skip(f"{p} não gerado")
    return pd.read_csv(p, sep=";", decimal=",", encoding="utf-8-sig")


def texto(rel):
    p = RAIZ / rel
    if not p.exists():
        pytest.skip(f"{rel} não gerado")
    return p.read_text(encoding="utf-8")


# ---- erros confirmados ---------------------------------------------------------------------------------------

def test_item01_regra_unica_de_gl_e_svyglm_como_sensibilidade():
    """Sem o NHANES, a regra gl = UPAs − estratos vale na PNS (única base com estrato e UPA); svyglm é sensibilidade."""
    rb = csv("003", "rp_bruta_ajustada")
    pns = rb[rb.base == "pns2019"].iloc[0]
    gl_pns = int(pns.n_upas - pns.n_estratos)
    assert gl_pns == 7453
    h3 = csv("003", "hipoteses")
    assert {"p_svyglm", "p_holm_svyglm", "decisao_svyglm"} <= set(h3.columns)
    r = h3[(h3.hipotese == "H3.2") & (h3.exposicao == "digital")].iloc[0]
    assert r.gl2 == gl_pns
    so_pns = h3[h3.gl2_svyglm.notna()]
    assert len(so_pns) and (so_pns.base == "pns2019").all() and (so_pns.gl2_svyglm < so_pns.gl2).all()
    assert (h3.decisao_svyglm == h3.decisao).all(), "a regra do svyglm mudou alguma decisão"
    s3 = csv("003", "sensibilidade")
    assert s3.modelo.str.contains("regra do svyglm").any()
    h5 = csv("005", "hipoteses").set_index("hipotese")
    assert (h5.regra_gl.dropna() == "UPAs − estratos").all()
    rel = texto("docs/relatorio.md")
    assert "svyglm" in rel and "UPAs − estratos" in rel and f"({gl_pns:,} gl)".replace(",", ".") in rel


def test_item02_roteiro_usa_o_F_do_excel_na_equivalencia():
    h5 = csv("005", "hipoteses").set_index("hipotese")
    f_excel = f"{h5.loc['H5.7', 'f_sem_peso']:.2f}".replace(".", ",")
    rot = texto("docs/roteiro_apresentacao.md")
    assert f"ANOVA de um fator do Excel no Vigitel (F = {f_excel})" in rot


def test_item03_tabela_53_separa_sem_peso_e_com_peso_com_gl():
    rel = texto("docs/relatorio.md")
    assert "| Sem peso (Excel) | Com peso (decisão) |" in rel
    linha = [l for l in rel.splitlines() if l.startswith("| H5.9 |")][0]
    assert re.search(r"t\([\d.,]+\) = ", linha), linha


def test_item04_conferencia_conta_excecoes_separadas():
    c = pd.read_csv(R / "005" / "conferencia.csv", sep=";", decimal=",", encoding="utf-8-sig")
    assert {"dentro_tolerancia", "excecao_documentada"} <= set(c.columns)
    dentro = c.dentro_tolerancia.astype(str).str.lower().eq("true")
    exc = c.excecao_documentada.astype(str).str.lower().eq("true")
    assert (dentro | exc).all(), "comparação fora da tolerância sem exceção documentada"
    assert "exceções documentadas" in texto("docs/relatorio.md")


@pytest.mark.parametrize("rel", ["docs/relatorio.md", "docs/roteiro_apresentacao.md",
                                 "docs/explicacoes/002_pca_analise_fatorial.md", "resultados/002/RESUMO.md",
                                 "resultados/003/RESUMO.md", "resultados/004/RESUMO.md", "resultados/005/RESUMO.md",
                                 "docs/explicacoes/003_brasil_eua.md", "docs/explicacoes/004_comparacao_mundial.md",
                                 "docs/explicacoes/005_regressao_anova_t.md"])
def test_item05_sem_igualdade_afirmada(rel):
    t = texto(rel)
    for frase in ["Brasil e EUA não diferem", "A associação é a mesma", "não varia por faixa etária", "quase não difere"]:
        assert frase not in t, f"{rel}: '{frase}'"


def test_item06_korn_graubard_na_pns():
    """H3.7 na PNS: Wald de q = 6 interações com d = 7453 gl de desenho vira F(q, d − q + 1)."""
    h3 = csv("003", "hipoteses")
    r = h3[(h3.hipotese == "H3.7") & (h3.base == "pns2019")].iloc[0]
    d, q = int(r.gl_desenho), int(r.gl1)
    assert (q, d) == (6, 7453) and r.gl2 == d - q + 1 == 7448
    assert "Korn-Graubard" in texto("docs/relatorio.md")


def test_item07_frase_de_rastreabilidade_restrita_a_resultados_proprios():
    assert "Todos os resultados próprios deste texto" in texto("docs/relatorio.md")


def test_item08_regex_causal_ampliada():
    t = texto("tests/test_006_entrega.py")
    assert r"\befeitos? d[aeo]s?\b" in t and r"\bleva(m)? (a|ao|à)\b" in t


def test_item09_nenhuma_base_empilhada_nem_nhanes():
    """O item 9 (gl da base empilhada Brasil + EUA) deixou de existir: não há base empilhada nem NHANES."""
    c = csv("003", "comparacoes_entre_bases")
    assert not c.metodo.str.contains("empilhada|interação país", regex=True).any()
    assert c.gl_base_empilhada.isna().all()
    h3 = csv("003", "hipoteses")
    assert not h3.hipotese.isin(["H3.3", "H3.6"]).any()
    assert not h3.base.astype(str).str.contains("nhanes").any()
    h5 = csv("005", "hipoteses")
    assert not h5.hipotese.isin(["H5.2", "H5.8", "H5.10", "H5.11"]).any()
    for spec, nome, col in [("001", "n_por_base", "base"), ("004", "efeitos_por_base", "base")]:
        assert not csv(spec, nome)[col].astype(str).str.contains("nhanes").any(), f"{spec}/{nome}"


def test_item10_rp_por_faixa_estimada_por_dominio():
    r = csv("003", "rp_por_faixa_etaria")
    pns = r[r.base == "pns2019"]
    assert pns.variancia.str.contains("domínio").all() and (pns.estratos_1upa == 0).all()
    assert (pns.n_upas == pns.n_upas.max()).all()       # todas as UPAs do desenho, não só as do subconjunto


def test_item11_clone_limpo_e_contagem_no_parquet():
    assert "def test_conferencia_funciona_em_clone_limpo" in texto("tests/test_005_confere_excel.py")
    assert "def test_contagem_no_proprio_parquet" in texto("tests/test_001_contagens.py")
    assert "skipped" in texto("README.md")


# ---- sugestões -----------------------------------------------------------------------------------------------

def test_sug_hartung_knapp_e_deff():
    m = csv("004", "meta_analise")
    assert {"rho_ic_inf_hk", "rho_ic_sup_hk", "p_efeito_hk"} <= set(m.columns)
    s = csv("004", "sensibilidade")
    assert s.analise.str.contains("deff de Kish").any()
    assert not s.analise.str.contains("NHANES").any()         # deff só da PNS e do Vigitel
    assert "Hartung-Knapp" in texto("docs/relatorio.md")


def test_sug_h42_omnibus_declarado():
    assert "omnibus" in texto("specs/004-comparacao-mundial/spec.md")


def test_sug_vif_abaixo_de_10():
    d = csv("005", "diagnostico")
    assert (d.vif_maximo <= 10).all(), d[["base", "vif_maximo", "regressor_vif_maximo"]]


def test_sug_escolaridade_anotada():
    eq = csv("001", "equivalencia")
    assert eq.astype(str).apply(lambda col: col.str.contains("médio incompleto")).any().any()


def test_sug_h1_bilateral_na_spec_003():
    assert "RP ≠ 1" in texto("specs/003-brasil-eua/spec.md")


def test_sug_cabecalhos_legiveis_no_site():
    h = texto("site/003.html")
    assert "<th>p (Holm)</th>" in h and "<th>p_holm</th>" not in h


def test_sug_sem_nome_pessoal_nas_specs():
    for p in (RAIZ / "specs").rglob("*.md"):
        assert "Felipe" not in p.read_text(encoding="utf-8"), p


def test_sug_holm_no_maximo_5pct():
    assert "no máximo 5%" in texto("docs/explicacoes/003_brasil_eua.md")


TECNICOS = ["efeito do desenho", "efeito de redação", "armadilha das dummies", "não dizer", "não permite",
            "não permitem", "não mostra causa", "não uma relação de causa", "causa insônia?", "não é causa",
            "falar em causa", "por causa d"]


@pytest.mark.parametrize("arq", sorted([*(RAIZ / "docs" / "explicacoes").glob("*.md"), *R.glob("*/RESUMO.md")]),
                         ids=lambda p: p.parent.name + "/" + p.name)
def test_item05_item08_sem_linguagem_causal_em_explicacoes_e_resumos(arq):
    """Inclui a 002: varre todas as explicações e todos os RESUMO.md."""
    ruins = []
    for linha in arq.read_text(encoding="utf-8").lower().splitlines():
        if any(t in linha for t in TECNICOS):
            continue
        if re.search(r"\b(causa|causam|provoca\w*)\b|\bleva(m)? (a|ao|à)\b|\befeitos? d[aeo]s? tela", linha):
            ruins.append(linha.strip()[:90])
    assert not ruins, ruins


def test_sug_plano_do_excel_sem_caminho_local():
    """Sugestão da verificação: o plano do ToolPak guarda só nomes de arquivo; o caminho absoluto vai num temporário."""
    p = RAIZ / "analise" / "dados" / "excel" / "plano_toolpak.json"
    if not p.exists():
        pytest.skip("plano não gerado (rode analise.regressao.prepara_excel)")
    t = p.read_text(encoding="utf-8")
    assert ":\\" not in t and ":/" not in t and "Users" not in t
    assert "mkstemp" in texto("analise/regressao/roda_excel.py")


def test_sug_roteiro_com_apresentadores_configuraveis():
    assert (RAIZ / "docs" / "modelos" / "integrantes.csv").exists()
    assert not re.search(r"Pessoa [1-4]", texto("docs/roteiro_apresentacao.md"))
