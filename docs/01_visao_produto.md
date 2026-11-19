# 01 - Visão do Produto

**Projeto:** GridPower - Otimização da Infraestrutura Urbana (Squad 2 da plataforma UrbanTech)

## Problema
Conectar pontos de uma infraestrutura urbana (subestações, quadros, estações, reservatórios e
pontos de distribuição) gastando o mínimo possível em cabeamento ou tubulação.

## Usuário
Gestor ou analista de infraestrutura urbana que precisa decidir **quais conexões construir**.

## Objetivo
Dado um conjunto de pontos e de conexões candidatas com custo, determinar o conjunto de conexões
que liga toda a rede com o menor custo total (Árvore Geradora Mínima).

## Entrada → Processamento → Saída
| Etapa | Descrição |
|---|---|
| Entrada | Pontos, conexões candidatas e custo (em R$) de cada conexão |
| Processamento | Validação, execução de Prim e de Kruskal sobre a mesma rede, comparação |
| Saída | Conexões escolhidas, custo total, verificação de equivalência, relatório de otimização |

## Valor produzido
- Reduz o custo de implantação de redes em relação a escolher conexões sem critério.
- Detecta redes desconectadas antes de qualquer obra.
- Permite comparar dois algoritmos clássicos e entender por que chegam ao mesmo custo.

## Fora do escopo
Microsserviços, banco de dados, API REST, Docker e frameworks web puros. O foco é Python,
estruturas discretas, algoritmos, Git/GitHub, testes, profiling e matplotlib.

**Observação:** O dashboard Streamlit (python -m streamlit run app.py) é uma interface
complementar para visualização e testes rápidos. Como frameworks web estão fora do escopo,
confirme com o professor se essa interface pode permanecer como "extra" ou se deve ser removida.

## Limitação conhecida
A AGM é uma árvore: minimiza o custo, mas **não tem redundância**. A falha de uma conexão
desconecta parte da rede.
