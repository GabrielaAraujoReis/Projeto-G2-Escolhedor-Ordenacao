"""Ordenação por inserção.

Custo: O(n + I), onde I é o número de inversões da entrada.
Por isso é ótima em listas minúsculas e em listas quase ordenadas,
e péssima (O(n²)) em listas aleatórias grandes. É estável.
"""


def insercao(v):
    """Devolve uma nova lista ordenada; não altera `v`."""
    a = list(v)
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return a
