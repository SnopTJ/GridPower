"""Testes da camada de aplicação: ServicoRede, relatório, experimento e interface."""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from src.dados.exemplos import rede_exemplo_artigo, rede_exemplo_desconectada
from src.servicos.experimento import executar_experimento, perfilar, salvar_csv
from src.servicos.relatorio import gerar_relatorio_otimizacao
from src.servicos.servico_rede import ServicoRede
from src.utilitarios.excecoes import DadoInvalidoError, RedeDesconectadaError
from src.utilitarios.formatacao import formatar_reais
from src.utilitarios.visualizacao import descrever_rede


class TestServicoRede(unittest.TestCase):
    def test_cadastro_e_comparacao(self):
        s = ServicoRede()
        for nome in "ABC":
            s.cadastrar_ponto(nome)
        s.cadastrar_conexao("A", "B", 1000)
        s.cadastrar_conexao("B", "C", 2000)
        s.cadastrar_conexao("A", "C", 3000)
        comparacao = s.comparar()
        self.assertTrue(comparacao.custos_equivalentes)
        self.assertTrue(comparacao.mesmas_arestas)
        self.assertEqual(comparacao.custo_prim, 3000)
        self.assertEqual(s.calcular_custo_total(comparacao.kruskal), 3000)

    def test_comparacao_com_empate_explica_varias_agms(self):
        s = ServicoRede()
        for nome in "ABC":
            s.cadastrar_ponto(nome)
        for a, b in [("A", "B"), ("B", "C"), ("A", "C")]:
            s.cadastrar_conexao(a, b, 1)
        comparacao = s.comparar()
        self.assertTrue(comparacao.custos_equivalentes)
        self.assertIn("propriedade do corte", comparacao.justificativa)

    def test_entrada_invalida(self):
        s = ServicoRede()
        s.cadastrar_ponto("A")
        with self.assertRaises(DadoInvalidoError):
            s.cadastrar_conexao("A", "B", 10)

    def test_conectividade(self):
        conexa, _ = ServicoRede(rede_exemplo_artigo()).verificar_conectividade()
        self.assertTrue(conexa)
        conexa, componentes = ServicoRede(rede_exemplo_desconectada()).verificar_conectividade()
        self.assertFalse(conexa)
        self.assertEqual(len(componentes), 2)

    def test_comparar_rede_desconectada_levanta_erro(self):
        with self.assertRaises(RedeDesconectadaError):
            ServicoRede(rede_exemplo_desconectada()).comparar()


class TestRelatorioEFormatacao(unittest.TestCase):
    def test_formatar_reais(self):
        self.assertEqual(formatar_reais(18500), "R$ 18.500,00")
        self.assertEqual(formatar_reais(1234567.5), "R$ 1.234.567,50")

    def test_relatorio_contem_custo_e_justificativa(self):
        servico = ServicoRede(rede_exemplo_artigo())
        texto = gerar_relatorio_otimizacao(servico.grafo, servico.comparar())
        self.assertIn("R$ 18.500,00", texto)
        self.assertIn("Custos equivalentes: sim", texto)

    def test_descrever_rede_marca_arestas_da_agm(self):
        servico = ServicoRede(rede_exemplo_artigo())
        texto = descrever_rede(servico.grafo, servico.executar_kruskal())
        self.assertIn("* S1 -- Q1", texto)
        self.assertIn("  Q1 -- Q2", texto)     # Q1-Q2 não está na AGM


class TestExperimento(unittest.TestCase):
    def test_experimento_pequeno(self):
        resultados = executar_experimento(tamanhos=(10, 20))
        self.assertEqual([r["vertices"] for r in resultados], [10, 20])
        self.assertTrue(all(r["custos_iguais"] for r in resultados))
        self.assertTrue(all(r["prim_ms"] > 0 and r["kruskal_kib"] > 0 for r in resultados))

    def test_salvar_csv_e_profiling(self):
        resultados = executar_experimento(tamanhos=(10,))
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "resultados.csv")
            salvar_csv(resultados, caminho)
            with open(caminho, encoding="utf-8") as f:
                self.assertEqual(len(f.read().strip().splitlines()), 2)
        self.assertIn("Kruskal", perfilar(n=20))


class TestInterface(unittest.TestCase):
    def test_menu_executa_fluxo_completo(self):
        import main
        respostas = iter(["1", "A", "", "1", "B", "", "2", "A", "B", "1500,50", "6", "0"])
        saidas = []
        main.menu_interativo(entrada=lambda _="": next(respostas), saida=saidas.append)
        texto = "\n".join(saidas)
        self.assertIn("Ponto cadastrado.", texto)
        self.assertIn("Conexão cadastrada.", texto)
        self.assertIn("Até logo!", texto)

    def test_menu_mostra_erro_de_validacao_sem_quebrar(self):
        import main
        respostas = iter(["2", "X", "Y", "10", "0"])
        saidas = []
        main.menu_interativo(entrada=lambda _="": next(respostas), saida=saidas.append)
        self.assertTrue(any("Entrada inválida" in s for s in saidas))

    def test_demonstracao_imprime_custo(self):
        import main
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            main.demonstracao()
        self.assertIn("R$ 18.500,00", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
