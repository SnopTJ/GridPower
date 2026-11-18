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
    """Rede urbana de 6 pontos dividida em 2 ilhas isoladas (Setor Norte e Setor Sul)."""
    g = Grafo()
    for nome, tipo in [("Sub-A", "subestacao"), ("Q-Norte1", "quadro"), ("Q-Norte2", "quadro"),
                       ("Sub-B", "subestacao"), ("Q-Sul1", "quadro"), ("Est-Sul", "estacao")]:
        g.adicionar_vertice(nome, tipo)
    # Ilha 1 (Norte)
    g.adicionar_aresta("Sub-A", "Q-Norte1", 2000)
    g.adicionar_aresta("Q-Norte1", "Q-Norte2", 1500)
    # Ilha 2 (Sul - isolada da Norte)
    g.adicionar_aresta("Sub-B", "Q-Sul1", 2500)
    g.adicionar_aresta("Q-Sul1", "Est-Sul", 1800)
    return g


def rede_exemplo_5_pontos():
    """Rede de 5 pontos com 7 conexões; custo mínimo R$ 10.000."""
    g = Grafo()
    for nome in ["A", "B", "C", "D", "E"]:
        g.adicionar_vertice(nome)
    for a, b, custo in [("A", "B", 3000), ("A", "C", 2500),
                        ("B", "C", 4000), ("B", "D", 2000),
                        ("C", "E", 3500), ("D", "E", 2500),
                        ("A", "E", 4500)]:
        g.adicionar_aresta(a, b, custo)
    return g


def rede_exemplo_6_pontos():
    """Rede de 6 pontos com 9 conexões; custo mínimo R$ 12.500."""
    g = Grafo()
    for nome in ["A", "B", "C", "D", "E", "F"]:
        g.adicionar_vertice(nome)
    for a, b, custo in [("A", "B", 3000), ("A", "C", 2000),
                        ("B", "D", 4000), ("C", "D", 2500),
                        ("C", "E", 3000), ("D", "F", 2000),
                        ("E", "F", 3500), ("A", "F", 4500),
                        ("B", "E", 3500)]:
        g.adicionar_aresta(a, b, custo)
    return g


def rede_exemplo_7_pontos():
    """Rede de 7 pontos com 10 conexões; custo mínimo R$ 15.000."""
    g = Grafo()
    for nome in ["A", "B", "C", "D", "E", "F", "G"]:
        g.adicionar_vertice(nome)
    for a, b, custo in [("A", "B", 3000), ("A", "C", 2500),
                        ("B", "D", 4000), ("C", "D", 2500),
                        ("C", "E", 3000), ("D", "F", 2000),
                        ("E", "F", 3500), ("E", "G", 2000),
                        ("F", "G", 3000), ("A", "G", 4000)]:
        g.adicionar_aresta(a, b, custo)
    return g


EXEMPLOS = {
    "artigo": rede_exemplo_artigo,
    "simples": rede_exemplo_simples,
    "desconectada": rede_exemplo_desconectada,
    "5_pontos": rede_exemplo_5_pontos,
    "6_pontos": rede_exemplo_6_pontos,
    "7_pontos": rede_exemplo_7_pontos,
}
