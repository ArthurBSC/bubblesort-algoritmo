"""
MODULO 4 - Merge Sort.

Divisao e conquista: divide o vetor ao meio ate' sobrarem partes de 1 elemento
e INTERCALA as partes ja ordenadas.
Complexidade: O(n log n) em TODOS os casos (a divisao nao depende dos dados);
espaco O(n), porque precisa de vetores auxiliares. E' estavel.
"""

from contador import Metrica


def merge_sort(v, chave=lambda x: x):
    v = list(v)
    m = Metrica("Merge Sort").iniciar()
    _merge_sort(v, 0, len(v) - 1, chave, m)
    return v, m.parar()


def _merge_sort(v, ini, fim, chave, m):
    if ini >= fim:
        return
    meio = (ini + fim) // 2
    _merge_sort(v, ini, meio, chave, m)
    _merge_sort(v, meio + 1, fim, chave, m)
    _intercalar(v, ini, meio, fim, chave, m)


def _intercalar(v, ini, meio, fim, chave, m):
    esq = v[ini:meio + 1]
    dir_ = v[meio + 1:fim + 1]
    i = j = 0
    k = ini
    while i < len(esq) and j < len(dir_):
        m.comparacoes += 1
        if chave(esq[i]) <= chave(dir_[j]):
            v[k] = esq[i]
            i += 1
        else:
            v[k] = dir_[j]
            j += 1
        m.movimentacoes += 1
        k += 1
    while i < len(esq):
        v[k] = esq[i]
        i += 1
        k += 1
        m.movimentacoes += 1
    while j < len(dir_):
        v[k] = dir_[j]
        j += 1
        k += 1
        m.movimentacoes += 1
