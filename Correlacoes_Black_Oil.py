"""
Correlação para fator de COMPRESSIBILIDADE ISOTÉRMICO
"""
import math as M


def correlacao_de_Brill_e_Beggs(Ppr, Tpr):
    """
    :param Ppr: Pressão pseudoreduzida [adimensional]
    :param Tpr: Temperatura pseudocrítica [adimensional]
    :return: Fator de compressibilidade do gás
    """
    A = 1.39 * (Tpr-0.92)**0.5 - 0.36 * Tpr - 0.101
    B = (0.62 - 0.23 * Tpr) * Ppr + ((0.066/(Tpr - 0.86)) - 0.037) * Ppr**2 + (0.32/10**(9*(Tpr - 1))) * Ppr**6
    C = 0.132 - 0.32 * M.log10(Tpr)
    D = 10**(0.3106 - 0.49 * Tpr + 0.1824 * Tpr**2)
    Z = A + ((1-A)/M.exp(B)) + C * Ppr**D
    return Z


def correlacao_Papay(Ppr, Tpr):
    """
    :param Ppr: Pressão pseudoreduzida [adimensional]
    :param Tpr: Temperatura pseudocrítica [adimensional]
    :return: Fator de compressibilidade do gás
    """
    Z = 1 - ((3.53 * Ppr)/(10**(0.9813 * Tpr))) + ((0.274 * Ppr**2)/(10**(0.8157 * Tpr)))
    return Z


def correlacao_de_Hall_Yarborough(Ppr, Tpr, x0):
    """
    :param Ppr: Pressão pseudoreduzida [adimensional]
    :param Tpr: Temperatura pseudocrítica [adimensional]
    :param x0: Densidade reduzida da mistura gasosa (valor que zera a função objetivo)
    :return: Fator de compressibilidade do gás
    """
    # Acho que tem um erro nesse cálculo. Inclusive, o resultado não beteu quando fiz um exemplo
    """
    Ou tavez não esteja errado. Na verdade ele é um chute no início. Mas é calculado pelo método da secante.
    """

    A = 14.7 * Tpr - 9.76 * Tpr**2 + 4.58 * Tpr**3
    B = 90.7 * Tpr - 242.2 * Tpr**2 + 42.4 * Tpr**3
    F = lambda y: - 0.06125 * Ppr * Tpr * M.exp(-1.2 * (1-Tpr)**2) + ((y + y**2 + y**3 - y**4)/(1 - y)**3) -\
                  A * y**2 + B * y**(1.18 + 2.82 * Tpr)

    Pert = 10**-6  # pertubation
    Parad = 10**-4  # Stop's Criterion

    while True:
        xold = x0
        x0 = xold - ((Pert * xold * F(xold))/(F(xold + Pert * xold) - F(x0)))
        Erro = ((xold - x0)/xold) * 100
        if Erro <= Parad:
            break

    z = ((1 + x0 + xold**2 - x0**3)/(1 - x0)**3) - A * x0 + B * x0**(1.18 + 2.82 * Tpr)
    return z


def correlacao_dranchukabukassem(Ppr, Tpr, zc, x0):
    """
    :param Ppr: Pressão pseudoreduzida [adimensional]
    :param Tpr: Temperatura pseudocrítica [adimensional]
    :param zc: z crítico. Fornecido pelo usuário?
    :param x0: Valor que zera função objetivo
    :return: Fator de compressibilidade do gás
    """
    A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11 = 0.3265, -1.0700, -0.5339, 0.01569, -0.05165, 0.5475, -0.7361, \
                                                   0.1844, 0.1056, 0.6134, 0.7210
    F = lambda z: 1 + (A1 + A2/Tpr + A3/Tpr**3 + A4/Tpr**4 + A5/Tpr**5) * ((zc * Ppr)/(z * Tpr)) + (A6 + A7/Tpr + A8/Tpr**2) * \
        ((zc * Ppr)/(z * Tpr))**2 - A9 * (A7/Tpr + A8/Tpr**2) * ((zc * Ppr)/(z * Tpr))**5 +\
        A10 * (1 + A11 * ((zc * Ppr)/(z * Tpr))**2) * ((((zc * Ppr)/(z * Tpr))**2) * M.exp(-A11 * ((zc * Ppr)/(z * Tpr))**2))/(Tpr**3) - z

    Pert = 10 ** -6  # pertubation
    Parad = 10 ** -4  # Stop's Criterion

    while True:
        xold = x0
        x0 = xold - ((Pert * xold * F(xold)) / (F(xold + Pert * xold) - F(x0)))
        Erro = ((xold - x0) / xold) * 100  # verificar se o erro deve estar em porcentagem ou se é muito grande
        if Erro <= Parad:
            break

    z = x0
    return z


def fator_volume_formação_gas(Z, T, P):  # Fator volume-formação do gás real (Bg)
    """
    :param Z: Fator Z [adimensional]
    :param T: Temperatura [°F] - Acho
    :param P: Presão [psia] - Acho
    :return: Fator volume-formação do gás [m³/m³ std]

    Notas:
    Pressão na condição de superfície (Psc) [psia]
    Temperatura na condição de superfície (Tsc) [°F]
    """
    Psc = 14.7
    Tsc = 60
    Bg = (Psc/Tsc)/(P/Z * T)

    # Verificar as unidades e se precisa transformá-las para cálculos posteriores
    return Bg


def correlacao_Dempsey(Ppr, Tpr, u):
    """
    :param Ppr: Pressão pseudoreduzida [adimensional]
    :param Tpr: Temperatura pseudocrítica [adimensional]
    :param u: viscosidade do gás para uma dada condição de pressão e temperatura. Fornecido pelo usuário?
    :return: viscosidade do gás na condição de pressão atmosférica [cP]

    Nota, em alguns cáculos anteriores a formulação geral, a temperatura foi dada em °F e y_ em mol
    """
    A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15 = -2.4621, 2.9705, -2.8626 * 10**-1, \
        8.0542 * 10**-3, 2.8086, -3.4980, 3.6037 * 10**-1, -1.0443 * 10**-2, -7.9339 * 10**-1, 1.3964,\
            1.4914 * 10**-1, 4.4102 * 10**-3, 8.3939 * 10**-2, -1.8641 * 10**-1, 2.0336 * 10-2, -6.0958 * 10**-4

    ug = u/(M.exp((A0 + A1 * Ppr + A2* Ppr**2 + A3 * Ppr**3 + Tpr * (A4 + A5 * Ppr + A6 * Ppr**2 + A7 * Ppr ** 3) +
                   Tpr**2 * (A8 * A9 * Ppr + A10 * Ppr**2 + A11 * Ppr**3) + Tpr**3 * (A12 + A13 * Ppr + A14 * Ppr**2 +
                                                                                      A15 * Ppr**3))-(M.log(Tpr, M.e))))

    # verificar se essa expressão está correta, vamos verificar nas propriedades dos logaritmos
    return ug

def correlacao_lee_et_al(Deg, T, Mg):
    """
    :param Deg: Densidade do gás [lb/ft³]
    :param T: Temperatura [°R]
    :param Mg: Peso molecular do gás [lbm/(lb mol)]
    :return: viscosidade de gás [cP]
    """
    xv = 3.448 + (986.4/T) + 0.01009 * Mg
    yv = 2.4 - 0.2 * xv
    kv = ((9.379 + 0.0160 * Mg) * T**1.5)/(209.2 + 19.26 * Mg + T)
    ug = 10**-4 * M.exp(xv * (Deg/62.4)**yv)
    return ug


# Falta colocar o cálculo da mássa específica do gás, que depende do fator de compressibilidade isotérmico do gás.
# que é o mesmo que nós calculamos nas correlações.
