"""Casos de teste compartilhados por todos os arquivos de teste."""

import random

# Casos-limite exigidos no enunciado. Cada um aparece em dois tamanhos:
# pequeno (cai na regra "lista minúscula" do escolhedor) e grande (força o
# escolhedor a passar pelas outras regras).
CASOS_LIMITE = {
    "vazia": [],
    "um elemento": [42],
    "todos iguais (pequena)": [7] * 10,
    "todos iguais (grande)": [7] * 2_000,
    "já ordenada (pequena)": list(range(10)),
    "já ordenada (grande)": list(range(2_000)),
    "invertida (pequena)": list(range(10, 0, -1)),
    "invertida (grande)": list(range(2_000, 0, -1)),
    "negativos (pequena)": [3, -1, -7, 0, 12, -7, 5, -100],
    "negativos (grande)": random.Random(1).choices(range(-5_000, 5_000), k=2_000),
    "só negativos": [-5, -1, -300, -2, -1],
    "dois elementos fora de ordem": [2, 1],
    "chaves enormes": [10**30, -(10**30), 0, 10**18, -1, 10**30],
}


def listas_aleatorias(quantidade=200, semente=0):
    """Listas de tamanho e faixa variados, para comparar com sorted()."""
    r = random.Random(semente)
    for _ in range(quantidade):
        n = r.choice([0, 1, 2, 3, 10, 25, 100, 300, 1_500])
        expoente = r.randint(0, 12)
        yield [r.randint(-(10**expoente), 10**expoente) for _ in range(n)]
