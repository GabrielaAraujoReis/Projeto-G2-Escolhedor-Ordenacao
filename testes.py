"""Casos obrigatorios do Projeto G2."""

import unittest

from algoritmos import (
    ordenacao_base,
    ordenacao_contagem,
    ordenacao_hibrida,
    ordenacao_insercao,
    ordenacao_intercalacao,
    ordenacao_rapida,
)


ALGORITMOS = (
    ordenacao_insercao,
    ordenacao_intercalacao,
    ordenacao_rapida,
    ordenacao_hibrida,
    ordenacao_contagem,
    ordenacao_base,
)


@unittest.skip("Estrutura inicial: algoritmos ainda nao implementados")
class TesteMetodosDeOrdenacao(unittest.TestCase):
    """Aplica os mesmos casos obrigatorios a todos os metodos."""

    CASOS = (
        ([], []),
        ([7], [7]),
        ([4, 4, 4, 4], [4, 4, 4, 4]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([3, -1, 0, -5, 2], [-5, -1, 0, 2, 3]),
    )

    def test_casos_obrigatorios(self) -> None:
        for algoritmo in ALGORITMOS:
            for entrada, esperado in self.CASOS:
                with self.subTest(algoritmo=algoritmo.__name__, entrada=entrada):
                    original = entrada.copy()
                    self.assertEqual(algoritmo(entrada), esperado)
                    self.assertEqual(entrada, original)


if __name__ == "__main__":
    unittest.main(verbosity=2)

