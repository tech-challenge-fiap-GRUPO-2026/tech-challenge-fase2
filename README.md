# Tech Challenge - Fase 2

Sistema de otimizacao de rotas medicas com Algoritmos Geneticos.

## Visao geral

O projeto esta sendo construido em sprints. O baseline atual migra o resolvedor de TSP da pasta `references/` para `src/`, com:

- algoritmo genetico para TSP;
- visualizacao com Pygame;
- grafico de fitness com Matplotlib;
- testes unitarios com `pytest`.

## Estrutura

- `src/`: implementacao principal
- `tests/`: testes unitarios
- `references/`: baseline e documentacao tecnica de apoio
- `docs/`: contexto do projeto e roteiro das sprints
- `data/`: datasets de exemplo
- `config/`: configuracoes de experimentos

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
- `--population-size <n>`: define o tamanho da populacao do algoritmo genetico. Padrao: `100`.
- `--mutation-probability <p>`: define a probabilidade de mutacao. Padrao: `0.5`.
- `--deliveries-file <path>`: define o CSV de entregas. Padrao: `data/deliveries_sample.csv`.
- `--vehicles-file <path>`: define o CSV de veiculos. Padrao: `data/vehicles_sample.csv`.

Exemplo:

```bash
.venv/bin/python -m src.main --vehicle-id 3 --population-size 200 --mutation-probability 0.3
```

Fechar a janela:

- pressione `q`, ou
- feche a janela do Pygame

Executar os testes:

```bash
.venv/bin/pytest
```

## Documentacao

- `docs/project_context.md`: contexto do projeto
- `docs/prompts.md`: definicao das sprints
- `docs/sprint3_priorities.md`: prioridades e penalizacao por atraso HIGH
- `docs/sprint4_capacity.md`: peso e capacidade maxima do veiculo
- `references/docs/architecture.md`: arquitetura do baseline TSP
- `references/docs/extension_plan.md`: analise da Sprint 1 e plano de extensao

## Observacoes

- O entrypoint atual esta em `src/main.py`.
- A visualizacao em `src/main.py` usa o solver migrado da Sprint 2 como base de execucao.
- O projeto ainda evolui para VRP, prioridades, capacidade, autonomia e LLM nas proximas sprints.
