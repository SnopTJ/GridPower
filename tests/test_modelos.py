"""Testes das estruturas de dados: Vertice, Aresta, Grafo, UnionFind e MST."""
import unittest

from src.modelos.aresta import Aresta
from src.modelos.grafo import Grafo
from src.modelos.mst import MST
from src.modelos.union_find import UnionFind
from src.modelos.vertice import Vertice
from src.utilitarios.excecoes import DadoInvalidoError


class TestVertice(unittest.TestCase):
    def test_vertice_valido(self):
        self.assertEqual(Vertice("S1", "subestacao").tipo, "subestacao")

    def test_nome_vazio(self):
        with self.assertRaises(DadoInvalidoError):
            Vertice("   ")

    def test_tipo_invalido(self):
        with self.assertRaises(DadoInvalidoError):
            Vertice("A", "foguete")


class TestAresta(unittest.TestCase):
    def test_chave_nao_depende_da_ordem(self):
        self.assertEqual(Aresta("A", "B", 1).chave, Aresta("B", "A", 1).chave)

    def test_laco(self):
        with self.assertRaises(DadoInvalidoError):
            Aresta("A", "A", 1)

    def test_custo_invalido(self):
        for custo in (-1, "caro", None, True, float("nan"), float("inf")):
            with self.subTest(custo=custo), self.assertRaises(DadoInvalidoError):
                Aresta("A", "B", custo)

    def test_custo_zero_e_permitido(self):
        self.assertEqual(Aresta("A", "B", 0).custo, 0)


class TestGrafo(unittest.TestCase):
    def setUp(self):
        self.g = Grafo()
        for nome in "ABC":
            self.g.adicionar_vertice(nome)

    def test_vertice_duplicado(self):
        with self.assertRaises(DadoInvalidoError):
            self.g.adicionar_vertice("A")

    def test_nome_invalido(self):
        for nome in (None, "", "   ", 123, 4.5):
            with self.subTest(nome=nome), self.assertRaises(DadoInvalidoError):
                self.g.adicionar_vertice(nome)

    def test_nome_invalido_lista(self):
        with self.assertRaises(DadoInvalidoError):
            self.g.adicionar_vertice(["A", "B"])

    def test_nome_invalido_dic(self):
        with self.assertRaises(DadoInvalidoError):
            self.g.adicionar_vertice({"nome": "A"})

    def test_nome_invalido_bytes(self):
        with self.assertRaises(DadoInvalidoError):
            self.g.adicionar_vertice(b"Estacao")

    def test_nome_com_espacos_e_strip(self):
        v = self.g.adicionar_vertice("  D  ")
        self.assertEqual(v.nome, "D")

    def test_aresta_origem_invalido(self):
        with self.assertRaises(DadoInvalidoError):
            self.g.adicionar_aresta([], "B", 1)

    def test_aresta_destino_invalido(self):
        with self.assertRaises(DadoInvalidoError):
            self.g.adicionar_aresta("A", {}, 1)

    def test_aresta_vazia(self):
        with self.assertRaises(DadoInvalidoError):
            self.g.adicionar_aresta("", "B", 1)

    def test_aresta_destino_vazio(self):
        with self.assertRaises(DadoInvalidoError):
            self.g.adicionar_aresta("A", "", 1)

    def test_vertice_inexistente(self):
        with self.assertRaises(DadoInvalidoError):
            self.g.adicionar_aresta("A", "Z", 1)

    def test_laco(self):
        with self.assertRaises(DadoInvalidoError):
            self.g.adicionar_aresta("A", "A", 1)

    def test_aresta_duplicada_mantem_a_mais_barata(self):
        self.g.adicionar_aresta("A", "B", 4)
        self.g.adicionar_aresta("B", "A", 2)
        self.g.adicionar_aresta("A", "B", 3)
        self.assertEqual(self.g.quantidade_arestas, 1)
        self.assertEqual(self.g.arestas[0].custo, 2)

    def test_lista_adjacencia(self):
        self.g.adicionar_aresta("A", "B", 5)
        adj = self.g.lista_adjacencia()
        self.assertEqual(adj["A"], [(5.0, "B")])
        self.assertEqual(adj["B"], [(5.0, "A")])
        self.assertEqual(adj["C"], [])

    def test_componentes_conexos(self):
        self.g.adicionar_aresta("A", "B", 1)
        componentes = sorted(sorted(c) for c in self.g.componentes_conexos())
        self.assertEqual(componentes, [["A", "B"], ["C"]])
        self.assertFalse(self.g.eh_conexo())
        self.g.adicionar_aresta("B", "C", 1)
        self.assertTrue(self.g.eh_conexo())


class TestUnionFind(unittest.TestCase):
    def test_unir_e_encontrar(self):
        uf = UnionFind(range(5))
        self.assertEqual(uf.quantidade_conjuntos, 5)
        self.assertTrue(uf.unir(0, 1))
        self.assertTrue(uf.unir(1, 2))
        self.assertFalse(uf.unir(0, 2))          # já no mesmo conjunto
        self.assertTrue(uf.conectados(0, 2))
        self.assertFalse(uf.conectados(0, 3))
        self.assertEqual(uf.quantidade_conjuntos, 3)

    def test_compressao_de_caminho(self):
        uf = UnionFind(range(6))
        uf.pai = {0: 0, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4}   # cadeia longa
        raiz = uf.encontrar(5)
        self.assertEqual(raiz, 0)
        self.assertTrue(all(uf.pai[x] == 0 for x in range(6)))

    def test_apelidos_em_ingles(self):
        uf = UnionFind("ab")
        self.assertTrue(uf.union("a", "b"))
        self.assertEqual(uf.find("a"), uf.find("b"))


class TestMST(unittest.TestCase):
    def test_custo_total_e_pares(self):
        arvore = MST([Aresta("A", "B", 2), Aresta("C", "B", 3)], "Teste")
        self.assertEqual(arvore.custo_total, 5)
        self.assertEqual(len(arvore), 2)
        self.assertEqual(arvore.pares(), {frozenset("AB"), frozenset("BC")})


if __name__ == "__main__":
    unittest.main()
