"""Testes específicos da contagem e da base."""

import unittest

from ordenacao.base import _passada_estavel, base, passadas_necessarias
from ordenacao.contagem import FaixaGrandeDemais, contagem


class TestContagem(unittest.TestCase):
    def test_recusa_faixa_grande_antes_de_alocar(self):
        # 10⁹ contadores seriam ~8 GB; a função tem de recusar sem tentar.
        with self.assertRaises(FaixaGrandeDemais):
            contagem([0, 10**9])

    def test_faixa_grande_e_um_memory_error(self):
        # quem já trata MemoryError não precisa conhecer a exceção nova
        with self.assertRaises(MemoryError):
            contagem([0, 10**12])

    def test_limite_configuravel(self):
        self.assertEqual(contagem([5, 1, 3], limite=5), [1, 3, 5])
        with self.assertRaises(FaixaGrandeDemais):
            contagem([5, 1, 3], limite=4)

    def test_aceita_minimo_e_maximo_calculados_fora(self):
        v = [4, -2, 9, -2]
        self.assertEqual(contagem(v, minimo=-2, maximo=9), sorted(v))

    def test_rejeita_reais(self):
        with self.assertRaises(TypeError):
            contagem([1.5, 0.5, 2.0])

    def test_faixa_negativa(self):
        v = [-10, -3, -10, -7, -1]
        self.assertEqual(contagem(v), sorted(v))


class TestBase(unittest.TestCase):
    def test_passada_e_estavel(self):
        # Mesmo byte menos significativo (0x01), bytes altos diferentes e em
        # ordem: depois da passada no byte baixo, a ordem relativa tem de
        # ser a mesma da entrada.
        v = [0x0301, 0x0101, 0x0201, 0x0005]
        saida = _passada_estavel(v, 0, 0xFF, 256)
        self.assertEqual(saida, [0x0301, 0x0101, 0x0201, 0x0005])

    def test_passadas_necessarias(self):
        self.assertEqual(passadas_necessarias(0), 1)
        self.assertEqual(passadas_necessarias(255), 1)
        self.assertEqual(passadas_necessarias(256), 2)
        self.assertEqual(passadas_necessarias(10**9), 4)
        self.assertEqual(passadas_necessarias(2**64 - 1), 8)

    def test_chaves_muito_grandes(self):
        v = [2**100, 3, 2**64, -(2**70), 0]
        self.assertEqual(base(v), sorted(v))

    def test_faixa_enorme_nao_usa_memoria_proporcional(self):
        # onde a contagem desiste, a base resolve
        v = [10**9, 0, 5 * 10**8, 3]
        self.assertEqual(base(v), sorted(v))

    def test_rejeita_reais(self):
        with self.assertRaises(TypeError):
            base([1.5, 0.5, 2.0])


if __name__ == "__main__":
    unittest.main()
