"""
Contador de operacoes compartilhado pelos algoritmos de ordenacao.

Mantem o mesmo criterio adotado no projeto N1: alem do tempo de execucao,
contamos COMPARACOES e MOVIMENTACOES (trocas ou copias de elementos),
porque o tempo depende da maquina e a contagem de operacoes nao.
"""

import time


class Metrica:
    def __init__(self, nome):
        self.nome = nome
        self.comparacoes = 0
        self.movimentacoes = 0
        self.tempo = 0.0
        self._inicio = None

    def iniciar(self):
        self._inicio = time.perf_counter()
        return self

    def parar(self):
        self.tempo = time.perf_counter() - self._inicio
        return self

    def como_dict(self):
        return {"algoritmo": self.nome, "comparacoes": self.comparacoes,
                "movimentacoes": self.movimentacoes, "tempo": self.tempo}

    def __str__(self):
        return (f"{self.nome:<12} tempo={self.tempo:>9.5f}s  "
                f"comparacoes={self.comparacoes:>12,}  "
                f"movimentacoes={self.movimentacoes:>12,}")
