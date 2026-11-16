"""Dashboard visual do GridPower - árvore geradora mínima da infraestrutura urbana.

Uso:
    streamlit run app.py
"""
import csv
import io
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

from src.dados.exemplos import rede_exemplo_artigo
from src.dados.gerador import gerar_rede_sintetica
from src.modelos.grafo import Grafo
from src.servicos.experimento import executar_experimento, perfilar
from src.servicos.relatorio import gerar_relatorio_otimizacao
from src.servicos.servico_rede import ServicoRede
from src.utilitarios.formatacao import formatar_reais

# Cores: paleta validada (CVD ΔE 9.2, visão normal ΔE 27.6 em ambos os temas).
COR_PRIM = "#2a78d6"      # azul
COR_KRUSKAL = "#eb6834"   # laranja
COR_NEUTRA = "#898781"    # cinza para arestas fora da AGM

# ------------------------------------------------------------------ figuras


def _posicoes(grafo):
    """Layout circular: nome -> (x, y)."""
    nomes = grafo.nomes_vertices
    n = max(len(nomes), 1)
    return {
        nome: (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))
        for i, nome in enumerate(nomes)
    }


def _figura_rede(grafo, mst=None, cor_destaque=COR_PRIM):
    """Rede em layout circular; arestas da AGM em cor forte, demais em cinza tracejado."""
    pos = _posicoes(grafo)
    escolhidas = mst.pares() if mst is not None else set()

    fig, ax = plt.subplots(figsize=(6, 5.2))
    for a in grafo.arestas:
        (x1, y1), (x2, y2) = pos[a.origem], pos[a.destino]
        na_mst = a.chave in escolhidas
        ax.plot(
            [x1, x2], [y1, y2],
            color=cor_destaque if na_mst else COR_NEUTRA,
            lw=2.6 if na_mst else 0.8,
            ls="-" if na_mst else "--",
            zorder=1,
        )
        ax.text(
            (x1 + x2) / 2, (y1 + y2) / 2,
            f"{a.custo:,.0f}".replace(",", "."),
            fontsize=7, ha="center", va="center",
            bbox=dict(fc="white", ec="none", pad=0.6, alpha=0.9), zorder=2,
        )
    for nome, (x, y) in pos.items():
        ax.scatter([x], [y], s=620, c="white", edgecolors="#0b0b0b",
                   linewidths=1.4, zorder=3)
        ax.text(x, y, nome, ha="center", va="center", fontsize=8.5, zorder=4)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    return fig


def _figura_serie(ns, serie_prim, serie_kruskal, rotulo_y, titulo):
    """Linhas de Prim e Kruskal em escala log-log com legenda e rótulos diretos."""
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(ns, serie_prim, marker="o", ms=7, lw=2, color=COR_PRIM, label="Prim (heap)")
    ax.plot(ns, serie_kruskal, marker="s", ms=6.5, lw=2, ls="--",
            color=COR_KRUSKAL, label="Kruskal (Union-Find)")
    # rótulos diretos no último ponto (identidade nunca só pela cor)
    ax.annotate("Prim", (ns[-1], serie_prim[-1]), textcoords="offset points",
                xytext=(8, 6), fontsize=9, color=COR_PRIM, fontweight="bold")
    ax.annotate("Kruskal", (ns[-1], serie_kruskal[-1]), textcoords="offset points",
                xytext=(8, -14), fontsize=9, color=COR_KRUSKAL, fontweight="bold")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Número de vértices (|V|)", color="#52514e")
    ax.set_ylabel(rotulo_y, color="#52514e")
    ax.set_title(titulo, color="#0b0b0b", loc="left", fontsize=12)
    ax.set_xticks(ns)
    ax.set_xticklabels([str(n) for n in ns])
    ax.grid(True, which="major", color="#e1e0d9", lw=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#c3c2b7")
    ax.tick_params(colors="#898781", labelsize=8.5)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------ página principal


def _barra_lateral_opcoes():
    """Painel de entrada: escolhe ou gera a rede."""
    st.sidebar.header("Rede")
    modo = st.sidebar.radio(
        "Origem dos dados",
        ["Exemplo do artigo (8 pontos)", "Aleatória", "Personalizada"],
        key="modo_entrada",
    )

    if modo == "Exemplo do artigo (8 pontos)":
        if st.sidebar.button("Carregar exemplo", use_container_width=True):
            grafo = rede_exemplo_artigo()
            st.session_state["grafo"] = grafo
            st.session_state["servico"] = ServicoRede(grafo)

    elif modo == "Aleatória":
        n = st.sidebar.slider("Pontos", 4, 40, 10)
        semente = st.sidebar.number_input("Semente", min_value=0, value=7, step=1)
        if st.sidebar.button("Gerar rede aleatória", use_container_width=True):
            grafo = gerar_rede_sintetica(int(n), semente=int(semente))
            st.session_state["grafo"] = grafo
            st.session_state["servico"] = ServicoRede(grafo)

    else:  # Personalizada
        st.sidebar.caption("Digite os pontos e as conexões.")
        with st.sidebar.form("form_rede", clear_on_submit=False):
            nomes = st.text_area(
                "Pontos (um por linha)",
                "S1\nQ1\nQ2\nE1\nR1\nP1\nP2\nP3",
                height=150,
            )
            conexoes = st.text_area(
                "Conexões (origem, destino, custo)",
                "S1,Q1,2000\nS1,Q2,2200\nQ1,E1,2500\nQ1,Q2,2600\n"
                "Q2,R1,2700\nE1,P1,2800\nR1,P2,3000\nP1,P2,3100\n"
                "P2,P3,3300\nE1,R1,4100\nQ1,P1,4500\nR1,P3,4800\nS1,E1,5200",
                height=230,
            )
            enviado = st.form_submit_button("Montar rede", use_container_width=True)

        if enviado:
            try:
                grafo = Grafo()
                for linha in nomes.splitlines():
                    if linha.strip():
                        grafo.adicionar_vertice(linha.strip())
                for linha in conexoes.splitlines():
                    if not linha.strip():
                        continue
                    partes = [p.strip() for p in linha.replace(";", ",").split(",")]
                    if len(partes) != 3:
                        raise ValueError(f"Linha inválida: {linha!r} (use origem, destino, custo)")
                    grafo.adicionar_aresta(partes[0], partes[1],
                                           float(partes[2].replace(".", "").replace(",", ".")))
                st.session_state["grafo"] = grafo
                st.session_state["servico"] = ServicoRede(grafo)
            except ValueError as erro:
                st.sidebar.error(f"Não foi possível montar a rede: {erro}")


def pagina_dashboard():
    st.title("GridPower")
    st.caption("Otimização da infraestrutura urbana por árvore geradora mínima "
               "(Prim x Kruskal). Squad 2 · UrbanTech.")

    _barra_lateral_opcoes()

    if "servico" not in st.session_state:
        st.info("Escolha uma rede no painel à esquerda para começar.")
        return

    grafo = st.session_state["grafo"]
    servico = st.session_state["servico"]

    total_pares = grafo.quantidade_vertices * (grafo.quantidade_vertices - 1) / 2
    densidade = grafo.quantidade_arestas / total_pares if total_pares else 0.0
    conexa, componentes = servico.verificar_conectividade()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pontos", grafo.quantidade_vertices)
    col2.metric("Conexões", grafo.quantidade_arestas)
    col3.metric("Densidade", f"{densidade:.0%}")
    col4.metric("Conectividade", "Conexa" if conexa else f"{len(componentes)} ilhas")

    if not conexa:
        st.warning(
            "A rede está **desconectada**: não existe árvore geradora. "
            "Componentes: " + " · ".join("{" + ", ".join(c) + "}" for c in componentes)
        )

    # ---------------------------------------------------- comparação
    st.subheader("Prim x Kruskal")
    comparacao = servico.comparar()

    colA, colB, colC = st.columns(3)
    colA.metric("Custo Prim", formatar_reais(comparacao.custo_prim))
    colB.metric("Custo Kruskal", formatar_reais(comparacao.custo_kruskal))
    colC.metric("Conexões na AGM", len(comparacao.prim))

    if comparacao.custos_equivalentes:
        st.success("Os dois algoritmos chegaram ao mesmo custo mínimo.")
    else:
        st.error("Os custos diferem: há erro em alguma das implementações.")

    st.markdown(f"**Mesmas conexões:** {'sim' if comparacao.mesmas_arestas else 'não'}  \n"
                f"**Justificativa:** {comparacao.justificativa}")

    # ---------------------------------------------------- visualização
    st.subheader("Rede e árvore geradora mínima")
    colP, colK = st.columns(2)
    with colP:
        st.caption(f"Prim — {formatar_reais(comparacao.custo_prim)}")
        fig = _figura_rede(grafo, comparacao.prim, COR_PRIM)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with colK:
        st.caption(f"Kruskal — {formatar_reais(comparacao.custo_kruskal)}")
        fig = _figura_rede(grafo, comparacao.kruskal, COR_KRUSKAL)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    st.caption("Linhas grossas coloridas = conexões escolhidas pela AGM. "
               "Linhas finas tracejadas = conexões candidatas descartadas.")

    # ---------------------------------------------------- tabelas e relatório
    with st.expander("Conexões escolhidas"):
        colP, colK = st.columns(2)
        for coluna, arvore in ((colP, comparacao.prim), (colK, comparacao.kruskal)):
            with coluna:
                st.markdown(f"**{arvore.algoritmo}**")
                st.dataframe(
                    [{"Origem": a.origem, "Destino": a.destino,
                      "Custo": formatar_reais(a.custo)}
                     for a in arvore.arestas],
                    use_container_width=True, hide_index=True,
                )

    with st.expander("Todas as conexões candidatas"):
        st.dataframe(
            [{"Origem": a.origem, "Destino": a.destino,
              "Custo": formatar_reais(a.custo),
              "Na AGM (Prim)": "sim" if a.chave in comparacao.prim.pares() else "não"}
             for a in sorted(grafo.arestas, key=lambda a: a.custo)],
            use_container_width=True, hide_index=True,
        )

    st.subheader("Relatório de otimização")
    texto_relatorio = gerar_relatorio_otimizacao(grafo, comparacao)
    st.download_button("Baixar relatório (.md)", texto_relatorio,
                       file_name="relatorio_otimizacao.md")
    st.code(texto_relatorio, language="markdown")


# ------------------------------------------------------------------ experimento


def pagina_experimento():
    st.title("Experimento de complexidade")
    st.caption("Tempo e memória de Prim e Kruskal em redes sintéticas conexas "
               "com |E| = 5|V|.")

    if "resultados" not in st.session_state:
        if st.button("Executar experimento (10 a 1000 vértices)", type="primary"):
            with st.spinner("Medindo tempo e memória... pode levar alguns segundos."):
                st.session_state["resultados"] = executar_experimento()
        else:
            st.info("O experimento mede cada algoritmo em malhas de 10, 50, 100, "
                    "500 e 1000 pontos. Clique para rodar na sua máquina.")
            return

    resultados = st.session_state["resultados"]
    ns = [r["vertices"] for r in resultados]

    st.subheader("Resultados medidos")
    st.dataframe(
        [{"|V|": r["vertices"], "|E|": r["arestas"],
          "Prim (ms)": round(r["prim_ms"], 3),
          "Kruskal (ms)": round(r["kruskal_ms"], 3),
          "Prim (KiB)": round(r["prim_kib"], 1),
          "Kruskal (KiB)": round(r["kruskal_kib"], 1),
          "Custo (R$)": formatar_reais(r["custo_prim"]),
          "Custos iguais": "sim" if r["custos_iguais"] else "NÃO"}
         for r in resultados],
        use_container_width=True, hide_index=True,
    )

    st.subheader("Tempo de execução")
    fig = _figura_serie(ns, [r["prim_ms"] for r in resultados],
                        [r["kruskal_ms"] for r in resultados],
                        "Tempo (ms)", "Tempo por tamanho da rede")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.subheader("Pico de memória")
    fig = _figura_serie(ns, [r["prim_kib"] for r in resultados],
                        [r["kruskal_kib"] for r in resultados],
                        "Pico de memória (KiB)", "Memória por tamanho da rede")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    buffer = io.StringIO()
    escritor = csv.DictWriter(buffer, fieldnames=list(resultados[0]))
    escritor.writeheader()
    escritor.writerows(resultados)
    st.download_button("Baixar resultados (.csv)", buffer.getvalue(),
                       file_name="resultados.csv")

    with st.expander("Profiling com cProfile (n=1000)"):
        if st.button("Gerar perfil"):
            with st.spinner("Profilando..."):
                st.code(perfilar(n=1000), language="text")


# ------------------------------------------------------------------ navegação


def main():
    st.set_page_config(page_title="GridPower Dashboard", page_icon="⚡",
                       layout="wide")

    st.sidebar.title("⚡ GridPower")
    pagina = st.sidebar.radio("Navegação", ["Rede e AGM", "Experimento"])

    if pagina == "Rede e AGM":
        pagina_dashboard()
    else:
        pagina_experimento()


if __name__ == "__main__":
    main()