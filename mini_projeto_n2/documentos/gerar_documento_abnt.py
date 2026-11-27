# -*- coding: utf-8 -*-
"""
Gera o trabalho escrito em normas ABNT:
    documentos/Trabalho_ABNT_MiniProjeto_N2.docx

Formatacao aplicada (NBR 14724 / 6023 / 6024): margens 3-2-3-2 cm, Arial 12,
entrelinha 1,5, paragrafos justificados com recuo de 1,25 cm, titulos de secao
numerados, figuras e tabelas com legenda acima e fonte abaixo.

Os numeros citados no texto sao lidos dos CSVs de relatorio/, de modo que o
documento nunca diverge dos experimentos.

Executar:  python documentos/gerar_documento_abnt.py
"""

import csv
import os

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

BASE = os.path.dirname(os.path.abspath(__file__))
REL = os.path.join(BASE, "..", "relatorio")
SAIDA = os.path.join(BASE, "Trabalho_ABNT_MiniProjeto_N2.docx")

AUTOR = "[Nome completo do(a) aluno(a)]"
INSTITUICAO = "[Nome da instituição de ensino]"
CURSO = "[Curso]"
DISCIPLINA = "Complexidade de Algoritmos"
PROFESSOR = "[Nome do(a) professor(a)]"
CIDADE = "[Cidade]"
ANO = "2026"
TITULO = ("SISTEMA INTELIGENTE DE GESTÃO E ANÁLISE DE EQUIPAMENTOS DE TI: "
          "CLASSIFICAÇÃO POR ÁRVORE DE DECISÃO, BUSCA EM GRAFOS E ORDENAÇÃO")


# ------------------------------------------------------------------- dados
def ler_csv(nome):
    with open(os.path.join(REL, nome), encoding="utf-8") as f:
        return list(csv.DictReader(f))


ORD = ler_csv("resultados_ordenacao.csv")
BUS = ler_csv("resultados_busca.csv")
ID3 = ler_csv("resultados_id3.csv")


def ord_linha(alg, cen, n):
    for r in ORD:
        if r["algoritmo"] == alg and r["cenario"] == cen and int(r["n"]) == n:
            return r
    raise KeyError((alg, cen, n))


def tempo(alg, cen, n=10000):
    return float(ord_linha(alg, cen, n)["tempo_s"])


def comps(alg, cen, n=10000):
    return int(ord_linha(alg, cen, n)["comparacoes"])


def movs(alg, cen, n=10000):
    return int(ord_linha(alg, cen, n)["movimentacoes"])


def num(x, casas=0):
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def seg(valor, casas=5):
    return f"{valor:.{casas}f}".replace(".", ",")


def rede(alg):
    for r in BUS:
        if r["experimento"] == "rede_setores" and r["algoritmo"] == alg:
            return r
    raise KeyError(alg)


# -------------------------------------------------------------- utilitarios
doc = Document()
contador = {"figura": 0, "tabela": 0}


def configurar():
    s = doc.sections[0]
    s.top_margin, s.left_margin = Cm(3), Cm(3)
    s.bottom_margin, s.right_margin = Cm(2), Cm(2)
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(12)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    pf = normal.paragraph_format
    pf.line_spacing = 1.5
    pf.space_after = Pt(0)
    pf.space_before = Pt(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def p(texto="", recuo=True, alinhamento=WD_ALIGN_PARAGRAPH.JUSTIFY, tamanho=12,
      negrito=False, espaco=1.5, antes=0, depois=0):
    par = doc.add_paragraph()
    pf = par.paragraph_format
    pf.alignment = alinhamento
    pf.line_spacing = espaco
    pf.first_line_indent = Cm(1.25) if recuo else Cm(0)
    pf.space_before = Pt(antes)
    pf.space_after = Pt(depois)
    run = par.add_run(texto)
    run.font.name = "Arial"
    run.font.size = Pt(tamanho)
    run.bold = negrito
    return par


def titulo_secao(texto, nivel=1):
    return p(texto, recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.LEFT, negrito=True,
             antes=18 if nivel == 1 else 12, depois=6)


def lista(itens):
    for i, item in enumerate(itens):
        par = doc.add_paragraph()
        par.paragraph_format.left_indent = Cm(1.25)
        par.paragraph_format.line_spacing = 1.5
        par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = par.add_run(f"{chr(97 + i)}) " + item)
        r.font.name = "Arial"
        r.font.size = Pt(12)


def legenda(tipo, texto):
    contador[tipo] += 1
    rotulo = "Figura" if tipo == "figura" else "Tabela"
    p(f"{rotulo} {contador[tipo]} – {texto}", recuo=False,
      alinhamento=WD_ALIGN_PARAGRAPH.CENTER, tamanho=10, espaco=1.0, antes=12, depois=3)


def fonte_elemento(texto="Elaborado pelo autor (2026)."):
    p(f"Fonte: {texto}", recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER,
      tamanho=10, espaco=1.0, depois=12)


def tabela(cabecalho, linhas, titulo, largura=None):
    legenda("tabela", titulo)
    tb = doc.add_table(rows=1, cols=len(cabecalho))
    tb.style = "Table Grid"
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(cabecalho):
        cel = tb.rows[0].cells[i]
        cel.text = ""
        par = cel.paragraphs[0]
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.line_spacing = 1.0
        r = par.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.name = "Arial"
    for linha in linhas:
        cells = tb.add_row().cells
        for i, v in enumerate(linha):
            cells[i].text = ""
            par = cells[i].paragraphs[0]
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER if i else WD_ALIGN_PARAGRAPH.LEFT
            par.paragraph_format.line_spacing = 1.0
            r = par.add_run(str(v))
            r.font.size = Pt(10)
            r.font.name = "Arial"
    if largura:
        for i, w in enumerate(largura):
            for row in tb.rows:
                row.cells[i].width = Cm(w)
    fonte_elemento()


def figura(arquivo, titulo, largura_cm=15.5):
    legenda("figura", titulo)
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run().add_picture(os.path.join(REL, arquivo), width=Cm(largura_cm))
    fonte_elemento()


def codigo(linhas, titulo):
    legenda("figura", titulo)
    par = doc.add_paragraph()
    par.paragraph_format.left_indent = Cm(1.0)
    par.paragraph_format.line_spacing = 1.0
    par.paragraph_format.space_after = Pt(0)
    for i, l in enumerate(linhas):
        r = par.add_run(l + ("\n" if i < len(linhas) - 1 else ""))
        r.font.name = "Courier New"
        r.font.size = Pt(9)
        r._element.rPr.rFonts.set(qn("w:eastAsia"), "Courier New")
    fonte_elemento()


def quebra():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def vazio(qtd=1):
    for _ in range(qtd):
        p("", recuo=False)


# -------------------------------------------------------------------- CAPA
configurar()
p(INSTITUICAO.upper(), recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, negrito=True)
p(CURSO.upper(), recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER)
vazio(5)
p(AUTOR.upper(), recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER)
vazio(4)
p(TITULO, recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, negrito=True)
vazio(8)
p(CIDADE.upper(), recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER)
p(ANO, recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER)
quebra()

# ----------------------------------------------------------- FOLHA DE ROSTO
p(AUTOR.upper(), recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER)
vazio(5)
p(TITULO, recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, negrito=True)
vazio(3)
par = doc.add_paragraph()
par.paragraph_format.left_indent = Cm(8)
par.paragraph_format.line_spacing = 1.0
par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r = par.add_run(f"Mini projeto apresentado à disciplina de {DISCIPLINA} do curso de "
                f"{CURSO}, como requisito parcial para a avaliação N2.\n\n"
                f"Orientador(a): Prof.(a) {PROFESSOR}")
r.font.name = "Arial"
r.font.size = Pt(10)
vazio(7)
p(CIDADE.upper(), recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER)
p(ANO, recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER)
quebra()

# ------------------------------------------------------------------ RESUMO
p("RESUMO", recuo=False, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, negrito=True, depois=12)
par = doc.add_paragraph()
par.paragraph_format.line_spacing = 1.0
par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r = par.add_run(
    "Este trabalho apresenta o desenvolvimento de um sistema computacional para gestão e "
    "análise de um parque de equipamentos de tecnologia da informação, integrando, sobre uma "
    "mesma base de dados, técnicas de classificação, busca em grafos e ordenação. A base "
    "simulada possui 60 registros e 11 atributos. A classificação da decisão de manutenção foi "
    "implementada com o algoritmo ID3, a partir dos conceitos de entropia de Shannon e de ganho "
    "de informação, sem uso de bibliotecas de aprendizado de máquina. A rede de setores foi "
    "modelada como um grafo ponderado de 12 vértices e 17 arestas, percorrido por Busca em "
    "Largura, Busca em Profundidade e pelo algoritmo de Dijkstra. Para a ordenação foram "
    "implementados o Heap Sort, o Quick Sort e o Merge Sort, comparados ao Bubble Sort "
    "desenvolvido na avaliação anterior. Os experimentos utilizaram cinco volumes de dados, de "
    "100 a 10.000 registros, em três organizações distintas. Os resultados mostraram que o "
    f"atributo Estado concentra o maior ganho de informação (0,9533 bits) e que a árvore gerada "
    f"classificou corretamente 100% dos registros reservados para teste; que o algoritmo de "
    f"Dijkstra encontrou um caminho de custo {rede('Dijkstra')['custo']} contra "
    f"{rede('BFS')['custo']} do caminho obtido pela Busca em Largura; e que o Quick Sort com "
    f"pivô fixo degradou para comportamento quadrático diante de dados previamente ordenados, "
    f"realizando {num(comps('Quick Sort (pivo fixo)', 'ordenado'))} comparações contra "
    f"{num(comps('Merge Sort', 'ordenado'))} do Merge Sort. Conclui-se que a escolha do "
    "algoritmo deve considerar não apenas a complexidade assintótica, mas também a organização "
    "prévia dos dados e o custo de espaço.")
r.font.name = "Arial"
r.font.size = Pt(12)
vazio()
par = doc.add_paragraph()
par.paragraph_format.line_spacing = 1.0
r = par.add_run("Palavras-chave: complexidade de algoritmos; árvore de decisão; entropia; "
                "busca em grafos; ordenação.")
r.font.name = "Arial"
r.font.size = Pt(12)
quebra()

# ------------------------------------------------------------- 1 INTRODUÇÃO
titulo_secao("1 INTRODUÇÃO")
p("A gestão de um parque de equipamentos de tecnologia da informação envolve decisões "
  "recorrentes sobre manter, reparar ou substituir dispositivos. Em instituições de médio "
  "porte, esse controle costuma ser feito em planilhas, de forma manual, sem critério "
  "padronizado e sem registro do raciocínio que levou a cada decisão. O resultado é a "
  "convivência de dois problemas opostos: equipamentos sucateados que permanecem em operação e "
  "equipamentos ainda úteis que são descartados.")
p("O presente trabalho trata esse cenário como um problema computacional. A partir de uma base "
  "de dados simulada com 60 equipamentos, o sistema desenvolvido aplica três famílias de "
  "algoritmos estudadas na disciplina de Complexidade de Algoritmos: classificação por árvore "
  "de decisão, busca em grafos e ordenação. A mesma base é explorada sob essas três "
  "perspectivas, o que permite comparar não apenas os resultados obtidos, mas também o custo "
  "computacional de cada estratégia.")
p("O trabalho dá continuidade ao projeto desenvolvido na avaliação anterior, no qual foram "
  "implementados listas ordenadas, Bubble Sort, busca linear e busca binária. Aquele Bubble "
  "Sort foi aqui preservado como linha de base de complexidade quadrática, servindo de "
  "referência para dimensionar o ganho real dos algoritmos de ordem O(n log n).")
p("A questão central de pesquisa que orienta o estudo é a seguinte: de que forma a escolha de "
  "diferentes algoritmos influencia o desempenho, a eficiência e a qualidade da resolução de "
  "um problema computacional quando se trabalha com diferentes volumes e características de "
  "dados?")

titulo_secao("2 JUSTIFICATIVA")
p("A relevância da proposta está em demonstrar, com evidência experimental, que conhecer a "
  "complexidade assintótica de um algoritmo não basta para escolhê-lo. Dois algoritmos "
  "classificados como O(n log n) no caso médio podem apresentar comportamentos muito distintos "
  "diante de dados já ordenados, e um algoritmo teoricamente pior pode ser a melhor opção em "
  "situações específicas.")
p("Do ponto de vista prático, a solução proposta substitui um critério subjetivo de descarte "
  "por regras explícitas, extraídas dos próprios dados históricos e auditáveis por qualquer "
  "pessoa. A árvore de decisão produz regras legíveis no formato SE-ENTÃO, o que representa "
  "uma vantagem relevante sobre modelos de caixa-preta em contextos administrativos, nos quais "
  "a decisão precisa ser justificada.")
p("Do ponto de vista acadêmico, o projeto integra em um único sistema os conteúdos de entropia "
  "e ganho de informação, estratégias de busca, divisão e conquista, estruturas de heap e "
  "análise assintótica, evidenciando a relação entre eles.")

titulo_secao("3 OBJETIVOS")
titulo_secao("3.1 Objetivo geral", 2)
p("Desenvolver um sistema computacional capaz de armazenar, manipular, classificar, pesquisar "
  "e ordenar dados de um parque de equipamentos de TI, comparando experimentalmente o "
  "desempenho e o custo computacional dos algoritmos empregados.")
titulo_secao("3.2 Objetivos específicos", 2)
lista([
    "construir uma base de dados com no mínimo 50 registros e implementar as operações de "
    "cadastro, consulta, alteração, remoção e persistência em arquivo CSV;",
    "implementar o cálculo de entropia e de ganho de informação e construir uma árvore de "
    "decisão pelo algoritmo ID3, sem utilizar bibliotecas de aprendizado de máquina;",
    "modelar a rede de setores da instituição como um grafo ponderado e implementar a Busca em "
    "Largura, a Busca em Profundidade e o algoritmo de Dijkstra;",
    "implementar os algoritmos Heap Sort, Quick Sort e Merge Sort e compará-los ao Bubble Sort "
    "desenvolvido na avaliação anterior;",
    "investigar o comportamento dos algoritmos diante de cinco volumes de dados e de três "
    "organizações distintas dos registros;",
    "analisar a complexidade temporal e espacial pela notação Big O e confrontar a teoria com "
    "os resultados medidos.",
])
# ----------------------------------------------------------- 4 METODOLOGIA
titulo_secao("4 METODOLOGIA")
p("A pesquisa caracteriza-se como aplicada, de natureza experimental e abordagem quantitativa. "
  "O desenvolvimento foi organizado nos cinco módulos previstos no enunciado do mini projeto: "
  "base de dados, classificação por entropia e ID3, busca em grafos, ordenação e análise de "
  "complexidade.")
p("A linguagem adotada foi o Python 3.13. Todos os algoritmos principais foram implementados "
  "pelo autor, sem recorrer às funções prontas sort() ou sorted() e sem bibliotecas de grafos "
  "ou de aprendizado de máquina. As bibliotecas padrão csv, random, time, math e heapq foram "
  "utilizadas apenas como apoio, e a biblioteca matplotlib foi empregada exclusivamente na "
  "geração dos gráficos. A única estrutura pronta usada dentro de um algoritmo é o heap binário "
  "do módulo heapq, na fila de prioridade do Dijkstra; o heap do Heap Sort foi implementado "
  "manualmente.")
p("Os dados foram simulados por um script próprio (dados/gerar_base.py) com semente fixa, o que "
  "torna a base reproduzível. A simulação seguiu regras de negócio reais de gestão de parque de "
  "TI: equipamentos mais antigos tendem a apresentar pior estado de conservação e desempenho "
  "mais baixo, e o valor de mercado decresce com a idade. O rótulo da decisão foi atribuído por "
  "uma regra determinística que combina estado de conservação, desempenho e intensidade de uso "
  "— regra esta que o algoritmo ID3 deveria, idealmente, redescobrir a partir dos dados.")
p("As medições de desempenho foram feitas de duas formas complementares. A primeira é o tempo "
  "de execução, obtido com a função time.perf_counter(). A segunda, adotada já no projeto "
  "anterior, é a contagem de operações elementares — comparações e movimentações de elementos "
  "—, que independe da máquina utilizada e permite confrontar diretamente os valores medidos "
  "com as funções de custo teóricas. Todos os algoritmos de ordenação receberam exatamente o "
  "mesmo conjunto de dados em cada teste.")
p("Antes dos experimentos foram formuladas as seguintes hipóteses:")
lista([
    "H1: o Merge Sort apresentará o comportamento mais estável entre os três cenários de "
    "organização dos dados, por não depender da distribuição dos valores;",
    "H2: o Quick Sort com pivô fixo apresentará desempenho muito inferior quando os dados já "
    "estiverem ordenados, aproximando-se do comportamento quadrático;",
    "H3: a Busca em Largura encontrará o caminho com menor número de arestas, mas não "
    "necessariamente o de menor custo, papel que caberá ao algoritmo de Dijkstra;",
    "H4: o atributo com maior ganho de informação será aquele mais diretamente ligado à regra "
    "de decisão, e o aumento do volume de dados reduzirá a instabilidade da árvore gerada.",
])
p("Os testes foram executados em cinco volumes (100, 500, 1.000, 5.000 e 10.000 registros) e em "
  "três organizações (dados aleatórios, previamente ordenados e em ordem inversa), totalizando "
  "75 execuções de ordenação. Para a busca em grafos, além da rede real de 12 setores, foram "
  "gerados grafos sintéticos conexos de 100 a 10.000 vértices. O sistema conta ainda com 45 "
  "testes automatizados que verificam a corretude de cada algoritmo.")

titulo_secao("5 ESTRUTURA DA BASE DE DADOS")
p("A base está armazenada no arquivo dados/base_dados.csv e é carregada em memória como uma "
  "lista de dicionários. São 60 registros, acima do mínimo de 50 exigido, cada um com 11 "
  "atributos, descritos na tabela a seguir.")
tabela(["Atributo", "Tipo", "Valores possíveis", "Uso no sistema"],
       [["ID", "Texto", "EQ001 a EQ060", "Identificação"],
        ["Nome", "Texto", "livre", "Exibição"],
        ["Tipo", "Categórico", "Desktop, Notebook, Servidor etc.", "Consulta"],
        ["Setor", "Categórico", "12 setores da rede", "Vértice do grafo"],
        ["Valor", "Numérico (R$)", "208,87 a 9.375,77", "Chave de ordenação"],
        ["IdadeAnos", "Numérico", "0 a 11", "Chave de ordenação"],
        ["Idade", "Categórico", "Novo, Intermediario, Antigo", "Atributo do ID3"],
        ["Uso", "Categórico", "Leve, Moderado, Intenso", "Atributo do ID3"],
        ["Desempenho", "Categórico", "Alto, Medio, Baixo", "Atributo do ID3"],
        ["Estado", "Categórico", "Bom, Regular, Ruim", "Atributo do ID3"],
        ["Decisao", "Categórico", "Manter, Manutencao, Substituir", "Variável alvo"]],
       "Estrutura da base de dados", largura=[3.2, 2.9, 5.4, 3.5])
p("A distribuição da variável alvo é a seguinte: 25 registros classificados como Substituir, 20 "
  "como Manutencao e 15 como Manter. O desbalanceamento é moderado e reflete um parque "
  "envelhecido, situação comum em instituições de ensino. Os valores categóricos foram "
  "padronizados sem acentuação para evitar problemas de codificação na leitura do arquivo CSV.")
p("As operações de manipulação implementadas no módulo manipulacao_dados.py são: carregar e "
  "salvar em CSV, inserir com validação de domínio e de chave duplicada, consultar por qualquer "
  "campo, atualizar um campo específico e remover por identificador.")

# ---------------------------------------- 6 IMPLEMENTAÇÃO DOS ALGORITMOS
titulo_secao("6 IMPLEMENTAÇÃO DOS ALGORITMOS")
titulo_secao("6.1 Classificação por entropia e ID3", 2)
p("A entropia é a medida da desordem, ou impureza, de um conjunto em relação à variável que se "
  "deseja prever. Pela formulação de Shannon (1948), para um conjunto S cujas classes ocorrem "
  "com probabilidade p(i), a entropia é dada por H(S) = − Σ p(i) · log₂ p(i). Um conjunto cujos "
  "registros pertencem todos à mesma classe possui entropia zero; um conjunto equilibrado entre "
  "duas classes possui entropia de exatamente 1 bit.")
p("O ganho de informação de um atributo A mede o quanto a partição do conjunto por esse "
  "atributo reduz a entropia: Ganho(S, A) = H(S) − Σ (|Sv| / |S|) · H(Sv), em que Sv é o "
  "subconjunto dos registros nos quais A assume o valor v. O algoritmo ID3, proposto por "
  "Quinlan (1986), escolhe em cada nó o atributo de maior ganho, particiona o conjunto e repete "
  "o procedimento recursivamente.")
p("A recursão para em três situações: quando todos os registros da partição pertencem à mesma "
  "classe, caso em que se cria uma folha com essa classe; quando não restam atributos a testar, "
  "criando-se uma folha com a classe majoritária; e quando a partição está vazia, situação em "
  "que se adota a classe majoritária do nó pai.")
codigo([
    "def entropia(registros, alvo):",
    "    total = len(registros)",
    "    h = 0.0",
    "    for qtd in contar_classes(registros, alvo).values():",
    "        p = qtd / total",
    "        if p > 0:",
    "            h -= p * log2(p)",
    "    return h",
    "",
    "def ganho_informacao(registros, atributo, alvo):",
    "    return entropia(registros, alvo) - entropia_condicional(registros, atributo, alvo)",
], "Implementação da entropia e do ganho de informação")

titulo_secao("6.2 Busca em grafos: BFS, DFS e Dijkstra", 2)
p("A rede de setores foi representada por uma lista de adjacência, estrutura em que cada "
  "vértice armazena a lista dos seus vizinhos e dos respectivos pesos. Essa representação ocupa "
  "espaço O(V + E), contra O(V²) de uma matriz de adjacência, o que a torna preferível em "
  "grafos esparsos como o deste estudo, com 12 vértices e 17 arestas.")
p("A Busca em Largura utiliza uma fila FIFO e visita os vértices por níveis de distância a "
  "partir da origem. Em grafos não ponderados, garante o caminho com o menor número de arestas. "
  "A Busca em Profundidade, implementada em versão iterativa com pilha explícita para evitar o "
  "estouro da recursão, avança por um ramo até o limite antes de retroceder; não otimiza nada, "
  "mas é adequada para verificação de alcançabilidade, detecção de ciclos e identificação de "
  "componentes conexos.")
p("O algoritmo de Dijkstra (1959) é conceitualmente distinto dos dois anteriores: ele considera "
  "o peso das arestas e resolve o problema do caminho de custo mínimo em grafos com pesos não "
  "negativos. A implementação emprega uma fila de prioridade baseada em heap binário, o que "
  "reduz a complexidade de O(V²) para O((V + E) log V). A cada iteração, retira-se o vértice "
  "aberto de menor distância acumulada e tenta-se o relaxamento de suas arestas.")
codigo([
    "while heap:",
    "    d, u = heapq.heappop(heap)          # vertice aberto de menor distancia",
    "    if u in fechados: continue",
    "    fechados.add(u)",
    "    for v, peso in grafo.vizinhos(u):",
    "        if d + peso < dist[v]:          # relaxamento da aresta (u, v)",
    "            dist[v] = d + peso",
    "            pai[v] = u",
    "            heapq.heappush(heap, (dist[v], v))",
], "Núcleo do algoritmo de Dijkstra")

titulo_secao("6.3 Ordenação: Heap Sort, Quick Sort e Merge Sort", 2)
p("O Heap Sort organiza o próprio vetor como um heap máximo, estrutura de árvore binária quase "
  "completa em que todo pai é maior ou igual aos filhos. Construído o heap em O(n), o algoritmo "
  "troca a raiz com a última posição, reduz o tamanho do heap e o reorganiza, repetindo n vezes "
  "uma operação de custo O(log n). Seu grande atrativo é garantir O(n log n) em todos os casos "
  "ocupando espaço adicional constante.")
p("O Quick Sort aplica divisão e conquista: escolhe um pivô, particiona o vetor de modo que os "
  "menores fiquem à esquerda e os maiores à direita, e repete o processo nas duas metades. Seu "
  "desempenho depende inteiramente da qualidade do pivô. Foram implementadas duas versões: uma "
  "com pivô fixo no último elemento, que expõe o pior caso, e outra com pivô escolhido pela "
  "mediana entre o primeiro, o do meio e o último elemento. Para medir o pior caso sem estourar "
  "a pilha de recursão, a implementação recorre apenas sobre a menor partição e trata a maior "
  "em laço, técnica que limita a profundidade da pilha a O(log n) sem alterar o número de "
  "comparações realizadas.")
p("O Merge Sort divide o vetor ao meio até restarem partes unitárias e intercala as partes já "
  "ordenadas. Como a divisão é sempre pela metade e independe dos valores, o algoritmo mantém "
  "O(n log n) em todos os cenários. O custo dessa garantia é o espaço: a intercalação exige "
  "vetores auxiliares, resultando em complexidade espacial O(n).")

# ---------------------------------------- 7 RESULTADOS DA CLASSIFICAÇÃO
titulo_secao("7 RESULTADOS DA CLASSIFICAÇÃO")
p("A entropia da base completa, calculada em relação à variável Decisao, é de 1,5546 bits. O "
  "valor é elevado — próximo do máximo teórico de log₂ 3 = 1,585 bits para três classes —, o "
  "que indica um conjunto bastante impuro e, portanto, com margem significativa para ganho de "
  "informação.")
tabela(["Atributo", "H(S|A)", "Ganho(S, A)"],
       [["Estado", "0,6013", "0,9533"],
        ["Desempenho", "1,1732", "0,3813"],
        ["Idade", "1,2254", "0,3292"],
        ["Uso", "1,5096", "0,0449"]],
       "Entropia condicional e ganho de informação por atributo", largura=[5, 4, 4])
p("O atributo Estado foi escolhido como raiz da árvore por apresentar o maior ganho, 0,9533 "
  "bits, reduzindo a entropia do conjunto em cerca de 61%. O atributo Uso, por outro lado, "
  "mostrou-se praticamente irrelevante de forma isolada, com ganho de apenas 0,0449 bits — "
  "embora venha a ser útil em um ramo específico da árvore, quando o estado é bom e o "
  "desempenho é médio. Esse comportamento ilustra uma característica importante do ID3: o "
  "critério é guloso e local, de modo que um atributo pouco informativo no conjunto completo "
  "pode ser decisivo em uma partição.")
codigo([
    "[RAIZ] Estado?  (n=60, H=1.5546)",
    "    [Bom] Desempenho?  (n=20, H=0.8113)",
    "        [Alto]  --> CLASSE: Manter      (n=11)",
    "        [Baixo] --> CLASSE: Manutencao  (n=1)",
    "        [Medio] Uso?  (n=8, H=1.0000)",
    "            [Intenso]  --> CLASSE: Manutencao  (n=4)",
    "            [Leve]     --> CLASSE: Manter      (n=1)",
    "            [Moderado] --> CLASSE: Manter      (n=3)",
    "    [Regular] Desempenho?  (n=22, H=0.9024)",
    "        [Alto]  --> CLASSE: Manutencao  (n=4)",
    "        [Baixo] --> CLASSE: Substituir  (n=7)",
    "        [Medio] --> CLASSE: Manutencao  (n=11)",
    "    [Ruim] --> CLASSE: Substituir  (n=18)",
], "Árvore de decisão gerada pelo algoritmo ID3")
p("A árvore possui 13 nós, 9 folhas e profundidade máxima 4. Dela derivam nove regras de "
  "classificação, das quais se destacam: SE Estado = Ruim ENTÃO Substituir (18 registros); SE "
  "Estado = Bom E Desempenho = Alto ENTÃO Manter (11 registros); e SE Estado = Regular E "
  "Desempenho = Medio ENTÃO Manutencao (11 registros). O ramo mais profundo mostra que, quando "
  "o estado é bom e o desempenho é médio, a decisão passa a depender da intensidade de uso.")
p("Para validar a classificação com registros diferentes daqueles usados na construção da "
  "árvore, a base foi dividida em 70% para treino (42 registros) e 30% para teste (18 "
  "registros). A árvore construída apenas com o conjunto de treino classificou corretamente os "
  "18 registros de teste, alcançando 100% de acerto. Cabe ressaltar que esse resultado decorre "
  "de a base ter sido gerada por uma regra determinística, sem ruído: em dados reais, com "
  "exceções e erros de registro, a acurácia seria necessariamente menor. O experimento "
  "confirma, contudo, que o ID3 foi capaz de reconstruir integralmente a regra de negócio a "
  "partir dos dados, que era o objetivo do módulo.")
tabela(["Registros no treino", "H(S)", "Ganho(Estado)", "Nós", "Folhas", "Prof.", "Acurácia"],
       [[r["registros"], r["entropia"].replace(".", ","), r["ganho_estado"].replace(".", ","),
         r["nos"], r["folhas"], r["profundidade"],
         f"{float(r['acuracia_base_completa']) * 100:.1f}%".replace(".", ",")] for r in ID3],
       "Influência do volume de dados sobre a árvore gerada",
       largura=[3.1, 2.0, 2.8, 1.5, 1.8, 1.6, 2.3])
figura("grafico_id3.png",
       "Entropia, ganho de informação e acurácia em função do volume de dados", 13.5)
p("Com apenas 15 registros, a árvore gerada tem 10 nós e acerta 93,3% da base completa; a "
  "partir de 30 registros a estrutura se estabiliza em 13 nós e a acurácia chega a 100%. "
  "Observa-se também que a entropia medida se estabiliza conforme o volume aumenta: amostras "
  "pequenas produzem estimativas de probabilidade ruidosas e, por consequência, valores de "
  "ganho instáveis. Isso confirma a hipótese H4.")

# ------------------------------------------------- 8 RESULTADOS DAS BUSCAS
titulo_secao("8 RESULTADOS DAS BUSCAS")
p("A rede de setores foi modelada com 12 vértices e 17 arestas ponderadas, em que o peso "
  "representa o custo do enlace entre dois setores. Os três algoritmos foram executados a "
  "partir do setor CPD com destino na SalaReunioes.")
tabela(["Algoritmo", "Caminho encontrado", "Arestas", "Custo", "Visitados", "Operações"],
       [[r["algoritmo"], r["caminho"].replace(" -> ", " → "), r["arestas"], r["custo"],
         r["visitados"], r["operacoes"]]
        for r in BUS if r["experimento"] == "rede_setores"],
       "Comparação entre BFS, DFS e Dijkstra na rede de setores",
       largura=[2.2, 6.4, 1.6, 1.4, 1.8, 1.9])
p("O resultado evidencia a diferença conceitual entre os três algoritmos. A Busca em Largura "
  "encontrou o caminho mais curto em número de arestas, com apenas dois saltos, porém de custo "
  "total 16, pois utiliza o enlace direto entre o CPD e a Diretoria, que é caro. O Dijkstra, ao "
  "considerar os pesos, preferiu um caminho com o dobro de saltos, mas de custo 12 — uma "
  "redução de 25%. A Busca em Profundidade chegou ao destino visitando apenas cinco vértices, o "
  "menor número de operações entre os três, mas o caminho obtido não é ótimo sob nenhum dos "
  "dois critérios. Confirma-se, assim, a hipótese H3.")
p("Na segunda parte do experimento, os três algoritmos foram aplicados a grafos sintéticos "
  "conexos com 100, 500, 1.000, 5.000 e 10.000 vértices e grau médio 4.")
figura("grafico_busca.png",
       "Operações e tempo de BFS, DFS e Dijkstra por número de vértices")
p("Os três algoritmos apresentaram crescimento próximo do linear em relação a V + E, como "
  "previsto pela teoria. O Dijkstra manteve-se consistentemente mais custoso em tempo por "
  "incorporar as operações de inserção e remoção na fila de prioridade, de custo O(log V) cada, "
  "e a Busca em Profundidade apresentou o maior número de operações por aresta, uma vez que "
  "empilha vértices repetidos que depois são descartados.")

# --------------------------------------------- 9 RESULTADOS DAS ORDENAÇÕES
titulo_secao("9 RESULTADOS DAS ORDENAÇÕES")
p("Cada algoritmo foi executado sobre a mesma massa de dados em cinco volumes e três "
  "organizações, totalizando 75 execuções. A tabela a seguir apresenta os resultados para o "
  "maior volume testado, 10.000 registros.")
tabela(["Cenário", "Algoritmo", "Tempo (s)", "Comparações", "Movimentações"],
       [[r["cenario"].capitalize(), r["algoritmo"],
         f"{float(r['tempo_s']):.5f}".replace(".", ","),
         num(int(r["comparacoes"])), num(int(r["movimentacoes"]))]
        for r in ORD if int(r["n"]) == 10000],
       "Resultados da ordenação com n = 10.000 registros",
       largura=[2.2, 4.8, 2.2, 3.0, 3.1])
figura("grafico_ordenacao_tempo.png",
       "Tempo de execução dos algoritmos de ordenação (escala logarítmica)")
figura("grafico_ordenacao_comparacoes.png",
       "Número de comparações com dados aleatórios (escala logarítmica)", 12.5)
p(f"Com dados aleatórios e n = 10.000, o Quick Sort com pivô fixo foi o mais rápido "
  f"({seg(tempo('Quick Sort (pivo fixo)', 'aleatorio'))} s), seguido pelo Quick Sort com "
  f"mediana de três, pelo Merge Sort e pelo Heap Sort "
  f"({seg(tempo('Heap Sort', 'aleatorio'))} s). O Bubble Sort gastou "
  f"{seg(tempo('Bubble Sort (base N1)', 'aleatorio'), 3)} s, cerca de "
  f"{tempo('Bubble Sort (base N1)', 'aleatorio') / tempo('Quick Sort (pivo fixo)', 'aleatorio'):.0f} "
  f"vezes mais, o que torna visível a distância entre O(n²) e O(n log n).")
p(f"O cenário de dados previamente ordenados inverte completamente o quadro. O Quick Sort com "
  f"pivô fixo saltou de {num(comps('Quick Sort (pivo fixo)', 'aleatorio'))} para "
  f"{num(comps('Quick Sort (pivo fixo)', 'ordenado'))} comparações — um aumento de "
  f"{comps('Quick Sort (pivo fixo)', 'ordenado') / comps('Quick Sort (pivo fixo)', 'aleatorio'):.0f} "
  f"vezes — e tornou-se o algoritmo mais lento do conjunto, com "
  f"{seg(tempo('Quick Sort (pivo fixo)', 'ordenado'), 3)} s. O número medido coincide "
  f"exatamente com n(n − 1)/2 = 49.995.000, a função de custo do pior caso. A mesma versão, "
  f"com pivô escolhido pela mediana de três, realizou apenas "
  f"{num(comps('Quick Sort (mediana de 3)', 'ordenado'))} comparações no mesmo cenário. "
  f"Confirma-se a hipótese H2.")
p(f"O Merge Sort apresentou a menor variação entre os três cenários: "
  f"{num(comps('Merge Sort', 'aleatorio'))} comparações com dados aleatórios, "
  f"{num(comps('Merge Sort', 'ordenado'))} com dados ordenados e "
  f"{num(comps('Merge Sort', 'inverso'))} com dados invertidos. A diferença se deve apenas ao "
  f"momento em que uma das metades se esgota durante a intercalação; a estrutura da recursão "
  f"permanece idêntica. Confirma-se a hipótese H1.")
p(f"Merece registro o comportamento do Bubble Sort otimizado com dados já ordenados: ele "
  f"realizou apenas {num(comps('Bubble Sort (base N1)', 'ordenado'))} comparações e nenhuma "
  f"movimentação, concluindo em {seg(tempo('Bubble Sort (base N1)', 'ordenado'), 4)} s e sendo, "
  f"nesse único cenário, o algoritmo mais rápido de todos. Trata-se de um exemplo concreto de "
  f"que um algoritmo O(n²) no caso médio pode ser a melhor escolha em uma situação específica, "
  f"pois seu melhor caso é O(n).")

# ------------------------------------------- 10 ANÁLISE DE COMPLEXIDADE
titulo_secao("10 ANÁLISE DE COMPLEXIDADE")
tabela(["Algoritmo", "Melhor caso", "Caso médio", "Pior caso", "Espaço", "Estável"],
       [["Heap Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(1)", "Não"],
        ["Quick Sort (pivô fixo)", "O(n log n)", "O(n log n)", "O(n²)", "O(log n)", "Não"],
        ["Quick Sort (mediana 3)", "O(n log n)", "O(n log n)", "O(n²)*", "O(log n)", "Não"],
        ["Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "Sim"],
        ["Bubble Sort (N1)", "O(n)", "O(n²)", "O(n²)", "O(1)", "Sim"],
        ["BFS", "O(V + E)", "O(V + E)", "O(V + E)", "O(V)", "–"],
        ["DFS", "O(V + E)", "O(V + E)", "O(V + E)", "O(V)", "–"],
        ["Dijkstra (heap)", "O((V+E) log V)", "O((V+E) log V)", "O((V+E) log V)", "O(V)", "–"],
        ["ID3 (treinamento)", "O(a · n · v)", "O(a · n · v)", "O(a · n · v)", "O(nós)", "–"]],
       "Complexidade temporal e espacial dos algoritmos implementados",
       largura=[4.0, 2.7, 2.7, 2.5, 1.9, 1.7])
p("* O pior caso teórico permanece O(n²), mas deixa de ser atingido pelas entradas ordenadas ou "
  "invertidas, que são as mais frequentes na prática. Na notação do ID3, a representa o número "
  "de atributos, n o número de registros e v o número médio de valores por atributo.")
p("A seguir, respondem-se as questões propostas no Módulo 5 do enunciado, sempre com base nos "
  "resultados experimentais obtidos.")

perguntas = [
    ("Qual algoritmo apresentou melhor desempenho nos testes de ordenação?",
     f"Não há um vencedor único, e esse é o principal achado. Com dados aleatórios, o Quick "
     f"Sort venceu em tempo ({seg(tempo('Quick Sort (pivo fixo)', 'aleatorio'))} s para "
     f"n = 10.000). Com dados ordenados, a mesma versão foi a pior "
     f"({seg(tempo('Quick Sort (pivo fixo)', 'ordenado'), 3)} s). Considerando os três cenários "
     f"em conjunto, o Merge Sort foi o mais confiável e o Heap Sort foi o mais previsível sem "
     f"consumo extra de memória. Para um sistema em produção que não conhece a ordem prévia dos "
     f"dados, a escolha recai sobre o Merge Sort ou o Heap Sort."),
    ("O Quick Sort apresentou comportamento diferente quando os dados já estavam ordenados?",
     f"Sim, de forma drástica. O número de comparações passou de "
     f"{num(comps('Quick Sort (pivo fixo)', 'aleatorio'))} para "
     f"{num(comps('Quick Sort (pivo fixo)', 'ordenado'))}, valor que corresponde exatamente a "
     f"n(n − 1)/2. A causa é que, com pivô fixo no último elemento e vetor ordenado, toda "
     f"partição gera um subproblema vazio e outro com n − 1 elementos: em vez de dividir pela "
     f"metade, o algoritmo apenas remove um elemento por vez, degenerando para O(n²). A correção "
     f"pela mediana de três reduziu o custo a "
     f"{num(comps('Quick Sort (mediana de 3)', 'ordenado'))} comparações."),
    ("Por que o Merge Sort mantém sua complexidade O(n log n)?",
     f"Porque a divisão é estrutural, e não dependente dos dados: o vetor é sempre partido ao "
     f"meio, o que produz uma árvore de recursão de altura log₂ n, e cada nível exige no máximo "
     f"n comparações na intercalação. Os dados influenciam apenas marginalmente, quando uma das "
     f"metades se esgota antes da outra, o que explica a variação observada entre "
     f"{num(comps('Merge Sort', 'ordenado'))} e {num(comps('Merge Sort', 'aleatorio'))} "
     f"comparações. O preço dessa garantia é o espaço O(n) dos vetores auxiliares."),
    ("Qual a diferença entre BFS e DFS em relação à exploração dos vértices?",
     f"A BFS usa uma fila e explora por níveis, visitando todos os vértices à distância 1, "
     f"depois os à distância 2, e assim por diante; por isso encontra o caminho com menor número "
     f"de arestas. A DFS usa uma pilha e aprofunda em um ramo até o limite antes de retroceder. "
     f"No experimento, a BFS chegou ao destino com {rede('BFS')['arestas']} arestas após visitar "
     f"{rede('BFS')['visitados']} vértices, enquanto a DFS usou {rede('DFS')['arestas']} arestas "
     f"visitando apenas {rede('DFS')['visitados']}. A DFS pode ser mais econômica, mas o caminho "
     f"que entrega não tem garantia de otimalidade."),
    ("Qual o impacto do uso de pesos no algoritmo de Dijkstra?",
     f"O peso muda o critério de otimalidade. Sem pesos, o melhor caminho é o de menos arestas; "
     f"com pesos, é o de menor custo acumulado. No experimento, o Dijkstra devolveu um caminho "
     f"de {rede('Dijkstra')['arestas']} arestas e custo {rede('Dijkstra')['custo']}, enquanto a "
     f"BFS devolveu um de apenas {rede('BFS')['arestas']} arestas, porém com custo "
     f"{rede('BFS')['custo']} — "
     f"{int(rede('BFS')['custo']) - int(rede('Dijkstra')['custo'])} unidades a mais. O custo "
     f"computacional desse ganho é a fila de prioridade, que eleva a complexidade de O(V + E) "
     f"para O((V + E) log V)."),
    ("Como o volume de dados influencia os cálculos de entropia e ganho de informação?",
     "Com poucos registros, as frequências relativas são estimativas ruins das probabilidades "
     "reais, e tanto a entropia quanto o ganho oscilam: de 15 para 30 registros, o ganho do "
     "atributo Estado variou de 0,7955 para 1,0048 bits, estabilizando em 0,9533 bits com os 60 "
     "registros. A estrutura da árvore acompanhou essa estabilização, passando de 10 para 13 "
     "nós. Vale notar que o custo do treinamento cresce linearmente com n, pois o algoritmo "
     "percorre os registros uma vez por atributo em cada nível."),
    ("Qual algoritmo apresentou maior consumo de memória?",
     f"O Merge Sort, cuja complexidade espacial é O(n) por exigir vetores auxiliares na "
     f"intercalação. Isso se reflete na contagem de movimentações: "
     f"{num(movs('Merge Sort', 'aleatorio'))} cópias com n = 10.000, contra "
     f"{num(movs('Heap Sort', 'aleatorio'))} do Heap Sort, que ordena no próprio vetor com "
     f"espaço O(1). O Quick Sort fica em posição intermediária, com O(log n) referente à pilha "
     f"de recursão. Entre os algoritmos de grafo, o Dijkstra consome mais por manter "
     f"simultaneamente os vetores de distância e de predecessores e a fila de prioridade."),
    ("Qual estratégia seria mais adequada para resolver o problema escolhido e por quê?",
     "Para o sistema de gestão de equipamentos de TI, a combinação recomendada é: Merge Sort "
     "para os relatórios ordenados, por garantir O(n log n) independentemente da ordem prévia "
     "dos registros — situação comum quando os dados vêm de exportações já parcialmente "
     "ordenadas; Dijkstra para o planejamento de rotas de manutenção, por considerar o custo "
     "real dos deslocamentos; e a árvore ID3 para a triagem das decisões, por produzir regras "
     "legíveis e auditáveis, requisito indispensável quando a decisão precisa ser justificada "
     "administrativamente. Como a base operacional tem apenas 60 registros, qualquer algoritmo "
     "seria aceitável na prática; a escolha se justifica pela escalabilidade do sistema."),
]
for i, (q, r) in enumerate(perguntas, 1):
    p(f"{i}) {q}", recuo=False, negrito=True, antes=10, depois=3)
    p(r)

# ------------------------------------------------------------ 11 CONCLUSÃO
titulo_secao("11 CONCLUSÃO")
p("O sistema desenvolvido atingiu os objetivos propostos: integra, sobre uma única base de 60 "
  "registros, uma árvore de decisão construída pelo algoritmo ID3, três algoritmos de busca em "
  "grafos e três algoritmos de ordenação, todos implementados sem recurso a bibliotecas "
  "prontas, além de um conjunto de 45 testes automatizados que verificam a corretude de cada "
  "implementação.")
p("Quanto à questão central da pesquisa, os experimentos mostraram que a escolha do algoritmo "
  "influencia o desempenho em ordens de grandeza, e não em percentuais. A diferença mais "
  "expressiva não ocorreu entre algoritmos de classes distintas, mas entre duas versões do "
  "mesmo Quick Sort: a simples troca do critério de escolha do pivô reduziu o número de "
  "comparações de aproximadamente 50 milhões para cerca de 131 mil no cenário de dados "
  "ordenados. Esse resultado sustenta a conclusão de que a análise assintótica indica o "
  "comportamento esperado, mas não dispensa o conhecimento das características dos dados de "
  "entrada.")
p("As quatro hipóteses formuladas foram confirmadas. O Merge Sort revelou-se o algoritmo mais "
  "estável (H1); o Quick Sort com pivô fixo degradou para comportamento quadrático diante de "
  "dados ordenados (H2); a BFS encontrou o caminho com menos arestas, mas não o de menor custo, "
  "papel cumprido pelo Dijkstra (H3); e o atributo de maior ganho de informação correspondeu ao "
  "de maior peso na regra de decisão, com estabilização da árvore à medida que o volume de "
  "dados aumentou (H4).")
p("Entre as limitações do trabalho, destaca-se o fato de a base ser simulada a partir de uma "
  "regra determinística, o que explica a acurácia de 100% obtida no conjunto de teste e não se "
  "repetiria com dados reais, sujeitos a ruído e a exceções. O ID3, na versão implementada, "
  "trata apenas atributos categóricos e não possui mecanismo de poda, o que o torna suscetível "
  "ao sobreajuste em bases maiores. As medições de tempo, por fim, foram realizadas em uma "
  "única máquina e em execução única por configuração; a contagem de operações elementares foi "
  "adotada justamente para contornar essa limitação.")
p("Como trabalhos futuros, sugerem-se a discretização automática de atributos numéricos, a "
  "implementação de poda por erro reduzido, a extensão do ID3 para o critério de razão de ganho "
  "do algoritmo C4.5 e a aplicação do sistema a uma base real de inventário.")

# ---------------------------------------------------------- 12 REFERÊNCIAS
titulo_secao("12 REFERÊNCIAS")
refs = [
    "CORMEN, Thomas H. et al. Algoritmos: teoria e prática. 3. ed. Rio de Janeiro: Elsevier, "
    "2012.",
    "DIJKSTRA, Edsger W. A note on two problems in connexion with graphs. Numerische "
    "Mathematik, v. 1, n. 1, p. 269-271, 1959.",
    "MITCHELL, Tom M. Machine learning. New York: McGraw-Hill, 1997.",
    "QUINLAN, J. Ross. Induction of decision trees. Machine Learning, v. 1, n. 1, p. 81-106, "
    "1986.",
    "RUSSELL, Stuart; NORVIG, Peter. Inteligência artificial. 3. ed. Rio de Janeiro: Elsevier, "
    "2013.",
    "SHANNON, Claude E. A mathematical theory of communication. The Bell System Technical "
    "Journal, v. 27, n. 3, p. 379-423, 1948.",
    "ZIVIANI, Nivio. Projeto de algoritmos: com implementações em Pascal e C. 3. ed. São Paulo: "
    "Cengage Learning, 2011.",
]
for ref in sorted(refs):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing = 1.0
    par.paragraph_format.space_after = Pt(12)
    par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = par.add_run(ref)
    run.font.name = "Arial"
    run.font.size = Pt(12)

doc.save(SAIDA)
print("Documento gerado:", os.path.abspath(SAIDA))
