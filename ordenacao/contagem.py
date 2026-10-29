"""Ordenação por contagem (encontro 13).

O valor de cada chave serve de endereço do seu contador: nenhuma chave é
comparada com outra. Custo O(n + k), onde k = máximo - mínimo + 1 é o
tamanho da faixa. Exige chaves inteiras.

O vetor de contadores tem o tamanho da *faixa*, não dos dados. Por isso
a função se recusa a alocar mais do que LIMITE_CONTADORES contadores:
com 10 mil números entre 0 e 10⁹ ela pediria ~8 GB só para os contadores.
Quem chama (o `escolher`) deve prever isso antes; a guarda aqui é a última
linha de defesa.

Valores negativos funcionam: o contador de x fica na posição x - mínimo.
"""

LIMITE_CONTADORES = 10_000_000  # ≈ 80 MB de ponteiros em CPython 64 bits
BYTES_POR_CONTADOR = 8


class FaixaGrandeDemais(MemoryError):
    """A faixa de valores exigiria contadores demais."""


def _milhar(x):
    return f"{x:,}".replace(",", ".")


def contagem(v, minimo=None, maximo=None, limite=LIMITE_CONTADORES):
    """Devolve uma nova lista ordenada; não altera `v`.

    `minimo` e `maximo` podem ser passados por quem já os calculou (o
    escolhedor), para não percorrer a lista de novo.
    """
    if len(v) < 2:
        return list(v)
    mn = min(v) if minimo is None else minimo
    mx = max(v) if maximo is None else maximo
    k = mx - mn + 1
    if k > limite:
        raise FaixaGrandeDemais(
            f"faixa de {_milhar(k)} valores exigiria ~{_milhar(k * BYTES_POR_CONTADOR // 2**20)} MB "
            f"de contadores (limite: {_milhar(limite)})"
        )

    cont = [0] * k
    if mn == 0:
        for x in v:
            cont[x] += 1
    else:
        for x in v:
            cont[x - mn] += 1

    saida = []
    despeja = saida.extend
    for i, c in enumerate(cont):
        if c:
            despeja([i + mn] * c)
    return saida
