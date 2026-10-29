"""Ordenação rápida (quicksort) com pivô aleatório.

Custo esperado: O(n log n) para qualquer entrada, porque o pivô é sorteado
(nenhuma entrada específica é sempre ruim). Não é estável.

Usamos partição em três partes (menores | iguais | maiores), de Dijkstra.
Sem isso, uma lista com todos os valores iguais (ou uma faixa estreita,
com muitos repetidos) levaria a O(n²) e estouraria a pilha de recursão.
Também recursamos só no lado menor e iteramos no maior, o que limita a
profundidade da pilha a O(log n).
"""

import random

_sorteio = random.Random()


def particiona3(a, lo, hi):
    """Particiona a[lo..hi] em torno de um pivô sorteado.

    Ao final: a[lo..lt-1] < pivô, a[lt..gt] == pivô, a[gt+1..hi] > pivô.
    Devolve (lt, gt).
    """
    p = a[lo + int(_sorteio.random() * (hi - lo + 1))]
    lt, i, gt = lo, lo, hi
    while i <= gt:
        x = a[i]
        if x < p:
            a[lt], a[i] = x, a[lt]
            lt += 1
            i += 1
        elif p < x:
            a[i], a[gt] = a[gt], x
            gt -= 1
        else:
            i += 1
    return lt, gt


def _rapida(a, lo, hi):
    while lo < hi:
        lt, gt = particiona3(a, lo, hi)
        if lt - lo < hi - gt:
            _rapida(a, lo, lt - 1)
            lo = gt + 1
        else:
            _rapida(a, gt + 1, hi)
            hi = lt - 1


def rapida(v):
    """Devolve uma nova lista ordenada; não altera `v`."""
    a = list(v)
    _rapida(a, 0, len(a) - 1)
    return a
