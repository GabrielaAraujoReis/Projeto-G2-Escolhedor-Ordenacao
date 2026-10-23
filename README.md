# Projeto G2 - Escolhedor de Ordenacao

Projeto em dupla da disciplina de **Estruturas de Dados Avancadas**, com entrega prevista para 29/10.

## Objetivo

Construir um ordenador que analisa uma lista de inteiros, escolhe automaticamente o metodo mais adequado e executa a ordenacao. A escolha sera comparada, nos mesmos dados, com seis metodos fixos:

- insercao;
- intercalacao;
- rapida com pivo aleatorio;
- hibrida (rapida + insercao);
- contagem;
- base (Radix Sort).

O projeto esta na fase de **estrutura inicial**. Os algoritmos, as regras do escolhedor e as medicoes ainda serao implementados e validados. Nenhum resultado experimental foi preenchido antecipadamente.

## Estrutura do repositorio

```text
.
|-- algoritmos/
|   |-- __init__.py
|   |-- insercao.py
|   |-- intercalacao.py
|   |-- rapida.py
|   |-- hibrida.py
|   |-- contagem.py
|   `-- base.py
|-- resultados/
|   `-- .gitkeep
|-- escolher.py
|-- medir.py
|-- testes.py
|-- RELATORIO.md
`-- README.md
```

## Planejamento tecnico

`escolher(v)` devera observar somente caracteristicas baratas da entrada, como:

- quantidade de elementos;
- menor e maior valor, para estimar a faixa;
- quantidade de pares consecutivos fora de ordem, como aproximacao do grau de ordenacao.

Sempre que possivel, essas informacoes serao obtidas em **uma unica passagem**. Isso evita que o custo da decisao elimine o ganho da ordenacao escolhida.

Antes de selecionar a ordenacao por contagem, o programa devera limitar a faixa de valores. Esse metodo custa `O(n + k)` e usa memoria proporcional a `k`, portanto uma faixa muito grande pode tornar sua execucao lenta ou ate inviavel. A ordenacao por base sera estudada como alternativa para inteiros com faixa ampla; suas passadas por digito precisam ser estaveis.

As regras definitivas e seus limites serao definidos a partir das medicoes, nao por suposicao.

## Cenarios obrigatorios

O benchmark comparara o ordenador automatico e os seis metodos fixos em quatro cenarios:

1. lista aleatoria com chaves grandes;
2. lista com faixa estreita de valores;
3. lista quase ordenada;
4. lista minuscula.

Cada execucao devera usar copias dos mesmos dados de entrada para manter a comparacao justa.

## Testes obrigatorios

Os testes cobrirao:

- lista vazia;
- lista com um elemento;
- todos os valores iguais;
- lista ja ordenada;
- lista invertida;
- valores negativos.

Quando a implementacao estiver pronta, execute:

```bash
python -m unittest -v testes.py
```

## Como refazer as medicoes

Depois da implementacao dos algoritmos e do benchmark:

```bash
python medir.py
```

O programa devera registrar em `resultados/` os dados brutos usados no `RELATORIO.md`. Para reduzir ruido, cada caso sera repetido varias vezes e o relatorio informara o tamanho das listas, a semente aleatoria, a quantidade de repeticoes e a medida de tempo escolhida.

## Etapas sugeridas

1. Implementar e testar os seis metodos.
2. Medir caracteristicas das entradas em uma passagem.
3. Definir e implementar `escolher(v)` e `ordenar(v)`.
4. Executar os quatro cenarios contra todos os metodos.
5. Registrar os resultados e concluir o relatorio.

## Situacao atual

- [x] Estrutura inicial do repositorio
- [x] Roteiro inicial do relatorio
- [ ] Implementacao dos seis metodos
- [ ] Implementacao do escolhedor
- [ ] Testes completos
- [ ] Medicoes reproduziveis
- [ ] Analise final

