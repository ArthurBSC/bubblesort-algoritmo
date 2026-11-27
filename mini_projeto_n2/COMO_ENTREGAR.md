# Guia de entrega — onde cada exigência do enunciado está atendida

## 1. O que foi adaptado do projeto N1

| Projeto N1 (`../sistema_estoque`) | Mini projeto N2 (`mini_projeto_n2/`) |
|---|---|
| Estoque de produtos em vetor | Parque de equipamentos de TI em lista de dicionários + CSV |
| Bubble Sort (Etapa 4) | Virou **linha de base O(n²)** contra Heap, Quick e Merge Sort |
| Busca linear × binária (Etapa 5) | Virou **busca em grafos**: BFS, DFS e Dijkstra |
| Contador de operações (`contador.py`) | Mantido e reaproveitado em `modulos/contador.py` |
| Relatório de desempenho | Ampliado: 5 volumes × 3 cenários + 4 gráficos |
| — | **Novo**: classificação por Entropia, Ganho de Informação e ID3 |

O tema escolhido é o 10 da lista do enunciado (*Sistema de Gestão e Análise de
Equipamentos de TI*): classificar equipamentos, ordenar inventários e identificar
caminhos de conexão entre dispositivos.

## 2. Requisitos técnicos obrigatórios (item 6 do enunciado)

| Requisito | Exigência | Onde está |
|---|---|---|
| Linguagem | Livre | Python 3.8+ |
| Base de dados | Mínimo 50 registros | `dados/base_dados.csv` — **60 registros** |
| Estrutura de dados | Listas, dicionários, vetores ou matrizes | Lista de dicionários + lista de adjacência |
| Classificação | Entropia, Ganho e ID3 | `modulos/entropia.py`, `modulos/classificacao_id3.py` |
| Busca | BFS e DFS | `modulos/busca_bfs.py`, `modulos/busca_dfs.py` |
| Caminho mínimo | Dijkstra | `modulos/dijkstra.py` |
| Ordenação | Heap, Quick e Merge Sort | `modulos/heap_sort.py`, `quick_sort.py`, `merge_sort.py` |
| Análise | Notação Big O | Seção 10 do documento + opção 5 do menu do Módulo 5 |
| Testes | Diferentes volumes | 100, 500, 1.000, 5.000 e 10.000 registros |
| Resultados | Tabelas, gráficos e comparações | `relatorio/` (4 PNG + 3 CSV + relatório .md) |

**Restrição atendida:** nenhum `sort()`/`sorted()` dentro dos algoritmos, nenhuma
biblioteca de grafos ou de machine learning. `matplotlib` só desenha os gráficos.
A única estrutura pronta usada dentro de um algoritmo é o `heapq` na fila de
prioridade do Dijkstra — o heap do Heap Sort foi feito à mão.

## 3. Os cinco módulos (item 4)

| Módulo | Entregue em |
|---|---|
| 1 — Pesquisa e base de dados | `modulos/manipulacao_dados.py`, `dados/`, menu 1 |
| 2 — Entropia e ID3 | `modulos/entropia.py` + `classificacao_id3.py`, menu 2 |
| 3 — BFS, DFS e Dijkstra | `modulos/grafo.py` + os 3 algoritmos, menu 3 |
| 4 — Heap, Quick e Merge Sort | `modulos/*_sort.py`, menu 4 |
| 5 — Análise e relatório | `experimentos/`, menu 5 |

## 4. Documentação obrigatória (item 8)

As 12 seções exigidas estão em `documentos/Trabalho_ABNT_MiniProjeto_N2.docx`
(20 páginas, ABNT): 1 Introdução, 2 Justificativa, 3 Objetivos, 4 Metodologia,
5 Estrutura da base, 6 Implementação dos algoritmos, 7 Resultados da classificação,
8 Resultados das buscas, 9 Resultados das ordenações, 10 Análise de complexidade
(com as 8 perguntas do Módulo 5 respondidas), 11 Conclusão e 12 Referências.

## 5. Apresentação (item 9)

`documentos/Apresentacao_MiniProjeto_N2.pptx` — 24 slides divididos exatamente na
cronometragem exigida: 3 min problema · 4 min base e entropia · 4 min buscas ·
4 min ordenação · 3 min resultados.

## 6. Antes de entregar

1. Abra `documentos/Trabalho_ABNT_MiniProjeto_N2.docx` e substitua os campos entre
   colchetes: nome, instituição, curso, professor, cidade e ano. Faça o mesmo no
   slide de capa do `.pptx`.
2. Confira a formatação exigida pelo seu professor (algumas instituições pedem
   sumário e numeração de páginas a partir da introdução).
3. Rode `python testes.py` antes da apresentação: os 45 testes devem passar.
4. Se quiser números novos (outra máquina), rode `python experimentos/resultados.py`
   e depois **regere** os dois arquivos:
   `python documentos/gerar_documento_abnt.py` e `python documentos/gerar_slides.py`.
   Os textos leem os CSVs, então as tabelas e as frases se atualizam sozinhas.
5. O professor pode pedir para explicar um trecho de código ou alterar dados de
   entrada ao vivo: use o menu 1 (inserir registro) e depois o menu 2 (reconstruir
   a árvore) para mostrar o sistema reagindo.
