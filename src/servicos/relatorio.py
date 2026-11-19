"""Relatório de otimização (RF10)."""
from datetime import datetime

from src.utilitarios.formatacao import formatar_reais


def gerar_relatorio_otimizacao(grafo, comparacao):
    """Retorna o relatório em texto (formato Markdown)."""
    linhas = [
        "# Relatório de otimização - GridPower",
        f"Gerado em {datetime.now():%d/%m/%Y %H:%M}",
        "",
        "## Rede analisada",
        f"- Pontos: {grafo.quantidade_vertices}",
        f"- Conexões candidatas: {grafo.quantidade_arestas}",
        "",
        "## Resultado",
    ]
    for arvore in (comparacao.prim, comparacao.kruskal):
        linhas.append(f"### {arvore.algoritmo} - custo total {formatar_reais(arvore.custo_total)}")
        for a in arvore.arestas:
            linhas.append(f"- {a.origem} -- {a.destino}: {formatar_reais(a.custo)}")
        linhas.append("")
    linhas += [
        "## Comparação",
        f"- Custos equivalentes: {'sim' if comparacao.custos_equivalentes else 'NÃO'}",
        f"- Mesmas conexões: {'sim' if comparacao.mesmas_arestas else 'não'}",
        f"- Justificativa: {comparacao.justificativa}",
    ]
    return "\n".join(linhas) + "\n"


def salvar_relatorio(texto, caminho):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)
