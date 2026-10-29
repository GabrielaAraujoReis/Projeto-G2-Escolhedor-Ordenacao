"""Mede os quatro cenários do enunciado contra os seis métodos e o `ordenar`.

Uso:
    python -m benchmarks.medir

Gera:
    resultados/cenarios.md   tabelas prontas para o RELATORIO.md
    resultados/cenarios.csv  os mesmos tempos, em segundos, para planilha

Leva por volta de um minuto; quase todo o tempo é a inserção ordenando
10 mil números aleatórios, que é O(n²) (e está aqui justamente para mostrar
isso).
"""

import csv
import platform
from datetime import date
from itertools import islice
from operator import gt
from pathlib import Path

from benchmarks.cenarios import CENARIOS
from benchmarks.cronometro import formata, medir
from ordenacao import METODOS, escolher, ordenar
from ordenacao.contagem import BYTES_POR_CONTADOR, LIMITE_CONTADORES

RAIZ = Path(__file__).resolve().parent.parent
SAIDA_MD = RAIZ / "resultados" / "cenarios.md"
SAIDA_CSV = RAIZ / "resultados" / "cenarios.csv"

COLUNAS = list(METODOS) + ["ordenar"]
NOMES = {
    "insercao": "inserção", "intercalacao": "intercalação", "rapida": "rápida",
    "hibrida": "híbrida", "contagem": "contagem", "base": "base", "ordenar": "**ordenar**",
}


def tabela(cabecalho, linhas):
    out = ["| " + " | ".join(cabecalho) + " |", "|" + "---|" * len(cabecalho)]
    out += ["| " + " | ".join(str(c) for c in linha) + " |" for linha in linhas]
    return "\n".join(out)


def _milhar(x):
    return f"{x:,}".replace(",", ".")


def _razao(x):
    return f"{x:.2f}×".replace(".", ",") if x < 10 else f"{x:.0f}×"


# --- duas formas de olhar a lista, para responder "o escolher compensa?" ---

def olhar_com_embutidas(v):
    """As 4 passadas completas, todas em C (sem a parada antecipada)."""
    descidas = sum(map(gt, v, islice(v, 1, None)))
    return descidas, min(v), max(v), set(map(type, v)) == {int}


def olhar_com_um_laco(v):
    """A alternativa "óbvia": UMA passada, mas com um laço em Python."""
    descidas, mn, mx, inteiros = 0, v[0], v[0], True
    anterior = v[0]
    for x in v:
        if anterior > x:
            descidas += 1
        if x < mn:
            mn = x
        elif x > mx:
            mx = x
        if type(x) is not int:
            inteiros = False
        anterior = x
    return descidas, mn, mx, inteiros


def main():
    tempos = {}        # (cenario, coluna) -> segundos, ou None se recusada
    recusas = {}       # cenario -> mensagem
    decisoes = {}      # cenario -> Escolha
    custo_escolher = {}
    custo_olhar = {}

    for chave, cen in CENARIOS.items():
        v = cen["gerar"]()
        print(f"{cen['titulo']}:")
        for nome, f in METODOS.items():
            if nome == "contagem":
                k = max(v) - min(v) + 1
                if k > LIMITE_CONTADORES:
                    tempos[chave, nome] = None
                    gb = f"{k * BYTES_POR_CONTADOR / 2**30:.1f}".replace(".", ",")
                    recusas[chave] = f"recusada, k = {_milhar(k)} pediria ~{gb} GB"
                    print(f"  {nome:13s} {recusas[chave]}")
                    continue
            tempos[chave, nome] = medir(f, v)
            print(f"  {nome:13s} {formata(tempos[chave, nome])}")
        tempos[chave, "ordenar"] = medir(ordenar, v)
        decisoes[chave] = escolher(v)
        custo_escolher[chave] = medir(escolher, v)
        if len(v) > 1:
            custo_olhar[chave] = (medir(olhar_com_embutidas, v), medir(olhar_com_um_laco, v))
        print(f"  {'ordenar':13s} {formata(tempos[chave, 'ordenar'])}  -> {decisoes[chave].nome}")

    # ------------------------------------------------------------ tabelas
    cab = ["cenário"] + [NOMES[c] for c in COLUNAS]
    linhas_tempo, linhas_razao = [], []
    melhor_fixo = {}
    for chave, cen in CENARIOS.items():
        fixos = {m: tempos[chave, m] for m in METODOS if tempos[chave, m] is not None}
        melhor = min(fixos, key=fixos.get)
        melhor_fixo[chave] = (melhor, fixos[melhor])
        linha_t, linha_r = [cen["titulo"]], [cen["titulo"]]
        for c in COLUNAS:
            t = tempos[chave, c]
            if t is None:
                linha_t.append("estouro¹")
                linha_r.append("—")
                continue
            txt = formata(t)
            linha_t.append(f"**{txt}**" if c == melhor else txt)
            linha_r.append(_razao(t / fixos[melhor]))
        linhas_tempo.append(linha_t)
        linhas_razao.append(linha_r)

    # pior caso de cada estratégia: a maior razão em relação ao melhor fixo
    pior = []
    for c in COLUNAS:
        razoes = []
        for chave in CENARIOS:
            t = tempos[chave, c]
            razoes.append(float("inf") if t is None else t / melhor_fixo[chave][1])
        r = max(razoes)
        pior.append("estoura" if r == float("inf") else _razao(r))

    linhas_decisao = []
    for chave, cen in CENARIOS.items():
        e = decisoes[chave]
        m, t_m = melhor_fixo[chave]
        acertou = "sim" if e.nome == m else f"não (melhor: {NOMES[m]})"
        linhas_decisao.append([cen["titulo"], NOMES[e.nome], e.motivo, acertou])

    linhas_custo = []
    for chave, cen in CENARIOS.items():
        t_esc = custo_escolher[chave]
        t_ord = tempos[chave, "ordenar"]
        linha = [cen["titulo"], formata(t_esc), f"{t_esc / t_ord:.1%}".replace(".", ",")]
        if chave in custo_olhar:
            emb, laco = custo_olhar[chave]
            linha += [formata(emb), formata(laco)]
        else:
            linha += ["—", "—"]
        linhas_custo.append(linha)

    md = [
        "# Resultados dos quatro cenários",
        "",
        f"Gerado por `python -m benchmarks.medir` em {date.today():%d/%m/%Y}.  ",
        f"Python {platform.python_version()} ({platform.python_implementation()}), "
        f"{platform.system()} {platform.machine()}.",
        "",
        "Tempo mediano de uma chamada. Em negrito, o melhor método fixo do cenário. "
        "A coluna **ordenar** inclui o tempo do `escolher`.",
        "",
        "## Cenários",
        "",
        tabela(["cenário", "entrada"], [[c["titulo"], c["descricao"]] for c in CENARIOS.values()]),
        "",
        "## Tempos",
        "",
        tabela(cab, linhas_tempo),
        "",
        "¹ " + "; ".join(f"{CENARIOS[c]['titulo']}: {m}" for c, m in recusas.items())
        + f". A contagem recusa faixas acima de {_milhar(LIMITE_CONTADORES)} contadores.",
        "",
        "## Quantas vezes mais lento que o melhor método fixo do cenário",
        "",
        tabela(cab, linhas_razao + [["**pior caso**"] + pior]),
        "",
        "## O que o `escolher` decidiu",
        "",
        tabela(["cenário", "escolha", "motivo", "acertou o melhor fixo?"], linhas_decisao),
        "",
        "## Quanto custa o `escolher`",
        "",
        "*olhar (embutidas)*: as quatro passadas que o `escolher` faz no pior caso "
        "(descidas, mínimo, máximo, tipos), com funções embutidas em C.  ",
        "*olhar (um laço)*: as mesmas quatro informações numa ÚNICA passada com "
        "um laço `for` em Python.",
        "",
        tabela(["cenário", "escolher", "% do ordenar", "olhar (embutidas)", "olhar (um laço)"],
               linhas_custo),
        "",
    ]
    SAIDA_MD.parent.mkdir(exist_ok=True)
    SAIDA_MD.write_text("\n".join(md), encoding="utf-8")

    with open(SAIDA_CSV, "w", newline="", encoding="utf-8") as arq:
        w = csv.writer(arq)
        w.writerow(["cenario", "metodo", "segundos"])
        for (chave, c), t in tempos.items():
            w.writerow([chave, c, "" if t is None else f"{t:.9f}"])
    print(f"\nescrito em {SAIDA_MD} e {SAIDA_CSV}")


if __name__ == "__main__":
    main()
