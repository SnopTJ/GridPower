"""GridPower - Otimização da Infraestrutura Urbana (UrbanTech, Squad 2).

Uso:
    python main.py                 menu interativo
    python main.py --demo          demonstração com a rede de exemplo do artigo
    python main.py --experimento   experimento de complexidade (10 a 1000 vértices)
"""
import argparse
import os
import sys

from src.dados.exemplos import EXEMPLOS
from src.servicos.experimento import (executar_experimento, gerar_graficos, perfilar,
                                      salvar_csv)
from src.servicos.relatorio import gerar_relatorio_otimizacao, salvar_relatorio
from src.servicos.servico_rede import ServicoRede
from src.utilitarios.excecoes import ErroGridPower, RedeDesconectadaError
from src.utilitarios.formatacao import formatar_reais
from src.utilitarios.visualizacao import descrever_rede, desenhar_rede

def _configurar_codificacao():
    """Reconfigura stdout/stderr para UTF-8 quando o console herda cp1252 (Windows).

    Sem isso, caracteres como õ, ã e é são codificados como byte único e
    renderizados como  no terminal UTF-8.
    """
    for nome in ("stdout", "stderr"):
        fluxo = getattr(sys, nome, None)
        if fluxo is None:
            continue
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
            continue
        except (AttributeError, ValueError):
            pass
        buffer = getattr(fluxo, "buffer", None)
        if buffer is not None:
            try:
                setattr(sys, nome, type(fluxo)(buffer, encoding="utf-8",
                                               errors="replace", line_buffering=True))
            except (TypeError, ValueError):
                pass


_configurar_codificacao()

MENU = """
=== GRIDPOWER - Menu ===
 1) Cadastrar ponto            (RF01)
 2) Cadastrar conexão + custo  (RF02, RF03)
 3) Visualizar rede            (RF04)
 4) Executar Prim              (RF05)
 5) Executar Kruskal           (RF06)
 6) Comparar Prim x Kruskal    (RF07, RF08)
 7) Verificar conectividade    (RF09)
 8) Gerar relatório            (RF10)
 9) Carregar rede de exemplo
10) Rodar experimento de complexidade
 0) Sair
"""


def imprimir_arvore(arvore):
    print(f"\nResultado de {arvore.algoritmo}:")
    for a in arvore.arestas:
        print(f"  {a.origem} -- {a.destino}: {formatar_reais(a.custo)}")
    print(f"Custo total: {formatar_reais(arvore.custo_total)}")


def comparar_e_imprimir(servico):
    comparacao = servico.comparar()
    imprimir_arvore(comparacao.prim)
    imprimir_arvore(comparacao.kruskal)
    print(f"\nPrim: {formatar_reais(comparacao.custo_prim)} | "
          f"Kruskal: {formatar_reais(comparacao.custo_kruskal)}")
    print(comparacao.justificativa)
    return comparacao


def demonstracao():
    servico = ServicoRede(EXEMPLOS["artigo"]())
    print("GRIDPOWER - demonstração com a rede de exemplo (8 pontos)\n")
    print(descrever_rede(servico.grafo))
    comparar_e_imprimir(servico)


def rodar_experimento():
    print("Executando experimento (pode levar alguns segundos)...")
    resultados = executar_experimento()
    print(f"{'|V|':>5} {'|E|':>6} {'Prim ms':>9} {'Kruskal ms':>11} {'Prim KiB':>9} {'Kruskal KiB':>12}")
    for r in resultados:
        print(f"{r['vertices']:>5} {r['arestas']:>6} {r['prim_ms']:>9.3f} {r['kruskal_ms']:>11.3f} "
              f"{r['prim_kib']:>9.1f} {r['kruskal_kib']:>12.1f}")
    os.makedirs("relatorios/complexidade", exist_ok=True)
    os.makedirs("relatorios/figuras", exist_ok=True)
    os.makedirs("relatorios/profiling", exist_ok=True)
    salvar_csv(resultados, "relatorios/complexidade/resultados.csv")
    gerar_graficos(resultados, "relatorios/figuras")
    with open("relatorios/profiling/perfil.txt", "w", encoding="utf-8") as f:
        f.write(perfilar())
    print("Arquivos salvos em relatorios/ (CSV, gráficos e profiling).")


def ler_custo(texto):
    try:
        return float(texto.replace(",", "."))
    except ValueError:
        return texto          # deixa a validação do modelo recusar


def menu_interativo(servico=None, entrada=input, saida=print):
    servico = servico or ServicoRede()
    ultima_comparacao = None
    while True:
        saida(MENU)
        opcao = entrada("Escolha uma opção: ").strip()
        try:
            if opcao == "1":
                nome = entrada("Nome do ponto: ")
                tipo = entrada("Tipo (ponto/subestacao/quadro/estacao/reservatorio/distribuicao) [ponto]: ").strip() or "ponto"
                servico.cadastrar_ponto(nome, tipo)
                saida("Ponto cadastrado.")
            elif opcao == "2":
                origem = entrada("Origem: ").strip()
                destino = entrada("Destino: ").strip()
                custo = ler_custo(entrada("Custo (R$): "))
                servico.cadastrar_conexao(origem, destino, custo)
                saida("Conexão cadastrada.")
            elif opcao == "3":
                saida(descrever_rede(servico.grafo))
                if entrada("Salvar imagem da rede? (s/N): ").strip().lower() == "s":
                    os.makedirs("relatorios/figuras", exist_ok=True)
                    desenhar_rede(servico.grafo, caminho="relatorios/figuras/rede.png")
                    saida("Imagem salva em relatorios/figuras/rede.png")
            elif opcao == "4":
                imprimir_arvore(servico.executar_prim())
            elif opcao == "5":
                imprimir_arvore(servico.executar_kruskal())
            elif opcao == "6":
                ultima_comparacao = comparar_e_imprimir(servico)
            elif opcao == "7":
                conexa, componentes = servico.verificar_conectividade()
                if conexa:
                    saida("A rede é conexa.")
                else:
                    saida(f"A rede é DESCONECTADA: {len(componentes)} componentes.")
                    for c in componentes:
                        saida("  - " + ", ".join(c))
            elif opcao == "8":
                comparacao = ultima_comparacao or servico.comparar()
                texto = gerar_relatorio_otimizacao(servico.grafo, comparacao)
                os.makedirs("relatorios", exist_ok=True)
                salvar_relatorio(texto, "relatorios/relatorio_otimizacao.md")
                saida(texto)
                saida("Relatório salvo em relatorios/relatorio_otimizacao.md")
            elif opcao == "9":
                nome = entrada(f"Exemplo ({'/'.join(EXEMPLOS)}): ").strip()
                if nome not in EXEMPLOS:
                    saida("Exemplo inexistente.")
                else:
                    servico = ServicoRede(EXEMPLOS[nome]())
                    ultima_comparacao = None
                    saida(f"Rede de exemplo '{nome}' carregada.")
            elif opcao == "10":
                rodar_experimento()
            elif opcao == "0":
                saida("Até logo!")
                return
            else:
                saida("Opção inválida.")
        except RedeDesconectadaError as erro:
            saida(f"Erro: {erro}")
        except ErroGridPower as erro:
            saida(f"Entrada inválida: {erro}")


def main():
    analisador = argparse.ArgumentParser(description="GridPower - árvore geradora mínima")
    analisador.add_argument("--demo", action="store_true", help="demonstração com a rede do artigo")
    analisador.add_argument("--experimento", action="store_true", help="experimento de complexidade")
    args = analisador.parse_args()
    if args.demo:
        demonstracao()
    elif args.experimento:
        rodar_experimento()
    else:
        menu_interativo()


if __name__ == "__main__":
    main()
