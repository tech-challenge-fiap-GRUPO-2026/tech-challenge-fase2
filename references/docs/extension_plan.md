# Extension Plan

## Objetivo

Este documento registra a evolucao do baseline em `references/` para o Projeto 2 do Tech Challenge Fase 2: otimizacao de rotas para distribuicao de medicamentos e insumos com Algoritmos Geneticos e apoio futuro de LLM.

O projeto saiu de um TSP didatico e hoje possui uma implementacao em `src/` com restricoes de prioridade, capacidade, autonomia e VRP com multiplos veiculos e evolucao conjunta da frota. O foco das proximas sprints e completar LLM, experimentos e artefatos finais.

## Escopo do Projeto 2

Requisitos funcionais do enunciado:

- resolver TSP para rotas de entrega;
- representar entregas medicas e veiculos;
- considerar distancia, prioridade e restricoes relevantes no fitness;
- considerar prioridade de entregas;
- considerar capacidade limitada dos veiculos;
- considerar autonomia limitada dos veiculos;
- evoluir para multiplos veiculos, isto e, VRP;
- visualizar rotas otimizadas;
- gerar instrucoes e relatorios com LLM;
- responder perguntas sobre rotas em linguagem natural;
- comparar resultados com diferentes configuracoes.

Requisitos tecnicos:

- projeto Python estruturado;
- ambiente virtual com dependencias;
- testes automatizados;
- documentacao tecnica;
- relatorio tecnico;
- roteiro de demonstracao.

## Estado Atual

### Implementado

- Implementacao principal em `src/`.
- Type hints e dataclasses nos modelos principais.
- TSP com Algoritmo Genetico.
- Representacao de rota como permutacao de entregas.
- Deposito opcional fixado no inicio da rota.
- Populacao inicial aleatoria.
- Selecao por melhores individuos.
- Order crossover.
- Mutacao por troca adjacente.
- Elitismo.
- Fitness por distancia de rota fechada.
- Penalizacao por atraso por prioridade.
- Penalizacao por excesso de capacidade.
- Penalizacao por excesso de autonomia.
- VRP com cromossomo de frota e distribuicao evolutiva de entregas entre veiculos.
- Fitness agregado por frota.
- Visualizacao VRP animada com uma rota por veiculo.
- Selecao de frota no modo VRP via `--vehicle-ids`.
- Leitura de entregas e veiculos via CSV.
- Dataset de entregas sinteticas.
- Dataset de capitais brasileiras em 2D.
- Dataset de veiculos com capacidade e autonomia.
- Demo visual com Pygame.
- Grafico de fitness com Matplotlib.
- CLI configuravel.
- Testes automatizados com `pytest`.
- Documentacao de arquitetura, sprints, roteiro e relatorio inicial.
- Referencia de agente LLM em `references/agent-llm.py`.

### Validacao Atual

Ultima validacao conhecida:

```text
42 passed
```

## Arquitetura Atual

```text
data/*.csv
   |
   v
src/data_loader.py
   |
   v
Delivery / Vehicle / City / Priority
   |
   v
TSPProblem / VRPProblem
   |
   v
src/ga/genetic_algorithm.py
   |
   v
TSPSolution / TSPGenerationState / VRPSolution
   |
   v
src/main.py + src/visualization/
```

## Componentes

### Modelos

- `src/models/delivery.py`: `City` e `Delivery`.
- `src/models/priority.py`: `Priority` com `HIGH`, `MEDIUM`, `LOW`.
- `src/models/vehicle.py`: `Vehicle` com `max_capacity` e `max_distance`.

### Algoritmo Genetico

- `src/ga/genetic_algorithm.py`

Responsabilidades:

- gerar populacao;
- calcular distancia;
- calcular fitness;
- aplicar crossover;
- aplicar mutacao;
- ordenar populacao por fitness;
- executar geracoes;
- retornar melhor rota e historico.

### Roteamento TSP

- `src/routing/tsp.py`

Responsabilidades:

- adaptar entregas e veiculo ao algoritmo genetico;
- aplicar deposito fixo quando existir;
- propagar limites de capacidade e autonomia;
- disponibilizar execucao completa e iterativa.

### Roteamento VRP

- `src/routing/vrp.py`

Responsabilidades:

- representar problema de multiplos veiculos;
- distribuir entregas entre veiculos;
- evoluir cromossomos completos de frota;
- agregar fitness da frota;
- mover e trocar entregas entre veiculos;
- expor rotas por veiculo;
- alimentar a visualizacao animada do modo VRP.

### Visualizacao e CLI

- `src/main.py`
- `src/visualization/maps.py`
- `src/visualization/plots.py`

Opcoes atuais da CLI:

- `--vehicle-id`
- `--vehicle-ids`
- `--mode`
- `--population-size`
- `--mutation-probability`
- `--elite-size`
- `--fps`
- `--deliveries-file`
- `--vehicles-file`

## Fitness Atual

O fitness e minimizado.

```text
fitness = distancia_total_da_rota
        + penalidade_por_atraso
        + penalidade_por_capacidade
        + penalidade_por_autonomia
```

Penalidades:

- atraso `HIGH`: `100.0` por unidade de atraso;
- atraso `MEDIUM`: `30.0` por unidade de atraso;
- atraso `LOW`: `10.0` por unidade de atraso;
- excesso de capacidade: `25.0` por unidade acima de `max_capacity`;
- excesso de autonomia: `25.0` por unidade acima de `max_distance`.

## Comparacao com o Enunciado

| Requisito | Estado |
|---|---|
| TSP com Algoritmo Genetico | Atendido |
| Representacao genetica de rotas | Atendido |
| Operadores de selecao, crossover e mutacao | Atendido |
| Fitness com distancia | Atendido |
| Prioridades de entrega | Atendido |
| Capacidade limitada dos veiculos | Atendido |
| Autonomia limitada dos veiculos | Atendido |
| Visualizacao de rotas | Atendido parcialmente |
| Testes automatizados | Atendido |
| Documentacao tecnica | Atendido parcialmente |
| Multiplos veiculos / VRP | Atendido parcialmente |
| Integracao com LLM | Pendente |
| Instrucoes para motoristas | Pendente |
| Relatorios operacionais | Pendente |
| Perguntas em linguagem natural | Pendente |
| Experimentos comparativos | Pendente |
| Graficos e artefatos finais | Pendente |
| Relatorio tecnico consolidado | Em andamento |
| Video de demonstracao | Planejado |

## Riscos Tecnicos Atuais

### VRP com operadores simples

O enunciado exige multiplos veiculos. O sistema ja otimiza uma frota completa, mas os operadores geneticos de VRP ainda sao simples.

Mitigacao:

- refinar crossover para preservar agrupamentos geograficos;
- adicionar mutacoes como inversao de segmento e realocacao guiada por capacidade;
- comparar os operadores atuais com abordagens alternativas.

### LLM ainda ausente no `src/`

Os arquivos em `src/llm/` ainda nao possuem implementacao. O arquivo `references/agent-llm.py` foi adicionado como referencia de integracao com OpenAI, historico de mensagens e function calling.

Mitigacao:

- criar prompts reutilizaveis;
- implementar gerador de relatorio operacional;
- implementar explicador de rotas;
- manter funcoes testaveis sem depender obrigatoriamente de chamada externa.

### Experimentos ainda nao automatizados

Existem arquivos em `config/`, mas ainda nao ha runner consolidado.

Mitigacao:

- implementar logger de experimentos;
- registrar tempo, fitness e convergencia;
- gerar graficos em `artifacts/charts/`.

### Distancia Euclidiana

O projeto usa coordenadas 2D e distancia euclidiana, nao malha viaria real.

Mitigacao:

- documentar essa limitacao;
- manter como aproximacao valida para demonstracao;
- considerar integracao futura com APIs de roteamento real.

### Parametros de penalidade fixos

Os pesos das penalidades estao definidos como constantes no codigo.

Mitigacao:

- expor penalidades em configuracao futura;
- comparar sensibilidade nos experimentos.

## Plano Incremental Atualizado

### Sprint 1 - Analise

Status: Concluida.

Entregaveis:

- analise do baseline;
- identificacao de lacunas;
- plano de extensao inicial.

### Sprint 2 - Migracao para `src/`

Status: Concluida.

Entregaveis:

- nucleo genetico testavel;
- type hints;
- dataclasses;
- testes de fitness, populacao, ordenacao, crossover e mutacao;
- comportamento equivalente ao baseline.

### Sprint 3 - Prioridades

Status: Concluida.

Entregaveis:

- `Priority` com `HIGH`, `MEDIUM`, `LOW`;
- `Delivery.priority`;
- `Delivery.due_time`;
- penalizacao por atraso;
- testes;
- `docs/sprint3_priorities.md`.

### Sprint 4 - Capacidade

Status: Concluida.

Entregaveis:

- `Delivery.weight`;
- `Vehicle.max_capacity`;
- penalizacao por excesso de capacidade;
- exemplos em `data/`;
- testes;
- `docs/sprint4_capacity.md`.

### Sprint 5 - Autonomia

Status: Concluida.

Entregaveis:

- `Vehicle.max_distance`;
- penalizacao por excesso de autonomia;
- propagacao do limite no TSP e algoritmo genetico;
- testes;
- `docs/sprint5_autonomy.md`.

### Sprint 5.1 - Dados, CLI e Documentacao

Status: Concluida.

Entregaveis:

- CLI com `--vehicle-id`, `--vehicle-ids`, `--population-size`, `--mutation-probability`, `--elite-size`, `--fps`, `--deliveries-file`, `--vehicles-file`;
- dataset `data/brazil_capitals_sample.csv`;
- deposito coerente para o dataset de capitais;
- README atualizado;
- arquitetura documentada;
- relatorio tecnico inicial;
- roteiro de video;
- outline do relatorio.

### Sprint 6 - VRP

Status: Concluida.

Objetivo:

Expandir TSP para multiplos veiculos.

Entregaveis:

- preencher `src/routing/vrp.py`;
- preencher `tests/test_vrp.py`;
- criar modelo ou estrutura para solucao de frota;
- distribuir entregas entre veiculos;
- calcular fitness agregado;
- respeitar capacidade e autonomia por veiculo;
- integrar modo visual `--mode vrp`;
- permitir selecionar frota com `--vehicle-ids`, mantendo todos os veiculos como padrao;
- documentar estrategia em `docs/sprint6_vrp.md`.

### Sprint 7 - LLM

Status: Proxima.

Objetivo:

Gerar textos operacionais a partir das rotas otimizadas.

Referencia:

- `references/agent-llm.py`

Esse exemplo deve orientar o desenho da integracao LLM, mas o dominio financeiro deve ser substituido pelo dominio de rotas medicas.

Entregaveis:

- `src/llm/prompts.py`;
- `src/llm/report_generator.py`;
- `src/llm/route_explainer.py`;
- prompts para relatorio, instrucoes e perguntas;
- testes de formatacao e montagem de prompt;
- documentacao de uso em `docs/sprint7_llm.md`.

### Sprint 8 - Experimentos

Status: Pendente.

Objetivo:

Comparar configuracoes do algoritmo genetico.

Entregaveis:

- runner de experimentos;
- uso de `config/pop50.yaml`, `config/pop100.yaml`, `config/pop500.yaml`;
- metricas de tempo, fitness e convergencia;
- graficos em `artifacts/charts/`;
- atualizacao de `reports/final_report.md`.

### Sprint 9 - Consolidacao

Status: Planejada.

Entregaveis:

- graficos finais;
- mapas finais;
- relatorio consolidado;
- roteiro final de apresentacao;
- evidencias de execucao.

### Sprint 10 - Integracao Final com LLM

Status: Planejada.

Entregaveis:

- LLM integrada ao fluxo final;
- relatorio gerado a partir da rota;
- instrucoes por motorista ou veiculo;
- perguntas e respostas sobre rotas;
- exemplos documentados.

## Criterios de Aceite para as Proximas Sprints

### Sprint 7

- O sistema deve gerar instrucoes legiveis para motoristas.
- O sistema deve gerar relatorio operacional com distancia, entregas e restricoes.
- O sistema deve responder perguntas simples sobre rotas.
- Prompts devem ficar centralizados e testaveis.
- A integracao real com OpenAI deve ser opcional nos testes.

### Sprint 8

- Os tres cenarios de configuracao devem ser executaveis.
- Resultados devem ser comparaveis em tabela.
- Graficos de convergencia devem ser gerados.
- O relatorio deve incluir analise dos experimentos.

## Conclusao

O projeto ja atende ao nucleo de TSP com Algoritmo Genetico, as principais restricoes logisticas individuais e um VRP com multiplas rotas e evolucao conjunta da frota. A implementacao atual e testavel, configuravel via CLI e possui visualizacao 2D.

Para aderencia completa ao Projeto 2, as proximas prioridades sao LLM para instrucoes e relatorios, experimentos comparativos, artefatos finais e refinamento dos operadores do VRP.
