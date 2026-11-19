# GridPower - Estrutura do Repositório e Requisições

## Visão Geral do Projeto

**GridPower** é um projeto de otimização da infraestrutura urbana desenvolvido pelo **Squad 2** da plataforma **UrbanTech** (disciplina de Matemática Discreta e Algoritmos). O sistema modela redes de abastecimento urbano como grafos não direcionados e calcula a Árvore Geradora Mínima (AGM) usando os algoritmos **Prim** (com heap) e **Kruskal** (com Union-Find), comparando resultados e gerando relatórios.

---

## Estrutura de Diretórios

### Raiz do Repositório

| Arquivo | Descrição |
|---|---|
| `app.py` | Dashboard principal Streamlit (visualização da rede, AGM, experimentos de complexidade) |
| `main.py` | Interface CLI com menu interativo, demonstração e modo experimento |
| `README.md` | Documentação completa do projeto (funcionalidades, execução, testes) |
| `requirements.txt` | Dependências: pytest>=8.0, pytest-cov>=5.0, matplotlib>=3.8, streamlit>=1.67 |
| `pytest.ini` | Configuração de testes |
| `LICENSE` | Licença do projeto |

### `docs/` - Documentação Técnica

| Arquivo | Conteúdo |
|---|---|
| `01_visao_produto.md` | Visão do produto e requisitos do usuário |
| `02_requisitos.md` | Requisitos funcionais RF01 a RF10 |
| `03_modelagem_matematica.md` | Modelagem do problema como grafo, propriedades da AGM |
| `04_arquitetura.md` | Arquitetura em camadas: interface → serviços → algoritmos → dados → estruturas |
| `05_algoritmos.md` | Implementações de Kruskal (Union-Find) e Prim (heap), pseudocódigo, tabela de comparação |
| `06_complexidade.md` | Análise de complexidade: Prim O(E log V), Kruskal O(E log V), Union-Find O(E · α(V)) |
| `07_testes.md` | Estratégias de teste, casos de teste extremos, evidências |
| `08_resultados.md` | Resultados de experimentos (tabela de tempos e memória para redes de 10 a 1000 vértices) |
| `artigo_gridpower.docx` | Versão em documento do artigo do projeto |
| `previa_desenvolvimento.md` | Registro de desenvolvimento preliminar |

### `src/` - Código-Fonte Organizado por Camadas

#### `src/modelos/` - Modelos de Dados

| Arquivo | Descrição |
|---|---|
| `vertice.py` | Classe Vertex vértice (nome, tipo: subestacao, quadro, estação, reservatório, distribuição) |
| `aresta.py` | Classe Aresta com atributos origem, destino, custo |
| `grafo.py` | Classe Grafo com métodos para adicionar vértices/arestas, lista de adjacência, componentes conexos |
| `mst.py` | Classe MST (Árvore Geradora Mínima) armazenando arestas selecionadas e custo total |
| `union_find.py` | Estrutura Union-Find com *find* (com compressão de caminho) e *union* (por rank) |

#### `src/algoritmos/` - Núcleo Matemático dos Algoritmos

| Arquivo | Descrição |
|---|---|
| `prim.py` | Algoritmo de Prim com lista de adjacência e fila de prioridade (heap). Complexidade O(E log V) |
| `kruskal.py` | Algoritmo de Kruskal com Union-Find. Complexidade O(E log E) = O(E log V) |

#### `src/dados/` - Dados e Geração de Redes

| Arquivo | Descrição |
|---|---|
| `exemplos.py` | Redes de exemplo: artigo (8 pts, R$ 18.500), simples (4 pts, R$ 9.000), desconectada (6 pts, 2 ilhas), 5/6/7 pontos |
| `gerador.py` | Geração de redes sintéticas para experimentos de complexidade |

#### `src/servicos/` - Serviços e Casos de Uso

| Arquivo | Descrição |
|---|---|
| `servico_rede.py` | Serviço principal (RF01-RF09): cadastrar pontos, conexões, executar Prim/Kruskal, comparar, verificar conectividade |
| `experimento.py` | Experimento de complexidade (Sprint 4): mede tempo e memória para tamanhos 10, 50, 100, 500, 1000 vértices |
| `relatorio.py` | Geração de relatórios de otimização em Markdown com formatação de valores em Reais |

#### `src/utilitarios/` - Utilitários Gerais

| Arquivo | Descrição |
|---|---|
| `excecoes.py` | Exceções personalizadas: `RedeDesconectadaError`, `DadoInvalidoError` |
| `formatacao.py` | Função `formatar_reais` para formatação de valores monetários |
| `visualizacao.py` | Funções de visualização de redes e gráficos de complexidade |

### `tests/` - Testes Automatizados

| Arquivo | Finalidade |
|---|---|
| `test_algoritmos.py` | Testes unitários dos algoritmos Prim e Kruskal |
| `test_casos_extremos.py` | Testes com redes desconectadas, simples, casos extremos |
| `test_evidencias.py` | Validação das evidências do projeto |
| `test_modelos.py` | Testes das classes de modelo (Grafo, MST, Union-Find, Vertice, Aresta) |
| `test_servicos.py` | Testes dos serviços (RF01 a RF10) |

### `dados/` - Dados Brutos e Processados

| Diretório | Conteúdo |
|---|---|
| `dados/bruto/.gitkeep` | Dados de entrada brutos |
| `dados/processado/.gitkeep` | Dados processados para análise |

### `notebooks/` - Notebooks de Exploração

- `exploracao.ipynb` - Análise exploratória de dados e experimentos

### `relatorios/` - Relatórios Gerados

- `complexidade/` - Gráficos de tempo e memória do experimento
- `profiling/` - Relatórios de profiling cProfile
- `figuras/` - Figuras e imagens geradas

---

## Funcionalidades (Requisitos RF01 a RF10)

| Código | Funcionalidade |
|---|---|
| **RF01** | Cadastrar pontos na rede (subestações, quadros, estações, reservatórios, pontos de distribuição) |
| **RF02** | Cadastrar conexões candidatas entre pontos com custos associados |
| **RF03** | Informar o custo de cada conexão candidata |
| **RF04** | Visualizar a rede em layout circular com a AGM destacada |
| **RF05** | Executar algoritmo de Prim (com heap) para encontrar AGM |
| **RF06** | Executar algoritmo de Kruskal (com Union-Find) para encontrar AGM |
| **RF07** | Comparar resultados de Prim e Kruskal (custos equivalentes, mesmas arestas) |
| **RF08** | Calcular custo total da Árvore Geradora Mínima |
| **RF09** | Detectar se a rede está desconecta (levanta exceção `RedeDesconectadaError`) |
| **RF10** | Gerar relatório de otimização em Markdown |

---

## Modos de Execução

### Modo CLI Interativo

```bash
python main.py          # menu interativo
python main.py --demo   # demonstração: rede de 8 pontos, Prim x Kruskal = R$ 18.500
python main.py --experimento  # experimento de complexidade (10 a 1000 vértices)
python main.py --demo --rapido  # modo demonstração rápida (apenas 4 pontos)
```

### Dashboard Streamlit

```bash
streamlit run app.py
```

- Abre automaticamente no navegador em `http://localhost:8501`
- Mostra a rede em layout circular com AGM destacada
- Compara Prim e Kruskal em tempo real
- Gera relatórios em Markdown e roda experimento de complexidade com gráficos e download de CSV

---

## Exemplos de Uso

```python
from src.dados.exemplos import rede_exemplo_artigo, rede_exemplo_simples
from src.algoritmos.prim import prim
from src.algoritmos.kruskal import kruskal

# Exemplo 1: Rede do artigo (8 pontos)
g = rede_exemplo_artigo()
agm_prim = prim(g)
agm_kruskal = kruskal(g)
print(f"Artigo - Custo Prim: R$ {agm_prim.custo_total:,}")
print(f"Artigo - Custo Kruskal: R$ {agm_kruskal.custo_total:,}")

# Exemplo 2: Rede simples (4 pontos)
g = rede_exemplo_simples()
agm_prim = prim(g)
agm_kruskal = kruskal(g)
print(f"Simples - Custo: R$ {agm_prim.custo_total:,}")
```

---

## Arquitetura em Camadas

O projeto segue uma arquitetura em 5 camadas, separando preocupações:

1. **Interface** (app.py, main.py) - Interação com usuário, dashboard Streamlit, CLI
2. **Serviços** (servico_rede.py, experimento.py, relatorio.py) - Casos de uso, lógica de aplicação RF01-RF10
3. **Algoritmos** (prim.py, kruskal) - Núcleo matemático dos algoritmos MST
4. **Dados** (exemplos.py, gerador.py) - Dados de exemplo e geração de redes sintéticas
5. **Estruturas** (grafo.py, union_find.py, mst.py, vertice.py, aresta.py) - Abstrações de dados fundamentais

---

## Testes

```bash
python -m pytest                          # ou: python -m unittest discover -s tests -v
python -m pytest --cov=src --cov-report=term-missing
```

---

## Deploy e Hospedagem

- **Streamlit Community Cloud**: recomendado para deployment rápido
- **PythonAnywhere**: alternativa para hospedagem contínua
- **Railway/Render**: opções de hospedagem de aplicações Python

---

## Equipe (Squad 2)

1. Lázaro Alves Pereira da Silva
2. Gabriel Geraldo Salgado dos Anjos
3. Nilton Clemente de Almeida Neto
4. Gabriel Bezerra Marques
5. Vinícius Gonçalves Araújo
6. João Victor da Conceição Alves Silva
7. Bruno Victor Dos Santos Lima