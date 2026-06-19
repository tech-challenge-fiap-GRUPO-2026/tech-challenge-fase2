# Extension Plan

## Objetivo da Sprint 1

Comparar a implementacao existente em `references/` com os requisitos do Projeto 2 e registrar:

- requisitos ja atendidos;
- requisitos ausentes;
- riscos tecnicos;
- possiveis refatoracoes.

Esta sprint e apenas analitica. Nao ha implementacao de codigo de producao nesta etapa.

## Escopo do Projeto 2

O Projeto 2 tem como objetivo evoluir um resolvedor de rotas baseado em Algoritmos Geneticos para um sistema de otimizacao de rotas medicas.

Requisitos funcionais previstos:

- resolver TSP para uma rota unica;
- evoluir para VRP com multiplos veiculos;
- representar entregas medicas;
- considerar prioridade de entregas `HIGH`, `MEDIUM` e `LOW`;
- considerar peso da entrega;
- respeitar capacidade maxima dos veiculos;
- respeitar autonomia ou distancia maxima por veiculo;
- gerar metricas, graficos e comparacoes experimentais;
- produzir relatorios e explicacoes com apoio de LLM.

Requisitos tecnicos previstos:

- Python 3.12;
- implementacao em `src/`;
- uso de type hints;
- uso de dataclasses para entidades de dominio;
- testes unitarios com `pytest`;
- reproducibilidade de experimentos;
- documentacao tecnica incremental.

## Estado atual da pasta `references/`

A pasta `references/` contem uma implementacao didatica de TSP com Algoritmo Genetico.

Arquivos principais:

- `genetic_algorithm.py`: operadores geneticos, fitness, populacao e demo em linha de comando;
- `tsp.py`: loop visual com Pygame;
- `draw_functions.py`: funcoes de visualizacao;
- `benchmark_att48.py`: dados do benchmark `att48`;
- `demo_crossover.py`: demonstracao isolada de crossover;
- `demo_mutation.py`: demonstracao isolada de mutacao;
- `README.md`: descricao geral do resolvedor TSP;
- `LICENSE`: licenca CC0.

## Requisitos ja atendidos

### TSP basico

Atendido parcialmente.

A implementacao representa uma solucao como uma permutacao de cidades e calcula a distancia total de uma rota fechada. Isso cobre o nucleo do TSP: visitar todas as cidades uma vez e retornar ao ponto inicial.

### Algoritmo Genetico

Atendido parcialmente.

Ja existem os componentes principais:

- geracao de populacao inicial;
- calculo de fitness;
- ordenacao por fitness;
- selecao de pais;
- crossover do tipo order crossover;
- mutacao;
- elitismo simples;
- repeticao por geracoes.

### Fitness por distancia

Atendido.

O fitness e calculado pela soma das distancias Euclidianas entre pontos consecutivos, incluindo o retorno da ultima cidade para a primeira.

### Crossover para permutacao

Atendido parcialmente.

O operador `order_crossover` e adequado para problemas de permutacao porque evita duplicacao de cidades e preserva ordem relativa dos genes restantes.

### Mutacao

Atendido parcialmente.

A mutacao atual troca duas cidades adjacentes com probabilidade configuravel. Isso preserva a validade do cromossomo, mas e uma perturbacao limitada.

### Elitismo

Atendido.

O melhor individuo de cada geracao e preservado diretamente na nova populacao.

### Visualizacao

Atendido parcialmente.

O projeto ja exibe:

- cidades;
- melhor rota da geracao;
- uma rota secundaria;
- grafico de evolucao do fitness.

### Benchmark inicial

Atendido parcialmente.

Ha dados do benchmark `att48` e uma solucao de referencia. O uso esta comentado em `tsp.py`, mas fornece uma base para comparacao posterior.

## Requisitos ausentes

### Estrutura final em `src/`

Ausente.

Os arquivos em `src/` existem, mas ainda estao vazios. A implementacao de referencia ainda nao foi migrada para uma arquitetura reutilizavel e testavel.

### Type hints consistentes

Ausente parcialmente.

Algumas funcoes de `genetic_algorithm.py` e `draw_functions.py` possuem type hints, mas a cobertura nao e completa nem esta organizada em modulos finais.

### Dataclasses de dominio

Ausente.

Ainda nao ha modelos implementados para:

- entrega;
- veiculo;
- prioridade;
- rota;
- resultado de otimizacao.

### Testes unitarios

Ausente.

Os arquivos de teste existem em `tests/`, mas estao vazios. Ainda nao ha cobertura para fitness, crossover, mutacao, constraints, TSP ou VRP.

### Prioridade de entregas

Ausente.

O cromossomo atual contem apenas coordenadas. Nao ha campo para prioridade, janela de atendimento, SLA ou penalizacao por atraso.

### Capacidade de veiculo

Ausente.

Nao ha peso de entrega nem capacidade maxima de veiculo no modelo atual.

### Autonomia ou distancia maxima

Ausente.

A implementacao atual minimiza distancia total, mas nao penaliza ou invalida rotas que excedem uma distancia maxima por veiculo.

### Multiplos veiculos / VRP

Ausente.

O cromossomo atual representa apenas uma rota unica. Nao ha distribuicao de entregas entre veiculos.

### Experimentos reprodutiveis

Ausente.

Nao ha mecanismo consolidado para executar configuracoes como `pop50.yaml`, `pop100.yaml` e `pop500.yaml`, registrar metricas, controlar seed ou exportar resultados.

### Relatorios com LLM

Ausente.

Nao ha implementacao para gerar relatorio operacional, instrucoes para motoristas ou respostas sobre rotas.

## Riscos tecnicos

### Acoplamento com Pygame

O loop principal em `tsp.py` mistura evolucao genetica, configuracao do problema, visualizacao e controle de eventos. Isso dificulta testes automatizados e execucoes batch.

Mitigacao recomendada:

- separar motor genetico de visualizacao;
- mover Pygame para camada opcional;
- criar funcoes puras para TSP e VRP.

### Reprodutibilidade limitada

O uso de aleatoriedade nao controla seed de forma centralizada. Isso dificulta comparar experimentos.

Mitigacao recomendada:

- permitir seed em configuracao;
- registrar seed nos resultados;
- evitar dependencia direta de estado global de `random` quando possivel.

### Crossover degenerado em `tsp.py`

Em `tsp.py`, a chamada atual usa `order_crossover(parent1, parent1)`. Isso reduz a recombinacao genetica, pois o segundo pai selecionado nao participa efetivamente da geracao do filho.

Mitigacao recomendada:

- usar `order_crossover(parent1, parent2)` na implementacao final;
- cobrir esse comportamento por teste.

### Mutacao pouco exploratoria

A mutacao por troca adjacente preserva validade, mas explora pouco o espaco de busca.

Mitigacao recomendada:

- manter swap adjacente como baseline;
- considerar mutacao por swap arbitrario ou inversao de segmento em sprint posterior, se necessario;
- nao alterar comportamento durante a Sprint 2, pois ela pede preservar comportamento.

### Fitness ainda nao representa o dominio medico

O fitness mede apenas distancia. O dominio final precisa considerar prioridade, atraso, peso, capacidade, autonomia e multiplos veiculos.

Mitigacao recomendada:

- introduzir penalidades gradualmente;
- manter distancia como componente base;
- criar testes especificos para cada penalidade.

### Dados representados apenas como coordenadas

O gene atual e uma tupla `(x, y)`. Isso e suficiente para TSP, mas insuficiente para entrega medica.

Mitigacao recomendada:

- criar dataclass `Delivery` contendo id, coordenadas, peso e prioridade;
- criar dataclass `Vehicle` contendo id, capacidade e distancia maxima;
- adaptar fitness para ler entidades de dominio.

### Benchmark nao automatizado

O benchmark `att48` existe, mas seu uso depende de trechos comentados no codigo.

Mitigacao recomendada:

- criar runner de experimentos;
- salvar metricas por execucao;
- gerar graficos em `artifacts/charts/`.

### Ausencia de testes de invariantes geneticos

Operadores de crossover e mutacao precisam garantir que o cromossomo continue sendo uma permutacao valida.

Mitigacao recomendada:

- testar tamanho do filho;
- testar ausencia de duplicatas;
- testar preservacao do conjunto de cidades;
- testar comportamento com seed fixa.

## Possiveis refatoracoes

### Separar nucleo genetico da aplicacao visual

Criar um modulo de algoritmo genetico sem dependencia de Pygame ou Matplotlib.

Responsabilidades sugeridas:

- gerar populacao;
- calcular fitness;
- selecionar pais;
- aplicar crossover;
- aplicar mutacao;
- executar geracoes;
- retornar melhor solucao e historico.

### Criar modelos de dominio

Modelos sugeridos:

- `Delivery`: entrega medica com coordenada, prioridade e peso;
- `Vehicle`: veiculo com capacidade e distancia maxima;
- `Route`: sequencia de entregas alocada a um veiculo;
- `OptimizationResult`: melhor solucao, fitness final e historico.

### Introduzir configuracao explicita

Centralizar parametros como:

- tamanho da populacao;
- numero de geracoes;
- probabilidade de mutacao;
- seed;
- estrategia de selecao;
- parametros de penalizacao.

### Criar camada de constraints

Separar regras de dominio em `src/routing/constraints.py`.

Constraints previstas:

- penalidade por atraso de entrega `HIGH`;
- penalidade por excesso de capacidade;
- penalidade por excesso de distancia maxima;
- validacao de distribuicao de entregas por veiculo.

### Criar camada de experimentos

Criar uma forma padronizada de executar configuracoes e registrar resultados.

Saidas sugeridas:

- fitness final;
- melhor rota;
- tempo de execucao;
- historico de convergencia;
- parametros usados;
- graficos exportados.

### Manter compatibilidade comportamental na Sprint 2

A Sprint 2 pede nova implementacao em `src/` com type hints, dataclasses e testes, sem novas funcionalidades. Portanto, a migracao inicial deve preservar o comportamento do TSP basico antes de adicionar prioridades, capacidade ou VRP.

## Plano incremental recomendado

### Sprint 2

Migrar o TSP basico para `src/`.

Entregaveis:

- nucleo genetico testavel;
- type hints consistentes;
- dataclasses minimas;
- testes para fitness, populacao, ordenacao, crossover e mutacao;
- comportamento equivalente ao baseline de `references/`.

### Sprint 3

Adicionar prioridades.

Entregaveis:

- enum ou constantes para `HIGH`, `MEDIUM`, `LOW`;
- penalizacao por atraso de entregas `HIGH`;
- testes da penalizacao;
- documentacao da nova funcao de fitness.

### Sprint 4

Adicionar peso e capacidade.

Entregaveis:

- peso por entrega;
- capacidade maxima por veiculo;
- penalidade por excesso de capacidade;
- exemplos em `data/`;
- testes de capacidade.

### Sprint 5

Adicionar distancia maxima.

Entregaveis:

- campo de distancia maxima no veiculo;
- penalidade por exceder autonomia;
- testes de limite de distancia.

### Sprint 6

Expandir TSP para VRP.

Entregaveis:

- representacao de multiplas rotas;
- distribuicao de entregas entre veiculos;
- fitness agregado por frota;
- testes de alocacao.

### Sprint 7

Adicionar camada LLM.

Entregaveis:

- gerador de relatorio operacional;
- explicador de rotas;
- prompts reutilizaveis;
- respostas a perguntas sobre rotas.

### Sprint 8

Executar experimentos.

Entregaveis:

- execucao de `pop50.yaml`, `pop100.yaml` e `pop500.yaml`;
- comparacao de fitness, convergencia e tempo;
- graficos em `artifacts/charts/`;
- atualizacao de `reports/final_report.md`.

### Sprint 9

Consolidar apresentacao e artefatos finais.

Entregaveis:

- graficos finais;
- mapas finais;
- relatorio consolidado;
- roteiro de apresentacao.

### Sprint 10

Integrar LLM ao fluxo final.

Entregaveis:

- integracao da geracao textual ao resultado das rotas;
- validacao de prompts;
- documentacao de uso.

## Criterios de aceite para seguir para Sprint 2

Antes de iniciar a Sprint 2, o projeto deve ter clareza sobre:

- quais comportamentos da referencia precisam ser preservados;
- quais funcoes serao migradas para `src/`;
- quais invariantes geneticos devem ser testados;
- como representar cidades, entregas e veiculos sem adicionar funcionalidades antes da hora;
- como manter separada a logica de otimizacao da visualizacao.

## Conclusao

A pasta `references/` atende ao nucleo inicial de um TSP com Algoritmo Genetico, mas ainda esta longe do sistema final de rotas medicas. Ela deve ser tratada como baseline tecnico: util para preservar o comportamento de fitness, populacao, crossover, mutacao e elitismo, mas inadequada como arquitetura final por estar acoplada a visualizacao, nao possuir modelos de dominio, nao ter testes e nao cobrir constraints medicas.

O proximo passo recomendado e migrar o baseline para `src/` com testes e tipos, mantendo comportamento equivalente antes de introduzir prioridades, capacidade, autonomia, VRP e LLM.
