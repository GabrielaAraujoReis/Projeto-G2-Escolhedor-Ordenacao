"""Métodos de ordenação do semestre."""

from .insercao import insercao
from .intercalacao import intercalacao

# Os métodos fixos, na ordem em que aparecem nas tabelas.
# Cada etapa do trabalho registra aqui os métodos novos; os testes de
# tests/test_metodos.py passam a cobri-los automaticamente.
METODOS = {
    "insercao": insercao,
    "intercalacao": intercalacao,
}
