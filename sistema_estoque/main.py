"""
Sistema de Estoque - Complexidade de Algoritmos (Projeto N1)

  Etapa 3: Inserção Ordenada          -> lista_ordenada.py
  Etapa 4: Bubble Sort                -> ordenacao.py
  Etapa 5: Busca Linear x Binária     -> buscas.py + relatorio.py

Como no "Exercício de fixação" dos slides: o sistema começa com uma lista
NÃO ordenada de produtos, ordena com o Bubble Sort e depois oferece o menu.

Executar:  python main.py
"""

import random

from buscas import busca_binaria, busca_linear
from contador import Contador
from lista_ordenada import ListaProdutos, Produto
from ordenacao import bubble_sort_otimizado

MAX_PRODUTOS = 50

# Mesma ordem do exercício dos slides {10, 9, 8, 5, 4, 3, 2, 1, 7, 6}, com códigos x10
PRODUTOS_INICIAIS = [
    Produto(100, "Teclado", 15),
    Produto(90, "Mouse", 40),
    Produto(80, "Monitor 24\"", 8),
    Produto(50, "Cabo HDMI", 60),
    Produto(40, "Webcam", 12),
    Produto(30, "Headset", 20),
    Produto(20, "Pen drive 32GB", 75),
    Produto(10, "Mousepad", 90),
    Produto(70, "SSD 480GB", 18),
    Produto(60, "Hub USB", 25),
]


def linha():
    print("-" * 64)


def ler_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("  Digite um número inteiro.")


def mostrar_codigos(lista):
    return " ".join(str(lista.v[i].codigo) for i in range(lista.n))


def listar(lista):
    if lista.vazia():
        print("  Estoque vazio.")
        return
    print(f"  {'Pos':>3}  {'Código':>6}  {'Produto':<22} {'Qtd':>5}")
    for i in range(lista.n):
        p = lista.v[i]
        print(f"  {i:>3}  {p.codigo:>6}  {p.nome:<22} {p.quantidade:>5}")
    print(f"  n = {lista.n} produto(s) cadastrados (capacidade {lista.max})")


def ordenar_com_bubble(lista, mostrar_passos=True):
    print(f"  Lista antes:  {mostrar_codigos(lista)}")
    c = Contador()

    def passo(numero, v):
        if mostrar_passos:
            print(f"  Passada {numero:>2}:   " + " ".join(str(v[i].codigo) for i in range(lista.n)))

    bubble_sort_otimizado(lista.v, lista.n, c, passo)
    print(f"  Lista depois: {mostrar_codigos(lista)}")
    print(f"  Comparações entre elementos: {c.comp_elementos} | trocas: {c.trocas} | "
          f"custo T(n) = {c.custo_total()}")


def cadastrar(lista):
    codigo = ler_int("  Código do produto: ")
    if busca_binaria(lista.v, lista.n, codigo) != -1:
        print("  Já existe um produto com esse código.")
        return
    nome = input("  Nome: ").strip() or f"Produto {codigo}"
    qtd = ler_int("  Quantidade: ")
    c = Contador()
    try:
        pos = lista.inserir_ordenado(Produto(codigo, nome, qtd), c)
    except OverflowError as e:
        print(f"  {e}")
        return
    print(f"  Inserido na posição {pos}. Lista: {mostrar_codigos(lista)}")
    print(f"  Deslocamentos: {c.deslocamentos} | {c.resumo()}")


def remover(lista):
    codigo = ler_int("  Código a remover: ")
    c = Contador()
    p = lista.remover(codigo, c)
    if p is None:
        print("  Produto não encontrado.")
    else:
        print(f"  Removido: {p.codigo} - {p.nome}. Lista: {mostrar_codigos(lista)}")
        print(f"  Deslocamentos: {c.deslocamentos} | {c.resumo()}")


def buscar(lista, funcao, nome):
    codigo = ler_int("  Código a buscar: ")
    c = Contador()
    pos = funcao(lista.v, lista.n, codigo, c)
    if pos == -1:
        print(f"  [{nome}] Código {codigo} não encontrado.")
    else:
        p = lista.v[pos]
        print(f"  [{nome}] Encontrado na posição {pos}: {p.nome} (qtd {p.quantidade})")
    print(f"  Passos: {c.n_passos} | {c.resumo()}")


def comparar_buscas(lista):
    codigo = ler_int("  Código a buscar: ")
    cl, cb = Contador(), Contador()
    pl = busca_linear(lista.v, lista.n, codigo, cl)
    pb = busca_binaria(lista.v, lista.n, codigo, cb)
    print(f"  {'':<16}{'Posição':>8}{'Passos':>8}{'Comparações':>13}{'Custo T(n)':>12}")
    print(f"  {'Busca Linear':<16}{pl:>8}{cl.n_passos:>8}{cl.comp_elementos:>13}{cl.custo_total():>12}")
    print(f"  {'Busca Binária':<16}{pb:>8}{cb.n_passos:>8}{cb.comp_elementos:>13}{cb.custo_total():>12}")


def gerar_lista_grande(lista):
    """Recria o estoque com n produtos em ordem aleatória, para testar com volumes maiores."""
    n = ler_int(f"  Quantos produtos (2 a {MAX_PRODUTOS * 200})? ")
    n = max(2, min(n, MAX_PRODUTOS * 200))
    codigos = [(i + 1) * 10 for i in range(n)]
    random.shuffle(codigos)
    nova = ListaProdutos(max(n + 10, MAX_PRODUTOS))
    nova.carregar([Produto(cod, f"Produto {cod}", random.randint(0, 100)) for cod in codigos])
    print(f"  Gerados {n} produtos desordenados. Ordenando com Bubble Sort...")
    ordenar_com_bubble(nova, mostrar_passos=n <= 12)
    return nova


def main():
    lista = ListaProdutos(MAX_PRODUTOS)
    lista.carregar(PRODUTOS_INICIAIS)

    linha()
    print("  SISTEMA DE ESTOQUE - Complexidade de Algoritmos")
    linha()
    print("  Produtos carregados fora de ordem. Ordenando com Bubble Sort:")
    ordenar_com_bubble(lista)

    opcoes = {
        "1": ("Cadastrar produto (inserção ordenada)", lambda: cadastrar(lista)),
        "2": ("Remover produto", lambda: remover(lista)),
        "3": ("Buscar produto - Busca Binária", lambda: buscar(lista, busca_binaria, "Binária")),
        "4": ("Buscar produto - Busca Linear", lambda: buscar(lista, busca_linear, "Linear")),
        "5": ("Comparar Busca Linear x Binária", lambda: comparar_buscas(lista)),
        "6": ("Listar estoque", lambda: listar(lista)),
        "7": ("Gerar estoque grande desordenado + Bubble Sort", None),
        "8": ("Gerar relatório de desempenho (Etapa 5)", None),
        "0": ("Sair", None),
    }

    while True:
        linha()
        for k, (texto, _) in opcoes.items():
            print(f"  {k}) {texto}")
        op = input("  Opção: ").strip()
        linha()
        if op == "0":
            print("  Até mais!")
            break
        elif op == "7":
            lista = gerar_lista_grande(lista)
        elif op == "8":
            import relatorio
            relatorio.main()
        elif op in opcoes:
            opcoes[op][1]()
        else:
            print("  Opção inválida.")


if __name__ == "__main__":
    main()
