# -*- coding: utf-8 -*-
"""Roda as tabelas que vao para o README.

    python -m ferramentas.medidor
    python -m ferramentas.medidor --completo
"""
import sys
import time

from quadrados import legendre, soma, varredura

LIMITE = 20_000
LIMITE_JUIZ = 5_000
LIMITE_LAGRANGE = 400
LIMITE_COMPLETO = 200_000


def titulo(texto):
    print()
    print(texto)
    print('-' * len(texto))


def os_pequenos():
    titulo('Quantos quadrados cada numero precisa')
    print('%-8s %-10s %-22s %s' % ('n', 'minimo', 'uma representacao', 'forma 4^a(8b+7)?'))
    for n in range(1, 21):
        partes = soma.uma_representacao(n)
        texto = ' + '.join('%d^2' % x for x in partes)
        print('%-8d %-10d %-22s %s'
              % (n, soma.minimo_de_quadrados(n), texto,
                 'sim' if legendre.precisa_de_quatro(n) else ''))


def a_contagem():
    titulo('A conta ate %d' % LIMITE)
    conta = varredura.contagem_por_minimo(LIMITE)
    print('%-12s %-12s %s' % ('minimo', 'quantos', 'fatia'))
    for k in sorted(conta):
        print('%-12d %-12d %.4f%%' % (k, conta[k], 100.0 * conta[k] / LIMITE))
    print()
    print('total: %d' % sum(conta.values()))
    print('nenhum numero precisou de cinco. E isso e o teorema de Lagrange,')
    print('conferido numero a numero e nao assumido.')


def a_densidade():
    titulo('A fatia que precisa dos quatro, por faixa')
    print('%-24s %-12s %s' % ('faixa', 'quantos', 'fatia'))
    for baixo, alto, quantos, fatia in varredura.densidade_por_faixa(LIMITE, 10):
        print('%-24s %-12d %.5f' % ('%d a %d' % (baixo, alto), quantos, fatia))
    conta = varredura.contagem_por_minimo(LIMITE)
    print()
    print('no total        : %.6f' % (conta[4] / LIMITE))
    print('previsto por 1/6: %.6f' % legendre.densidade_prevista())
    print('diferenca       : %.6f' % abs(conta[4] / LIMITE - legendre.densidade_prevista()))


def os_expoentes():
    titulo('Entre os que precisam de quatro, o expoente de 4^a')
    conta = varredura.por_expoente_de_quatro(LIMITE)
    total = sum(conta.values())
    print('%-10s %-12s %s' % ('a', 'quantos', 'fatia'))
    for a in sorted(conta):
        print('%-10d %-12d %.4f%%' % (a, conta[a], 100.0 * conta[a] / total))
    print()
    print('Cada potencia de quatro contribui com um quarto da anterior.')
    print('Somando a serie 1/8 + 1/32 + 1/128 + ... da exatamente 1/6.')


def o_juiz():
    titulo('As tres conferencias')
    print('a busca x a forma fechada de Legendre: %d numeros conferidos'
          % varredura.conferir_contra_legendre(LIMITE_JUIZ))
    print('toda representacao soma mesmo o numero: %d conferidas'
          % varredura.conferir_representacoes(LIMITE_JUIZ))
    print('todo numero cabe em quatro quadrados  : %d conferidos por enumeracao'
          % varredura.conferir_lagrange(LIMITE_LAGRANGE))


def completo():
    titulo('Varredura ate %d' % LIMITE_COMPLETO)
    comeco = time.time()
    quantos = legendre.quantos_precisam_de_quatro_ate(LIMITE_COMPLETO)
    print('numeros que precisam de quatro quadrados: %d' % quantos)
    print('fatia                                   : %.6f' % (quantos / LIMITE_COMPLETO))
    print('previsto por 1/6                        : %.6f' % legendre.densidade_prevista())
    print('diferenca                               : %.6f'
          % abs(quantos / LIMITE_COMPLETO - legendre.densidade_prevista()))
    print()
    conferidos = varredura.conferir_contra_legendre(LIMITE_JUIZ)
    print('a busca e a formula concordaram em %d numeros' % conferidos)
    conta = varredura.por_expoente_de_quatro(LIMITE_COMPLETO)
    print()
    print('%-10s %-12s %s' % ('a', 'quantos', 'fatia'))
    total = sum(conta.values())
    for a in sorted(conta):
        print('%-10d %-12d %.4f%%' % (a, conta[a], 100.0 * conta[a] / total))
    print()
    print('tempo: %.1f s' % (time.time() - comeco))

    if abs(quantos / LIMITE_COMPLETO - 1.0 / 6.0) > 0.001:
        print('MEDIDA MUDOU: a fatia deveria estar a menos de 0,001 de 1/6')
        sys.exit(1)
    print('a fatia bateu com 1/6')


def main():
    if '--completo' in sys.argv:
        completo()
        return
    os_pequenos()
    a_contagem()
    a_densidade()
    os_expoentes()
    o_juiz()


if __name__ == '__main__':
    main()
