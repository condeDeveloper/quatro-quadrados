# -*- coding: utf-8 -*-
"""Os numeros do README, presos. Todos sairam do medidor."""
import math
import unittest

from ferramentas import medidor
from quadrados import legendre, varredura


class TestMedidas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conta = varredura.contagem_por_minimo(medidor.LIMITE)

    def test_a_conta_ate_vinte_mil(self):
        self.assertEqual(self.conta[1], 141)
        self.assertEqual(self.conta[2], 5_117)
        self.assertEqual(self.conta[3], 11_411)
        self.assertEqual(self.conta[4], 3_331)
        self.assertEqual(sum(self.conta.values()), 20_000)

    def test_os_141_de_um_quadrado_sao_os_quadrados_perfeitos(self):
        self.assertEqual(self.conta[1], math.isqrt(medidor.LIMITE))
        self.assertEqual(141 * 141, 19_881)
        self.assertGreater(142 * 142, 20_000)

    def test_nenhum_numero_precisou_de_cinco(self):
        self.assertNotIn(5, self.conta)
        self.assertEqual(max(self.conta), 4)

    def test_a_fatia_de_quatro_e_um_sexto(self):
        fatia = self.conta[4] / medidor.LIMITE
        self.assertAlmostEqual(fatia, 0.166550, places=6)
        self.assertAlmostEqual(legendre.densidade_prevista(), 1 / 6, places=10)
        self.assertLess(abs(fatia - 1 / 6), 0.0002)

    def test_a_fatia_ja_nasce_em_um_sexto_e_nao_converge(self):
        faixas = varredura.densidade_por_faixa(medidor.LIMITE, 10)
        for baixo, alto, quantos, fatia in faixas:
            self.assertLess(abs(fatia - 1 / 6), 0.002, 'faixa %d a %d' % (baixo, alto))
        self.assertAlmostEqual(faixas[0][3], 0.16600, places=5)
        self.assertAlmostEqual(faixas[-1][3], 0.16700, places=5)

    def test_cada_potencia_de_quatro_contribui_um_quarto_da_anterior(self):
        conta = varredura.por_expoente_de_quatro(medidor.LIMITE)
        self.assertEqual(conta[0], 2_500)
        self.assertEqual(conta[1], 625)
        self.assertEqual(conta[2], 156)
        self.assertEqual(conta[3], 39)
        self.assertEqual(conta[4], 9)
        self.assertEqual(conta[5], 2)
        self.assertEqual(conta[0] // 4, conta[1])
        self.assertEqual(conta[1] // 4, conta[2])
        self.assertEqual(conta[2] // 4, conta[3])

    def test_a_soma_dos_expoentes_e_o_total_de_quatro(self):
        conta = varredura.por_expoente_de_quatro(medidor.LIMITE)
        self.assertEqual(sum(conta.values()), self.conta[4])

    def test_as_tres_conferencias(self):
        self.assertEqual(
            varredura.conferir_contra_legendre(medidor.LIMITE_JUIZ), 5_000)
        self.assertEqual(
            varredura.conferir_representacoes(medidor.LIMITE_JUIZ), 5_000)
        self.assertEqual(
            varredura.conferir_lagrange(medidor.LIMITE_LAGRANGE), 400)


if __name__ == '__main__':
    unittest.main()
