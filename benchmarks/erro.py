"""Um cenário em que o `escolher` toma a decisão errada.

A regra "poucas descidas → inserção" foi calibrada com desordem *local*
(cada elemento fora do lugar está a poucas posições de onde deveria estar).
Aqui cada troca é entre duas posições quaisquer da lista. O número de
descidas continua pequeno (cada troca cria no máximo 4), então o escolhedor
continua achando que a lista está "quase ordenada"; mas cada elemento
deslocado precisa andar, em média, n/3 posições, e a inserção, que custa
O(n + inversões), vira praticamente quadrática.

Uso:
    python -m benchmarks.erro      # gera resultados/erro.md
"""

import platform
from datetime import date
from pathlib import Path

from benchmarks.cenarios import quase_ordenado, quase_ordenado_trocas_distantes
from benchmarks.cronometro import formata, medir
from ordenacao import base, escolher, insercao, intercalacao, ordenar

SAIDA = Path(__file__).resolve().parent.parent / "resultados" / "erro.md"


def _milhar(x):
    return f"{x:,}".replace(",", ".")


def inversoes(v):
    """Número de pares i < j com v[i] > v[j], por intercalação: O(n log n)."""
    def rec(a):
        if len(a) <= 1:
            return a, 0
        m = len(a) // 2
        e, ie = rec(a[:m])
        d, id_ = rec(a[m:])
        res, i, j, inv = [], 0, 0, ie + id_
        while i < len(e) and j < len(d):
            if d[j] < e[i]:
                res.append(d[j]); j += 1; inv += len(e) - i
            else:
                res.append(e[i]); i += 1
        res += e[i:] + d[j:]
        return res, inv
    return rec(list(v))[1]


def _med(f, v):
    return medir(f, v, repeticoes_min=3, repeticoes_max=10, tempo_min=0.2)


def main():
    linhas = []
    for n in (5_000, 10_000, 20_000, 40_000):
        for rotulo, gerar in (("vizinhos (≤ 10 posições)", quase_ordenado),
                              ("posições quaisquer", quase_ordenado_trocas_distantes)):
            v = gerar(n, fracao=0.01)
            e = escolher(v)
            t_ins, t_base = _med(insercao, v), _med(base, v)
            t_inter, t_ord = _med(intercalacao, v), _med(ordenar, v)
            melhor = min(t_ins, t_base, t_inter)
            linhas.append([_milhar(n), rotulo, e.motivo.split("(")[1].rstrip(")"),
                           _milhar(inversoes(v)), e.nome, formata(t_ord),
                           formata(t_ins), formata(t_base), formata(t_inter),
                           f"{t_ord / melhor:.1f}×".replace(".", ",")])
            print(linhas[-1])

    cab = ["n", "trocas de 1% das posições entre", "descidas", "inversões", "escolha",
           "ordenar", "inserção", "base", "intercalação", "ordenar / melhor"]
    md = [
        "# Cenário em que o escolhedor erra",
        "",
        f"Gerado por `python -m benchmarks.erro` em {date.today():%d/%m/%Y}.  ",
        f"Python {platform.python_version()} ({platform.python_implementation()}), "
        f"{platform.system()} {platform.machine()}.",
        "",
        "Listas ordenadas em que 1% das posições foi trocado. Nas linhas "
        "*vizinhos*, a troca é com alguém a até 10 posições (o cenário "
        "\"quase ordenado\" do enunciado). Nas linhas *posições quaisquer*, "
        "com qualquer posição da lista.",
        "",
        "| " + " | ".join(cab) + " |",
        "|" + "---|" * len(cab),
        *("| " + " | ".join(l) + " |" for l in linhas),
        "",
        "O escolhedor só enxerga as **descidas**, e elas são quase as mesmas nos "
        "dois tipos de lista. Quem decide o custo da inserção são as **inversões**, "
        "e essas explodem quando as trocas são distantes.",
        "",
    ]
    SAIDA.write_text("\n".join(md), encoding="utf-8")
    print(f"escrito em {SAIDA}")


if __name__ == "__main__":
    main()
