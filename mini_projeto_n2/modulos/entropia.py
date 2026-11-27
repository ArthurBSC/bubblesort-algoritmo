"""
MODULO 2 (parte 1) - Entropia e Ganho de Informacao.

Entropia (Shannon):      H(S) = - SOMA p_i * log2(p_i)
Entropia condicional:    H(S|A) = SOMA (|Sv|/|S|) * H(Sv)
Ganho de informacao:     Ganho(S,A) = H(S) - H(S|A)

Implementado do zero (sem biblioteca de machine learning), como exige o
item 6 do enunciado.
"""

from math import log2


def contar_classes(registros, alvo):
    contagem = {}
    for r in registros:
        contagem[r[alvo]] = contagem.get(r[alvo], 0) + 1
    return contagem


def entropia(registros, alvo):
    """H(S) do conjunto em relacao ao atributo alvo."""
    total = len(registros)
    if total == 0:
        return 0.0
    h = 0.0
    for qtd in contar_classes(registros, alvo).values():
        p = qtd / total
        if p > 0:
            h -= p * log2(p)
    return h


def particionar(registros, atributo):
    """Divide o conjunto em subconjuntos S_v, um para cada valor do atributo."""
    particoes = {}
    for r in registros:
        particoes.setdefault(r[atributo], []).append(r)
    return particoes


def entropia_condicional(registros, atributo, alvo):
    """H(S|A) - media ponderada da entropia das particoes."""
    total = len(registros)
    if total == 0:
        return 0.0
    soma = 0.0
    for sub in particionar(registros, atributo).values():
        soma += (len(sub) / total) * entropia(sub, alvo)
    return soma


def ganho_informacao(registros, atributo, alvo):
    """Ganho(S, A) = H(S) - H(S|A)."""
    return entropia(registros, alvo) - entropia_condicional(registros, atributo, alvo)


def melhor_atributo(registros, atributos, alvo):
    """Atributo com maior ganho - criterio de escolha do no' no ID3."""
    return max(atributos, key=lambda a: ganho_informacao(registros, a, alvo))


def detalhar_calculos(registros, atributos, alvo):
    """Texto passo a passo dos calculos (usado no relatorio e na apresentacao)."""
    linhas = []
    total = len(registros)
    contagem = contar_classes(registros, alvo)
    h = entropia(registros, alvo)

    partes = " + ".join(f"({q}/{total})*log2({q}/{total})" for q in contagem.values())
    linhas.append(f"Conjunto S: {total} registros -> " +
                  ", ".join(f"{c}={q}" for c, q in sorted(contagem.items())))
    linhas.append(f"H(S) = -[{partes}] = {h:.4f} bits")
    linhas.append("")
    linhas.append(f"{'Atributo':<14}{'H(S|A)':>10}{'Ganho(S,A)':>14}")
    linhas.append("-" * 38)
    for a in sorted(atributos, key=lambda x: -ganho_informacao(registros, x, alvo)):
        hc = entropia_condicional(registros, a, alvo)
        linhas.append(f"{a:<14}{hc:>10.4f}{h - hc:>14.4f}")
    linhas.append("")
    linhas.append(f"Atributo escolhido para a raiz: "
                  f"{melhor_atributo(registros, atributos, alvo)}")
    return "\n".join(linhas)
