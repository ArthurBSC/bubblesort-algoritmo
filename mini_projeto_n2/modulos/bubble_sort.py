"""
Bubble Sort - trazido do projeto N1 apenas como LINHA DE BASE O(n^2).

Serve para dimensionar o ganho dos algoritmos O(n log n) do Modulo 4.
Versao otimizada: para assim que uma passada nao faz nenhuma troca.
"""

from contador import Metrica


def bubble_sort(v, chave=lambda x: x):
    v = list(v)
    m = Metrica("Bubble Sort").iniciar()
    n = len(v)
    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            m.comparacoes += 1
            if chave(v[j]) > chave(v[j + 1]):
                v[j], v[j + 1] = v[j + 1], v[j]
                m.movimentacoes += 1
                trocou = True
        if not trocou:
            break
    return v, m.parar()
