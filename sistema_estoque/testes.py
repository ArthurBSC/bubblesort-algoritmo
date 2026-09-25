"""
Testes automatizados do projeto.  Executar:  python testes.py
"""

import math
import random
import unittest

from buscas import busca_binaria, busca_linear
from contador import Contador
from lista_ordenada import ListaProdutos, Produto
from ordenacao import bubble_sort, bubble_sort_otimizado


def lista_de(codigos, maximo=100):
    lista = ListaProdutos(maximo)
    lista.carregar([Produto(c, f"P{c}") for c in codigos])
    return lista


class TestInsercaoOrdenada(unittest.TestCase):
    """Testes obrigatórios da Entrega 3."""

    def test_1_inserir_no_final(self):
        lista = lista_de([10, 20, 30, 40])
        c = Contador()
        lista.inserir_ordenado(Produto(50, "P50"), c)
        self.assertEqual(lista.codigos(), [10, 20, 30, 40, 50])
        self.assertEqual(c.deslocamentos, 0)  # melhor cenário

    def test_2_inserir_no_meio(self):
        lista = lista_de([10, 20, 40, 50])
        c = Contador()
        lista.inserir_ordenado(Produto(30, "P30"), c)
        self.assertEqual(lista.codigos(), [10, 20, 30, 40, 50])
        self.assertEqual(c.deslocamentos, 2)

    def test_3_inserir_no_inicio(self):
        lista = lista_de([20, 30, 40, 50])
        c = Contador()
        lista.inserir_ordenado(Produto(10, "P10"), c)
        self.assertEqual(lista.codigos(), [10, 20, 30, 40, 50])
        self.assertEqual(c.deslocamentos, 4)  # pior cenário: desloca todos

    def test_exemplo_da_atividade(self):
        lista = lista_de([10, 20, 30, 40, 50])
        lista.inserir_ordenado(Produto(35, "P35"))
        self.assertEqual(lista.codigos(), [10, 20, 30, 35, 40, 50])

    def test_lista_cheia(self):
        lista = lista_de([10, 20], maximo=2)
        with self.assertRaises(OverflowError):
            lista.inserir_ordenado(Produto(30, "P30"))


class TestRemocao(unittest.TestCase):
    def test_remover_do_meio(self):
        lista = lista_de([10, 20, 30, 40, 50])
        removido = lista.remover(30)
        self.assertEqual(removido.codigo, 30)
        self.assertEqual(lista.codigos(), [10, 20, 40, 50])
        self.assertEqual(lista.n, 4)

    def test_remover_inexistente(self):
        lista = lista_de([10, 20, 30])
        self.assertIsNone(lista.remover(25))
        self.assertEqual(lista.n, 3)


class TestBubbleSort(unittest.TestCase):
    def test_exemplo_dos_slides(self):
        notas = [7, 8, 5, 6, 10, 1.5, 7, 6.5, 9.2, 7]
        for funcao in (bubble_sort, bubble_sort_otimizado):
            v = [Produto(x, "") for x in notas]
            funcao(v, len(v))
            self.assertEqual([p.codigo for p in v], sorted(notas))

    def test_exercicio_de_fixacao(self):
        v = [Produto(x, "") for x in [10, 9, 8, 5, 4, 3, 2, 1, 7, 6]]
        bubble_sort_otimizado(v, len(v))
        self.assertEqual([p.codigo for p in v], list(range(1, 11)))

    def test_aleatorios(self):
        rnd = random.Random(1)
        for n in (0, 1, 2, 3, 17, 100):
            dados = [rnd.randint(-50, 50) for _ in range(n)]
            for funcao in (bubble_sort, bubble_sort_otimizado):
                v = [Produto(x, "") for x in dados]
                funcao(v, n)
                self.assertEqual([p.codigo for p in v], sorted(dados))

    def test_contagem_melhor_e_pior_caso(self):
        n = 10
        c = Contador()
        bubble_sort_otimizado([Produto(x, "") for x in range(n)], n, c)
        self.assertEqual(c.comp_elementos, n - 1)          # melhor caso O(n)
        self.assertEqual(c.trocas, 0)

        c = Contador()
        bubble_sort_otimizado([Produto(x, "") for x in range(n, 0, -1)], n, c)
        self.assertEqual(c.comp_elementos, n * (n - 1) // 2)  # pior caso O(n²)
        self.assertEqual(c.trocas, n * (n - 1) // 2)

        c = Contador()
        bubble_sort([Produto(x, "") for x in range(n)], n, c)
        self.assertEqual(c.comp_elementos, (n - 1) ** 2)    # versão básica sempre (n-1)²


class TestBuscas(unittest.TestCase):
    def setUp(self):
        self.v = [Produto(x, "") for x in [10, 20, 30, 40, 50, 60, 70, 80]]
        self.n = len(self.v)

    def test_busca_linear_exemplo_atividade(self):
        # PDF da Etapa 3: lista 10..70, procurar 60 -> "foram necessárias 6 verificações"
        v = self.v[:7]
        c = Contador()
        self.assertEqual(busca_linear(v, 7, 60, c), 5)
        self.assertEqual(c.n_passos, 6)
        self.assertEqual(c.comp_elementos, 6)

    def test_busca_binaria_exemplo_atividade(self):
        # PDF da Etapa 3: lista 10..80, procurar 70 -> acha olhando 50, depois 70
        c = Contador()
        self.assertEqual(busca_binaria(self.v, self.n, 70, c), 6)
        self.assertLessEqual(c.n_passos, 4)
        # cada passo da binária descarta metade: no máximo log2(n)+1 passos
        self.assertLessEqual(c.n_passos, math.floor(math.log2(self.n)) + 1)

    def test_passos_no_pior_caso(self):
        for n in (1, 7, 10, 100, 1000):
            v = [Produto((i + 1) * 10, "") for i in range(n)]
            c = Contador()
            busca_linear(v, n, 10 * n + 5, c)
            self.assertEqual(c.n_passos, n)          # examina todos os elementos
            c = Contador()
            busca_binaria(v, n, 10 * n + 5, c)
            self.assertEqual(c.n_passos, math.floor(math.log2(n)) + 1)

    def test_nao_encontrado(self):
        self.assertEqual(busca_linear(self.v, self.n, 55), -1)
        self.assertEqual(busca_binaria(self.v, self.n, 55), -1)
        self.assertEqual(busca_binaria(self.v, 0, 10), -1)

    def test_todas_as_posicoes(self):
        for i, p in enumerate(self.v):
            self.assertEqual(busca_linear(self.v, self.n, p.codigo), i)
            self.assertEqual(busca_binaria(self.v, self.n, p.codigo), i)

    def test_funcoes_de_custo_pior_caso(self):
        for n in (1, 7, 10, 100, 1000):
            v = [Produto((i + 1) * 10, "") for i in range(n)]
            c = Contador()
            busca_linear(v, n, 10 * n + 5, c)
            self.assertEqual(c.custo_total(), 7 * n + 3)
            c = Contador()
            busca_binaria(v, n, 10 * n + 5, c)
            k = math.floor(math.log2(n)) + 1
            self.assertEqual(c.custo_total(), 16 * k + 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
