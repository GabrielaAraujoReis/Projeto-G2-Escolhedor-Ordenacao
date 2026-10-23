# Relatorio - Projeto G2: Escolhedor de Ordenacao

> Documento inicial. Os campos de resultados e conclusoes serao preenchidos somente depois da execucao dos experimentos.

## 1. Objetivo

O objetivo do projeto e construir um mecanismo que examine uma lista de inteiros, escolha um metodo de ordenacao adequado para suas caracteristicas e execute a ordenacao. A solucao automatica sera comparada com cada um dos seis metodos usados de forma fixa.

## 2. Metodos analisados

- Insercao
- Intercalacao
- Rapida com pivo aleatorio
- Hibrida (rapida + insercao)
- Contagem
- Base (Radix Sort)

## 3. Metodologia

### 3.1 Ambiente de execucao

- Computador/processador: a preencher
- Sistema operacional: a preencher
- Versao do Python: a preencher
- Semente aleatoria: a preencher
- Repeticoes por caso: a preencher
- Medida apresentada: a preencher

### 3.2 Comparacao justa

Cada metodo recebera uma copia da mesma lista de entrada. A correcao da saida sera verificada antes de registrar o tempo. O custo de `escolher(v)` sera medido separadamente e tambem fara parte do tempo total de `ordenar(v)`.

### 3.3 Cenarios

1. **Aleatorio com chaves grandes:** tamanho e faixa a definir.
2. **Faixa estreita:** tamanho e faixa a definir.
3. **Quase ordenado:** criterio de perturbacao a definir.
4. **Lista minuscula:** tamanho a definir.

## 4. Regras do escolhedor

As regras definitivas serao registradas depois dos experimentos. A versao inicial investigara:

- tamanho da lista;
- faixa `maximo - minimo + 1`;
- proporcao de pares consecutivos fora de ordem.

Essas caracteristicas deverao ser calculadas em uma unica passagem `O(n)`. A ordenacao por contagem so podera ser escolhida se a faixa estimada respeitar um limite seguro de tempo e memoria.

### Tabela de regras

| Condicao observada | Metodo escolhido | Justificativa experimental |
|---|---|---|
| A preencher | A preencher | A preencher |

## 5. Resultados

Tempos na unidade que sera indicada apos as medicoes.

| Cenario | `ordenar` | Insercao | Intercalacao | Rapida | Hibrida | Contagem | Base |
|---|---:|---:|---:|---:|---:|---:|---:|
| Aleatorio com chaves grandes | - | - | - | - | - | - | - |
| Faixa estreita | - | - | - | - | - | - | - |
| Quase ordenado | - | - | - | - | - | - | - |
| Lista minuscula | - | - | - | - | - | - | - |

## 6. Vencedor de cada cenario

| Cenario | Metodo vencedor | Explicacao |
|---|---|---|
| Aleatorio com chaves grandes | A preencher | A preencher |
| Faixa estreita | A preencher | A preencher |
| Quase ordenado | A preencher | A preencher |
| Lista minuscula | A preencher | A preencher |

## 7. Custo de `escolher(v)`

### Analise assintotica

A inspecao planejada percorre a entrada uma vez, portanto custa `O(n)` em tempo e `O(1)` em memoria adicional. Essa analise devera ser confirmada na implementacao final.

### Medicao

| Cenario | Tempo de `escolher` | Tempo total de `ordenar` | Percentual gasto na escolha |
|---|---:|---:|---:|
| Aleatorio com chaves grandes | - | - | - |
| Faixa estreita | - | - | - |
| Quase ordenado | - | - | - |
| Lista minuscula | - | - | - |

Conclusao sobre a compensacao do custo: a preencher.

## 8. Um cenario em que o escolhedor erra

- Entrada e caracteristicas: a preencher
- Metodo escolhido: a preencher
- Metodo que venceu: a preencher
- Motivo provavel do erro: a preencher
- Possivel melhoria da regra: a preencher

## 9. Limitacoes

- A ordenacao por contagem pode consumir memoria excessiva quando a faixa de valores e grande.
- Metodos lineares considerados no projeto dependem de chaves inteiras ou de uma transformacao adequada para inteiros.
- O tempo observado depende do computador, da versao do Python e do ruido do ambiente.
- Uma heuristica baseada em poucas caracteristicas pode escolher um metodo que nao seja o mais rapido em casos de fronteira.

## 10. Conclusao

A preencher depois dos testes e das medicoes.

