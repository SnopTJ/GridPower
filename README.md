# GridPower - Otimização da Infraestrutura Urbana

Projeto do **Squad 2** da plataforma **UrbanTech** (Disciplina de Matemática Discreta e Algoritmos).

O GridPower recebe pontos de uma infraestrutura urbana (subestações, quadros, estações,
reservatórios e pontos de distribuição) e as conexões candidatas com seus custos, e determina
**quais conexões construir para ligar toda a rede com o menor custo total**. Para isso modela a
rede como um grafo não direcionado e calcula a **Árvore Geradora Mínima (AGM)** com os algoritmos
de **Prim** (heap) e **Kruskal** (Union-Find), comparando os resultados.

## Funcionalidades (requisitos RF01 a RF10)
| Código | Funcionalidade |
|---|---|
| RF01 | Cadastrar pontos |
| RF02 | Cadastrar conexões |
| RF03 | Informar custo |
| RF04 | Visualizar rede (texto e imagem) |
| RF05 | Executar Prim |
| RF06 | Executar Kruskal |
| RF07 | Comparar resultados |
| RF08 | Calcular custo total |
| RF09 | Detectar rede desconectada |
| RF10 | Gerar relatório de otimização |

## Estrutura do repositório
```
urban-tech-gridpower/
├── main.py                  interface (menu, --demo, --experimento)
├── requirements.txt
├── pytest.ini
├── docs/                    documentação (01 a 08)
├── src/
│   ├── modelos/             Vertice, Aresta, Grafo, UnionFind, MST
│   ├── algoritmos/          prim.py, kruskal.py (somente o núcleo matemático)
│   ├── servicos/            servico_rede.py, relatorio.py, experimento.py
│   ├── dados/               exemplos.py, gerador.py
│   └── utilitarios/         excecoes.py, formatacao.py, visualizacao.py
├── tests/                   testes automatizados
├── dados/                   bruto/ e processado/
├── notebooks/               exploracao.ipynb
└── relatorios/              complexidade/, profiling/, figuras/
```

## Como executar
```bash
pip install -r requirements.txt

# Modos de execução:
python main.py                  # menu interativo
python main.py --demo           # demonstração: rede de 8 pontos, Prim x Kruskal = R$ 18.500
python main.py --experimento    # experimento de complexidade (10 a 1000 vértices)

# Modo demonstração rápida (apenas 4 pontos):
python main.py --demo --rapido
```

## Dashboard visual (Streamlit)
```bash
streamlit run app.py
```
Abre automaticamente no navegador (http://localhost:8501). O dashboard mostra a rede em layout circular com a AGM destacada, compara Prim e Kruskal em tempo real, gera relatórios em Markdown e roda o experimento de complexidade com gráficos e download de CSV. A paleta de cores foi validada com o validador do método de visualização (CVD ΔE ≥ 9.2, visão normal ΔE ≥ 27.6 em ambos os temas).

**Dica:** O modo `--demo` roda apenas no terminal. Para o dashboard visual, inicie o Streamlit separadamente: `streamlit run app.py`.

## Testes
```bash
python -m pytest                          # ou: python -m unittest discover -s tests -v
python -m pytest --cov=src --cov-report=term-missing
```

## Exemplos de uso
```python
from src.dados.exemplos import rede_exemplo_artigo, rede_exemplo_simples, rede_exemplo_desconectada
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

# Exemplo 3: Rede desconectada (levanta erro)
from src.utilitarios.excecoes import RedeDesconectadaError
g = rede_exemplo_desconectada()
try:
    prim(g)
except RedeDesconectadaError as e:
    print(f"Rede desconectada detectada: {e}")
```

## Documentação
1. [Visão do produto](docs/01_visao_produto.md)
2. [Requisitos](docs/02_requisitos.md)
3. [Modelagem matemática](docs/03_modelagem_matematica.md)
4. [Arquitetura](docs/04_arquitetura.md)
5. [Algoritmos](docs/05_algoritmos.md)
6. [Complexidade](docs/06_complexidade.md)
7. [Testes](docs/07_testes.md)
8. [Resultados](docs/08_resultados.md)

## Equipe (Squad 2)
1. Lázaro Alves Pereira da Silva
2. Gabriel Geraldo Salgado dos Anjos
3. Nilton Clemente de Almeida Neto
4. Gabriel Bezerra Marques
5. Vinícius Gonçalves Araújo
6. João Victor da Conceição Alves Silva
7. Bruno Victor Dos Santos Lima