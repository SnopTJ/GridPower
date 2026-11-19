"""Testes para cobrir os caminhos de saída: gráficos, relatórios e desenhos (Sprint 5)."""
import os
import tempfile
import unittest

from src.dados.exemplos import rede_exemplo_artigo
from src.servicos.experimento import executar_experimento, gerar_graficos, perfilar
from src.servicos.relatorio import gerar_relatorio_otimizacao, salvar_relatorio
from src.servicos.servico_rede import ServicoRede
from src.utilitarios.visualizacao import desenhar_rede
from src.modelos.grafo import Grafo


class TestGeracaoEvidencias(unittest.TestCase):
    def setUp(self):
        self.servico = ServicoRede(rede_exemplo_artigo())
        self.comparacao = self.servico.comparar()

    def test_gerar_graficos_salva_arquivos(self):
        resultados = executar_experimento(tamanhos=(10, 20))
        with tempfile.TemporaryDirectory() as pasta:
            gerar_graficos(resultados, pasta)
            self.assertTrue(os.path.isfile(os.path.join(pasta, "tempo.png")))
            self.assertTrue(os.path.isfile(os.path.join(pasta, "memoria.png")))

    def test_salvar_relatorio_arquivo(self):
        texto = gerar_relatorio_otimizacao(self.servico.grafo, self.comparacao)
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "relatorio.md")
            salvar_relatorio(texto, caminho)
            with open(caminho, encoding="utf-8") as f:
                self.assertEqual(f.read(), texto)

    def test_desenhar_rede_salva_imagem(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "rede.png")
            desenhar_rede(self.servico.grafo, self.servico.executar_kruskal(), caminho)
            self.assertTrue(os.path.isfile(caminho))
            self.assertGreater(os.path.getsize(caminho), 0)

    def test_desenhar_rede_sem_mst_nao_explode(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "rede_sem_mst.png")
            desenhar_rede(self.servico.grafo, None, caminho)
            self.assertTrue(os.path.isfile(caminho))

    def test_perfilar_retorna_texto_com_ambos_algoritmos(self):
        texto = perfilar(n=30)
        self.assertIn("Prim", texto)
        self.assertIn("Kruskal", texto)

    def test_desenhar_rede_sem_caminho_nao_explode(self):
        """Cobre o caminho plt.show() (exibição interativa) com backend não gráfico."""
        import matplotlib
        matplotlib.use("Agg")
        desenhar_rede(self.servico.grafo, self.servico.executar_kruskal(), None)

    def test_desenhar_rede_com_mostrar_true_abre_janela(self):
        """Cobre o caminho plt.show() quando mostrar=True."""
        import matplotlib
        matplotlib.use("Agg")
        desenhar_rede(self.servico.grafo, self.servico.executar_kruskal(), None, mostrar=True)

    def test_desenhar_rede_salva_e_nao_exibe(self):
        """Com caminho, salva em disco e não chama plt.show()."""
        import matplotlib
        matplotlib.use("Agg")
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "rede.png")
            desenhar_rede(self.servico.grafo, self.servico.executar_kruskal(), caminho)
            self.assertTrue(os.path.isfile(caminho))
            self.assertGreater(os.path.getsize(caminho), 0)


class TestComparacaoCaminhosRaros(unittest.TestCase):
    """Cobre os ramos de justificativa que exigem grafos especiais."""

    def test_prim_e_kruskal_escolhem_conexoes_diferentes_mesmo_custo(self):
        # Quadrado A-B-C-D-A com diagonal A-C: duas AGMs distintas de custo 3.
        g = Grafo()
        for v in "ABCD":
            g.adicionar_vertice(v)
        for a, b, c in [("A", "B", 1), ("B", "C", 1), ("C", "D", 1),
                        ("D", "A", 1), ("A", "C", 2)]:
            g.adicionar_aresta(a, b, c)
        comparacao = ServicoRede(g).comparar()
        self.assertTrue(comparacao.custos_equivalentes)
        self.assertFalse(comparacao.mesmas_arestas)
        self.assertIn("propriedade do corte", comparacao.justificativa)

    def test_aviso_quando_custos_diferem(self):
        servico = ServicoRede(rede_exemplo_artigo())
        original = servico.executar_prim

        def prim_falso():
            from src.modelos.mst import MST
            return MST(algoritmo="Prim")

        servico.executar_prim = prim_falso
        try:
            comparacao = servico.comparar()
        finally:
            servico.executar_prim = original
        self.assertFalse(comparacao.custos_equivalentes)
        self.assertIn("ATENÇÃO", comparacao.justificativa)


if __name__ == "__main__":
    unittest.main()