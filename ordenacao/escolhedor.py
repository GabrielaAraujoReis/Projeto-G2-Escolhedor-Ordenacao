"""O escolhedor: olha a lista e decide qual dos seis métodos usar.

Regras, em ordem (as mais baratas primeiro). Os números vêm de
`resultados/calibracao.md`, gerado por `python -m benchmarks.calibrar`.

  1. n ≤ 16                         → inserção      (calibração §1)
  2. descidas ≤ 5% de n              → inserção      (calibração §2)
  3. chaves inteiras e faixa ≤ 2·n   → contagem      (calibração §3)
     (e faixa ≤ LIMITE_CONTADORES, para nunca estourar a memória)
  4. chaves inteiras, n ≥ 256 e
     até 4 passadas (faixa < 2³²)    → base          (calibração §4)
  5. n < 1.000                       → híbrida       (calibração §4 e §5)
  6. senão                           → intercalação  (calibração §4 e §5)

Custo de olhar os dados: no pior caso quatro passadas pela lista (descidas,
mínimo, máximo, tipos), todas feitas por funções embutidas escritas em C.
A contagem de descidas para cedo quando a lista claramente não está quase
ordenada. Ver "Quanto custa o escolher" no RELATORIO.md.

`escolher` devolve uma `Escolha` com o nome do método, o motivo e uma
função pronta para executar. Quando já calculou mínimo e máximo, repassa
os dois para a contagem/base, que assim não percorrem a lista de novo.
"""

from functools import partial
from itertools import islice
from operator import gt
from typing import Callable, NamedTuple

from .base import base, passadas_necessarias
from .contagem import LIMITE_CONTADORES, contagem
from .hibrida import hibrida
from .insercao import insercao
from .intercalacao import intercalacao

# ---- limiares (ver resultados/calibracao.md) --------------------------
LIMIAR_MINUSCULA = 16        # §1: até aqui inserção ≈ híbrida (que É inserção
                             #     abaixo de 16) e as duas batem o resto
FRACAO_DESCIDAS = 0.05       # §2: virada observada ~30%; usamos 1/6 disso
                             #     como margem para desordem não local
FATOR_FAIXA_CONTAGEM = 2     # §3: contagem venceu em todo n com k ≤ 2n
N_MIN_BASE = 256             # §4: abaixo disso a base só ganha com 1 passada
MAX_PASSADAS_BASE = 4        # §4: até 4 passadas a base venceu em todo n ≥ 256
N_MAX_HIBRIDA = 1_000        # §4/§5: a híbrida ganha da intercalação só em n pequeno
TAMANHO_BLOCO = 1_024        # descidas são contadas em blocos (ver _conta_descidas)


class Escolha(NamedTuple):
    nome: str                       # um dos nomes de ordenacao.METODOS
    motivo: str                     # explicação legível da decisão
    executar: Callable[[list], list]


# Escolhas sem parâmetros são criadas uma vez só: no caso da lista
# minúscula, até montar a explicação custaria mais que ordenar.
_MINUSCULA = Escolha("insercao", f"lista minúscula (n ≤ {LIMIAR_MINUSCULA})", insercao)
_JA_ORDENADA = Escolha("insercao", "lista já ordenada (nenhuma descida)", insercao)


def _milhar(x):
    return f"{x:,}".replace(",", ".")


def _pct(x):
    return f"{x * 100:.1f} %".replace(".", ",")


def _so_inteiros(v):
    # bool é subclasse de int, mas não faz sentido ordenar por contagem;
    # por isso comparamos o tipo exato.
    return set(map(type, v)) == {int}


def _conta_descidas(v, limite):
    """Conta os pares v[i] > v[i+1], mas desiste assim que passar de `limite`.

    Numa lista desordenada metade dos pares é descida, então o limite de 5%
    estoura já no primeiro bloco e o resto da lista nem é olhado. Numa
    lista quase ordenada a contagem vai até o fim (e precisa ir).
    """
    n = len(v)
    passo = max(TAMANHO_BLOCO, n // 8)
    descidas = 0
    for ini in range(0, n - 1, passo):
        bloco = v[ini:ini + passo + 1]           # +1: o par que cruza a borda
        descidas += sum(map(gt, bloco, islice(bloco, 1, None)))
        if descidas > limite:
            break
    return descidas


def escolher(v):
    """Olha a lista `v` (sem alterá-la) e devolve a `Escolha` do método."""
    n = len(v)

    # 1. tamanho: O(1)
    if n <= LIMIAR_MINUSCULA:
        return _MINUSCULA

    # 2. desordem: conta descidas v[i] > v[i+1], em blocos, e para assim
    #    que passar do limite (lista desordenada: olha só ~1/8 dela)
    descidas = _conta_descidas(v, FRACAO_DESCIDAS * n)
    if descidas == 0:
        return _JA_ORDENADA
    if descidas <= FRACAO_DESCIDAS * n:
        return Escolha("insercao",
                       f"quase ordenada ({_milhar(descidas)} descidas = "
                       f"{_pct(descidas / n)} de n)",
                       insercao)

    # 3 e 4. faixa: mínimo e máximo (duas passadas, em C)
    mn, mx = min(v), max(v)
    if type(mn) is int and type(mx) is int and _so_inteiros(v):
        faixa = mx - mn + 1
        if faixa <= FATOR_FAIXA_CONTAGEM * n and faixa <= LIMITE_CONTADORES:
            return Escolha("contagem",
                           f"inteiros com faixa estreita (k = {_milhar(faixa)} ≤ "
                           f"{FATOR_FAIXA_CONTAGEM}·n)",
                           partial(contagem, minimo=mn, maximo=mx))
        passadas = passadas_necessarias(mx - mn)
        if n >= N_MIN_BASE and passadas <= MAX_PASSADAS_BASE:
            return Escolha("base",
                           f"inteiros com faixa larga (k = {_milhar(faixa)}), "
                           f"{passadas} passada(s) de 8 bits",
                           partial(base, minimo=mn, maximo=mx))

    # 5 e 6. comparação
    if n < N_MAX_HIBRIDA:
        return Escolha("hibrida", f"caso geral com n = {_milhar(n)} < {_milhar(N_MAX_HIBRIDA)}", hibrida)
    return Escolha("intercalacao", f"caso geral com n = {_milhar(n)} ≥ {_milhar(N_MAX_HIBRIDA)}", intercalacao)


def ordenar(v):
    """Ordena `v` com o método que `escolher` indicar. Devolve nova lista."""
    return escolher(v).executar(v)
