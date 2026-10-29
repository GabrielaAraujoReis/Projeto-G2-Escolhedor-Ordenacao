# Calibração do escolhedor

Gerado por `python -m benchmarks.calibrar` em 29/10/2026.  
Python 3.12.3 (CPython), Linux x86_64.

Tempos são medianas (ver `benchmarks/cronometro.py`).

## 1. Lista minúscula: até que n a inserção ganha?

Média de 20 listas aleatórias (chaves de 0 a 10⁹) para cada n.

| n | insercao | intercalacao | hibrida | base | vencedor |
|---|---|---|---|---|---|
| 4 | 0,4 µs | 1,4 µs | 0,4 µs | 25,4 µs | **insercao** |
| 8 | 1,0 µs | 3,8 µs | 1,1 µs | 34,5 µs | **insercao** |
| 12 | 1,8 µs | 5,1 µs | 2,2 µs | 32,2 µs | **insercao** |
| 16 | 3,5 µs | 8,7 µs | 3,1 µs | 34,6 µs | **hibrida** |
| 24 | 6,5 µs | 14,4 µs | 6,3 µs | 43,4 µs | **hibrida** |
| 32 | 12,5 µs | 22,4 µs | 9,3 µs | 38,5 µs | **hibrida** |
| 48 | 24,5 µs | 27,8 µs | 18,7 µs | 47,9 µs | **hibrida** |
| 64 | 38,9 µs | 42,1 µs | 23,3 µs | 51,2 µs | **hibrida** |
| 96 | 91,3 µs | 65,6 µs | 40,7 µs | 78,5 µs | **hibrida** |
| 128 | 165,9 µs | 83,5 µs | 55,8 µs | 75,4 µs | **hibrida** |
| 256 | 645,9 µs | 191,0 µs | 137,6 µs | 128,8 µs | **base** |

**Maior n em que a inserção venceu: 12.**

## 2. Quase ordenado: até quantas descidas a inserção compensa?

n = 10.000. Trocas apenas entre vizinhos a até 10 posições. *Descidas* são os pares adjacentes fora de ordem (v[i] > v[i+1]); é o que o escolhedor consegue contar numa passada barata.

| trocas | descidas / n | inserção | base | intercalação | vencedor |
|---|---|---|---|---|---|
| 0,1% | 0,18% | 676,8 µs | 4,57 ms | 7,29 ms | inserção |
| 0,5% | 0,92% | 688,0 µs | 4,50 ms | 7,31 ms | inserção |
| 1,0% | 1,83% | 680,3 µs | 4,39 ms | 7,22 ms | inserção |
| 2,0% | 3,64% | 758,6 µs | 4,45 ms | 7,40 ms | inserção |
| 5,0% | 8,57% | 977,1 µs | 4,50 ms | 7,19 ms | inserção |
| 8,0% | 12,84% | 1,06 ms | 4,47 ms | 7,21 ms | inserção |
| 12,0% | 17,83% | 1,29 ms | 4,80 ms | 7,79 ms | inserção |
| 20,0% | 25,69% | 1,69 ms | 4,54 ms | 7,89 ms | inserção |
| 30,0% | 32,29% | 1,80 ms | 4,85 ms | 7,97 ms | inserção |

**Maior fração de descidas em que a inserção ainda venceu: 32,29%.**

Atenção: este experimento só tem desordem *local*. Se as trocas forem entre posições distantes, cada descida esconde muitas inversões e a inserção fica muito mais cara — ver `resultados/erro.md`.

## 3. Contagem x base: até que faixa a contagem compensa?

Chaves sorteadas entre 0 e k-1. *razão* = k / n.

| n | razão k/n | k | contagem | base | vencedor |
|---|---|---|---|---|---|
| 1.000 | 0,01 | 10 | 42,3 µs | 116,2 µs | contagem |
| 1.000 | 0,1 | 100 | 46,1 µs | 111,2 µs | contagem |
| 1.000 | 1 | 1.000 | 130,4 µs | 254,7 µs | contagem |
| 1.000 | 2 | 2.000 | 172,2 µs | 235,6 µs | contagem |
| 1.000 | 4 | 4.000 | 226,3 µs | 267,8 µs | contagem |
| 1.000 | 8 | 8.000 | 359,6 µs | 267,9 µs | base |
| 1.000 | 16 | 16.000 | 624,7 µs | 274,1 µs | base |
| 1.000 | 32 | 32.000 | 996,6 µs | 273,9 µs | base |
| 1.000 | 64 | 64.000 | 1,81 ms | 288,5 µs | base |
| 10.000 | 0,01 | 100 | 384,8 µs | 1,04 ms | contagem |
| 10.000 | 0,1 | 1.000 | 620,1 µs | 2,63 ms | contagem |
| 10.000 | 1 | 10.000 | 2,40 ms | 4,47 ms | contagem |
| 10.000 | 2 | 20.000 | 1,77 ms | 2,57 ms | contagem |
| 10.000 | 4 | 40.000 | 3,29 ms | 5,31 ms | contagem |
| 10.000 | 8 | 80.000 | 5,58 ms | 3,59 ms | base |
| 10.000 | 16 | 160.000 | 5,77 ms | 3,61 ms | base |
| 10.000 | 32 | 320.000 | 10,27 ms | 3,50 ms | base |
| 10.000 | 64 | 640.000 | 20,40 ms | 3,62 ms | base |
| 100.000 | 0,01 | 1.000 | 5,71 ms | 38,52 ms | contagem |
| 100.000 | 0,1 | 10.000 | 5,87 ms | 27,63 ms | contagem |
| 100.000 | 1 | 100.000 | 12,95 ms | 43,86 ms | contagem |
| 100.000 | 2 | 200.000 | 19,95 ms | 55,59 ms | contagem |
| 100.000 | 4 | 400.000 | 28,48 ms | 48,34 ms | contagem |
| 100.000 | 8 | 800.000 | 53,18 ms | 54,78 ms | contagem |
| 100.000 | 16 | 1.600.000 | 69,08 ms | 51,59 ms | base |
| 100.000 | 32 | 3.200.000 | 114 ms | 49,77 ms | base |
| 100.000 | 64 | 6.400.000 | 215 ms | 54,33 ms | base |

**Maior razão k/n em que a contagem venceu, por n:** n=1.000: 4, n=10.000: 4, n=100.000: 8.

## 4. Base x comparação: quantas passadas a base aguenta?

Chaves sorteadas entre 0 e 2^bits - 1. Cada 8 bits = 1 passada.

| n | bits | passadas | base | intercalação | híbrida | vencedor |
|---|---|---|---|---|---|---|
| 64 | 8 | 1 | 12,6 µs | 39,5 µs | 22,9 µs | base |
| 64 | 16 | 2 | 27,6 µs | 36,2 µs | 22,8 µs | comparação |
| 64 | 32 | 4 | 52,2 µs | 36,8 µs | 25,5 µs | comparação |
| 64 | 64 | 8 | 103,4 µs | 37,0 µs | 26,0 µs | comparação |
| 64 | 128 | 16 | 216,4 µs | 37,7 µs | 24,9 µs | comparação |
| 256 | 8 | 1 | 30,5 µs | 175,2 µs | 114,3 µs | base |
| 256 | 16 | 2 | 69,2 µs | 180,8 µs | 128,7 µs | base |
| 256 | 32 | 4 | 141,0 µs | 192,2 µs | 145,8 µs | base |
| 256 | 64 | 8 | 274,6 µs | 189,7 µs | 147,1 µs | comparação |
| 256 | 128 | 16 | 545,2 µs | 189,9 µs | 139,0 µs | comparação |
| 1.000 | 8 | 1 | 112,2 µs | 825,1 µs | 626,9 µs | base |
| 1.000 | 16 | 2 | 258,4 µs | 861,3 µs | 851,6 µs | base |
| 1.000 | 32 | 4 | 561,1 µs | 912,0 µs | 887,5 µs | base |
| 1.000 | 64 | 8 | 1,02 ms | 890,8 µs | 923,2 µs | comparação |
| 1.000 | 128 | 16 | 1,98 ms | 880,6 µs | 911,9 µs | comparação |
| 10.000 | 8 | 1 | 1,04 ms | 10,29 ms | 6,09 ms | base |
| 10.000 | 16 | 2 | 4,16 ms | 10,93 ms | 12,17 ms | base |
| 10.000 | 32 | 4 | 5,37 ms | 11,23 ms | 12,52 ms | base |
| 10.000 | 64 | 8 | 9,90 ms | 11,41 ms | 12,97 ms | base |
| 10.000 | 128 | 16 | 20,05 ms | 11,13 ms | 12,75 ms | comparação |
| 100.000 | 8 | 1 | 11,45 ms | 121 ms | 58,40 ms | base |
| 100.000 | 16 | 2 | 27,08 ms | 156 ms | 145 ms | base |
| 100.000 | 32 | 4 | 77,63 ms | 185 ms | 170 ms | base |
| 100.000 | 64 | 8 | 150 ms | 153 ms | 186 ms | base |
| 100.000 | 128 | 16 | 291 ms | 156 ms | 171 ms | comparação |

**Maior número de passadas em que a base venceu, por n:** n=64: 1, n=256: 4, n=1.000: 4, n=10.000: 8, n=100.000: 8 (n ausente = a base não venceu em nenhum caso).

## 5. Melhor método por comparação (chaves não inteiras)

n = 10.000.

| entrada | intercalação | rápida | híbrida | vencedor |
|---|---|---|---|---|
| reais aleatórios | 10,53 ms | 13,11 ms | 11,43 ms | **intercalacao** |
| textos aleatórios | 12,04 ms | 15,34 ms | 12,62 ms | **intercalacao** |
| reais com 10 valores distintos | 9,99 ms | 2,40 ms | 2,14 ms | **hibrida** |
