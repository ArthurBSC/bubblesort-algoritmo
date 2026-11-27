"""
MODULO 5 - Consolidacao dos resultados: graficos e relatorio tecnico.

Executa os tres experimentos, gera os graficos comparativos em PNG e grava
o relatorio em relatorio/relatorio_tecnico.md.

Executar:  python experimentos/resultados.py
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "modulos"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt              # noqa: E402

import testes_busca                          # noqa: E402
import testes_classificacao                  # noqa: E402
import testes_ordenacao                      # noqa: E402

REL = os.path.join(os.path.dirname(__file__), "..", "relatorio")
CORES = {"Heap Sort": "#1f77b4", "Quick Sort (pivo fixo)": "#d62728",
         "Quick Sort (mediana de 3)": "#ff7f0e", "Merge Sort": "#2ca02c",
         "Bubble Sort (base N1)": "#7f7f7f"}


def grafico_ordenacao(linhas):
    """Tempo x n, um painel por cenario (escala log nos dois eixos)."""
    cenarios = ["aleatorio", "ordenado", "inverso"]
    fig, eixos = plt.subplots(1, 3, figsize=(15, 4.6), sharey=True)
    for ax, cen in zip(eixos, cenarios):
        for alg, cor in CORES.items():
            pontos = [(l["n"], l["tempo_s"]) for l in linhas
                      if l["algoritmo"] == alg and l["cenario"] == cen]
            pontos.sort()
            ax.plot([p[0] for p in pontos], [max(p[1], 1e-6) for p in pontos],
                    marker="o", label=alg, color=cor, linewidth=1.8, markersize=4)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title(f"Dados {cen}s")
        ax.set_xlabel("n (registros)")
        ax.grid(True, which="both", alpha=0.25)
    eixos[0].set_ylabel("Tempo de execucao (s)")
    eixos[0].legend(fontsize=8)
    fig.suptitle("Modulo 4 - Tempo de execucao dos algoritmos de ordenacao", fontsize=12)
    fig.tight_layout()
    destino = os.path.join(REL, "grafico_ordenacao_tempo.png")
    fig.savefig(destino, dpi=150); plt.close(fig)
    return destino


def grafico_comparacoes(linhas):
    """Comparacoes x n (aleatorio) - independe da maquina."""
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    for alg, cor in CORES.items():
        pontos = [(l["n"], l["comparacoes"]) for l in linhas
                  if l["algoritmo"] == alg and l["cenario"] == "aleatorio"]
        pontos.sort()
        ax.plot([p[0] for p in pontos], [p[1] for p in pontos],
                marker="s", label=alg, color=cor, linewidth=1.8, markersize=4)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("n (registros)"); ax.set_ylabel("Numero de comparacoes")
    ax.set_title("Comparacoes realizadas (dados aleatorios)")
    ax.grid(True, which="both", alpha=0.25); ax.legend(fontsize=8)
    fig.tight_layout()
    destino = os.path.join(REL, "grafico_ordenacao_comparacoes.png")
    fig.savefig(destino, dpi=150); plt.close(fig)
    return destino


def grafico_busca(linhas):
    """Operacoes e tempo de BFS, DFS e Dijkstra por numero de vertices."""
    dados = [l for l in linhas if l["experimento"] == "escalabilidade"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.4))
    cores = {"BFS": "#1f77b4", "DFS": "#d62728", "Dijkstra": "#2ca02c"}
    for alg, cor in cores.items():
        p = sorted([(l["n_vertices"], l["operacoes"], l["tempo_s"])
                    for l in dados if l["algoritmo"] == alg])
        ax1.plot([x[0] for x in p], [x[1] for x in p], marker="o", color=cor, label=alg)
        ax2.plot([x[0] for x in p], [max(x[2], 1e-7) for x in p], marker="o", color=cor, label=alg)
    for ax, rot in ((ax1, "Operacoes (arestas analisadas)"), (ax2, "Tempo (s)")):
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlabel("V (vertices)"); ax.set_ylabel(rot)
        ax.grid(True, which="both", alpha=0.25); ax.legend(fontsize=9)
    fig.suptitle("Modulo 3 - BFS, DFS e Dijkstra em grafos de 100 a 10.000 vertices")
    fig.tight_layout()
    destino = os.path.join(REL, "grafico_busca.png")
    fig.savefig(destino, dpi=150); plt.close(fig)
    return destino


def grafico_id3(linhas):
    """Entropia, ganho e acuracia em funcao do volume de dados."""
    dados = [l for l in linhas if isinstance(l["registros"], int)]
    xs = [l["registros"] for l in dados]
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    ax.plot(xs, [l["entropia"] for l in dados], marker="o", label="H(S) - entropia")
    ax.plot(xs, [l["ganho_estado"] for l in dados], marker="s", label="Ganho(S, Estado)")
    ax.set_xlabel("Registros usados no treino"); ax.set_ylabel("bits")
    ax.grid(alpha=0.25)
    ax2 = ax.twinx()
    ax2.plot(xs, [l["acuracia_base_completa"] * 100 for l in dados],
             marker="^", color="#2ca02c", linestyle="--", label="Acuracia (%)")
    ax2.set_ylabel("Acuracia sobre a base completa (%)"); ax2.set_ylim(80, 102)
    linhas_l, rot_l = ax.get_legend_handles_labels()
    linhas_r, rot_r = ax2.get_legend_handles_labels()
    ax.legend(linhas_l + linhas_r, rot_l + rot_r, fontsize=8, loc="center right")
    ax.set_title("Modulo 2 - Volume de dados x entropia, ganho e acuracia")
    fig.tight_layout()
    destino = os.path.join(REL, "grafico_id3.png")
    fig.savefig(destino, dpi=150); plt.close(fig)
    return destino


def tabela_md(linhas, colunas, titulos=None):
    titulos = titulos or colunas
    out = ["| " + " | ".join(titulos) + " |",
           "|" + "|".join(["---"] * len(colunas)) + "|"]
    for l in linhas:
        out.append("| " + " | ".join(str(l[c]) for c in colunas) + " |")
    return "\n".join(out)


def gerar_relatorio(ord_, bus, id3_):
    fmt = lambda x: f"{x:,}".replace(",", ".")
    por_cenario = {}
    for l in ord_:
        por_cenario.setdefault((l["n"], l["cenario"]), []).append(l)

    md = ["# Relatorio tecnico - resultados experimentais",
          "",
          "Gerado automaticamente por `experimentos/resultados.py`.",
          "",
          "## 1. Ordenacao (Modulo 4)", "",
          "Tempo em segundos, mesma massa de dados para todos os algoritmos.", "",
          tabela_md([l for l in ord_ if l["n"] == 10000],
                    ["cenario", "algoritmo", "tempo_s", "comparacoes", "movimentacoes"],
                    ["Cenario", "Algoritmo", "Tempo (s)", "Comparacoes", "Movimentacoes"]),
          "", "![Tempo](grafico_ordenacao_tempo.png)", "",
          "![Comparacoes](grafico_ordenacao_comparacoes.png)", "",
          "## 2. Busca em grafos (Modulo 3)", "",
          tabela_md([l for l in bus if l["experimento"] == "rede_setores"],
                    ["algoritmo", "caminho", "arestas", "custo", "visitados", "operacoes"],
                    ["Algoritmo", "Caminho CPD -> SalaReunioes", "Arestas", "Custo",
                     "Visitados", "Operacoes"]),
          "", "![Busca](grafico_busca.png)", "",
          "## 3. Classificacao ID3 (Modulo 2)", "",
          tabela_md(id3_, ["registros", "entropia", "ganho_estado", "nos", "folhas",
                           "profundidade", "acuracia_base_completa"],
                    ["Registros", "H(S)", "Ganho(Estado)", "Nos", "Folhas",
                     "Profundidade", "Acuracia"]),
          "", "![ID3](grafico_id3.png)", ""]

    destino = os.path.join(REL, "relatorio_tecnico.md")
    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    return destino


def main():
    os.makedirs(REL, exist_ok=True)
    print(">> Experimento 1/3: ordenacao (pode levar cerca de 30 s)")
    ord_ = testes_ordenacao.executar(verboso=False)
    print(">> Experimento 2/3: busca em grafos")
    bus = testes_busca.executar(verboso=False)
    print(">> Experimento 3/3: classificacao ID3")
    id3_ = testes_classificacao.executar(verboso=False)

    print(">> Gerando graficos")
    for g in (grafico_ordenacao(ord_), grafico_comparacoes(ord_),
              grafico_busca(bus), grafico_id3(id3_)):
        print("   " + os.path.abspath(g))
    print(">> Relatorio: " + os.path.abspath(gerar_relatorio(ord_, bus, id3_)))


if __name__ == "__main__":
    main()
