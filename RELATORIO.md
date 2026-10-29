# Relatório — ordenação que escolhe o próprio método

**Dupla:** Gabriela de Araújo Reis e Euclides Carlos Pilon Neto  
**Disciplina:** Estruturas de Dados Avançadas — trabalho de 29/10

## 1. Resumo

Implementamos os seis métodos do semestre e um `escolher(v)` que, olhando
só o tamanho da lista, quantos pares adjacentes estão fora de ordem, o
mínimo, o máximo e o tipo das chaves, decide qual deles usar. Nos quatro
cenários pedidos o `escolher` acertou o melhor método fixo nas quatro vezes,
e o `ordenar` ficou no máximo **1,7×** mais lento que o melhor método de
cada cenário. Qualquer método fixo, no seu pior cenário, fica entre
**16× e 3.300×** mais lento — ou nem roda (a contagem pediria 7,4 GB).

Também encontramos um caso em que o `escolher` erra feio (seção 7) e
explicamos por quê.

## 2. Como medimos

- Python 3.12.3 (CPython), Linux x86_64, máquina virtual de 1 núcleo.
- Entradas geradas com semente fixa (`benchmarks/cenarios.py`).
- Cada número é a **mediana** de pelo menos 5 execuções, com o coletor de
  lixo desligado; chamadas de microssegundos são repetidas em lote e
  divididas (`benchmarks/cronometro.py`).
- Todos os métodos devolvem uma lista nova, então a cópia da entrada está
  incluída no tempo de todos, igualmente.
- O tempo do `ordenar` **inclui** o tempo do `escolher`.
- Em máquina virtual há ruído de ±10–20 % entre execuções. Diferenças
  menores que isso (por exemplo, `ordenar` 0,98× no primeiro cenário) não
  significam nada.

Os números abaixo são da execução registrada em `resultados/`. Para
refazer, ver o README.

## 3. Os quatro cenários contra os seis métodos

| cenário | entrada |
|---|---|
| Aleatório, chaves grandes | 10.000 inteiros sorteados entre 0 e 10⁹ |
| Faixa estreita | 10.000 notas sorteadas entre 0 e 100 |
| Quase ordenado | 10.000 inteiros entre 0 e 10⁹, ordenados, com 1% das posições trocadas com um vizinho a até 10 posições |
| Lista minúscula | 10 inteiros sorteados entre 0 e 1.000 |

Tempo de uma chamada (em negrito, o melhor método fixo):

| cenário | inserção | intercalação | rápida | híbrida | contagem | base | **ordenar** |
|---|---|---|---|---|---|---|---|
| Aleatório, chaves grandes | 1,42 s | 10,97 ms | 13,83 ms | 12,19 ms | estouro¹ | **4,74 ms** | 4,63 ms |
| Faixa estreita | 1,21 s | 9,95 ms | 4,26 ms | 4,47 ms | **366,1 µs** | 1,00 ms | 489,1 µs |
| Quase ordenado | **709,3 µs** | 7,07 ms | 13,42 ms | 11,48 ms | estouro¹ | 4,56 ms | 920,9 µs |
| Lista minúscula | **1,4 µs** | 4,2 µs | 3,4 µs | 1,5 µs | 22,2 µs | 23,6 µs | 2,4 µs |

¹ A faixa é de ~10⁹ valores: a contagem precisaria de ~7,4 GB só de
contadores. Ela se recusa a alocar (lança `FaixaGrandeDemais`) em vez de
derrubar a máquina.

Quantas vezes mais lento que o melhor método fixo do cenário:

| cenário | inserção | intercalação | rápida | híbrida | contagem | base | **ordenar** |
|---|---|---|---|---|---|---|---|
| Aleatório, chaves grandes | 300× | 2,31× | 2,91× | 2,57× | — | 1,00× | 0,98× |
| Faixa estreita | 3318× | 27× | 12× | 12× | 1,00× | 2,73× | 1,34× |
| Quase ordenado | 1,00× | 9,97× | 19× | 16× | — | 6,43× | 1,30× |
| Lista minúscula | 1,00× | 3,02× | 2,48× | 1,06× | 16× | 17× | 1,71× |
| **pior caso** | 3318× | 27× | 19× | 16× | estoura | 17× | **1,71×** |

A última linha é o argumento central do trabalho: **cada método fixo tem um
cenário em que é desastroso; o `ordenar` não tem.** Escolher um método fixo
é apostar num tipo de entrada; o `ordenar` olha antes de apostar.

## 4. Quem venceu cada cenário, e por quê

**Aleatório, chaves grandes → base.** Como o slide 13 mostrou, a contagem
fica inviável quando a faixa é grande: aqui ela pediria um bilhão de
contadores. A base resolve o mesmo problema quebrando a chave em pedaços:
um número até 10⁹ cabe em 4 bytes, então são 4 passadas de contagem com
256 contadores cada, ou seja O(4·n). As comparativas precisam de cerca de
n·log₂n ≈ 133 mil comparações, e cada comparação em Python custa caro;
por isso a base ganha delas por mais de 2×. A inserção faz ~25 milhões de
deslocamentos (n²/4) e leva mais de um segundo.

**Faixa estreita → contagem.** É exatamente o exemplo das notas do slide 4:
com k = 101 o vetor de contadores é minúsculo, a contagem passa uma vez
pela entrada e despeja 101 blocos em ordem. A base também ganharia das
comparativas (1 passada só, porque 100 cabe em um byte), mas cada passada
dela tem três laços contra um da contagem. Rápida e híbrida vão bem aqui
(4 ms, contra 10 ms da intercalação) graças à partição em três partes:
com só 101 valores distintos, cada partição tira todos os iguais ao pivô
de uma vez. A inserção é 3.300× pior: muitos repetidos não ajudam em nada
quando os elementos estão em ordem aleatória.

**Quase ordenado → inserção.** A inserção custa O(n + inversões). Com cada
elemento deslocado no máximo 10 posições, há só ~1.000 inversões em
10.000 elementos, e a inserção vira praticamente uma passada só. A
intercalação e a rápida não aproveitam a ordem que já existe e pagam o
n log n inteiro. A contagem, de novo, nem roda (as chaves vão até 10⁹).

**Lista minúscula → inserção.** Com 10 elementos, a ordem de crescimento
não importa: ganha quem tem a menor constante. A inserção não aloca nada
nem faz chamadas recursivas. A contagem e a base pagam custos fixos que
não dependem de n (alocar 1.001 contadores; 256 contadores por passada) e
ficam 16–17× mais lentas. A híbrida empata com a inserção porque, abaixo
de 16 elementos, ela *é* uma inserção.

Uma observação: a rápida nunca é a melhor de um cenário (fica perto da
híbrida ou atrás dela), e a intercalação só vale a pena quando as chaves
não são inteiras e há muitos elementos. Por isso o `escolher` nunca devolve
a rápida, e só devolve a intercalação no caso geral com n grande.

## 5. As regras do `escolher`, e de onde vieram

As regras estão em `ordenacao/escolhedor.py`, testadas na ordem abaixo
(das mais baratas para as mais caras de verificar). Cada limiar saiu de um
experimento em `benchmarks/calibrar.py`; os resultados estão em
`resultados/calibracao.md` (seções §1 a §5).

| # | condição | método | de onde veio |
|---|---|---|---|
| 1 | n ≤ 16 | inserção | §1: até 16 a inserção (e a híbrida, que nesse tamanho é inserção) ganha de todos; a partir de 32 a híbrida ganha por ~25 %. |
| 2 | descidas ≤ 5 % de n | inserção | §2: com desordem local, a inserção ganhou até 32 % de descidas. Usamos um sexto disso como margem, porque as descidas não medem *distância* (ver seção 7). |
| 3 | inteiros e k ≤ 2·n (e k ≤ 10⁷) | contagem | §3: com k ≤ 2n a contagem ganhou da base em todos os n testados (1 mil, 10 mil, 100 mil); a virada fica entre 4n e 16n e muda com n, então ficamos do lado seguro. O teto de 10⁷ contadores (~80 MB) é a guarda de memória. |
| 4 | inteiros, n ≥ 256 e até 4 passadas (k < 2³²) | base | §4: com n ≥ 256 a base venceu as comparativas em todos os casos até 4 passadas; com 8 passadas só às vezes, com 16 nunca. Com n = 64 só venceu com 1 passada. |
| 5 | n < 1.000 | híbrida | §1 e §4: entre as comparativas, a híbrida ganha em listas pequenas e médias. |
| 6 | demais casos | intercalação | §4 e §5: com n ≥ 10 mil e chaves distintas a intercalação ganhou da híbrida e da rápida (reais, textos, inteiros de 128 bits). |

Três detalhes de implementação:

- **A contagem nunca é chamada com faixa grande.** O escolhedor calcula
  k = máx − mín + 1 antes e só escolhe a contagem se k ≤ 2n e k ≤ 10⁷.
  Isso responde ao primeiro aviso do enunciado. Como segunda linha de
  defesa, a própria `contagem` se recusa a alocar acima do limite.
- **Tipo das chaves.** Contagem e base só servem para inteiros. O
  escolhedor confere o tipo exato de cada elemento (`set(map(type, v))`),
  então reais, textos, booleanos e listas misturadas vão para as
  comparativas. Isso é o slide 20 em código: quando a chave não é inteira,
  é preciso comparar, e o limite de n log n volta a valer.
- **O escolhedor repassa o que já descobriu.** Quando escolhe contagem ou
  base, entrega mínimo e máximo já calculados (`functools.partial`), para o
  método não percorrer a lista de novo atrás deles.

## 6. Quanto custa rodar o `escolher` — ele compensa?

| cenário | escolher | % do ordenar | 4 passadas em C | 1 passada em Python |
|---|---|---|---|---|
| Aleatório, chaves grandes | 365 µs | 7,9 % | 464 µs | 532 µs |
| Faixa estreita | 281 µs | 57,5 % | 414 µs | 436 µs |
| Quase ordenado | 224 µs | 24,3 % | 489 µs | 436 µs |
| Lista minúscula | 0,1 µs | 3,1 % | 1,3 µs | 0,8 µs |

As duas últimas colunas respondem ao segundo aviso do enunciado ("se o
`escolher` percorrer a lista duas vezes, pode anular o ganho"). Medimos as
mesmas quatro informações (descidas, mínimo, máximo, tipos) de dois jeitos:
quatro passadas usando funções embutidas (`sum(map(...))`, `min`, `max`,
`set(map(type, ...))`), que rodam em C, e **uma** passada com um laço `for`
em Python. Deu praticamente empate. Em CPython, o que custa não é o número
de passadas, é cada iteração executada pelo interpretador. Numa linguagem
compilada a conclusão seria outra: lá, fundir tudo numa passada só seria o
certo.

O que realmente reduziu o custo foi **olhar menos**:

- A contagem de descidas é feita em blocos e **para assim que passa do
  limite de 5 %**. Numa lista desordenada metade dos pares é descida, então
  o escolhedor desiste depois do primeiro bloco e olha só ~1/8 da lista.
- Mínimo e máximo são calculados só se a lista não for quase ordenada, e
  são reaproveitados pela contagem/base. É por isso que, na faixa
  estreita, `ordenar` (489 µs) sai mais barato que contagem (366 µs) +
  escolher (281 µs) somados: a contagem chamada pelo `ordenar` não
  recalcula mínimo e máximo.
- Lista minúscula decide só pelo tamanho, em O(1), sem olhar os elementos.

**Compensa?** Depende do que se compara:

- **Contra quem não sabe nada sobre os dados, compensa muito.** O pior caso
  do `ordenar` é 1,7×; o de qualquer método fixo é no mínimo 16×.
- **Contra quem já sabe o tipo de dado, não compensa.** Se a aplicação só
  ordena notas de 0 a 100, o `ordenar` gasta 34 % a mais do que chamar a
  contagem direto. Na faixa estreita o `escolher` custa
  mais da metade do tempo total, porque a contagem é tão rápida que
  qualquer olhada pesa.
- **Em listas minúsculas o custo relativo é alto** (1,4 µs → 2,4 µs), mas
  absoluto de ~1 µs, gasto em chamadas de função e não em olhar dados. Só
  importaria em quem ordena milhões de listas minúsculas.

Para comparação: o `sorted` do Python (Timsort, escrito em C) leva 1,4 ms
no cenário aleatório e 87 µs no quase ordenado. Ele não entra na tabela
porque não é um dos seis métodos, mas ilustra a mesma ideia deste trabalho:
o Timsort também é adaptativo, detecta trechos já ordenados e usa inserção
em pedaços pequenos.

## 7. Um cenário em que o `escolher` erra

A regra 2 olha as **descidas** (pares v[i] > v[i+1]), mas o custo da
inserção depende das **inversões** (pares i < j com v[i] > v[j]). Quando a
desordem é local, as duas coisas andam juntas. Quando não é, uma única
descida pode esconder milhares de inversões.

Montamos listas ordenadas e trocamos 1 % das posições de dois jeitos:
com um vizinho próximo (como no cenário "quase ordenado") e com uma posição
qualquer (`python -m benchmarks.erro`, resultado em `resultados/erro.md`):

| n | trocas com | descidas | inversões | escolha | ordenar | base | ordenar / melhor |
|---|---|---|---|---|---|---|---|
| 10.000 | vizinhos | 183 (1,8 %) | 1.044 | inserção | 923 µs | 4,86 ms | 1,3× |
| 10.000 | posições quaisquer | 196 (2,0 %) | 684.082 | inserção | 42,6 ms | 5,11 ms | **8,3×** |
| 20.000 | posições quaisquer | 389 (1,9 %) | 2.619.540 | inserção | 139 ms | 10,9 ms | **12,7×** |
| 40.000 | posições quaisquer | 783 (2,0 %) | 11.065.840 | inserção | 623 ms | 24,4 ms | **25,5×** |

O escolhedor vê ~2 % de descidas nos dois tipos de lista e escolhe a
inserção nos dois. Com trocas distantes, cada elemento deslocado precisa
andar em média n/3 posições, as inversões crescem com n², e o erro piora
com o tamanho: de 8× com 10 mil elementos para 25× com 40 mil.

**Por que não consertamos com uma regra mais rígida.** Abaixar o limiar
para log₂n descidas (13, com n = 10 mil) garantiria que a inserção nunca
passasse de O(n log n), mas faria o escolhedor perder o cenário "quase
ordenado" do enunciado, onde a inserção é 6× melhor que a base. Contar
inversões de verdade custa O(n log n), o mesmo que ordenar.

**Como consertaríamos.** A saída mais robusta não é olhar melhor, é
**limitar o prejuízo**: rodar a inserção com um orçamento de deslocamentos
(por exemplo, 4·n·log₂n) e, se ele estourar, abandonar e chamar a base ou a
intercalação. No pior caso isso custa o orçamento gasto mais o método
seguro, ou seja, um fator constante — a mesma ideia do *introsort*, que
abandona a rápida quando a recursão fica funda demais.

## 8. Limitações

- **Python puro.** Os tempos refletem o custo do interpretador: em C ou
  Java as constantes seriam outras e os limiares mudariam (as regras, não).
- **Ruído.** Uma máquina virtual de um núcleo, ±10–20 %. Os limiares foram
  escolhidos longe dos pontos de virada para não depender de diferenças
  pequenas.
- **Valores extremos.** A regra da contagem olha só mínimo e máximo: 9.999
  notas de 0 a 100 e um único 10⁹ bastam para descartar a contagem e ir
  para a base (que ainda é uma boa escolha, mas 2–3× mais lenta que a
  contagem nas notas sem o valor extremo). Também calibramos só com chaves
  uniformes.
- **Estabilidade.** O escolhedor pode escolher métodos não estáveis
  (híbrida). Para ordenar números isso não importa; para ordenar registros
  por uma chave, o `escolher` teria de se restringir aos estáveis.
- **"Híbrida".** Na nossa versão é rápida + inserção abaixo de 16
  elementos.

## 9. Como reproduzir

Ver a seção "Refazendo as medições" do `README.md`. Em resumo:

```bash
python -m unittest -v
python -m benchmarks.calibrar
python -m benchmarks.medir
python -m benchmarks.erro
```
