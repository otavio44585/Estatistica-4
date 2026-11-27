"""Spec 006 — design system da ESEG nas páginas, entrada do GitHub Pages e README gerado do modelo."""
import base64
import re

import pytest

from analise.comum import caminhos

RAIZ = caminhos.RAIZ
PAGINAS = ["index", "001", "002", "003", "004", "005", "roteiro", "verificacao"]
PAGES_URL = "https://otavio44585.github.io/Estatistica-4/"
MARINHO = "#08223D"


def _logo_b64(nome="eseg-branco.svg"):
    f = RAIZ / "site" / "assets" / nome
    assert f.is_file(), f"logo ausente: site/assets/{nome}"
    return base64.b64encode(f.read_bytes()).decode()


def test_logos_da_eseg_em_assets():
    for nome in ("eseg-branco.svg", "eseg-marinho.svg"):
        f = RAIZ / "site" / "assets" / nome
        assert f.is_file() and f.read_text(encoding="utf-8").lstrip().startswith("<svg"), nome


def test_index_da_raiz_leva_ao_site():
    f = RAIZ / "index.html"
    assert f.exists(), "index.html da raiz ausente (rode analise.relatorio.gerar_site)"
    h = f.read_text(encoding="utf-8")
    assert re.search(r'<meta http-equiv="refresh" content="0; url=site/index\.html"', h), "sem meta refresh"
    assert 'href="site/index.html"' in h, "sem link visível para site/index.html"
    assert MARINHO.lower() in h.lower(), "sem o marinho da ESEG"


def test_nojekyll_existe():
    assert (RAIZ / ".nojekyll").exists()


@pytest.mark.parametrize("slug", PAGINAS)
def test_paginas_com_visual_eseg(slug):
    p = RAIZ / "site" / f"{slug}.html"
    if not p.exists():
        pytest.skip("site não gerado")
    h = p.read_text(encoding="utf-8")
    assert MARINHO.lower() in h.lower(), "sem o marinho #08223D"
    assert "#00A1B8".lower() in h.lower(), "sem o turquesa #00A1B8"
    assert f"data:image/svg+xml;base64,{_logo_b64()}" in h, "logo branco da ESEG não embutido"
    assert '"Public Sans"' in h, "sem a fonte da marca"
    assert 'href="apresentacao.html"' in h, "navegação sem a Apresentação"
    assert ':root[data-theme="dark"]' in h and "prefers-color-scheme:dark" in h, "tema escuro ausente"


def test_readme_gerado_do_modelo():
    assert (RAIZ / "docs" / "modelos" / "README.md").exists()
    r = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "{{" not in r, "README com marcador pendente (rode analise.relatorio.relatorio)"
    assert r.startswith("<!-- Arquivo GERADO"), "README não foi gerado do modelo"
    assert PAGES_URL in r
    assert "site/assets/eseg-marinho.svg" in r
