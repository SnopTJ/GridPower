"""Aresta: uma conexão candidata (cabeamento ou tubulação) com custo em R$."""
import math
from dataclasses import dataclass

from src.utilitarios.excecoes import DadoInvalidoError


@dataclass(frozen=True)
class Aresta:
    origem: str
    destino: str
    custo: float

    def __post_init__(self):
        if self.origem == self.destino:
            raise DadoInvalidoError("Não é permitido conectar um vértice a ele mesmo.")
        if (isinstance(self.custo, bool) or not isinstance(self.custo, (int, float))
                or not math.isfinite(self.custo) or self.custo < 0):
            raise DadoInvalidoError("O custo deve ser um número finito e não negativo.")

    @property
    def chave(self):
        """Identifica a conexão sem depender da ordem (A-B == B-A)."""
        return frozenset((self.origem, self.destino))
