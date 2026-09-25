"""
Interface web do Sistema de Estoque.

Sobe um servidor local e abre a página no navegador. A página é só a tela:
toda a lógica (inserção ordenada, Bubble Sort, busca linear e binária) continua
nos módulos lista_ordenada.py, ordenacao.py e buscas.py, que são os mesmos
usados pelo main.py e pelos testes.

Executar:   python web.py
Depois abra:  http://localhost:8000
Para parar:   Ctrl + C
"""

import json
import os
import random
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from buscas import busca_binaria, busca_linear
from contador import Contador
from lista_ordenada import ListaProdutos, Produto
from ordenacao import bubble_sort, bubble_sort_otimizado

PORTA = 8000
PASTA = os.path.dirname(os.path.abspath(__file__))
LIMITE_PASSOS = 3000  # acima disso não devolvemos a animação, só os números

PRODUTOS_INICIAIS = [
    (100, "Teclado", 15), (90, "Mouse", 40), (80, 'Monitor 24"', 8),
    (50, "Cabo HDMI", 60), (40, "Webcam", 12), (30, "Headset", 20),
    (20, "Pen drive 32GB", 75), (10, "Mousepad", 90),
    (70, "SSD 480GB", 18), (60, "Hub USB", 25),
]

estado = {"lista": None, "ordenada": False}
trava = threading.Lock()


def reiniciar():
    lista = ListaProdutos(50)
    lista.carregar([Produto(c, n, q) for c, n, q in PRODUTOS_INICIAIS])
    estado["lista"] = lista
    estado["ordenada"] = False


def contador_para_json(c):
    return {
        "n_passos": c.n_passos,
        "comparacoes": c.comparacoes,
        "comp_elementos": c.comp_elementos,
        "atribuicoes": c.atribuicoes,
        "matematicas": c.matematicas,
        "trocas": c.trocas,
        "deslocamentos": c.deslocamentos,
        "custo": c.custo_total(),
        "passos": c.passos if len(c.passos) <= LIMITE_PASSOS else [],
        "passos_omitidos": len(c.passos) > LIMITE_PASSOS,
    }


def estado_para_json(msg="", tipo="info", c=None, extra=None):
    lista = estado["lista"]
    resposta = {
        "produtos": [{"codigo": lista.v[i].codigo, "nome": lista.v[i].nome,
                      "quantidade": lista.v[i].quantidade} for i in range(lista.n)],
        "n": lista.n,
        "max": lista.max,
        "ordenada": estado["ordenada"] and lista.esta_ordenada(),
        "mensagem": msg,
        "tipo": tipo,
    }
    if c is not None:
        resposta["contador"] = contador_para_json(c)
    if extra:
        resposta.update(extra)
    return resposta


# ---------------------------------------------------------------------------
# Ações
# ---------------------------------------------------------------------------
def acao_estado(_):
    return estado_para_json()


def acao_reiniciar(_):
    reiniciar()
    return estado_para_json("Estoque recarregado fora de ordem. Use o Bubble Sort para ordenar.",
                            "aviso")


def acao_inserir(dados):
    lista = estado["lista"]
    if not estado["ordenada"] or not lista.esta_ordenada():
        return estado_para_json("A inserção ordenada exige a lista ordenada. "
                                "Ordene com o Bubble Sort primeiro.", "erro")
    codigo = int(dados["codigo"])
    if busca_binaria(lista.v, lista.n, codigo) != -1:
        return estado_para_json(f"Já existe um produto com o código {codigo}.", "erro")
    c = Contador()
    try:
        pos = lista.inserir_ordenado(Produto(codigo, dados.get("nome") or f"Produto {codigo}",
                                             int(dados.get("quantidade") or 0)), c)
    except OverflowError as e:
        return estado_para_json(str(e), "erro")

    if c.deslocamentos == 0:
        cenario = "melhor cenário: inserido no final, nenhum deslocamento"
    elif pos == 0:
        cenario = f"pior cenário: inserido no início, {c.deslocamentos} deslocamentos"
    else:
        cenario = f"cenário intermediário: inserido no meio, {c.deslocamentos} deslocamentos"
    return estado_para_json(f"Produto {codigo} inserido na posição {pos} ({cenario}).",
                            "ok", c, {"destaque": [pos]})


def acao_remover(dados):
    lista = estado["lista"]
    codigo = int(dados["codigo"])
    c = Contador()
    p = lista.remover(codigo, c)
    if p is None:
        return estado_para_json(f"Código {codigo} não encontrado.", "erro", c)
    return estado_para_json(f"Removido: {p.codigo} - {p.nome}. "
                            f"{c.deslocamentos} elemento(s) deslocado(s) para trás.", "ok", c)


def acao_buscar(dados):
    lista = estado["lista"]
    codigo = int(dados["codigo"])
    tipo = dados.get("tipo", "binaria")
    if tipo == "binaria" and not (estado["ordenada"] and lista.esta_ordenada()):
        return estado_para_json("A Busca Binária exige a lista ordenada. "
                                "Ordene com o Bubble Sort primeiro.", "erro")

    funcao = busca_linear if tipo == "linear" else busca_binaria
    nome = "Busca Linear" if tipo == "linear" else "Busca Binária"
    c = Contador()
    pos = funcao(lista.v, lista.n, codigo, c)
    if pos == -1:
        msg = f"{nome}: código {codigo} não encontrado após {c.n_passos} passo(s)."
        tipo_msg = "aviso"
    else:
        msg = (f"{nome}: {lista.v[pos].nome} encontrado na posição {pos} "
               f"após {c.n_passos} passo(s).")
        tipo_msg = "ok"
    return estado_para_json(msg, tipo_msg, c, {"destaque": [pos] if pos >= 0 else [],
                                               "animar": tipo})


def acao_comparar(dados):
    lista = estado["lista"]
    if not (estado["ordenada"] and lista.esta_ordenada()):
        return estado_para_json("Para comparar as duas buscas a lista precisa estar ordenada.",
                                "erro")
    codigo = int(dados["codigo"])
    cl, cb = Contador(), Contador()
    pl = busca_linear(lista.v, lista.n, codigo, cl)
    pb = busca_binaria(lista.v, lista.n, codigo, cb)
    return estado_para_json(
        f"Comparação para o código {codigo}: "
        f"Linear {cl.n_passos} passo(s) x Binária {cb.n_passos}.",
        "ok", None,
        {"comparacao": {
            "linear": {"posicao": pl, **contador_para_json(cl)},
            "binaria": {"posicao": pb, **contador_para_json(cb)},
        }})


def acao_ordenar(dados):
    lista = estado["lista"]
    versao = dados.get("versao", "otimizada")
    c = Contador(gravar_passos=lista.n <= 60)
    inicio = time.perf_counter()
    if versao == "basica":
        bubble_sort(lista.v, lista.n, c)
    else:
        bubble_sort_otimizado(lista.v, lista.n, c)
    ms = (time.perf_counter() - inicio) * 1000
    estado["ordenada"] = True
    nome = "básica" if versao == "basica" else "otimizada"
    return estado_para_json(
        f"Bubble Sort ({nome}): {c.comp_elementos} comparações entre elementos, "
        f"{c.trocas} trocas, custo T(n) = {c.custo_total()}, em {ms:.2f} ms.", "ok", c)


def acao_desordenar(dados):
    n = max(2, min(int(dados.get("n") or 10), 50))
    codigos = [(i + 1) * 10 for i in range(n)]
    nomes = ["Teclado", "Mouse", "Monitor", "Cabo HDMI", "Webcam", "Headset", "Pen drive",
             "Mousepad", "SSD", "Hub USB", "Impressora", "Roteador", "Notebook", "Estabilizador"]
    random.shuffle(codigos)
    lista = ListaProdutos(max(50, n))
    lista.carregar([Produto(cod, f"{nomes[i % len(nomes)]} {cod}", random.randint(1, 99))
                    for i, cod in enumerate(codigos)])
    estado["lista"] = lista
    estado["ordenada"] = False
    return estado_para_json(f"Gerados {n} produtos em ordem aleatória. "
                            "Agora ordene com o Bubble Sort.", "aviso")


ACOES = {
    "estado": acao_estado, "reiniciar": acao_reiniciar, "inserir": acao_inserir,
    "remover": acao_remover, "buscar": acao_buscar, "comparar": acao_comparar,
    "ordenar": acao_ordenar, "desordenar": acao_desordenar,
}


# ---------------------------------------------------------------------------
# Servidor
# ---------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # não polui o terminal

    def _enviar(self, codigo, corpo, tipo="application/json; charset=utf-8"):
        dados = corpo if isinstance(corpo, bytes) else corpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        caminho = self.path.split("?")[0]
        if caminho in ("/", "/index.html"):
            try:
                with open(os.path.join(PASTA, "interface.html"), encoding="utf-8") as f:
                    return self._enviar(200, f.read(), "text/html; charset=utf-8")
            except FileNotFoundError:
                return self._enviar(500, "interface.html não encontrado", "text/plain; charset=utf-8")
        if caminho == "/relatorio":
            arq = os.path.join(PASTA, "relatorio", "relatorio_desempenho.html")
            if os.path.exists(arq):
                with open(arq, encoding="utf-8") as f:
                    return self._enviar(200, f.read(), "text/html; charset=utf-8")
            return self._enviar(404, "<p>Relatório ainda não gerado. Rode: python relatorio.py</p>",
                                "text/html; charset=utf-8")
        self._enviar(404, "Não encontrado", "text/plain; charset=utf-8")

    def do_POST(self):
        if self.path != "/api":
            return self._enviar(404, json.dumps({"erro": "rota inválida"}))
        tamanho = int(self.headers.get("Content-Length") or 0)
        try:
            dados = json.loads(self.rfile.read(tamanho) or "{}")
        except json.JSONDecodeError:
            return self._enviar(400, json.dumps({"erro": "JSON inválido"}))

        acao = ACOES.get(dados.get("acao"))
        if acao is None:
            return self._enviar(400, json.dumps({"erro": "ação desconhecida"}))
        try:
            with trava:
                resposta = acao(dados)
        except (ValueError, KeyError, TypeError) as e:
            resposta = estado_para_json(f"Dado inválido: {e}", "erro")
        self._enviar(200, json.dumps(resposta, ensure_ascii=False))


def main():
    reiniciar()
    servidor = ThreadingHTTPServer(("127.0.0.1", PORTA), Handler)
    url = f"http://localhost:{PORTA}"
    print("-" * 60)
    print("  SISTEMA DE ESTOQUE - interface web")
    print(f"  Abra no navegador: {url}")
    print("  Para parar o servidor: Ctrl + C")
    print("-" * 60)
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor encerrado.")
        servidor.server_close()


if __name__ == "__main__":
    main()
