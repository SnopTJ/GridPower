# 08 - Resultados

## Estudo de caso (rede de 8 pontos)
Prim e Kruskal escolhem as mesmas 7 conexões, com custo total de **R$ 18.500**. O Kruskal rejeita
duas conexões por formarem ciclo: Q1-Q2 (R$ 2.600) e P1-P2 (R$ 3.100). Como todos os custos são
distintos, a AGM é única. Rode `python main.py --demo` para ver a saída.

> **Nota:** esta é a única fonte de verdade do estudo de caso. Uma versão anterior da apresentação
> integrada (arquivo `apresentacao-gridpower.html`, já removido) utilizava um exemplo ilustrativo
> separado de 12 pontos e R$ 27.300, que não faz parte do repositório. O caso canônico, usado em
> `main.py --demo`, nos testes e no artigo, é o de 8 pontos e R$ 18.500.

## Experimento de complexidade
Redes sintéticas conexas, |E| = 5|V| (limitado ao grafo completo), custos inteiros entre R$ 1.000
e R$ 20.000. Tempo: mediana de 30 execuções (10 para as maiores); memória: pico do `tracemalloc`.

| \|V\| | \|E\| | Prim (ms) | Kruskal (ms) | Prim (KiB) | Kruskal (KiB) | Custo (R$) |
|---|---|---|---|---|---|---|
| 10 | 45 | 0.070 | 0.040 | 3.8 | 1.8 | 16,558 |
| 50 | 250 | 0.412 | 0.307 | 16.1 | 9.8 | 154,936 |
| 100 | 500 | 0.813 | 0.565 | 37.3 | 23.3 | 272,127 |
| 500 | 2500 | 3.223 | 2.348 | 357.0 | 139.1 | 1,604,914 |
| 1000 | 5000 | 10.748 | 8.746 | 908.5 | 402.6 | 3,225,832 |

Gráficos: `relatorios/figuras/tempo.png` e `relatorios/figuras/memoria.png`.
Profiling: `relatorios/profiling/perfil.txt`.

> **Atenção:** estes números foram medidos no ambiente em que o repositório foi gerado.
> Rode `python main.py --experimento` na sua máquina e use os **seus** resultados na entrega e no artigo.

## Interpretação
- Prim e Kruskal obtiveram o mesmo custo em todos os tamanhos (como esperado para AGM).
- Tempo: o Kruskal foi mais rápido em **todos** os cinco tamanhos testados. A diferença absoluta
  cresce com o tamanho (0,030 ms em |V|=10 contra 2,0 ms em |V|=1000), mas a razão diminui
  (1,76× em |V|=10, 1,23× em |V|=1000), pois o custo da ordenação das arestas (O(E log E))
  é compensado pela ausência de operações de heap. Em |V|=1000: Prim 10,7 ms, Kruskal 8,7 ms.
- Memória: Kruskal usou sempre menos memória que Prim (~2,2× menos em |V|=1000). A vantagem
  vem de Prim construir a lista de adjacência (2|E| entradas) mais um heap, enquanto o Kruskal
  mantém a lista de arestas (já existente no grafo) e as estruturas Union-Find de tamanho |V|.
  A ordenação é feita com `sorted(...)` sobre a lista de arestas, que produz uma nova lista
  ordenada de tamanho |E| (custo real de O(E) memória adicional, não in-place).
- Não se deve generalizar para redes densas, que não foram avaliadas (|E| = 5|V| é esparsa).
