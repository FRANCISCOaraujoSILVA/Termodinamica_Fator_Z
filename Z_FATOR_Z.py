from Fator_Z_Correlacoes_Black_Oil import *
variavel = 'variavel'
dg = float(input('SE A GRAVIDADE ESPECÍFICA (DG) FOR CONHECIDA INFORME SEU VALOR! CASO CONTRÁRIO, DIGITE "0">> '))

if dg != 0 and variavel == 'variavel':
    if dg < 0.75:  # gás seco
        Ppc = (677 + 15 * dg - 37.5 * dg ** 2)
        Tpc = (168 + 325 * dg - 12.5 * dg ** 2)
    else:  # gás úmido
        Ppc = (706 - 51.7 * dg - 11.1 * dg ** 2)
        Tpc = (187 + 330 * dg - 71.5 * dg ** 2)
else:
    if dg < 0.75:  # gás seco
        Ppc = (677 + 15 * dg - 37.5 * dg ** 2)
        Tpc = (168 + 325 * dg - 12.5 * dg ** 2)
    else:
        Ppc = (706 - 51.7 * dg - 11.1 * dg ** 2)
        Tpc = (187 + 330 * dg - 71.5 * dg ** 2)

if dg == 0:
    caminho = input('POSSUI DADOS DE PRESSÃO CRÍTICA E TEMPERATURA CRÍTICA? S/N>> ').upper()
    if caminho == "N":
        Qnt = int(input('INFORME A QUANTIDADE DE COMPONENTES>> '))
        unidade = input('UNIDADE DA MASSA MOLAR (MM): "kg/mol" ou "lb/mol">> ').upper()
        MMT = 0
        MM = 0
        yi = 0
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
        unit_Tc = input('INFORME A UNIDADE (K, C, R OU F)>> ').upper()
        if unit_Tc.upper() == "C":
            unit_Tc = [float(dados) * 9/5 + 491.67 for dados in TC]
        elif unit_Tc.upper() == "R":
            unit_Tc = [float(dados) for dados in TC]
        elif unit_Tc.upper() == "F":
            unit_Tc = [(float(dados) + 459.67) for dados in TC]
        elif unit_Tc.upper() == "K":
            unit_Tc = [float(dados) * 1.8 for dados in TC]

        # CONVERSÕES PARA R

        PC = input('INSIRA AS PRESSÕES CRÍTICAS P1 P2 P3>> ').split(' ')

        unit_Pc = input('INFORME A UNIDADE (Bar Pa Atm Torr mmHg Kgf/cm2 Kgf/in2 ou Psi)>> ').upper()
        if unit_Pc.upper() == "BAR":
            unit_Pc = [float(dados) * 14.504 for dados in PC]
        elif unit_Pc.upper() == "PA":
            unit_Pc = [float(dados) / 6895 for dados in PC]
        elif unit_Pc.upper() == "ATM":
            unit_Pc = [float(dados) * 14.696 for dados in PC]
        elif unit_Pc.upper() == "TORR":
            unit_Pc = [float(dados) / 51.715 for dados in PC]
        elif unit_Pc.upper() == "MMHG":
            unit_Pc = [float(dados) / 51.715 for dados in PC]
        elif unit_Pc.upper() == "KGF/CM2":
            unit_Pc = [float(dados) * 14.223 for dados in PC]
        elif unit_Pc.upper() == "KGF/IN2":
            unit_Pc = [float(dados) * 2.205 for dados in PC]
        elif unit_Pc.upper() == "PSI":
            unit_Pc = [float(dados) for dados in PC]

        # CONVERSÕES PARA PSI

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

Tabs = input('INFORME A TEMPERATURA ABSOLUTA (K, C, R OU F) SEGUIDA COM A SIGLA E SEPERADOS POR ESPAÇO>> ').upper()\
    .split(' ')

if Tabs[1].upper() == "C":
    Tabs = float(Tabs[0]) * 9/5 + 491.67
elif Tabs[1].upper() == "R":
    Tabs = float(Tabs[0])
elif Tabs[1].upper() == "F":
    Tabs = (float(Tabs[0]) + 459.67)
elif Tabs[1].upper() == "K":
    Tabs = float(Tabs[0]) * 1.8

# CONVERSÕES PARA R


Pabs = input('INFORME A PRESSÃO ABSOLUTA (Bar Pa Atm Torr mmHg Kgf/cm2 Kgf/in2 ou Psi) SEGUIDA COM A SIGLA E SEPARADO '
             'POR ESPAÇO>> ').upper().split(' ')

if Pabs[1] == "BAR":
    Pabs = float(Pabs[0]) * 14.514
elif Pabs[1].upper() == "PA":
    Pabs = float(Pabs[0]) / 6895
elif Pabs[1].upper() == "ATM":
    Pabs = float(Pabs[0]) * 14.696
elif Pabs[1].upper() == "TORR":
    Pabs = float(Pabs[0]) / 51.715
elif Pabs[1].upper() == "MMHG":
    Pabs = float(Pabs[0]) / 51.715
elif Pabs[1].upper() == "KGF/CM2":
    Pabs = float(Pabs[0]) * 14.223
elif Pabs[1].upper() == "KGF/IN2":
    Pabs = float(Pabs[0]) * 2.205
elif Pabs[1].upper() == "PSI":
    Pabs = float(Pabs[0])

# CONVERSÕES PARA PSI

Ppr = Pabs/Ppc
Tpr = Tabs/Tpc


def iterando_correlacoes(A1="HY", A2="DK"):
    if A2 == "DK":
        if 1 < Tpr < 3 and 0.2 < Ppr < 30:
            x0 = correlacao_Papay(Ppr, Tpr)
            zc = float(input('INFORME O VALOR DE Z CRÍTICO DA MISTURA PARA DAK>> '))
            print(' ')
            print(correlacao_dranchukabukassem(Ppr, Tpr, zc, x0))
        else:
            print('TPR OU PPR ESTÁ FORA DO INTERVALO!!!')
    if A1 == "HY":
        if 1.2 < Tpr < 3 and 0.1 < Ppr < 24:
            print(correlacao_de_Hall_Yarborough(Ppr, Tpr))
        else:
            print('TPR OU PPR ESTÁ FORA DO INTERVALO!!!')
    print(f'Tpr>> {Tpr}\nPpr>> {Ppr}')
    print(' ')
    return ' '


print(iterando_correlacoes())
"""
Caso:
300 k
50 kgf/cm²
Yi = 0.8 0.1 0.05 0.05
Tci = 190.6 305.4 369.9 407.9 [K]
Pci = 46.9 49.7 43.3 37.1 [kgf/cm²]


Caso: 
194 f
3810 pia
yi = 0.9712 0.0242 0.0031 0.0005 0.0002 0.0002 0.0006
Tci = 343.33 549.92 666.06 734.46 765.62 913.60 [R]
Pci = 666.4 706.5 616.0 527.9 550.6 436.9 372.0 [psia]
"""
