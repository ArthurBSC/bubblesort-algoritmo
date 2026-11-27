"""
MODULO 3 - BFS (Busca em Largura).

Explora o grafo por NIVEIS usando uma FILA (FIFO).
Em grafo NAO PONDERADO devolve o caminho com o MENOR NUMERO DE ARESTAS.
Complexidade: O(V + E) de tempo e O(V) de espaco.
"""

from collections import deque


def bfs(grafo, origem, destino=None):
    """Percorre o grafo a partir da origem.

    Devolve um dicionario com: ordem de visita, nivel de cada vertice,
    antecessores, caminho ate' o destino (se informado) e operacoes contadas.
    """
    visitado = {origem}
    nivel = {origem: 0}
    pai = {origem: None}
    ordem = []
    operacoes = 0

    fila = deque([origem])
    while fila:
        u = fila.popleft()
        ordem.append(u)
        if destino is not None and u == destino:
            break
        for v, _peso in grafo.vizinhos(u):
            operacoes += 1                     # 1 verificacao por aresta
            if v not in visitado:
                visitado.add(v)
                nivel[v] = nivel[u] + 1
                pai[v] = u
                fila.append(v)

    return {
        "ordem": ordem,
        "nivel": nivel,
        "pai": pai,
        "caminho": reconstruir(pai, destino) if destino else None,
        "arestas_no_caminho": (len(reconstruir(pai, destino)) - 1) if destino and destino in pai else None,
        "visitados": len(visitado),
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
