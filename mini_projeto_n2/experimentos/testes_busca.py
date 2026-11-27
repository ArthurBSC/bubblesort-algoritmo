"""
MODULO 5 (experimento 2) - Comparacao de BFS, DFS e Dijkstra.

Parte A: os tres algoritmos sobre a rede real de setores (12 vertices),
         comparando caminho encontrado, numero de arestas e custo total.
Parte B: escalabilidade em grafos sinteticos conexos de 100 a 10.000 vertices.

Saida: relatorio/resultados_busca.csv

Executar:  python experimentos/testes_busca.py
"""

import csv
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "modulos"))

from busca_bfs import bfs                    # noqa: E402
from busca_dfs import dfs                    # noqa: E402
from dijkstra import dijkstra                # noqa: E402
from grafo import grafo_aleatorio, rede_setores  # noqa: E402

TAMANHOS = [100, 500, 1000, 5000, 10000]
SAIDA = os.path.join(os.path.dirname(__file__), "..", "relatorio", "resultados_busca.csv")


def custo_do_caminho(g, caminho):
    if not caminho or len(caminho) < 2:
        return 0
    total = 0
    for a, b in zip(caminho, caminho[1:]):
        total += min(p for v, p in g.vizinhos(a) if v == b)
    return total


def parte_a(origem="CPD", destino="SalaReunioes", verboso=True):
    g = rede_setores()
    linhas = []
    for nome, func in (("BFS", bfs), ("DFS", dfs), ("Dijkstra", dijkstra)):
        ini = time.perf_counter()
        r = func(g, origem, destino)
        tempo = time.perf_counter() - ini
        caminho = r["caminho"]
        linhas.append({
            "experimento": "rede_setores", "algoritmo": nome, "n_vertices": len(g.vertices),
            "caminho": " -> ".join(caminho), "arestas": len(caminho) - 1,
            "custo": custo_do_caminho(g, caminho), "visitados": r["visitados"],
            "operacoes": r["operacoes"], "tempo_s": round(tempo, 8),
        })
    if verboso:
        print(f"Caminho {origem} -> {destino} na rede de setores\n")
        for l in linhas:
            print(f"  {l['algoritmo']:<9} {l['caminho']}")
            print(f"  {'':<9} arestas={l['arestas']}  custo={l['custo']}  "
                  f"visitados={l['visitados']}  operacoes={l['operacoes']}\n")
    return linhas


def parte_b(verboso=True):
    linhas = []
    for n in TAMANHOS:
        g = grafo_aleatorio(n)
        origem, destino = "S0", f"S{n - 1}"
        for nome, func in (("BFS", bfs), ("DFS", dfs), ("Dijkstra", dijkstra)):
            ini = time.perf_counter()
            r = func(g, origem, destino)
            tempo = time.perf_counter() - ini
            caminho = r["caminho"]
            linhas.append({
                "experimento": "escalabilidade", "algoritmo": nome, "n_vertices": n,
                "caminho": f"{len(caminho)} vertices", "arestas": len(caminho) - 1,
                "custo": custo_do_caminho(g, caminho), "visitados": r["visitados"],
                "operacoes": r["operacoes"], "tempo_s": round(tempo, 8),
            })
            if verboso:
                print(f"V={n:>6} {nome:<9} arestas={len(caminho) - 1:>4} "
                      f"custo={custo_do_caminho(g, caminho):>6} "
                      f"visitados={r['visitados']:>6} ops={r['operacoes']:>7} "
                      f"tempo={tempo:.6f}s")
        if verboso:
            print("-" * 86)
    return linhas


def executar(verboso=True):
    linhas = parte_a(verboso=verboso) + parte_b(verboso=verboso)
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)
    if verboso:
        print(f"\nResultados gravados em {os.path.abspath(SAIDA)}")
    return linhas


if __name__ == "__main__":
    executar()
