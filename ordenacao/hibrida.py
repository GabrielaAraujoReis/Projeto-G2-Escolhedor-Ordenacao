"""Ordenação híbrida: rápida + inserção.

Enquanto o pedaço é grande, particiona como a ordenação rápida (pivô
aleatório, partição em três). Quando o pedaço fica com até LIMIAR_HIBRIDA
elementos, termina com inserção, que nesse tamanho é mais barata que
continuar recursando (menos chamadas de função, menos sorteios).

Custo esperado: O(n log n). Não é estável.
"""

from .rapida import particiona3

LIMIAR_HIBRIDA = 16


def _insercao_trecho(a, lo, hi):
    for i in range(lo + 1, hi + 1):
        x = a[i]
        j = i - 1
        while j >= lo and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


def _hibrida(a, lo, hi):
    while hi - lo + 1 > LIMIAR_HIBRIDA:
        lt, gt = particiona3(a, lo, hi)
        if lt - lo < hi - gt:
            _hibrida(a, lo, lt - 1)
            lo = gt + 1
        else:
            _hibrida(a, gt + 1, hi)
            hi = lt - 1
    _insercao_trecho(a, lo, hi)


def hibrida(v):
    """Devolve uma nova lista ordenada; não altera `v`."""
    a = list(v)
    _hibrida(a, 0, len(a) - 1)
    return a
