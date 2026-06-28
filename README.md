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
- VRP com multiplas rotas e evolucao conjunta da frota;
- representacao genetica de rotas;
- operadores de crossover, mutacao, selecao por fitness e elitismo;
- fitness com distancia, prioridade, atraso, capacidade e autonomia;
- camada LLM testavel para relatorios, instrucoes e perguntas sobre rotas;
- experimentos comparativos em VRP com artefatos em `artifacts/`;
- leitura de entregas e veiculos via CSV;
- visualizacao 2D das rotas, com fundo simplificado do Brasil para o dataset de capitais;
- relatorio tecnico e roteiro de demonstracao consolidados;
- CLI configuravel;
- testes automatizados.

Entrega final consolidada:

- relatorio tecnico em `reports/final_report.md`;
- roteiro de demonstracao em `docs/video_script.md`;
- manifesto de artefatos em `artifacts/final/manifest.md`.

Experimentos disponíveis em VRP:

- `python -m src.metrics`: executa `pop50`, `pop100`, `pop100_no_elitism`, `pop500` e `pop500_no_elitism` em modo VRP, gera tabelas e graficos.

## Estrutura

- `src/`: implementacao principal
- `tests/`: testes unitarios
- `references/`: baseline e documentacao tecnica de apoio
- `docs/`: contexto do projeto e roteiro das sprints
- `data/`: datasets de exemplo
- `config/`: configuracoes de experimentos

## Dados de Exemplo

- `data/deliveries_sample.csv`: entregas sintéticas usadas no demo atual
- `data/brazil_capitals_sample.csv`: capitais brasileiras posicionadas em 2D para simulação visual com fundo do Brasil

## Requisitos

- Python 3.12
- `pygame`
- `matplotlib`
- `numpy`
- `pytest`

Instalar dependencias principais:

```bash
.venv/bin/pip install -r requirements.txt
```

Dependencias opcionais para chamada real da OpenAI:

```bash
.venv/bin/pip install -r requirements-llm.txt
```

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
- `--elite-size <n>`: define quantos melhores individuos sao preservados entre geracoes. Padrao: `1`.
- `--fps <n>`: define a taxa de quadros da animacao. Padrao: `30`.
- `--deliveries-file <path>`: define o CSV de entregas. Padrao: `data/deliveries_sample.csv`.
- `--vehicles-file <path>`: define o CSV de veiculos. Padrao: `data/vehicles_sample.csv`.

Exemplo:

```bash
.venv/bin/python -m src.main --vehicle-id 3 --population-size 200 --mutation-probability 0.3 --elite-size 2 --fps 15
```

Exemplo com multiplos veiculos:

```bash
.venv/bin/python -m src.main --mode vrp --vehicle-ids 1 3 5 --deliveries-file data/brazil_capitals_sample.csv --population-size 100 --mutation-probability 0.3 --elite-size 2 --fps 15
```

Se `--vehicle-ids` nao for informado no modo `vrp`, todos os veiculos de `data/vehicles_sample.csv` sao usados.

## Execucao da Camada LLM

A camada LLM pode ser executada sem chave de API. Nesse modo, o sistema otimiza uma rota/frota e gera uma resposta textual deterministica.

Gerar relatorio operacional VRP:

```bash
.venv/bin/python -m src.llm --mode vrp --output report --deliveries-file data/brazil_capitals_sample.csv --generations 80 --population-size 80
```

Gerar instrucoes para motoristas:

```bash
.venv/bin/python -m src.llm --mode vrp --output instructions --vehicle-ids 1 3 5 --deliveries-file data/brazil_capitals_sample.csv
```

Responder uma pergunta sobre a rota:

```bash
.venv/bin/python -m src.llm --mode tsp --output question --question "Qual e o fitness da rota?" --deliveries-file data/brazil_capitals_sample.csv --vehicle-id 3
```

Opcoes principais:

- `--mode <tsp|vrp>`: escolhe se a solucao textual sera gerada para uma rota unica ou frota.
- `--output <report|instructions|question>`: define o tipo de texto gerado.
- `--question <texto>`: pergunta usada com `--output question`.
- `--generations <n>`: numero de geracoes antes de gerar o texto. Padrao: `80`.
- `--population-size <n>`: tamanho da populacao. Padrao: `80`.
- `--seed <n>`: semente para reproducibilidade. Padrao: `7`.

Essa execucao usa o fallback offline da Sprint 7. A integracao real com OpenAI pode ser feita depois injetando um cliente LLM compatível com `complete(messages)`.

Para usar OpenAI de verdade, instale as dependencias opcionais e configure a chave:

```bash
.venv/bin/pip install -r requirements-llm.txt
export OPENAI_API_KEY="sua-chave"
```

Depois execute com `--provider openai`:

```bash
.venv/bin/python -m src.llm --provider openai --model gpt-4o-mini --mode vrp --output report --deliveries-file data/brazil_capitals_sample.csv
```

Se existir um arquivo `.env` com `OPENAI_API_KEY=...`, ele sera carregado automaticamente quando `python-dotenv` estiver instalado.

Fechar a janela:

- pressione `q`, ou
- feche a janela do Pygame

Executar os testes:

```bash
.venv/bin/pytest
```

## Documentacao

- `docs/project_context.md`: contexto do projeto
- `docs/architecture.md`: arquitetura atual e evolucao futura
- `docs/prompts.md`: definicao das sprints
- `docs/report_outline.md`: estrutura sugerida do relatorio tecnico
- `docs/sprint3_priorities.md`: prioridades e penalizacao por atraso HIGH
- `docs/sprint4_capacity.md`: peso e capacidade maxima do veiculo
- `docs/sprint5_autonomy.md`: distancia maxima e penalizacao por autonomia
- `docs/sprint6_vrp.md`: VRP com multiplos veiculos e evolucao conjunta da frota
- `docs/sprint7_llm.md`: camada LLM baseada em `references/agent-llm.py`
- `docs/sprint8_experiments.md`: experimentos comparativos em VRP e artefatos da Sprint 8
- `docs/sprint9_consolidation.md`: consolidacao final, comandos e evidencias
- `src/metrics/`: experimentos comparativos e graficos da Sprint 8
- `docs/brazil_capitals_map.md`: mapeamento das capitais brasileiras em 2D
- `docs/video_script.md`: roteiro do video de demonstracao
- `references/docs/architecture.md`: arquitetura do baseline TSP
- `references/docs/extension_plan.md`: analise da Sprint 1 e plano de extensao

## Observacoes

- O entrypoint atual esta em `src/main.py`.
- A visualizacao em `src/main.py` usa o solver migrado da Sprint 2 como base de execucao.
- Evolucoes futuras naturais incluem operadores VRP mais especializados, dados reais e malha viaria real.
