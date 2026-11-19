"""Gerador de redes sintéticas conexas para o experimento de complexidade."""
import random

from src.modelos.grafo import Grafo


def gerar_rede_sintetica(n, semente=0, arestas_por_vertice=5, custo_min=1000, custo_max=20000):
    """Gera uma rede conexa com n pontos e |E| = arestas_por_vertice * n
    (limitado ao grafo completo). Custos inteiros aleatórios em [custo_min, custo_max]."""
    rnd = random.Random(semente)
    g = Grafo()
    for i in range(n):
        g.adicionar_vertice(f"V{i}")
    ordem = list(range(n))
    rnd.shuffle(ordem)
    for i in range(1, n):                       # um caminho garante a conectividade
        g.adicionar_aresta(f"V{ordem[i - 1]}", f"V{ordem[i]}", rnd.randint(custo_min, custo_max))
    alvo = min(arestas_por_vertice * n, n * (n - 1) // 2)
    while g.quantidade_arestas < alvo:
        u, v = rnd.sample(range(n), 2)
        g.adicionar_aresta(f"V{u}", f"V{v}", rnd.randint(custo_min, custo_max))
    return g
