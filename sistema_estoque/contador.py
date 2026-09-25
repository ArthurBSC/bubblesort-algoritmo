"""
Contador de operações segundo o modelo de custo visto na Aula 02:

    Comparação           -> custo 1
    Atribuição           -> custo 2
    Operação matemática  -> custo 3

Além dos três tipos acima, também registramos trocas (Bubble Sort)
e deslocamentos (inserção/remoção), que são citados na Etapa 3.
"""

CUSTO_COMPARACAO = 1
CUSTO_ATRIBUICAO = 2
CUSTO_MATEMATICA = 3


class Contador:
    def __init__(self, gravar_passos=True):
        self.gravar_passos = gravar_passos
        self.zerar()

    def zerar(self):
        self.comparacoes = 0
        self.comp_elementos = 0
        self.atribuicoes = 0
        self.matematicas = 0
        self.trocas = 0
        self.deslocamentos = 0
        self.n_passos = 0
        self.passos = []

    def passo(self, indice, info=None):
        """Registra um passo do algoritmo: a posição que ele está examinando agora.

        Em uma busca, n_passos é o número de elementos examinados (busca linear) ou
        de iterações do laço (busca binária) - é a contagem usada nos exemplos da
        atividade ("foram necessárias 6 verificações", "busca binária: 3 passos").
        A lista passos serve para a interface web animar o algoritmo; com listas
        grandes, desligue com gravar_passos = False para poupar memória."""
        self.n_passos += 1
        if self.gravar_passos:
            self.passos.append({"i": indice, "info": info})

    # Os métodos recebem a quantidade para permitir contar várias de uma vez
    def comp(self, qtd=1):
        self.comparacoes += qtd

    def comp_elem(self):
        """Comparação entre elementos da lista (operação predominante).
        Também entra no total de comparações do custo T(n)."""
        self.comparacoes += 1
        self.comp_elementos += 1

    def atr(self, qtd=1):
        self.atribuicoes += qtd

    def mat(self, qtd=1):
        self.matematicas += qtd

    def troca(self):
        self.trocas += 1

    def desloc(self):
        self.deslocamentos += 1

    def custo_total(self):
        """T(n) = comparações*1 + atribuições*2 + operações matemáticas*3"""
        return (self.comparacoes * CUSTO_COMPARACAO
                + self.atribuicoes * CUSTO_ATRIBUICAO
                + self.matematicas * CUSTO_MATEMATICA)

    def resumo(self):
        return (f"passos={self.n_passos} | comparações={self.comparacoes} "
                f"(entre elementos={self.comp_elementos}) | atribuições={self.atribuicoes} | "
                f"op. matemáticas={self.matematicas} | trocas={self.trocas} | "
                f"deslocamentos={self.deslocamentos} | custo T(n)={self.custo_total()}")


class ContadorNulo(Contador):
    """Não conta nada. Usado para medir tempo sem a interferência da contagem."""

    def comp(self, qtd=1):
        pass

    def comp_elem(self):
        pass

    def passo(self, indice, info=None):
        pass

    def atr(self, qtd=1):
        pass

    def mat(self, qtd=1):
        pass

    def troca(self):
        pass

    def desloc(self):
        pass
