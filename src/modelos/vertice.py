"""Vertice: um ponto da infraestrutura urbana."""
from dataclasses import dataclass

from src.utilitarios.excecoes import DadoInvalidoError

TIPOS_VALIDOS = ("ponto", "subestacao", "quadro", "estacao", "reservatorio", "distribuicao")


@dataclass(frozen=True)
class Vertice:
    nome: str
    tipo: str = "ponto"

    def __post_init__(self):
        if not isinstance(self.nome, str) or not self.nome.strip():
            raise DadoInvalidoError("O nome do vértice não pode ser vazio.")
        if self.tipo not in TIPOS_VALIDOS:
            raise DadoInvalidoError(
                f"Tipo de ponto inválido: {self.tipo!r}. Use um de {TIPOS_VALIDOS}."
            )
