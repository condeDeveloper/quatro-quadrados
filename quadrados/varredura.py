# -*- coding: utf-8 -*-
"""Varre os inteiros medindo quantos quadrados cada um precisa."""
from . import legendre, soma


def minimos_ate(limite):
    """O minimo de quadrados de cada n de 1 ate o limite."""
    if limite < 1:
        raise ValueError('limite tem que ser positivo: %r' % (limite,))
    return [soma.minimo_de_quadrados(n) for n in range(1, limite + 1)]


def contagem_por_minimo(limite):
    """Quantos numeros precisam de 1, 2, 3 e 4 quadrados."""
    conta = {1: 0, 2: 0, 3: 0, 4: 0}
    for k in minimos_ate(limite):
        conta[k] += 1
    return conta


def conferir_contra_legendre(limite):
    """Confere a busca contra a forma fechada, numero a numero.

    Devolve quantos numeros foram conferidos.
    """
    conferidos = 0
    for n in range(1, limite + 1):
        pela_busca = soma.minimo_de_quadrados(n) == 4
        pela_formula = legendre.precisa_de_quatro(n)
        if pela_busca != pela_formula:
            raise AssertionError(
                'discordaram em %d: a busca diz %s, Legendre diz %s'
                % (n, pela_busca, pela_formula))
        conferidos += 1
    return conferidos


def conferir_representacoes(limite):
    """Confere que a representacao devolvida realmente soma o numero.

    Devolve quantos numeros foram conferidos.
    """
    conferidos = 0
    for n in range(1, limite + 1):
        partes = soma.uma_representacao(n)
        if sum(x * x for x in partes) != n:
            raise AssertionError('a representacao de %d nao soma: %r' % (n, partes))
        if len(partes) != soma.minimo_de_quadrados(n):
            raise AssertionError(
                'a representacao de %d tem %d partes e o minimo e %d'
                % (n, len(partes), soma.minimo_de_quadrados(n)))
        if len(partes) > 4:
            raise AssertionError('Lagrange falhou em %d' % n)
        conferidos += 1
    return conferidos


def conferir_lagrange(limite):
    """Confere que TODO numero ate o limite cabe em quatro quadrados.

    Usa a enumeracao de representacoes, que nao sabe nada do teorema.
    """
    conferidos = 0
    for n in range(1, limite + 1):
        if not soma.todas_as_representacoes(n, 4):
            raise AssertionError('%d nao e soma de quatro quadrados' % n)
        conferidos += 1
    return conferidos


def densidade_por_faixa(limite, faixas=10):
    """A fatia que precisa de quatro quadrados, por faixa."""
    tamanho = limite // faixas
    linhas = []
    for f in range(faixas):
        baixo = f * tamanho + 1
        alto = baixo + tamanho - 1
        quantos = sum(1 for n in range(baixo, alto + 1)
                      if legendre.precisa_de_quatro(n))
        linhas.append((baixo, alto, quantos, quantos / tamanho))
    return linhas


def por_expoente_de_quatro(limite):
    """Entre os que precisam de quatro, quantos tem cada expoente a."""
    conta = {}
    for n in range(1, limite + 1):
        if legendre.precisa_de_quatro(n):
            a = legendre.expoente_de_quatro(n)
            conta[a] = conta.get(a, 0) + 1
    return conta


def quantidade_de_representacoes(limite, partes=4):
    """Quantas maneiras cada numero tem de virar soma de ``partes`` quadrados."""
    return [(n, len(soma.todas_as_representacoes(n, partes)))
            for n in range(1, limite + 1)]
