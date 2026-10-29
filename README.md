# Ordenação adaptativa

Trabalho em dupla de Estruturas de Dados Avançadas (entrega 29/10).

Nenhum método de ordenação ganha sempre. Este repositório reúne os seis
métodos do semestre, um `escolher(v)` que olha a lista e decide qual deles
usar, e as medições que mostram que `ordenar(v)` fica perto do melhor
método em cada cenário, enquanto qualquer escolha fixa perde feio em
pelo menos um.

O relatório completo está em [`RELATORIO.md`](RELATORIO.md).

## Integrantes

- Gabriela de Araújo Reis
- Euclides Carlos Pilon Neto

## Requisitos

Python 3.9 ou mais novo. Só a biblioteca padrão: não há nada para instalar.

## Uso

```python
from ordenacao import ordenar, escolher

ordenar([5, 3, 9, 1])          # [1, 3, 5, 9]

e = escolher(lista)
e.nome                          # 'contagem', 'base', 'insercao', ...
e.motivo                        # 'inteiros com faixa estreita (k = 101 ≤ 2·n)'
e.executar(lista)               # ordena com o método escolhido
```

Os métodos também podem ser chamados diretamente
(`from ordenacao import insercao, intercalacao, rapida, hibrida, contagem, base`)
ou pelo dicionário `ordenacao.METODOS`. Todos devolvem uma lista nova e não
alteram a entrada.

## Estrutura

```
ordenacao/            os seis métodos, um por arquivo, e o escolhedor
  insercao.py
  intercalacao.py
  rapida.py           pivô aleatório + partição em três
  hibrida.py          rápida + inserção abaixo de 16 elementos
  contagem.py         com guarda de memória (recusa faixas enormes)
  base.py             radix LSD, dígitos de 8 bits
  escolhedor.py       escolher(v) e ordenar(v)
benchmarks/
  cenarios.py         geradores de entrada, com semente fixa
  cronometro.py       medição (mediana, coletor de lixo desligado)
  calibrar.py         experimentos que definem as regras do escolher
  medir.py            os 4 cenários x 6 métodos + ordenar
  erro.py             o cenário em que o escolher erra
resultados/           saídas dos scripts acima (markdown e csv)
tests/                testes (unittest)
```

## Rodando os testes

```bash
python -m unittest -v
```

Cobrem, para todos os métodos e para o `ordenar`: lista vazia, um
elemento, todos iguais, já ordenada, invertida, valores negativos, chaves
enormes, além de centenas de listas aleatórias conferidas contra `sorted()`.
Também testam que a contagem recusa faixas grandes *antes* de alocar
memória, que a base é estável a cada passada, que a rápida não estoura a
pilha com valores repetidos e que o escolhedor nunca manda reais ou faixas
enormes para a contagem.

## Refazendo as medições

Sempre da raiz do repositório, com o computador o mais ocioso possível
(feche navegador e IDE; em notebook, deixe na tomada):

```bash
python -m benchmarks.calibrar   # ~3 min  -> resultados/calibracao.md
python -m benchmarks.medir      # ~1 min  -> resultados/cenarios.md e .csv
python -m benchmarks.erro       # ~1 min  -> resultados/erro.md
```

- As entradas usam sementes fixas: todo mundo mede exatamente as mesmas listas.
- Cada tempo é a **mediana** de no mínimo 5 execuções (até juntar 0,3 s);
  chamadas muito rápidas são repetidas em lote e divididas, para o relógio
  conseguir medir. O coletor de lixo fica desligado durante a medição.
- A inserção no cenário aleatório leva mais de um segundo por execução:
  é de propósito (é O(n²)).
- Os tempos absolutos mudam de máquina para máquina; as **razões** entre os
  métodos (quem ganha e por quanto) mudam bem menos. Em máquina virtual ou
  compartilhada, espere ±10–20 % de ruído entre execuções.

Se rodarem `calibrar` numa máquina muito diferente e algum ponto de virada
mudar, os limiares ficam todos no topo de `ordenacao/escolhedor.py`, cada
um com a referência da seção da calibração de onde veio.
