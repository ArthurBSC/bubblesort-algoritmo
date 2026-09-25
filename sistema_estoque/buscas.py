"""
Etapa 5 - Estruturas de busca: Busca Linear x Busca Binária.

Busca Linear (sequencial): verifica do início ao fim, um elemento por vez.
    Melhor caso: o código está na 1ª posição         -> O(1)
    Pior caso:   está no fim ou não existe            -> O(n)
    Função de custo (não encontrado): T(n) = 7n + 3

Busca Binária: só funciona em lista ORDENADA. Olha o elemento do meio e
descarta metade da lista a cada passo (n -> n/2 -> n/4 -> ...).
    Melhor caso: o código está exatamente no meio     -> O(1)
    Pior caso:   não existe                           -> O(log n)
    Função de custo (não encontrado, k iterações): T(k) = 16k + 8,
    com k = floor(log2 n) + 1 no pior caso.

As duas funções devolvem a posição (índice) ou -1 se não encontrar.
"""

from contador import Contador


def busca_linear(v, n, codigo, c=None):
    if c is None:
        c = Contador()

    i = 0
    c.atr()                      # i = 0                         -> 1 atribuição
    while i < n:
        c.comp()                 # teste i < n                   -> até n+1 comparações
        c.comp_elem()            # v[i] == codigo                -> até n comparações
        c.passo(i)
        if v[i].codigo == codigo:
            return i
        i = i + 1
        c.mat()                  # i + 1                         -> até n op. matemáticas
        c.atr()                  # i = ...                       -> até n atribuições
    c.comp()                     # último teste i < n (falso)
    return -1


def busca_binaria(v, n, codigo, c=None):
    if c is None:
        c = Contador()

    ini = 0
    fim = n - 1
    c.atr(2)                     # ini = 0 ; fim = ...
    c.mat()                      # n - 1
    while ini <= fim:
        c.comp()                 # teste ini <= fim
        meio = (ini + fim) // 2
        c.mat(2)                 # soma e divisão
        c.atr()                  # meio = ...
        c.comp_elem()
        c.passo(meio, {"ini": ini, "fim": fim})
        if v[meio].codigo == codigo:
            return meio
        c.comp_elem()
        if v[meio].codigo < codigo:
            ini = meio + 1       # procurado está acima: descarta a metade esquerda
        else:
            fim = meio - 1       # procurado está abaixo: descarta a metade direita
        c.mat()
        c.atr()
    c.comp()                     # último teste ini <= fim (falso)
    return -1
