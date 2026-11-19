"""Casos de teste da seção A.9 do documento do projeto GridPower.

1. Grafo vazio            5. Custos diferentes
2. Um único vértice      6. MST única
3. Grafo desconectado    7. Múltiplas MST possíveis
4. Arestas duplicadas    8. Custos iguais
"""
import unittest

from src.algoritmos.kruskal import kruskal
from src.algoritmos.prim import prim
from src.modelos.grafo import Grafo
from src.utilitarios.excecoes import RedeDesconectadaError

ALGORITMOS = (("Prim", prim), ("Kruskal", kruskal))


def montar(vertices, conexoes):
    g = Grafo()
    for v in vertices:
        g.adicionar_vertice(v)
    for a, b, custo in conexoes:
        g.adicionar_aresta(a, b, custo)
    return g


class TestCasosA9(unittest.TestCase):
    def test_1_grafo_vazio(self):
        for nome, algoritmo in ALGORITMOS:
            with self.subTest(algoritmo=nome):
                arvore = algoritmo(Grafo())
                self.assertEqual(len(arvore), 0)
                self.assertEqual(arvore.custo_total, 0)

    def test_2_um_unico_vertice(self):
        g = montar(["A"], [])
        for nome, algoritmo in ALGORITMOS:
            with self.subTest(algoritmo=nome):
                arvore = algoritmo(g)
                self.assertEqual(len(arvore), 0)
                self.assertEqual(arvore.custo_total, 0)

    def test_3_grafo_desconectado(self):
        g = montar(["A", "B"], [])
        for nome, algoritmo in ALGORITMOS:
            with self.subTest(algoritmo=nome), self.assertRaises(RedeDesconectadaError):
                algoritmo(g)

    def test_4_arestas_duplicadas(self):
        g = montar(["A", "B"], [("A", "B", 4), ("A", "B", 2), ("B", "A", 3)])
        for nome, algoritmo in ALGORITMOS:
            with self.subTest(algoritmo=nome):
                arvore = algoritmo(g)
                self.assertEqual(len(arvore), 1)
                self.assertEqual(arvore.custo_total, 2)

    def test_5_custos_diferentes(self):
        g = montar("ABC", [("A", "B", 1), ("B", "C", 2), ("A", "C", 3)])
        for nome, algoritmo in ALGORITMOS:
            with self.subTest(algoritmo=nome):
                self.assertEqual(algoritmo(g).custo_total, 3)

    def test_6_mst_unica(self):
        g = montar("ABCD", [("A", "B", 4), ("A", "C", 2), ("B", "C", 5), ("B", "D", 3), ("C", "D", 6)])
        esperado = {frozenset("AC"), frozenset("BD"), frozenset("AB")}
        self.assertEqual(prim(g).pares(), esperado)
        self.assertEqual(kruskal(g).pares(), esperado)

    def test_7_multiplas_mst_mesmo_custo(self):
        # ciclo de 4 vértices com custos iguais: 4 AGMs possíveis, todas com custo 3
        g = montar("ABCD", [("A", "B", 1), ("B", "C", 1), ("C", "D", 1), ("D", "A", 1)])
        for nome, algoritmo in ALGORITMOS:
            with self.subTest(algoritmo=nome):
                arvore = algoritmo(g)
                self.assertEqual(len(arvore), 3)
                self.assertEqual(arvore.custo_total, 3)

    def test_8_custos_iguais(self):
        g = montar("ABC", [("A", "B", 1), ("B", "C", 1), ("A", "C", 1)])
        for nome, algoritmo in ALGORITMOS:
            with self.subTest(algoritmo=nome):
                arvore = algoritmo(g)
                self.assertEqual(len(arvore), 2)
                self.assertEqual(arvore.custo_total, 2)


if __name__ == "__main__":
    unittest.main()
