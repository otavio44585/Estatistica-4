"""T-006 — Gera as páginas HTML da entrega em site/ (autocontidas: CSS inline, figuras e logo em data URI).

Fontes:
  docs/relatorio.md                 -> site/index.html        (gerado por analise.relatorio.relatorio)
  docs/explicacoes/00N_*.md         -> site/00N.html           (explicação da técnica)
  resultados/00N/RESUMO.md          -> site/00N.html           (resultados, depois da explicação)
  resultados/00N/tabelas/hipoteses* -> tabela renderizada do CSV, no topo dos resultados
  resultados/006/figuras + tabelas  -> site/006.html          (figuras-síntese da apresentação, com legenda)
  docs/roteiro_apresentacao.md      -> site/roteiro.html
  docs/verificacao_independente.md  -> site/verificacao.html
  (sem fonte)                       -> index.html na raiz     (GitHub Pages: redireciona para site/index.html)

site/apresentacao.html (slides) só entra na navegação: quem gera é analise.relatorio.relatorio,
a partir de docs/modelos/apresentacao.html.

Visual: design system da Faculdade ESEG (Eseg/design-system): marinho #08223D, turquesa #00A1B8,
âmbar #F1B634 como destaque pontual, Public Sans 600/400 com fallback do sistema, cantos de 16 px.
Logo branco de site/assets/ (cópia de design-system/logos/, sem recolorir) embutido como data URI.

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
ASSETS = SITE / "assets"
LOGO_BRANCO = ASSETS / "eseg-branco.svg"   # sobre fundo marinho
REPO = "https://github.com/otavio44585/Estatistica-4"
REPO_URL = REPO + "/blob/main/"
PAGES_URL = "https://otavio44585.github.io/Estatistica-4/"

# (slug, título, spec ou None, descrição do cartão na visão geral). Estas são geradas aqui.
PAGINAS = [
    ("index", "Visão geral", None, ""),
    ("001", "Dados", "001", "Seis bases abertas harmonizadas: tela, sono e covariáveis na mesma escala."),
    ("002", "PCA e análise fatorial", "002", "O índice de insônia do Vigitel mede uma coisa só? Quantas dimensões tem cada escala?"),
    ("003", "Brasil: PNS × Vigitel", "003", "Razões de prevalência ajustadas nas duas pesquisas nacionais e a comparação entre elas."),
    ("004", "Mundo", "004", "Meta-análise das seis bases, Brasil × resto do mundo e posição frente à literatura."),
    ("005", "Regressão, ANOVA e t", "005", "Formato da disciplina, com os p-valores conferidos no Excel e no script."),
    ("006", "Figuras-síntese", "006", "Teste desenhado, quanto a tela explica, confundimento por idade e o Brasil no mundo."),
    ("roteiro", "Roteiro", None, "Quem fala o quê, bloco a bloco, e que tela mostrar."),
    ("verificacao", "Verificação", None, "O que a revisão independente refez, apontou e como foi resolvido."),
]
# Só na navegação: gerada por analise.relatorio.relatorio (docs/modelos/apresentacao.html).
EXTERNAS = {"apresentacao": ("Apresentação", "Slides da apresentação oral, com os números lidos de resultados/.")}
NAV = ["index", "001", "002", "003", "004", "005", "006", "apresentacao", "roteiro", "verificacao"]

# Tokens do design system da ESEG. --link no tema claro mistura turquesa (65%) e marinho (35%):
# o turquesa puro sobre branco tem contraste 3,1:1, abaixo do 4,5:1 do WCAG AA para texto; o
# sublinhado e os detalhes continuam no turquesa da marca. No tema escuro o link usa o turquesa claro.
CSS = """
:root{color-scheme:light;--marinho:#08223D;--turquesa:#00A1B8;--ambar:#F1B634;
--bg:#FFFFFF;--fg:#1F2230;--muted:#474A56;--titulo:#08223D;--line:#E5E6E7;--card:#FAFAFA;--zebra:rgba(8,34,61,.04);
--link:#03758D;--link-sub:#00A1B8;--code:#F1F2F3;--img-borda:#E5E6E7;
--raio:16px;--fonte:"Public Sans",system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#0F1322;--fg:#E5E6E7;--muted:#C2C3C7;--titulo:#FFFFFF;--line:#333643;--card:#1F2230;--zebra:rgba(255,255,255,.04);--link:#00AFC4;--link-sub:#00A1B8;--code:#1F2230;--img-borda:#333643}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#0F1322;--fg:#E5E6E7;--muted:#C2C3C7;--titulo:#FFFFFF;--line:#333643;--card:#1F2230;--zebra:rgba(255,255,255,.04);--link:#00AFC4;--link-sub:#00A1B8;--code:#1F2230;--img-borda:#333643}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:400 16px/1.5 var(--fonte);overflow-wrap:break-word}
.pular{position:absolute;left:-9999px;top:0}
.pular:focus{left:16px;top:8px;z-index:9;background:var(--ambar);color:var(--marinho);padding:6px 14px;border-radius:100px}
.topo{background:var(--marinho);color:#FFFFFF}
.topo .barra{max-width:1120px;margin:0 auto;padding:14px 16px;display:flex;align-items:center;gap:16px}
.marca{display:flex;align-items:center;gap:14px;color:#FFFFFF;text-decoration:none;min-width:0}
.marca img{height:40px;width:auto;flex:none;border:0;padding:0;margin:0;background:none;border-radius:0}
.marca span{display:flex;flex-direction:column;line-height:1.2;padding-left:14px;border-left:1px solid rgba(255,255,255,.25);min-width:0}
.marca strong{font-weight:600;font-size:18px}
.marca small{font-size:13px;color:#C2C3C7}
.tema{margin-left:auto;flex:none;background:none;border:1px solid rgba(255,255,255,.4);color:#FFFFFF;border-radius:100px;padding:6px 14px;font:600 13px var(--fonte);cursor:pointer}
.tema:hover,.tema:focus-visible{border-color:var(--turquesa)}
.menu{position:sticky;top:0;z-index:5;background:var(--marinho);border-bottom:3px solid var(--turquesa)}
.menu .links{position:relative;max-width:1120px;margin:0 auto;padding:0 8px;display:flex;gap:2px;overflow-x:auto;scrollbar-width:thin;white-space:nowrap}
@media (hover:none){.menu .links{scrollbar-width:none}.menu .links::-webkit-scrollbar{display:none}}
.menu a{color:#E5E6E7;text-decoration:none;padding:10px 10px 8px;font-size:14px;border-bottom:3px solid transparent}
.menu a:hover{color:#FFFFFF;background:rgba(255,255,255,.08)}
.menu a.ativo{color:#FFFFFF;font-weight:600;border-bottom-color:var(--ambar)}
main{max-width:1120px;margin:0 auto;padding:28px 16px 48px}
h1,h2,h3,h4{font-weight:600;line-height:1.2;color:var(--titulo)}
h1{font-size:32px;margin:4px 0 16px}
h2{font-size:24px;margin:44px 0 12px}
h2::before{content:"";display:block;width:40px;height:4px;border-radius:4px;background:var(--turquesa);margin-bottom:12px}
h3{font-size:20px;margin:28px 0 8px}
p,li{max-width:80ch}
a{color:var(--link);text-decoration-color:var(--link-sub);text-decoration-thickness:2px;text-underline-offset:3px}
a:hover{color:var(--link-sub)}
strong{font-weight:600}
code{background:var(--code);padding:1px 6px;border-radius:6px;font-size:.88em;font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace}
pre{background:var(--code);padding:14px 16px;border-radius:var(--raio);overflow-x:auto;max-width:100%;border:1px solid var(--line)}
pre code{padding:0;background:none}
.tabela{overflow-x:auto;margin:14px 0;border:1px solid var(--line);border-radius:var(--raio);background:var(--bg)}
table{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
th,td{padding:8px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);overflow-wrap:normal}
thead th{background:var(--marinho);color:#FFFFFF;font-weight:600;border-bottom:0;white-space:nowrap}
tbody tr:nth-child(even){background:var(--zebra)}
tbody tr:last-child td{border-bottom:0}
td.longo{min-width:24ch}
img{max-width:100%;height:auto;border:1px solid var(--img-borda);border-radius:12px;background:#FFFFFF;padding:6px;margin:8px 0}
figure{margin:16px 0}
blockquote{margin:16px 0;padding:10px 18px;border:1px solid var(--line);border-left:4px solid var(--turquesa);background:var(--card);border-radius:var(--raio)}
blockquote p{margin:6px 0}
hr{border:0;border-top:1px solid var(--line);margin:32px 0}
.kicker,.secao-rotulo{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.kicker{margin:0;color:var(--link)}
.secao-rotulo{margin-top:32px}
.hero{background:var(--card);border:1px solid var(--line);border-radius:var(--raio);padding:24px;margin:0 0 20px}
.hero h1{margin-top:0}
.hero p{margin-bottom:0;color:var(--muted)}
.cartoes{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin:0 0 8px}
.cartao{display:block;padding:16px 18px;border:1px solid var(--line);border-radius:var(--raio);background:var(--bg);color:var(--fg);text-decoration:none}
.cartao:hover{border-color:var(--turquesa);color:var(--fg)}
.cartao strong{display:block;color:var(--titulo);margin-bottom:4px}
.cartao span{font-size:14px;color:var(--muted)}
.rodape{border-top:1px solid var(--line);color:var(--muted);font-size:13px}
.rodape div{max-width:1120px;margin:0 auto;padding:16px 16px 32px}
@media (max-width:700px){h1{font-size:26px}h2{font-size:21px}.marca img{height:32px}.marca small{display:none}.hero{padding:18px}main{padding-top:20px}}
@media print{.menu,.tema,.pular{display:none}.topo,thead th{-webkit-print-color-adjust:exact;print-color-adjust:exact}img,table,.cartao{break-inside:avoid}}
"""

# Aplica o tema salvo antes de pintar a página (sem piscar).
JS_CABECA = "try{var t=localStorage.getItem('tema');if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}"

JS = """
(function(){var l=document.querySelector('.menu .links'),a=l&&l.querySelector('.ativo');
if(a&&l.scrollWidth>l.clientWidth)l.scrollLeft=a.offsetLeft-(l.clientWidth-a.offsetWidth)/2;})();
(function(){var b=document.querySelector('.tema');if(!b)return;var r=document.documentElement;
b.addEventListener('click',function(){var e=r.getAttribute('data-theme');
var n=e==='dark'?'light':(e==='light'?'dark':(matchMedia('(prefers-color-scheme: dark)').matches?'light':'dark'));
r.setAttribute('data-theme',n);try{localStorage.setItem('tema',n);}catch(e){}});})();
"""


def logo_uri(f: Path = LOGO_BRANCO) -> str:
    """Logo da ESEG como data URI (a página não depende de arquivo ao lado)."""
    return "data:image/svg+xml;base64," + base64.b64encode(f.read_bytes()).decode()


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
            ("vigitel_indice", ["variavel_vigitel", "rotulo", "media", "dp", "carga_pc1", "carga_af1_ml",
                                "comunalidade_af1", "msa", "alfa_sem_item", "r_item_total"],
             "Índice de insônia do Vigitel 2024, pergunta a pergunta")],
    "003": [("hipoteses", ["familia", "hipotese", "base", "exposicao", "estimativa", "ic_inf", "ic_sup", "estatistica",
                           "tipo_estat", "gl2", "p", "p_holm", "decisao"],
             "Decisão das hipóteses H3.1–H3.9 (RP ajustada; H3.3 e H3.6 retiradas com os EUA)"),
            ("rp_bruta_ajustada", ["base", "exposicao", "modelo", "comparacao", "rp", "ic_inf", "ic_sup", "p", "n"],
             "Razão de prevalências bruta, só idade e ajustada")],
    "004": [("hipoteses", ["hipotese", "h0", "teste", "estatistica", "gl", "p", "p_holm", "decisao", "efeito"],
             "Decisão das hipóteses H4.1–H4.4"),
            ("efeitos_por_base", ["nome", "tipo", "n", "rho", "rho_ic_inf", "rho_ic_sup", "peso_aleatorio_pct"],
             "Correlação de Spearman por base (positivo = mais tela, pior sono)"),
            ("meta_analise", ["analise", "papel", "k", "rho", "rho_ic_inf", "rho_ic_sup", "p_efeito", "rho_ic_inf_hk",
                              "rho_ic_sup_hk", "p_efeito_hk", "I2"],
             "Meta-análise: global, subgrupos, Brasil e resto do mundo")],
    "005": [("hipoteses", ["hipotese", "familia", "base", "teste", "n", "versao_decisao", "b", "ic_inf", "ic_sup",
                           "estatistica", "gl2", "p", "p_holm", "decisao", "efeito_nome", "efeito"],
             "Decisão das hipóteses H5.1–H5.9 (H5.2, H5.8, H5.10 e H5.11 retiradas com os EUA)")],
}

# Página 006: figuras-síntese da apresentação (analise.relatorio.figuras_apresentacao), cada uma com legenda e,
# quando houver, a tabela de onde saem os números. (figura, título, legenda, tabela em resultados/006/tabelas ou None)
FIGURAS_006 = [
    ("teste_explicado", "Um teste de hipótese desenhado (H3.1, Vigitel 2024)",
     "A curva é a distribuição da estatística z se H0 (RP = 1) fosse verdadeira. As áreas em âmbar somam α = 0,05, "
     "2,5% em cada cauda, além de ±1,96. A seta marca o z observado: quando ele cai numa das caudas, rejeita-se H0.",
     None),
    ("testes_painel", "A mesma leitura para cada teste t ou z confirmatório",
     "Specs 003 e 005, na versão que decide. O título de cada painel traz a decisão e o p corrigido por Holm.",
     "testes_apresentacao"),
    ("decomposicao_r2", "Quanto a tela explica do sono",
     "Queda do R² da regressão linear ponderada quando cada fator sai do modelo: a parte da variação do sono que só "
     "aquele fator explica. Vigitel: índice de insônia (0–12); PNS: problema de sono (0–3).",
     "decomposicao_r2"),
    ("confundimento_idade", "Confundimento por idade na PNS 2019",
     "Por faixa etária, com peso amostral: % dos adultos com tela digital 3 h ou mais por dia e % com problema de sono "
     "em mais da metade dos dias. As curvas andam em sentidos opostos, e é isso que inverte a RP bruta.",
     "confundimento_idade_pns"),
    ("brasil_no_mundo", "O Brasil no mundo",
     "Correlação de Spearman (IC 95%) por base, o Brasil combinado (PNS + Vigitel) e o resto do mundo combinado "
     "(Argentina, Japão, China, Turquia), por meta-análise de efeitos aleatórios. Comparação exploratória, pedida "
     "depois de ver os resultados e fora da correção de Holm.",
     None),
]
COLUNAS_006 = {"decomposicao_r2": ["base", "desfecho", "n", "rotulo", "r2_completo", "r2_unico_pct", "r2_sozinho_pct"]}
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
    "variavel_vigitel": "Variável", "rotulo": "Pergunta / fator", "media": "Média", "dp": "DP",
    "carga_pc1": "Carga na PCA", "carga_af1_ml": "Carga na AF", "comunalidade_af1": "Comunalidade", "msa": "MSA",
    "alfa_sem_item": "α sem o item", "r_item_total": "r item-total", "modelo": "Modelo", "comparacao": "Comparação",
    "rp": "RP", "analise": "Combinação", "papel": "Papel", "k": "k", "p_efeito": "p (DL)",
    "rho_ic_inf_hk": "IC 95% inf. (HK)", "rho_ic_sup_hk": "IC 95% sup. (HK)", "p_efeito_hk": "p (HK)", "I2": "I²",
    "spec": "Spec", "desfecho": "Desfecho", "r2_completo": "R² do modelo completo",
    "r2_unico_pct": "% explicado só pelo fator", "r2_sozinho_pct": "% explicado pelo fator sozinho",
    "faixa_etaria": "Faixa etária", "pct_tela_3h": "% com tela ≥ 3 h", "pct_problema_sono": "% com problema de sono",
}
LEGENDAS = {
    ("002", "adequacao"): "KMO ≥ 0,60 e Bartlett significativo indicam que os itens têm correlação suficiente para análise fatorial. O número de fatores retidos segue a análise paralela de Horn.",
    ("002", "vigitel_indice"): "As três perguntas de insônia do Vigitel, recodificadas de 0 (nunca) a 4 (sempre). Cargas altas nas duas técnicas e α que cairia sem qualquer item: a soma 0–12 resume uma dimensão só.",
    ("003", "hipoteses"): "Estimativa = razão de prevalências (RP), tela ≥ 3 h × < 1 h, ajustada por faixa etária, sexo e escolaridade. RP > 1: mais problema de sono no grupo de mais tela. H0: RP = 1 (ou razão = 1 em H3.8 e H3.9), α = 0,05 bilateral, Holm dentro de cada família.",
    ("003", "rp_bruta_ajustada"): "Na PNS, a RP bruta da tela digital fica abaixo de 1 e passa a acima de 1 com o ajuste por idade: quem usa mais tela é mais jovem, e os jovens relatam menos problema de sono.",
    ("004", "efeitos_por_base"): "ρ positivo = mais tela, pior sono. Peso = participação de cada base na estimativa combinada de efeitos aleatórios.",
    ("004", "meta_analise"): "IC por DerSimonian-Laird (DL, normal) e por Hartung-Knapp (HK, t com k − 1 gl, mais honesto com poucas bases). A linha do resto do mundo é exploratória, decidida depois de ver os resultados.",
    ("005", "hipoteses"): "Coeficiente = diferença no desfecho por categoria ou unidade de tela, com covariáveis fixas. H0: coeficiente = 0 (ou médias iguais), α = 0,05 bilateral. No Vigitel decide a versão com peso amostral; nas bases de repositório não há desenho e vale a regressão do Excel.",
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
    # Só apresentação: célula curta ("< 0,001", "rejeita H0") não quebra linha; texto longo quebra.
    fmt = fmt.map(lambda s: s.replace(" ", " ") if isinstance(s, str) and len(s) <= 18 else s)
    fmt = fmt.rename(columns={c: ROTULOS.get(c, c) for c in fmt.columns})
    tab = fmt.to_html(index=False, border=0, escape=True, na_rep="")
    rel = caminho.resolve().relative_to(RAIZ.resolve()).as_posix()
    return f'{tab}<p class="secao-rotulo">Fonte: <a href="{REPO_URL}{rel}"><code>{rel}</code></a></p>'


def tabela_conferencia() -> str:
    f = RAIZ / "resultados" / "005" / "conferencia.csv"
    if not f.exists():
        return ""
    c = pd.read_csv(f, sep=";", decimal=",", encoding="utf-8-sig")
    c["_exc"] = c.excecao_documentada.astype(str).str.strip().str.lower().eq("true")
    c["_dentro"] = c.dentro_tolerancia.astype(str).str.strip().str.lower().eq("true") & ~c["_exc"]
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


def _titulos() -> dict:
    return {s: t for s, t, _, _ in PAGINAS} | {s: t for s, (t, _) in EXTERNAS.items()}


def _descricoes() -> dict:
    return {s: d for s, _, _, d in PAGINAS} | {s: d for s, (_, d) in EXTERNAS.items()}


def _envolve_tabelas(corpo: str) -> str:
    """Cada tabela num contêiner com rolagem própria: no celular a tabela rola, a página não.
    Célula de texto longo ganha largura mínima, para não virar uma coluna estreita de muitas linhas."""
    corpo = re.sub(r"<td>(?=[^<]{40,}</td>)", '<td class="longo">', corpo)
    return re.sub(r"</table>", "</table></div>", re.sub(r"<table\b", '<div class="tabela"><table', corpo))


def pagina(slug: str, titulo: str, corpo: str) -> str:
    nomes = _titulos()
    links = "".join(
        f'<a href="{s}.html"' + (' class="ativo" aria-current="page"' if s == slug else "") + f">{html.escape(nomes[s])}</a>"
        for s in NAV)
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#08223D"><meta name="description" content="Insônia digital: uso de telas e sono no Brasil (PNS 2019 e Vigitel 2024) e em outros quatro países. Estatística 4, Faculdade ESEG.">
<title>{html.escape(titulo)} · Insônia digital</title><script>{JS_CABECA}</script><style>{CSS}</style></head>
<body><a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="topo"><div class="barra"><a class="marca" href="index.html"><img src="{logo_uri()}" alt="Faculdade ESEG" width="56" height="40"><span><strong>Insônia digital</strong><small>Estatística 4 · Faculdade ESEG</small></span></a><button class="tema" type="button" aria-label="Alternar tema claro ou escuro">◐ Tema</button></div></header>
<nav class="menu" aria-label="Páginas do trabalho"><div class="links">{links}</div></nav>
<main id="conteudo">{_envolve_tabelas(corpo)}</main>
<footer class="rodape"><div>Estatística 4 · Faculdade ESEG · Gerado por <code>analise/relatorio/gerar_site.py</code> a partir dos arquivos em <code>resultados/</code> e <code>docs/</code>. Associação observada em dados transversais não é causalidade. <a href="{REPO}">Código no GitHub</a>.</div></footer>
<script>{JS}</script></body></html>"""


def capa_index(corpo: str) -> str:
    """Visão geral: título e linha de abertura do relatório num cartão, seguidos dos cartões das páginas."""
    m = re.search(r"(<h1[^>]*>.*?</h1>)\s*(<p>.*?</p>)?", corpo, flags=re.S)
    desc = _descricoes()
    nomes = _titulos()
    cartoes = "".join(
        f'<a class="cartao" href="{s}.html"><strong>{html.escape(nomes[s])}</strong><span>{html.escape(desc[s])}</span></a>'
        for s in NAV if s != "index")
    grade = f'<nav class="cartoes" aria-label="Páginas">{cartoes}</nav>'
    if not m:
        return grade + corpo
    hero = f'<section class="hero"><p class="kicker">Estatística 4 · Faculdade ESEG</p>{m.group(1)}{m.group(2) or ""}</section>'
    return corpo[:m.start()] + hero + grade + corpo[m.end():]


def pagina_raiz() -> str:
    """index.html da raiz do repositório (GitHub Pages servido da main, pasta /): leva a site/index.html."""
    nomes = _titulos()
    extras = " · ".join(f'<a href="site/{s}.html">{html.escape(nomes[s])}</a>' for s in ("apresentacao", "roteiro", "verificacao"))
    return f"""<!doctype html>
<!-- GERADO por analise/relatorio/gerar_site.py. Edite o script, não este arquivo. -->
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="0; url=site/index.html"><meta name="theme-color" content="#08223D">
<title>Insônia digital · Estatística 4 · ESEG</title>
<style>
:root{{color-scheme:dark;--marinho:#08223D;--turquesa:#00A1B8;--fonte:"Public Sans",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--marinho);color:#FFFFFF;font:400 16px/1.5 var(--fonte);padding:24px 16px}}
.caixa{{max-width:560px;width:100%;border:1px solid rgba(255,255,255,.18);border-top:4px solid var(--turquesa);border-radius:16px;padding:28px 24px;background:rgba(255,255,255,.03)}}
img{{height:56px;width:auto;display:block;margin-bottom:20px}}
h1{{font-weight:600;font-size:30px;line-height:1.2;margin:0 0 8px}}
p{{margin:8px 0;color:#E5E6E7}}
a{{color:#00AFC4;text-decoration-thickness:2px;text-underline-offset:3px}}
.botao{{display:inline-block;margin:16px 0 8px;background:var(--turquesa);color:var(--marinho);font-weight:600;text-decoration:none;padding:10px 22px;border-radius:100px}}
.botao:hover{{background:#00AFC4}}
small{{color:#C2C3C7}}
</style></head>
<body><main class="caixa">
<img src="{logo_uri()}" alt="Faculdade ESEG" width="78" height="56">
<h1>Insônia digital</h1>
<p>Uso de telas e sono no Brasil (PNS 2019 e Vigitel 2024), comparado com outros quatro países e com a literatura. Trabalho de Estatística 4.</p>
<p>Abrindo a visão geral… Se a página não mudar sozinha, use o botão.</p>
<a class="botao" href="site/index.html">Abrir o site</a>
<p>{extras}</p>
<p><small>Código, dados derivados e testes: <a href="{REPO}">{REPO.removeprefix("https://")}</a></small></p>
</main></body></html>
"""


def pagina_spec(spec: str, titulo: str) -> str:
    partes = [f'<p class="kicker">Etapa {spec}</p><h1>{html.escape(titulo)}</h1>']
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


def pagina_006(titulo: str) -> str:
    """Figuras-síntese da apresentação: cada figura com título, legenda e a tabela de onde saem os números."""
    pasta = RAIZ / "resultados" / "006"
    partes = [f'<p class="kicker">Etapa 006</p><h1>{html.escape(titulo)}</h1>',
              "<p>Figuras feitas para a apresentação a partir dos dados processados e das tabelas das specs 003 a 005 "
              "(<code>python -m analise.relatorio.figuras_apresentacao</code>). Os números aparecem na figura e na tabela "
              "logo abaixo; nenhum foi digitado à mão.</p>"]
    for nome, tit, legenda, tabela in FIGURAS_006:
        f = pasta / "figuras" / f"{nome}.png"
        if not f.exists():
            continue
        rel = f.resolve().relative_to(RAIZ.resolve()).as_posix()
        partes.append(f"<h2>{html.escape(tit)}</h2><p>{html.escape(legenda)}</p>")
        partes.append(f'<figure><img alt="{html.escape(tit)}" src="{_data_uri(f)}">'
                      f'<figcaption class="secao-rotulo">{rel}</figcaption></figure>')
        t = pasta / "tabelas" / f"{tabela}.csv" if tabela else None
        if t is not None and t.exists():
            partes.append(tabela_csv(t, COLUNAS_006.get(tabela)))
    return "\n".join(partes)


def _sem_titulo(texto: str) -> str:
    """Rebaixa o '# título' do markdown para não repetir o h1 da página."""
    return re.sub(r"^# (.+)$", r"## \1", texto, count=1, flags=re.M)


def main():
    SITE.mkdir(exist_ok=True)
    if not LOGO_BRANCO.is_file():
        raise FileNotFoundError(f"{LOGO_BRANCO} (copie de Eseg/design-system/logos/)")
    for slug, titulo, spec, _ in PAGINAS:
        if slug == "index":
            f = RAIZ / "docs" / "relatorio.md"
            corpo, _ = md_para_html(f.read_text(encoding="utf-8"), f.parent) if f.exists() else ("<h1>Relatório pendente</h1>", None)
            corpo = capa_index(corpo)
        elif slug in ("roteiro", "verificacao"):
            f = RAIZ / "docs" / ("roteiro_apresentacao.md" if slug == "roteiro" else "verificacao_independente.md")
            corpo, _ = md_para_html(f.read_text(encoding="utf-8"), f.parent) if f.exists() else (f"<h1>{titulo} pendente</h1>", None)
        elif slug == "006":
            corpo = pagina_006(titulo)
        else:
            corpo = pagina_spec(spec, titulo)
        (SITE / f"{slug}.html").write_text(pagina(slug, titulo, corpo), encoding="utf-8")
        print(f"site/{slug}.html")
    (RAIZ / "index.html").write_text(pagina_raiz(), encoding="utf-8")
    (RAIZ / ".nojekyll").touch()   # GitHub Pages sem Jekyll: serve os arquivos como estão
    print("index.html, .nojekyll")
    if not (SITE / "apresentacao.html").exists():
        print("aviso: site/apresentacao.html ainda não existe (gere com python -m analise.relatorio.relatorio)")


if __name__ == "__main__":
    main()
