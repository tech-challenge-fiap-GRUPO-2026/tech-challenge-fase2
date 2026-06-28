# Introdução

Este relatorio descreve o desenvolvimento do Projeto 2 do Tech Challenge Fase 2: um sistema de otimizacao de rotas medicas para distribuicao de medicamentos e insumos.

O projeto parte de um codigo base de TSP e evolui para um resolvedor em `src/` com Algoritmo Genetico, restricoes operacionais, visualizacao e testes automatizados.

Estado atual: TSP com prioridades, capacidade e autonomia implementado, VRP com multiplos veiculos e evolucao conjunta da frota, e Sprint 7 de LLM finalizada. Comparativos experimentais ainda estao planejados.

# Fundamentação Teórica

## Algoritmos Genéticos

Algoritmos Geneticos sao metodos de otimizacao inspirados em processos evolutivos. Uma populacao de solucoes candidatas e avaliada por uma funcao fitness, e novas geracoes sao criadas por operadores como selecao, crossover, mutacao e elitismo.

Neste projeto, cada individuo representa uma rota no TSP ou uma frota completa no VRP. A qualidade da solucao e avaliada por distancia total e penalidades ligadas ao contexto logistico medico.

## Problema do Caixeiro Viajante

O Problema do Caixeiro Viajante, ou TSP, busca encontrar a menor rota que visita todos os pontos uma unica vez e retorna ao ponto inicial.

No contexto do projeto, os pontos representam entregas de medicamentos e insumos. O deposito representa o ponto de partida da rota.

## Vehicle Routing Problem

O Vehicle Routing Problem, ou VRP, generaliza o TSP para multiplos veiculos e multiplas rotas.

O VRP e um requisito do enunciado e foi implementado com um cromossomo de frota. O modulo `src/routing/vrp.py` evolui distribuicao e ordem das entregas em conjunto, permitindo mover e trocar entregas entre veiculos durante a evolucao genetica.

## Large Language Models

Large Language Models podem transformar dados operacionais em explicacoes, instrucoes e relatorios em linguagem natural.

No Projeto 2, a LLM deve gerar instrucoes para motoristas, relatorios de eficiencia e respostas sobre rotas. A Sprint 7 implementou uma camada LLM testavel em `src/llm/`, usando `references/agent-llm.py` como referencia tecnica de mensagens e function calling.

# Metodologia

O projeto foi conduzido em sprints incrementais:

1. Analise do codigo base e plano de extensao.
2. Migracao do TSP para `src/` com dataclasses, type hints e testes.
3. Inclusao de prioridades e penalizacao por atraso.
4. Inclusao de peso e capacidade maxima dos veiculos.
5. Inclusao de autonomia maxima dos veiculos.
6. Inclusao de VRP com multiplas rotas e evolucao conjunta da frota.
7. Inclusao de camada LLM para relatorios, instrucoes e perguntas sobre rotas.

A validacao foi feita com testes automatizados usando `pytest`.

# Implementação

## Estrutura

- `src/ga/genetic_algorithm.py`: algoritmo genetico e fitness.
- `src/routing/tsp.py`: adaptacao do algoritmo para TSP.
- `src/routing/vrp.py`: otimizacao de frota com multiplas rotas.
- `src/models/`: modelos de entrega, prioridade, cidade e veiculo.
- `src/data_loader.py`: leitura dos arquivos CSV.
- `src/visualization/`: desenho da rota e grafico de fitness.
- `src/llm/`: prompts, relatorios, instrucoes e explicacoes sobre rotas.
- `src/main.py`: CLI e demo visual.
- `tests/`: testes automatizados.

## Fitness

O fitness atual e:

```text
fitness = distancia_total
        + penalidade_de_atraso
        + penalidade_de_capacidade
        + penalidade_de_autonomia
```

As penalidades sao:

- atraso `HIGH`: `100.0` por unidade de atraso;
- atraso `MEDIUM`: `30.0` por unidade de atraso;
- atraso `LOW`: `10.0` por unidade de atraso;
- excesso de capacidade: `25.0` por unidade acima do limite;
- excesso de autonomia: `25.0` por unidade acima do limite.

## Dados

O projeto possui datasets de exemplo:

- `data/deliveries_sample.csv`: entregas sinteticas;
- `data/brazil_capitals_sample.csv`: capitais brasileiras em plano 2D;
- `data/vehicles_sample.csv`: veiculos com capacidade e autonomia.

## Execucao

Exemplo:

```bash
.venv/bin/python -m src.main --deliveries-file data/brazil_capitals_sample.csv --vehicle-id 3 --population-size 200 --mutation-probability 0.3 --elite-size 2 --fps 15
```

Exemplo VRP:

```bash
.venv/bin/python -m src.main --mode vrp --deliveries-file data/brazil_capitals_sample.csv --population-size 100 --mutation-probability 0.3 --elite-size 2 --fps 15
```

Para restringir a frota do VRP, use `--vehicle-ids`:

```bash
.venv/bin/python -m src.main --mode vrp --vehicle-ids 1 3 5 --deliveries-file data/brazil_capitals_sample.csv --population-size 100 --mutation-probability 0.3 --elite-size 2 --fps 15
```

## VRP

O VRP atual cria uma solucao de frota, com uma rota por veiculo, e evolui essa solucao como um individuo completo.

O processo e:

1. criar uma populacao inicial de frotas completas;
2. avaliar cada frota pelo fitness agregado;
3. aplicar crossover entre solucoes de frota;
4. aplicar mutacoes que podem mover, trocar ou reordenar entregas;
5. manter as melhores frotas por elitismo.

Essa abordagem permite otimizar distribuicao e ordem das rotas em conjunto.

A visualizacao do modo VRP anima a evolucao geracional, desenha uma rota por veiculo com cores diferentes, revela o tracado progressivamente e exibe o historico agregado de fitness da frota. Quando o dataset de capitais brasileiras e usado, a tela tambem exibe um fundo simplificado do mapa do Brasil.

## LLM

A camada LLM monta contexto textual a partir de `TSPSolution` ou `VRPSolution`.

Ela permite:

1. gerar relatorio operacional;
2. gerar instrucoes para motoristas;
3. responder perguntas sobre rotas.

Sem cliente externo, a camada retorna respostas deterministicas. Com cliente injetado ou `--provider openai`, ela envia mensagens com prompt de sistema e prompt do usuario ao provedor LLM.

Exemplo de execucao:

```bash
.venv/bin/python -m src.llm --mode vrp --output report --deliveries-file data/brazil_capitals_sample.csv
```

Exemplo com OpenAI:

```bash
.venv/bin/python -m src.llm --provider openai --model gpt-4o-mini --mode vrp --output report --deliveries-file data/brazil_capitals_sample.csv
```

# Experimentos

A Sprint 8 foi concluida com um runner em `src/metrics/` e comparacao das configuracoes `pop50`, `pop100`, `pop100_no_elitism`, `pop500` e `pop500_no_elitism` em modo VRP.

Artefatos gerados:

- `artifacts/experiments/sprint8_summary.csv`
- `artifacts/experiments/sprint8_summary.md`
- `artifacts/experiments/sprint8_summary.json`
- `artifacts/charts/fitness_curves.png`
- `artifacts/charts/final_fitness.png`
- `artifacts/charts/execution_time.png`

Resultado de referencia no dataset de entregas sinteticas:

| Configuracao | Fitness final | Convergencia | Tempo | Melhoria |
| --- | ---: | ---: | ---: | ---: |
| pop50 | 0.16 | 103 | 1.323s | 0.40 |
| pop100 | 0.16 | 187 | 2.588s | 0.40 |
| pop100_no_elitism | 0.16 | 176 | 2.639s | 0.40 |
| pop500 | 0.16 | 33 | 13.404s | 0.35 |
| pop500_no_elitism | 0.16 | 33 | 13.425s | 0.35 |

As cinco configuracoes atingiram o mesmo fitness final no smoke test VRP. O cenario `pop100_no_elitism` convergiu um pouco antes que o `pop100` com elitismo, enquanto `pop500_no_elitism` manteve a mesma convergencia do `pop500` com tempo levemente maior. O `pop50` entregou o melhor equilibrio entre convergencia e tempo.

# Resultados

Resultado atual validado:

- TSP funcional com visualizacao;
- VRP com multiplas rotas e evolucao conjunta da frota;
- fitness com distancia, atraso, capacidade e autonomia;
- leitura de entregas e veiculos via CSV;
- camada LLM testavel para relatorios, instrucoes e perguntas;
- experimento comparativo em VRP com cinco configuracoes, incluindo elitismo desligado;
- comparacao de convergencia entre cinco cenarios VRP;
- CLI configuravel;
- suite de testes automatizados passando.

Ultima validacao conhecida:

```text
62 passed
```

# Trabalhos Futuros

Prioridades para aderencia completa ao enunciado:

1. Refinar operadores geneticos do VRP para preservar melhor agrupamentos geograficos.
2. Integrar cliente OpenAI concreto se a demonstracao exigir chamada real.
3. Completar video de demonstracao.

# Referências

- Documento do Tech Challenge Fase 2.
- Codigo base em `references/`.
- Documentacao interna em `docs/`.
