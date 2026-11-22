"""Grafo não direcionado ponderado G = (V, E) da rede urbana."""
from src.modelos.aresta import Aresta
from src.modelos.union_find import UnionFind
from src.modelos.vertice import Vertice
from src.utilitarios.excecoes import DadoInvalidoError


class Grafo:
    def __init__(self):
        self._vertices = {}     # nome -> Vertice (mantém a ordem de cadastro)
        self._arestas = {}      # chave (frozenset) -> Aresta

    # ----------------------------------------------------- cadastro
    def adicionar_vertice(self, nome, tipo="ponto"):
        if not isinstance(nome, str):
            raise DadoInvalidoError("O nome do vértice deve ser um texto.")
        if not nome.strip():
            raise DadoInvalidoError("O nome do vértice não pode ser vazio ou apenas espaços.")
        nome = nome.strip()
        if nome in self._vertices:
            raise DadoInvalidoError(f"O ponto {nome!r} já está cadastrado.")
        vertice = Vertice(nome, tipo)
        self._vertices[nome] = vertice
        return vertice

    def adicionar_aresta(self, origem, destino, custo):
        """Cadastra uma conexão. Se já existir, mantém a de menor custo."""
        if not isinstance(origem, str) or not isinstance(destino, str):
            raise DadoInvalidoError("A origem e o destino devem ser textos.")
        if origem == destino:
            raise DadoInvalidoError("Não é permitido conectar um vértice a ele mesmo.")
        if not origem or not destino:
            raise DadoInvalidoError("A origem e o destino não podem ser vazios.")
        if origem not in self._vertices or destino not in self._vertices:
            raise DadoInvalidoError("Os dois vértices precisam estar cadastrados.")
        if isinstance(custo, int) and not isinstance(custo, bool):
            custo = float(custo)
        nova = Aresta(origem, destino, custo)      # valida o custo
        atual = self._arestas.get(nova.chave)
        if atual is None or nova.custo < atual.custo:
            self._arestas[nova.chave] = nova
        return self._arestas[nova.chave]

    # ----------------------------------------------------- consulta
    @property
    def vertices(self):
        return list(self._vertices.values())

    @property
    def nomes_vertices(self):
        return list(self._vertices)

    @property
    def arestas(self):
        return list(self._arestas.values())

    @property
    def quantidade_vertices(self):
        return len(self._vertices)

    @property
    def quantidade_arestas(self):
        return len(self._arestas)

    def lista_adjacencia(self):
        """nome -> lista de (custo, vizinho)."""
        adj = {nome: [] for nome in self._vertices}
        for a in self._arestas.values():
            adj[a.origem].append((a.custo, a.destino))
            adj[a.destino].append((a.custo, a.origem))
        return adj

    def componentes_conexos(self):
        """Lista de componentes conexos (cada um é uma lista de nomes), via Union-Find."""
        uf = UnionFind(self._vertices)
        for a in self._arestas.values():
            uf.unir(a.origem, a.destino)
        grupos = {}
        for nome in self._vertices:
            grupos.setdefault(uf.encontrar(nome), []).append(nome)
        return list(grupos.values())

    def remover_ponto(self, nome):
        """Remove um ponto e todas as conexões associadas a ele."""
        if nome not in self._vertices:
            raise DadoInvalidoError(f"O ponto {nome!r} não está cadastrado.")
        # Remove todas as arestas que envolvem este ponto
        for a in list(self._arestas.values()):
            if a.origem == nome or a.destino == nome:
                del self._arestas[a.chave]
        # Remove o ponto em si
        del self._vertices[nome]

    def remover_conexao(self, origem, destino):
        """Remove uma conexão entre dois pontos."""
        if origem not in self._vertices or destino not in self._vertices:
            raise DadoInvalidoError("Os dois vértices precisam estar cadastrados.")
        chave = frozenset([origem, destino])
        if chave in self._arestas:
            del self._arestas[chave]

    def alterar_custo(self, origem, destino, novo_custo):
        """Altera o custo de uma conexão existente."""
        if origem not in self._vertices or destino not in self._vertices:
            raise DadoInvalidoError("Os dois vértices precisam estar cadastrados.")
        chave = frozenset([origem, destino])
        if chave not in self._arestas:
            raise DadoInvalidoError(f"Não existe conexão entre {origem} e {destino}.")
        # Aresta é imutável (frozen): substitui por uma nova instância com o novo custo
        antiga = self._arestas[chave]
        self._arestas[chave] = Aresta(antiga.origem, antiga.destino, novo_custo)

    def eh_conexo(self):
        return len(self.componentes_conexos()) <= 1
