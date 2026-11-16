# 07 - Testes

Execução (na raiz do repositório):
```
python -m pytest                  # com pytest
python -m unittest discover -s tests -v   # sem pytest
python -m pytest --cov=src --cov-report=term-missing    # cobertura
```

| Arquivo | O que verifica |
|---|---|
| `tests/test_modelos.py` | `Vertice`, `Aresta`, `Grafo` (validações, duplicadas, componentes), `UnionFind`, `MST` |
| `tests/test_algoritmos.py` | exemplos (R$ 9.000 e R$ 18.500), todos os vértices iniciais de Prim, rede desconectada, concordância em 25 redes aleatórias e **comparação com força bruta** em redes pequenas |
| `tests/test_casos_extremos.py` | os 8 casos da seção A.9 do documento do projeto |
| `tests/test_servicos.py` | `ServicoRede`, relatório, formatação, experimento e menu |
| `tests/test_evidencias.py` | Geração de gráficos (tempo/memória), salvamento de relatórios, desenho de rede (imagem), profiling com cProfile e os dois ramos da justificativa de comparação |

## Casos da seção A.9
| # | Caso | Teste |
|---|---|---|
| 1 | Grafo vazio | `test_1_grafo_vazio` |
| 2 | Um único vértice | `test_2_um_unico_vertice` |
| 3 | Grafo desconectado | `test_3_grafo_desconectado` |
| 4 | Arestas duplicadas | `test_4_arestas_duplicadas` |
| 5 | Custos diferentes | `test_5_custos_diferentes` |
| 6 | MST única | `test_6_mst_unica` |
| 7 | Múltiplas MST possíveis | `test_7_multiplas_mst_mesmo_custo` |
| 8 | Custos iguais | `test_8_custos_iguais` |

Nos casos 7 e 8 compara-se o **custo**, não as arestas, porque Prim e Kruskal podem escolher
árvores diferentes com o mesmo custo mínimo.
