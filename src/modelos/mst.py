"""MST: resultado de um algoritmo de árvore geradora mínima."""
from dataclasses import dataclass, field


@dataclass
class MST:
    arestas: list = field(default_factory=list)
    algoritmo: str = ""

    @property
    def custo_total(self):
        return sum(a.custo for a in self.arestas)

    def pares(self):
        """Conjunto de conexões escolhidas, sem ordem (útil para comparar algoritmos)."""
        return {a.chave for a in self.arestas}

    def __len__(self):
        return len(self.arestas)
