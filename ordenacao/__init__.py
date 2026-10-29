"""Métodos de ordenação do semestre e o escolhedor automático."""

from .insercao import insercao
from .intercalacao import intercalacao
from .rapida import rapida
from .hibrida import hibrida
from .contagem import contagem, FaixaGrandeDemais
from .base import base
from .escolhedor import Escolha, escolher, ordenar

# Os seis métodos fixos, na ordem em que aparecem nas tabelas.
METODOS = {
    "insercao": insercao,
    "intercalacao": intercalacao,
    "rapida": rapida,
    "hibrida": hibrida,
    "contagem": contagem,
    "base": base,
}
