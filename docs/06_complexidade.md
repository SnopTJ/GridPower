# 06 - Complexidade

Sejam V o número de vértices e E o de arestas.

| Etapa | Custo |
|---|---|
| Montar lista de adjacência | O(V + E) |
| Prim com heap binário | O(E log V) |
| Ordenar arestas (Kruskal) | O(E log E) = O(E log V) |
| Operações Union-Find | O(E · α(V)), praticamente O(E) |
| Kruskal total | O(E log V) |

**Memória:** Prim guarda a lista de adjacência (2E entradas) e o heap; Kruskal guarda a lista
ordenada de arestas e dois dicionários de tamanho V. Em ambos, O(V + E).

**Observação:** nos experimentos o número de arestas cresce junto com V (|E| = 5|V|), então são
redes esparsas. Redes densas não foram avaliadas e podem favorecer Prim.

Os resultados medidos estão em `08_resultados.md` e em `relatorios/complexidade/resultados.csv`.
