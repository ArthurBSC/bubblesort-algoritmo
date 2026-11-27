"""
MODULO 5 (experimento 3) - Validacao da classificacao por ID3.

1. Calculos de entropia e ganho de informacao sobre a base completa.
2. Arvore de decisao e regras geradas.
3. Treino/teste 70/30: a arvore e' construida SO' com 70% dos registros e
   testada com os 30% restantes (registros que ela nunca viu).
4. Influencia do volume de dados sobre entropia, ganho e tamanho da arvore.

Saida: relatorio/resultados_id3.csv

Executar:  python experimentos/testes_classificacao.py
"""

import csv
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "modulos"))

import classificacao_id3 as id3              # noqa: E402
import entropia as ent                       # noqa: E402
from manipulacao_dados import ALVO, ATRIBUTOS_ID3, carregar  # noqa: E402

SAIDA = os.path.join(os.path.dirname(__file__), "..", "relatorio", "resultados_id3.csv")


def dividir(registros, proporcao=0.7, semente=13):
    r = list(registros)
    random.Random(semente).shuffle(r)
    corte = int(len(r) * proporcao)
    return r[:corte], r[corte:]


def executar(verboso=True):
    base = carregar()
    linhas = []

    if verboso:
        print("=" * 70)
        print("1) ENTROPIA E GANHO DE INFORMACAO - base completa")
        print("=" * 70)
        print(ent.detalhar_calculos(base, ATRIBUTOS_ID3, ALVO))

    arvore = id3.construir_arvore(base, ATRIBUTOS_ID3, ALVO)
    nos, folhas, prof = id3.estatisticas(arvore)
    if verboso:
        print("\n" + "=" * 70)
        print("2) ARVORE DE DECISAO (ID3)")
        print("=" * 70)
        print(id3.imprimir_arvore(arvore))
        print(f"\nNos: {nos} | Folhas: {folhas} | Profundidade: {prof}")
        print("\nREGRAS EXTRAIDAS:")
        for regra in id3.extrair_regras(arvore):
            print("  " + regra)

    treino, teste = dividir(base)
    arv_treino = id3.construir_arvore(treino, ATRIBUTOS_ID3, ALVO)
    ac_tr, n_tr, p_tr = id3.avaliar(arv_treino, treino, ALVO)
    ac_te, n_te, p_te = id3.avaliar(arv_treino, teste, ALVO)
    if verboso:
        print("\n" + "=" * 70)
        print("3) VALIDACAO TREINO/TESTE (70/30)")
        print("=" * 70)
        print(f"  Treino: {ac_tr}/{n_tr} corretos = {p_tr:.1%}")
        print(f"  Teste : {ac_te}/{n_te} corretos = {p_te:.1%}  "
              f"(registros nunca vistos pela arvore)")
        print("\n  Classificacoes do conjunto de teste:")
        for r in teste:
            previsto, caminho = id3.classificar(arv_treino, r)
            marca = "OK " if previsto == r[ALVO] else "ERRO"
            print(f"   {marca} {r['ID']}  real={r[ALVO]:<11} previsto={previsto:<11} "
                  f"[{' | '.join(caminho)}]")

    if verboso:
        print("\n" + "=" * 70)
        print("4) INFLUENCIA DO VOLUME DE DADOS")
        print("=" * 70)
        print(f"{'registros':>10}{'H(S)':>10}{'Ganho(Estado)':>16}"
              f"{'nos':>6}{'folhas':>8}{'prof':>6}{'acuracia':>10}")
    for qtd in (15, 30, 45, 60):
        amostra = base[:qtd]
        h = ent.entropia(amostra, ALVO)
        g = ent.ganho_informacao(amostra, "Estado", ALVO)
        a = id3.construir_arvore(amostra, ATRIBUTOS_ID3, ALVO)
        n_, f_, p_ = id3.estatisticas(a)
        _, _, acc = id3.avaliar(a, base, ALVO)
        linhas.append({"registros": qtd, "entropia": round(h, 4),
                       "ganho_estado": round(g, 4), "nos": n_, "folhas": f_,
                       "profundidade": p_, "acuracia_base_completa": round(acc, 4)})
        if verboso:
            print(f"{qtd:>10}{h:>10.4f}{g:>16.4f}{n_:>6}{f_:>8}{p_:>6}{acc:>10.1%}")

    linhas.append({"registros": "treino(42)", "entropia": round(ent.entropia(treino, ALVO), 4),
                   "ganho_estado": round(ent.ganho_informacao(treino, "Estado", ALVO), 4),
                   "nos": id3.estatisticas(arv_treino)[0],
                   "folhas": id3.estatisticas(arv_treino)[1],
                   "profundidade": id3.estatisticas(arv_treino)[2],
                   "acuracia_base_completa": round(p_te, 4)})

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)
    if verboso:
        print(f"\nResultados gravados em {os.path.abspath(SAIDA)}")
    return linhas


if __name__ == "__main__":
    executar()
