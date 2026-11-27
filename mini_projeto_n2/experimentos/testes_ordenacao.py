"""
MODULO 5 (experimento 1) - Comparacao dos algoritmos de ordenacao.

Executa Heap Sort, Quick Sort (pivo fixo), Quick Sort (mediana de tres),
Merge Sort e Bubble Sort (linha de base do N1) sobre os MESMOS conjuntos
de dados, em 5 volumes e 3 organizacoes diferentes.

Saida: relatorio/resultados_ordenacao.csv

Executar:  python experimentos/testes_ordenacao.py
"""

import csv
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "modulos"))

from bubble_sort import bubble_sort          # noqa: E402
from heap_sort import heap_sort              # noqa: E402
from merge_sort import merge_sort            # noqa: E402
from quick_sort import quick_sort, quick_sort_mediana3  # noqa: E402

TAMANHOS = [100, 500, 1000, 5000, 10000]
ALGORITMOS = [
    ("Heap Sort", heap_sort),
    ("Quick Sort (pivo fixo)", quick_sort),
    ("Quick Sort (mediana de 3)", quick_sort_mediana3),
    ("Merge Sort", merge_sort),
    ("Bubble Sort (base N1)", bubble_sort),
]
SAIDA = os.path.join(os.path.dirname(__file__), "..", "relatorio", "resultados_ordenacao.csv")


def conjuntos(n, semente=42):
    """Mesmos dados para todos os algoritmos: aleatorio, ordenado e inverso."""
    rnd = random.Random(semente)
    aleatorio = [rnd.randint(1, 10 ** 6) for _ in range(n)]
    return {
        "aleatorio": aleatorio,
        "ordenado": sorted(aleatorio),
        "inverso": sorted(aleatorio, reverse=True),
    }


def executar(verboso=True):
    linhas = []
    for n in TAMANHOS:
        dados = conjuntos(n)
        for cenario, base in dados.items():
            esperado = sorted(base)
            for nome, func in ALGORITMOS:
                resultado, m = func(base)
                assert resultado == esperado, f"{nome} ordenou errado em n={n}"
                linhas.append({
                    "n": n, "cenario": cenario, "algoritmo": nome,
                    "tempo_s": round(m.tempo, 6),
                    "comparacoes": m.comparacoes,
                    "movimentacoes": m.movimentacoes,
                })
                if verboso:
                    print(f"n={n:>6} {cenario:<10} {nome:<27} "
                          f"{m.tempo:>9.5f}s  comp={m.comparacoes:>12,}  "
                          f"mov={m.movimentacoes:>12,}")
        if verboso:
            print("-" * 95)

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
