# -*- coding: utf-8 -*-
"""
Gera a apresentacao do mini projeto:
    documentos/Apresentacao_MiniProjeto_N2.pptx

A estrutura segue exatamente a divisao de tempo exigida no item 9 do
enunciado (15 a 20 minutos):
    3 min - apresentacao do problema e da tematica
    4 min - base de dados e classificacao por Entropia
    4 min - buscas BFS, DFS e Dijkstra
    4 min - algoritmos de ordenacao
    3 min - resultados experimentais e analise de complexidade

Executar:  python documentos/gerar_slides.py
"""

import csv
import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Cm, Pt

BASE = os.path.dirname(os.path.abspath(__file__))
REL = os.path.join(BASE, "..", "relatorio")
SAIDA = os.path.join(BASE, "Apresentacao_MiniProjeto_N2.pptx")

AUTOR = "[Nome completo do(a) aluno(a)]"
DISCIPLINA = "Complexidade de Algoritmos"
PROFESSOR = "[Nome do(a) professor(a)]"

AZUL = RGBColor(0x14, 0x3D, 0x6B)
AZUL_CLARO = RGBColor(0x2E, 0x75, 0xB6)
CINZA = RGBColor(0x44, 0x4B, 0x53)
CINZA_CLARO = RGBColor(0xF2, 0xF4, 0xF7)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
LARANJA = RGBColor(0xD9, 0x53, 0x1E)
VERDE = RGBColor(0x2C, 0x7A, 0x3F)

L, A = Cm(33.87), Cm(19.05)          # 16:9


def ler_csv(nome):
    with open(os.path.join(REL, nome), encoding="utf-8") as f:
        return list(csv.DictReader(f))


ORD = ler_csv("resultados_ordenacao.csv")
BUS = ler_csv("resultados_busca.csv")


def ord_(alg, cen, n=10000, campo="tempo_s"):
    for r in ORD:
        if r["algoritmo"] == alg and r["cenario"] == cen and int(r["n"]) == n:
            return r[campo]
    raise KeyError(alg)


def num(x):
    return f"{int(x):,}".replace(",", ".")


def seg(v, casas=5):
    return f"{float(v):.{casas}f}".replace(".", ",")


def rede(alg):
    for r in BUS:
        if r["experimento"] == "rede_setores" and r["algoritmo"] == alg:
            return r
    raise KeyError(alg)


prs = Presentation()
prs.slide_width, prs.slide_height = L, A
BRANCA = prs.slide_layouts[6]


# ------------------------------------------------------------- utilitarios
def caixa(slide, x, y, w, h, texto, tam=18, cor=CINZA, negrito=False,
          alinhamento=PP_ALIGN.LEFT, fonte="Arial", espaco=1.15):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Cm(0)
    tf.margin_top = tf.margin_bottom = Cm(0)
    par = tf.paragraphs[0]
    par.alignment = alinhamento
    par.line_spacing = espaco
    run = par.add_run()
    run.text = texto
    run.font.size = Pt(tam)
    run.font.bold = negrito
    run.font.color.rgb = cor
    run.font.name = fonte
    return tb


def retangulo(slide, x, y, w, h, cor):
    from pptx.enum.shapes import MSO_SHAPE
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = cor
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def slide_base(titulo, bloco=None):
    s = prs.slides.add_slide(BRANCA)
    retangulo(s, Cm(0), Cm(0), L, Cm(0.35), AZUL)
    caixa(s, Cm(1.6), Cm(1.1), L - Cm(3.2), Cm(1.4), titulo, 30, AZUL, True)
    if bloco:
        caixa(s, Cm(1.6), Cm(2.5), L - Cm(3.2), Cm(0.8), bloco, 13, AZUL_CLARO, True)
    return s


def bullets(slide, itens, x=Cm(1.6), y=Cm(4.0), w=None, tam=18, espacamento=Cm(0.35)):
    w = w or (L - Cm(3.2))
    tb = slide.shapes.add_textbox(x, y, w, A - y - Cm(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(itens):
        destaque = item.startswith("*")
        item = item.lstrip("*")
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.line_spacing = 1.25
        par.space_after = espacamento
        r1 = par.add_run()
        r1.text = "▪  "
        r1.font.size = Pt(tam)
        r1.font.color.rgb = AZUL_CLARO if not destaque else LARANJA
        r1.font.name = "Arial"
        r2 = par.add_run()
        r2.text = item
        r2.font.size = Pt(tam)
        r2.font.color.rgb = CINZA if not destaque else LARANJA
        r2.font.bold = destaque
        r2.font.name = "Arial"
    return tb


def tabela(slide, cabecalho, linhas, x, y, w, h, tam=13, larguras=None,
           destacar=None):
    tb = slide.shapes.add_table(len(linhas) + 1, len(cabecalho), x, y, w, h).table
    if larguras:
        for i, cm in enumerate(larguras):
            tb.columns[i].width = Cm(cm)
    for i, texto in enumerate(cabecalho):
        cel = tb.cell(0, i)
        cel.text = texto
        cel.fill.solid()
        cel.fill.fore_color.rgb = AZUL
        par = cel.text_frame.paragraphs[0]
        par.alignment = PP_ALIGN.CENTER
        par.runs[0].font.size = Pt(tam)
        par.runs[0].font.bold = True
        par.runs[0].font.color.rgb = BRANCO
        par.runs[0].font.name = "Arial"
    for j, linha in enumerate(linhas, 1):
        for i, v in enumerate(linha):
            cel = tb.cell(j, i)
            cel.text = str(v)
            cel.fill.solid()
            cel.fill.fore_color.rgb = CINZA_CLARO if j % 2 else BRANCO
            par = cel.text_frame.paragraphs[0]
            par.alignment = PP_ALIGN.CENTER if i else PP_ALIGN.LEFT
            r = par.runs[0]
            r.font.size = Pt(tam)
            r.font.name = "Arial"
            r.font.color.rgb = LARANJA if (destacar and j - 1 in destacar) else CINZA
            r.font.bold = bool(destacar and j - 1 in destacar)
    return tb


def imagem(slide, arquivo, x, y, largura):
    slide.shapes.add_picture(os.path.join(REL, arquivo), x, y, width=largura)


def monoespacado(slide, linhas, x, y, tam=12, cor=CINZA, largura=None):
    largura = largura or (L - x - Cm(1.6))
    tb = slide.shapes.add_textbox(x, y, largura, A - y - Cm(1.2))
    tf = tb.text_frame
    tf.word_wrap = False
    for i, l in enumerate(linhas):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.line_spacing = 1.0
        par.alignment = PP_ALIGN.LEFT
        r = par.add_run()
        r.text = l
        r.font.size = Pt(tam)
        r.font.name = "Consolas"
        r.font.color.rgb = cor
    return tb


def divisor(titulo, tempo, itens):
    s = prs.slides.add_slide(BRANCA)
    retangulo(s, Cm(0), Cm(0), L, A, AZUL)
    retangulo(s, Cm(2.2), Cm(6.0), Cm(1.6), Cm(0.18), BRANCO)
    caixa(s, Cm(2.2), Cm(6.8), L - Cm(4.4), Cm(2.0), titulo, 40, BRANCO, True)
    caixa(s, Cm(2.2), Cm(9.6), L - Cm(4.4), Cm(1.0), tempo, 18,
          RGBColor(0x9E, 0xC5, 0xE8), True)
    caixa(s, Cm(2.2), Cm(11.0), L - Cm(4.4), Cm(3.0),
          "   •   ".join(itens), 16, RGBColor(0xD8, 0xE4, 0xF0))
    return s


# =========================================================== 1. CAPA
s = prs.slides.add_slide(BRANCA)
retangulo(s, Cm(0), Cm(0), Cm(1.0), A, AZUL)
caixa(s, Cm(2.6), Cm(3.2), L - Cm(5.2), Cm(1.0),
      "MINI PROJETO N2  –  DESAFIO INTEGRADOR", 16, AZUL_CLARO, True)
caixa(s, Cm(2.6), Cm(4.6), L - Cm(5.2), Cm(4.0),
      "Sistema Inteligente de Gestão e Análise\nde Equipamentos de TI", 40, AZUL, True)
retangulo(s, Cm(2.6), Cm(9.4), Cm(6.0), Cm(0.12), LARANJA)
caixa(s, Cm(2.6), Cm(10.2), L - Cm(5.2), Cm(2.5),
      "Classificação por Árvore de Decisão (ID3)  •  Busca em Grafos "
      "(BFS, DFS, Dijkstra)  •  Ordenação (Heap, Quick, Merge)", 17, CINZA)
caixa(s, Cm(2.6), Cm(14.2), L - Cm(5.2), Cm(2.0),
      f"{AUTOR}\n{DISCIPLINA}  •  Prof.(a) {PROFESSOR}", 15, CINZA)

# =========================================================== 2. ROTEIRO
s = slide_base("Roteiro da apresentação")
tabela(s, ["Bloco", "Conteúdo", "Tempo"],
       [["1", "O problema e a temática escolhida", "3 min"],
        ["2", "Base de dados e classificação por Entropia e ID3", "4 min"],
        ["3", "Buscas em grafos: BFS, DFS e Dijkstra", "4 min"],
        ["4", "Ordenação: Heap Sort, Quick Sort e Merge Sort", "4 min"],
        ["5", "Resultados experimentais e análise de complexidade", "3 min"]],
       Cm(3.0), Cm(4.6), Cm(27.8), Cm(8.0), 16, [2.5, 20.3, 5.0])
caixa(s, Cm(3.0), Cm(13.6), Cm(27.8), Cm(1.5),
      "Demonstração ao vivo do sistema ao final de cada bloco.", 15, AZUL_CLARO, True)

# ====================================================== BLOCO 1 (3 min)
divisor("O problema e a temática", "BLOCO 1  –  3 minutos",
        ["Contexto", "Problema", "Proposta", "Questão de pesquisa"])

s = slide_base("O problema", "BLOCO 1 – Contextualização")
bullets(s, [
    "Instituições de médio porte controlam o parque de TI em planilhas manuais.",
    "A decisão de manter, reparar ou substituir um equipamento é subjetiva e "
    "não fica registrada.",
    "*Resultado: equipamentos sucateados continuam em uso e equipamentos úteis são "
    "descartados.",
    "Não há critério para priorizar rotas de manutenção entre os setores.",
    "Relatórios de inventário precisam ser ordenados por valor, idade ou criticidade "
    "— e a base cresce.",
], y=Cm(4.6), tam=20)

s = slide_base("A proposta", "BLOCO 1 – Temática e questão de pesquisa")
bullets(s, [
    "Um sistema que trata o mesmo conjunto de dados sob três perspectivas: "
    "classificar, buscar e ordenar.",
    "Base própria com 60 equipamentos e 11 atributos (mínimo exigido: 50).",
    "Continuidade do projeto N1: o Bubble Sort daquele trabalho virou a "
    "linha de base O(n²) desta comparação.",
], y=Cm(4.4), tam=19)
retangulo(s, Cm(1.6), Cm(11.0), L - Cm(3.2), Cm(2.6), CINZA_CLARO)
caixa(s, Cm(2.2), Cm(11.5), L - Cm(4.4), Cm(2.0),
      "Questão central: de que forma a escolha de diferentes algoritmos influencia o "
      "desempenho e a qualidade da solução diante de diferentes volumes e "
      "características de dados?", 17, AZUL, True)
caixa(s, Cm(1.6), Cm(14.2), L - Cm(3.2), Cm(2.0),
      "Hipóteses testadas:  H1 Merge Sort é o mais estável  •  H2 Quick Sort "
      "degrada com dados ordenados  •  H3 BFS ≠ Dijkstra  •  H4 mais dados, "
      "árvore mais estável", 14, CINZA)

# ====================================================== BLOCO 2 (4 min)
divisor("Base de dados e classificação", "BLOCO 2  –  4 minutos",
        ["Estrutura", "Entropia", "Ganho de informação", "Árvore ID3", "Validação"])

s = slide_base("Módulo 1 – A base de dados", "BLOCO 2 – 60 registros, 11 atributos")
tabela(s, ["Atributo", "Valores", "Papel no sistema"],
       [["Idade", "Novo / Intermediario / Antigo", "Atributo do ID3"],
        ["Uso", "Leve / Moderado / Intenso", "Atributo do ID3"],
        ["Desempenho", "Alto / Medio / Baixo", "Atributo do ID3"],
        ["Estado", "Bom / Regular / Ruim", "Atributo do ID3"],
        ["Decisao", "Manter / Manutencao / Substituir", "Variável alvo"],
        ["Valor, IdadeAnos", "numéricos", "Chaves de ordenação"],
        ["Setor", "12 setores", "Vértices do grafo"]],
       Cm(2.0), Cm(4.6), Cm(29.8), Cm(8.0), 15, [6.0, 13.0, 10.8])
caixa(s, Cm(2.0), Cm(13.8), Cm(29.8), Cm(1.5),
      "Operações: inserir, consultar, atualizar, remover, salvar e carregar CSV  "
      "—  Distribuição: 25 Substituir, 20 Manutencao, 15 Manter", 15, CINZA)

s = slide_base("Módulo 2 – Entropia", "BLOCO 2 – Quanta desordem há na base?")
retangulo(s, Cm(1.6), Cm(4.4), L - Cm(3.2), Cm(2.2), CINZA_CLARO)
caixa(s, Cm(2.2), Cm(5.0), L - Cm(4.4), Cm(1.4),
      "H(S) = − Σ p(i) · log₂ p(i)", 26, AZUL, True, PP_ALIGN.CENTER)
bullets(s, [
    "Conjunto puro (uma só classe) → H = 0.   Conjunto 50/50 → H = 1 bit.",
    "Na nossa base: Manter = 15, Manutencao = 20, Substituir = 25, em 60 registros.",
    "*H(S) = 1,5546 bits — muito perto do máximo teórico log₂3 = 1,585.",
    "Leitura: a base é bastante impura, logo há muito a ganhar escolhendo bem o "
    "primeiro atributo.",
], y=Cm(7.6), tam=19)

s = slide_base("Módulo 2 – Ganho de informação",
               "BLOCO 2 – Qual atributo pergunta primeiro?")
caixa(s, Cm(1.6), Cm(4.2), L - Cm(3.2), Cm(1.0),
      "Ganho(S, A) = H(S) − Σ (|Sv| / |S|) · H(Sv)", 20, AZUL, True)
tabela(s, ["Atributo", "H(S|A)", "Ganho(S, A)"],
       [["Estado", "0,6013", "0,9533"],
        ["Desempenho", "1,1732", "0,3813"],
        ["Idade", "1,2254", "0,3292"],
        ["Uso", "1,5096", "0,0449"]],
       Cm(4.0), Cm(6.0), Cm(25.8), Cm(5.0), 16, [10.0, 7.9, 7.9], destacar={0})
caixa(s, Cm(4.0), Cm(12.2), Cm(25.8), Cm(2.5),
      "O atributo Estado reduz a entropia em 61% — vai para a raiz.\n"
      "O atributo Uso parece inútil (0,0449 bit), mas será decisivo dentro de um ramo: "
      "o critério do ID3 é guloso e local.", 16, CINZA)

s = slide_base("Módulo 2 – A árvore ID3", "BLOCO 2 – 13 nós, 9 folhas, profundidade 4")
monoespacado(s, [
    "[RAIZ] Estado?  (n=60, H=1.5546)",
    "    [Bom] Desempenho?  (n=20, H=0.8113)",
    "        [Alto]  --> MANTER      (n=11)",
    "        [Baixo] --> MANUTENCAO  (n=1)",
    "        [Medio] Uso?  (n=8, H=1.0000)",
    "            [Intenso]  --> MANUTENCAO  (n=4)",
    "            [Leve]     --> MANTER      (n=1)",
    "            [Moderado] --> MANTER      (n=3)",
    "    [Regular] Desempenho?  (n=22, H=0.9024)",
    "        [Alto]  --> MANUTENCAO  (n=4)",
    "        [Baixo] --> SUBSTITUIR  (n=7)",
    "        [Medio] --> MANUTENCAO  (n=11)",
    "    [Ruim] --> SUBSTITUIR  (n=18)",
], Cm(1.6), Cm(4.4), 13, largura=Cm(17.5))
caixa(s, Cm(19.6), Cm(4.6), Cm(12.6), Cm(9.0),
      "Regras extraídas:\n\n"
      "SE Estado = Ruim\nENTÃO Substituir  (18)\n\n"
      "SE Estado = Bom E Desempenho = Alto\nENTÃO Manter  (11)\n\n"
      "SE Estado = Regular E Desempenho = Medio\nENTÃO Manutencao  (11)", 15, AZUL)

s = slide_base("Módulo 2 – Validação", "BLOCO 2 – Testes com registros nunca vistos")
bullets(s, [
    "Divisão 70 / 30: árvore treinada com 42 registros, testada com 18.",
    "*Acerto no conjunto de teste: 18 / 18 = 100%.",
    "Ressalva honesta: a base é simulada por regra determinística, sem ruído — "
    "em dados reais a acurácia seria menor.",
    "O que o experimento prova: o ID3 reconstruiu integralmente a regra de negócio a "
    "partir dos dados.",
    "Com 15 registros: 10 nós e 93,3% de acerto; a partir de 30 registros estabiliza "
    "em 13 nós (hipótese H4).",
], y=Cm(4.4), w=Cm(18.4), tam=17)
imagem(s, "grafico_id3.png", Cm(20.4), Cm(5.4), Cm(12.2))

# ====================================================== BLOCO 3 (4 min)
divisor("Busca em grafos", "BLOCO 3  –  4 minutos",
        ["O grafo", "BFS", "DFS", "Dijkstra", "Escalabilidade"])

s = slide_base("Módulo 3 – A rede como grafo", "BLOCO 3 – 12 vértices, 17 arestas")
bullets(s, [
    "Vértices = setores da instituição.  Arestas = enlaces de rede.  "
    "Peso = custo do enlace.",
    "Estrutura: lista de adjacência — espaço O(V + E), contra O(V²) da matriz.",
], y=Cm(4.4), tam=19)
monoespacado(s, [
    "CPD            -> Suporte(2), Administrativo(5), Laboratorio1(4), Diretoria(14)",
    "Administrativo -> CPD(5), Financeiro(2), Recepcao(3)",
    "Financeiro     -> Administrativo(2), Diretoria(3), SalaReunioes(6)",
    "Diretoria      -> CPD(14), Financeiro(3), SalaReunioes(2)",
    "...",
], Cm(1.8), Cm(8.2), 12, largura=Cm(30.0))
retangulo(s, Cm(1.6), Cm(12.0), L - Cm(3.2), Cm(2.4), CINZA_CLARO)
caixa(s, Cm(2.2), Cm(12.5), L - Cm(4.4), Cm(1.8),
      "Atenção: BFS e DFS são estratégias de exploração. Dijkstra é um algoritmo de "
      "caminho mínimo com pesos não negativos. Não são três versões da mesma coisa.",
      16, AZUL, True)

s = slide_base("Módulo 3 – Os três algoritmos no mesmo percurso",
               "BLOCO 3 – CPD → SalaReunioes")
tabela(s, ["Algoritmo", "Estrutura", "Caminho", "Arestas", "Custo", "Operações"],
       [["BFS", "Fila (FIFO)", rede("BFS")["caminho"].replace(" -> ", " → "),
         rede("BFS")["arestas"], rede("BFS")["custo"], rede("BFS")["operacoes"]],
        ["DFS", "Pilha (LIFO)", rede("DFS")["caminho"].replace(" -> ", " → "),
         rede("DFS")["arestas"], rede("DFS")["custo"], rede("DFS")["operacoes"]],
        ["Dijkstra", "Fila de prioridade",
         rede("Dijkstra")["caminho"].replace(" -> ", " → "),
         rede("Dijkstra")["arestas"], rede("Dijkstra")["custo"],
         rede("Dijkstra")["operacoes"]]],
       Cm(1.4), Cm(4.4), Cm(31.0), Cm(5.5), 13, [3.6, 5.2, 12.6, 3.0, 3.0, 3.6],
       destacar={2})
bullets(s, [
    "*BFS vence em saltos (2 arestas), mas paga custo 16 pelo enlace caro CPD→Diretoria.",
    "*Dijkstra usa 4 arestas e paga apenas 12 — 25% mais barato. Hipótese H3 confirmada.",
    "DFS chega ao destino visitando só 5 vértices, mas sem garantia nenhuma de otimalidade.",
], y=Cm(10.6), tam=17)

s = slide_base("Módulo 3 – Escalabilidade", "BLOCO 3 – Grafos de 100 a 10.000 vértices")
imagem(s, "grafico_busca.png", Cm(3.4), Cm(4.4), Cm(27.0))
caixa(s, Cm(3.4), Cm(14.4), Cm(27.0), Cm(2.0),
      "Os três crescem linearmente com V + E. O Dijkstra é consistentemente mais caro "
      "em tempo: paga O(log V) por operação na fila de prioridade — esse é o preço "
      "de considerar os pesos.", 16, CINZA)

# ====================================================== BLOCO 4 (4 min)
divisor("Ordenação", "BLOCO 4  –  4 minutos",
        ["Heap Sort", "Quick Sort", "Merge Sort", "O pior caso"])

s = slide_base("Módulo 4 – Os três algoritmos", "BLOCO 4 – Como cada um funciona")
tabela(s, ["Algoritmo", "Ideia central", "Tempo", "Espaço", "Estável"],
       [["Heap Sort", "Heap máximo no próprio vetor; extrai a raiz n vezes",
         "O(n log n) sempre", "O(1)", "Não"],
        ["Quick Sort", "Divisão e conquista com pivô e particionamento",
         "O(n log n) médio / O(n²) pior", "O(log n)", "Não"],
        ["Merge Sort", "Divide ao meio e intercala as metades ordenadas",
         "O(n log n) sempre", "O(n)", "Sim"],
        ["Bubble Sort (N1)", "Trocas sucessivas entre vizinhos",
         "O(n) melhor / O(n²) pior", "O(1)", "Sim"]],
       Cm(1.4), Cm(4.6), Cm(31.0), Cm(8.0), 14, [5.4, 12.0, 7.6, 3.0, 3.0])
caixa(s, Cm(1.4), Cm(13.8), Cm(31.0), Cm(1.5),
      "Todos implementados do zero, com contagem de comparações e movimentações — "
      "métrica que independe da máquina.", 15, AZUL_CLARO, True)

s = slide_base("Módulo 4 – Resultados com n = 10.000",
               "BLOCO 4 – Mesma massa de dados para todos")
tabela(s, ["Algoritmo", "Aleatório (s)", "Ordenado (s)", "Inverso (s)",
           "Comparações (aleatório)"],
       [["Heap Sort", seg(ord_("Heap Sort", "aleatorio")),
         seg(ord_("Heap Sort", "ordenado")), seg(ord_("Heap Sort", "inverso")),
         num(ord_("Heap Sort", "aleatorio", campo="comparacoes"))],
        ["Quick Sort (pivô fixo)", seg(ord_("Quick Sort (pivo fixo)", "aleatorio")),
         seg(ord_("Quick Sort (pivo fixo)", "ordenado")),
         seg(ord_("Quick Sort (pivo fixo)", "inverso")),
         num(ord_("Quick Sort (pivo fixo)", "aleatorio", campo="comparacoes"))],
        ["Quick Sort (mediana 3)", seg(ord_("Quick Sort (mediana de 3)", "aleatorio")),
         seg(ord_("Quick Sort (mediana de 3)", "ordenado")),
         seg(ord_("Quick Sort (mediana de 3)", "inverso")),
         num(ord_("Quick Sort (mediana de 3)", "aleatorio", campo="comparacoes"))],
        ["Merge Sort", seg(ord_("Merge Sort", "aleatorio")),
         seg(ord_("Merge Sort", "ordenado")), seg(ord_("Merge Sort", "inverso")),
         num(ord_("Merge Sort", "aleatorio", campo="comparacoes"))],
        ["Bubble Sort (N1)", seg(ord_("Bubble Sort (base N1)", "aleatorio")),
         seg(ord_("Bubble Sort (base N1)", "ordenado")),
         seg(ord_("Bubble Sort (base N1)", "inverso")),
         num(ord_("Bubble Sort (base N1)", "aleatorio", campo="comparacoes"))]],
       Cm(1.4), Cm(4.6), Cm(31.0), Cm(7.0), 14, [7.4, 5.9, 5.9, 5.9, 5.9],
       destacar={1})
bullets(s, [
    "*Com dados já ordenados o Quick Sort de pivô fixo vira o pior de todos: "
    f"{seg(ord_('Quick Sort (pivo fixo)', 'ordenado'), 3)} s.",
    f"O Bubble Sort, nesse mesmo cenário, é o mais rápido "
    f"({seg(ord_('Bubble Sort (base N1)', 'ordenado'), 5)} s): o melhor caso dele é O(n).",
], y=Cm(12.4), tam=17)

s = slide_base("Módulo 4 – O pior caso do Quick Sort",
               "BLOCO 4 – Por que o pivô importa tanto")
imagem(s, "grafico_ordenacao_tempo.png", Cm(1.6), Cm(4.4), Cm(30.6))
retangulo(s, Cm(1.6), Cm(12.6), L - Cm(3.2), Cm(4.2), CINZA_CLARO)
caixa(s, Cm(2.2), Cm(13.1), L - Cm(4.4), Cm(3.4),
      f"Pivô fixo + vetor ordenado: toda partição gera um lado vazio e outro com n−1 "
      f"elementos. Em vez de dividir pela metade, remove um por vez → O(n²).\n"
      f"{num(ord_('Quick Sort (pivo fixo)', 'ordenado', campo='comparacoes'))} comparações "
      f"= exatamente n(n−1)/2.   Com mediana de três: apenas "
      f"{num(ord_('Quick Sort (mediana de 3)', 'ordenado', campo='comparacoes'))}. "
      f"Mesmo algoritmo, 380× menos trabalho.", 16, AZUL, True)

# ====================================================== BLOCO 5 (3 min)
divisor("Resultados e complexidade", "BLOCO 5  –  3 minutos",
        ["Big O", "Hipóteses", "Conclusão"])

s = slide_base("Módulo 5 – Análise de complexidade", "BLOCO 5 – Notação Big O")
tabela(s, ["Algoritmo", "Melhor", "Médio", "Pior", "Espaço"],
       [["Heap Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(1)"],
        ["Quick Sort (pivô fixo)", "O(n log n)", "O(n log n)", "O(n²)", "O(log n)"],
        ["Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)"],
        ["Bubble Sort (N1)", "O(n)", "O(n²)", "O(n²)", "O(1)"],
        ["BFS / DFS", "O(V + E)", "O(V + E)", "O(V + E)", "O(V)"],
        ["Dijkstra (heap)", "O((V+E) log V)", "O((V+E) log V)", "O((V+E) log V)", "O(V)"],
        ["ID3 (treino)", "O(a · n · v)", "O(a · n · v)", "O(a · n · v)", "O(nós)"]],
       Cm(1.8), Cm(4.6), Cm(30.2), Cm(9.0), 14, [7.4, 5.7, 5.7, 5.7, 5.7])
caixa(s, Cm(1.8), Cm(14.4), Cm(30.2), Cm(1.5),
      "Maior consumo de memória: Merge Sort — "
      f"{num(ord_('Merge Sort', 'aleatorio', campo='movimentacoes'))} movimentações "
      f"contra {num(ord_('Heap Sort', 'aleatorio', campo='movimentacoes'))} do Heap Sort.",
      15, CINZA)

s = slide_base("As quatro hipóteses", "BLOCO 5 – Confirmadas pelos experimentos")
tabela(s, ["Hipótese", "Veredito", "Evidência"],
       [["H1 – Merge Sort é o mais estável", "Confirmada",
         f"{num(ord_('Merge Sort', 'ordenado', campo='comparacoes'))} a "
         f"{num(ord_('Merge Sort', 'aleatorio', campo='comparacoes'))} comparações nos 3 cenários"],
        ["H2 – Quick Sort degrada ordenado", "Confirmada",
         f"{num(ord_('Quick Sort (pivo fixo)', 'ordenado', campo='comparacoes'))} "
         f"comparações = n(n−1)/2"],
        ["H3 – BFS ≠ Dijkstra", "Confirmada",
         f"BFS: 2 arestas, custo {rede('BFS')['custo']}  |  "
         f"Dijkstra: 4 arestas, custo {rede('Dijkstra')['custo']}"],
        ["H4 – Mais dados, árvore estável", "Confirmada",
         "10 nós e 93,3% com 15 registros → 13 nós e 100% a partir de 30"]],
       Cm(1.6), Cm(4.8), Cm(30.6), Cm(8.0), 14, [9.0, 4.6, 17.0])

s = slide_base("Conclusão", "BLOCO 5 – O que ficou demonstrado")
bullets(s, [
    "*A diferença mais expressiva não foi entre algoritmos diferentes, e sim entre duas "
    "versões do mesmo Quick Sort.",
    "Complexidade assintótica indica o comportamento esperado, mas não dispensa conhecer "
    "a organização prévia dos dados.",
    "Para o sistema proposto: Merge Sort nos relatórios, Dijkstra nas rotas de manutenção "
    "e ID3 na triagem — por produzir regras auditáveis.",
    "Limitações: base simulada sem ruído, ID3 sem poda e apenas para atributos categóricos.",
    "Próximos passos: discretizar atributos numéricos, poda por erro reduzido e "
    "critério de razão de ganho (C4.5).",
], y=Cm(4.6), tam=18)

s = prs.slides.add_slide(BRANCA)
retangulo(s, Cm(0), Cm(0), L, A, AZUL)
caixa(s, Cm(3.0), Cm(6.4), L - Cm(6.0), Cm(2.5), "Demonstração do sistema", 40,
      BRANCO, True, PP_ALIGN.CENTER)
caixa(s, Cm(3.0), Cm(9.6), L - Cm(6.0), Cm(3.0),
      "python main.py   —   menu com os cinco módulos\n"
      "python testes.py   —   45 testes automatizados\n"
      "python experimentos/resultados.py   —   refaz todos os experimentos",
      19, RGBColor(0xD8, 0xE4, 0xF0), False, PP_ALIGN.CENTER)
caixa(s, Cm(3.0), Cm(14.6), L - Cm(6.0), Cm(1.5), "Obrigado! Perguntas?", 22,
      RGBColor(0x9E, 0xC5, 0xE8), True, PP_ALIGN.CENTER)

prs.save(SAIDA)
print(f"Apresentacao gerada: {os.path.abspath(SAIDA)}  ({len(prs.slides.__iter__.__self__._sldIdLst)} slides)")
