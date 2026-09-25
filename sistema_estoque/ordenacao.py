"""
Etapa 4 - Ordenação por troca: Bubble Sort.

Ideia (slides "Listas Ordenadas"): comparar os elementos dois a dois e
trocar quando estiverem fora de ordem, fazendo o maior "borbulhar" até o fim.

Duas versões:
  - bubble_sort:            versão dos slides (Exercício 5) - sempre faz n-1 passadas
                            completas, comparando de i=0 até n-2.
  - bubble_sort_otimizado:  versão do Exercício 6 - a cada passada o maior elemento
                            já está no lugar, então o fim diminui; e se uma passada
                            não fizer nenhuma troca, a lista já está ordenada e paramos.

Simplificação da contagem: o cálculo de índice v[i + 1] não é contado como
operação matemática; contamos os testes dos laços, a comparação entre elementos,
as atribuições da troca (aux) e os incrementos/decrementos dos contadores.
"""

from contador import Contador


def _trocar(v, i, c):
    aux = v[i]
    v[i] = v[i + 1]
    v[i + 1] = aux
    c.atr(3)
    c.troca()


def bubble_sort(v, n, c=None):
    """Versão básica: (n-1) passadas x (n-1) comparações = (n-1)^2 comparações sempre -> O(n^2)."""
    if c is None:
        c = Contador()

    passo = 0
    c.atr()
    while passo < n - 1:
        c.comp()
        i = 0
        c.atr()
        while i < n - 1:
            c.comp()
            c.comp_elem()  # comparação entre elementos (operação predominante)
            if v[i].codigo > v[i + 1].codigo:
                _trocar(v, i, c)
            i = i + 1
            c.mat()
            c.atr()
        c.comp()
        passo = passo + 1
        c.mat()
        c.atr()
    c.comp()
    return c


def bubble_sort_otimizado(v, n, c=None, ao_fim_da_passada=None):
    """
    Versão otimizada.
      Melhor caso (lista já ordenada):   1 passada, n-1 comparações      -> O(n)
      Pior caso (ordem decrescente):     n(n-1)/2 comparações e trocas   -> O(n^2)

    ao_fim_da_passada(numero_passada, v) é opcional e serve para o menu
    mostrar a lista passo a passo.
    """
    if c is None:
        c = Contador()

    fim = n - 1
    c.mat()
    c.atr()
    trocou = True
    c.atr()
    passada = 0
    while trocou:
        c.comp()
        passada += 1
        trocou = False
        c.atr()
        i = 0
        c.atr()
        while i < fim:
            c.comp()
            c.comp_elem()  # comparação entre elementos (operação predominante)
            if v[i].codigo > v[i + 1].codigo:
                _trocar(v, i, c)
                c.passo(i, {"trocou": True, "passada": passada})
                trocou = True
                c.atr()
            else:
                c.passo(i, {"trocou": False, "passada": passada})
            i = i + 1
            c.mat()
            c.atr()
        c.comp()
        fim = fim - 1  # o maior elemento desta passada já está na posição final
        c.mat()
        c.atr()
        if ao_fim_da_passada:
            ao_fim_da_passada(passada, v)
    c.comp()
    return c
