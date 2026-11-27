# Mini Projeto N2 — Sistema Inteligente de Gestão e Análise de Equipamentos de TI

Desafio Integrador de Complexidade de Algoritmos. O sistema recebe, armazena, manipula,
**classifica** (ID3), **busca** (BFS, DFS, Dijkstra) e **ordena** (Heap, Quick, Merge) dados
de um parque de equipamentos de TI, medindo o custo computacional de cada estratégia.

Continuidade do projeto N1 (`../sistema_estoque`): o Bubble Sort daquele trabalho foi mantido
como **linha de base O(n²)** para dimensionar o ganho dos algoritmos O(n log n).

## Como executar

```bash
python main.py
```
```bash
python testes.py
```
```bash
python experimentos/resultados.py
```

`main.py` abre o menu com os cinco módulos. `testes.py` roda 45 testes automatizados.
`experimentos/resultados.py` refaz todos os experimentos, gera os 4 gráficos PNG e o
relatório técnico em `relatorio/` (leva cerca de 30 s).

Requisitos: Python 3.8+. Apenas `matplotlib` é externo, e só para os gráficos —
todos os algoritmos usam exclusivamente a biblioteca padrão.

## Estrutura

```
mini_projeto_n2/
├── main.py                      menu integrado dos 5 módulos
├── testes.py                    45 testes automatizados
├── dados/
│   ├── base_dados.csv           60 registros (mínimo exigido: 50)
│   └── gerar_base.py            script que gerou a base simulada
├── modulos/
│   ├── manipulacao_dados.py     MÓDULO 1 — CRUD + CSV
│   ├── entropia.py              MÓDULO 2 — entropia e ganho de informação
│   ├── classificacao_id3.py     MÓDULO 2 — árvore de decisão ID3
│   ├── grafo.py                 MÓDULO 3 — lista de adjacência
│   ├── busca_bfs.py             MÓDULO 3 — BFS
│   ├── busca_dfs.py             MÓDULO 3 — DFS
│   ├── dijkstra.py              MÓDULO 3 — Dijkstra
│   ├── heap_sort.py             MÓDULO 4 — Heap Sort
│   ├── quick_sort.py            MÓDULO 4 — Quick Sort (pivô fixo e mediana de 3)
│   ├── merge_sort.py            MÓDULO 4 — Merge Sort
│   ├── bubble_sort.py           linha de base vinda do N1
│   └── contador.py              contagem de comparações e movimentações
├── experimentos/
│   ├── testes_ordenacao.py      5 volumes × 3 cenários × 5 algoritmos
│   ├── testes_busca.py          rede real + grafos de 100 a 10.000 vértices
│   ├── testes_classificacao.py  entropia, árvore, validação 70/30
│   └── resultados.py            gráficos + relatório técnico
├── relatorio/
│   ├── relatorio_tecnico.md     resultados consolidados
│   ├── resultados_*.csv         dados brutos dos experimentos
│   └── grafico_*.png            4 gráficos comparativos
└── documentos/
    ├── Trabalho_ABNT_MiniProjeto_N2.docx    trabalho escrito (ABNT, 20 páginas)
    ├── Apresentacao_MiniProjeto_N2.pptx     slides (24, cronometrados)
    ├── gerar_documento_abnt.py              gera o .docx a partir dos CSVs
    └── gerar_slides.py                      gera o .pptx a partir dos CSVs
```

Os dois documentos leem os resultados de `relatorio/`: se os experimentos forem
refeitos, basta regerá-los para que todas as tabelas e números se atualizem.
Ver `COMO_ENTREGAR.md` para o mapa de cada exigência do enunciado.

## Base de dados

60 equipamentos, 11 atributos. Atributos categóricos usados pelo ID3:
`Idade` (Novo/Intermediario/Antigo), `Uso` (Leve/Moderado/Intenso),
`Desempenho` (Alto/Medio/Baixo) e `Estado` (Bom/Regular/Ruim).
Variável alvo: `Decisao` ∈ {Manter, Manutencao, Substituir}.
Atributos numéricos usados na ordenação: `Valor` (R$) e `IdadeAnos`.

## Principais resultados

| Medida | Resultado |
|---|---|
| Entropia da base, H(S) | 1,5546 bits |
| Maior ganho de informação | `Estado` = 0,9533 bits (raiz da árvore) |
| Árvore gerada | 13 nós, 9 folhas, profundidade 4 |
| Acurácia em registros não vistos (70/30) | 100% (18/18) |
| Caminho CPD → SalaReunioes (BFS) | 2 arestas, custo 16 |
| Caminho CPD → SalaReunioes (Dijkstra) | 4 arestas, custo 12 |
| Ordenação mais rápida com n = 10.000 aleatório | Quick Sort (pivô fixo) |
| Ordenação mais estável nos 3 cenários | Merge Sort |
| Pior caso observado | Quick Sort com pivô fixo e dados ordenados: 49.995.000 comparações |

## Complexidades

| Algoritmo | Melhor | Médio | Pior | Espaço |
|---|---|---|---|---|
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| Quick Sort (pivô fixo) | O(n log n) | O(n log n) | **O(n²)** | O(log n) |
| Quick Sort (mediana de 3) | O(n log n) | O(n log n) | O(n²) raro | O(log n) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Bubble Sort (N1) | O(n) | O(n²) | O(n²) | O(1) |
| BFS / DFS | O(V+E) | O(V+E) | O(V+E) | O(V) |
| Dijkstra (heap) | O((V+E) log V) | idem | idem | O(V) |
| ID3 (treino) | O(a·n·v) | — | — | O(nós) |
