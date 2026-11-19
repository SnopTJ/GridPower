"""Dashboard visual do GridPower — Otimização da Infraestrutura Urbana por Árvore Geradora Mínima.
Executar:  streamlit run app.py
"""

"""Redes de exemplo usadas na demonstração, nos testes e no artigo."""
from src.modelos.grafo import Grafo
from src.servicos.servico_rede import ServicoRede
from src.utilitarios.formatacao import formatar_reais

CUSTO_EXEMPLO_ARTIGO = 18500.0   # custo mínimo da rede de 8 pontos (seção A.8 do projeto)


def rede_exemplo_artigo():
    """Rede de 8 pontos e 13 conexões; AGM única com custo R$ 18.500 (Figura 1 do artigo)."""
    g = Grafo()
    for nome, tipo in [("S1", "subestacao"), ("Q1", "quadro"), ("Q2", "quadro"),
                       ("E1", "estacao"), ("R1", "reservatorio"),
                       ("P1", "distribuicao"), ("P2", "distribuicao"), ("P3", "distribuicao")]:
        g.adicionar_vertice(nome, tipo)
    conexoes = [("S1", "Q1", 2000), ("S1", "Q2", 2200), ("Q1", "E1", 2500),
                ("Q1", "Q2", 2600), ("Q2", "R1", 2700), ("E1", "P1", 2800),
                ("R1", "P2", 3000), ("P1", "P2", 3100), ("P2", "P3", 3300),
                ("E1", "R1", 4100), ("Q1", "P1", 4500), ("R1", "P3", 4800),
                ("S1", "E1", 5200)]
    for a, b, custo in conexoes:
        g.adicionar_aresta(a, b, custo)
    return g


def rede_exemplo_simples():
    """Rede de 4 pontos do protótipo inicial; custo mínimo R$ 9.000."""
    g = Grafo()
    for nome in ["A", "B", "C", "D"]:
        g.adicionar_vertice(nome)
    for a, b, custo in [("A", "B", 4000), ("A", "C", 2000), ("B", "C", 5000),
                        ("B", "D", 3000), ("C", "D", 6000)]:
        g.adicionar_aresta(a, b, custo)
    return g


def rede_exemplo_desconectada():
    """Rede urbana de 6 pontos dividida em 2 ilhas isoladas (Setor Norte e Setor Sul)."""
    g = Grafo()
    for nome, tipo in [("Sub-A", "subestacao"), ("Q-Norte1", "quadro"), ("Q-Norte2", "quadro"),
                       ("Sub-B", "subestacao"), ("Q-Sul1", "quadro"), ("Est-Sul", "estacao")]:
        g.adicionar_vertice(nome, tipo)
    # Ilha 1 (Norte)
    g.adicionar_aresta("Sub-A", "Q-Norte1", 2000)
    g.adicionar_aresta("Q-Norte1", "Q-Norte2", 1500)
    # Ilha 2 (Sul - isolada da Norte)
    g.adicionar_aresta("Sub-B", "Q-Sul1", 2500)
    g.adicionar_aresta("Q-Sul1", "Est-Sul", 1800)
    return g


def rede_exemplo_5_pontos():
    """Rede de 5 pontos com 7 conexões; custo mínimo R$ 10.000."""
    g = Grafo()
    for nome in ["A", "B", "C", "D", "E"]:
        g.adicionar_vertice(nome)
    for a, b, custo in [("A", "B", 3000), ("A", "C", 2500),
                        ("B", "C", 4000), ("B", "D", 2000),
                        ("C", "E", 3500), ("D", "E", 2500),
                        ("A", "E", 4500)]:
        g.adicionar_aresta(a, b, custo)
    return g


def rede_exemplo_6_pontos():
    """Rede de 6 pontos com 9 conexões; custo mínimo R$ 12.500."""
    g = Grafo()
    for nome in ["A", "B", "C", "D", "E", "F"]:
        g.adicionar_vertice(nome)
    for a, b, custo in [("A", "B", 3000), ("A", "C", 2000),
                        ("B", "D", 4000), ("C", "D", 2500),
                        ("C", "E", 3000), ("D", "F", 2000),
                        ("E", "F", 3500), ("A", "F", 4500),
                        ("B", "E", 3500)]:
        g.adicionar_aresta(a, b, custo)
    return g


def rede_exemplo_7_pontos():
    """Rede de 7 pontos com 10 conexões; custo mínimo R$ 15.000."""
    g = Grafo()
    for nome in ["A", "B", "C", "D", "E", "F", "G"]:
        g.adicionar_vertice(nome)
    for a, b, custo in [("A", "B", 3000), ("A", "C", 2500),
                        ("B", "D", 4000), ("C", "D", 2500),
                        ("C", "E", 3000), ("D", "F", 2000),
                        ("E", "F", 3500), ("E", "G", 2000),
                        ("F", "G", 3000), ("A", "G", 4000)]:
        g.adicionar_aresta(a, b, custo)
    return g


EXEMPLOS = {
    "artigo": rede_exemplo_artigo,
    "simples": rede_exemplo_simples,
    "desconectada": rede_exemplo_desconectada,
    "5_pontos": rede_exemplo_5_pontos,
    "6_pontos": rede_exemplo_6_pontos,
    "7_pontos": rede_exemplo_7_pontos,
}

# ────────────────────────────── PALETA VALIDADA (CVD ΔE ≥ 9.2, visão normal ΔE ≥ 27.6)
# Palette validated using CVD-aware rules: OkLab × 100 minimum ΔE ≥ 8 on adjacent pairs
# Light mode: blue #2a78d6, orange #eb6834, gray #898781, white background
# Dark mode: adapted from same palette
COR_PRIM = "#2a78d6"      # azul (categorical prime)
COR_KRUSKAL = "#eb6834"   # laranja (categorical secondary)
COR_NEUTRA = "#898781"    # cinza neutro
COR_FUNDO_LIGHT = "#0e1117"
COR_FUNDO_DARK = "#1a1d24"
COR_TEXTO_LIGHT = "#e6e6e6"
COR_TEXTO_DARK = "#c8c8c8"

# ────────────────────────────── CONFIGURAÇÃO DA PÁGINA
import streamlit as st

st.set_page_config(
    page_title="GridPower — AGM Urbana",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ────────────────────────────── CSS GLOBAL — MODO APRESENTAÇÃO
APRESENTACAO_CSS = """
<style>
/* ====== MODO APRESENTAÇÃO (toggle) ====== */
.apresentacao .stSidebar { display: none !important; }
.apresentacao .block-container { max-width: 100% !important; padding-left: 1rem !important; padding-right: 1rem !important; }
.apresentacao h1 { font-size: 2.6rem !important; font-weight: 700 !important; }
.apresentacao h2 { font-size: 1.9rem !important; font-weight: 600 !important; }
.apresentacao h3 { font-size: 1.5rem !important; font-weight: 600 !important; }
.apresentacao .stMetric { font-size: 1.6rem !important; }
.apresentacao .stMetric label { font-size: 1.2rem !important; }
.apresentacao .stMetric div[data-testid="stMetricValue"] { font-size: 2.2rem !important; }
.apresentacao .stCaption, .apresentacao .stMarkdown p { font-size: 1.15rem !important; line-height: 1.5 !important; }
.apresentacao .stDataFrame { font-size: 1.1rem !important; }
.apresentacao .stTabs [data-baseweb="tab"] { font-size: 1.2rem !important; padding: 0.6rem 1.2rem !important; }
.apresentacao .stButton > button { font-size: 1.15rem !important; padding: 0.6rem 1.4rem !important; }
.apresentacao .stSelectbox label, .apresentacao .stSlider label, .apresentacao .stNumberInput label,
.apresentacao .stTextArea label, .apresentacao .stRadio label { font-size: 1.15rem !important; }
.apresentacao .stExpander summary { font-size: 1.2rem !important; font-weight: 600 !important; }
.apresentacao .stCodeBlock { font-size: 1.05rem !important; }
.apresentacao .stDownloadButton > button { font-size: 1.15rem !important; padding: 0.6rem 1.4rem !important; }

/* ====== BASE (sempre ativo) ====== */
.block-container { padding-top: 1.5rem; }
h1 { color: #e6e6e6; font-weight: 700; margin-bottom: 0.3rem; }
h2 { color: #f0f0f0; font-weight: 600; margin-top: 1.8rem; margin-bottom: 0.6rem; }
h3 { color: #f5f5f5; font-weight: 600; }
.stMetric { background: #1a1d24; border: 1px solid #2a2d35; border-radius: 12px; padding: 1rem 1.2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.3); }
.stMetric label { color: #a0a0a0 !important; font-weight: 500; }
.stTabs [data-baseweb="tab-list"] { gap: 0.4rem; }
.stTabs [data-baseweb="tab"] { border-radius: 8px 8px 0 0; background: #1a1d24; border: 1px solid #2a2d35; border-bottom: none; transition: all 0.15s; }
.stTabs [aria-selected="true"] { background: #0e1117 !important; border-color: #2a78d6 !important; border-bottom: 2px solid #2a78d6 !important; font-weight: 600; }
.stButton > button[kind="primary"] { background: #2a78d6; border: none; border-radius: 8px; }
.stButton > button[kind="secondary"] { background: #1a1d24; border: 1px solid #2a2d35; border-radius: 8px; color: #e6e6e6; }
.stButton > button:hover { filter: brightness(1.15); }
.stExpander { border: 1px solid #2a2d35; border-radius: 10px; background: #1a1d24; }
.stDataFrame { border: 1px solid #2a2d35; border-radius: 8px; }
[data-testid="stSidebar"] { background: #0e1117; border-right: 1px solid #2a2d35; }
.stRadio [role="radiogroup"] label { font-size: 1rem; color: #e6e6e6; }
.stSlider [data-testid="stTickBar"] { display: none; }
</style>
"""

def _inject_css(modo_apresentacao: bool):
    css = APRESENTACAO_CSS
    if modo_apresentacao:
        css = css.replace(".apresentacao ", "")
    st.markdown(css, unsafe_allow_html=True)

# ────────────────────────────── FIGURAS — LAYOUT CIRCULAR GRANDE
import math
import matplotlib.pyplot as plt

def _posicoes(grafo: Grafo) -> dict:
    nomes = grafo.nomes_vertices
    n = max(len(nomes), 1)
    return {
        nome: (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))
        for i, nome in enumerate(nomes)
    }

def _figura_rede(grafo: Grafo, mst=None, cor_destaque=COR_PRIM, titulo: str = "") -> plt.Figure:
    """Rede em layout circular; arestas da AGM em cor forte, demais em cinza tracejado."""
    pos = _posicoes(grafo)
    escolhidas = mst.pares() if mst is not None else set()

    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=120)
    fig.patch.set_facecolor(COR_FUNDO_LIGHT)
    ax.set_facecolor(COR_FUNDO_LIGHT)
    for a in grafo.arestas:
        (x1, y1), (x2, y2) = pos[a.origem], pos[a.destino]
        na_mst = a.chave in escolhidas
        ax.plot(
            [x1, x2], [y1, y2],
            color=cor_destaque if na_mst else COR_NEUTRA,
            lw=3.5 if na_mst else 1.2,
            ls="-" if na_mst else "--",
            zorder=1,
            alpha=0.95 if na_mst else 0.6,
        )
        # rótulo de custo no meio da aresta (bem visível, fundo escuro)
        ax.text(
            (x1 + x2) / 2, (y1 + y2) / 2,
            f"R$ {a.custo:,.0f}".replace(",", "."),
            fontsize=11, ha="center", va="center", fontweight="bold",
            color="#e6e6e6",
            bbox=dict(fc="#1a1d24", ec=cor_destaque if na_mst else COR_NEUTRA, lw=1.5, pad=4, alpha=0.98),
            zorder=2,
        )
    # vértices
    for nome, (x, y) in pos.items():
        ax.scatter([x], [y], s=900, c="#1a1d24", edgecolors="#e6e6e6", linewidths=2, zorder=3)
        ax.text(x, y, nome, ha="center", va="center", fontsize=12, fontweight="bold", color="#e6e6e6", zorder=4)
    ax.set_aspect("equal")
    ax.axis("off")
    if titulo:
        ax.set_title(titulo, fontsize=16, fontweight="bold", pad=16, color=COR_TEXTO_LIGHT)
    fig.tight_layout(pad=1.0)
    return fig

def _figura_serie(ns, serie_prim, serie_kruskal, rotulo_y, titulo) -> plt.Figure:
    """Linhas de Prim e Kruskal em escala log-log com legenda e rótulos diretos."""
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=120)
    fig.patch.set_facecolor(COR_FUNDO_LIGHT)
    ax.set_facecolor(COR_FUNDO_LIGHT)
    ax.plot(ns, serie_prim, marker="o", ms=10, lw=3, color=COR_PRIM, label="Prim (heap)")
    ax.plot(ns, serie_kruskal, marker="s", ms=9, lw=3, ls="--", color=COR_KRUSKAL, label="Kruskal (Union-Find)")
    # rótulos diretos no último ponto
    ax.annotate("Prim", (ns[-1], serie_prim[-1]), textcoords="offset points",
                xytext=(12, 10), fontsize=11, color=COR_PRIM, fontweight="bold")
    ax.annotate("Kruskal", (ns[-1], serie_kruskal[-1]), textcoords="offset points",
                xytext=(12, -18), fontsize=11, color=COR_KRUSKAL, fontweight="bold")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Número de vértices (|V|)", fontsize=13, color="#a0a0a0", labelpad=10)
    ax.set_ylabel(rotulo_y, fontsize=13, color="#a0a0a0", labelpad=10)
    ax.set_title(titulo, fontsize=16, fontweight="bold", color=COR_TEXTO_LIGHT, loc="left", pad=12)
    ax.set_xticks(ns)
    ax.set_xticklabels([str(n) for n in ns], fontsize=11, color="#c8c8c8")
    ax.tick_params(axis='y', labelsize=11, colors="#a0a0a0")
    ax.grid(True, which="major", color="#2a2d35", lw=1)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#2a2d35")
        ax.spines[lado].set_linewidth(1.2)
    ax.legend(frameon=True, fontsize=12, loc="upper left", facecolor=COR_FUNDO_LIGHT, edgecolor="#2a2d35", labelcolor=COR_TEXTO_LIGHT)
    fig.tight_layout()
    return fig

# ────────────────────────────── TOGGLE FLUTUANTE (sempre visível no conteúdo)
def _toggle_float(modo_apresentacao: bool):
    """Botão de alternância no topo do conteúdo — sempre visível, mesmo com a barra lateral escondida.

    Quando o modo apresentação está ligado, o CSS `.apresentacao .stSidebar { display: none }`
    esconde a barra lateral inteira — incluindo o toggle que está dentro dela. Isso criava um
    "ponto sem saída": o usuário ligava o modo e não conseguia desligar.
    Este botão no conteúdo principal é a saída confiável, e também serve para ligar o modo
    quando a barra lateral estiver escondida por qualquer outro motivo.
    """
    col_toggle, _ = st.columns([4.0, 8.0])
    with col_toggle:
        if modo_apresentacao:
            rotulo = "❌ Sair do modo apresentação"
            ajuda = "Desliga o modo apresentação (barra lateral, fontes grandes)"
            tipo = "primary"
        else:
            rotulo = "🖥️ Ativar modo apresentação (projetor)"
            ajuda = "Esconde a barra lateral, aumenta fontes e figuras para projetor"
            tipo = "secondary"
        if st.button(rotulo, key="toggle_float", help=ajuda, use_container_width=True, type=tipo):
            st.session_state["modo_apresentacao"] = not modo_apresentacao
            st.rerun()


# ────────────────────────────── SIDEBAR — ENTRADA DE DADOS
def _sidebar_entrada():
    st.sidebar.header("⚡  Entrada da Rede")
    modo = st.sidebar.radio(
        "Origem dos dados",
        ["Exemplo do artigo (8 pts)", "Exemplo simples (4 pts)", "Exemplo desconectado", "Aleatória", "Personalizada"],
        key="modo_entrada",
    )

    if modo == "Exemplo do artigo (8 pts)":
        if st.sidebar.button("Carregar exemplo do artigo", use_container_width=True, type="primary"):
            st.session_state["grafo"] = rede_exemplo_artigo()
            st.session_state["servico"] = ServicoRede(st.session_state["grafo"])
            st.toast("Rede do artigo carregada (R$ 18.500)", icon="✅")

    elif modo == "Exemplo simples (4 pts)":
        if st.sidebar.button("Carregar exemplo simples", use_container_width=True):
            st.session_state["grafo"] = rede_exemplo_simples()
            st.session_state["servico"] = ServicoRede(st.session_state["grafo"])
            st.toast("Exemplo simples carregado (R$ 9.000)", icon="✅")

    elif modo == "Exemplo desconectado":
        if st.sidebar.button("Carregar exemplo desconectado", use_container_width=True):
            st.session_state["grafo"] = rede_exemplo_desconectada()
            st.session_state["servico"] = ServicoRede(st.session_state["grafo"])
            st.toast("Rede desconectada carregada (2 ilhas)", icon="⚠️")

    elif modo == "Aleatória":
        n = st.sidebar.slider("Número de pontos (|V|)", 4, 60, 12, help="Redes sintéticas conexas com |E| = 5|V|")
        semente = st.sidebar.number_input("Semente (reprodutibilidade)", min_value=0, value=42, step=1)
        if st.sidebar.button("Gerar rede aleatória", use_container_width=True, type="primary"):
            from src.dados.gerador import gerar_rede_sintetica
            grafo = gerar_rede_sintetica(int(n), semente=int(semente))
            st.session_state["grafo"] = grafo
            st.session_state["servico"] = ServicoRede(grafo)
            st.toast(f"Rede gerada: {grafo.quantidade_vertices} vértices, {grafo.quantidade_arestas} arestas", icon="🎲")

    else:  # Personalizada
        st.sidebar.caption("Digite os pontos (um por linha) e conexões (origem, destino, custo).")
        with st.sidebar.form("form_rede", clear_on_submit=False):
            nomes = st.text_area(
                "Pontos (um por linha)",
                "S1\nQ1\nQ2\nE1\nR1\nP1\nP2\nP3",
                height=140,
            )
            conexoes = st.text_area(
                "Conexões (origem, destino, custo)",
                "S1,Q1,2000\nS1,Q2,2200\nQ1,E1,2500\nQ1,Q2,2600\n"
                "Q2,R1,2700\nE1,P1,2800\nR1,P2,3000\nP1,P2,3100\n"
                "P2,P3,3300\nE1,R1,4100\nQ1,P1,4500\nR1,P3,4800\nS1,E1,5200",
                height=220,
            )
            enviado = st.form_submit_button("Montar rede", use_container_width=True, type="primary")

        if enviado:
            try:
                grafo = Grafo()
                for linha in nomes.splitlines():
                    if linha.strip():
                        grafo.adicionar_vertice(linha.strip())
                for linha in conexoes.splitlines():
                    if not linha.strip():
                        continue
                    # Divide em até 3 campos, preservando vírgula decimal no custo
                    # Remove pontos que são separadores de milhar, mantém vírgula decimal
                    partes = [p.strip() for p in linha.replace(";", ",").split(",", 2)]
                    if len(partes) != 3:
                        raise ValueError(f"Linha inválida: {linha!r} (use: origem, destino, custo)")
                    custo_str = partes[2].strip()
                    # Normaliza: trata vírgula como decimal (formato brasileiro) e ponto como milhar
                    if "," in custo_str:
                        # Formato com vírgula decimal: "2000,50" ou "2.000,50"
                        if "." in custo_str:
                            # Tem ambos: "2.000,50" -> remove pontos (milhar), troca vírgula por ponto
                            custo = float(custo_str.replace(".", "").replace(",", "."))
                        else:
                            # Apenas vírgula: "2000,50" -> troca vírgula por ponto
                            custo = float(custo_str.replace(",", "."))
                    else:
                        # Apenas ponto: "2000" ou "2.000" (milhar)
                        if "." in custo_str and len(custo_str.split(".")[1]) > 2:
                            # Provavelmente milhar: "2.000" -> remove ponto
                            custo = float(custo_str.replace(".", ""))
                        else:
                            custo = float(custo_str)
                    grafo.adicionar_aresta(partes[0], partes[1], custo)
                st.session_state["grafo"] = grafo
                st.session_state["servico"] = ServicoRede(grafo)
                st.toast("Rede personalizada montada com sucesso", icon="✅")
            except ValueError as erro:
                st.sidebar.error(f"Não foi possível montar a rede: {erro}")

    # Toggle modo apresentação
    st.sidebar.divider()
    modo_apresentacao = st.sidebar.toggle(
        "🖥️ Modo Apresentação (projetor)",
        value=st.session_state.get("modo_apresentacao", False),
        help="Remove a barra lateral, aumenta fontes e figuras para projetor",
    )
    st.session_state["modo_apresentacao"] = modo_apresentacao
    return modo_apresentacao

# ────────────────────────────── PÁGINA: REDE & AGM
def pagina_rede_agm(modo_apresentacao: bool):
    from src.servicos.relatorio import gerar_relatorio_otimizacao

    st.title("⚡ GridPower — Árvore Geradora Mínima")
    st.caption("Prim (heap)  ×  Kruskal (Union-Find)  |  Squad 2 · UrbanTech")

    if "servico" not in st.session_state:
        st.info("👈  Escolha uma rede no painel à esquerda para começar.")
        if not modo_apresentacao:
            st.markdown("""
            **Como usar:**
            1. Selecione **Exemplo do artigo (8 pts)** e clique *Carregar* para ver o caso pedagógico (R$ 18.500).
            2. Ou gere uma **Aleatória** com a semente desejada.
            3. Compare Prim vs Kruskal, veja as figuras, baixe o relatório.
            4. Vá na aba **Experimento** para medir tempo/memória de 10 a 1000 vértices.
            """)
        return

    grafo = st.session_state["grafo"]
    servico = st.session_state["servico"]

    total_pares = grafo.quantidade_vertices * (grafo.quantidade_vertices - 1) / 2
    densidade = grafo.quantidade_arestas / total_pares if total_pares else 0.0
    conexa, componentes = servico.verificar_conectividade()

    # KPI ROW — GRANDE
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📍  Pontos (|V|)", grafo.quantidade_vertices)
    c2.metric("🔗  Conexões (|E|)", grafo.quantidade_arestas)
    c3.metric("📊  Densidade", f"{densidade:.0%}")
    c4.metric("🌐  Conectividade", "Conexa ✅" if conexa else f"{len(componentes)} ilhas ⚠️")

    if not conexa:
        st.warning(
            "A rede está **desconectada**: não existe árvore geradora que cubra todos os pontos.  "
            "Componentes isolados: " + "  |  ".join("{" + ", ".join(sorted(c)) + "}" for c in componentes)
        )
        return

    # COMPARAÇÃO
    st.subheader("Prim  ×  Kruskal")
    comparacao = servico.comparar()

    k1, k2, k3 = st.columns(3)
    k1.metric("Custo Prim", formatar_reais(comparacao.custo_prim))
    k2.metric("Custo Kruskal", formatar_reais(comparacao.custo_kruskal))
    k3.metric("Conexões na AGM", len(comparacao.prim))

    if comparacao.custos_equivalentes:
        st.success("✅  Os dois algoritmos chegaram ao mesmo custo mínimo.")
    else:
        st.error("❌  Os custos diferem — há erro em alguma das implementações.")

    st.markdown(
        f"**Mesmas conexões:** {'✅ sim' if comparacao.mesmas_arestas else '❌ não'}  \n"
        f"**Justificativa técnica:** {comparacao.justificativa}"
    )

    # VISUALIZAÇÃO — DUAS FIGURAS LADO A LADO (GRANDES)
    st.subheader("Rede e Árvore Geradora Mínima")
    colP, colK = st.columns(2, gap="large")
    with colP:
        st.caption(f"Prim — {formatar_reais(comparacao.custo_prim)}")
        fig = _figura_rede(grafo, comparacao.prim, COR_PRIM, "Prim — árvore geradora mínima")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with colK:
        st.caption(f"Kruskal — {formatar_reais(comparacao.custo_kruskal)}")
        fig = _figura_rede(grafo, comparacao.kruskal, COR_KRUSKAL, "Kruskal — árvore geradora mínima")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.caption("Legenda: linhas **grossas coloridas** = conexões escolhidas pela AGM  •  linhas **finas tracejadas** = conexões candidatas descartadas")

    # TABELAS EXPANSÍVEIS
    with st.expander("🔍  Conexões escolhidas (detalhe)", expanded=False):
        cp, ck = st.columns(2)
        for coluna, arvore in ((cp, comparacao.prim), (ck, comparacao.kruskal)):
            with coluna:
                st.markdown(f"### {arvore.algoritmo}")
                st.dataframe(
                    [{"Origem": a.origem, "Destino": a.destino, "Custo (R$)": formatar_reais(a.custo)}
                     for a in arvore.arestas],
                    use_container_width=True, hide_index=True,
                )

    with st.expander("📋  Todas as conexões candidatas", expanded=False):
        st.dataframe(
            [{"Origem": a.origem, "Destino": a.destino,
              "Custo (R$)": formatar_reais(a.custo),
              "Na AGM (Prim)": "✅" if a.chave in comparacao.prim.pares() else "❌"}
             for a in sorted(grafo.arestas, key=lambda a: a.custo)],
            use_container_width=True, hide_index=True,
        )

    # RELATÓRIO
    st.subheader("📄  Relatório de Otimização")
    texto_relatorio = gerar_relatorio_otimizacao(grafo, comparacao)
    st.download_button(
        "⬇️  Baixar relatório (.md)",
        texto_relatorio,
        file_name="relatorio_otimizacao.md",
        mime="text/markdown",
        use_container_width=True,
    )
    st.code(texto_relatorio, language="markdown", line_numbers=False)

# ────────────────────────────── PÁGINA: EXPERIMENTO
def pagina_experimento():
    from src.servicos.experimento import executar_experimento, perfilar
    import csv
    import io

    st.title("📈  Experimento de Complexidade")
    st.caption("Tempo e memória de Prim e Kruskal em redes sintéticas conexas com |E| = 5|V|")

    if "resultados_exp" not in st.session_state:
        col_btn, col_info = st.columns([1, 3])
        with col_btn:
            if st.button("▶️  Executar experimento (10 → 1000 vértices)", type="primary", use_container_width=True):
                with st.spinner("Medindo tempo e memória… pode levar alguns segundos."):
                    st.session_state["resultados_exp"] = executar_experimento()
                st.toast("Experimento concluído!", icon="✅")
                st.rerun()
        with col_info:
            st.info(
                "O experimento mede cada algoritmo nas 5 tamanhos do DOC: **10, 50, 100, 500, 1000 vértices**.\n"
                "Redes sintéticas conexas, |E| = 5|V|, custos U[1000, 20000].  \n"
                "Tempo: mediana de 30 execuções (10 para ≥500). Memória: pico do `tracemalloc`."
            )
        return

    resultados = st.session_state["resultados_exp"]
    ns = [r["vertices"] for r in resultados]

    # TABELA DE RESULTADOS
    st.subheader("Resultados Medidos")
    st.dataframe(
        [{"|V|": r["vertices"], "|E|": r["arestas"],
          "Prim (ms)": round(r["prim_ms"], 3),
          "Kruskal (ms)": round(r["kruskal_ms"], 3),
          "Prim (KiB)": round(r["prim_kib"], 1),
          "Kruskal (KiB)": round(r["kruskal_kib"], 1),
          "Custo (R$)": formatar_reais(r["custo_prim"]),
          "Custos iguais": "✅" if r["custos_iguais"] else "❌"}
         for r in resultados],
        use_container_width=True, hide_index=True,
    )

    # GRÁFICOS LOG-LOG GRANDES
    g1, g2 = st.columns(2, gap="large")
    with g1:
        st.subheader("⏱️  Tempo de Execução")
        fig = _figura_serie(ns, [r["prim_ms"] for r in resultados],
                            [r["kruskal_ms"] for r in resultados],
                            "Tempo (ms)", "Tempo por tamanho da rede (log-log)")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with g2:
        st.subheader("💾  Pico de Memória")
        fig = _figura_serie(ns, [r["prim_kib"] for r in resultados],
                            [r["kruskal_kib"] for r in resultados],
                            "Pico de memória (KiB)", "Memória por tamanho da rede (log-log)")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # DOWNLOAD CSV
    buffer = io.StringIO()
    escritor = csv.DictWriter(buffer, fieldnames=list(resultados[0].keys()))
    escritor.writeheader()
    escritor.writerows(resultados)
    st.download_button(
        "⬇️  Baixar resultados (.csv)",
        buffer.getvalue(),
        file_name="resultados_complexidade.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # PROFILING
    with st.expander("🔬  Profiling com cProfile (n=1000)", expanded=False):
        if st.button("Gerar perfil cProfile", use_container_width=True):
            with st.spinner("Profilando Prim e Kruskal com n=1000…"):
                perfil_texto = perfilar(n=1000)
            st.code(perfil_texto, language="text", line_numbers=True)

    # INTERPRETAÇÃO
    st.subheader("📝  Interpretação")
    st.markdown("""
- **Prim e Kruskal obtiveram o mesmo custo mínimo** em todos os tamanhos testados (corretude).
- **Nas redes esparsas (|E| = 5|V|) o Kruskal foi mais rápido e usou menos memória** que o Prim.
- **Explicação plausível:** o Prim constrói a lista de adjacência (2|E| entradas) e mantém um heap;
  o Kruskal apenas ordena as arestas e mantém estruturas de tamanho |V| (Union-Find).
- **Atenção:** não se deve generalizar para redes densas (|E| ≈ |V|²), que não foram avaliadas.
""")

# ────────────────────────────── MAIN
def main():
    # Sidebar (entrada + toggle apresentação)
    modo_apresentacao = _sidebar_entrada()
    _inject_css(modo_apresentacao)

    # Botão flutuante de toggle (sempre visível, mesmo com sidebar escondida)
    _toggle_float(modo_apresentacao)

    # Abas principais
    aba1, aba2 = st.tabs(["🌐  Rede & AGM", "📈  Experimento"])

    with aba1:
        pagina_rede_agm(modo_apresentacao)

    with aba2:
        pagina_experimento()

if __name__ == "__main__":
    main()