# Arquitetura

## Escopo

Este projeto implementa o Projeto 2 do Tech Challenge Fase 2: otimizacao de rotas para distribuicao de medicamentos e insumos usando Algoritmos Geneticos.

O estado atual cobre TSP com restricoes de prioridade, capacidade e autonomia, VRP com multiplos veiculos e evolucao conjunta da frota, alem de uma camada LLM testavel para relatorios, instrucoes e perguntas sobre rotas.

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
- fundo simplificado do Brasil quando o CSV de capitais e usado;
- no modo TSP, melhor rota atual e rota secundaria da populacao;
- no modo VRP, a evolucao geracional da frota com uma rota por veiculo em cores diferentes e tracado progressivo.

O argumento `--fps` controla a velocidade da animacao.

### Camada LLM

`references/agent-llm.py` foi usado como referencia para a Sprint 7.

O arquivo demonstra:

- uso de OpenAI com `dotenv`;
- historico de mensagens;
- function calling;
- execucao de funcoes locais chamadas pela LLM;
- interface Streamlit.

No projeto principal, a camada LLM fica em `src/llm/` e gera instrucoes, relatorios e respostas sobre rotas. O dominio financeiro do exemplo nao foi reaproveitado.

Arquivos principais:

- `src/llm/prompts.py`: contexto da solucao e prompts reutilizaveis;
- `src/llm/report_generator.py`: relatorio operacional e instrucoes para motoristas;
- `src/llm/route_explainer.py`: respostas e explicacoes sobre rotas.
- `src/llm/openai_client.py`: cliente OpenAI opcional;
- `src/llm/__main__.py`: execucao via `python -m src.llm`.

A integracao com provedor externo e opcional por cliente injetado ou `--provider openai`, o que permite testes sem internet ou `OPENAI_API_KEY`.

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
- `--elite-size`
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
- prompts e respostas offline da camada LLM.

## Limitacoes Atuais

- Distancias sao euclidianas em 2D, nao por malha viaria real.
- O VRP atual otimiza a frota em conjunto, mas ainda usa operadores geneticos simples e distancia euclidiana.
- A camada LLM possui fallback deterministico e cliente OpenAI opcional em `src/llm/openai_client.py`.
- Os modulos de metricas e experimentos ainda estao pendentes.
- A visualizacao usa um fundo simplificado do Brasil para o dataset de capitais, mas nao usa mapa geografico real nem malha viaria.

## Evolucao Planejada

1. Executar experimentos com `config/pop50.yaml`, `config/pop100.yaml` e `config/pop500.yaml`.
2. Refinar operadores geneticos do VRP para preservar melhor agrupamentos geograficos.
3. Integrar cliente OpenAI concreto se a demonstracao exigir chamada real.
4. Gerar artefatos comparativos e atualizar `reports/final_report.md` com os resultados.
5. Preparar o video de demonstracao.
