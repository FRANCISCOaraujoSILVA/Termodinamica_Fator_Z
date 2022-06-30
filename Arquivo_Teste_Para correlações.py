from Correlacoes_Black_Oil import *
Dado = input('Defina qual propriedade deseja encontrar: "Z" para fator Z, "UG" para viscosidade do gás, "BG"'
             'para Fator volume-Formação de Gás:  ').upper()

if Dado == "Z":
    Dado = input('Defina a correlação a ser usada: Digite "BB" para Brill e Beggs, "PP" para Papay, '
                 '"HY" para Hall Yarborough, "DK" para Dranchuk & Abu-Kassem:  ').upper()

# Será que esse dado aqui fora é igual ao dado ali dentro do if de cima? Acho que sim, pois usou a correlação certa

elif Dado == "UG":
    Dado = input(f'Defina a correlação para o cálculo da viscosidade do gás: Digite "DP", para Dempsey:  ').upper()


dg = float(input('Se a gravidade específica (dg) for conhecida, informe seu valor! Caso contrário, digite "0":  '))

if dg == 0:
    Qnt = int(input('Informe a quantidade de componentes:  '))
    MMT = 0
    # Tratar o erro das frações molares
    for i in range(0, Qnt):
        MM = float(input(f'Informe a massa molar do {i + 1} componente [kg/mol]:  '))
        yi = float(input(f'Informe a fração molar do {i + 1}° componente:  '))
        MMT += yi * MM
    dg = MMT/0.02896  # 0.02896 é a massa molecular do ar

if dg < 0.75:  # gás seco
    Ppc = (677 + 15 * dg - 37.5 * dg**2) * 6894.757228  # conversor de Psi para Pa
    Tpc = (168 + 325 * dg - 12.5 * dg**2) * 5/9  # conversor de Rankine para K
else:
    Ppc = (706 - 51.7 * dg - 11.1 * dg**2) * 6894.76
    Tpc = (187 + 330 * dg - 71.5 * dg**2) * 5/9

Ci = input(f'Possui componente inorgânico no fluido? S/N:  ').upper()

if Ci == "S":
    Qnt = input('Quais? [CO2, H2S, N2]. Insira os componentes separados por espaço!:  ').upper()

    if len(Qnt) == 1:
        if Qnt == "CO2":
            yi = (float(input(f'Informe a fração molar do componente {Qnt}:  ')))
            Ppc += 440 * yi
            Tpc += -80 * yi
        elif Qnt == "H2S":
            yi = (float(input(f'Informe a fração molar do componente {Qnt}:  ')))
            Ppc += 600 * yi
            Tpc += 130 * yi
        elif Qnt == "N2":
            yi = (float(input(f'Informe a fração molar do componente {Qnt}:  ')))
            Ppc += -170 * yi
            Tpc += -250 * yi
    else:
        Qnt = Qnt.split(' ')  # Cria uma lista de strings com a quantidade de componentes inseridas
        for i in range(0, len(Qnt)):
            yi = (float(input(f'Informe a fração molar do componente {Qnt[i]}:  ')))
            if Qnt[i] == "C02":
                Ppc += 440 * yi
                Tpc += -80 * yi
            elif Qnt[i] == "H2S":
                Ppc += 600 * yi
                Tpc += 130 * yi
            elif Qnt[i] == "N2":
                Ppc += -170 * yi
                Tpc += -250 * yi

Tabs = input('Informe a temperatura absoluta (K, °C, °R ou °F) seguida com a sigla e seperados por espaço:  ').split(' ')
if Tabs[1].upper() == "°C":
    Tabs = float(Tabs[0]) + 273.15
elif Tabs[1].upper() == "°R":
    Tabs = float(Tabs[0]) * 5/9
elif Tabs[1].upper() == "°F":
    Tabs = (float(Tabs[0]) + 459.67) * 5/9  # Mudei! antes era (Tabs * 9/5) - 459.67
elif Tabs[1].upper() == "K":
    Tabs = float(Tabs[0])

Pabs = input('Informe a pressão absoluta (Pa, Bar, Psi) seguida com a sigla e separado por espaço:  ').upper().split(' ')

if Pabs[1].upper() == "BAR":
    Pabs = (float(Pabs[0]) * 100000)
elif Pabs[1].upper() == "PSI":
    Pabs = (float(Pabs[0]) * 6894.757228)
elif Pabs[1].upper() == "PA":
    Pabs = (float(Pabs[0]))


Ppr = Pabs/Ppc
Tpr = Tabs/Tpc  # ele tá considerando o Tabs como string? Acho que vou paasr para tipo float para ver o que está havendo

# No futuro esse valores devem sair daqui
print(f'Valor de Tpr: {Tpr}')
print(f'Valor de Ppr: {Ppr}')
print(f'Valor de Tpc: {Tpc}')
print(f'Valor de Ppc: {Ppc}')

if Dado == "PP":
    FatorZ = correlacao_Papay(Tpr, Ppr)
    print(f'Fator Z para Correlação de Papay:  {FatorZ}')

elif Dado == 'BB':
    if 1.2 < Tpr < 2.4 and 0 < Ppr < 13:
        FatorZ = correlacao_de_Brill_e_Beggs(Ppr, Tpr)
        print(f'Fator Z para Correlação de Brill e Beggs:  {FatorZ}')
    else:
        print('Tpr ou Ppr podem estar fora do intervalo.')

elif Dado == "HY":
    if 1.2 < Tpr < 3 and 0.1 < Ppr < 24:
        x0 = correlacao_Papay(Ppr, Tpr)
        FatorZ = correlacao_de_Hall_Yarborough(Ppr, Tpr, x0)
        print(f'Fator Z para Correlação de Hall-Yarborough:  {FatorZ}')
    else:
        print('Tpr ou Ppr podem estar fora do intervalo.')

elif Dado == "DK":
    if 1 < Tpr < 3 and 0.2 < Ppr < 30:
        x0 = correlacao_Papay(Ppr, Tpr)
        zc = float(input('Informe o valor de z crítico da mistura:  '))
        FatorZ = correlacao_dranchukabukassem(Ppr, Tpr, zc, x0)
        print(f'Fator Z para Correlação de Dranchuk & Abu-Kassem:  {FatorZ}')
    else:
        print('Tpr ou Ppr podem estar fora do intervalo.')

elif Dado == "BG":
    Z = correlacao_Papay(Ppr, Tpr)
    T = float(input('Informe a temperatura da condição de superfície (°F):  '))
    P = float(input('Informe a Pressão da condição de superfície (psia):  '))
    BG = fator_volume_formação_gas(Z, T, P)
    print(f'Fator volume-formação de gás: {BG} {"Tem unidade?"}')
    print(f'Fator de expansão do gás (Eg): {1/BG} {"Tem unidade?"}')
    print(f'Ppr: {Ppr} {"Tem unidade?"}, Tpr: {Tpr} {"Tem unidade?"}')

elif Dado == "DP":
    u = float(input(f'Informe a viscosidade do gás (cp): '))
    UG = correlacao_Dempsey(Ppr, Tpr, u)
    print(f'Viscosidade do gás:  {UG}')