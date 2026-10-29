# Resultados dos quatro cenários

Gerado por `python -m benchmarks.medir` em 29/10/2026.  
Python 3.12.3 (CPython), Linux x86_64.

Tempo mediano de uma chamada. Em negrito, o melhor método fixo do cenário. A coluna **ordenar** inclui o tempo do `escolher`.

## Cenários

| cenário | entrada |
|---|---|
| Aleatório, chaves grandes | 10.000 inteiros sorteados entre 0 e 10⁹ |
| Faixa estreita | 10.000 notas sorteadas entre 0 e 100 |
| Quase ordenado | 10.000 inteiros entre 0 e 10⁹, ordenados, com 1% das posições trocadas com um vizinho a até 10 posições |
| Lista minúscula | 10 inteiros sorteados entre 0 e 1.000 |

## Tempos

| cenário | inserção | intercalação | rápida | híbrida | contagem | base | **ordenar** |
|---|---|---|---|---|---|---|---|
| Aleatório, chaves grandes | 1,42 s | 10,97 ms | 13,83 ms | 12,19 ms | estouro¹ | **4,74 ms** | 4,63 ms |
| Faixa estreita | 1,21 s | 9,95 ms | 4,26 ms | 4,47 ms | **366,1 µs** | 1,00 ms | 489,1 µs |
| Quase ordenado | **709,3 µs** | 7,07 ms | 13,42 ms | 11,48 ms | estouro¹ | 4,56 ms | 920,9 µs |
| Lista minúscula | **1,4 µs** | 4,2 µs | 3,4 µs | 1,5 µs | 22,2 µs | 23,6 µs | 2,4 µs |

¹ Aleatório, chaves grandes: recusada, k = 999.411.452 pediria ~7,4 GB; Quase ordenado: recusada, k = 999.927.996 pediria ~7,5 GB. A contagem recusa faixas acima de 10.000.000 contadores.

## Quantas vezes mais lento que o melhor método fixo do cenário

| cenário | inserção | intercalação | rápida | híbrida | contagem | base | **ordenar** |
|---|---|---|---|---|---|---|---|
| Aleatório, chaves grandes | 300× | 2,31× | 2,91× | 2,57× | — | 1,00× | 0,98× |
| Faixa estreita | 3318× | 27× | 12× | 12× | 1,00× | 2,73× | 1,34× |
| Quase ordenado | 1,00× | 9,97× | 19× | 16× | — | 6,43× | 1,30× |
| Lista minúscula | 1,00× | 3,02× | 2,48× | 1,06× | 16× | 17× | 1,71× |
| **pior caso** | 3318× | 27× | 19× | 16× | estoura | 17× | 1,71× |

## O que o `escolher` decidiu

| cenário | escolha | motivo | acertou o melhor fixo? |
|---|---|---|---|
| Aleatório, chaves grandes | base | inteiros com faixa larga (k = 999.411.452), 4 passada(s) de 8 bits | sim |
| Faixa estreita | contagem | inteiros com faixa estreita (k = 101 ≤ 2·n) | sim |
| Quase ordenado | inserção | quase ordenada (183 descidas = 1,8 % de n) | sim |
| Lista minúscula | inserção | lista minúscula (n ≤ 16) | sim |

## Quanto custa o `escolher`

*olhar (embutidas)*: as quatro passadas que o `escolher` faz no pior caso (descidas, mínimo, máximo, tipos), com funções embutidas em C.  
*olhar (um laço)*: as mesmas quatro informações numa ÚNICA passada com um laço `for` em Python.

| cenário | escolher | % do ordenar | olhar (embutidas) | olhar (um laço) |
|---|---|---|---|---|
| Aleatório, chaves grandes | 365,2 µs | 7,9% | 464,3 µs | 531,8 µs |
| Faixa estreita | 281,4 µs | 57,5% | 413,6 µs | 436,0 µs |
| Quase ordenado | 223,6 µs | 24,3% | 489,0 µs | 435,6 µs |
| Lista minúscula | 0,1 µs | 3,1% | 1,3 µs | 0,8 µs |
