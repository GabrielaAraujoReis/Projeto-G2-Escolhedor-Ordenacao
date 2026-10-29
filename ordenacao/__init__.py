"""Métodos de ordenação do semestre."""

from .insercao import insercao
from .intercalacao import intercalacao
from .rapida import rapida
from .hibrida import hibrida
from .contagem import contagem, FaixaGrandeDemais
from .base import base

# Os seis métodos fixos, na ordem em que aparecem nas tabelas.
METODOS = {
    "insercao": insercao,
    "intercalacao": intercalacao,
    "rapida": rapida,
    "hibrida": hibrida,
    "contagem": contagem,
    "base": base,
}
