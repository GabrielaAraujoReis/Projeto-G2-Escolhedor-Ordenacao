# Cenário em que o escolhedor erra

Gerado por `python -m benchmarks.erro` em 29/10/2026.  
Python 3.12.3 (CPython), Linux x86_64.

Listas ordenadas em que 1% das posições foi trocado. Nas linhas *vizinhos*, a troca é com alguém a até 10 posições (o cenário "quase ordenado" do enunciado). Nas linhas *posições quaisquer*, com qualquer posição da lista.

| n | trocas de 1% das posições entre | descidas | inversões | escolha | ordenar | inserção | base | intercalação | ordenar / melhor |
|---|---|---|---|---|---|---|---|---|---|
| 5.000 | vizinhos (≤ 10 posições) | 96 descidas = 1,9 % de n | 490 | insercao | 488,0 µs | 373,4 µs | 2,26 ms | 3,45 ms | 1,3× |
| 5.000 | posições quaisquer | 96 descidas = 1,9 % de n | 165.754 | insercao | 9,06 ms | 8,96 ms | 2,24 ms | 3,93 ms | 4,1× |
| 10.000 | vizinhos (≤ 10 posições) | 183 descidas = 1,8 % de n | 1.044 | insercao | 923,4 µs | 687,6 µs | 4,86 ms | 6,97 ms | 1,3× |
| 10.000 | posições quaisquer | 196 descidas = 2,0 % de n | 684.082 | insercao | 42,62 ms | 35,36 ms | 5,11 ms | 9,31 ms | 8,3× |
| 20.000 | vizinhos (≤ 10 posições) | 379 descidas = 1,9 % de n | 2.074 | insercao | 1,89 ms | 3,25 ms | 13,45 ms | 15,37 ms | 0,6× |
| 20.000 | posições quaisquer | 389 descidas = 1,9 % de n | 2.619.540 | insercao | 139 ms | 142 ms | 10,90 ms | 32,50 ms | 12,7× |
| 40.000 | vizinhos (≤ 10 posições) | 748 descidas = 1,9 % de n | 4.014 | insercao | 4,01 ms | 3,16 ms | 24,38 ms | 34,53 ms | 1,3× |
| 40.000 | posições quaisquer | 783 descidas = 2,0 % de n | 11.065.840 | insercao | 623 ms | 588 ms | 24,39 ms | 42,11 ms | 25,5× |

O escolhedor só enxerga as **descidas**, e elas são quase as mesmas nos dois tipos de lista. Quem decide o custo da inserção são as **inversões**, e essas explodem quando as trocas são distantes.
