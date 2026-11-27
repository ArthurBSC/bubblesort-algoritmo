"""
Gera a base de dados do mini projeto (dados/base_dados.csv).

A base e' SIMULADA, mas criada a partir de regras de negocio reais de gestao
de parque de TI: equipamento muito antigo, com desempenho baixo ou em mau
estado de conservacao tende a ser substituido; equipamento bom e novo e'
mantido. O rotulo "Decisao" e' a variavel que o ID3 aprende a prever.

Executar:  python dados/gerar_base.py
"""

import csv
import os
import random

random.seed(2024)  # base reproduzivel: todo mundo gera o mesmo CSV

SETORES = [
    "CPD", "Recepcao", "Administrativo", "Financeiro", "Suporte",
    "Laboratorio1", "Laboratorio2", "Biblioteca", "Almoxarifado",
    "Diretoria", "SalaReunioes", "Deposito",
]

TIPOS = {
    "Desktop":    (1800, 5200),
    "Notebook":   (2500, 7800),
    "Monitor":    (600, 2400),
    "Impressora": (900, 4500),
    "Switch":     (700, 6000),
    "Roteador":   (400, 3800),
    "Servidor":   (9000, 32000),
    "Nobreak":    (800, 5600),
    "Projetor":   (1500, 6200),
    "Scanner":    (700, 3100),
}


def faixa_idade(anos):
    if anos <= 2:
        return "Novo"
    if anos <= 5:
        return "Intermediario"
    return "Antigo"


def decidir(idade, uso, desempenho, estado):
    """Regra de negocio usada para rotular a base (o ID3 vai redescobri-la)."""
    if estado == "Ruim":
        return "Substituir"
    if estado == "Regular":
        if desempenho == "Baixo":
            return "Substituir"
        return "Manutencao"
    # estado Bom
    if desempenho == "Baixo":
        return "Manutencao"
    if desempenho == "Medio":
        return "Manutencao" if uso == "Intenso" else "Manter"
    return "Manter"


def gerar(qtd=60):
    linhas = []
    for i in range(1, qtd + 1):
        tipo = random.choice(list(TIPOS))
        vmin, vmax = TIPOS[tipo]
        anos = random.randint(0, 11)
        idade = faixa_idade(anos)

        # desempenho e estado sao correlacionados com a idade (realismo)
        if idade == "Novo":
            desempenho = random.choices(["Alto", "Medio", "Baixo"], [6, 3, 1])[0]
            estado = random.choices(["Bom", "Regular", "Ruim"], [7, 2, 1])[0]
        elif idade == "Intermediario":
            desempenho = random.choices(["Alto", "Medio", "Baixo"], [3, 5, 2])[0]
            estado = random.choices(["Bom", "Regular", "Ruim"], [4, 4, 2])[0]
        else:
            desempenho = random.choices(["Alto", "Medio", "Baixo"], [1, 3, 6])[0]
            estado = random.choices(["Bom", "Regular", "Ruim"], [2, 4, 4])[0]

        uso = random.choices(["Leve", "Moderado", "Intenso"], [3, 4, 3])[0]

        # valor de mercado cai com a idade
        valor = random.uniform(vmin, vmax) * max(0.25, 1 - 0.07 * anos)

        linhas.append({
            "ID": f"EQ{i:03d}",
            "Nome": f"{tipo} {i:03d}",
            "Tipo": tipo,
            "Setor": SETORES[(i - 1) % len(SETORES)],
            "Valor": f"{valor:.2f}",
            "IdadeAnos": anos,
            "Idade": idade,
            "Uso": uso,
            "Desempenho": desempenho,
            "Estado": estado,
            "Decisao": decidir(idade, uso, desempenho, estado),
        })
    return linhas


if __name__ == "__main__":
    destino = os.path.join(os.path.dirname(__file__), "base_dados.csv")
    registros = gerar(60)
    with open(destino, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(registros[0].keys()))
        w.writeheader()
        w.writerows(registros)
    print(f"{len(registros)} registros gravados em {destino}")
