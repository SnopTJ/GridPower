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
| 10 | 45 | 0.036 | 0.023 | 3.8 | 1.8 | 16,558 |
| 50 | 250 | 0.407 | 0.294 | 16.1 | 9.8 | 154,936 |
| 100 | 500 | 0.804 | 0.512 | 37.3 | 23.3 | 272,127 |
| 500 | 2500 | 5.134 | 3.736 | 357.0 | 139.1 | 1,604,914 |
| 1000 | 5000 | 11.888 | 9.531 | 908.5 | 402.6 | 3,225,832 |

Gráficos: `relatorios/figuras/tempo.png` e `relatorios/figuras/memoria.png`.
Profiling: `relatorios/profiling/perfil.txt`.

> **Atenção:** estes números foram medidos no ambiente em que o repositório foi gerado.
> Rode `python main.py --experimento` na sua máquina e use os **seus** resultados na entrega e no artigo.

## Interpretação
- Prim e Kruskal obtiveram o mesmo custo em todos os tamanhos.
- Nas redes esparsas testadas, Kruskal foi mais rápido e usou menos memória que Prim.
- Uma explicação plausível: Prim monta a lista de adjacência (2|E| entradas) e mantém um heap;
  Kruskal apenas ordena as arestas e mantém estruturas de tamanho |V|.
- Não se deve generalizar para redes densas, que não foram avaliadas.
