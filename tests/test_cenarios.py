"""Testes dos geradores de entrada e do cronômetro."""

import unittest

from benchmarks.cenarios import (CENARIOS, aleatorio, quase_ordenado,
                                 quase_ordenado_trocas_distantes)
from benchmarks.cronometro import formata, medir


class TestCenarios(unittest.TestCase):
    def test_reprodutiveis(self):
        # mesma semente, mesma lista: todo mundo mede a mesma entrada
        for nome, c in CENARIOS.items():
            with self.subTest(cenario=nome):
                self.assertEqual(c["gerar"](), c["gerar"]())

    def test_faixas(self):
        v = aleatorio(1_000, 100)
        self.assertTrue(all(0 <= x <= 100 for x in v))

    def test_quase_ordenado_tem_desordem_local(self):
        v = quase_ordenado(5_000, fracao=0.01, distancia=10)
        ordenada = sorted(v)
        posicao = {}
        for i, x in enumerate(ordenada):
            posicao.setdefault(x, i)
        # ninguém longe do lugar certo (≤ 20: uma posição pode ser trocada
        # duas vezes, cada vez a até 10 posições)
        self.assertTrue(all(abs(i - posicao[x]) <= 20 for i, x in enumerate(v)))
        self.assertNotEqual(v, ordenada)

    def test_trocas_distantes_tem_mesma_quantidade_de_descidas(self):
        def descidas(v):
            return sum(a > b for a, b in zip(v, v[1:]))
        perto = descidas(quase_ordenado(10_000))
        longe = descidas(quase_ordenado_trocas_distantes(10_000))
        self.assertLess(abs(perto - longe), 0.5 * perto)


class TestCronometro(unittest.TestCase):
    def test_medir_devolve_tempo_positivo(self):
        self.assertGreater(medir(sorted, [3, 1, 2], tempo_min=0.01), 0)

    def test_formata(self):
        self.assertEqual(formata(0.0000015), "1,5 µs")
        self.assertEqual(formata(0.0123), "12,30 ms")
        self.assertEqual(formata(1.5), "1,50 s")


if __name__ == "__main__":
    unittest.main()
