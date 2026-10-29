"""Testes do escolher/ordenar."""

import random
import unittest

from benchmarks.cenarios import CENARIOS, quase_ordenado
from ordenacao import METODOS, escolher, ordenar
from ordenacao.escolhedor import LIMIAR_MINUSCULA
from tests.casos import CASOS_LIMITE, listas_aleatorias


class TestOrdenar(unittest.TestCase):
    def test_casos_limite(self):
        for caso, v in CASOS_LIMITE.items():
            with self.subTest(caso=caso):
                self.assertEqual(ordenar(v), sorted(v))

    def test_aleatorios(self):
        for v in listas_aleatorias(quantidade=400, semente=9):
            self.assertEqual(ordenar(v), sorted(v))

    def test_nao_altera_a_entrada(self):
        v = [5, 3, 1, 4] * 100
        copia = list(v)
        ordenar(v)
        self.assertEqual(v, copia)

    def test_tipos_nao_inteiros(self):
        r = random.Random(4)
        casos = {
            "reais": [r.random() for _ in range(3_000)],
            "textos": [str(r.random()) for _ in range(3_000)],
            "int e float misturados": [r.choice([1, 2.5, -3, 7.25]) for _ in range(3_000)],
            "booleanos": [r.choice([True, False]) for _ in range(3_000)],
        }
        for nome, v in casos.items():
            with self.subTest(caso=nome):
                self.assertEqual(ordenar(v), sorted(v))


class TestDecisoes(unittest.TestCase):
    def test_nome_sempre_e_um_dos_seis(self):
        for v in listas_aleatorias(quantidade=100, semente=2):
            self.assertIn(escolher(v).nome, METODOS)

    def test_cenarios_do_enunciado(self):
        esperado = {
            "aleatorio_chaves_grandes": "base",
            "faixa_estreita": "contagem",
            "quase_ordenado": "insercao",
            "minuscula": "insercao",
        }
        for cenario, metodo in esperado.items():
            with self.subTest(cenario=cenario):
                self.assertEqual(escolher(CENARIOS[cenario]["gerar"]()).nome, metodo)

    def test_minuscula(self):
        self.assertEqual(escolher(list(range(LIMIAR_MINUSCULA, 0, -1))).nome, "insercao")

    def test_ja_ordenada_e_todos_iguais(self):
        self.assertEqual(escolher(list(range(5_000))).nome, "insercao")
        self.assertEqual(escolher([3] * 5_000).nome, "insercao")

    def test_nunca_escolhe_contagem_com_faixa_grande(self):
        # o aviso do enunciado: prever o estouro ANTES de chamar a contagem
        r = random.Random(8)
        for maximo in (10**7, 10**9, 10**15, 10**40):
            v = [r.randint(0, maximo) for _ in range(5_000)]
            with self.subTest(maximo=maximo):
                self.assertNotEqual(escolher(v).nome, "contagem")
                self.assertEqual(ordenar(v), sorted(v))

    def test_chaves_maiores_que_32_bits_vao_para_comparacao(self):
        r = random.Random(6)
        v = [r.randint(0, 2**64) for _ in range(5_000)]
        self.assertEqual(escolher(v).nome, "intercalacao")

    def test_reais_nunca_vao_para_contagem_ou_base(self):
        v = [float(x) for x in range(1_000, 0, -1)]
        self.assertIn(escolher(v).nome, {"hibrida", "intercalacao"})

    def test_quase_ordenado_decrescente_nao_e_quase_ordenado(self):
        self.assertNotEqual(escolher(list(range(5_000, 0, -1))).nome, "insercao")

    def test_motivo_e_legivel(self):
        e = escolher(quase_ordenado(10_000))
        self.assertIn("quase ordenada", e.motivo)


if __name__ == "__main__":
    unittest.main()
