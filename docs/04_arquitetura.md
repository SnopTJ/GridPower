# 04 - Arquitetura

## Camadas (padrão UrbanTech)
```mermaid
flowchart TB
    I["INTERFACE<br/>main.py (menu / --demo / --experimento)"]
    A["CAMADA DE APLICAÇÃO<br/>servicos/ (ServicoRede, relatorio, experimento)"]
    N["NÚCLEO MATEMÁTICO<br/>algoritmos/ (prim, kruskal)"]
    E["ESTRUTURAS DE DADOS<br/>modelos/ (Vertice, Aresta, Grafo, UnionFind, MST)"]
    D["DADOS / E-S<br/>dados/ (exemplos, gerador) + relatorios/"]
    I --> A --> N --> E --> D
```

## Fluxo de uma comparação (RF07)
```mermaid
sequenceDiagram
    actor U as Usuário
    participant M as main.py
    participant S as ServicoRede
    participant G as Grafo
    participant P as prim()
    participant K as kruskal()
    U->>M: opção "Comparar"
    M->>S: comparar()
    S->>P: prim(grafo)
    P->>G: lista_adjacencia()
    P-->>S: MST (Prim)
    S->>K: kruskal(grafo)
    K->>G: arestas
    K-->>S: MST (Kruskal)
    S-->>M: ResultadoComparacao
    M-->>U: custos, arestas e justificativa
```

## Estrutura de pastas
| Pasta | Conteúdo |
|---|---|
| `src/modelos/` | entidades do domínio: `Vertice`, `Aresta`, `Grafo`, `UnionFind`, `MST` |
| `src/algoritmos/` | somente o núcleo matemático: `prim.py`, `kruskal.py` |
| `src/servicos/` | casos de uso: `servico_rede.py`, `relatorio.py`, `experimento.py` |
| `src/dados/` | redes de exemplo e gerador de redes sintéticas |
| `src/utilitarios/` | exceções, formatação em reais e visualização |
| `tests/` | testes automatizados |
| `docs/` | documentação |
| `relatorios/` | CSV de complexidade, profiling e figuras |

(Equivalência com o modelo do documento UrbanTech: models→modelos, algorithms→algoritmos,
services→servicos, data→dados, utils→utilitarios.)

## Decisões de projeto
- Os vértices são identificados por **nome** (texto), simples de cadastrar e de ler nos relatórios.
- Arestas duplicadas: mantém-se a de **menor custo** (A–B e B–A são a mesma conexão).
- Desempate determinístico `(custo, origem, destino)` para resultados reprodutíveis.
- Prim usa o primeiro ponto cadastrado como início, salvo se outro for informado.
