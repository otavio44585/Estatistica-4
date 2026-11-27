"""T-006 — Gera as páginas HTML da entrega em site/ (autocontidas: CSS inline, figuras em data URI).

Fontes:
  docs/relatorio.md                 -> site/index.html        (gerado por analise.relatorio.relatorio)
  docs/explicacoes/00N_*.md         -> site/00N.html           (explicação da técnica)
  resultados/00N/RESUMO.md          -> site/00N.html           (resultados, depois da explicação)
  resultados/00N/tabelas/hipoteses* -> tabela renderizada do CSV, no topo dos resultados
  docs/roteiro_apresentacao.md      -> site/roteiro.html

Uso: python -m analise.relatorio.gerar_site
"""
import base64
import html
import re
from pathlib import Path

import markdown
import pandas as pd

from analise.comum import caminhos
from analise.comum.estatistica import formata_p

RAIZ = caminhos.RAIZ
SITE = RAIZ / "site"
REPO_URL = "https://github.com/otavio44585/Estatistica-4/blob/main/"

PAGINAS = [
    ("index", "Visão geral", None),
    ("001", "Dados", "001"),
    ("002", "PCA e análise fatorial", "002"),
    ("003", "Brasil × EUA", "003"),
    ("004", "Mundo", "004"),
    ("005", "Regressão, ANOVA e t", "005"),
    ("roteiro", "Roteiro", None),
    ("verificacao", "Verificação", None),
]

CSS = """
:root{--bg:#ffffff;--fg:#1d1f21;--muted:#5f6368;--line:#e3e5e8;--card:#f6f8f7;--accent:#00795a;--accent2:#0072B2;--warn:#8a5a00;--code:#f2f4f3}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121416;--fg:#e8eaed;--muted:#a0a6ad;--line:#2c3035;--card:#1b1e21;--accent:#3fc79b;--accent2:#6cb6ff;--warn:#e0b050;--code:#1f2326}}
:root[data-theme="dark"]{--bg:#121416;--fg:#e8eaed;--muted:#a0a6ad;--line:#2c3035;--card:#1b1e21;--accent:#3fc79b;--accent2:#6cb6ff;--warn:#e0b050;--code:#1f2326}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header{border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:2}
nav{max-width:1040px;margin:0 auto;padding:10px 16px;display:flex;gap:4px;flex-wrap:wrap;align-items:center}
nav .marca{font-weight:700;margin-right:12px;color:var(--accent)}
nav a{color:var(--muted);text-decoration:none;padding:4px 10px;border-radius:6px;font-size:14px}
nav a.ativo,nav a:hover{background:var(--card);color:var(--fg)}
main{max-width:1040px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:30px;line-height:1.2;margin:8px 0 16px}
h2{font-size:22px;margin-top:40px;padding-top:8px;border-top:1px solid var(--line)}
h3{font-size:18px;margin-top:28px}
a{color:var(--accent2)}
code{background:var(--code);padding:1px 5px;border-radius:4px;font-size:.9em}
pre{background:var(--code);padding:12px;border-radius:8px;overflow-x:auto}
pre code{padding:0;background:none}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px;display:block;overflow-x:auto}
th,td{border-bottom:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
th{background:var(--card);font-weight:600}
img{max-width:100%;height:auto;border:1px solid var(--line);border-radius:8px;background:#fff;margin:8px 0}
blockquote{margin:12px 0;padding:8px 16px;border-left:4px solid var(--accent);background:var(--card);border-radius:0 8px 8px 0}
.secao-rotulo{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-top:32px}
.rodape{color:var(--muted);font-size:13px;border-top:1px solid var(--line);margin-top:48px;padding-top:12px}
.tema{margin-left:auto;background:none;border:1px solid var(--line);color:var(--muted);border-radius:6px;padding:3px 8px;cursor:pointer}
@media print{header{position:static}.tema{display:none}h2{break-before:auto}img,table{break-inside:avoid}}
@media (max-width:600px){h1{font-size:24px}nav .marca{width:100%}}
"""

JS = """
(function(){var b=document.querySelector('.tema');if(!b)return;var r=document.documentElement;
try{var t=localStorage.getItem('tema');if(t)r.setAttribute('data-theme',t);}catch(e){}
b.addEventListener('click',function(){var e=r.getAttribute('data-theme');
var n=e==='dark'?'light':(e==='light'?'dark':(matchMedia('(prefers-color-scheme: dark)').matches?'light':'dark'));
r.setAttribute('data-theme',n);try{localStorage.setItem('tema',n);}catch(e){}});})();
"""


def _data_uri(caminho: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(caminho.read_bytes()).decode()


def _resolve(src: str, base_dir: Path) -> Path | None:
    for cand in (base_dir / src, RAIZ / src):
        if cand.is_file():
            return cand
    return None


def md_para_html(texto: str, base_dir: Path) -> tuple[str, set]:
    corpo = markdown.markdown(texto, extensions=["tables", "fenced_code", "sane_lists", "toc"])
    usadas = set()

    def troca_img(m):
        caminho = _resolve(html.unescape(m.group(1)), base_dir)
        if caminho is None:
            return m.group(0)
        usadas.add(caminho.resolve())
        return f'src="{_data_uri(caminho)}"'

    corpo = re.sub(r'src="([^"]+\.png)"', troca_img, corpo)

    def troca_link(m):
        alvo = html.unescape(m.group(1))
        if alvo.startswith(("http", "#", "mailto:")) or alvo.endswith(".html"):
            return m.group(0)
        if _resolve(alvo, base_dir) is not None or (RAIZ / alvo).exists():
            rel = (_resolve(alvo, base_dir) or (RAIZ / alvo)).resolve().relative_to(RAIZ.resolve()).as_posix()
            return f'href="{REPO_URL}{rel}"'
        return m.group(0)

    corpo = re.sub(r'href="([^"]+)"', troca_link, corpo)
    return corpo, usadas


# Tabelas mostradas no topo de cada página: (arquivo em resultados/<spec>/tabelas, colunas ou None, título)
TABELAS = {
    "001": [("prevalencias", None, "Exposição e desfechos nos inquéritos"),
            ("equivalencia", None, "Grau de equivalência de cada variável entre as bases")],
    "002": [("hipoteses", None, "Decisão das hipóteses H2.1–H2.6"),
            ("adequacao", ["conjunto", "n", "p", "alfa", "kmo", "bartlett_chi2", "bartlett_gl", "lambda1", "var_pc1",
                           "k_kaiser", "k_paralela", "k_decidido"], "Adequação e número de fatores por conjunto de itens"),
            ("tucker", ["hipotese", "instrumento", "base_a", "base_b", "solucao", "phi", "classificacao", "dif_max_carga"],
             "Congruência de Tucker entre países")],
    "003": [("hipoteses", ["familia", "hipotese", "base", "exposicao", "estimativa", "ic_inf", "ic_sup", "estatistica",
                           "tipo_estat", "gl2", "p", "p_holm", "decisao"], "Decisão das hipóteses H3.1–H3.9 (RP ajustada)")],
    "004": [("hipoteses", ["hipotese", "h0", "teste", "estatistica", "gl", "p", "p_holm", "decisao", "efeito"],
             "Decisão das hipóteses H4.1–H4.4"),
            ("efeitos_por_base", ["nome", "tipo", "n", "rho", "rho_ic_inf", "rho_ic_sup", "peso_aleatorio_pct"],
             "Correlação de Spearman por base (positivo = mais tela, pior sono)")],
    "005": [("hipoteses", ["hipotese", "familia", "base", "teste", "n", "versao_decisao", "b", "ic_inf", "ic_sup",
                           "estatistica", "gl2", "p", "p_holm", "decisao", "efeito_nome", "efeito"],
             "Decisão das hipóteses H5.1–H5.11")],
}
COLUNAS_P = {"p", "p_holm", "p_q", "p_rho", "p_efeito", "bartlett_p"}

ROTULOS = {
    "hipotese": "Hipótese", "familia": "Família", "base": "Base", "exposicao": "Exposição", "estimativa": "Estimativa",
    "ic_inf": "IC 95% inf.", "ic_sup": "IC 95% sup.", "estatistica": "Estatística", "tipo_estat": "Tipo",
    "gl": "gl", "gl2": "gl", "p": "p", "p_holm": "p (Holm)", "decisao": "Decisão", "efeito": "Tamanho de efeito",
    "efeito_nome": "Medida de efeito", "versao_decisao": "Versão que decide", "teste": "Teste", "n": "n",
    "b": "Coeficiente", "h0": "H0", "nome": "Base", "tipo": "Tipo de exposição", "rho": "ρ de Spearman",
    "rho_ic_inf": "IC 95% inf.", "rho_ic_sup": "IC 95% sup.", "peso_aleatorio_pct": "Peso na meta-análise (%)",
    "conjunto": "Conjunto de itens", "alfa": "α de Cronbach", "kmo": "KMO", "bartlett_chi2": "Bartlett χ²",
    "bartlett_gl": "gl", "lambda1": "1º autovalor", "var_pc1": "Variância do 1º componente",
    "k_kaiser": "Fatores (Kaiser)", "k_paralela": "Fatores (análise paralela)", "k_decidido": "Fatores retidos",
    "instrumento": "Instrumento", "base_a": "Base A", "base_b": "Base B", "solucao": "Solução", "phi": "Tucker φ",
    "classificacao": "Classificação", "dif_max_carga": "Maior diferença entre cargas", "criterio": "Critério",
    "valor": "Valor obtido", "variavel": "Variável", "categoria": "Categoria", "pct_sem_peso": "% sem peso",
    "pct_com_peso": "% com peso",
}
LEGENDAS = {
    ("002", "adequacao"): "KMO ≥ 0,60 e Bartlett significativo indicam que os itens têm correlação suficiente para análise fatorial. O número de fatores retidos segue a análise paralela de Horn.",
    ("002", "tucker"): "φ ≥ 0,95: estruturas equivalentes; 0,85–0,94: similares (Lorenzo-Seva e ten Berge, 2006). A maior diferença entre cargas complementa φ, que sai alto quando todas as cargas são positivas.",
    ("003", "hipoteses"): "Estimativa = razão de prevalências (RP), tela ≥ 3 h × < 1 h, ajustada por faixa etária, sexo e escolaridade. RP > 1: mais problema de sono no grupo de mais tela. Holm dentro de cada família.",
    ("004", "efeitos_por_base"): "ρ positivo = mais tela, pior sono. Peso = participação de cada base na estimativa combinada de efeitos aleatórios.",
    ("005", "hipoteses"): "Coeficiente = diferença no desfecho por categoria ou unidade de tela, com covariáveis fixas. Nos inquéritos decide a versão com peso amostral; nas bases de repositório não há desenho e vale a regressão do Excel.",
}


def tabela_csv(caminho: Path, colunas=None, max_linhas: int = 80) -> str:
    df = pd.read_csv(caminho, sep=";", decimal=",", encoding="utf-8-sig")
    if colunas:
        df = df[[c for c in colunas if c in df.columns]]
    if len(df) > max_linhas:
        df = df.head(max_linhas)
    fmt = df.copy()
    for c in fmt.columns:
        if c.lower() in COLUNAS_P and pd.api.types.is_numeric_dtype(fmt[c]):
            fmt[c] = fmt[c].map(lambda x: "" if pd.isna(x) else formata_p(float(x)))
        elif pd.api.types.is_float_dtype(fmt[c]):
            fmt[c] = fmt[c].map(lambda x: "" if pd.isna(x) else (f"{x:.3g}" if abs(x) < 1e-3 and x != 0 else f"{x:,.3f}".rstrip("0").rstrip(".")).replace(",", "X").replace(".", ",").replace("X", "."))
    fmt = fmt.rename(columns={c: ROTULOS.get(c, c) for c in fmt.columns})
    tab = fmt.to_html(index=False, border=0, escape=True, na_rep="")
    rel = caminho.resolve().relative_to(RAIZ.resolve()).as_posix()
    return f'{tab}<p class="secao-rotulo">Fonte: <a href="{REPO_URL}{rel}"><code>{rel}</code></a></p>'


def tabela_conferencia() -> str:
    f = RAIZ / "resultados" / "005" / "conferencia.csv"
    if not f.exists():
        return ""
    c = pd.read_csv(f, sep=";", decimal=",", encoding="utf-8-sig")
    ok = c.ok.astype(str).str.strip().str.lower()
    c["_exc"] = ok.eq("informativo")
    c["_dentro"] = ok.eq("true")
    g = c.groupby("base").agg(numeros=("item", "size"), dentro=("_dentro", "sum"), excecoes=("_exc", "sum"),
                              mx_a=("dif_rel_A_C", "max"), mx_b=("dif_rel_B_C", "max")).reset_index()
    for k in ["mx_a", "mx_b"]:
        g[k] = g[k].map(lambda x: "" if pd.isna(x) else f"{x:.1e}")
    g.columns = ["Base", "Números comparados", "Dentro da tolerância", "Exceções documentadas",
                 "Maior diferença Excel × script", "Maior diferença fórmula × script"]
    rel = f.resolve().relative_to(RAIZ.resolve()).as_posix()
    return ("<h2>Conferência dos p-valores e demais números: Excel × fórmula × script</h2>"
            + g.to_html(index=False, border=0) + f'<p class="secao-rotulo">Fonte: <a href="{REPO_URL}{rel}"><code>{rel}</code></a> '
            f"({len(c)} comparações; diferença relativa; tolerância 1e-8, exceto gl de Welch arredondado pelo Excel)</p>")


def pagina(slug: str, titulo: str, corpo: str) -> str:
    links = "".join(
        f'<a href="{s}.html"{" class=ativo" if s == slug else ""}>{html.escape(t)}</a>' for s, t, _ in PAGINAS)
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)} · Insônia digital</title><style>{CSS}</style></head>
<body><header><nav><span class="marca">Insônia digital</span>{links}<button class="tema" type="button" aria-label="Alternar tema">◐</button></nav></header>
<main>{corpo}
<div class="rodape">Estatística 4 · ESEG · Gerado por <code>analise/relatorio/gerar_site.py</code> a partir dos arquivos em <code>resultados/</code> e <code>docs/</code>. Associação observada em dados transversais não é causalidade.</div>
</main><script>{JS}</script></body></html>"""


def pagina_spec(spec: str, titulo: str) -> str:
    partes = [f"<h1>{spec} — {html.escape(titulo)}</h1>"]
    usadas = set()
    expl = sorted((RAIZ / "docs" / "explicacoes").glob(f"{spec}_*.md"))
    res = RAIZ / "resultados" / spec / "RESUMO.md"
    for nome, cols, tit in TABELAS.get(spec, []):
        f = RAIZ / "resultados" / spec / "tabelas" / f"{nome}.csv"
        if f.exists():
            partes.append(f'<h2>{html.escape(tit)}</h2>')
            if (spec, nome) in LEGENDAS:
                partes.append(f"<p>{html.escape(LEGENDAS[(spec, nome)])}</p>")
            partes.append(tabela_csv(f, cols))
    if spec == "005":
        partes.append(tabela_conferencia())
    for f in expl:
        partes.append('<p class="secao-rotulo">Explicação da técnica</p>')
        h, u = md_para_html(_sem_titulo(f.read_text(encoding="utf-8")), f.parent); partes.append(h); usadas |= u
    if res.exists():
        partes.append('<p class="secao-rotulo">Resultados</p>')
        h, u = md_para_html(_sem_titulo(res.read_text(encoding="utf-8")), res.parent); partes.append(h); usadas |= u
    figs = [f for f in sorted((RAIZ / "resultados" / spec / "figuras").glob("*.png")) if f.resolve() not in usadas]
    if figs:
        partes.append("<h2>Todas as figuras</h2>")
        for f in figs:
            rel = f.resolve().relative_to(RAIZ.resolve()).as_posix()
            partes.append(f'<figure><img alt="{html.escape(f.stem)}" src="{_data_uri(f)}"><figcaption class="secao-rotulo">{rel}</figcaption></figure>')
    return "\n".join(partes)


def _sem_titulo(texto: str) -> str:
    """Rebaixa o '# título' do markdown para não repetir o h1 da página."""
    return re.sub(r"^# (.+)$", r"## \1", texto, count=1, flags=re.M)


def main():
    SITE.mkdir(exist_ok=True)
    for slug, titulo, spec in PAGINAS:
        if slug == "index":
            f = RAIZ / "docs" / "relatorio.md"
            corpo, _ = md_para_html(f.read_text(encoding="utf-8"), f.parent) if f.exists() else ("<h1>Relatório pendente</h1>", None)
        elif slug in ("roteiro", "verificacao"):
            f = RAIZ / "docs" / ("roteiro_apresentacao.md" if slug == "roteiro" else "verificacao_independente.md")
            corpo, _ = md_para_html(f.read_text(encoding="utf-8"), f.parent) if f.exists() else (f"<h1>{titulo} pendente</h1>", None)
        else:
            corpo = pagina_spec(spec, titulo)
        (SITE / f"{slug}.html").write_text(pagina(slug, titulo, corpo), encoding="utf-8")
        print("site/", f"{slug}.html")


if __name__ == "__main__":
    main()
