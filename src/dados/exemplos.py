"""Redes de exemplo usadas na demonstração, nos testes e no artigo."""
from src.modelos.grafo import Grafo

CUSTO_EXEMPLO_ARTIGO = 18500.0   # custo mínimo da rede de 8 pontos (seção A.8 do projeto)


def rede_exemplo_artigo():
    """Rede de 8 pontos e 13 conexões; AGM única com custo R$ 18.500 (Figura 1 do artigo)."""
    g = Grafo()
    for nome, tipo in [("S1", "subestacao"), ("Q1", "quadro"), ("Q2", "quadro"),
                       ("E1", "estacao"), ("R1", "reservatorio"),
                       ("P1", "distribuicao"), ("P2", "distribuicao"), ("P3", "distribuicao")]:
        g.adicionar_vertice(nome, tipo)
    conexoes = [("S1", "Q1", 2000), ("S1", "Q2", 2200), ("Q1", "E1", 2500),
                ("Q1", "Q2", 2600), ("Q2", "R1", 2700), ("E1", "P1", 2800),
                ("R1", "P2", 3000), ("P1", "P2", 3100), ("P2", "P3", 3300),
                ("E1", "R1", 4100), ("Q1", "P1", 4500), ("R1", "P3", 4800),
                ("S1", "E1", 5200)]
    for a, b, custo in conexoes:
        g.adicionar_aresta(a, b, custo)
    return g


def rede_exemplo_simples():
    """Rede de 4 pontos do protótipo inicial; custo mínimo R$ 9.000."""
    g = Grafo()
    for nome in ["A", "B", "C", "D"]:
        g.adicionar_vertice(nome)
    for a, b, custo in [("A", "B", 4000), ("A", "C", 2000), ("B", "C", 5000),
                        ("B", "D", 3000), ("C", "D", 6000)]:
        g.adicionar_aresta(a, b, custo)
    return g


def rede_exemplo_desconectada():
    """Duas ilhas de rede sem ligação entre si (para demonstrar o RF09)."""
    g = Grafo()
    for nome in ["A", "B", "C", "D"]:
        g.adicionar_vertice(nome)
    g.adicionar_aresta("A", "B", 1000)
    g.adicionar_aresta("C", "D", 1500)
    return g


EXEMPLOS = {
    "artigo": rede_exemplo_artigo,
    "simples": rede_exemplo_simples,
    "desconectada": rede_exemplo_desconectada,
}
