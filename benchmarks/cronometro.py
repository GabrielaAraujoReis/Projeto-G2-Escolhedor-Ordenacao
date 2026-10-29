"""Cronometragem com o mínimo de ruído possível em Python puro.

- desliga o coletor de lixo durante a medição (como faz o `timeit`);
- se uma chamada for rápida demais para o relógio (< 2 ms), executa um
  *lote* de chamadas seguidas e divide o tempo pelo tamanho do lote;
- repete até juntar pelo menos `repeticoes_min` amostras e `tempo_min`
  segundos, e devolve a *mediana*, que é menos sensível a picos do
  sistema operacional do que a média.
"""

import gc
import statistics
from time import perf_counter

ALVO_POR_AMOSTRA = 0.002  # s


def _cronometra_lote(funcao, dados, lote):
    t0 = perf_counter()
    for _ in range(lote):
        funcao(dados)
    return (perf_counter() - t0) / lote


def medir(funcao, dados, repeticoes_min=5, repeticoes_max=30, tempo_min=0.3):
    """Mediana do tempo (em segundos) de uma chamada `funcao(dados)`."""
    gc_estava_ligado = gc.isenabled()
    gc.disable()
    try:
        # aquecimento + estimativa do tamanho do lote
        t = _cronometra_lote(funcao, dados, 1)
        lote = 1 if t >= ALVO_POR_AMOSTRA else max(1, int(ALVO_POR_AMOSTRA / max(t, 1e-7)))

        amostras = []
        gasto = 0.0
        while len(amostras) < repeticoes_min or (
            gasto < tempo_min and len(amostras) < repeticoes_max
        ):
            a = _cronometra_lote(funcao, dados, lote)
            amostras.append(a)
            gasto += a * lote
        return statistics.median(amostras)
    finally:
        if gc_estava_ligado:
            gc.enable()


def formata(segundos):
    """Formata um tempo de forma legível (µs, ms ou s), com vírgula decimal."""
    if segundos < 1e-3:
        txt = f"{segundos * 1e6:.1f} µs"
    elif segundos < 1:
        txt = f"{segundos * 1e3:.2f} ms" if segundos < 0.1 else f"{segundos * 1e3:.0f} ms"
    else:
        txt = f"{segundos:.2f} s"
    return txt.replace(".", ",")
