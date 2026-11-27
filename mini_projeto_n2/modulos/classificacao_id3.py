"""
MODULO 2 (parte 2) - Arvore de Decisao pelo algoritmo ID3.

ID3 (Quinlan): a cada passo escolhe o atributo de MAIOR GANHO DE INFORMACAO,
cria um no' com esse atributo e repete recursivamente em cada particao.

Criterios de parada:
  1. todos os registros da particao tem a mesma classe  -> folha com a classe;
  2. acabaram os atributos                              -> folha com a classe majoritaria;
  3. particao vazia                                     -> folha com a classe majoritaria do pai.
"""

from entropia import (contar_classes, entropia, ganho_informacao,
                      melhor_atributo, particionar)


class No:
    """No' interno (pergunta sobre um atributo) ou folha (classe prevista)."""

    def __init__(self, atributo=None, classe=None, amostras=0, entropia_no=0.0):
        self.atributo = atributo        # None nas folhas
        self.classe = classe            # preenchido so' nas folhas
        self.filhos = {}                # valor do atributo -> No
        self.amostras = amostras
        self.entropia = entropia_no

    @property
    def folha(self):
        return self.atributo is None


def classe_majoritaria(registros, alvo):
    contagem = contar_classes(registros, alvo)
    return max(contagem, key=contagem.get)


def construir_arvore(registros, atributos, alvo, classe_pai=None):
    """Constroi a arvore ID3 recursivamente."""
    if not registros:                                   # parada 3
        return No(classe=classe_pai, amostras=0)

    contagem = contar_classes(registros, alvo)
    h = entropia(registros, alvo)

    if len(contagem) == 1:                              # parada 1 - no' puro
        return No(classe=next(iter(contagem)), amostras=len(registros), entropia_no=0.0)

    if not atributos:                                   # parada 2
        return No(classe=classe_majoritaria(registros, alvo),
                  amostras=len(registros), entropia_no=h)

    escolhido = melhor_atributo(registros, atributos, alvo)
    no = No(atributo=escolhido, amostras=len(registros), entropia_no=h)
    restantes = [a for a in atributos if a != escolhido]
    maioria = classe_majoritaria(registros, alvo)

    for valor, sub in sorted(particionar(registros, escolhido).items()):
        no.filhos[valor] = construir_arvore(sub, restantes, alvo, maioria)
    return no


def classificar(no, registro):
    """Percorre a arvore de cima para baixo ate' chegar a uma folha."""
    caminho = []
    while not no.folha:
        valor = registro.get(no.atributo)
        caminho.append(f"{no.atributo}={valor}")
        if valor not in no.filhos:                      # valor nunca visto no treino
            return no.filhos and classe_majoritaria_de(no) or None, caminho
        no = no.filhos[valor]
    return no.classe, caminho


def classe_majoritaria_de(no):
    """Classe mais frequente entre as folhas de uma subarvore."""
    contagem = {}
    pilha = [no]
    while pilha:
        atual = pilha.pop()
        if atual.folha:
            contagem[atual.classe] = contagem.get(atual.classe, 0) + max(atual.amostras, 1)
        else:
            pilha.extend(atual.filhos.values())
    return max(contagem, key=contagem.get) if contagem else None


def imprimir_arvore(no, prefixo="", rotulo="RAIZ"):
    """Impressao legivel da arvore (texto indentado)."""
    linhas = []
    if no.folha:
        linhas.append(f"{prefixo}[{rotulo}] --> CLASSE: {no.classe}  (n={no.amostras})")
    else:
        linhas.append(f"{prefixo}[{rotulo}] {no.atributo}?  "
                      f"(n={no.amostras}, H={no.entropia:.4f})")
        for valor, filho in no.filhos.items():
            linhas.append(imprimir_arvore(filho, prefixo + "    ", valor))
    return "\n".join(linhas)


def extrair_regras(no, condicoes=None):
    """Converte a arvore em regras SE ... ENTAO ..."""
    condicoes = condicoes or []
    if no.folha:
        se = " E ".join(condicoes) if condicoes else "sempre"
        return [f"SE {se} ENTAO {no.classe}  (n={no.amostras})"]
    regras = []
    for valor, filho in no.filhos.items():
        regras += extrair_regras(filho, condicoes + [f"{no.atributo} = {valor}"])
    return regras


def avaliar(no, registros, alvo):
    """Acuracia da arvore sobre um conjunto de registros."""
    acertos = 0
    for r in registros:
        previsto, _ = classificar(no, r)
        acertos += (previsto == r[alvo])
    return acertos, len(registros), (acertos / len(registros) if registros else 0.0)


def estatisticas(no):
    """(numero de nos, numero de folhas, profundidade maxima)."""
    if no.folha:
        return 1, 1, 1
    nos = folhas = 0
    prof = 0
    for filho in no.filhos.values():
        n, f, p = estatisticas(filho)
        nos += n
        folhas += f
        prof = max(prof, p)
    return nos + 1, folhas, prof + 1
