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

python main.py                  # menu interativo
python main.py --demo           # demonstração: rede de 8 pontos, Prim x Kruskal = R$ 18.500
python main.py --experimento    # experimento de complexidade (10 a 1000 vértices)
```

## Dashboard visual (Streamlit)
```bash
streamlit run app.py
```
Abre automaticamente no navegador (http://localhost:8501). O dashboard mostra a rede em layout circular com a AGM destacada, compara Prim e Kruskal em tempo real, gera relatórios em Markdown e roda o experimento de complexidade com gráficos e download de CSV. A paleta de cores foi validada com o validador do método de visualização (CVD ΔE ≥ 9.2, visão normal ΔE ≥ 27.6 em ambos os temas).

## Testes
```bash
python -m pytest                          # ou: python -m unittest discover -s tests -v
python -m pytest --cov=src --cov-report=term-missing
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
8. [Inserir nome 8]
9. [Inserir nome 9]