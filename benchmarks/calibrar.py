"""Experimentos que definem as regras do `escolher`.

Cada experimento varia UMA característica barata de observar (tamanho,
desordem, faixa, número de bytes da chave) e mede onde um método passa a
ganhar do outro. Os limiares do escolhedor são esses pontos de virada.

Uso:
    python -m benchmarks.calibrar            # gera resultados/calibracao.md
    python -m benchmarks.calibrar --rapido   # menos pontos, para conferir

Leva alguns minutos. Os números dependem da máquina, mas os pontos de
virada costumam mudar pouco, porque são *razões* entre métodos que rodam
no mesmo interpretador.
"""

import platform
import random
import sys
from datetime import date
from pathlib import Path

from benchmarks.cenarios import aleatorio, quase_ordenado
from benchmarks.cronometro import formata, medir
from ordenacao import base, contagem, hibrida, insercao, intercalacao, rapida

RAPIDO = "--rapido" in sys.argv
SAIDA = Path(__file__).resolve().parent.parent / "resultados" / "calibracao.md"


def _medir(f, v):
    return medir(f, v, repeticoes_min=5, repeticoes_max=25, tempo_min=0.3)


def _pct(x, casas=2):
    return f"{x:.{casas}%}".replace(".", ",")


def _num(x):
    return f"{x:,}".replace(",", "X").replace(".", ",").replace("X", ".")


def _descidas(v):
    return sum(1 for a, b in zip(v, v[1:]) if a > b)


def tabela(cabecalho, linhas):
    out = ["| " + " | ".join(cabecalho) + " |", "|" + "---|" * len(cabecalho)]
    out += ["| " + " | ".join(str(c) for c in linha) + " |" for linha in linhas]
    return "\n".join(out)


def vencedor(tempos):
    return min(tempos, key=tempos.get)


# ---------------------------------------------------------------- 1
def exp_minuscula():
    """Até que tamanho a inserção ganha de todo o resto?"""
    tamanhos = [4, 8, 16, 32, 64, 128] if RAPIDO else [4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 256]
    metodos = {"insercao": insercao, "intercalacao": intercalacao,
               "hibrida": hibrida, "base": base}
    linhas, ultimo_n_insercao = [], 0
    for n in tamanhos:
        # média de 20 listas diferentes do mesmo tamanho, para não depender de uma só
        listas = [aleatorio(n, 10**9, semente=s) for s in range(20)]
        tempos = {nome: sum(_medir(f, v) for v in listas) / len(listas)
                  for nome, f in metodos.items()}
        v = vencedor(tempos)
        if v == "insercao":
            ultimo_n_insercao = n
        linhas.append([n] + [formata(tempos[m]) for m in metodos] + [f"**{v}**"])
    return linhas, list(metodos), ultimo_n_insercao


# ---------------------------------------------------------------- 2
def exp_quase_ordenado():
    """Com quantas descidas (v[i] > v[i+1]) a inserção deixa de compensar?"""
    n = 10_000
    fracoes = [0.005, 0.02, 0.08, 0.2] if RAPIDO else [0.001, 0.005, 0.01, 0.02, 0.05, 0.08, 0.12, 0.2, 0.3]
    linhas, maior_frac_ok = [], 0.0
    for f in fracoes:
        v = quase_ordenado(n, fracao=f)
        frac_desc = _descidas(v) / n
        t_ins = _medir(insercao, v)
        # a alternativa que o escolhedor usaria para inteiros grandes é a base;
        # para chaves não inteiras, a melhor por comparação (intercalação)
        t_base = _medir(base, v)
        t_inter = _medir(intercalacao, v)
        ganha = t_ins < min(t_base, t_inter)
        if ganha:
            maior_frac_ok = max(maior_frac_ok, frac_desc)
        linhas.append([_pct(f, 1), _pct(frac_desc), formata(t_ins), formata(t_base),
                       formata(t_inter), "inserção" if ganha else "outra"])
    return linhas, maior_frac_ok


# ---------------------------------------------------------------- 3
def exp_contagem_vs_base():
    """Até que razão faixa/n a contagem ganha da base?"""
    ns = [1_000, 10_000] if RAPIDO else [1_000, 10_000, 100_000]
    razoes = [0.01, 1, 8, 32] if RAPIDO else [0.01, 0.1, 1, 2, 4, 8, 16, 32, 64]
    linhas, viradas = [], {}
    for n in ns:
        for r in razoes:
            k = max(2, int(n * r))
            v = aleatorio(n, k - 1, semente=7)
            t_c, t_b = _medir(contagem, v), _medir(base, v)
            if t_c < t_b:
                viradas[n] = r
            linhas.append([_num(n), _num(r), _num(k),
                           formata(t_c), formata(t_b), "contagem" if t_c < t_b else "base"])
    return linhas, viradas


# ---------------------------------------------------------------- 4
def exp_base_vs_comparacao():
    """Com quantos bytes de chave a base deixa de ganhar das comparativas?"""
    ns = [64, 1_000, 10_000] if RAPIDO else [64, 256, 1_000, 10_000, 100_000]
    bits_lista = [16, 32, 64] if RAPIDO else [8, 16, 32, 64, 128]
    linhas, max_passadas = [], {}
    for n in ns:
        for bits in bits_lista:
            v = aleatorio(n, 2**bits - 1, semente=11)
            passadas = bits // 8
            t_b = _medir(base, v)
            t_i = _medir(intercalacao, v)
            t_h = _medir(hibrida, v)
            ganha = t_b < min(t_i, t_h)
            if ganha:
                max_passadas[n] = max(max_passadas.get(n, 0), passadas)
            linhas.append([_num(n), bits, passadas, formata(t_b),
                           formata(t_i), formata(t_h), "base" if ganha else "comparação"])
    return linhas, max_passadas


# ---------------------------------------------------------------- 5
def exp_comparativas():
    """Qual a melhor ordenação por comparação (para chaves não inteiras)?"""
    r = random.Random(5)
    entradas = {
        "reais aleatórios": [r.random() for _ in range(10_000)],
        "textos aleatórios": ["".join(r.choice("abcdefghij") for _ in range(8)) for _ in range(10_000)],
        "reais com 10 valores distintos": [float(r.randint(0, 9)) for _ in range(10_000)],
    }
    linhas = []
    for nome, v in entradas.items():
        t = {"intercalacao": _medir(intercalacao, v), "rapida": _medir(rapida, v),
             "hibrida": _medir(hibrida, v)}
        linhas.append([nome] + [formata(t[m]) for m in t] + [f"**{vencedor(t)}**"])
    return linhas


def main():
    print("calibrando... (alguns minutos)")
    l1, cab1, n_ins = exp_minuscula();          print("  1/5 minúscula")
    l2, frac_ok = exp_quase_ordenado();        print("  2/5 quase ordenado")
    l3, viradas = exp_contagem_vs_base();      print("  3/5 contagem x base")
    l4, max_pass = exp_base_vs_comparacao();   print("  4/5 base x comparação")
    l5 = exp_comparativas();                   print("  5/5 comparativas")

    md = [
        "# Calibração do escolhedor",
        "",
        f"Gerado por `python -m benchmarks.calibrar` em {date.today():%d/%m/%Y}.  ",
        f"Python {platform.python_version()} ({platform.python_implementation()}), "
        f"{platform.system()} {platform.machine()}.",
        "",
        "Tempos são medianas (ver `benchmarks/cronometro.py`).",
        "",
        "## 1. Lista minúscula: até que n a inserção ganha?",
        "",
        "Média de 20 listas aleatórias (chaves de 0 a 10⁹) para cada n.",
        "",
        tabela(["n"] + cab1 + ["vencedor"], l1),
        "",
        f"**Maior n em que a inserção venceu: {n_ins}.**",
        "",
        "## 2. Quase ordenado: até quantas descidas a inserção compensa?",
        "",
        "n = 10.000. Trocas apenas entre vizinhos a até 10 posições. "
        "*Descidas* são os pares adjacentes fora de ordem (v[i] > v[i+1]); "
        "é o que o escolhedor consegue contar numa passada barata.",
        "",
        tabela(["trocas", "descidas / n", "inserção", "base", "intercalação", "vencedor"], l2),
        "",
        f"**Maior fração de descidas em que a inserção ainda venceu: {_pct(frac_ok)}.**",
        "",
        "Atenção: este experimento só tem desordem *local*. Se as trocas forem "
        "entre posições distantes, cada descida esconde muitas inversões e a "
        "inserção fica muito mais cara — ver `resultados/erro.md`.",
        "",
        "## 3. Contagem x base: até que faixa a contagem compensa?",
        "",
        "Chaves sorteadas entre 0 e k-1. *razão* = k / n.",
        "",
        tabela(["n", "razão k/n", "k", "contagem", "base", "vencedor"], l3),
        "",
        "**Maior razão k/n em que a contagem venceu, por n:** "
        + ", ".join(f"n={_num(n)}: {_num(r)}" for n, r in viradas.items()) + ".",
        "",
        "## 4. Base x comparação: quantas passadas a base aguenta?",
        "",
        "Chaves sorteadas entre 0 e 2^bits - 1. Cada 8 bits = 1 passada.",
        "",
        tabela(["n", "bits", "passadas", "base", "intercalação", "híbrida", "vencedor"], l4),
        "",
        "**Maior número de passadas em que a base venceu, por n:** "
        + ", ".join(f"n={_num(n)}: {p}" for n, p in max_pass.items())
        + " (n ausente = a base não venceu em nenhum caso).",
        "",
        "## 5. Melhor método por comparação (chaves não inteiras)",
        "",
        "n = 10.000.",
        "",
        tabela(["entrada", "intercalação", "rápida", "híbrida", "vencedor"], l5),
        "",
    ]
    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text("\n".join(md), encoding="utf-8")
    print(f"escrito em {SAIDA}")


if __name__ == "__main__":
    main()
