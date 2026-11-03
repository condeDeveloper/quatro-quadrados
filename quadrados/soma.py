# -*- coding: utf-8 -*-
"""O teorema dos quatro quadrados de Lagrange.

Todo inteiro positivo e soma de no maximo QUATRO quadrados. Nao tres, nao
cinco: quatro, e isso vale para todo numero, sem excecao.

    7  = 4 + 1 + 1 + 1          precisa dos quatro
    6  = 4 + 1 + 1              tres bastam
    5  = 4 + 1                  dois bastam
    9  = 9                      um basta

A pergunta interessante nao e se quatro bastam — isso Lagrange provou em 1770.
E QUANTOS numeros realmente precisam dos quatro. A resposta tem forma fechada,
pelo teorema dos tres quadrados de Legendre: um numero precisa de quatro
quadrados se, e somente se, ele se escreve como

    4^a * (8b + 7)

Este repositorio nao usa essa formula para decidir nada. Ele VARRE, acha o
minimo de quadrados de cada numero por busca, e depois compara o resultado com
a formula — que e o juiz, e nao o metodo.
"""
import math


def eh_quadrado(n):
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def minimo_de_quadrados(n):
    """Quantos quadrados, no minimo, somam n. Achado por busca, nao por formula."""
    if n < 1:
        raise ValueError('n tem que ser positivo: %r' % (n,))
    if eh_quadrado(n):
        return 1
    # dois
    a = 1
    while a * a <= n:
        if eh_quadrado(n - a * a):
            return 2
        a += 1
    # tres
    a = 1
    while a * a <= n:
        b = a
        while a * a + b * b <= n:
            if eh_quadrado(n - a * a - b * b):
                return 3
            b += 1
        a += 1
    # Lagrange garante que nunca passa daqui
    return 4


def uma_representacao(n):
    """Uma lista de quadrados que soma n, com o menor tamanho possivel."""
    if n < 1:
        raise ValueError('n tem que ser positivo: %r' % (n,))
    if eh_quadrado(n):
        return [math.isqrt(n)]
    a = 1
    while a * a <= n:
        if eh_quadrado(n - a * a):
            return sorted([a, math.isqrt(n - a * a)], reverse=True)
        a += 1
    a = 1
    while a * a <= n:
        b = a
        while a * a + b * b <= n:
            resto = n - a * a - b * b
            if eh_quadrado(resto):
                return sorted([a, b, math.isqrt(resto)], reverse=True)
            b += 1
        a += 1
    a = 1
    while a * a <= n:
        b = a
        while a * a + b * b <= n:
            c = b
            while a * a + b * b + c * c <= n:
                resto = n - a * a - b * b - c * c
                if eh_quadrado(resto):
                    return sorted([a, b, c, math.isqrt(resto)], reverse=True)
                c += 1
            b += 1
        a += 1
    raise AssertionError('Lagrange falhou em %d, o que e impossivel' % n)


def todas_as_representacoes(n, quantidade):
    """Todas as maneiras de escrever n como soma de ``quantidade`` quadrados.

    Os termos vem em ordem nao crescente, e o zero e permitido para que
    "ate k quadrados" e "exatamente k" sejam a mesma pergunta.
    """
    if n < 0 or quantidade < 1:
        raise ValueError('entrada invalida: %r, %r' % (n, quantidade))
    achadas = []

    def descer(resto, restantes, teto, atual):
        if restantes == 0:
            if resto == 0:
                achadas.append(list(atual))
            return
        maior = math.isqrt(resto)
        for x in range(min(teto, maior), -1, -1):
            if x * x * restantes < resto:
                break
            atual.append(x)
            descer(resto - x * x, restantes - 1, x, atual)
            atual.pop()

    descer(n, quantidade, math.isqrt(n), [])
    return achadas
