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
- Explicar que a solucao atual resolve TSP com restricoes e possui modo VRP com multiplos veiculos.

## 3. Algoritmo Genetico

Tempo sugerido: 3 minutos.

Conteudo:

- Mostrar `src/ga/genetic_algorithm.py`.
- Explicar representacao da rota como permutacao.
- Explicar que, no VRP, o individuo representa uma frota completa.
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
- Explicar que, com o dataset de capitais, a tela exibe um fundo simplificado do Brasil.
- Executar:

```bash
.venv/bin/python -m src.main --deliveries-file data/brazil_capitals_sample.csv --vehicle-id 3 --population-size 100 --mutation-probability 0.3 --elite-size 2 --fps 15
```

- Mostrar a rota e o grafico de fitness em execucao.
- Executar tambem o modo VRP:

```bash
.venv/bin/python -m src.main --mode vrp --vehicle-ids 1 3 5 --deliveries-file data/brazil_capitals_sample.csv --population-size 100 --mutation-probability 0.3 --elite-size 2 --fps 15
```

- Mostrar a evolucao do fitness agregado e o tracado progressivo das rotas por veiculo com cores diferentes.
- Explicar que o VRP evolui distribuicao e ordem das entregas em conjunto.

## 6. Testes

Tempo sugerido: 1 minuto.

Conteudo:

- Executar:

```bash
.venv/bin/python -m pytest
```

- Mostrar a suite passando.

## 7. LLM e Experimentos

Tempo sugerido: 2 minutos.

Conteudo:

- Executar a LLM offline:

```bash
.venv/bin/python -m src.llm --mode vrp --output report --deliveries-file data/brazil_capitals_sample.csv
```

- Mostrar o relatorio textual gerado para a frota.
- Mostrar `artifacts/experiments/sprint8_summary.md`.
- Mostrar `artifacts/charts/fitness_curves.png`, `final_fitness.png` e `execution_time.png`.
- Explicar que os experimentos foram executados em modo VRP com cinco configuracoes.

## 8. Encerramento

Tempo sugerido: 30 segundos.

Conteudo:

- Reforcar que o projeto ja cobre TSP, VRP com frota, restricoes principais e visualizacao.
- Reforcar que a entrega tambem cobre LLM, experimentos, relatorio final e artefatos de demonstracao.
- Indicar como evolucao futura o uso de malha viaria real e operadores VRP mais especializados.
