"""Visualização da rede (RF04): em texto e em imagem."""
import math

from src.utilitarios.formatacao import formatar_reais


def descrever_rede(grafo, mst=None):
    """Retorna um texto com os pontos e conexões. Arestas da AGM ficam marcadas com '*'."""
    escolhidas = mst.pares() if mst is not None else set()
    linhas = [f"Pontos ({grafo.quantidade_vertices}):"]
    for v in grafo.vertices:
        linhas.append(f"  - {v.nome} [{v.tipo}]")
    linhas.append(f"Conexões ({grafo.quantidade_arestas}):")
    for a in sorted(grafo.arestas, key=lambda a: (a.custo, a.origem, a.destino)):
        marca = "*" if a.chave in escolhidas else " "
        linhas.append(f" {marca} {a.origem} -- {a.destino}: {formatar_reais(a.custo)}")
    if mst is not None:
        linhas.append("(* = conexão escolhida pela árvore geradora mínima)")
    return "\n".join(linhas)


def desenhar_rede(grafo, mst=None, caminho=None):
    """Desenha a rede (layout circular). Salva em `caminho` ou abre uma janela."""
    import matplotlib
    if caminho:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    nomes = grafo.nomes_vertices
    n = max(len(nomes), 1)
    pos = {nome: (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))
           for i, nome in enumerate(nomes)}
    escolhidas = mst.pares() if mst is not None else set()

    fig, ax = plt.subplots(figsize=(6, 5))
    for a in grafo.arestas:
        (x1, y1), (x2, y2) = pos[a.origem], pos[a.destino]
        na_mst = a.chave in escolhidas
        ax.plot([x1, x2], [y1, y2], color="black" if na_mst else "#999999",
                lw=2.4 if na_mst else 0.8, ls="-" if na_mst else "--", zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{a.custo:,.0f}".replace(",", "."),
                fontsize=7, ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=0.5), zorder=2)
    for nome, (x, y) in pos.items():
        ax.scatter([x], [y], s=500, c="white", edgecolors="black", zorder=3)
        ax.text(x, y, nome, ha="center", va="center", fontsize=8, zorder=4)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    if caminho:
        fig.savefig(caminho, dpi=200)
        plt.close(fig)
    else:
        plt.show()
