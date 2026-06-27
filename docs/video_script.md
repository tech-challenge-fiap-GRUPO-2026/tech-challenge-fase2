# Roteiro do Video de Demonstracao

Duracao alvo: ate 15 minutos.

## 1. Abertura

Tempo sugerido: 1 minuto.

Conteudo:

- Apresentar o Tech Challenge Fase 2.
- Informar que o projeto escolhido foi o Projeto 2.
- Explicar o problema: otimizar rotas de entrega de medicamentos e insumos.

## 2. Visao Geral da Solucao

Tempo sugerido: 2 minutos.

Conteudo:

- Mostrar a estrutura do repositorio.
- Explicar `src/`, `tests/`, `data/`, `docs/`, `config/` e `reports/`.
- Explicar que a solucao atual resolve TSP com restricoes e possui modo VRP inicial.

## 3. Algoritmo Genetico

Tempo sugerido: 3 minutos.

Conteudo:

- Mostrar `src/ga/genetic_algorithm.py`.
- Explicar representacao da rota como permutacao.
- Explicar populacao, crossover, mutacao e elitismo.
- Explicar que o objetivo e minimizar o fitness.

## 4. Fitness e Restricoes

Tempo sugerido: 3 minutos.

Conteudo:

- Mostrar o calculo de fitness.
- Explicar distancia da rota fechada.
- Explicar penalidade por atraso e prioridade.
- Explicar penalidade por capacidade.
- Explicar penalidade por autonomia.

## 5. Dados e Visualizacao

Tempo sugerido: 3 minutos.

Conteudo:

- Mostrar `data/deliveries_sample.csv`.
- Mostrar `data/brazil_capitals_sample.csv`.
- Mostrar `data/vehicles_sample.csv`.
- Executar:

```bash
.venv/bin/python -m src.main --deliveries-file data/brazil_capitals_sample.csv --vehicle-id 3 --population-size 100 --mutation-probability 0.3 --fps 15
```

- Mostrar a rota e o grafico de fitness em execucao.
- Executar tambem o modo VRP:

```bash
.venv/bin/python -m src.main --mode vrp --vehicle-ids 1 3 5 --deliveries-file data/brazil_capitals_sample.csv --population-size 100 --mutation-probability 0.3 --fps 15
```

- Mostrar a evolucao do fitness agregado e o tracado progressivo das rotas por veiculo com cores diferentes.

## 6. Testes

Tempo sugerido: 1 minuto.

Conteudo:

- Executar:

```bash
.venv/bin/python -m pytest
```

- Mostrar a suite passando.

## 7. Proximos Passos

Tempo sugerido: 2 minutos.

Conteudo:

- Explicar o que ainda falta para aderencia completa:
- LLM para instrucoes e relatorios.
- Experimentos comparativos.
- Relatorio final completo.

## 8. Encerramento

Tempo sugerido: 30 segundos.

Conteudo:

- Reforcar que o projeto ja cobre TSP, VRP inicial, restricoes principais e visualizacao.
- Indicar que a evolucao natural e LLM + experimentos.
