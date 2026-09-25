# Relatório de Complexidade — Busca Linear x Busca Binária
Sistema de Estoque — Complexidade de Algoritmos — Etapa 5

## 1. Objetivo

Identificar qual das estruturas de busca implementadas no Sistema de Estoque — Busca Linear ou Busca Binária — obteve melhor desempenho, relacionando o tamanho da entrada (n = quantidade de produtos cadastrados) com a quantidade de operações realizadas e com o tempo de execução. Como a Busca Binária só funciona em lista ordenada, também foi analisado o custo do Bubble Sort (Etapa 4).

## 2. Metodologia

Para cada n ∈ {10, 100, 1.000, 10.000, 100.000} foi criada uma lista ordenada de produtos com códigos 10, 20, 30, ... Em cada lista foram medidos três cenários: melhor caso (Linear: 1º elemento; Binária: elemento do meio), pior caso (código inexistente, maior que todos) e caso médio (média de 1.000 buscas por códigos existentes sorteados).

Foram contados os passos de cada busca — na Busca Linear, cada elemento examinado; na Busca Binária, cada divisão da lista ao meio — que é a contagem usada nos exemplos da atividade ("foram necessárias 6 verificações", "busca binária: 3 passos de comparação"). Também foi calculado o custo T(n) pelo modelo da aula: comparação = 1, atribuição = 2, operação matemática = 3; nesse custo a Busca Binária pesa mais por passo, pois faz duas comparações (igualdade e maior/menor) e o cálculo do meio. O tempo foi medido com time.perf_counter(), sem a contagem de operações, e depende da máquina; por isso a análise principal usa a contagem.

Ambiente: Python 3.14.4 — Windows 11 — semente aleatória 2026 — gerado em 25/09/2026 10:19.

## 3. Funções de custo

Busca Linear — pior caso (percorre os n elementos e não encontra): 1 atribuição (i = 0) + (n + 1) testes do laço + n comparações com o código + n somas + n atribuições (i = i + 1). T(n) = 2 + (n + 1) + n + 3n + 2n = 7n + 3 → O(n).

Busca Binária — pior caso (k passagens pelo laço, k = ⌊log₂ n⌋ + 1): inicialização (2 atribuições + 1 subtração) = 7; por passagem: 1 teste do laço + cálculo do meio (2 operações + 1 atribuição = 8) + 2 comparações + atualização de ini/fim (1 operação + 1 atribuição = 5) = 16; mais o teste final = 1. T(k) = 16k + 8 → O(log n).

## 4. Resultados — passos de cada busca

A Busca Linear cresce na mesma proporção de n: multiplicar n por 10 multiplica os passos por 10, porque no pior caso ela examina os n elementos. A Busca Binária cresce muito devagar: multiplicar n por 10 acrescenta só cerca de 3 passos (log₂ 10 ≈ 3,3), porque cada passo descarta metade do que restou.

| n | Linear melhor | Linear médio | Linear pior | Binária melhor | Binária médio | Binária pior |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 1 | 5,6 | 10 | 1 | 2,9 | 4 |
| 100 | 1 | 50,1 | 100 | 1 | 5,8 | 7 |
| 1.000 | 1 | 497,1 | 1.000 | 1 | 8,9 | 10 |
| 10.000 | 1 | 5.059,4 | 10.000 | 1 | 12,3 | 14 |
| 100.000 | 1 | 48.638,0 | 100.000 | 1 | 15,7 | 17 |

## 5. Resultados — custo T(n) no pior caso

Os valores medidos pelo contador coincidem com as fórmulas T(n) = 7n + 3 (Linear) e T(k) = 16k + 8 (Binária), onde k é o número de passos da tabela anterior, k = ⌊log₂ n⌋ + 1. Isso confirma o modelo matemático construído na seção 3.

| n | Linear medido | Linear 7n+3 | Binária medido | Binária 16k+8 |
|---:|---:|---:|---:|---:|
| 10 | 73 | 73 | 72 | 72 |
| 100 | 703 | 703 | 120 | 120 |
| 1.000 | 7.003 | 7.003 | 168 | 168 |
| 10.000 | 70.003 | 70.003 | 232 | 232 |
| 100.000 | 700.003 | 700.003 | 280 | 280 |

## 6. Resultados — tempo médio real por busca (µs)

Com poucos elementos a diferença é pequena, pois a Linear faz menos trabalho por passo. Conforme n cresce, o tempo da Linear sobe proporcionalmente (×10 a cada ×10 em n) e o da Binária aumenta só um pouco a cada ×10 em n.

| n | Linear (µs) | Binária (µs) | Binária mais rápida |
|---:|---:|---:|---:|
| 10 | 1,59 | 1,99 | 0,8x |
| 100 | 16,70 | 3,83 | 4,4x |
| 1.000 | 162,68 | 5,76 | 28,2x |
| 10.000 | 1.612,72 | 9,38 | 171,9x |
| 100.000 | 14.659,00 | 12,37 | 1.185,3x |

## 7. Bubble Sort (Etapa 4) — custo de ordenar

Versão básica (slides, Exercício 5): sempre (n − 1) passadas completas → (n − 1)² comparações em qualquer cenário, O(n²). Versão otimizada (Exercício 6): diminui o fim a cada passada e para quando uma passada não faz trocas → melhor caso n − 1 comparações, O(n); pior caso n(n − 1)/2 comparações e trocas, O(n²). Para n = 10.000, pelas fórmulas, a versão básica faria (n − 1)² = 99.980.001 comparações e a otimizada no pior caso n(n − 1)/2 = 49.995.000 (rode com --completo para medir).

| Versão | Cenário | n | Comparações | Trocas | Custo T(n) | Tempo (ms) |
|:---|:---|---:|---:|---:|---:|---:|
| Básica | Melhor (já ordenada) | 10 | 81 | 0 | 651 | 0,05 |
| Otimizada | Melhor (já ordenada) | 10 | 9 | 0 | 82 | 0,01 |
| Básica | Médio (aleatória) | 10 | 81 | 28 | 819 | 0,05 |
| Otimizada | Médio (aleatória) | 10 | 45 | 28 | 657 | 0,05 |
| Básica | Pior (decrescente) | 10 | 81 | 45 | 921 | 0,05 |
| Otimizada | Pior (decrescente) | 10 | 45 | 45 | 793 | 0,05 |
| Básica | Melhor (já ordenada) | 100 | 9.801 | 0 | 69.501 | 4,61 |
| Otimizada | Melhor (já ordenada) | 100 | 99 | 0 | 712 | 0,07 |
| Básica | Médio (aleatória) | 100 | 9.801 | 2.371 | 83.727 | 5,14 |
| Otimizada | Médio (aleatória) | 100 | 4.905 | 2.371 | 54.301 | 5,85 |
| Básica | Pior (decrescente) | 100 | 9.801 | 4.950 | 99.201 | 5,77 |
| Otimizada | Pior (decrescente) | 100 | 4.950 | 4.950 | 75.358 | 5,91 |
| Básica | Melhor (já ordenada) | 1.000 | 998.001 | 0 | 6.995.001 | 509,26 |
| Otimizada | Melhor (já ordenada) | 1.000 | 999 | 0 | 7.012 | 0,81 |
| Básica | Médio (aleatória) | 1.000 | 998.001 | 253.453 | 8.515.719 | 602,70 |
| Otimizada | Médio (aleatória) | 1.000 | 499.149 | 253.453 | 5.532.378 | 782,42 |
| Básica | Pior (decrescente) | 1.000 | 998.001 | 499.500 | 9.992.001 | 679,20 |
| Otimizada | Pior (decrescente) | 1.000 | 499.500 | 499.500 | 7.503.508 | 688,91 |

## 8. Vale a pena ordenar para usar a Busca Binária?

Se a lista chegar desordenada, a Binária exige ordenar antes. Ordenar é um custo único; cada busca depois economiza (comparações da Linear − comparações da Binária). O número mínimo de buscas m para compensar é: m > custo de ordenar ÷ economia por busca. No Sistema de Estoque isso é ainda mais favorável, pois a Inserção Ordenada (Etapa 3) mantém a lista sempre ordenada e o Bubble Sort só é necessário uma vez, ao importar dados desordenados.

| n | Comparações p/ ordenar (Bubble otimizado, médio) | Linear: comparações (médio) | Binária: comparações (médio) | Buscas para compensar |
|---:|---:|---:|---:|---:|
| 10 | 45 | 5,6 | 4,7 | 49 |
| 100 | 4.905 | 50,1 | 10,7 | 125 |
| 1.000 | 499.149 | 497,1 | 16,9 | 1.040 |

## 9. Conclusão

A Busca Binária obteve o melhor desempenho. Com n = 100.000 produtos, ela precisou em média de 15,7 passos contra 48.638,0 da Linear (≈ 3.096 vezes menos) e foi ≈ 1.185 vezes mais rápida no tempo medido. No pior caso a Linear precisou examinar os 100.000 elementos e a Binária resolveu em apenas 17 passos.

Isso acontece porque a Busca Linear é O(n): quando a quantidade de produtos aumenta, o trabalho cresce na mesma proporção. Já a Busca Binária é O(log n): a cada passo ela descarta metade dos elementos restantes, então dobrar a quantidade de produtos acrescenta apenas uma passagem pelo laço.

A condição para usar a Binária é a lista estar ordenada. Ordenar com Bubble Sort custa O(n²) e, pela seção 8, só se paga depois de aproximadamente n buscas (≈ n²/2 comparações para ordenar ÷ ≈ n/2 economizadas por busca). Por isso o projeto mantém a lista sempre ordenada com a Inserção Ordenada (Etapa 3): o Bubble Sort é usado apenas uma vez, ao carregar dados desordenados, e a partir daí todas as buscas aproveitam o O(log n). A Busca Linear só é preferível quando a lista está desordenada e serão feitas poucas buscas (menos que n).
