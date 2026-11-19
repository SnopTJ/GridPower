"""Testes para a CLI (main.py): configuração de codificação e demonstração."""
import io
import subprocess
import sys
import unittest


class TestConfiguracaoUtf8(unittest.TestCase):
    """Cobre _configurar_codificacao() do main.py (regressão do commit 8126031)."""

    def _importar_main(self):
        import main
        return main

    def test_stdout_e_stderr_sao_utf8(self):
        main = self._importar_main()
        self.assertEqual(sys.stdout.encoding, "utf-8")
        self.assertEqual(sys.stderr.encoding, "utf-8")

    def test_caracteres_portugueses_nao_garrafiram(self):
        """Ajusta se o console herdou cp1252 e o print() perdeu õ, ã, é."""
        main = self._importar_main()
        buffer = io.StringIO()
        original = sys.stdout
        try:
            sys.stdout = buffer
            print("conexões são únicas")
        finally:
            sys.stdout = original
        self.assertIn("conexões", buffer.getvalue())
        self.assertIn("única", buffer.getvalue())


class TestDemoCli(unittest.TestCase):
    """Executa o --demo via subprocess para confirmar saida correta em UTF-8."""

    def test_demo_imprime_justificativa_sem_garrafico(self):
        saida = subprocess.run(
            [sys.executable, "main.py", "--demo"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=120,
        )
        self.assertEqual(saida.returncode, 0, msg=saida.stderr)
        self.assertIn("conexões", saida.stdout)
        self.assertIn("única", saida.stdout)
        self.assertIn("R$ 18.500,00", saida.stdout)


if __name__ == "__main__":
    unittest.main()