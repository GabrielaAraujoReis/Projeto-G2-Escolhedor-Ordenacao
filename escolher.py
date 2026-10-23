"""Escolha automatica e execucao do metodo de ordenacao."""

from collections.abc import Callable

MetodoOrdenacao = Callable[[list[int]], list[int]]


def escolher(v: list[int]) -> MetodoOrdenacao:
    """Analisa a entrada e devolve a funcao de ordenacao escolhida.

    A implementacao final devera calcular tamanho, faixa e uma medida barata de
    desordem em uma unica passagem sempre que possivel.
    """
    raise NotImplementedError("Regras do escolhedor ainda nao definidas")


def ordenar(v: list[int]) -> list[int]:
    """Escolhe um metodo e retorna uma nova lista ordenada."""
    metodo = escolher(v)
    return metodo(v)

