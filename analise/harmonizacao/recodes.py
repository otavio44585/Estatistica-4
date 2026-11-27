"""Tabelas de recodificação da spec 001 (plano, seção "Recodificações de exposição").

tela_*_cat: 0 = não usa ou < 1 h; 1 = 1 a < 3 h; 2 = ≥ 3 h.
tela_*_ord: ordem original das faixas com "não usa" no 0 (para correlação de postos, spec 004).
"""

# PNS 2019, P04501 (TV) e P04502 (computador/tablet/celular): 1 <1 h, 2 1-<2, 3 2-<3, 4 3-<6, 5 6+, 6 não usa
PNS_CAT = {6: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2}
PNS_ORD = {6: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5}

# Vigitel 2024, q59c / q59a: 1 <1 h, 2 1-2, 3 2-3, 4 3-4, 5 4-5, 6 5-6, 7 >6 h; q59a 8 = não assiste
VIG_CAT = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 2}   # 0 = não usa (q59b = 2) ou não assiste (q59a = 8)
VIG_ORD = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}

# Escolaridade em 3 faixas: 0 = abaixo do ensino médio, 1 = ensino médio, 2 = superior (completo ou não)
PNS_ESC = {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 2, 7: 2}            # VDD004A
VIG_ESC = {1: 0, 2: 1, 3: 2}                                    # fesc: 0-8, 9-11, 12+ anos de estudo

# PHQ-9 na ordem padrão do instrumento; a PNS faz as perguntas em outra ordem
PHQ_PNS = ["N012", "N016", "N010", "N011", "N014", "N017", "N013", "N015", "N018"]
PHQ_ROTULOS = ["interesse", "deprimido", "sono", "cansaço", "apetite", "fracasso", "concentração", "psicomotor", "autolesão"]
