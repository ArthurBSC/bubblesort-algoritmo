"""
MODULO 1 - Pesquisa, construcao e manipulacao da base de dados.

Responsavel por carregar, salvar, inserir, consultar e remover registros
de equipamentos de TI. A base fica em memoria como uma LISTA DE DICIONARIOS
(estrutura exigida no item 6 do enunciado) e e' persistida em CSV.
"""

import csv
import os

CAMPOS = ["ID", "Nome", "Tipo", "Setor", "Valor", "IdadeAnos",
          "Idade", "Uso", "Desempenho", "Estado", "Decisao"]

ATRIBUTOS_ID3 = ["Idade", "Uso", "Desempenho", "Estado"]
ALVO = "Decisao"

VALORES_VALIDOS = {
    "Idade": ["Novo", "Intermediario", "Antigo"],
    "Uso": ["Leve", "Moderado", "Intenso"],
    "Desempenho": ["Alto", "Medio", "Baixo"],
    "Estado": ["Bom", "Regular", "Ruim"],
    "Decisao": ["Manter", "Manutencao", "Substituir"],
}

CAMINHO_PADRAO = os.path.join(os.path.dirname(__file__), "..", "dados", "base_dados.csv")


# ---------------------------------------------------------------- persistencia
def carregar(caminho=CAMINHO_PADRAO):
    """Le o CSV e devolve uma lista de dicionarios (um por equipamento)."""
    registros = []
    with open(caminho, newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            linha["Valor"] = float(linha["Valor"])
            linha["IdadeAnos"] = int(linha["IdadeAnos"])
            registros.append(linha)
    return registros


def salvar(registros, caminho=CAMINHO_PADRAO):
    """Grava a lista de dicionarios de volta no CSV."""
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for r in registros:
            w.writerow({c: r.get(c, "") for c in CAMPOS})
    return len(registros)


# ----------------------------------------------------------------------- CRUD
def proximo_id(registros):
    numeros = [int(r["ID"][2:]) for r in registros if r["ID"].startswith("EQ")]
    return f"EQ{(max(numeros) + 1 if numeros else 1):03d}"


def inserir(registros, novo):
    """Insere um registro novo; devolve o registro inserido."""
    if any(r["ID"] == novo["ID"] for r in registros):
        raise ValueError(f"Ja existe equipamento com ID {novo['ID']}.")
    for campo, validos in VALORES_VALIDOS.items():
        if campo in novo and novo[campo] not in validos and novo[campo] != "":
            raise ValueError(f"{campo} deve ser um de {validos}.")
    registros.append(novo)
    return novo


def consultar(registros, campo, valor):
    """Busca sequencial simples por qualquer campo (O(n))."""
    valor = str(valor).lower()
    return [r for r in registros if str(r.get(campo, "")).lower() == valor]


def remover(registros, id_equip):
    for i, r in enumerate(registros):
        if r["ID"] == id_equip:
            return registros.pop(i)
    return None


def atualizar(registros, id_equip, campo, valor):
    for r in registros:
        if r["ID"] == id_equip:
            r[campo] = valor
            return r
    return None


# ------------------------------------------------------------------ relatorios
def resumo(registros):
    """Contagens por classe e por setor - usado no menu e no relatorio."""
    por_classe, por_setor = {}, {}
    for r in registros:
        por_classe[r[ALVO]] = por_classe.get(r[ALVO], 0) + 1
        por_setor[r["Setor"]] = por_setor.get(r["Setor"], 0) + 1
    return por_classe, por_setor


def tabela(registros, limite=None):
    """Devolve a base formatada em texto."""
    linhas = [f"{'ID':<7}{'Nome':<16}{'Setor':<16}{'Valor':>11}  "
              f"{'Idade':<14}{'Uso':<10}{'Desemp.':<8}{'Estado':<9}{'Decisao'}"]
    linhas.append("-" * 110)
    for r in (registros[:limite] if limite else registros):
        linhas.append(
            f"{r['ID']:<7}{r['Nome']:<16}{r['Setor']:<16}"
            f"{r['Valor']:>11,.2f}  {r['Idade']:<14}{r['Uso']:<10}"
            f"{r['Desempenho']:<8}{r['Estado']:<9}{r['Decisao']}"
        )
    if limite and len(registros) > limite:
        linhas.append(f"... (+{len(registros) - limite} registros)")
    return "\n".join(linhas)
