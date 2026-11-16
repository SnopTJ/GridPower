# 02 - Requisitos

## Requisitos funcionais
| Código | Descrição | Onde está no código |
|---|---|---|
| RF01 | Cadastrar pontos | `ServicoRede.cadastrar_ponto` / `Grafo.adicionar_vertice` |
| RF02 | Cadastrar conexões | `ServicoRede.cadastrar_conexao` / `Grafo.adicionar_aresta` |
| RF03 | Informar custo | parâmetro `custo` de `adicionar_aresta` (validado em `Aresta`) |
| RF04 | Visualizar rede | `utilitarios/visualizacao.py` (`descrever_rede`, `desenhar_rede`) |
| RF05 | Executar Prim | `algoritmos/prim.py` |
| RF06 | Executar Kruskal | `algoritmos/kruskal.py` |
| RF07 | Comparar resultados | `ServicoRede.comparar` |
| RF08 | Calcular custo total | `MST.custo_total` |
| RF09 | Detectar rede desconectada | `Grafo.componentes_conexos` e `RedeDesconectadaError` |
| RF10 | Gerar relatório de otimização | `servicos/relatorio.py` |

## Requisitos não funcionais
- **Corretude:** o custo retornado deve ser mínimo (verificado por força bruta em redes pequenas).
- **Desempenho:** Prim em O(E log V) e Kruskal em O(E log V); experimento de 10 a 1000 vértices.
- **Robustez:** entradas inválidas levantam `DadoInvalidoError`; rede desconectada levanta
  `RedeDesconectadaError`. Ambas herdam de `ValueError`.
- **Manutenibilidade:** arquitetura em camadas, docstrings e testes automatizados.

## Casos de uso
1. Cadastrar a rede (RF01 a RF03) e visualizá-la (RF04).
2. Executar Prim e/ou Kruskal (RF05, RF06) e ver o custo (RF08).
3. Comparar os dois algoritmos (RF07).
4. Verificar se a rede é conexa (RF09).
5. Gerar o relatório de otimização (RF10).
