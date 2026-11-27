"""
MINI PROJETO N2 - Desafio Integrador de Complexidade de Algoritmos
Sistema Inteligente de Gestao e Analise de Equipamentos de TI

Integra os cinco modulos exigidos no enunciado:
  1. BASE DE DADOS        -> modulos/manipulacao_dados.py
  2. CLASSIFICACAO (ID3)  -> modulos/entropia.py + modulos/classificacao_id3.py
  3. BUSCA EM GRAFOS      -> modulos/busca_bfs.py, busca_dfs.py, dijkstra.py
  4. ORDENACAO            -> modulos/heap_sort.py, quick_sort.py, merge_sort.py
  5. ANALISE              -> experimentos/

Executar:  python main.py
"""

import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "modulos"))
sys.path.insert(0, os.path.join(BASE, "experimentos"))

import classificacao_id3 as id3              # noqa: E402
import entropia as ent                       # noqa: E402
import manipulacao_dados as dados            # noqa: E402
from busca_bfs import bfs                    # noqa: E402
from busca_dfs import dfs, dfs_recursivo     # noqa: E402
from dijkstra import dijkstra                # noqa: E402
from grafo import rede_setores               # noqa: E402
from heap_sort import heap_sort              # noqa: E402
from merge_sort import merge_sort            # noqa: E402
from quick_sort import quick_sort, quick_sort_mediana3  # noqa: E402

ORDENADORES = [("Heap Sort", heap_sort),
               ("Quick Sort (pivo fixo)", quick_sort),
               ("Quick Sort (mediana de 3)", quick_sort_mediana3),
               ("Merge Sort", merge_sort)]


def titulo(txt):
    print("\n" + "=" * 74)
    print(txt)
    print("=" * 74)


def pausar():
    input("\n[ENTER] para voltar ao menu...")


def ler(msg, opcoes=None):
    while True:
        v = input(msg).strip()
        if opcoes is None or v in opcoes:
            return v
        print(f"  Valores aceitos: {opcoes}")


# ------------------------------------------------------- 1. BASE DE DADOS
def menu_base(base):
    titulo("MODULO 1 - BASE DE DADOS")
    print(" 1 Listar registros      2 Inserir      3 Consultar")
    print(" 4 Remover               5 Salvar CSV   6 Recarregar CSV   0 Voltar")
    op = ler(" > ")

    if op == "1":
        print()
        print(dados.tabela(base))
        classes, setores = dados.resumo(base)
        print(f"\n  Total: {len(base)} registros")
        print("  Por decisao: " + ", ".join(f"{k}={v}" for k, v in sorted(classes.items())))
        print("  Por setor  : " + ", ".join(f"{k}={v}" for k, v in sorted(setores.items())))
    elif op == "2":
        novo = {"ID": dados.proximo_id(base)}
        print(f"  ID gerado: {novo['ID']}")
        novo["Nome"] = input("  Nome: ") or "Equipamento"
        novo["Tipo"] = input("  Tipo: ") or "Desktop"
        novo["Setor"] = input("  Setor: ") or "CPD"
        novo["Valor"] = float(input("  Valor (R$): ") or 1000)
        novo["IdadeAnos"] = int(input("  Idade em anos: ") or 1)
        novo["Idade"] = ler("  Idade [Novo/Intermediario/Antigo]: ",
                            dados.VALORES_VALIDOS["Idade"])
        novo["Uso"] = ler("  Uso [Leve/Moderado/Intenso]: ", dados.VALORES_VALIDOS["Uso"])
        novo["Desempenho"] = ler("  Desempenho [Alto/Medio/Baixo]: ",
                                 dados.VALORES_VALIDOS["Desempenho"])
        novo["Estado"] = ler("  Estado [Bom/Regular/Ruim]: ", dados.VALORES_VALIDOS["Estado"])
        novo["Decisao"] = ler("  Decisao real [Manter/Manutencao/Substituir]: ",
                              dados.VALORES_VALIDOS["Decisao"])
        dados.inserir(base, novo)
        print(f"\n  Inserido. A base agora tem {len(base)} registros "
              f"(use a opcao 5 para gravar no CSV).")
    elif op == "3":
        campo = input("  Campo (ID/Tipo/Setor/Estado/Decisao...): ") or "Setor"
        valor = input("  Valor: ")
        achados = dados.consultar(base, campo, valor)
        print(f"\n  {len(achados)} registro(s):\n")
        print(dados.tabela(achados) if achados else "  nenhum.")
    elif op == "4":
        r = dados.remover(base, input("  ID: ").strip().upper())
        print("  Removido: " + (r["Nome"] if r else "ID nao encontrado."))
    elif op == "5":
        print(f"  {dados.salvar(base)} registros gravados em dados/base_dados.csv")
    elif op == "6":
        base[:] = dados.carregar()
        print(f"  {len(base)} registros recarregados.")
    if op != "0":
        pausar()


# ------------------------------------------------- 2. CLASSIFICACAO ID3
def menu_id3(base, estado):
    titulo("MODULO 2 - CLASSIFICACAO POR ENTROPIA, GANHO E ID3")
    print(" 1 Calcular entropia e ganho      2 Treinar/reconstruir a arvore")
    print(" 3 Exibir a arvore                4 Exibir as regras")
    print(" 5 Classificar novo equipamento   6 Validar (treino/teste 70-30)   0 Voltar")
    op = ler(" > ")

    if op == "1":
        print()
        print(ent.detalhar_calculos(base, dados.ATRIBUTOS_ID3, dados.ALVO))
    elif op == "2":
        estado["arvore"] = id3.construir_arvore(base, dados.ATRIBUTOS_ID3, dados.ALVO)
        n, f, p = id3.estatisticas(estado["arvore"])
        print(f"\n  Arvore construida com {len(base)} registros: "
              f"{n} nos, {f} folhas, profundidade {p}.")
    elif op in ("3", "4", "5"):
        if estado["arvore"] is None:
            estado["arvore"] = id3.construir_arvore(base, dados.ATRIBUTOS_ID3, dados.ALVO)
        if op == "3":
            print("\n" + id3.imprimir_arvore(estado["arvore"]))
        elif op == "4":
            print()
            for r in id3.extrair_regras(estado["arvore"]):
                print("  " + r)
        else:
            novo = {
                "Idade": ler("  Idade [Novo/Intermediario/Antigo]: ",
                             dados.VALORES_VALIDOS["Idade"]),
                "Uso": ler("  Uso [Leve/Moderado/Intenso]: ", dados.VALORES_VALIDOS["Uso"]),
                "Desempenho": ler("  Desempenho [Alto/Medio/Baixo]: ",
                                  dados.VALORES_VALIDOS["Desempenho"]),
                "Estado": ler("  Estado [Bom/Regular/Ruim]: ",
                              dados.VALORES_VALIDOS["Estado"]),
            }
            classe, caminho = id3.classificar(estado["arvore"], novo)
            print(f"\n  Caminho na arvore: {' -> '.join(caminho)}")
            print(f"  DECISAO PREVISTA : {classe}")
    elif op == "6":
        import testes_classificacao as tc
        treino, teste = tc.dividir(base)
        arv = id3.construir_arvore(treino, dados.ATRIBUTOS_ID3, dados.ALVO)
        print(f"\n  Treino: {len(treino)} registros | Teste: {len(teste)} registros")
        for conj, nome in ((treino, "treino"), (teste, "teste ")):
            a, t, p = id3.avaliar(arv, conj, dados.ALVO)
            print(f"  Acuracia no {nome}: {a}/{t} = {p:.1%}")
    if op != "0":
        pausar()


# ----------------------------------------------------- 3. BUSCA EM GRAFOS
def menu_grafos(base):
    g = rede_setores()
    titulo("MODULO 3 - BUSCA EM GRAFOS (BFS, DFS E DIJKSTRA)")
    print(" 1 Exibir o grafo (lista de adjacencia)   2 BFS   3 DFS")
    print(" 4 Dijkstra      5 Comparar os tres       0 Voltar")
    op = ler(" > ")

    if op == "1":
        print(f"\n  {len(g.vertices)} setores, {len(list(g.arestas))} enlaces:\n")
        print(g)
    elif op in ("2", "3", "4", "5"):
        print("\n  Setores: " + ", ".join(sorted(g.vertices)))
        origem = input("  Origem [CPD]: ").strip() or "CPD"
        destino = input("  Destino [SalaReunioes]: ").strip() or "SalaReunioes"
        if origem not in g.adj or destino not in g.adj:
            print("  Setor inexistente.")
            return pausar()

        def mostrar(nome, r):
            cam = r["caminho"]
            custo = sum(min(p for v, p in g.vizinhos(a) if v == b)
                        for a, b in zip(cam, cam[1:])) if len(cam) > 1 else 0
            print(f"\n  {nome}")
            print(f"    caminho : {' -> '.join(cam)}")
            print(f"    arestas : {len(cam) - 1}   custo: {custo}   "
                  f"visitados: {r['visitados']}   operacoes: {r['operacoes']}")
            if nome == "BFS":
                print(f"    ordem   : {' '.join(r['ordem'][:12])}"
                      f"{' ...' if len(r['ordem']) > 12 else ''}")

        if op in ("2", "5"):
            mostrar("BFS", bfs(g, origem, destino))
        if op in ("3", "5"):
            mostrar("DFS", dfs(g, origem, destino))
            print(f"    DFS recursivo (ordem completa): "
                  f"{' '.join(dfs_recursivo(g, origem)[:12])} ...")
        if op in ("4", "5"):
            r = dijkstra(g, origem, destino)
            mostrar("Dijkstra", r)
            print("    custos minimos a partir da origem:")
            for v, d in sorted(r["dist"].items(), key=lambda x: x[1]):
                print(f"      {v:<15}{d}")
        if op == "5":
            print("\n  Leitura: BFS minimiza o NUMERO DE ARESTAS; Dijkstra minimiza o")
            print("  CUSTO TOTAL (pode usar mais saltos); DFS nao otimiza nada - ele")
            print("  apenas alcanca o destino seguindo um ramo ate' o fim.")
    if op != "0":
        pausar()


# --------------------------------------------------------- 4. ORDENACAO
def menu_ordenacao(base):
    titulo("MODULO 4 - ORDENACAO (HEAP SORT, QUICK SORT E MERGE SORT)")
    print(" 1 Ordenar a base por Valor      2 Ordenar a base por IdadeAnos")
    print(" 3 Comparar os algoritmos na base real")
    print(" 4 Rodar o experimento completo (100 a 10.000 registros)   0 Voltar")
    op = ler(" > ")

    if op in ("1", "2"):
        campo = "Valor" if op == "1" else "IdadeAnos"
        print("\n  Algoritmo: 1 Heap  2 Quick  3 Quick(med3)  4 Merge")
        escolha = ler("  > ", ["1", "2", "3", "4"])
        nome, func = ORDENADORES[int(escolha) - 1]
        ordenado, m = func(base, chave=lambda r: r[campo])
        print(f"\n  {m}\n")
        print(dados.tabela(ordenado, limite=15))
    elif op == "3":
        print(f"\n  Base real com {len(base)} equipamentos, ordenando por Valor:\n")
        for nome, func in ORDENADORES:
            _, m = func(base, chave=lambda r: r["Valor"])
            print("  " + str(m))
        print("\n  Com n=60 a diferenca e' irrelevante: por isso o experimento do")
        print("  Modulo 5 repete o teste com 100, 500, 1.000, 5.000 e 10.000 registros.")
    elif op == "4":
        import testes_ordenacao
        testes_ordenacao.executar()
    if op != "0":
        pausar()


# ---------------------------------------------------------- 5. ANALISE
def menu_analise():
    titulo("MODULO 5 - ANALISE DE COMPLEXIDADE E RELATORIO")
    print(" 1 Experimento de ordenacao    2 Experimento de busca em grafos")
    print(" 3 Validacao do ID3            4 Gerar TUDO + graficos + relatorio")
    print(" 5 Tabela de complexidades (Big O)                        0 Voltar")
    op = ler(" > ")

    if op == "1":
        import testes_ordenacao; testes_ordenacao.executar()
    elif op == "2":
        import testes_busca; testes_busca.executar()
    elif op == "3":
        import testes_classificacao; testes_classificacao.executar()
    elif op == "4":
        import resultados; resultados.main()
    elif op == "5":
        print("""
  Algoritmo            Melhor      Medio       Pior        Espaco   Estavel
  -------------------------------------------------------------------------
  Heap Sort            O(n log n)  O(n log n)  O(n log n)  O(1)     nao
  Quick Sort (fixo)    O(n log n)  O(n log n)  O(n^2)      O(log n) nao
  Quick Sort (med3)    O(n log n)  O(n log n)  O(n^2)*     O(log n) nao
  Merge Sort           O(n log n)  O(n log n)  O(n log n)  O(n)     sim
  Bubble Sort (N1)     O(n)        O(n^2)      O(n^2)      O(1)     sim
  BFS                  O(V + E)    O(V + E)    O(V + E)    O(V)      -
  DFS                  O(V + E)    O(V + E)    O(V + E)    O(V)      -
  Dijkstra (heap)      O((V+E)logV) idem       idem        O(V)      -
  ID3 (treino)         O(a * n * v) a=atributos, v=valores, n=registros

  * teoricamente O(n^2), mas o pior caso deixa de ocorrer com dados ordenados.""")
    if op != "0":
        pausar()


def main():
    base = dados.carregar()
    estado = {"arvore": None}
    while True:
        titulo("SISTEMA INTELIGENTE DE GESTAO E ANALISE DE EQUIPAMENTOS DE TI")
        print(f"  Base carregada: {len(base)} equipamentos | "
              f"Arvore ID3: {'treinada' if estado['arvore'] else 'nao treinada'}\n")
        print("  1 - Modulo 1: Base de dados (cadastro, consulta, CSV)")
        print("  2 - Modulo 2: Classificacao por Entropia e ID3")
        print("  3 - Modulo 3: Busca em grafos (BFS, DFS, Dijkstra)")
        print("  4 - Modulo 4: Ordenacao (Heap, Quick, Merge)")
        print("  5 - Modulo 5: Analise de complexidade e relatorio")
        print("  0 - Sair")
        op = ler("\n  > ")
        if op == "1":
            menu_base(base)
        elif op == "2":
            menu_id3(base, estado)
        elif op == "3":
            menu_grafos(base)
        elif op == "4":
            menu_ordenacao(base)
        elif op == "5":
            menu_analise()
        elif op == "0":
            print("\n  Encerrado.\n")
            return


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Encerrado.\n")
