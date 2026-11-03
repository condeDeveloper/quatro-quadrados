# -*- coding: utf-8 -*-
"""O juiz: a forma fechada de Legendre.

O teorema dos tres quadrados diz que um numero NAO e soma de tres quadrados
se, e somente se, ele tem a forma

    4^a * (8b + 7)

Isso e uma formula, nao uma busca: tira os fatores quatro e olha o resto na
divisao por oito. Decide em microssegundos o que a busca decide em
milissegundos.

E ele nao e usado para calcular nada no modulo ``soma``. Ele existe aqui para
JULGAR a busca: se os dois discordam em um unico numero, um dos dois esta
errado.
"""


def forma_quatro_a_oito_b_mais_sete(n):
    """True se n se escreve como 4^a * (8b + 7)."""
    if n < 1:
        raise ValueError('n tem que ser positivo: %r' % (n,))
    while n % 4 == 0:
        n //= 4
    return n % 8 == 7


def expoente_de_quatro(n):
    """O a de 4^a na decomposicao, so para a tabela."""
    if n < 1:
        raise ValueError('n tem que ser positivo: %r' % (n,))
    a = 0
    while n % 4 == 0:
        n //= 4
        a += 1
    return a


def precisa_de_quatro(n):
    """True quando tres quadrados nao bastam, pela forma fechada."""
    return forma_quatro_a_oito_b_mais_sete(n)


def quantos_precisam_de_quatro_ate(limite):
    """Quantos numeros ate o limite tem a forma, contados pela formula."""
    return sum(1 for n in range(1, limite + 1) if forma_quatro_a_oito_b_mais_sete(n))


def densidade_prevista():
    """A fatia dos inteiros com a forma 4^a(8b+7), em forma fechada.

    Entre os impares, um em cada oito termina em 7 modulo 8. Somando as
    contribuicoes de cada potencia de quatro, a serie da 1/6.
    """
    return 1.0 / 6.0
