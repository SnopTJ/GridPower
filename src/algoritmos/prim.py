"""Algoritmo de Prim com lista de adjacência e fila de prioridade (heap). O(E log V)."""
import heapq

from src.modelos.aresta import Aresta
from src.modelos.mst import MST
from src.utilitarios.excecoes import DadoInvalidoError, RedeDesconectadaError


def prim(grafo, inicio=None):
    """Retorna a AGM. Levanta RedeDesconectadaError se a rede não for conexa."""
    nomes = grafo.nomes_vertices
    arvore = MST(algoritmo="Prim")
    if not nomes:
        return arvore
    if inicio is None:
        inicio = nomes[0]
    elif inicio not in nomes:
        raise DadoInvalidoError(f"Vértice inicial inexistente: {inicio!r}.")

    adjacencia = grafo.lista_adjacencia()
    visitados = {inicio}
    fila = [(custo, inicio, v) for custo, v in adjacencia[inicio]]
    heapq.heapify(fila)

    while fila and len(visitados) < len(nomes):
        custo, u, v = heapq.heappop(fila)
        if v in visitados:                 # entrada obsoleta: descarta
            continue
        visitados.add(v)
        arvore.arestas.append(Aresta(u, v, custo))
        for custo2, x in adjacencia[v]:
            if x not in visitados:
                heapq.heappush(fila, (custo2, v, x))

    if len(visitados) < len(nomes):
        raise RedeDesconectadaError(grafo.componentes_conexos())
    return arvore
