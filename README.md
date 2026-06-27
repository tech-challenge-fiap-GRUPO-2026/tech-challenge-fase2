# Tech Challenge - Fase 2

Sistema de otimizacao de rotas medicas com Algoritmos Geneticos.

## Visao geral

O projeto escolhido e o **Projeto 2: Otimizacao de Rotas para Distribuicao de Medicamentos e Insumos**.

O projeto esta sendo construido em sprints. O baseline atual migra o resolvedor de TSP da pasta `references/` para `src/`, com:

- algoritmo genetico para TSP;
- visualizacao com Pygame;
- grafico de fitness com Matplotlib;
- testes unitarios com `pytest`.

## Estado Atual

Implementado:

- TSP com Algoritmo Genetico;
- VRP inicial com multiplas rotas por veiculo;
- representacao genetica de rotas;
- operadores de crossover, mutacao, selecao por fitness e elitismo;
- fitness com distancia, prioridade, atraso, capacidade e autonomia;
- leitura de entregas e veiculos via CSV;
- visualizacao 2D das rotas;
- CLI configuravel;
- testes automatizados.

Ainda pendente para aderencia completa ao enunciado:

- camada LLM para instrucoes, relatorios e perguntas sobre rotas;
- experimentos comparativos com diferentes configuracoes;
- relatorio tecnico final completo;
- roteiro e gravacao do video de demonstracao.

## Estrutura

- `src/`: implementacao principal
- `tests/`: testes unitarios
- `references/`: baseline e documentacao tecnica de apoio
- `docs/`: contexto do projeto e roteiro das sprints
- `data/`: datasets de exemplo
- `config/`: configuracoes de experimentos

## Dados de Exemplo

- `data/deliveries_sample.csv`: entregas sintéticas usadas no demo atual
- `data/brazil_capitals_sample.csv`: capitais brasileiras posicionadas em 2D para simulação visual

## Requisitos

- Python 3.12
- `pygame`
- `matplotlib`
- `numpy`
- `pytest`

## Execucao

Executar a interface visual:

```bash
.venv/bin/python -m src.main
```

Opcoes disponiveis:

- `--vehicle-id <id>`: seleciona o veiculo de `data/vehicles_sample.csv` usado na simulacao. Padrao: primeiro veiculo do arquivo.
- `--vehicle-ids <id...>`: seleciona os veiculos usados no modo `vrp`. Padrao: todos os veiculos do arquivo.
- `--mode <tsp|vrp>`: define o modo da visualizacao. Padrao: `tsp`.
- `--population-size <n>`: define o tamanho da populacao do algoritmo genetico. Padrao: `100`.
- `--mutation-probability <p>`: define a probabilidade de mutacao. Padrao: `0.5`.
- `--fps <n>`: define a taxa de quadros da animacao. Padrao: `30`.
- `--deliveries-file <path>`: define o CSV de entregas. Padrao: `data/deliveries_sample.csv`.
- `--vehicles-file <path>`: define o CSV de veiculos. Padrao: `data/vehicles_sample.csv`.

Exemplo:

```bash
.venv/bin/python -m src.main --vehicle-id 3 --population-size 200 --mutation-probability 0.3 --fps 15
```

Exemplo com multiplos veiculos:

```bash
.venv/bin/python -m src.main --mode vrp --vehicle-ids 1 3 5 --deliveries-file data/brazil_capitals_sample.csv --population-size 100 --mutation-probability 0.3 --fps 15
```

Se `--vehicle-ids` nao for informado no modo `vrp`, todos os veiculos de `data/vehicles_sample.csv` sao usados.

Fechar a janela:

- pressione `q`, ou
- feche a janela do Pygame

Executar os testes:

```bash
.venv/bin/pytest
```

## Documentacao

- `docs/project_context.md`: contexto do projeto
- `docs/architecture.md`: arquitetura atual e componentes planejados
- `docs/prompts.md`: definicao das sprints
- `docs/report_outline.md`: estrutura sugerida do relatorio tecnico
- `docs/sprint3_priorities.md`: prioridades e penalizacao por atraso HIGH
- `docs/sprint4_capacity.md`: peso e capacidade maxima do veiculo
- `docs/sprint5_autonomy.md`: distancia maxima e penalizacao por autonomia
- `docs/sprint6_vrp.md`: VRP inicial com multiplos veiculos
- `docs/brazil_capitals_map.md`: mapeamento das capitais brasileiras em 2D
- `docs/video_script.md`: roteiro do video de demonstracao
- `references/docs/architecture.md`: arquitetura do baseline TSP
- `references/docs/extension_plan.md`: analise da Sprint 1 e plano de extensao

## Observacoes

- O entrypoint atual esta em `src/main.py`.
- A visualizacao em `src/main.py` usa o solver migrado da Sprint 2 como base de execucao.
- O projeto ainda evolui para LLM, experimentos e novas otimizacoes nas proximas sprints.
