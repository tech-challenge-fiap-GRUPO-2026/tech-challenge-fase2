# Sprint 6 - VRP

## Objetivo

Expandir o TSP para um VRP com multiplos veiculos e evolucao conjunta da frota.

## Modelo

O modulo `src/routing/vrp.py` adiciona:

- `VRPProblem`: entregas, veiculos e deposito opcional;
- `VRPRoute`: rota resolvida para um veiculo;
- `VRPSolution`: conjunto de rotas e fitness total.

## Estrategia de Otimizacao

O VRP agora usa um cromossomo de frota.

Cada individuo representa:

- quais entregas ficam em cada veiculo;
- a ordem de visita dentro de cada rota.

Exemplo conceitual:

```text
Veiculo 1: A -> C -> F
Veiculo 2: B -> D
Veiculo 3: E -> G -> H
```

A populacao inicial combina:

- uma solucao heuristica ordenada por prioridade, prazo e capacidade;
- solucoes aleatorias de frota para gerar diversidade.

As entregas da solucao heuristica sao ordenadas por:

- prioridade;
- `due_time`;
- `id`.

Depois sao alocadas nos veiculos tentando respeitar `max_capacity`.

Durante a evolucao genetica, o VRP pode mudar tanto a ordem das entregas quanto a distribuicao entre veiculos.

## Operadores Geneticos

O crossover combina a sequencia global de entregas de dois individuos e reaproveita uma divisao de rotas de um dos pais.

A mutacao pode:

- mover uma entrega de um veiculo para outro;
- trocar entregas entre dois veiculos;
- alterar a ordem dentro de uma rota.

## Fitness Agregado

Cada rota de veiculo e avaliada com:

- entregas alocadas ao veiculo;
- mesmo deposito;
- capacidade e autonomia do proprio veiculo.

O fitness total da frota e:

```text
total_fitness = soma_do_fitness_de_todas_as_rotas
```

## Limitacoes

- A evolucao conjunta da frota ja existe, mas ainda usa operadores simples.
- O crossover de frota ainda pode ser refinado para preservar melhor agrupamentos geograficos.
- A visualizacao segue em 2D abstrato, sem malha viaria real.
- A visualizacao VRP usa `iterate_vrp` para animar a evolucao por geracao.

## Execucao Visual

O demo visual aceita o modo VRP:

```bash
.venv/bin/python -m src.main --mode vrp --deliveries-file data/brazil_capitals_sample.csv --population-size 100 --mutation-probability 0.3 --fps 15
```

No modo `vrp`, o sistema usa todos os veiculos do arquivo definido por `--vehicles-file`.

Para selecionar uma frota especifica:

```bash
.venv/bin/python -m src.main --mode vrp --vehicle-ids 1 3 5 --deliveries-file data/brazil_capitals_sample.csv --population-size 100 --mutation-probability 0.3 --fps 15
```

A cada geracao, o demo redesenha:

- fitness agregado da frota;
- rota atual de cada veiculo;
- uma cor diferente por veiculo;
- trecho visivel progressivo de cada rota, evitando exibir todas as rotas completas no primeiro frame.

## Testes

Os testes cobrem:

- alocacao de todas as entregas;
- erro quando nao ha veiculos;
- uma rota por veiculo;
- fitness agregado;
- penalidade de capacidade por rota;
- parsing do modo VRP na CLI;
- selecao padrao e customizada de veiculos no VRP;
- historico agregado de fitness da frota;
- estados geracionais do VRP;
- populacao inicial de frota preservando cada entrega uma unica vez;
- mutacao de frota alterando distribuicao/rotas sem perder entregas.
