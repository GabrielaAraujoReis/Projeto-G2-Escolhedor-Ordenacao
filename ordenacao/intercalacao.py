"""Ordenação por intercalação (merge sort), de cima para baixo.

Custo: O(n log n) em qualquer entrada, com O(n) de memória extra.
É estável: em caso de empate, o elemento da metade esquerda sai primeiro.
"""


def _intercala(esq, dir_):
    res = []
    i = j = 0
    ne, nd = len(esq), len(dir_)
    while i < ne and j < nd:
        if dir_[j] < esq[i]:
            res.append(dir_[j])
            j += 1
        else:
            res.append(esq[i])
            i += 1
    if i < ne:
        res.extend(esq[i:])
    if j < nd:
        res.extend(dir_[j:])
    return res


def intercalacao(v):
    """Devolve uma nova lista ordenada; não altera `v`."""
    n = len(v)
    if n <= 1:
        return list(v)
    m = n // 2
    return _intercala(intercalacao(v[:m]), intercalacao(v[m:]))
