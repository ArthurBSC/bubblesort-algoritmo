"""
MODULO 4 - Quick Sort.

Divisao e conquista: escolhe um PIVO, particiona o vetor (menores a esquerda,
maiores a direita) e repete nas duas metades.
Complexidade: O(n log n) no caso medio e O(n^2) no pior caso (pivo que gera
particoes muito desiguais - por exemplo, dados ja ordenados com pivo fixo).
Espaco O(log n) pela pilha de recursao.

Duas versoes para o experimento:
  quick_sort            -> pivo FIXO (ultimo elemento), mostra o pior caso;
  quick_sort_mediana3   -> pivo pela MEDIANA DE TRES, corrige o pior caso.
"""

from contador import Metrica


def quick_sort(v, chave=lambda x: x):
    """Pivo fixo = ultimo elemento (particionamento de Lomuto)."""
    v = list(v)
    m = Metrica("Quick Sort").iniciar()
    _quick(v, 0, len(v) - 1, chave, m, mediana3=False)
    return v, m.parar()


def quick_sort_mediana3(v, chave=lambda x: x):
    """Pivo escolhido pela mediana entre primeiro, meio e ultimo."""
    v = list(v)
    m = Metrica("Quick Sort (med3)").iniciar()
    _quick(v, 0, len(v) - 1, chave, m, mediana3=True)
    return v, m.parar()


def _quick(v, ini, fim, chave, m, mediana3):
    """Recursao apenas na MENOR particao + laco na maior.

    Isso limita a profundidade da pilha a O(log n) sem alterar o numero de
    comparacoes, permitindo medir o pior caso O(n^2) sem estourar a recursao.
    """
    while ini < fim:
        if mediana3:
            _mediana_de_tres(v, ini, fim, chave, m)
        p = _particionar(v, ini, fim, chave, m)
        if p - ini < fim - p:
            _quick(v, ini, p - 1, chave, m, mediana3)
            ini = p + 1
        else:
            _quick(v, p + 1, fim, chave, m, mediana3)
            fim = p - 1


def _particionar(v, ini, fim, chave, m):
    pivo = chave(v[fim])
    i = ini - 1
    for j in range(ini, fim):
        m.comparacoes += 1
        if chave(v[j]) <= pivo:
            i += 1
            v[i], v[j] = v[j], v[i]
            m.movimentacoes += 1
    v[i + 1], v[fim] = v[fim], v[i + 1]
    m.movimentacoes += 1
    return i + 1


def _mediana_de_tres(v, ini, fim, chave, m):
    meio = (ini + fim) // 2
    trio = sorted([ini, meio, fim], key=lambda k: chave(v[k]))
    m.comparacoes += 3
    v[trio[1]], v[fim] = v[fim], v[trio[1]]      # mediana vai para o fim
    m.movimentacoes += 1
