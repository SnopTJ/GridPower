"""Exceções do GridPower.

Todas herdam de ValueError para continuar compatíveis com código que
captura ValueError (como o protótipo inicial).
"""


class ErroGridPower(ValueError):
    """Erro base do sistema."""


class DadoInvalidoError(ErroGridPower):
    """Entrada inválida: nome vazio, custo negativo, vértice inexistente, laço..."""


class RedeDesconectadaError(ErroGridPower):
    """A rede não é conexa, então não existe árvore geradora (RF09)."""

    def __init__(self, componentes):
        self.componentes = [sorted(c) for c in componentes]
        partes = "; ".join("{" + ", ".join(c) + "}" for c in self.componentes)
        super().__init__(
            f"A rede é desconectada ({len(self.componentes)} componentes): {partes}. "
            "Não existe árvore geradora."
        )
