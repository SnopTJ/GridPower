# 03 - Modelagem Matemática

## Grafo
A rede é um grafo não direcionado ponderado **G = (V, E)**:
- **V**: pontos da infraestrutura;
- **E**: conexões candidatas; cada aresta `e` tem custo `w(e) ≥ 0` em reais.

## Problema
Encontrar **T ⊆ E** tal que (V, T) seja conexo e acíclico (portanto |T| = |V| − 1) e que minimize

    w(T) = Σ w(e), para e ∈ T

## Propriedades usadas
- **Propriedade do corte:** em qualquer corte do grafo, a aresta de menor custo que o atravessa
  pertence a alguma AGM. É o que justifica a escolha gananciosa de Prim e de Kruskal.
- **Unicidade:** se todos os custos forem distintos, a AGM é única.
- **Empates:** com custos repetidos pode haver várias AGMs, todas com o **mesmo custo total**.
- **Conectividade:** só existe árvore geradora se o grafo for conexo. Caso contrário existe uma
  floresta geradora mínima (uma árvore por componente).

## Por que Prim e Kruskal dão o mesmo custo
Os dois escolhem, a cada passo, uma aresta segura pela propriedade do corte. Logo ambos terminam
com uma AGM, e todas as AGMs têm o mesmo custo mínimo. As *arestas* só coincidem garantidamente
quando a AGM é única.
