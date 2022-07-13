from Fator_Z_Correlacoes_Black_Oil import *

dg = float(input('SE A GRAVIDADE ESPECÍFICA (DG) FOR CONHECIDA INFORME SEU VALOR! CASO CONTRÁRIO, DIGITE "0">> '))

if dg != 0:
    if dg < 0.75:  # gás seco
        Ppc = (677 + 15 * dg - 37.5 * dg ** 2) * 6894.76  # Pa
        Tpc = (168 + 325 * dg - 12.5 * dg ** 2) * 0.5556  # K
    else:
        Ppc = (706 - 51.7 * dg - 11.1 * dg ** 2) * 6894.76  # gás úmido
        Tpc = (187 + 330 * dg - 71.5 * dg ** 2) * 0.5556

if dg == 0:
    caminho = input('POSSUI DADOS DE PRESSÃO CRÍTICA E TEMPERATURA CRÍTICA? S/N>> ').upper()
    if caminho == "N":
        Qnt = int(input('INFORME A QUANTIDADE DE COMPONENTES>> '))
        unidade = input('UNIDADE DA MASSA MOLAR (MM): "kg/mol" ou "lb/mol">> ').upper()
        MMT = 0
        for i in range(0, Qnt):
            if unidade == "LB/MOL":
                MM = float(input(f'INFORME A MASSA MOLAR DO {i + 1}° COMPONENTE>> '))
                yi = float(input(f'INFORME A FRAÇÃO MOLAR DO {i + 1}° COMPONENTE>> '))
            elif unidade == "KG/MOL":
                MM = float(input(f'INFORME A MASSA MOLAR DO {i + 1}° COMPONENTE>> ')) * 2.20462
                yi = float(input(f'INFORME A FRAÇÃO MOLAR DO {i + 1}° COMPONENTE>> '))
            MMT += yi * MM
        dg = MMT / 28.96
    else:
        yi = input('INSIRA AS FRAÇÕES MOLARES SEPARADAS POR ESPAÇO>> ').split(' ')
        yi = [float(dado) for dado in yi]
        TC = input('INSIRA AS TEMPERATURAS CRÍTICAS SEPARADAS POR ESPAÇO>> ').split(' ')
        unit_Tc = input('INFORME A UNIDADE (K, C, R OU F)>> ')
        if unit_Tc.upper() == "C":
            unit_Tc = [float(dados)+274.15 for dados in TC]
        elif unit_Tc.upper() == "R":
            unit_Tc = [float(dados) * 0.5556 for dados in TC]
        elif unit_Tc.upper() == "F":
            unit_Tc = [(float(dados) - 32) * 5/9 + 273.15 for dados in TC]
        elif unit_Tc.upper() == "K":
            unit_Tc = [float(dados) * 1 for dados in TC]
        # CONVERSÕES PARA K
        PC = input('INSIRA AS PRESSÕES CRÍTICAS P1 P2 P3>> ').split(' ')
        unit_Pc = input('INFORME A UNIDADE (Bar Pa Atm Torr mmHg Kgf/cm² Kgf/in² ou Psi)>> ')
        if unit_Pc.upper() == "BAR":
            unit_Pc = [float(dados) * 100_000 for dados in PC]
        elif unit_Pc.upper() == "PA":
            unit_Pc = [float(dados) for dados in PC]
        elif unit_Pc.upper() == "ATM":
            unit_Pc = [float(dados) * 101_325 for dados in PC]
        elif unit_Pc.upper() == "TORR":
            unit_Pc = [float(dados) * 133.322 for dados in PC]
        elif unit_Pc.upper() == "MMHG":
            unit_Pc = [float(dados) * 133.322 for dados in PC]
        elif unit_Pc.upper() == "KGF/CM²":
            unit_Pc = [float(dados) * 98066.52 for dados in PC]
        elif unit_Pc.upper() == "KGF/IN²":
            unit_Pc = [float(dados) * 15200.3 for dados in PC]
        elif unit_Pc.upper() == "PSI":
            unit_Pc = [float(dados) * 6894.76 for dados in PC]
        # CONVERSÕES PARA Pa
        PC = unit_Pc
        TC = unit_Tc

        Tpc = sum([x * y for x, y in zip(yi, TC)])
        Ppc = sum([x * y for x, y in zip(yi, PC)])


Ci = input(f'POSSUI COMPONENTE INORGÂNICO NO FLUIDO? S/N>> ').upper()


if Ci == "S":
    YCO2 = float(input('INFORME A FRAÇÃO MOLAR DE CO2>> '))
    YN2 = float(input('INFORME A FRAÇÃO MOLAR DE N2>> '))
    YH2S = float(input('INFORME A FRAÇÃO MOLAR DE H2S>> '))
    Ppc = Ppc + 440 * YCO2 + 600 * YH2S - 170 * YN2
    Tpc = Tpc - 80 * YCO2 + 130 * YH2S - 250 * YN2

Tabs = input('INFORME A TEMPERATURA ABSOLUTA (K, C, R OU F) SEGUIDA COM A SIGLA E SEPERADOS POR ESPAÇO>> ').split(' ')
if Tabs[1].upper() == "C":
    Tabs = float(Tabs[0]) + 273.15
elif Tabs[1].upper() == "R":
    Tabs = float(Tabs[0]) * 5/9
elif Tabs[1].upper() == "F":
    Tabs = (float(Tabs[0]) - 32) * 5/9 + 273.15
elif Tabs[1].upper() == "K":
    Tabs = float(Tabs[0]) * 1
# CONVERSÕES PARA K
Pabs = input('INFORME A PRESSÃO ABSOLUTA (Bar Pa Atm Torr mmHg Kgf/cm² Kgf/in² ou Psi) SEGUIDA COM A SIGLA E SEPARADO '
             'POR ESPAÇO>> ').split(' ')
if Pabs[1] == "BAR":
    Pabs = float(Pabs[0]) * 100_000
elif Pabs[1].upper() == "PA":
    Pabs = float(Pabs[0])
elif Pabs[1].upper() == "ATM":
    Pabs = float(Pabs[0]) * 101_325
elif Pabs[1].upper() == "TORR":
    Pabs = float(Pabs[0]) * 133.322
elif Pabs[1].upper() == "MMHG":
    Pabs = float(Pabs[0]) * 133.322
elif Pabs[1].upper() == "KGF/CM²":
    Pabs = float(Pabs[0]) * 98066.52
elif Pabs[1].upper() == "KGF/IN²":
    Pabs = float(Pabs[0]) * 15200.3
elif Pabs[1].upper() == "PSI":
    Pabs = float(Pabs[0]) * 6894.76
# CONVERSÕES PARA PA


Ppr = Pabs/Ppc
Tpr = Tabs/Tpc


def iterando_correlacoes(A1="BB", A2="HY", A3="DK"):
    if A3 == "DK":
        if 1 < Tpr < 3 and 0.2 < Ppr < 30:
            x0 = correlacao_Papay(Ppr, Tpr)
            zc = float(input('INFORME O VALOR DE Z CRÍTICO DA MISTURA PARA DAK>> '))
            print(' ')
            print(correlacao_dranchukabukassem(Ppr, Tpr, zc, x0))
        else:
            print('TPR OU PPR ESTÁ FORA DO INTERVALO!!!')
    if A1 == 'BB':
        if 1.2 < Tpr < 2.4 and 0 < Ppr < 13:
            print(correlacao_de_Brill_e_Beggs(Ppr, Tpr))
        else:
            print('TPR OU PPR ESTÁ FORA DO INTERVALO!!!')
    if A2 == "HY":
        if 1.2 < Tpr < 3 and 0.1 < Ppr < 24:
            print(correlacao_de_Hall_Yarborough(Ppr, Tpr))
        else:
            print('TPR OU PPR ESTÁ FORA DO INTERVALO!!!')
    print(f'Tpr>> {Tpr}\nPpr>> {Ppr}')
    print(' ')
    return ' '


print(iterando_correlacoes())
"""
Exemplo 2-5
yi = 0.02 0.01 0.85 0.04 0.03 0.03 0.02
tc = 547.91 227.49 343.33 549.92 666.06 734.46 765.62
pc = 1071 493.1 666.4 706.5 616.4 527.9 550.6
Zc = 0.288
"""
