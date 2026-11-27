# 001 — Como os dados foram preparados

## O problema

Cada pesquisa pergunta sobre tela e sono de um jeito. A PNS pergunta "quantas horas do seu tempo livre você usa computador, tablet ou celular", com 5 faixas. O Vigitel pergunta primeiro se a pessoa usa, depois quantas horas, com 7 faixas. O NHANES de 2005 pergunta sobre computador e videogame, com faixas de 1 hora. Se compararmos o número cru de cada uma, a diferença entre países pode ser só diferença de pergunta.

**Harmonizar** é criar, para cada base, as mesmas variáveis com o mesmo significado, e dizer quanto cada uma é parecida entre as bases.

## O que foi feito

1. **Um script por base** lê o arquivo bruto oficial e grava uma tabela limpa (`analise/dados/processados/<base>.parquet`). O script anota quantas pessoas sobram depois de cada filtro (`analise/dados/logs/`).
2. **Códigos especiais viram faltante.** Questionários usam números para "não sabe" e "recusou" (9, 77, 99, 777, 888, 999). Se um 99 ficasse como número, a média de horas de sono sairia absurda. A tabela de códigos de cada base está em `analise/comum/faltantes.py`, e um teste automático falha se algum valor fora da faixa válida aparecer.
3. **Faixas comuns de tela.** O corte comum às três bases de inquérito é 1 h e 3 h: 0 = não usa ou menos de 1 h; 1 = de 1 a menos de 3 h; 2 = 3 h ou mais.
4. **Grau de equivalência** de cada variável em cada base (`resultados/001/tabelas/equivalencia.csv`):
   - *equivalente*: mesma pergunta (os 3 sintomas de insônia do Vigitel e do NHANES);
   - *aproximada*: pergunta ou faixa diferente (o item de sono da PNS inclui "dormir mais do que de costume");
   - *não comparável*: escalas diferentes (PSQI, AIS, PDSS), que só se comparam por uma medida padronizada na spec 004.

## As bases

| Base | Quem | n usado | Medida de sono | Medida de tela |
|---|---|---|---|---|
| PNS 2019 | adultos do Brasil | 88.531 | item de sono do PHQ-9 (nas 2 últimas semanas) | horas de computador/tablet/celular e de TV |
| Vigitel 2024 | adultos das 27 capitais | 27.048 | 3 sintomas de insônia, duração do sono | idem |
| NHANES 2005-06 | adultos dos EUA | 5.563 | 3 sintomas de insônia, minutos para adormecer, duração | horas de computador/games e de TV |
| Xuzhou | universitários (China) | 2.317 | PSQI | escala de uso problemático do celular (SAS-SV) |
| Pérez-Chada | adolescentes (Argentina) | 864 | minutos para adormecer, duração, sonolência (PDSS) | horas de tela no dia e antes de dormir |
| Doomscrolling | 18–40 anos (Turquia) | 1.216 | PSQI, minutos para adormecer | escala de doomscrolling |
| Okajima | 18–29 anos (Japão) | 381 | escala de insônia de Atenas (AIS) | horas de celular nas 3 h antes de dormir |

As três primeiras são **inquéritos com desenho amostral**: cada pessoa tem um peso que diz quantas pessoas da população ela representa. As quatro últimas são amostras de conveniência, sem peso.

## Cuidados que aparecem depois

- **NHANES 2005-06 é de antes do smartphone.** Em 2005, 7% dos adultos americanos usavam computador ou games 3 h ou mais por dia. No Vigitel 2024 eram 27% (`resultados/001/tabelas/prevalencias.csv`). Comparar Brasil e EUA é comparar país e época juntos.
- **Sexo sem rótulo** em Xuzhou e no Japão (códigos 1 e 2 sem dizer qual é qual): entra como controle nos modelos, sem interpretar o coeficiente.
- **Argentina sem idade** para 163 dos 864 adolescentes: modelos com idade perdem esses casos, e a spec 005 testa o efeito disso.
- **Microdados não vão para o repositório.** O repositório é público e a licença do Vigitel não é declarada. Quem clonar roda os scripts a partir dos brutos (`STAT4_BRUTOS`).

## Como reproduzir

```bash
export STAT4_BRUTOS=/caminho/para/pesquisa/dados
python -m analise.harmonizacao.pns2019
python -m analise.harmonizacao.vigitel2024
python -m analise.harmonizacao.nhanes0506
python -m analise.harmonizacao.repositorios
python -m analise.harmonizacao.dicionario
python -m analise.harmonizacao.figuras
python -m pytest
```
