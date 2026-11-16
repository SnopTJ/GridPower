"""UnionFind (conjuntos disjuntos) com compressão de caminho e união por posto."""


class UnionFind:
    def __init__(self, elementos):
        self.pai = {x: x for x in elementos}
        self.posto = {x: 0 for x in elementos}       # posto = rank
        self.quantidade_conjuntos = len(self.pai)

    def encontrar(self, x):
        """find(): retorna a raiz do conjunto de x, comprimindo o caminho."""
        raiz = x
        while self.pai[raiz] != raiz:
            raiz = self.pai[raiz]
        while self.pai[x] != raiz:                   # compressão de caminho
            self.pai[x], x = raiz, self.pai[x]
        return raiz

    def unir(self, a, b):
        """union(): une os conjuntos de a e b. Retorna False se já eram o mesmo."""
        raiz_a, raiz_b = self.encontrar(a), self.encontrar(b)
        if raiz_a == raiz_b:
            return False
        if self.posto[raiz_a] < self.posto[raiz_b]:  # união por posto
            raiz_a, raiz_b = raiz_b, raiz_a
        self.pai[raiz_b] = raiz_a
        if self.posto[raiz_a] == self.posto[raiz_b]:
            self.posto[raiz_a] += 1
        self.quantidade_conjuntos -= 1
        return True

    def conectados(self, a, b):
        return self.encontrar(a) == self.encontrar(b)

    # nomes em inglês usados no documento do projeto
    find = encontrar
    union = unir
