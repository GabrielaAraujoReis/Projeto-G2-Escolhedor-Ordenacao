"""Geradores de entrada, todos com semente fixa (reprodutíveis).

Os quatro cenários pedidos no enunciado estão em CENARIOS.
"""

import random

N_PADRAO = 10_000  # o mesmo n dos slides do encontro 13
_N = f"{N_PADRAO:,}".replace(",", ".")


def aleatorio(n, maximo, minimo=0, semente=1):
    r = random.Random(semente)
    return [r.randint(minimo, maximo) for _ in range(n)]


def quase_ordenado(n, fracao=0.01, distancia=10, maximo=10**9, semente=2):
    """Lista ordenada em que `fracao` das posições trocou de lugar com um
    vizinho a no máximo `distancia` posições. Modela dados que já vêm
    praticamente em ordem (um registro de eventos com pequenos atrasos,
    uma planilha que alguém editou à mão)."""
    r = random.Random(semente)
    v = sorted(r.randint(0, maximo) for _ in range(n))
    for _ in range(int(n * fracao)):
        i = r.randrange(n)
        j = min(n - 1, i + r.randint(1, distancia))
        v[i], v[j] = v[j], v[i]
    return v


def quase_ordenado_trocas_distantes(n, fracao=0.01, maximo=10**9, semente=3):
    """Lista ordenada em que `fracao` das posições trocou de lugar com uma
    posição *qualquer* da lista. Usada no cenário em que o escolhedor erra."""
    r = random.Random(semente)
    v = sorted(r.randint(0, maximo) for _ in range(n))
    for _ in range(int(n * fracao)):
        i, j = r.randrange(n), r.randrange(n)
        v[i], v[j] = v[j], v[i]
    return v


CENARIOS = {
    "aleatorio_chaves_grandes": {
        "titulo": "Aleatório, chaves grandes",
        "descricao": f"{_N} inteiros sorteados entre 0 e 10⁹",
        "gerar": lambda: aleatorio(N_PADRAO, 10**9),
    },
    "faixa_estreita": {
        "titulo": "Faixa estreita",
        "descricao": f"{_N} notas sorteadas entre 0 e 100",
        "gerar": lambda: aleatorio(N_PADRAO, 100),
    },
    "quase_ordenado": {
        "titulo": "Quase ordenado",
        "descricao": (
            f"{_N} inteiros entre 0 e 10⁹, ordenados, com 1% das posições "
            "trocadas com um vizinho a até 10 posições"
        ),
        "gerar": lambda: quase_ordenado(N_PADRAO),
    },
    "minuscula": {
        "titulo": "Lista minúscula",
        "descricao": "10 inteiros sorteados entre 0 e 1.000",
        "gerar": lambda: aleatorio(10, 1000),
    },
}
