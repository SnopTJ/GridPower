# 05 - Algoritmos

## Union-Find (`modelos/union_find.py`)
- `encontrar(x)` (find): devolve a raiz do conjunto de `x`, com **compressão de caminho**.
- `unir(a, b)` (union): junta os conjuntos por **posto** (rank); devolve `False` se já eram o mesmo.
- Custo amortizado por operação: praticamente constante (inverso de Ackermann).

## Kruskal (`algoritmos/kruskal.py`)
```
ordenar as arestas por custo
para cada aresta (u, v) em ordem crescente:
    se unir(u, v) juntou dois conjuntos diferentes:
        aceitar a aresta
        se já há |V| - 1 arestas: parar
se aceitou menos de |V| - 1 arestas: rede desconectada
```

## Prim (`algoritmos/prim.py`)
```
escolher um vértice inicial; marcá-lo como visitado
colocar suas arestas em uma fila de prioridade (heap)
enquanto a fila não estiver vazia e faltarem vértices:
    retirar a aresta de menor custo (u, v)
    se v já foi visitado: descartar
    senão: aceitar a aresta, marcar v e inserir as arestas de v na fila
se algum vértice não foi visitado: rede desconectada
```

## Comparação
| Aspecto | Prim | Kruskal |
|---|---|---|
| Estratégia | cresce uma única árvore | une componentes |
| Estrutura auxiliar | heap + lista de adjacência | ordenação + Union-Find |
| Complexidade | O(E log V) | O(E log V) |
| Cenário favorável | A implementação atual de Prim é independente de densidade (heap + lista de adjacência). | A implementação atual é vantajosa em redes esparsas (E ≈ 5V). Para redes densas com matriz de adjacência, a complexidade de Prim seria O(V²). |

## Rede desconectada
Os dois algoritmos levantam `RedeDesconectadaError`, cuja mensagem lista os componentes isolados.
