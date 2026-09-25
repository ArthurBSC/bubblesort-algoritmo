"""
Lista linear sequencial ordenada de produtos (Etapa 3 - Inserção Ordenada).

A lista é um vetor de tamanho fixo (MAX) mais a quantidade de elementos
ocupados (n), exatamente como nos slides "Listas Ordenadas":

    nota: 0 1 2 3 4 5 6 7 8 9
          ? ? ? ? ? ? ? ? ? ?
    n: 0

No projeto, n representa a quantidade de produtos cadastrados no estoque.
"""

from contador import Contador
from buscas import busca_binaria


class Produto:
    def __init__(self, codigo, nome, quantidade=0):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade

    def __repr__(self):
        return f"Produto({self.codigo}, {self.nome!r}, {self.quantidade})"


class ListaProdutos:
    def __init__(self, maximo=100):
        # Inicializar: vetor com MAX posições e n = 0
        self.v = [None] * maximo
        self.n = 0
        self.max = maximo

    def cheia(self):
        return self.n == self.max

    def vazia(self):
        return self.n == 0

    def codigos(self):
        return [self.v[i].codigo for i in range(self.n)]

    def inserir_ordenado(self, produto, c=None):
        """
        Insere mantendo a ordem crescente por código:
          1. localiza a posição correta;
          2. desloca os elementos maiores uma casa para a direita;
          3. coloca o novo elemento na posição encontrada.

        Melhor caso (inserir no final): nenhum deslocamento  -> O(1) de movimentação
        Pior caso (inserir no início):  n deslocamentos        -> O(n)
        """
        if c is None:
            c = Contador()
        if self.cheia():
            raise OverflowError("Estoque cheio: não há espaço para novos produtos.")

        c.atr()
        i = self.n  # começa depois do último elemento

        # enquanto o elemento anterior for maior que o novo, desloca para a direita
        while i > 0:
            c.comp()  # teste i > 0
            c.comp_elem()  # compara elemento anterior com o novo
            if self.v[i - 1].codigo > produto.codigo:
                self.v[i] = self.v[i - 1]
                c.mat()
                c.atr()
                c.desloc()
                c.passo(i - 1, {"acao": "deslocar"})
                i = i - 1
                c.mat()
                c.atr()
            else:
                break
        else:
            c.comp()  # último teste i > 0 que encerrou o laço

        self.v[i] = produto
        c.atr()
        self.n = self.n + 1
        c.mat()
        c.atr()
        return i

    def remover(self, codigo, c=None):
        """
        Remove um produto pelo código:
          1. encontra a posição com a busca binária;
          2. copia todos os elementos posteriores "para trás";
          3. desconta um da quantidade (n).
        Retorna o produto removido ou None se não existir.
        """
        if c is None:
            c = Contador()
        pos = busca_binaria(self.v, self.n, codigo, c)
        if pos == -1:
            return None

        removido = self.v[pos]
        c.atr()
        i = pos
        while i < self.n - 1:
            c.comp()
            self.v[i] = self.v[i + 1]
            c.mat()
            c.atr()
            c.desloc()
            i = i + 1
            c.mat()
            c.atr()
        c.comp()

        self.v[self.n - 1] = None
        self.n = self.n - 1
        c.mat()
        c.atr()
        return removido

    def carregar(self, produtos):
        """Carrega produtos na ordem recebida (sem ordenar), para depois usar o Bubble Sort."""
        if len(produtos) > self.max:
            raise OverflowError(f"Capacidade máxima é {self.max} produtos.")
        self.v = [None] * self.max
        for i, p in enumerate(produtos):
            self.v[i] = p
        self.n = len(produtos)

    def esta_ordenada(self):
        return all(self.v[i].codigo <= self.v[i + 1].codigo for i in range(self.n - 1))
