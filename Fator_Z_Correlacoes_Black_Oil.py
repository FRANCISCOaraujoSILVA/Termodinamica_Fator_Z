"""
Correlação para fator de COMPRESSIBILIDADE ISOTÉRMICO
Usando o Método de Newton-Raphson e Secante Modificada
"""
from sympy import *
import math as M

def correlacao_Papay(Ppr, Tpr):  # Essa correlação é simples mas tem suas limitações
    """
    :param Ppr: Pressão pseudoreduzida [adimensional]
    :param Tpr: Temperatura pseudoreduzida [adimensional]
    :return: Fator de compressibilidade do gás
    """
    Z = 1 - ((3.53 * Ppr) / (10 ** (0.9813 * Tpr))) + ((0.274 * Ppr ** 2) / (10 ** (0.8157 * Tpr)))
    return Z


def correlacao_de_Brill_e_Beggs(Ppr, Tpr):
    """
    :param Ppr: Pressão pseudoreduzida [adimensional]
    :param Tpr: Temperatura pseudoreduzida [adimensional]
    :return: Fator de compressibilidade do gás
    """
    A = 1.39 * (Tpr - 0.92) ** 0.5 - 0.36 * Tpr - 0.101
    B = (0.62 - 0.23 * Tpr) * Ppr + ((0.066 / (Tpr - 0.86)) - 0.037) * Ppr ** 2 + (
                0.32 / 10 ** (9 * (Tpr - 1))) * Ppr ** 6
    C = 0.132 - 0.32 * M.log10(Tpr)
    D = 10 ** (0.3106 - 0.49 * Tpr + 0.1824 * Tpr ** 2)
    Z = A + ((1 - A) / M.exp(B)) + C * Ppr ** D
    return f'FATOR Z PELA CORRELAÇÃO DE BRILL E BEGGS>> {Z}'


def correlacao_de_Hall_Yarborough(Ppr, Tpr):
    """
    :param Ppr: Pressão pseudoreduzida [adimensional]
    :param Tpr: Temperatura pseudoreduzida [adimensional]
    :return: Fator de compressibilidade do gás
    """
    t = 1 / Tpr
    X1 = 0.06125 * t * M.exp(-1.2 * (1 - t)**2)
    X2 = 14.76 * t - 9.76 * t**2 + 4.58 * t**3
    X3 = 90.7 * t - 242.2 * t**2 + 42.4 * t**3
    X4 = 2.18 + (2.82 * t)

    # Definindo a função simbólica
    Y = Symbol('Y')
    fy = - X1 * Ppr + ((Y + Y**2 + Y**3 - Y**4) / (1 - Y)**3) - X2 * Y**2 + X3 * Y**X4
    derivada = fy.diff(Y)

    # Definindo a derivada numérica
    fderivada = lambdify(Y, derivada, 'sympy')

    # Transformando a função numericamente
    fy = lambda Y: - X1 * Ppr + ((Y + Y**2 + Y**3 - Y**4) / (1 - Y)**3) - X2 * Y**2 + X3 * Y**X4

    parad = 0.00000000001
    maxit = 50000
    iter = 0
    xr = 0.1  # 1ºchute

    while True:
        xold = xr
        xr = xr - ((fy(xr))/(fderivada(xr)))
        epest = abs((xold - xr)/xold) * 100
        if epest <= parad or iter >= maxit:
            break
    Z = (X1 * Ppr) / xr
    return f'FATOR Z PELA CORRELAÇÃO DE HALL-YARBOROUGH>> {Z}'


def correlacao_dranchukabukassem(Ppr, Tpr, zc, x0):
    """
    :param Ppr: Pressão pseudoreduzida [adimensional]
    :param Tpr: Temperatura pseudoreduzida [adimensional]
    :param zc: z crítico (metano)
    :param x0: Valor que zera função objetivo
    :return: Fator de compressibilidade do gás
    """
    A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11 = 0.3265, -1.0700, -0.5339, 0.01569, -0.05165, 0.5475, -0.7361, \
                                                   0.1844, 0.1056, 0.6134, 0.7210
    # Função Objetivo
    F = lambda z: 1 + (A1 + A2 / Tpr + A3 / Tpr ** 3 + A4 / Tpr ** 4 + A5 / Tpr ** 5) * ((zc * Ppr) / (z * Tpr)) + (
                A6 + A7 / Tpr + A8 / Tpr ** 2) * \
                  ((zc * Ppr) / (z * Tpr)) ** 2 - A9 * (A7 / Tpr + A8 / Tpr ** 2) * ((zc * Ppr) / (z * Tpr)) ** 5 + \
                  A10 * (1 + A11 * ((zc * Ppr) / (z * Tpr)) ** 2) * (
                              (((zc * Ppr) / (z * Tpr)) ** 2) * M.exp(-A11 * ((zc * Ppr) / (z * Tpr)) ** 2)) / (
                              Tpr ** 3) - z

    Pert = 10 ** -6
    Parad = 10 ** -11
    maxit = 50000
    iter = 0

    while True:
        iter += 1
        xold = x0
        x0 = xold - ((Pert * xold * F(xold)) / (F(xold + Pert * xold) - F(x0)))
        Erro = ((xold - x0) / xold) * 100
        if Erro <= Parad or iter >= maxit:
            break
    z = x0
    return f'FATOR Z PELA CORRELAÇÃO DE DRANCHUK & ABU-KASSEM>> {z}'
