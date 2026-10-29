"""Testes específicos dos métodos por comparação."""

import sys
import unittest

from ordenacao.hibrida import LIMIAR_HIBRIDA, hibrida
from ordenacao.insercao import insercao
from ordenacao.intercalacao import intercalacao
from ordenacao.rapida import rapida


class Registro:
    """Chave + rótulo, comparado só pela chave (para testar estabilidade)."""

    def __init__(self, chave, rotulo):
        self.chave, self.rotulo = chave, rotulo

    def __lt__(self, outro):
        return self.chave < outro.chave

    def __gt__(self, outro):
        return self.chave > outro.chave


class TestEstabilidade(unittest.TestCase):
    def test_insercao_e_intercalacao_sao_estaveis(self):
        dados = [Registro(c, i) for i, c in enumerate([3, 1, 3, 2, 1, 3, 2, 1])]
        for ordena in (insercao, intercalacao):
            with self.subTest(metodo=ordena.__name__):
                saida = ordena(dados)
                for a, b in zip(saida, saida[1:]):
                    if a.chave == b.chave:
                        self.assertLess(a.rotulo, b.rotulo)


class TestRapida(unittest.TestCase):
    def test_todos_iguais_nao_estoura_a_pilha(self):
        # Sem a partição em três, isto seria O(n²) e passaria do limite de
        # recursão do Python.
        n = sys.getrecursionlimit() * 20
        for ordena in (rapida, hibrida):
            with self.subTest(metodo=ordena.__name__):
                self.assertEqual(ordena([1] * n), [1] * n)

    def test_ja_ordenada_grande(self):
        # Com pivô fixo no primeiro elemento isto seria O(n²).
        v = list(range(50_000))
        self.assertEqual(rapida(v), v)
        self.assertEqual(hibrida(v), v)


class TestHibrida(unittest.TestCase):
    def test_tamanhos_em_volta_do_limiar(self):
        for n in range(LIMIAR_HIBRIDA - 3, LIMIAR_HIBRIDA + 4):
            v = list(range(n, 0, -1))
            with self.subTest(n=n):
                self.assertEqual(hibrida(v), sorted(v))


if __name__ == "__main__":
    unittest.main()
