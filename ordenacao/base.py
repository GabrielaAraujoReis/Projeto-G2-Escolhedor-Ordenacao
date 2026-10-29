"""Ordenação por base (radix sort, LSD), encontro 13.

Ordena um "dígito" por vez, do menos para o mais significativo. Cada
passada é uma ordenação por contagem *estável* sobre o dígito; é a
estabilidade que garante que a ordem das passadas anteriores sobrevive.

Usamos dígitos de 8 bits (base 256) em vez de dígitos decimais: a ideia é
a mesma do slide, mas uma chave de até 10⁹ precisa de 4 passadas em vez
de 10, e extrair o dígito é um deslocamento de bits em vez de divisão.

Custo: O(d · (n + 256)), com d = número de bytes da maior chave.
Valores negativos: subtraímos o mínimo de todas as chaves antes e somamos
de volta depois, para todas ficarem ≥ 0.
"""

BITS_POR_DIGITO = 8


def _passada_estavel(a, desloc, mascara, tam_base):
    digitos = [(x >> desloc) & mascara for x in a]

    cont = [0] * tam_base
    for d in digitos:
        cont[d] += 1

    # cont[d] passa a ser a primeira posição de saída do dígito d
    total = 0
    for d in range(tam_base):
        c = cont[d]
        cont[d] = total
        total += c

    # percorre na ordem original: empates mantêm a ordem anterior (estável)
    saida = [0] * len(a)
    for x, d in zip(a, digitos):
        saida[cont[d]] = x
        cont[d] += 1
    return saida


def passadas_necessarias(faixa, bits=BITS_POR_DIGITO):
    """Quantas passadas a base faz para chaves em [0, faixa]."""
    return max(1, -(-faixa.bit_length() // bits))


def base(v, minimo=None, maximo=None, bits=BITS_POR_DIGITO):
    """Devolve uma nova lista ordenada; não altera `v`."""
    if len(v) < 2:
        return list(v)
    mn = min(v) if minimo is None else minimo
    mx = max(v) if maximo is None else maximo

    a = [x - mn for x in v] if mn else list(v)
    maior = mx - mn
    tam_base = 1 << bits
    mascara = tam_base - 1

    desloc = 0
    while maior >> desloc:
        a = _passada_estavel(a, desloc, mascara, tam_base)
        desloc += bits

    return [x + mn for x in a] if mn else a
