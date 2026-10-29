"""Testes comuns a todos os métodos registrados em ordenacao.METODOS."""

import random
import unittest

from ordenacao import METODOS
from tests.casos import CASOS_LIMITE, listas_aleatorias

# contagem e base só aceitam inteiros
SO_INTEIROS = {"contagem", "base"}
POR_COMPARACAO = {nome: f for nome, f in METODOS.items() if nome not in SO_INTEIROS}

# A contagem recusa faixas grandes de propósito (ver test_contagem_base.py).
# Nos testes genéricos, para faixas acima disto, exigimos a recusa em vez do
# resultado. O valor é menor que o limite real só para os testes serem rápidos.
FAIXA_MAX_CONTAGEM_NOS_TESTES = 1_000_000


def confere(teste, nome, ordena, v):
    if nome == "contagem" and v and max(v) - min(v) + 1 > FAIXA_MAX_CONTAGEM_NOS_TESTES:
        with teste.assertRaises(MemoryError):
            ordena(v, limite=FAIXA_MAX_CONTAGEM_NOS_TESTES)
    else:
        teste.assertEqual(ordena(v), sorted(v))


class TestCasosLimite(unittest.TestCase):
    def test_casos_limite(self):
        for nome, ordena in METODOS.items():
            for caso, v in CASOS_LIMITE.items():
                with self.subTest(metodo=nome, caso=caso):
                    confere(self, nome, ordena, v)

    def test_nao_altera_a_entrada(self):
        for nome, ordena in METODOS.items():
            v = [5, 3, -1, 3, 9, 0]
            copia = list(v)
            with self.subTest(metodo=nome):
                resultado = ordena(v)
                self.assertEqual(v, copia)
                self.assertIsNot(resultado, v)

    def test_devolve_lista(self):
        for nome, ordena in METODOS.items():
            with self.subTest(metodo=nome):
                self.assertIsInstance(ordena((3, 1, 2)), list)


class TestAleatorios(unittest.TestCase):
    def test_contra_sorted(self):
        for nome, ordena in METODOS.items():
            for v in listas_aleatorias():
                with self.subTest(metodo=nome, n=len(v)):
                    confere(self, nome, ordena, v)


class TestChavesNaoInteiras(unittest.TestCase):
    def test_reais(self):
        r = random.Random(3)
        v = [r.uniform(-1e6, 1e6) for _ in range(500)]
        for nome, ordena in POR_COMPARACAO.items():
            with self.subTest(metodo=nome):
                self.assertEqual(ordena(v), sorted(v))

    def test_textos(self):
        v = ["pera", "uva", "abacate", "Banana", "uva", "", "maçã"]
        for nome, ordena in POR_COMPARACAO.items():
            with self.subTest(metodo=nome):
                self.assertEqual(ordena(v), sorted(v))


if __name__ == "__main__":
    unittest.main()
