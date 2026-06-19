# Architecture

Base analisada: pasta `references/`.

## Visao geral

O projeto implementa um resolvedor de TSP com Algoritmo Genetico. A logica principal esta dividida em:

- `genetic_algorithm.py`: operadores geneticos e funcoes basicas.
- `tsp.py`: loop principal, visualizacao e evolucao da populacao.
- `draw_functions.py`: desenho do grafo, das rotas e do grafico de fitness.
- `benchmark_att48.py`: instancias de benchmark `att48`.
- `demo_crossover.py` e `demo_mutation.py`: validacao isolada dos operadores.

## Fluxo de execucao

1. O problema e inicializado com uma lista de cidades.
2. A populacao inicial e criada com rotas aleatorias validas.
3. Em cada geracao, o fitness de todos os individuos e calculado.
4. A populacao e ordenada da melhor rota para a pior.
5. O melhor individuo da geracao e registrado para analise e grafico.
6. Uma nova populacao e montada usando selecao, crossover, mutacao e elitismo.
7. No modo visual, a tela e redesenhada a cada ciclo com o melhor caminho e o historico do fitness.
8. O processo termina por criterio externo: limite de geracoes no demo ou fechamento da janela no modo interativo.

### Dois modos de uso

- `genetic_algorithm.py` possui um `__main__` com execucao em linha de comando e numero fixo de geracoes.
- `tsp.py` executa em tempo real com Pygame e roda ate o usuario encerrar a janela.

## Representacao do cromossomo

O cromossomo e uma permutacao das cidades.

- Cada gene e uma cidade representada por uma tupla `(x, y)`.
- Um individuo e uma lista ordenada dessas tuplas.
- A ordem dos genes define a rota percorrida.
- Nao ha repeticao de cidades dentro de um cromossomo.

Exemplo conceitual:

```text
[(470, 169), (602, 202), (754, 239), ...]
```

Como o TSP exige uma rota fechada, a ultima cidade conecta de volta a primeira.

## Populacao

A populacao e uma lista de rotas candidatas.

- A geracao inicial e produzida por `generate_random_population`.
- Cada individuo e criado com `random.sample`, garantindo uma permutacao valida.
- O tamanho da populacao e configuravel por constante.
- No loop principal, a populacao nova substitui a anterior ao final de cada geracao.

No `tsp.py`, o tamanho padrao e `100` individuos.

## Fitness

O fitness mede o custo total da rota.

- A distancia entre dois pontos e Euclidiana.
- O fitness soma a distancia entre cidades consecutivas.
- A soma e ciclica: o ultimo gene retorna ao primeiro.
- Menor fitness significa melhor solucao.

Formula implementada:

```text
fitness = sum(dist(path[i], path[(i + 1) mod n]) for i in range(n))
```

## Selecao

Ha duas variantes nos arquivos de referencia.

### Em `tsp.py`

A selecao e por roleta ponderada inversa ao fitness:

- individuos com menor distancia recebem maior peso;
- o peso e calculado como `1 / fitness`;
- a amostragem usa `random.choices(..., weights=...)`;
- dois pais sao escolhidos a cada iteracao.

### Em `genetic_algorithm.py`

O demo usa selecao simples entre os 10 melhores individuos:

- `random.choices(population[:10], k=2)`;
- nao ha ponderacao por fitness dentro desse subconjunto;
- e uma estrategia mais simples e menos adaptativa que a usada em `tsp.py`.

## Crossover

O operador implementado e `order_crossover` (OX).

Etapas:

1. Escolhe um segmento aleatorio em `parent1`.
2. Copia esse segmento para o filho.
3. Percorre `parent2` na ordem original.
4. Insere no filho apenas genes ainda nao presentes.
5. Mantem a propriedade de permutacao valida.

Caracteristicas:

- preserva a ordem relativa dos genes restantes;
- evita duplicacao de cidades;
- e adequado para problemas de permutacao, como TSP.

Observacao importante:

- no demo e na implementacao de apoio, o crossover usa dois pais distintos;
- no `tsp.py`, o trecho atual chama `order_crossover(parent1, parent1)`, o que reduz o operador a uma recombinacao degenerada do proprio pai.

## Mutacao

O operador de mutacao faz uma troca local entre genes adjacentes.

Comportamento:

- copia a solucao antes de alterar;
- sorteia um numero aleatorio;
- se o evento de mutacao ocorrer, escolhe um indice valido;
- troca a cidade naquela posicao com a proxima.

Pontos relevantes:

- a mutacao nao e uma inversao de segmento completa, apesar do comentario no codigo;
- o efeito e uma perturbacao pequena e conservadora da rota;
- a probabilidade de mutacao e configuravel.

## Elitismo

Existe elitismo.

- O melhor individuo da populacao atual e copiado diretamente para a nova populacao.
- Isso evita perder a melhor solucao encontrada em uma geracao.
- O elitismo observado e simples, preservando apenas 1 individuo.

Trecho conceitual:

```text
new_population = [best_individual]
```

## Criterio de parada

O criterio de parada depende do ponto de execucao.

### `genetic_algorithm.py`

- execucao por numero fixo de geracoes;
- no demo, `N_GENERATIONS = 100`.

### `tsp.py`

- nao existe limite de geracoes aplicado ao loop principal;
- a execucao continua ate o usuario fechar a janela ou pressionar `q`;
- a constante `N_GENERATIONS` esta declarada, mas nao e usada no loop atual.

## Geracao de graficos

O modulo `draw_functions.py` integra Matplotlib e Pygame.

### Grafico de fitness

- `draw_plot` cria uma figura Matplotlib em modo `Agg`;
- plota geracoes no eixo `x` e fitness no eixo `y`;
- converte a figura para uma surface do Pygame;
- desenha o grafico no canto superior esquerdo da janela.

### Visualizacao da rota

- `draw_cities` desenha cada cidade como circulo;
- `draw_paths` desenha a rota como linha fechada;
- `tsp.py` exibe a melhor solucao em azul e uma solucao auxiliar em cinza;
- o historico do melhor fitness e atualizado a cada geracao.

## Benchmark

O benchmark principal fornecido nos arquivos de referencia e o `att48`.

### Fonte dos dados

- `benchmark_att48.py` contem as 48 coordenadas do problema;
- tambem contem a ordem conhecida da solucao de referencia;
- a origem citada no arquivo e o dataset classico de TSP da Florida State University.

### Uso previsto

No `tsp.py`, o benchmark aparece como configuracao comentada:

- as coordenadas sao escaladas para caber na janela;
- a solucao alvo e reconstruida a partir da ordem conhecida;
- o fitness da solucao de referencia pode ser calculado para comparacao.

### Outros cenarios de teste

- `default_problems` fornece instancias pequenas com 5, 10, 12 e 15 cidades;
- a geracao aleatoria de cidades e usada para experimentacao rapida;
- esses casos funcionam como benchmarks locais, mas nao ha um harness formal de medicao automatica.

## Resumo operacional

Em termos de arquitetura, o sistema segue este ciclo:

1. gerar uma populacao inicial valida;
2. calcular distancias totais;
3. ordenar por menor distancia;
4. preservar o melhor individuo;
5. selecionar pais;
6. aplicar crossover OX;
7. aplicar mutacao por swap adjacente;
8. repetir ate o fim da execucao.
