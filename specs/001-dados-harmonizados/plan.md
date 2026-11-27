# 001 — Plano: dados harmonizados

Status: executado (2026-11-27).

## Ambiente

- Python 3.11; pandas, numpy, pyreadstat (`.xpt`, `.sav`, `.dta`), openpyxl, pyarrow (parquet). Todos já instalados na máquina de referência; versões fixadas em `requirements.txt` na T001.
- Caminho dos brutos pela variável de ambiente `STAT4_BRUTOS` (ex.: `.../Stat4/pesquisa/dados`). Nenhum caminho pessoal no código.

## Estrutura

```text
analise/
  comum/
    caminhos.py        lê STAT4_BRUTOS e falha com mensagem clara se não existir
    faltantes.py       tabela de códigos especiais por base e função que troca por NaN
    validacao.py       asserts de n, de faixa de valores e de ausência de código especial
  harmonizacao/
    pns2019.py  vigitel2024.py  nhanes0506.py
    repositorios.py   (Xuzhou, Argentina, Turquia e Japão num só arquivo)
    recodes.py        tabelas de recodificação (testadas)
    dicionario.py     dicionário harmonizado, equivalência, descritiva
  dados/
    dicionario_harmonizado.csv     contrato da spec, uma linha por (base, variável)
    processados/<base>.parquet     saída de cada script
    logs/<base>.log                n antes/depois de cada filtro
tests/
  test_faltantes.py  test_contagens.py
resultados/001/
  equivalencia.csv               tabela de equivalência publicada
```

## Leitura por base

| Base | Arquivo bruto | Como ler | Cuidados |
|---|---|---|---|
| PNS 2019 | `pns_2019/extraido/.../PNS_2019.txt` (455 MB, largura fixa) | `read_fwf` só com as colunas usadas; posições tiradas de `input_PNS_2019.txt` | filtrar `M001 == 1`; 9 = ignorado; categoria 6 de `P0450x` = não usa |
| Vigitel 2024 | `vigitel-2006-2024-peso-rake-csv.zip` (578 MB descompactado) | ler direto do zip em blocos, `usecols`, filtrar `ano == 2024` | `q59c` é pulada quando `q59b == 2`; 777/888 = não resposta |
| NHANES 2005-06 | `SLQ_D.xpt`, `PAQ_D.xpt`, `DEMO_D.xpt`, `DPQ_D.xpt` | `pyreadstat.read_xport`, junção por `SEQN` | 7/9/77/99 = recusa/não sabe; `PAD600` 6 = nenhuma; peso `WTINT2YR`; estrato `SDMVSTRA`, UPA `SDMVPSU` (confirmar na T006) |
| Xuzhou | `pone.0340852.s001.xlsx` | `read_excel` | componentes do PSQI, não minutos; `time` e `aoye` sem rótulo |
| Argentina | `repositorio.xlsx` | `read_excel`; filtro `excluFINAL == 0` | 999 = faltante na latência; itens PDSS em texto ("2 A veces…"), extrair o dígito |
| Turquia | `Doomscrolling.csv` | `read_csv(sep=None)` | brancos = faltante; `DB11` constante; `S2`–`S24` sem rótulo |
| Japão | `BPS_study.csv` | `read_csv` | itens AIS 1–4; itens BPS com versão invertida (`R`); sono = 0 em 9 casos |

O código de leitura de PNS, Vigitel e NHANES já existe em `docs/exploratorio_comparativo_br_eua_2026-11-27.py` e é o ponto de partida.

## Recodificações de exposição

| Base | Variável original | 0 (não usa / < 1 h) | 1 (1 a < 3 h) | 2 (≥ 3 h) |
|---|---|---|---|---|
| PNS 2019 | `P04502` | 6, 1 | 2, 3 | 4, 5 |
| Vigitel 2024 | `q59b`/`q59c` | `q59b` = 2, ou `q59c` = 1 | 2, 3 | 4–7 |
| NHANES 2005-06 | `PAD600` | 6, 0 | 1, 2 | 3–5 |
| TV (todas) | `P04501`, `q59a`, `PAD590` | mesma lógica, com "não assiste" no 0 | | |

## Validação

- Contagens da spec em `tests/test_contagens.py`.
- Distribuições comparadas com o inventário (ex.: `N010` em ≥ 15 anos: 58.090 / 16.039 / 5.773 / 10.944).
- `tests/test_faltantes.py` falha se algum valor da tabela de códigos especiais aparecer numa variável do contrato.

## Riscos

| Risco | Efeito | Mitigação |
|---|---|---|
| Memória ao ler a PNS (455 MB) e o Vigitel (578 MB) | script lento ou travado | ler só as colunas usadas; Vigitel em blocos |
| Faixas de horas diferentes entre bases | exposição não equivalente | 3 categorias com cortes em 1 h e 3 h, comuns às três bases; equivalência marcada "aproximada" |
| Licença do Vigitel não declarada | recorte não pode ir para o git | versionar só o script até esclarecer |
| Turquia sem codebook | variáveis sem rótulo (sexo) | usar só o que tem rótulo; sexo fica ausente |

## Histórico

- 2026-11-27: executado. As quatro bases de repositório ficaram num único `repositorios.py` (são leituras curtas). `requirements.txt` com versões fixadas; `factor_analyzer` 0.5.1 instalado para a 002. R não está instalado na máquina (`Rscript` não encontrado), o que decide a T040 da 003 por Python.
