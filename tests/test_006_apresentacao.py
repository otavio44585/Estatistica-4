"""Spec 006 — deck da apresentação (site/apresentacao.html, gerado de docs/modelos/apresentacao.html) e roteiro.

Critérios: arquivo gerado sem marcador pendente; autocontido (imagens em data URI, sem CSS/JS/fonte externos;
links <a> para o repositório são permitidos); 15 a 20 slides de 1280×720 com regra de impressão; nota do
apresentador em todo slide; nenhuma frase causal afirmativa (mesma lógica de test_006_entrega.py); sem
"Pessoa 1–4"; EUA/NHANES fora do deck e do roteiro (decisão do grupo, 2026-11-27); figuras da apresentação
embutidas; tabela de testes com as hipóteses pedidas e decisões iguais às dos CSVs de resultados/.
"""
import html
import re

import pandas as pd
import pytest

from analise.comum import caminhos
from analise.relatorio.relatorio import MARCADOR

RAIZ = caminhos.RAIZ
RESULTADOS = caminhos.RESULTADOS
DECK = RAIZ / "site" / "apresentacao.html"
MODELO = RAIZ / "docs" / "modelos" / "apresentacao.html"
ROTEIRO_MODELO = RAIZ / "docs" / "modelos" / "roteiro_apresentacao.md"
ROTEIRO = RAIZ / "docs" / "roteiro_apresentacao.md"
CAUSAIS = [r"\bcausa(m|ram)?\b(?! insônia\?)", r"\bprovoca", r"\befeitos? d[aeo]s?\b", r"\bleva(m)? (a|ao|à)\b"]
NEGA_CAUSA = r"não (permite|permitem|é|causa)|causa insônia\?|exigiria"
SLIDE = re.compile(r'<div class="slide[\s"]')
EUA = re.compile(r"\bEUA\b|NHANES|Estados Unidos|norte-american", re.I)
FIGURAS = [
    "resultados/006/figuras/teste_explicado.png",
    "resultados/006/figuras/testes_painel.png",
    "resultados/006/figuras/confundimento_idade.png",
    "resultados/006/figuras/decomposicao_r2.png",
    "resultados/006/figuras/brasil_no_mundo.png",
    "resultados/002/figuras/cargas_insonia_vigitel.png",
    "resultados/003/figuras/rp_por_pais.png",
]
HIPOTESES = ["H3.1", "H3.2", "H3.4", "H3.7", "H3.8", "H3.9", "H4.1", "H4.2", "H4.3", "H4.4",
             "H5.1", "H5.3", "H5.4", "H5.5", "H5.6", "H5.7", "H5.9"]
LINHA_TESTE = re.compile(r'<tr data-h="(H\d\.\d+)"([^>]*)>(.*?)</tr>', re.S)


@pytest.fixture(scope="module")
def deck():
    assert DECK.exists(), "site/apresentacao.html não existe (rode python -m analise.relatorio.relatorio)"
    return DECK.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def modelo():
    assert MODELO.exists(), "docs/modelos/apresentacao.html não existe"
    return MODELO.read_text(encoding="utf-8")


def _frames(h):
    return h.split('<section class="frame"')[1:]


def _visivel(h):
    """Texto que aparece na tela ou nas notas: sem <script>, <style>, data URI e tags."""
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S | re.I)
    h = re.sub(r'src="data:[^"]*"', "", h)
    h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    return html.unescape(h)


def _sem_data_uri(h):
    return re.sub(r'src="data:[^"]*"', "", h)


def test_deck_gerado_sem_marcador(deck):
    assert "<title>" in deck
    assert "{{" not in deck


def test_modelo_usa_so_chaves_existentes(modelo):
    from analise.relatorio.numeros import carrega
    from analise.relatorio.relatorio import apresentadores
    N = carrega() | {"data": "x"}
    apresentadores(N)
    for nome, texto in [("apresentacao.html", modelo), ("roteiro_apresentacao.md", ROTEIRO_MODELO.read_text(encoding="utf-8"))]:
        faltam = set(MARCADOR.findall(texto)) - set(N)
        assert not faltam, f"{nome}: {faltam}"


def test_imagens_embutidas(deck):
    srcs = re.findall(r'\ssrc="([^"]*)"', deck)
    assert srcs, "deck sem imagem"
    fora = [s[:60] for s in srcs if not s.startswith("data:image/")]
    assert not fora, f"imagem não embutida: {fora}"


@pytest.mark.parametrize("figura", FIGURAS)
def test_figuras_da_apresentacao_no_modelo(modelo, figura):
    assert f'src="{figura}"' in modelo, f"figura fora do deck: {figura}"
    assert (RAIZ / figura).is_file(), f"figura não gerada: {figura}"


def test_sem_dependencia_externa(deck):
    """Nada carregado de fora. Link <a href> para o repositório é navegação, não dependência."""
    assert not re.search(r"<link[^>]+stylesheet|<script[^>]+src=", deck, re.I), "CSS/JS externo"
    assert not re.search(r"@import|fonts\.googleapis|fonts\.gstatic", deck, re.I), "fonte ou CSS importado"
    assert not re.search(r'src="(https?:)?//', deck, re.I), "recurso remoto"
    assert not re.search(r'<(link|img|script|iframe|source|video|audio)\b[^>]*href="(https?:)?//', deck, re.I), "recurso remoto"
    assert not re.search(r"url\((?!\s*['\"]?(data:|#))", deck), "url() que não é data URI nem âncora"


def test_repositorio_publico_no_fim(deck):
    fim = _frames(deck)[-1]
    assert "github.com/otavio44585/Estatistica-4" in fim
    assert "otavio44585.github.io/Estatistica-4" in fim


def test_numero_de_slides(deck):
    n = len(SLIDE.findall(deck))
    assert 15 <= n <= 20, f"{n} slides"
    assert n == len(_frames(deck)), "todo slide fica dentro de um <section class=\"frame\">"


def test_geometria_e_impressao(deck):
    assert re.search(r"--slide-w:\s*1280px", deck) and re.search(r"--slide-h:\s*720px", deck)
    assert re.search(r"@page\s*\{[^}]*size:\s*1280px 720px", deck), "@page sem tamanho do slide"
    assert re.search(r"@media print", deck) and "break-after: page" in deck


def test_cada_slide_tem_nota(deck):
    for k, f in enumerate(_frames(deck), 1):
        m = re.search(r'<aside class="notes[^"]*">(.*?)</aside>', f, re.S)
        assert m, f"slide {k} sem nota do apresentador"
        assert len(_visivel(m.group(1)).split()) >= 8, f"slide {k}: nota vazia ou curta demais"


def test_notas_trazem_quem_apresenta(modelo):
    for i in range(1, 5):
        assert "{{apresentador_%d}}" % i in modelo, f"notas sem apresentador_{i}"
        assert "{{apresentador_%d}}" % i in ROTEIRO_MODELO.read_text(encoding="utf-8"), f"roteiro sem apresentador_{i}"


def test_sem_linguagem_causal_afirmativa(deck):
    linhas = [l for l in _visivel(deck).lower().splitlines() if not re.search(NEGA_CAUSA, l)]
    for padrao in CAUSAIS:
        achou = [l.strip()[:80] for l in linhas if re.search(padrao, l)]
        assert not achou, f"linguagem causal no deck: {achou}"


def test_sem_marcador_de_pessoa(deck):
    assert not re.search(r"Pessoa [1-4]", deck)


def test_sem_eua_no_deck(deck, modelo):
    """O NHANES 2005-06 saiu do trabalho: nada de EUA no modelo (texto, alt, comentários) nem no deck gerado."""
    assert not EUA.search(modelo), EUA.search(modelo).group(0)
    achou = EUA.search(_visivel(_sem_data_uri(deck)))
    assert not achou, achou.group(0)
    assert not EUA.search(" ".join(re.findall(r'alt="([^"]*)"', deck)))


@pytest.mark.parametrize("arq", [ROTEIRO_MODELO, ROTEIRO], ids=["modelo", "gerado"])
def test_sem_eua_no_roteiro(arq):
    if not arq.exists():
        pytest.skip(f"{arq.name} não gerado")
    t = arq.read_text(encoding="utf-8")
    achou = EUA.search(t)
    assert not achou, achou.group(0)


@pytest.mark.parametrize("chave", ["data", "n_total", "n_brasil", "w_brasil", "pct_n_argentina_reg", "pct_n_resto3",
                                   "alfa_insonia3_vigitel", "kmo_insonia3_vigitel", "rho_max",
                                   "rp_bruta_digital_pns2019", "rp_ajustada_digital_pns2019",
                                   "r2u_vigitel2024_tela", "r2u_pns2019_idade", "r2u_pns2019_sexo"])
def test_conteudo_obrigatorio_no_modelo(modelo, chave):
    """Capa com data, países, PCA, Brasil no mundo, confundimento e decomposição do R²: vêm de marcadores."""
    assert "{{%s}}" % chave in modelo


def test_tabela_de_testes_tem_as_hipoteses_pedidas(deck):
    achadas = {m.group(1) for m in LINHA_TESTE.finditer(deck)}
    faltam = [h for h in HIPOTESES if h not in achadas]
    assert not faltam, f"hipóteses fora da tabela de testes: {faltam}"


def _attr(attrs, nome):
    m = re.search(rf'data-{nome}="([^"]*)"', attrs)
    return html.unescape(m.group(1)) if m else None


def test_decisoes_da_tabela_batem_com_os_csvs(deck):
    """Nas linhas da 003 a decisão é texto do modelo (não há chave por linha): confere contra hipoteses.csv."""
    for m in LINHA_TESTE.finditer(deck):
        h, attrs, corpo = m.groups()
        cel = re.search(r'<td class="dec[^"]*">(.*?)</td>', corpo, re.S)
        assert cel, f"{h}: linha sem célula de decisão"
        texto = _visivel(cel.group(1)).strip()
        assert texto.startswith(("rejeita H0", "não rejeita H0")), f"{h}: decisão '{texto}'"
        df = pd.read_csv(RESULTADOS / f"00{h[1]}" / "tabelas" / "hipoteses.csv", sep=";", decimal=",",
                         encoding="utf-8-sig")
        sub = df[df.hipotese == h]
        base, exp = _attr(attrs, "base"), _attr(attrs, "exp")
        if base and "base" in sub.columns:
            sub = sub[sub.base.isin(base.split(","))]
        if exp and exp != "todas":
            sub = sub[sub.exposicao == exp]
        assert len(sub), f"{h}: nenhuma linha no CSV para base={base}, exposição={exp}"
        esperado = "não rejeita H0" if texto.startswith("não") else "rejeita H0"
        assert set(sub.decisao) == {esperado}, f"{h}: deck '{texto}', CSV {set(sub.decisao)}"


def test_gl_digitado_de_h42(deck):
    """gl de H4.2 é o único gl digitado (3 subgrupos − 1): confere contra o CSV."""
    h4 = pd.read_csv(RESULTADOS / "004" / "tabelas" / "hipoteses.csv", sep=";", decimal=",", encoding="utf-8-sig")
    linha = re.search(r'<tr data-h="H4\.2"[^>]*>(.*?)</tr>', deck, re.S).group(1)
    gls = re.findall(r'<td class="n">([^<]*)</td>', linha)
    assert gls[1].strip() == str(int(h4.set_index("hipotese").loc["H4.2", "gl"]))


def test_roteiro_tem_um_bloco_por_apresentador_e_os_slides():
    t = ROTEIRO_MODELO.read_text(encoding="utf-8")
    n_deck = len(SLIDE.findall(MODELO.read_text(encoding="utf-8")))
    for k in range(1, n_deck + 1):
        assert f"**Slide {k} —" in t, f"roteiro sem o slide {k}"
    assert f"**Slide {n_deck + 1} —" not in t, "roteiro com slide que o deck não tem"
