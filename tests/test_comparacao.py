"""Testes específicos dos métodos por comparação."""

import unittest

from ordenacao.insercao import insercao
from ordenacao.intercalacao import intercalacao


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


if __name__ == "__main__":
    unittest.main()
