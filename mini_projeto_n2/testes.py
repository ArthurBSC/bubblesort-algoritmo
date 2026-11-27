"""
Testes automatizados do mini projeto (sem framework externo).

Executar:  python testes.py
"""

import os
import random
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "modulos"))

import classificacao_id3 as id3
import entropia as ent
import manipulacao_dados as dados
from bubble_sort import bubble_sort
from busca_bfs import bfs
from busca_dfs import dfs
from dijkstra import dijkstra
from grafo import rede_setores
from heap_sort import heap_sort
from merge_sort import merge_sort
from quick_sort import quick_sort, quick_sort_mediana3

ok = falhas = 0


def checar(descricao, condicao):
    global ok, falhas
    if condicao:
        ok += 1
        print(f"  [OK]   {descricao}")
    else:
        falhas += 1
        print(f"  [FALHA] {descricao}")


print("\n1. BASE DE DADOS")
base = dados.carregar()
checar("a base tem no minimo 50 registros (exigencia do enunciado)", len(base) >= 50)
checar("todos os registros tem os 11 campos", all(len(r) == len(dados.CAMPOS) for r in base))
checar("todos os rotulos sao validos",
       all(r["Decisao"] in dados.VALORES_VALIDOS["Decisao"] for r in base))
copia = list(base)
dados.inserir(copia, {"ID": "EQ999", "Nome": "Teste", "Tipo": "Desktop", "Setor": "CPD",
                      "Valor": 1000.0, "IdadeAnos": 1, "Idade": "Novo", "Uso": "Leve",
                      "Desempenho": "Alto", "Estado": "Bom", "Decisao": "Manter"})
checar("inserir adiciona o registro", len(copia) == len(base) + 1)
checar("consultar encontra o registro inserido", dados.consultar(copia, "ID", "EQ999"))
checar("remover retira o registro", dados.remover(copia, "EQ999") is not None)

print("\n2. ENTROPIA, GANHO E ID3")
puro = [{"X": "a", "C": "sim"}] * 10
checar("entropia de conjunto puro = 0", ent.entropia(puro, "C") == 0.0)
metade = [{"C": "sim"}] * 5 + [{"C": "nao"}] * 5
checar("entropia de conjunto 50/50 = 1 bit", abs(ent.entropia(metade, "C") - 1.0) < 1e-9)
h = ent.entropia(base, dados.ALVO)
checar(f"H(S) da base = {h:.4f} bits (entre 0 e log2(3)=1,585)", 0 < h < 1.585)
ganhos = {a: ent.ganho_informacao(base, a, dados.ALVO) for a in dados.ATRIBUTOS_ID3}
checar("todos os ganhos sao >= 0", all(g >= -1e-12 for g in ganhos.values()))
checar("o atributo de maior ganho e' Estado",
       ent.melhor_atributo(base, dados.ATRIBUTOS_ID3, dados.ALVO) == "Estado")
arvore = id3.construir_arvore(base, dados.ATRIBUTOS_ID3, dados.ALVO)
checar("a raiz da arvore e' o atributo de maior ganho", arvore.atributo == "Estado")
acertos, total, taxa = id3.avaliar(arvore, base, dados.ALVO)
checar(f"acuracia no proprio treino = {taxa:.1%}", taxa >= 0.95)
classe, _ = id3.classificar(arvore, {"Idade": "Antigo", "Uso": "Intenso",
                                     "Desempenho": "Baixo", "Estado": "Ruim"})
checar("equipamento em estado Ruim e' classificado como Substituir", classe == "Substituir")
classe, _ = id3.classificar(arvore, {"Idade": "Novo", "Uso": "Leve",
                                     "Desempenho": "Alto", "Estado": "Bom"})
checar("equipamento novo, bom e rapido e' classificado como Manter", classe == "Manter")

print("\n3. BUSCA EM GRAFOS")
g = rede_setores()
checar("o grafo tem 12 setores", len(g.vertices) == 12)
r_bfs = bfs(g, "CPD", "SalaReunioes")
r_dfs = dfs(g, "CPD", "SalaReunioes")
r_dij = dijkstra(g, "CPD", "SalaReunioes")
checar("BFS encontra o caminho com menos arestas (2)", r_bfs["arestas_no_caminho"] == 2)
checar("DFS chega ao destino", r_dfs["caminho"][-1] == "SalaReunioes")
checar("Dijkstra encontra custo 12 (menor que os 16 do caminho do BFS)",
       r_dij["custo"] == 12)
checar("Dijkstra usa mais arestas que o BFS, porem com custo menor",
       len(r_dij["caminho"]) > len(r_bfs["caminho"]))
checar("BFS alcanca todos os setores (grafo conexo)", r_bfs["visitados"] == 12)
checar("distancia do CPD ate' ele mesmo e' 0", dijkstra(g, "CPD")["dist"]["CPD"] == 0)

print("\n4. ORDENACAO")
rnd = random.Random(99)
for nome, func in (("Heap Sort", heap_sort), ("Quick Sort", quick_sort),
                   ("Quick Sort med3", quick_sort_mediana3),
                   ("Merge Sort", merge_sort), ("Bubble Sort", bubble_sort)):
    v = [rnd.randint(0, 9999) for _ in range(500)]
    checar(f"{nome} ordena 500 numeros aleatorios", func(v)[0] == sorted(v))
    checar(f"{nome} ordena vetor ja ordenado", func(sorted(v))[0] == sorted(v))
    checar(f"{nome} ordena vetor invertido", func(sorted(v, reverse=True))[0] == sorted(v))
    checar(f"{nome} trata vetor vazio e de 1 elemento",
           func([])[0] == [] and func([7])[0] == [7])
ordenado = list(range(2000))
_, m_fixo = quick_sort(ordenado)
_, m_med3 = quick_sort_mediana3(ordenado)
checar("Quick Sort com pivo fixo degrada em dados ordenados (pior caso O(n^2))",
       m_fixo.comparacoes > 50 * m_med3.comparacoes)
_, m_merge_r = merge_sort([rnd.randint(0, 999) for _ in range(1024)])
_, m_merge_o = merge_sort(list(range(1024)))
checar("Merge Sort mantem a mesma ordem de grandeza em qualquer cenario",
       0.5 < m_merge_o.comparacoes / m_merge_r.comparacoes < 1.5)
ordenados = heap_sort(base, chave=lambda r: r["Valor"])[0]
checar("Heap Sort ordena a base real por Valor",
       all(ordenados[i]["Valor"] <= ordenados[i + 1]["Valor"] for i in range(len(ordenados) - 1)))

print("\n" + "-" * 60)
print(f"  {ok} testes aprovados, {falhas} falha(s).")
print("-" * 60 + "\n")
sys.exit(1 if falhas else 0)
