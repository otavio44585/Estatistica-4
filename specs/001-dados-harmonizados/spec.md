# 001 — Dados harmonizados

Status: **concluída** (2026-11-27). Executada a pedido de um integrante, antes da aprovação formal do grupo (pendente).

## Pergunta

É possível construir, a partir das bases abertas, medidas de uso de tela e de sono comparáveis entre Brasil, EUA e outros países?

## Por quê

Todas as comparações das specs 003 e 004 dependem de medir a mesma coisa dos dois lados. Se a medida não for equivalente, a diferença entre países pode ser só diferença de pergunta.

## Bases (proposta — o grupo aprova)

| Grupo | Núcleo | Complementares, se houver tempo | Só sensibilidade |
|---|---|---|---|
| Brasil | PNS 2019, Vigitel 2024 | PNS 2013 (só TV), PeNSE 2015 (adolescentes) | — |
| EUA | NHANES 2005-06 | NHANES 2011–16, NSCH 2017/2025, YRBS 2021, ATUS 2025 | — |
| Outros países | Xuzhou (China), Pérez-Chada (Argentina), Doomscrolling (Turquia), Okajima (Japão) | Rede SA (China), China 3 ondas, Siebers (Holanda), Ibadan (Nigéria) | Paquistão, Bangladesh, Sleep Patterns |

## Contrato de variáveis

Cada base processada expõe as variáveis abaixo quando existirem. O grau de equivalência é parte do contrato.

| Variável | Definição | Onde existe | Equivalência |
|---|---|---|---|
| `dif_adormecer_freq` | dificuldade para adormecer nas 2 categorias de maior frequência (0/1) | Vigitel, NHANES 2005-06 | equivalente: mesma pergunta, 5 frequências com âncoras diferentes |
| `problema_sono_freq` | problema de sono em mais da metade dos dias (0/1) | PNS 2019, PNS 2013 | aproximada: o item inclui despertares e dormir demais; janela de 2 semanas |
| `sintoma_1..3` | 3 sintomas de insônia: adormecer, voltar a dormir, acordar cedo (0–4) | Vigitel, NHANES 2005-06 | equivalente |
| `insonia_idx` | soma dos 3 sintomas (0–12) | Vigitel, NHANES 2005-06 | equivalente |
| `sono_horas` | duração habitual do sono (h) | Vigitel, NHANES, Argentina, Japão, Turquia, Nigéria | aproximada: período de referência varia |
| `latencia_min` | minutos para adormecer | NHANES 2005-06 (topo 60), Argentina, Turquia | equivalente entre essas; **não existe em base brasileira aberta** |
| `escore_sono_escala` | escore de escala validada (PSQI, AIS, PDSS, PHQ-9 item 3) | conforme base | não comparável entre escalas diferentes; comparável via métrica padronizada (spec 004) |
| `tela_digital_cat` | computador/tablet/celular no lazer: 0 = não usa ou < 1 h; 1 = 1 a < 3 h; 2 = ≥ 3 h | PNS 2019, Vigitel, NHANES 2005-06 | aproximada: NHANES inclui games e é de 2005, antes do smartphone |
| `tela_tv_cat` | TV, mesmas faixas | PNS 2019, PNS 2013, Vigitel, NHANES, PeNSE | aproximada: PeNSE separa "> 3 h" de "≥ 3 h" |
| `tela_presono_h` | horas de tela antes de dormir | Japão (3 h antes), Argentina | aproximada: janelas diferentes |
| `uso_problematico` | escore de escala de dependência ou uso problemático | Xuzhou e Rede (SAS-SV), Turquia (doomscrolling), China 3 ondas | não comparável entre escalas; via métrica padronizada |
| `idade`, `faixa_etaria` | anos; 18–29 / 30–44 / 45–59 / 60+ | todas | equivalente |
| `sexo` | 0/1 | todas, exceto Turquia (sem rótulo) | equivalente |
| `escolaridade3` | < ensino médio / ensino médio / superior | PNS, Vigitel, NHANES | aproximada: sistemas de ensino diferentes |
| `depressao` | escore PHQ-9 ou diagnóstico referido | PNS, NHANES (PHQ-9); Vigitel (diagnóstico) | aproximada |
| `peso`, `estrato`, `upa` | desenho amostral | inquéritos | — |

## Critérios de aceite

- Dado o script de uma base, quando roda do zero a partir dos brutos, então gera o arquivo processado e um log com o n antes e depois de cada filtro.
- Os n conferem com o inventário: PNS 2019 morador selecionado 90.846 (88.531 com 18 anos ou mais); Vigitel 2024 27.048; NHANES 2005-06 6.139 no questionário de sono (5.563 com 18 anos ou mais); Xuzhou 2.317; Argentina 864 completos; Turquia 1.216; Japão 381.
- Toda variável do contrato tem entrada no dicionário harmonizado com fonte, recodificação, faltantes e equivalência.
- Nenhum código especial sobrevive como valor numérico (teste automatizado).
- As bases de inquérito saem com peso e, quando existirem, estrato e UPA.
- A tabela de equivalência é publicada em `resultados/001/`.

## Fora de escopo

Bases com acesso restrito (ABCD, UK Biobank, Pelotas, SONAR-Brasil etc.), coleta própria e os dados do sensor em `data_test_sono/`.

## Perguntas em aberto

1. O núcleo de bases acima está aprovado?
2. Adolescentes (PeNSE, YRBS, NSCH) entram, ou o trabalho fica em adultos?
3. Vigitel não declara licença: o recorte processado entra no git ou só o script?

## Histórico

- 2026-11-27: rascunho.
- 2026-11-27: executada. Decisões adotadas na execução (revisáveis pelo grupo): núcleo de 7 bases como proposto; adolescentes só na base argentina, rotulados; recortes processados fora do git (`.gitignore`), regenerados pelos scripts. Os n conferem com o inventário (`tests/test_001_contagens.py`). Na PNS, 18 pessoas com 101 a 107 anos são idades válidas: a faixa de validação de idade passou para 10–120. Xuzhou e Japão codificam sexo como 1/2 sem rótulo no depósito: entra como covariável com o rótulo marcado "desconhecido". Argentina: 163 dos 864 sem idade (sem data de nascimento no depósito).
- 2026-11-27: **NHANES 2005-06 retirado do trabalho inteiro** (decisão do usuário: "a única base deles foi de 2005; pode tirar do trabalho inteiro"; a prevalência de tela dos EUA de antes do smartphone não ajuda nas conclusões). O núcleo passa a ter 6 bases: PNS 2019 e Vigitel 2024 (Brasil) e as 4 de repositório. O script de harmonização do NHANES foi removido (fica no histórico do git, commit e5f249a), e as linhas do NHANES saíram do dicionário, da equivalência, das figuras e dos testes. As tabelas acima que ainda citam o NHANES descrevem a proposta original.
