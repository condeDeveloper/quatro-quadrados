# -*- coding: utf-8 -*-
import math
import unittest

from quadrados import legendre, soma


class TestSoma(unittest.TestCase):

    def test_os_minimos_dos_primeiros(self):
        esperado = [1, 2, 3, 1, 2, 3, 4, 2, 1, 2, 3, 3, 2, 3, 4, 1, 2, 2, 3, 2]
        for n, k in enumerate(esperado, start=1):
            self.assertEqual(soma.minimo_de_quadrados(n), k, 'n = %d' % n)

    def test_quadrado_perfeito_precisa_de_um_so(self):
        for r in range(1, 40):
            self.assertEqual(soma.minimo_de_quadrados(r * r), 1, 'r = %d' % r)

    def test_o_sete_precisa_dos_quatro(self):
        self.assertEqual(soma.minimo_de_quadrados(7), 4)
        self.assertEqual(soma.uma_representacao(7), [2, 1, 1, 1])
        self.assertEqual(4 + 1 + 1 + 1, 7)

    def test_toda_representacao_soma_o_numero(self):
        for n in range(1, 600):
            partes = soma.uma_representacao(n)
            self.assertEqual(sum(x * x for x in partes), n, 'n = %d' % n)
            self.assertEqual(len(partes), soma.minimo_de_quadrados(n), 'n = %d' % n)

    def test_lagrange_vale_em_todo_numero_ate_600(self):
        for n in range(1, 601):
            self.assertLessEqual(soma.minimo_de_quadrados(n), 4, 'n = %d' % n)
            self.assertTrue(soma.todas_as_representacoes(n, 4), 'n = %d' % n)

    def test_eh_quadrado(self):
        self.assertTrue(soma.eh_quadrado(0))
        self.assertTrue(soma.eh_quadrado(144))
        self.assertFalse(soma.eh_quadrado(145))
        self.assertFalse(soma.eh_quadrado(-4))
        # grande o bastante para o float errar
        gigante = 10 ** 20
        self.assertTrue(soma.eh_quadrado(gigante))
        self.assertFalse(soma.eh_quadrado(gigante + 1))

    def test_todas_as_representacoes_sao_validas(self):
        for n in range(1, 60):
            for partes in soma.todas_as_representacoes(n, 4):
                self.assertEqual(sum(x * x for x in partes), n)
                self.assertEqual(len(partes), 4)
                self.assertEqual(partes, sorted(partes, reverse=True))

    def test_a_forma_de_legendre(self):
        for n in (7, 15, 23, 28, 31, 39, 47, 55, 60, 63):
            self.assertTrue(legendre.forma_quatro_a_oito_b_mais_sete(n), n)
        for n in (1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16):
            self.assertFalse(legendre.forma_quatro_a_oito_b_mais_sete(n), n)

    def test_o_expoente_de_quatro(self):
        self.assertEqual(legendre.expoente_de_quatro(7), 0)
        self.assertEqual(legendre.expoente_de_quatro(28), 1)
        self.assertEqual(legendre.expoente_de_quatro(112), 2)
        self.assertEqual(legendre.expoente_de_quatro(448), 3)

    def test_entrada_invalida_e_recusada(self):
        with self.assertRaises(ValueError):
            soma.minimo_de_quadrados(0)
        with self.assertRaises(ValueError):
            soma.uma_representacao(-1)
        with self.assertRaises(ValueError):
            legendre.forma_quatro_a_oito_b_mais_sete(0)


if __name__ == '__main__':
    unittest.main()
