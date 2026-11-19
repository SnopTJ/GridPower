"""Algoritmo de Kruskal com Union-Find. O(E log E) = O(E log V)."""
from src.modelos.mst import MST
from src.modelos.union_find import UnionFind
from src.utilitarios.excecoes import RedeDesconectadaError


def kruskal(grafo):
    """Retorna a AGM. Levanta RedeDesconectadaError se a rede não for conexa."""
    nomes = grafo.nomes_vertices
    arvore = MST(algoritmo="Kruskal")
    alvo = max(len(nomes) - 1, 0)
    if alvo == 0:
        return arvore

    uf = UnionFind(nomes)
    for a in sorted(grafo.arestas, key=lambda a: (a.custo, a.origem, a.destino)):
        if uf.unir(a.origem, a.destino):   # só aceita se não formar ciclo
            arvore.arestas.append(a)
            if len(arvore.arestas) == alvo:
                break

    if len(arvore.arestas) != alvo:
        raise RedeDesconectadaError(grafo.componentes_conexos())
    return arvore
