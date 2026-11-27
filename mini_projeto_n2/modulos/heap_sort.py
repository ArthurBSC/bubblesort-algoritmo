"""
MODULO 4 - Heap Sort.

Monta um HEAP MAXIMO sobre o proprio vetor e retira repetidamente a raiz
(maior elemento), trocando-a com a ultima posicao e reorganizando o heap.
Complexidade: O(n log n) em TODOS os casos; espaco O(1) (ordena in place).
Nao e' estavel.
"""

from contador import Metrica


def heap_sort(v, chave=lambda x: x):
    v = list(v)
    m = Metrica("Heap Sort").iniciar()
    n = len(v)

    for i in range(n // 2 - 1, -1, -1):          # construcao do heap maximo
        _descer(v, n, i, chave, m)

    for fim in range(n - 1, 0, -1):              # extracao da raiz
        v[0], v[fim] = v[fim], v[0]
        m.movimentacoes += 1
        _descer(v, fim, 0, chave, m)

    return v, m.parar()


def _descer(v, tamanho, i, chave, m):
    """Heapify: faz o elemento i 'descer' ate' a posicao correta."""
    while True:
        maior = i
        esq, dir_ = 2 * i + 1, 2 * i + 2
        if esq < tamanho:
            m.comparacoes += 1
            if chave(v[esq]) > chave(v[maior]):
                maior = esq
        if dir_ < tamanho:
            m.comparacoes += 1
            if chave(v[dir_]) > chave(v[maior]):
                maior = dir_
        if maior == i:
            return
        v[i], v[maior] = v[maior], v[i]
        m.movimentacoes += 1
        i = maior
