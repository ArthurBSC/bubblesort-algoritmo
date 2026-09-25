"""
Etapa 5 - Relatório de complexidade: qual estrutura de busca teve melhor desempenho?

Executa experimentos com listas de n produtos (n = 10, 100, 1.000, 10.000, 100.000)
e mede, para a Busca Linear e a Busca Binária:
  - verificações (comparações entre elementos) e custo T(n) pelo modelo da aula;
  - tempo médio real de execução.
Também mede o Bubble Sort (versão básica e otimizada) em três cenários,
porque a Busca Binária exige a lista ordenada.

Gera na pasta relatorio/:
  - relatorio_desempenho.md    (texto e tabelas para o documento)
  - relatorio_desempenho.html  (mesmo conteúdo com gráficos, para os slides)
  - buscas.csv e bubble_sort.csv (dados brutos, abrem no Excel)

Uso:
    python relatorio.py              (Bubble Sort medido até n = 1.000)
    python relatorio.py --completo   (mede também o Bubble Sort com n = 10.000; demora alguns minutos)
"""

import csv
import html
import math
import os
import platform
import random
import sys
import time
from datetime import datetime

from buscas import busca_binaria, busca_linear
from contador import Contador, ContadorNulo
from lista_ordenada import Produto
from ordenacao import bubble_sort, bubble_sort_otimizado

SEMENTE = 2026
TAMANHOS_BUSCA = [10, 100, 1_000, 10_000, 100_000]
TAMANHOS_BUBBLE = [10, 100, 1_000]
AMOSTRAS_CASO_MEDIO = 1_000
PASTA_SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "relatorio")


def fmt(x, casas=0):
    """Formata número no padrão brasileiro (1.234,5)."""
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_lista_ordenada(n):
    # códigos 10, 20, 30, ... (como nos exemplos da atividade)
    return [Produto((i + 1) * 10, f"Produto {i + 1}") for i in range(n)]


def contar(funcao, v, n, codigo):
    c = Contador()
    funcao(v, n, codigo, c)
    return c


def tempo_medio_us(funcao, v, n, codigos):
    """Tempo médio por busca, em microssegundos, sem o custo de contar operações."""
    nulo = ContadorNulo()
    inicio = time.perf_counter()
    for cod in codigos:
        funcao(v, n, cod, nulo)
    return (time.perf_counter() - inicio) / len(codigos) * 1_000_000


# ---------------------------------------------------------------------------
# Experimento 1 - Buscas
# ---------------------------------------------------------------------------
def experimento_buscas(rnd):
    resultados = []
    for n in TAMANHOS_BUSCA:
        v = gerar_lista_ordenada(n)
        codigos = [p.codigo for p in v]
        amostra = [rnd.choice(codigos) for _ in range(AMOSTRAS_CASO_MEDIO)]
        inexistente = codigos[-1] + 5  # não existe e é maior que todos: pior caso das duas

        for nome, funcao, codigo_melhor in (
            ("Linear", busca_linear, codigos[0]),                # 1º elemento
            ("Binária", busca_binaria, codigos[(n - 1) // 2]),   # elemento do meio
        ):
            melhor = contar(funcao, v, n, codigo_melhor)
            pior = contar(funcao, v, n, inexistente)
            medios = [contar(funcao, v, n, cod) for cod in amostra]

            # a linear é lenta com n grande; diminuímos o nº de buscas cronometradas
            qtd = max(20, min(2_000, 2_000_000 // n)) if nome == "Linear" else 2_000
            tempo = tempo_medio_us(funcao, v, n, [rnd.choice(codigos) for _ in range(qtd)])

            resultados.append({
                "busca": nome,
                "n": n,
                "passos_melhor": melhor.n_passos,
                "passos_medio": sum(c.n_passos for c in medios) / len(medios),
                "passos_pior": pior.n_passos,
                "comp_medio": sum(c.comp_elementos for c in medios) / len(medios),
                "custo_melhor": melhor.custo_total(),
                "custo_medio": sum(c.custo_total() for c in medios) / len(medios),
                "custo_pior": pior.custo_total(),
                "tempo_medio_us": tempo,
            })
        lin, bi = resultados[-2], resultados[-1]
        print(f"  n={n:>7}: pior caso linear={lin['passos_pior']:>7} passos | "
              f"binária={bi['passos_pior']:>3} | tempo médio {lin['tempo_medio_us']:9.2f} us x "
              f"{bi['tempo_medio_us']:.2f} us")
    return resultados


# ---------------------------------------------------------------------------
# Experimento 2 - Bubble Sort
# ---------------------------------------------------------------------------
def experimento_bubble(rnd, tamanhos):
    resultados = []
    for n in tamanhos:
        base = list(range(1, n + 1))
        aleatoria = base[:]
        rnd.shuffle(aleatoria)
        cenarios = (
            ("Melhor (já ordenada)", base),
            ("Médio (aleatória)", aleatoria),
            ("Pior (decrescente)", base[::-1]),
        )
        for cenario, codigos in cenarios:
            for versao, funcao in (("Básica", bubble_sort), ("Otimizada", bubble_sort_otimizado)):
                v = [Produto(cod, "") for cod in codigos]
                c = Contador()
                inicio = time.perf_counter()
                funcao(v, n, c)
                tempo_ms = (time.perf_counter() - inicio) * 1000
                assert all(v[i].codigo <= v[i + 1].codigo for i in range(n - 1)), "falha na ordenação"
                resultados.append({
                    "versao": versao,
                    "cenario": cenario,
                    "n": n,
                    "comparacoes": c.comp_elementos,
                    "trocas": c.trocas,
                    "custo_total": c.custo_total(),
                    "tempo_ms": tempo_ms,
                })
        print(f"  n={n:>6}: ordenado e conferido")
    return resultados


# ---------------------------------------------------------------------------
# Análise: a partir de quantas buscas vale a pena ordenar para usar a binária?
# ---------------------------------------------------------------------------
def ponto_de_equilibrio(buscas, bubble):
    """
    Se a lista chega DESORDENADA, usar a binária exige ordenar antes (custo único).
    Vale a pena quando:  custo_ordenar + m * custo_binaria  <  m * custo_linear
                   =>    m > custo_ordenar / (custo_linear - custo_binaria)
    (usando as verificações do caso médio).
    """
    linhas = []
    for n in sorted({b["n"] for b in bubble}):
        lin = next(r for r in buscas if r["busca"] == "Linear" and r["n"] == n)
        bi = next(r for r in buscas if r["busca"] == "Binária" and r["n"] == n)
        ordenar = next(r for r in bubble if r["n"] == n and r["versao"] == "Otimizada"
                       and r["cenario"].startswith("Médio"))
        ganho = lin["comp_medio"] - bi["comp_medio"]
        m = math.floor(ordenar["comparacoes"] / ganho) + 1 if ganho > 0 else None
        linhas.append({"n": n, "ordenar": ordenar["comparacoes"], "linear": lin["comp_medio"],
                       "binaria": bi["comp_medio"], "m": m})
    return linhas


# ---------------------------------------------------------------------------
# Saídas
# ---------------------------------------------------------------------------
def salvar_csv(caminho, linhas):
    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()), delimiter=";")
        w.writeheader()
        for linha in linhas:
            w.writerow({k: (fmt(val, 3) if isinstance(val, float) else val) for k, val in linha.items()})


def tabela_md(cabecalho, linhas):
    # colunas de texto alinhadas à esquerda, numéricas à direita
    texto = [any(ch.isalpha() for ch in str(x).rstrip("x")) for x in linhas[0]]
    out = ["| " + " | ".join(cabecalho) + " |",
           "|" + "|".join(":---" if t else "---:" for t in texto) + "|"]
    out += ["| " + " | ".join(str(x) for x in linha) + " |" for linha in linhas]
    return "\n".join(out)


def montar_secoes(buscas, bubble, equilibrio, completo):
    """Monta o conteúdo do relatório como lista de (titulo, paragrafos, tabela)."""
    maior_n = TAMANHOS_BUSCA[-1]
    lin_max = next(r for r in buscas if r["busca"] == "Linear" and r["n"] == maior_n)
    bi_max = next(r for r in buscas if r["busca"] == "Binária" and r["n"] == maior_n)
    razao_passos = lin_max["passos_medio"] / bi_max["passos_medio"]
    razao_tempo = lin_max["tempo_medio_us"] / bi_max["tempo_medio_us"]

    s = []
    s.append(("1. Objetivo", [
        "Identificar qual das estruturas de busca implementadas no Sistema de Estoque — "
        "Busca Linear ou Busca Binária — obteve melhor desempenho, relacionando o tamanho "
        "da entrada (n = quantidade de produtos cadastrados) com a quantidade de operações "
        "realizadas e com o tempo de execução. Como a Busca Binária só funciona em lista "
        "ordenada, também foi analisado o custo do Bubble Sort (Etapa 4).",
    ], None))

    s.append(("2. Metodologia", [
        f"Para cada n ∈ {{{', '.join(fmt(n) for n in TAMANHOS_BUSCA)}}} foi criada uma lista ordenada "
        "de produtos com códigos 10, 20, 30, ... Em cada lista foram medidos três cenários: "
        "melhor caso (Linear: 1º elemento; Binária: elemento do meio), pior caso (código inexistente, "
        f"maior que todos) e caso médio (média de {fmt(AMOSTRAS_CASO_MEDIO)} buscas por códigos "
        "existentes sorteados).",
        "Foram contados os passos de cada busca — na Busca Linear, cada elemento examinado; na Busca "
        "Binária, cada divisão da lista ao meio — que é a contagem usada nos exemplos da atividade "
        "(\"foram necessárias 6 verificações\", \"busca binária: 3 passos de comparação\"). Também foi "
        "calculado o custo T(n) pelo modelo da aula: comparação = 1, atribuição = 2, operação "
        "matemática = 3; nesse custo a Busca Binária pesa mais por passo, pois faz duas comparações "
        "(igualdade e maior/menor) e o cálculo do meio. O tempo foi medido com time.perf_counter(), "
        "sem a contagem de operações, e depende da máquina; por isso a análise principal usa a contagem.",
        f"Ambiente: Python {platform.python_version()} — {platform.system()} {platform.release()} — "
        f"semente aleatória {SEMENTE} — gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}.",
    ], None))

    s.append(("3. Funções de custo", [
        "Busca Linear — pior caso (percorre os n elementos e não encontra): "
        "1 atribuição (i = 0) + (n + 1) testes do laço + n comparações com o código + "
        "n somas + n atribuições (i = i + 1). T(n) = 2 + (n + 1) + n + 3n + 2n = 7n + 3 → O(n).",
        "Busca Binária — pior caso (k passagens pelo laço, k = ⌊log₂ n⌋ + 1): "
        "inicialização (2 atribuições + 1 subtração) = 7; por passagem: 1 teste do laço + "
        "cálculo do meio (2 operações + 1 atribuição = 8) + 2 comparações + atualização de ini/fim "
        "(1 operação + 1 atribuição = 5) = 16; mais o teste final = 1. "
        "T(k) = 16k + 8 → O(log n).",
    ], None))

    linhas = []
    for n in TAMANHOS_BUSCA:
        lin = next(r for r in buscas if r["busca"] == "Linear" and r["n"] == n)
        bi = next(r for r in buscas if r["busca"] == "Binária" and r["n"] == n)
        linhas.append([fmt(n), fmt(lin["passos_melhor"]), fmt(lin["passos_medio"], 1), fmt(lin["passos_pior"]),
                       fmt(bi["passos_melhor"]), fmt(bi["passos_medio"], 1), fmt(bi["passos_pior"])])
    s.append(("4. Resultados — passos de cada busca", [
        "A Busca Linear cresce na mesma proporção de n: multiplicar n por 10 multiplica os passos "
        "por 10, porque no pior caso ela examina os n elementos. A Busca Binária cresce muito devagar: "
        "multiplicar n por 10 acrescenta só cerca de 3 passos (log₂ 10 ≈ 3,3), porque cada passo "
        "descarta metade do que restou.",
    ], (["n", "Linear melhor", "Linear médio", "Linear pior", "Binária melhor", "Binária médio",
         "Binária pior"], linhas)))

    linhas = []
    for n in TAMANHOS_BUSCA:
        lin = next(r for r in buscas if r["busca"] == "Linear" and r["n"] == n)
        bi = next(r for r in buscas if r["busca"] == "Binária" and r["n"] == n)
        linhas.append([fmt(n), fmt(lin["custo_pior"]), fmt(7 * n + 3), fmt(bi["custo_pior"]),
                       fmt(16 * (math.floor(math.log2(n)) + 1) + 8)])
    s.append(("5. Resultados — custo T(n) no pior caso", [
        "Os valores medidos pelo contador coincidem com as fórmulas T(n) = 7n + 3 (Linear) e "
        "T(k) = 16k + 8 (Binária), onde k é o número de passos da tabela anterior, "
        "k = ⌊log₂ n⌋ + 1. Isso confirma o modelo matemático construído na seção 3.",
    ], (["n", "Linear medido", "Linear 7n+3", "Binária medido", "Binária 16k+8"], linhas)))

    linhas = []
    for n in TAMANHOS_BUSCA:
        lin = next(r for r in buscas if r["busca"] == "Linear" and r["n"] == n)
        bi = next(r for r in buscas if r["busca"] == "Binária" and r["n"] == n)
        linhas.append([fmt(n), fmt(lin["tempo_medio_us"], 2), fmt(bi["tempo_medio_us"], 2),
                       fmt(lin["tempo_medio_us"] / bi["tempo_medio_us"], 1) + "x"])
    s.append(("6. Resultados — tempo médio real por busca (µs)", [
        "Com poucos elementos a diferença é pequena, pois a Linear faz menos trabalho por passo. "
        "Conforme n cresce, o tempo da Linear sobe proporcionalmente (×10 a cada ×10 em n) e o da "
        "Binária aumenta só um pouco a cada ×10 em n.",
    ], (["n", "Linear (µs)", "Binária (µs)", "Binária mais rápida"], linhas)))

    linhas = []
    for r in bubble:
        linhas.append([r["versao"], r["cenario"], fmt(r["n"]), fmt(r["comparacoes"]), fmt(r["trocas"]),
                       fmt(r["custo_total"]), fmt(r["tempo_ms"], 2)])
    obs_completo = "" if completo else (
        " Para n = 10.000, pelas fórmulas, a versão básica faria (n − 1)² = 99.980.001 comparações e "
        "a otimizada no pior caso n(n − 1)/2 = 49.995.000 (rode com --completo para medir).")
    s.append(("7. Bubble Sort (Etapa 4) — custo de ordenar", [
        "Versão básica (slides, Exercício 5): sempre (n − 1) passadas completas → (n − 1)² comparações "
        "em qualquer cenário, O(n²). Versão otimizada (Exercício 6): diminui o fim a cada passada e "
        "para quando uma passada não faz trocas → melhor caso n − 1 comparações, O(n); pior caso "
        "n(n − 1)/2 comparações e trocas, O(n²)." + obs_completo,
    ], (["Versão", "Cenário", "n", "Comparações", "Trocas", "Custo T(n)", "Tempo (ms)"], linhas)))

    linhas = [[fmt(e["n"]), fmt(e["ordenar"]), fmt(e["linear"], 1), fmt(e["binaria"], 1),
               fmt(e["m"]) if e["m"] else "—"] for e in equilibrio]
    s.append(("8. Vale a pena ordenar para usar a Busca Binária?", [
        "Se a lista chegar desordenada, a Binária exige ordenar antes. Ordenar é um custo único; "
        "cada busca depois economiza (comparações da Linear − comparações da Binária). "
        "O número mínimo de buscas m para compensar é: m > custo de ordenar ÷ economia por busca. "
        "No Sistema de Estoque isso é ainda mais favorável, pois a Inserção Ordenada (Etapa 3) "
        "mantém a lista sempre ordenada e o Bubble Sort só é necessário uma vez, ao importar "
        "dados desordenados.",
    ], (["n", "Comparações p/ ordenar (Bubble otimizado, médio)", "Linear: comparações (médio)",
         "Binária: comparações (médio)", "Buscas para compensar"], linhas)))

    s.append(("9. Conclusão", [
        f"A Busca Binária obteve o melhor desempenho. Com n = {fmt(maior_n)} produtos, ela precisou em "
        f"média de {fmt(bi_max['passos_medio'], 1)} passos contra {fmt(lin_max['passos_medio'], 1)} da "
        f"Linear (≈ {fmt(razao_passos, 0)} vezes menos) e foi ≈ {fmt(razao_tempo, 0)} vezes mais rápida "
        f"no tempo medido. No pior caso a Linear precisou examinar os {fmt(lin_max['passos_pior'])} "
        f"elementos e a Binária resolveu em apenas {fmt(bi_max['passos_pior'])} passos.",
        "Isso acontece porque a Busca Linear é O(n): quando a quantidade de produtos aumenta, o "
        "trabalho cresce na mesma proporção. Já a Busca Binária é O(log n): a cada passo ela descarta "
        "metade dos elementos restantes, então dobrar a quantidade de produtos acrescenta apenas uma "
        "passagem pelo laço.",
        "A condição para usar a Binária é a lista estar ordenada. Ordenar com Bubble Sort custa O(n²) "
        "e, pela seção 8, só se paga depois de aproximadamente n buscas (≈ n²/2 comparações para ordenar "
        "÷ ≈ n/2 economizadas por busca). Por isso o projeto mantém a lista sempre ordenada com a "
        "Inserção Ordenada (Etapa 3): o Bubble Sort é usado apenas uma vez, ao carregar dados "
        "desordenados, e a partir daí todas as buscas aproveitam o O(log n). A Busca Linear só é "
        "preferível quando a lista está desordenada e serão feitas poucas buscas (menos que n).",
    ], None))
    return s


def gerar_markdown(secoes):
    partes = ["# Relatório de Complexidade — Busca Linear x Busca Binária",
              "Sistema de Estoque — Complexidade de Algoritmos — Etapa 5\n"]
    for titulo, paragrafos, tabela in secoes:
        partes.append(f"## {titulo}\n")
        partes += [p + "\n" for p in paragrafos]
        if tabela:
            partes.append(tabela_md(*tabela) + "\n")
    return "\n".join(partes)


# ---------------------------- HTML com gráficos ----------------------------
def grafico_svg(titulo, series, eixo_y, log_y=True):
    """Gráfico de linhas em SVG puro (eixo x em escala log de n)."""
    L, T, W, H = 70, 40, 560, 260
    xs = sorted({x for _, pts, _ in series for x, _ in pts})
    ys = [y for _, pts, _ in series for _, y in pts if y > 0]
    xmin, xmax = math.log10(min(xs)), math.log10(max(xs))
    if log_y:
        ymin, ymax = math.floor(math.log10(min(ys))), math.ceil(math.log10(max(ys)))
        ty = lambda y: math.log10(max(y, 10 ** ymin))
    else:
        ymin, ymax = 0, max(ys) * 1.1
        ty = lambda y: y
    px = lambda x: L + (math.log10(x) - xmin) / (xmax - xmin) * W
    py = lambda y: T + H - (ty(y) - ymin) / ((ymax - ymin) or 1) * H

    out = [f'<svg viewBox="0 0 {L + W + 30} {T + H + 70}" role="img" aria-label="{html.escape(titulo)}">',
           f'<text x="{L}" y="22" class="t">{html.escape(titulo)}</text>']
    ticks = range(ymin, ymax + 1) if log_y else [ymax * i / 4 for i in range(5)]
    for t in ticks:
        yv = 10 ** t if log_y else t
        y = py(yv)
        out.append(f'<line x1="{L}" x2="{L + W}" y1="{y:.1f}" y2="{y:.1f}" class="g"/>')
        out.append(f'<text x="{L - 8}" y="{y + 4:.1f}" class="a" text-anchor="end">{fmt(yv, 0 if yv >= 1 else 2)}</text>')
    for x in xs:
        out.append(f'<text x="{px(x):.1f}" y="{T + H + 20}" class="a" text-anchor="middle">{fmt(x)}</text>')
    out.append(f'<text x="{L + W / 2}" y="{T + H + 40}" class="a" text-anchor="middle">n (quantidade de produtos)</text>')
    out.append(f'<text x="16" y="{T + H / 2}" class="a" text-anchor="middle" transform="rotate(-90 16 {T + H / 2})">{html.escape(eixo_y)}</text>')
    for i, (nome, pts, classe) in enumerate(series):
        d = " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in pts)
        out.append(f'<polyline points="{d}" class="{classe}" fill="none"/>')
        for x, y in pts:
            out.append(f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="4" class="{classe} p"><title>{nome}: n={fmt(x)} → {fmt(y, 1)}</title></circle>')
        lx = L + i * 190
        out.append(f'<line x1="{lx}" x2="{lx + 22}" y1="{T + H + 60}" y2="{T + H + 60}" class="{classe}"/>')
        out.append(f'<text x="{lx + 28}" y="{T + H + 64}" class="a">{html.escape(nome)}</text>')
    out.append("</svg>")
    return "\n".join(out)


def gerar_html(secoes, buscas):
    def serie(busca, campo):
        return [(r["n"], r[campo]) for r in buscas if r["busca"] == busca]

    g1 = grafico_svg("Passos no pior caso (escala logarítmica)",
                     [("Busca Linear", serie("Linear", "passos_pior"), "s1"),
                      ("Busca Binária", serie("Binária", "passos_pior"), "s2")], "passos")
    g2 = grafico_svg("Tempo médio por busca (escala logarítmica)",
                     [("Busca Linear", serie("Linear", "tempo_medio_us"), "s1"),
                      ("Busca Binária", serie("Binária", "tempo_medio_us"), "s2")], "microssegundos")

    corpo = []
    for titulo, paragrafos, tabela in secoes:
        corpo.append(f"<h2>{html.escape(titulo)}</h2>")
        corpo += [f"<p>{html.escape(p)}</p>" for p in paragrafos]
        if titulo.startswith("4."):
            corpo.append(f'<figure>{g1}</figure>')
        if titulo.startswith("6."):
            corpo.append(f'<figure>{g2}</figure>')
        if tabela:
            cab, linhas = tabela
            corpo.append("<div class='tw'><table><thead><tr>" + "".join(f"<th>{html.escape(c)}</th>" for c in cab)
                         + "</tr></thead><tbody>" + "".join(
                "<tr>" + "".join(f"<td>{html.escape(str(x))}</td>" for x in linha) + "</tr>" for linha in linhas)
                         + "</tbody></table></div>")

    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Relatório de Buscas</title>
<style>
:root {{ --bg:#fbfbf9; --fg:#1f2328; --muted:#5f6670; --line:#d9dcd6; --c1:#c2410c; --c2:#1d4ed8; --card:#ffffff; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#16181c; --fg:#e8e9eb; --muted:#9aa1ab; --line:#33373e; --c1:#fb923c; --c2:#7aa2ff; --card:#1d2025; }} }}
body {{ background:var(--bg); color:var(--fg); font:16px/1.6 system-ui, "Segoe UI", sans-serif; margin:0; padding:24px 16px; }}
main {{ max-width:860px; margin:0 auto; }}
h1 {{ font-size:1.6rem; margin:0 0 4px; }} .sub {{ color:var(--muted); margin:0 0 24px; }}
h2 {{ font-size:1.15rem; margin:32px 0 8px; border-bottom:1px solid var(--line); padding-bottom:4px; }}
p {{ text-align:justify; }}
.tw {{ overflow-x:auto; }} table {{ border-collapse:collapse; width:100%; font-size:.9rem; font-variant-numeric:tabular-nums; background:var(--card); }}
th, td {{ border:1px solid var(--line); padding:6px 8px; text-align:right; }} th {{ background:color-mix(in srgb, var(--line) 45%, transparent); }}
td:first-child, th:first-child {{ text-align:left; }}
figure {{ margin:16px 0; background:var(--card); border:1px solid var(--line); border-radius:8px; padding:8px; }}
svg {{ width:100%; height:auto; }} .t {{ fill:var(--fg); font-weight:600; font-size:14px; }}
.a {{ fill:var(--muted); font-size:12px; }} .g {{ stroke:var(--line); }}
.s1 {{ stroke:var(--c1); stroke-width:2.5; }} .s2 {{ stroke:var(--c2); stroke-width:2.5; }}
circle.s1 {{ fill:var(--c1); }} circle.s2 {{ fill:var(--c2); }}
</style></head>
<body><main>
<h1>Relatório de Complexidade — Busca Linear x Busca Binária</h1>
<p class="sub">Sistema de Estoque · Complexidade de Algoritmos · Etapa 5</p>
{''.join(corpo)}
</main></body></html>"""


def main():
    completo = "--completo" in sys.argv
    tamanhos_bubble = TAMANHOS_BUBBLE + ([10_000] if completo else [])
    rnd = random.Random(SEMENTE)
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    print("Experimento 1: Busca Linear x Busca Binária")
    buscas = experimento_buscas(rnd)
    print("Experimento 2: Bubble Sort")
    bubble = experimento_bubble(rnd, tamanhos_bubble)
    equilibrio = ponto_de_equilibrio(buscas, bubble)

    secoes = montar_secoes(buscas, bubble, equilibrio, completo)
    salvar_csv(os.path.join(PASTA_SAIDA, "buscas.csv"), buscas)
    salvar_csv(os.path.join(PASTA_SAIDA, "bubble_sort.csv"), bubble)
    with open(os.path.join(PASTA_SAIDA, "relatorio_desempenho.md"), "w", encoding="utf-8") as f:
        f.write(gerar_markdown(secoes))
    with open(os.path.join(PASTA_SAIDA, "relatorio_desempenho.html"), "w", encoding="utf-8") as f:
        f.write(gerar_html(secoes, buscas))

    print(f"\nRelatório gerado em: {PASTA_SAIDA}")
    print("  - relatorio_desempenho.md / .html")
    print("  - buscas.csv / bubble_sort.csv")
    return PASTA_SAIDA


if __name__ == "__main__":
    main()
