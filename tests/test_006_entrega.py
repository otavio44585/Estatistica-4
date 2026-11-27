"""Spec 006 — critérios de aceite da entrega: relatório sem marcador pendente, páginas autocontidas,
nenhuma frase causal, números do relatório vindos dos CSVs."""
import re

import pytest

from analise.comum import caminhos
from analise.relatorio.relatorio import MARCADOR, preenche

RAIZ = caminhos.RAIZ
PAGINAS = ["index", "001", "002", "003", "004", "005", "roteiro", "verificacao"]
CAUSAIS = [r"\bcausa(m|ram)?\b(?! insônia\?)", r"\bprovoca", r"\befeitos? d[aeo]s?\b", r"\bleva(m)? (a|ao|à)\b"]


def _texto(nome):
    p = RAIZ / "docs" / nome
    if not p.exists():
        pytest.skip(f"{nome} não gerado (rode analise.relatorio.relatorio)")
    return p.read_text(encoding="utf-8")


def test_preenche_falha_com_marcador_sem_valor():
    with pytest.raises(KeyError, match="nao_existe"):
        preenche("valor {{nao_existe}}", {})


def test_modelos_usam_so_chaves_existentes():
    from analise.relatorio.numeros import carrega
    from analise.relatorio.relatorio import apresentadores
    N = carrega() | {"data": "x"}
    apresentadores(N)
    for m in (RAIZ / "docs" / "modelos").glob("*.md"):
        faltam = set(MARCADOR.findall(m.read_text(encoding="utf-8"))) - set(N)
        assert not faltam, f"{m.name}: {faltam}"


@pytest.mark.parametrize("nome", ["relatorio.md", "roteiro_apresentacao.md"])
def test_documento_gerado_sem_marcador(nome):
    assert "{{" not in _texto(nome)


@pytest.mark.parametrize("nome", ["relatorio.md", "roteiro_apresentacao.md"])
def test_sem_linguagem_causal_afirmativa(nome):
    texto = _texto(nome).lower()
    # frases que NEGAM causalidade são permitidas ("não permitem dizer que a tela causa insônia")
    linhas = [l for l in texto.splitlines() if not re.search(r"não (permite|permitem|é|causa)|causa insônia\?|exigiria", l)]
    for padrao in CAUSAIS:
        achou = [l.strip()[:80] for l in linhas if re.search(padrao, l)]
        assert not achou, f"linguagem causal em {nome}: {achou}"


@pytest.mark.parametrize("slug", PAGINAS)
def test_paginas_autocontidas(slug):
    p = RAIZ / "site" / f"{slug}.html"
    if not p.exists():
        pytest.skip("site não gerado")
    h = p.read_text(encoding="utf-8")
    assert "<title>" in h and "{{" not in h
    srcs = re.findall(r'src="([^"]+)"', h)
    assert all(s.startswith("data:image/") for s in srcs), "imagem não embutida"
    assert not re.search(r'<link[^>]+stylesheet|<script[^>]+src=', h), "dependência externa"
    for alvo in re.findall(r'href="([^"#:]+\.html)"', h):
        assert (RAIZ / "site" / alvo).exists(), f"link quebrado {alvo}"


def test_referencias_do_relatorio_tem_doi():
    texto = _texto("relatorio.md")
    refs = texto.split("## Referências", 1)[1].strip().split("\n\n")
    assert refs and all("https://doi.org/" in r for r in refs)


def test_roteiro_sem_marcador_de_pessoa():
    """Sugestão da verificação: nada de "Pessoa 1–4"; o nome (ou o papel do bloco) vem de integrantes.csv."""
    assert not re.search(r"Pessoa [1-4]", _texto("roteiro_apresentacao.md"))
