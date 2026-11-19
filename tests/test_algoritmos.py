"""Testes do núcleo matemático: Prim e Kruskal."""
import itertools
import unittest

from src.algoritmos.kruskal import kruskal
from src.algoritmos.prim import prim
from src.dados.exemplos import (CUSTO_EXEMPLO_ARTIGO, rede_exemplo_artigo,
                                rede_exemplo_desconectada, rede_exemplo_simples)
from src.dados.gerador import gerar_rede_sintetica
from src.modelos.grafo import Grafo
from src.modelos.union_find import UnionFind
from src.utilitarios.excecoes import DadoInvalidoError, RedeDesconectadaError


def custo_minimo_por_forca_bruta(grafo):
    """Testa todas as combinações de |V|-1 arestas (apenas para redes pequenas)."""
    n = grafo.quantidade_vertices
    melhor = None
    for combinacao in itertools.combinations(grafo.arestas, n - 1):
        uf = UnionFind(grafo.nomes_vertices)
        if all(uf.unir(a.origem, a.destino) for a in combinacao):   # sem ciclos => árvore
            custo = sum(a.custo for a in combinacao)
            melhor = custo if melhor is None else min(melhor, custo)
    return melhor


class TestExemplos(unittest.TestCase):
    def test_exemplo_simples(self):
        g = rede_exemplo_simples()
        self.assertEqual(prim(g).custo_total, 9000)
        self.assertEqual(kruskal(g).custo_total, 9000)

    def test_exemplo_do_artigo_custa_18500(self):
        g = rede_exemplo_artigo()
        self.assertEqual(prim(g).custo_total, CUSTO_EXEMPLO_ARTIGO)
        self.assertEqual(kruskal(g).custo_total, CUSTO_EXEMPLO_ARTIGO)

    def test_exemplo_do_artigo_mesmas_arestas_e_sete_conexoes(self):
        g = rede_exemplo_artigo()
        self.assertEqual(prim(g).pares(), kruskal(g).pares())
        self.assertEqual(len(prim(g)), g.quantidade_vertices - 1)

    def test_prim_com_vertice_inicial_diferente(self):
        g = rede_exemplo_artigo()
        for inicio in g.nomes_vertices:
            self.assertEqual(prim(g, inicio).custo_total, CUSTO_EXEMPLO_ARTIGO)

    def test_prim_vertice_inicial_inexistente(self):
        with self.assertRaises(DadoInvalidoError):
            prim(rede_exemplo_simples(), "Z")


class TestRedeDesconectada(unittest.TestCase):
    def test_prim_e_kruskal_levantam_erro(self):
        g = rede_exemplo_desconectada()
        for algoritmo in (prim, kruskal):
            with self.subTest(algoritmo=algoritmo.__name__):
                with self.assertRaises(RedeDesconectadaError) as ctx:
                    algoritmo(g)
                # Rede desconectada em 2 ilhas: Norte (3 vértices) e Sul (2 vértices + 1 estacao)
                self.assertEqual(sorted(ctx.exception.componentes),
                                 [["Est-Sul", "Q-Sul1", "Sub-B"],
                                  ["Q-Norte1", "Q-Norte2", "Sub-A"]])

    def test_erro_e_um_value_error(self):
        with self.assertRaises(ValueError):
            prim(rede_exemplo_desconectada())


class TestCorretude(unittest.TestCase):
    def test_prim_e_kruskal_concordam_em_redes_aleatorias(self):
        for semente in range(25):
            g = gerar_rede_sintetica(30, semente=semente)
            with self.subTest(semente=semente):
                self.assertEqual(prim(g).custo_total, kruskal(g).custo_total)
                self.assertEqual(len(prim(g)), 29)
                self.assertEqual(len(kruskal(g)), 29)

    def test_custo_igual_ao_minimo_por_forca_bruta(self):
        for semente in range(15):
            g = gerar_rede_sintetica(6, semente=semente, arestas_por_vertice=2)
            esperado = custo_minimo_por_forca_bruta(g)
            with self.subTest(semente=semente):
                self.assertEqual(prim(g).custo_total, esperado)
                self.assertEqual(kruskal(g).custo_total, esperado)

    def test_resultado_e_arvore_sem_ciclos_que_cobre_todos_os_vertices(self):
        g = gerar_rede_sintetica(40, semente=7)
        for algoritmo in (prim, kruskal):
            arvore = algoritmo(g)
            uf = UnionFind(g.nomes_vertices)
            self.assertTrue(all(uf.unir(a.origem, a.destino) for a in arvore.arestas))
            self.assertEqual(uf.quantidade_conjuntos, 1)


class TestVazioEUnico(unittest.TestCase):
    def test_grafo_vazio(self):
        self.assertEqual(len(prim(Grafo())), 0)
        self.assertEqual(len(kruskal(Grafo())), 0)


if __name__ == "__main__":
    unittest.main()
