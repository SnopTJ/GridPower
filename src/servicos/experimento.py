"""Experimento de complexidade (Sprint 4): tempo e memória por tamanho da rede."""
import cProfile
import csv
import io
import pstats
import statistics
import time
import tracemalloc

from src.algoritmos.kruskal import kruskal
from src.algoritmos.prim import prim
from src.dados.gerador import gerar_rede_sintetica

TAMANHOS_PADRAO = (10, 50, 100, 500, 1000)
CAMPOS = ["vertices", "arestas", "prim_ms", "kruskal_ms", "prim_kib", "kruskal_kib",
          "custo_prim", "custo_kruskal", "custos_iguais"]


def medir(funcao, grafo, repeticoes):
    """Retorna (tempo mediano em ms, pico de memória em KiB)."""
    tempos = []
    for _ in range(repeticoes):
        t0 = time.perf_counter()
        funcao(grafo)
        tempos.append(time.perf_counter() - t0)
    tracemalloc.start()
    funcao(grafo)
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return statistics.median(tempos) * 1000, pico / 1024


def executar_experimento(tamanhos=TAMANHOS_PADRAO):
    resultados = []
    for n in tamanhos:
        grafo = gerar_rede_sintetica(n, semente=n)
        repeticoes = 30 if n <= 100 else 10
        t_p, m_p = medir(prim, grafo, repeticoes)
        t_k, m_k = medir(kruskal, grafo, repeticoes)
        c_p, c_k = prim(grafo).custo_total, kruskal(grafo).custo_total
        resultados.append({
            "vertices": n, "arestas": grafo.quantidade_arestas,
            "prim_ms": t_p, "kruskal_ms": t_k, "prim_kib": m_p, "kruskal_kib": m_k,
            "custo_prim": c_p, "custo_kruskal": c_k, "custos_iguais": c_p == c_k,
        })
    return resultados


def salvar_csv(resultados, caminho):
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS, lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(resultados)


def gerar_graficos(resultados, pasta):
    """Salva dois gráficos (tempo e memória) em `pasta`."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ns = [r["vertices"] for r in resultados]
    for chave, rotulo, arquivo in [("ms", "Tempo de execução (ms)", "tempo.png"),
                                   ("kib", "Pico de memória (KiB)", "memoria.png")]:
        fig, ax = plt.subplots(figsize=(5, 3.4))
        ax.plot(ns, [r[f"prim_{chave}"] for r in resultados], "o-", color="black", label="Prim (heap)")
        ax.plot(ns, [r[f"kruskal_{chave}"] for r in resultados], "s--", color="#555555",
                label="Kruskal (Union-Find)")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Número de vértices (|V|)")
        ax.set_ylabel(rotulo)
        ax.set_xticks(ns)
        ax.set_xticklabels([str(n) for n in ns])
        ax.grid(True, which="both", alpha=0.25)
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(f"{pasta}/{arquivo}", dpi=200)
        plt.close(fig)


def perfilar(n=1000, linhas=12):
    """Profiling com cProfile de Prim e Kruskal; retorna o texto do relatório."""
    grafo = gerar_rede_sintetica(n, semente=n)
    saida = io.StringIO()
    for nome, funcao in (("Prim", prim), ("Kruskal", kruskal)):
        perfil = cProfile.Profile()
        perfil.enable()
        funcao(grafo)
        perfil.disable()
        saida.write(f"===== {nome} (n={n}) =====\n")
        pstats.Stats(perfil, stream=saida).sort_stats("cumulative").print_stats(linhas)
    return saida.getvalue()
