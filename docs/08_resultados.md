# 08 - Resultados

## Estudo de caso (rede de 8 pontos)
Prim e Kruskal escolhem as mesmas 7 conexões, com custo total de **R$ 18.500**. O Kruskal rejeita
duas conexões por formarem ciclo: Q1-Q2 (R$ 2.600) e P1-P2 (R$ 3.100). Como todos os custos são
distintos, a AGM é única. Rode `python main.py --demo` para ver a saída.

## Experimento de complexidade
Redes sintéticas conexas, |E| = 5|V| (limitado ao grafo completo), custos inteiros entre R$ 1.000
e R$ 20.000. Tempo: mediana de 30 execuções (10 para as maiores); memória: pico do `tracemalloc`.

| \|V\| | \|E\| | Prim (ms) | Kruskal (ms) | Prim (KiB) | Kruskal (KiB) | Custo (R$) |
|---|---|---|---|---|---|---|
| 10 | 45 | 0.036 | 0.056 | 3.8 | 1.8 | 16,558 |
| 50 | 250 | 0.410 | 0.442 | 16.1 | 9.8 | 154,936 |
| 100 | 500 | 0.868 | 0.564 | 37.3 | 23.3 | 272,127 |
| 500 | 2500 | 5.470 | 4.097 | 357.0 | 139.1 | 1,604,914 |
| 1000 | 5000 | 15.216 | 8.369 | 908.5 | 402.6 | 3,225,832 |

Gráficos: `relatorios/figuras/tempo.png` e `relatorios/figuras/memoria.png`.
Profiling: `relatorios/profiling/perfil.txt`.

> **Atenção:** estes números foram medidos no ambiente em que o repositório foi gerado.
> Rode `python main.py --experimento` na sua máquina e use os **seus** resultados na entrega e no artigo.

## Interpretação
- Prim e Kruskal obtiveram o mesmo custo em todos os tamanhos (como esperado para AGM).
- Memória: Kruskal usou sempre menos memória que Prim (~2,2× menos em |V|=1000), pois
  mantém apenas estruturas de tamanho |V| (Union-Find) enquanto Prim constrói a lista de
  adjacência (2|E| entradas) e um heap.
- Tempo: em redes pequenas (|V| ≤ 50) o Prim foi ligeiramente mais rápido; a partir de |V|=100
  o Kruskal passa a liderar, e a diferença cresce com o tamanho (8,4 ms contra 15,2 ms em |V|=1000).
  O custo da ordenação das arestas (O(E log E)) fica compensado pela ausência de operações de heap.
- Não se deve generalizar para redes densas, que não foram avaliadas.
