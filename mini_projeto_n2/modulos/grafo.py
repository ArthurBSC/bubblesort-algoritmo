"""
MODULO 3 (base) - Representacao da rede de setores como GRAFO.

Vertices: setores da instituicao onde existem equipamentos de TI.
Arestas : enlaces de rede entre os setores.
Peso    : custo do enlace (latencia media em ms somada ao custo de manutencao
          normalizado do trecho) - usado pelo Dijkstra.

Estrutura: LISTA DE ADJACENCIA (dicionario de listas de pares).
"""


class Grafo:
    def __init__(self, direcionado=False):
        self.adj = {}
        self.direcionado = direcionado

    def adicionar_vertice(self, v):
        self.adj.setdefault(v, [])

    def adicionar_aresta(self, u, v, peso=1):
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)
        self.adj[u].append((v, peso))
        if not self.direcionado:
            self.adj[v].append((u, peso))

    def vizinhos(self, v):
        return self.adj.get(v, [])

    @property
    def vertices(self):
        return list(self.adj)

    @property
    def arestas(self):
        vistas = set()
        for u in self.adj:
            for v, p in self.adj[u]:
                chave = tuple(sorted((u, v))) if not self.direcionado else (u, v)
                if chave not in vistas:
                    vistas.add(chave)
                    yield u, v, p

    def __str__(self):
        linhas = []
        for u in sorted(self.adj):
            viz = ", ".join(f"{v}({p})" for v, p in sorted(self.adj[u]))
            linhas.append(f"  {u:<15} -> {viz}")
        return "\n".join(linhas)


# Rede usada no projeto: 12 setores, 17 enlaces com peso.
ENLACES = [
    ("CPD", "Suporte", 2), ("CPD", "Administrativo", 5), ("CPD", "Laboratorio1", 4),
    ("CPD", "Diretoria", 14), ("Suporte", "Almoxarifado", 3), ("Suporte", "Recepcao", 6),
    ("Administrativo", "Financeiro", 2), ("Administrativo", "Recepcao", 3),
    ("Financeiro", "Diretoria", 3), ("Laboratorio1", "Laboratorio2", 2),
    ("Laboratorio2", "Biblioteca", 4), ("Biblioteca", "SalaReunioes", 3),
    ("SalaReunioes", "Diretoria", 2), ("Almoxarifado", "Deposito", 2),
    ("Deposito", "Laboratorio2", 7), ("Recepcao", "Biblioteca", 8),
    ("Financeiro", "SalaReunioes", 6),
]


def rede_setores():
    """Devolve o grafo da rede de setores do estudo de caso."""
    g = Grafo()
    for u, v, p in ENLACES:
        g.adicionar_aresta(u, v, p)
    return g


def grafo_aleatorio(n_vertices, grau_medio=4, peso_max=20, semente=7):
    """Grafo sintetico conexo para os experimentos de desempenho."""
    import random
    rnd = random.Random(semente)
    g = Grafo()
    nomes = [f"S{i}" for i in range(n_vertices)]
    for i in range(1, n_vertices):                       # garante conectividade
        g.adicionar_aresta(nomes[i], nomes[rnd.randrange(i)], rnd.randint(1, peso_max))
    extras = max(0, (n_vertices * grau_medio) // 2 - (n_vertices - 1))
    for _ in range(extras):
        u, v = rnd.sample(nomes, 2)
        g.adicionar_aresta(u, v, rnd.randint(1, peso_max))
    return g
