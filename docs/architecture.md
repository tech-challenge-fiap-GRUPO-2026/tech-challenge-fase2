# Arquitetura

## Escopo

Este projeto implementa o Projeto 2 do Tech Challenge Fase 2: otimizacao de rotas para distribuicao de medicamentos e insumos usando Algoritmos Geneticos.

O estado atual cobre TSP com restricoes de prioridade, capacidade e autonomia, alem de um VRP inicial com multiplas rotas por veiculo. A camada LLM ainda esta planejada.

## Visao Geral

Fluxo principal:

```text
CSV de entregas + CSV de veiculos
        |
        v
src/data_loader.py
        |
        v
Delivery / Vehicle
        |
        v
TSPProblem / VRPProblem
        |
        v
Algoritmo Genetico
        |
        v
Melhor rota ou rotas por veiculo + historico de fitness
        |
        v
Visualizacao Pygame + grafico Matplotlib
```

## Componentes

### Entrada de Dados

`src/data_loader.py` carrega:

- `data/deliveries_sample.csv`
- `data/brazil_capitals_sample.csv`
- `data/vehicles_sample.csv`

As entregas possuem:

- `delivery_id`
- `latitude`
- `longitude`
- `priority`
- `weight`
- `due_time`

Os veiculos possuem:

- `vehicle_id`
- `max_capacity`
- `max_distance`

### Modelos

`src/models/delivery.py` define:

- `City`: ponto base ou deposito;
- `Delivery`: ponto de entrega com prioridade, peso e prazo.

`src/models/vehicle.py` define:

- `Vehicle`: capacidade maxima e autonomia maxima.

`src/models/priority.py` define:

- `HIGH`
- `MEDIUM`
- `LOW`

### Algoritmo Genetico

`src/ga/genetic_algorithm.py` contem:

- geracao de populacao inicial;
- calculo de distancia;
- calculo de fitness;
- crossover por ordem;
- mutacao por troca adjacente;
- ordenacao por fitness;
- execucao por geracoes.

A rota e representada como uma permutacao dos pontos de entrega. Quando ha deposito, ele e mantido como ponto fixo inicial.

### Fitness

O fitness e minimizado:

```text
fitness = distancia_total
        + penalidade_de_atraso
        + penalidade_de_capacidade
        + penalidade_de_autonomia
```

Penalidades atuais:

- atraso `HIGH`: `100.0` por unidade de atraso;
- atraso `MEDIUM`: `30.0` por unidade de atraso;
- atraso `LOW`: `10.0` por unidade de atraso;
- excesso de capacidade: `25.0` por unidade acima de `max_capacity`;
- excesso de autonomia: `25.0` por unidade acima de `max_distance`.

### Roteamento

`src/routing/tsp.py` adapta o algoritmo genetico para o problema TSP.

Ele recebe:

- entregas;
- deposito opcional;
- veiculo opcional.

Quando o veiculo existe, `max_capacity` e `max_distance` sao usados no fitness.

`src/routing/vrp.py` expande o fluxo para multiplos veiculos.

Ele fornece:

- `VRPProblem`: entregas, veiculos e deposito;
- `VRPRoute`: rota resolvida para um veiculo;
- `VRPSolution`: conjunto de rotas e fitness agregado;
- `distribute_deliveries`: heuristica usada para uma solucao inicial;
- `generate_fleet_population`: populacao de solucoes completas de frota;
- `fleet_crossover`: crossover para cromossomos de frota;
- `mutate_fleet`: mutacoes que podem mover/trocar entregas entre veiculos;
- `iterate_vrp`: evolucao geracional da frota completa.

### Visualizacao

`src/main.py` executa o demo visual com Pygame.

A tela mostra:

- grafico de fitness;
- deposito;
- pontos de entrega;
- no modo TSP, melhor rota atual e rota secundaria da populacao;
- no modo VRP, a evolucao geracional da frota com uma rota por veiculo em cores diferentes e tracado progressivo.

O argumento `--fps` controla a velocidade da animacao.

### CLI

Comando principal:

```bash
.venv/bin/python -m src.main
```

Opcoes:

- `--vehicle-id`
- `--vehicle-ids`
- `--mode`
- `--population-size`
- `--mutation-probability`
- `--fps`
- `--deliveries-file`
- `--vehicles-file`

## Testes

Os testes cobrem:

- distancia euclidiana;
- fitness de rota fechada;
- populacao inicial;
- crossover;
- mutacao;
- historico de fitness;
- prioridade e atraso;
- capacidade;
- autonomia;
- leitura de CSV;
- parsing da CLI;
- modo visual VRP;
- selecao de frota por CLI;
- integracao basica do TSP;
- distribuicao VRP;
- fitness agregado de frota.

## Limitacoes Atuais

- Distancias sao euclidianas em 2D, nao por malha viaria real.
- O VRP atual otimiza a frota em conjunto, mas ainda usa operadores geneticos simples e distancia euclidiana.
- A camada LLM ainda nao esta implementada.
- Os modulos de metricas e experimentos ainda estao pendentes.
- A visualizacao nao usa mapa geografico real.

## Evolucao Planejada

1. Implementar geracao de relatorios e instrucoes em `src/llm/`.
2. Executar experimentos com `config/pop50.yaml`, `config/pop100.yaml` e `config/pop500.yaml`.
3. Evoluir o VRP para otimizar a frota inteira de forma conjunta.
4. Gerar artefatos comparativos e completar `reports/final_report.md`.
5. Preparar o video de demonstracao.
