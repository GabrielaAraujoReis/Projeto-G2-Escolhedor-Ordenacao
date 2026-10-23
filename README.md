# Projeto G2 — Escolhedor de Ordenação

Este projeto implementa um ordenador que seleciona um algoritmo conforme as características da lista de entrada. A seleção será comparada com seis métodos fixos em quatro cenários, avaliando também o custo de analisar os dados.

> **Situação:** estrutura inicial do trabalho acadêmico em dupla. As implementações e os resultados experimentais ainda estão pendentes.

## Decisões de arquitetura

Os algoritmos ficam em módulos separados dentro de `algoritmos/`, enquanto `escolher.py` concentra a decisão automática e `medir.py` concentra os experimentos. Essa separação permite testar e comparar cada método de forma independente.

O projeto prevê funções que recebem uma lista de inteiros e retornam uma nova lista ordenada. A entrada original deverá permanecer inalterada, facilitando a execução dos métodos sobre cópias equivalentes dos mesmos dados.

| Método | Justificativa para inclusão | Custo teórico esperado |
|---|---|---|
| Inserção | Adequada a entradas pequenas ou quase ordenadas; será avaliada como alternativa para trechos curtos. | Melhor caso `O(n)`; pior caso `O(n²)`. |
| Intercalação (Merge Sort) | Referência por comparação com tempo `O(n log n)` e comportamento previsível; requer memória auxiliar `O(n)`. | `O(n log n)` em tempo. |
| Rápida com pivô aleatório | Método por comparação com desempenho esperado `O(n log n)`; o pior caso continua sendo `O(n²)`. | Esperado `O(n log n)`; pior caso `O(n²)`. |
| Híbrida | Combina Quicksort em trechos maiores com Inserção em trechos pequenos; o ponto de troca deverá ser avaliado experimentalmente. | Depende do corte e da entrada. |
| Contagem (Counting Sort) | Explora chaves inteiras em uma faixa limitada; o custo e a memória dependem da amplitude da faixa `k`. | `O(n + k)` em tempo e memória auxiliar proporcional a `k`. |
| Base (Radix Sort) | Permite tratar inteiros de faixa ampla por dígitos; cada passada precisa ser estável. | `O(d · n)`, sendo `d` a quantidade de dígitos processados. |

O seletor deverá extrair tamanho, mínimo, máximo e uma medida simples de desordem em uma única passagem, sempre que possível. Isso reduz o custo da decisão. A ordenação por contagem só deverá ser considerada quando a faixa estimada respeitar um limite seguro de memória. Os limites e as regras finais serão definidos a partir dos experimentos.

## Pré-requisitos

- Python **3.12.14** como versão de referência deste projeto;
- Git **2.53.0.windows.3** no ambiente Windows usado para configurar o repositório;
- nenhuma biblioteca externa nesta estrutura inicial: os arquivos usam apenas a biblioteca padrão do Python.

Os arquivos declaram tipos como `list[int]`, disponíveis a partir do Python 3.9. Para reproduzir os resultados nas mesmas condições, deve-se utilizar Python 3.12.14. A versão do Git registrada acima documenta o ambiente de configuração; o programa Python não depende do Git durante a execução.

## Execução

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/GabrielaAraujoReis/Projeto-G2-Escolhedor-Ordenacao.git
cd Projeto-G2-Escolhedor-Ordenacao
```

Confirme a versão do Python:

```bash
python --version
```

A saída esperada para o ambiente de referência é:

```text
Python 3.12.14
```

No Windows, caso o comando `python` não esteja disponível, pode-se usar o inicializador `py -3.12` nos comandos seguintes.

Execute a suíte de testes:

```bash
python -m unittest -v testes.py
```

Na estrutura atual, a classe de testes fica marcada como ignorada porque os seis algoritmos ainda são esqueletos. Portanto, a execução confirma apenas que a suíte pode ser carregada; ela não valida a ordenação. Após a implementação, os testes deverão cobrir lista vazia, um elemento, valores iguais, lista ordenada, lista invertida e valores negativos.

Após implementar os algoritmos, o seletor e os cenários do benchmark, as medições serão executadas com:

```bash
python medir.py
```

No estado atual, esse comando informa que o benchmark está pendente e não produz resultados. Os dados experimentais deverão ser registrados em `resultados/` antes de preencher a tabela do [relatório](RELATORIO.md).

## Estrutura do repositório

```text
.
├── algoritmos/
│   ├── __init__.py
│   ├── insercao.py
│   ├── intercalacao.py
│   ├── rapida.py
│   ├── hibrida.py
│   ├── contagem.py
│   └── base.py
├── resultados/
│   └── .gitkeep
├── escolher.py
├── medir.py
├── testes.py
├── RELATORIO.md
└── README.md
```
