"""
MODULO 3 - DFS (Busca em Profundidade).

Explora um caminho ate' o limite antes de voltar (backtracking), usando PILHA.
Nao garante o menor caminho: serve para alcancabilidade, deteccao de ciclos
e componentes conexos.
Complexidade: O(V + E) de tempo e O(V) de espaco.
"""


def dfs(grafo, origem, destino=None):
    """Versao ITERATIVA com pilha explicita (evita estouro de recursao)."""
    visitado = set()
    pai = {origem: None}
    ordem = []
    operacoes = 0

    pilha = [origem]
    while pilha:
        u = pilha.pop()
        if u in visitado:
            continue
        visitado.add(u)
        ordem.append(u)
        if destino is not None and u == destino:
            break
        for v, _peso in sorted(grafo.vizinhos(u), reverse=True):
            operacoes += 1
            if v not in visitado:
                pai.setdefault(v, u)
                pilha.append(v)

    return {
        "ordem": ordem,
        "pai": pai,
        "caminho": reconstruir(pai, destino) if destino else None,
        "arestas_no_caminho": (len(reconstruir(pai, destino)) - 1) if destino and destino in pai else None,
        "visitados": len(visitado),
        "operacoes": operacoes,
    }


def dfs_recursivo(grafo, origem, visitado=None, ordem=None):
    """Versao recursiva, mostrada na apresentacao para comparar com a iterativa."""
    visitado = visitado if visitado is not None else set()
    ordem = ordem if ordem is not None else []
    visitado.add(origem)
    ordem.append(origem)
    for v, _peso in sorted(grafo.vizinhos(origem)):
        if v not in visitado:
            dfs_recursivo(grafo, v, visitado, ordem)
    return ordem


def reconstruir(pai, destino):
    if destino not in pai:
        return []
    caminho, atual = [], destino
    while atual is not None:
        caminho.append(atual)
        atual = pai[atual]
    return caminho[::-1]
