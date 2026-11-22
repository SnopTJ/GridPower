# Comparação de Artigos e Apresentação vs. Projeto GridPower

## Visão Geral

Este relatório compara o artigo **Artigo_GridPower_Atualizado.docx** e a apresentação **GridPower — Apresentação.pdf** contra o projeto GridPower real, identificando concordâncias e discrepâncias.

---

## 1. Concordâncias (O que está correto)

### 1.1. Dados Experimentais (Artigo × Apresentação × Repo)

| Tamanho | Prim (ms) | Kruskal (ms) | Prim (KiB) | Kruskal (KiB) | Custo (R$) |
|---------|-----------|--------------|------------|---------------|------------|
| |V|= 10 | 0,070 | 0,040 | 3,8 | 1,8 | 16,5 |
| |V|= 50 | 0,412 | 0,307 | 16,1 | 9,8 | 54,9 |
| |V|= 100 | 0,813 | 0,565 | 37,3 | 23,3 | 2,127 |
| |V|= 500 | 3,223 | 2,348 | 357,0 | 139,1 | 1.604,9 |
| |V|= 1000 | 10,748 | 8,746 | 908,5 | 402,6 | 32.225,8 |

✅ **Todos os dados numéricos conferem** entre os três artefatos. O `docs/08_resultados.md` no repo corresponde exatemente à Tabela III do artigo e às páginas 10-11 da apresentação.

### 1.2. Estudo de Caso

- **8 pontos**, **13 conexões candidatas**, **7 na AGM**, **R$ 18.500** custo mínimo
- ✅ **Confirmado** no `docs/08_resultados.md`, na página 9 da apresentação e no estudo de caso do artigo (Seção VI.A)

### 1.3. Contagem de Testes e Cobertura

| Métrica | Apresentação | Artigo | Repo (verificado) |
|---------|-------------|--------|-------------------|
| Testes totais | 77 | "77 testes" | **77 testes** + **67 subtests** |
| Cobertura | 100% | "100% das instruções" | **100%** (430 statements) |

✅ **Apresentação e repo são precisos.** O artigo menciona 77 testes e 100% cobertura, o que confere.

### 1.4. Arquitetura e Funcionalidades

- ✅ Arquitetura em 5 camadas (Interface, Aplicação, Núcleo matemático, Estruturas de dados, Dados/E/S)
- ✅ RF01–RF10 (todos os requisitos listados tanto no artigo quanto na apresentação)
- ✅ Algoritmos: Prim (heap) e Kruskal (Union-Find com compressão de caminho + união por posto)
- ✅ Detecção de redes desconectadas (RF09)
- ✅ Geração de relatório (RF10)
- ✅ Interface: terminal (`main.py --demo`) e dashboard (Streamlit)
- ✅ 7 integrantes na equipe (Lázaro, Gabriel Geraldo, Nilton, Gabriel Bezerra, Vinícius, João Victor, Bruno)

### 1.5. Referências Cruzadas

- ✅ Apresentação página 15 e artigo referenciam `https://github.com/SnopTJ/GridPower`
- ✅ Referências [1]-[10] do artigo estão estruturadas corretamente

---

## 2. Discrepâncias Identificadas

### 2.1. URL do Repositório (Artigo × Repo Real)

| Fonte | URL |
|-------|-----|
| Artigo, Seção X / Reference [10] | `https://github.com/vinigcs/GridPower` |
| Apresentação, Página 15 | `https://github.com/SnopTJ/GridPower` |
| Git remote `origin` | `https://github.com/SnopTJ/GridPower.git` |
| Git remote `upstream` | `https://github.com/vinigcs/GridPower.git` |

**Problema:** A Reference [10] do artigo aponta para `vinigcs/GridPower`, mas o repositório ativo do projeto é `SnopTJ/GridPower`. O `upstream` ainda aponta para o antigo repositório `vinigcs`, enquanto o `origin` (remote oficial do projeto) aponta para o correto `SnopTJ/GridPower.git`.

**Correção necessária:** Atualizar Reference [10] no artigo de `https://github.com/vinigcs/GridPower` para `https://github.com/SnopTJ/GridPower`.

### 2.2. Versão do Python (Artigo × Repo Real)

| Fonte | Version |
|-------|---------|
| Artigo, Seção VI.B | "Python 3.12" |
| Ambiente real | **Python 3.13.15** |

**Problema:** O artigo menciona Python 3.12, mas o ambiente de execução real é Python 3.13.15.

**Correção necessária:** Atualizar o texto da Seção VI.B de "Python 3.12" para "Python 3.13.15".

### 2.3. Placeholder de Hardware (Artigo)

| Local | Conteúdo |
|-------|----------|
| Artigo, Seção VI.B | `[descrever CPU e RAM da máquina utilizada]` |

**Problema:** O artigo contém um placeholder não preenchido: "[descrever CPU e RAM da máquina utilizada]".

**Correção necessária:** Preencher com as especificações da máquina usada nos experimentos ou remover a frase se não for crítica.

### 2.4. Formatação da Tabela III (Artigo)

**Observação:** A Tabela III no artigo tem o rótulo "TABELA IIITEMPO" — parece haver uma fusão entre o título da tabela "TABELA III" e o nome da figura "TEMPO". O texto ao redor refere-se a "Tab. III" de forma consistente, mas o rótulo visual dentro da tabela parece misturado.

**Ação recomendada:** Verificar a formatação exata da Tabela III no layout final do artigo e corrigir se houver sobreposição de rótulos.

---

## 3. Resumo Comparativo

| Aspecto | Artigo | Apresentação | Projeto Real |
|---------|--------|-------------|--------------|
| URL repositório | `vinigcs/GridPower` ❌ | `SnopTJ/GridPower` ✅ | `SnopTJ/GridPower.git` ✅ |
| Python | 3.12 ❌ | (não mencionado) | **3.13.15** ✅ |
| 77 testes / 100% cobertura | Menção ✅ | **77 testes, 100%** ✅ | **77 testes, 100%** ✅ |
| Dados experimentais | ✅ (conferem com repo) | ✅ (conferem com repo) | — |
| Estudo de caso R$ 18.500 | ✅ | ✅ | — |
| 8 pontos / 13 arestas / 7 AGM | ✅ | ✅ | — |
| RF01–RF10 | ✅ (listados) | ✅ (listados) | ✅ (implementados) |
| Placeholder [CPU/RAM] | Presente ❌ | Ausente | — |
| Formatação Tabela III | Possível problema ⚠️ | — | — |

---

## 4. Próximos Passos Recomendados

1. **Corrigir Reference [10]** no artigo: `https://github.com/vinigcs/GridPower` → `https://github.com/SnopTJ/GridPower`
2. **Atualizar versão do Python** na Seção VI.B: "Python 3.12" → "Python 3.13.15"
3. **Preencher o placeholder** "[descrever CPU e RAM da máquina utilizada]" com as especificações reais ou remover
4. **Verificar formatação** da Tabela III para garantir rótulos consistentes
5. **Considerar atualizar** o `upstream` remoto do git se ainda apuntar para `vinigcs/GridPower`

---

## 5. Conclusão

A apresentação está **100% alinhada** com o projeto GridPower real — todos os dados, contagens de testes, cobertura e arquitetura conferem perfeitamente. O artigo apresenta as maiores concordâncias com o projeto, mas requer **três correções pontuais**: a URL do repositório (Reference [10]), a versão do Python e o placeholder de hardware. Após essas correções, o artigo estará plenamente consistente com o trabalho desenvolvido.

Todos os dados experimentais (Tabela III, estudo de caso R$ 18.500, 8 pontos/13 arestas/7 AGM) e a qualidade do software (77 testes, 100% cobertura) estão corretamente documentados e confirmados em todos os três artefatos.