from Correlacoes_Black_Oil import *

dg = float(input('SE A GRAVIDADE ESPECÍFICA (DG) FOR CONHECIDA INFORME SEU VALOR! CASO CONTRÁRIO, DIGITE "0":  '))
if dg == 0:
    caminho = input('POSSUI DADOS DE PRESSÃO CRÍTICA E TEMPERATURA CRÍTICA? S/N: ').upper()
    if caminho == "N":
        print(' ')
        print('ENCONTRANDO O DG POR FRAÇÃO MOLAR...')
        print(' ')
        Qnt = int(input('INFORME A QUANTIDADE DE COMPONENTES:  '))
        unidade = input('UNIDADE DA MASSA MOLAR (MM): "kg/mol" ou "lb/mol": ').upper()
        MMT = 0
        YI1 = 0
        YI2 = 0
        # Tratar o erro das frações molares
        for i in range(0, Qnt):
            if unidade == "LB/MOL":
                MM = float(input(f'INFORME A MASSA MOLAR DO {i + 1}° COMPONENTE:  '))
                yi = float(input(f'INFORME A FRAÇÃO MOLAR DO {i + 1}° COMPONENTE:  '))
                YI1 += yi
            elif unidade == "KG/MOL":
                MM = float(input(f'INFORME A MASSA MOLAR DO {i + 1}° COMPONENTE:  ')) * 2.20462
                yi = float(input(f'INFORME A FRAÇÃO MOLAR DO {i + 1}° COMPONENTE:  '))
                YI2 += yi
            MMT += yi * MM
        print(f'yi1: {YI1}, yi2: {YI2} ')
        if YI1 != 1 or YI2 != 1:
            raise ValueError('A soma da fração molar é diferente de 1.')
        dg = MMT / 28.96  # 28.96 é a massa molecular do ar. Precismos corrigir esssa
    else:
        print(' ')
        print('ENCONTRANDO O DG POR PRESSÕES CRÍTICAS E TEMPERATURAS CRÍTICAS...')
        print(' ')
        yi = input('INSIRA AS FRAÇÕES MOLARES Y1 Y2 Y3... : ').split(' ')
        yi = [float(dado) for dado in yi]

        tci = input('INSIRA AS TEMPERATURAS CRÍTICAS T1 T2 T3... EM RANKINE: ').split(' ')
        tci = [float(dado) for dado in tci]

        pci = input('INSIRA AS PRESSÕES CRÍTICAS P1 P2 P3... EM PSI: ').split(' ')
        pci = [float(dado) for dado in pci]

        Tpc = sum([x * y for x, y in zip(yi, tci)])
        Ppc = sum([x * y for x, y in zip(yi, pci)])

if dg != 0:
    if dg < 0.75:  # gás seco
        Ppc = (677 + 15 * dg - 37.5 * dg ** 2)  # Psia
        Tpc = (168 + 325 * dg - 12.5 * dg ** 2)  # Rankine
    else:
        Ppc = (706 - 51.7 * dg - 11.1 * dg ** 2)  # * 6894.76
        Tpc = (187 + 330 * dg - 71.5 * dg ** 2)  # * 5/9


Ci = input(f'POSSUI COMPONENTE INORGÂNICO NO FLUIDO? S/N:  ').upper()

if Ci == "S":
    CO2 = input('TEM CO2? "S/N"?: ').upper()
    if CO2 == "S":
        YCO2 = float(input('INFORME A FRAÇÃO MOLAR DE CO2:'))
    else:
        YCO2 = 0

    N2 = input('TEM N2? "S/N"?: ').upper()
    if N2 == "S":
        YN2 = float(input('INFORME A FRAÇÃO MOLAR DE N2:'))
    else:
        YN2 = 0

    H2S = input('TEM H2S? "S/N"?: ').upper()
    if H2S == "S":
        YH2S = float(input('INFORME A FRAÇÃO MOLAR DE H2S:'))
    else:
        YH2S = 0

    Ppc = Ppc + 440 * YCO2 + 600 * YH2S - 170 * YN2
    Tpc = Tpc - 80 * YCO2 + 130 * YH2S - 250 * YN2

# 0.02 0.01 0.85 0.04 0.03 0.03 0.02
# 547.91 227.49 343.33 549.92 666.06 734.46 765.62
# 1071 493.1 666.4 706.5 616.4 527.9 550.6

"""
Minha dúvida é em relação aos vários ppc's e tpc's que obtivemos e se eles vão interferir nos cálculos dos componentes
inorgânicos na mistura
"""

Tabs = input('INFORME A TEMPERATURA ABSOLUTA (K, C, R OU F) SEGUIDA COM A SIGLA E SEPERADOS POR ESPAÇO:  ').split(' ')

if Tabs[1].upper() == "C":
    Tabs = float(Tabs[0]) + 491.67
elif Tabs[1].upper() == "R":
    Tabs = float(Tabs[0])
elif Tabs[1].upper() == "F":
    Tabs = (float(Tabs[0]) + 459.67)   # Precisamos verificar
elif Tabs[1].upper() == "K":
    Tabs = float(Tabs[0]) * 1.8

Pabs = input('INFORME A PRESSÃO ABSOLUTA (PA, BAR, PSI) SEGUIDA COM A SIGLA E SEPARADO POR ESPAÇO:  ').upper().split(' ')

if Pabs[1].upper() == "BAR":
    Pabs = (float(Pabs[0]) * 14.503)
elif Pabs[1].upper() == "PSI":
    Pabs = float(Pabs[0])
elif Pabs[1].upper() == "PA":
    Pabs = (float(Pabs[0])) * 0.000145


Ppr = Pabs/Ppc
Tpr = Tabs/Tpc  # ele tá considerando o Tabs como string? Acho que vou paasr para tipo float para ver o que está havendo


Dado = input('DEFINA A CORRELAÇÃO: DIGITE "BB" PARA BRILL E BEGGS, "PP" PARA PAPAY, '
             '"HY" PARA HALL YARBOROUGH, "DK" PARA DRANCHUK & ABU-KASSEM:  ').upper()

if Dado == "PP":
    FatorZ = correlacao_Papay(Tpr, Ppr)
    print(f'FATOR Z PARA CORRELAÇÃO DE PAPAY:  {FatorZ}')

elif Dado == 'BB':
    if 1.2 < Tpr < 2.4 and 0 < Ppr < 13:
        FatorZ = correlacao_de_Brill_e_Beggs(Ppr, Tpr)
        print(f'FATOR Z PARA CORRELAÇÃO DE BRILL E BEGGS:  {FatorZ}')
    else:
        print('TPR OU PPR ESTÁ FORA DO LIMITE!')

elif Dado == "HY":
    if 1.2 < Tpr < 3 and 0.1 < Ppr < 24:
        x0 = correlacao_Papay(Ppr, Tpr)
        FatorZ = correlacao_de_Hall_Yarborough(Ppr, Tpr, x0)
        print(f'FATOR Z PARA CORRELAÇÃO DE HALL-YARBOROUGH:  {FatorZ}')
    else:
        print('TPR OU PPR ESTÁ FORA DO LIMITE!')

elif Dado == "DK":
    if 1 < Tpr < 3 and 0.2 < Ppr < 30:
        x0 = correlacao_Papay(Ppr, Tpr)
        zc = float(input('INFORME O VALOR DE Z CRÍTICO DA MISTURA:  '))
        FatorZ = correlacao_dranchukabukassem(Ppr, Tpr, zc, x0)
        print(f'FATOR Z PARA CORRELAÇÃO DE DRANCHUK & ABU-KASSEM:  {FatorZ}')
    else:
        print('TPR OU PPR ESTÁ FORA DO LIMITE!')

# NO FUTURO ISSO VAI SAI DAQUI
print(f'Esse é o valor de Ppc: {Ppc}')
print(f'Esse é o valor de Tpc: {Tpc}')
print(f'Esse é o valor de Ppr: {Ppr}')
print(f'Esse é o valor de Tpr: {Tpr}')
