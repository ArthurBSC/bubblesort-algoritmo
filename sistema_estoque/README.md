# Sistema de Estoque: Complexidade de Algoritmos (Projeto N1)

Sistema de estoque por **código de produto**, guardado em uma **lista linear sequencial ordenada**
(um vetor de tamanho fixo mais `n`, como nos slides "Listas Ordenadas"). Usa só a biblioteca padrão
do Python (3.8 ou mais recente), sem instalar nada.

> **O que é n no projeto:** n é a quantidade de produtos cadastrados no estoque.

## Como executar

```bash
python web.py         # interface web (abre o navegador sozinho) - use esta na apresentação
```
```bash
python main.py        # o mesmo sistema, em menu de terminal
```
```bash
python testes.py      # testes automatizados (17 testes)
```
```bash
python relatorio.py   # gera o relatório de desempenho da Etapa 5 (leva uns 40 s)
```

A tela web e o menu de terminal usam **exatamente os mesmos algoritmos**: a interface só desenha o
vetor e mostra os contadores. Para parar o servidor web, aperte Ctrl + C no terminal.

## Arquivos × etapas

| Arquivo | Etapa | Conteúdo |
|---|---|---|
| `lista_ordenada.py` | 3 | `inserir_ordenado` (localiza a posição, desloca e insere) e `remover` (busca binária + desloca "para trás") |
| `ordenacao.py` | **4** | `bubble_sort` (versão dos slides, Exercício 5) e `bubble_sort_otimizado` (Exercício 6) |
| `buscas.py` | **5** | `busca_linear` e `busca_binaria`, com a função de custo de cada uma |
| `relatorio.py` | **5** | experimentos com n = 10 até 100.000; gera o relatório em `relatorio/` |
| `contador.py` | 2 | conta operações pelo modelo da aula: comparação = 1, atribuição = 2, op. matemática = 3 |
| `web.py` + `interface.html` | | tela web: desenha o vetor e anima cada comparação |
| `main.py` | | menu do sistema no terminal (Exercício de fixação dos slides) |
| `testes.py` | 3–5 | os 3 testes obrigatórios de inserção, Bubble Sort, buscas e conferência das fórmulas |

## Tela web

Mostra o vetor com os índices em cima, como nos slides. Ao buscar, ela **anima** o algoritmo:
laranja é o elemento sendo verificado, azul é a faixa que a busca binária ainda considera,
verde é o elemento encontrado. Cada ação exibe as operações contadas e o custo T(n).

As ações que exigem lista ordenada (inserção ordenada, busca binária) ficam bloqueadas com um aviso
enquanto a lista estiver desordenada — é uma forma de mostrar na apresentação *por que* a
ordenação precisa vir antes.

## Menu de terminal

1. Cadastrar produto (inserção ordenada)
2. Remover produto
3. Buscar produto com Busca Binária
4. Buscar produto com Busca Linear
5. Comparar Busca Linear × Binária (mesmo código, lado a lado)
6. Listar o estoque
7. Gerar estoque grande desordenado e ordenar com Bubble Sort
8. Gerar o relatório de desempenho (Etapa 5)

Ao iniciar, o sistema carrega 10 produtos **fora de ordem** (na mesma ordem do exercício dos slides:
10, 9, 8, 5, 4, 3, 2, 1, 7, 6) e mostra o Bubble Sort passada por passada.

## Resumo das complexidades

| Algoritmo | Melhor caso | Pior caso | Função de custo (pior caso) |
|---|---|---|---|
| Inserção ordenada | O(1) (inserir no final) | O(n) (inserir no início) | até n deslocamentos |
| Bubble Sort (básico) | O(n²) | O(n²) | (n−1)² comparações |
| Bubble Sort (otimizado) | O(n) (já ordenada) | O(n²) (decrescente) | n(n−1)/2 comparações |
| Busca Linear | O(1) | O(n) | T(n) = 7n + 3 |
| Busca Binária | O(1) | O(log n) | T(k) = 16k + 8, k = ⌊log₂ n⌋ + 1 |

**Resultado da Etapa 5:** a Busca Binária teve o melhor desempenho. Veja `relatorio/relatorio_desempenho.md`.
