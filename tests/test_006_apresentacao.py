"""Spec 006 — deck da apresentação (site/apresentacao.html, gerado de docs/modelos/apresentacao.html).

Critérios: arquivo gerado sem marcador pendente; autocontido (imagens em data URI, sem CSS/JS/fonte externos);
15 a 20 slides de 1280×720 com regra de impressão; nota do apresentador em todo slide; nenhuma frase causal
afirmativa (mesma lógica de test_006_entrega.py); sem "Pessoa 1–4"; ressalvas e conferência obrigatórias no modelo.
"""
import html
import re

import pytest

from analise.comum import caminhos
from analise.relatorio.relatorio import MARCADOR

RAIZ = caminhos.RAIZ
DECK = RAIZ / "site" / "apresentacao.html"
MODELO = RAIZ / "docs" / "modelos" / "apresentacao.html"
CAUSAIS = [r"\bcausa(m|ram)?\b(?! insônia\?)", r"\bprovoca", r"\befeitos? d[aeo]s?\b", r"\bleva(m)? (a|ao|à)\b"]
NEGA_CAUSA = r"não (permite|permitem|é|causa)|causa insônia\?|exigiria"
SLIDE = re.compile(r'<div class="slide[\s"]')


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


def test_deck_gerado_sem_marcador(deck):
    assert "<title>" in deck
    assert "{{" not in deck


def test_modelo_usa_so_chaves_existentes(modelo):
    from analise.relatorio.numeros import carrega
    from analise.relatorio.relatorio import apresentadores
    N = carrega() | {"data": "x"}
    apresentadores(N)
    faltam = set(MARCADOR.findall(modelo)) - set(N)
    assert not faltam, f"apresentacao.html: {faltam}"


def test_imagens_embutidas(deck):
    srcs = re.findall(r'\ssrc="([^"]*)"', deck)
    assert srcs, "deck sem imagem"
    fora = [s[:60] for s in srcs if not s.startswith("data:image/")]
    assert not fora, f"imagem não embutida: {fora}"


def test_sem_dependencia_externa(deck):
    assert not re.search(r"<link[^>]+stylesheet|<script[^>]+src=", deck, re.I), "CSS/JS externo"
    assert not re.search(r"@import|fonts\.googleapis|fonts\.gstatic", deck, re.I), "fonte ou CSS importado"
    assert not re.search(r'(src|href)="(https?:)?//', deck, re.I), "recurso remoto"
    assert not re.search(r"url\((?!\s*['\"]?(data:|#))", deck), "url() que não é data URI nem âncora"


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


def test_sem_linguagem_causal_afirmativa(deck):
    linhas = [l for l in _visivel(deck).lower().splitlines() if not re.search(NEGA_CAUSA, l)]
    for padrao in CAUSAIS:
        achou = [l.strip()[:80] for l in linhas if re.search(padrao, l)]
        assert not achou, f"linguagem causal no deck: {achou}"


def test_sem_marcador_de_pessoa(deck):
    assert not re.search(r"Pessoa [1-4]", deck)


@pytest.mark.parametrize("chave", ["h33_pholm_svyglm", "conf_n", "conf_dentro", "conf_excecoes", "data", "n_total"])
def test_conteudo_obrigatorio_no_modelo(modelo, chave):
    """Ressalva de H3.3, conferência Excel × fórmula × script, capa com data: vêm de marcadores, não de texto fixo."""
    assert "{{%s}}" % chave in modelo
