"""Camada de aplicação: casos de uso do GridPower (RF01 a RF09)."""
import math
from dataclasses import dataclass

from src.algoritmos.kruskal import kruskal
from src.algoritmos.prim import prim
from src.modelos.grafo import Grafo
from src.modelos.mst import MST


@dataclass
class ResultadoComparacao:
    prim: MST
    kruskal: MST
    custos_equivalentes: bool
    mesmas_arestas: bool
    justificativa: str

    @property
    def custo_prim(self):
        return self.prim.custo_total

    @property
    def custo_kruskal(self):
        return self.kruskal.custo_total


class ServicoRede:
    def __init__(self, grafo=None):
        self.grafo = grafo if grafo is not None else Grafo()

    # RF01
    def cadastrar_ponto(self, nome, tipo="ponto"):
        return self.grafo.adicionar_vertice(nome, tipo)

    # RF02 e RF03
    def cadastrar_conexao(self, origem, destino, custo):
        return self.grafo.adicionar_aresta(origem, destino, custo)

    # RF05
    def executar_prim(self, inicio=None):
        return prim(self.grafo, inicio)

    # RF06
    def executar_kruskal(self):
        return kruskal(self.grafo)

    # RF08
    @staticmethod
    def calcular_custo_total(mst):
        return mst.custo_total

    # RF09
    def verificar_conectividade(self):
        """Retorna (conexa, componentes)."""
        componentes = self.grafo.componentes_conexos()
        return len(componentes) <= 1, componentes

    # RF07
    def comparar(self):
        """Executa Prim e Kruskal sobre a mesma rede e compara os resultados."""
        arvore_prim = self.executar_prim()
        arvore_kruskal = self.executar_kruskal()
        equivalentes = math.isclose(arvore_prim.custo_total, arvore_kruskal.custo_total,
                                    rel_tol=1e-9, abs_tol=1e-9)
        mesmas = arvore_prim.pares() == arvore_kruskal.pares()
        custos = [a.custo for a in self.grafo.arestas]
        ha_empates = len(set(custos)) < len(custos)
        if not equivalentes:
            texto = "ATENÇÃO: os custos diferem. Há erro em alguma das implementações."
        elif mesmas and not ha_empates:
            texto = ("Os dois algoritmos escolheram exatamente as mesmas conexões. Como todos "
                     "os custos da rede são distintos, a AGM é única.")
        elif mesmas:
            texto = ("Os dois algoritmos escolheram as mesmas conexões, mas há custos repetidos "
                     "na rede: podem existir outras AGMs de mesmo custo, e o critério de "
                     "desempate (custo, origem, destino) levou ambos à mesma árvore. Pela "
                     "propriedade do corte, todas as AGMs de um grafo têm o mesmo custo.")
        else:
            texto = ("Os custos são iguais, mas as conexões escolhidas diferem: existem várias "
                     "AGMs com o mesmo custo mínimo (empates). Pela propriedade do corte, toda "
                     "escolha gananciosa de Prim ou Kruskal leva a uma AGM, e todas as AGMs de "
                     "um grafo têm o mesmo custo.")
        return ResultadoComparacao(arvore_prim, arvore_kruskal, equivalentes, mesmas, texto)
