"""
MODULO 3 - Dijkstra (caminho de MENOR CUSTO).

Diferente de BFS/DFS, considera o PESO das arestas: encontra o caminho de
custo minimo em grafos com pesos NAO NEGATIVOS.
Implementado com fila de prioridade (heap binario - heapq).
Complexidade: O((V + E) log V).
"""

import heapq

INFINITO = float("inf")


def dijkstra(grafo, origem, destino=None):
    dist = {v: INFINITO for v in grafo.vertices}
    pai = {v: None for v in grafo.vertices}
    fechados = set()
    operacoes = 0

    dist[origem] = 0
    heap = [(0, origem)]

    while heap:
        d, u = heapq.heappop(heap)
        if u in fechados:
            continue
        fechados.add(u)
        if destino is not None and u == destino:
            break
        for v, peso in grafo.vizinhos(u):
            operacoes += 1                     # 1 relaxamento testado por aresta
            if d + peso < dist[v]:             # relaxamento
                dist[v] = d + peso
                pai[v] = u
                heapq.heappush(heap, (dist[v], v))

    return {
        "dist": dist,
        "pai": pai,
        "caminho": reconstruir(pai, destino) if destino else None,
        "custo": dist.get(destino) if destino else None,
        "visitados": len(fechados),
        "operacoes": operacoes,
    }


def reconstruir(pai, destino):
    if destino not in pai:
        return []
    caminho, atual = [], destino
    while atual is not None:
        caminho.append(atual)
        atual = pai[atual]
    return caminho[::-1]
