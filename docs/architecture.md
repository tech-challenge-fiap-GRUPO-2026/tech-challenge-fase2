# Arquitetura

## Escopo

Este projeto implementa o Projeto 2 do Tech Challenge Fase 2: otimizacao de rotas para distribuicao de medicamentos e insumos usando Algoritmos Geneticos.

O estado atual cobre TSP com restricoes de prioridade, capacidade e autonomia. VRP com multiplos veiculos e LLM ainda estao planejados.

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
TSPProblem
        |
        v
Algoritmo Genetico
        |
        v
Melhor rota + historico de fitness
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

### Visualizacao

`src/main.py` executa o demo visual com Pygame.

A tela mostra:

- grafico de fitness;
- deposito;
- pontos de entrega;
- melhor rota atual;
- rota secundaria da populacao.

O argumento `--fps` controla a velocidade da animacao.

### CLI

Comando principal:

```bash
.venv/bin/python -m src.main
```

Opcoes:

- `--vehicle-id`
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
- integracao basica do TSP.

## Limitacoes Atuais

- Distancias sao euclidianas em 2D, nao por malha viaria real.
- O sistema ainda resolve uma rota principal por vez, nao VRP completo.
- A camada LLM ainda nao esta implementada.
- Os modulos de metricas e experimentos ainda estao pendentes.
- A visualizacao nao usa mapa geografico real.

## Evolucao Planejada

1. Implementar VRP em `src/routing/vrp.py`.
2. Implementar geracao de relatorios e instrucoes em `src/llm/`.
3. Executar experimentos com `config/pop50.yaml`, `config/pop100.yaml` e `config/pop500.yaml`.
4. Gerar artefatos comparativos e completar `reports/final_report.md`.
5. Preparar o video de demonstracao.
