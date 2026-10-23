"""Algoritmos de ordenacao usados no Projeto G2."""

from .base import ordenacao_base
from .contagem import ordenacao_contagem
from .hibrida import ordenacao_hibrida
from .insercao import ordenacao_insercao
from .intercalacao import ordenacao_intercalacao
from .rapida import ordenacao_rapida

__all__ = [
    "ordenacao_base",
    "ordenacao_contagem",
    "ordenacao_hibrida",
    "ordenacao_insercao",
    "ordenacao_intercalacao",
    "ordenacao_rapida",
]

