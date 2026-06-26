# Introdução

Este relatorio descreve o desenvolvimento do Projeto 2 do Tech Challenge Fase 2: um sistema de otimizacao de rotas medicas para distribuicao de medicamentos e insumos.

O projeto parte de um codigo base de TSP e evolui para um resolvedor em `src/` com Algoritmo Genetico, restricoes operacionais, visualizacao e testes automatizados.

Estado atual: TSP com prioridades, capacidade e autonomia implementado. VRP com multiplos veiculos, LLM e comparativos experimentais ainda estao planejados.

# Fundamentação Teórica

## Algoritmos Genéticos

Algoritmos Geneticos sao metodos de otimizacao inspirados em processos evolutivos. Uma populacao de solucoes candidatas e avaliada por uma funcao fitness, e novas geracoes sao criadas por operadores como selecao, crossover, mutacao e elitismo.

Neste projeto, cada individuo representa uma rota. A qualidade da rota e avaliada por distancia total e penalidades ligadas ao contexto logistico medico.

## Problema do Caixeiro Viajante

O Problema do Caixeiro Viajante, ou TSP, busca encontrar a menor rota que visita todos os pontos uma unica vez e retorna ao ponto inicial.

No contexto do projeto, os pontos representam entregas de medicamentos e insumos. O deposito representa o ponto de partida da rota.

## Vehicle Routing Problem

O Vehicle Routing Problem, ou VRP, generaliza o TSP para multiplos veiculos e multiplas rotas.

O VRP e um requisito do enunciado, mas ainda nao foi implementado no estado atual do projeto. O modulo `src/routing/vrp.py` existe como ponto de extensao.

## Large Language Models

Large Language Models podem transformar dados operacionais em explicacoes, instrucoes e relatorios em linguagem natural.

No Projeto 2, a LLM deve gerar instrucoes para motoristas, relatorios de eficiencia e respostas sobre rotas. Esta camada ainda esta pendente no estado atual.

# Metodologia

O projeto foi conduzido em sprints incrementais:

1. Analise do codigo base e plano de extensao.
2. Migracao do TSP para `src/` com dataclasses, type hints e testes.
3. Inclusao de prioridades e penalizacao por atraso.
4. Inclusao de peso e capacidade maxima dos veiculos.
5. Inclusao de autonomia maxima dos veiculos.

A validacao foi feita com testes automatizados usando `pytest`.

# Implementação

## Estrutura

- `src/ga/genetic_algorithm.py`: algoritmo genetico e fitness.
- `src/routing/tsp.py`: adaptacao do algoritmo para TSP.
- `src/models/`: modelos de entrega, prioridade, cidade e veiculo.
- `src/data_loader.py`: leitura dos arquivos CSV.
- `src/visualization/`: desenho da rota e grafico de fitness.
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
.venv/bin/python -m src.main --deliveries-file data/brazil_capitals_sample.csv --vehicle-id 3 --population-size 200 --mutation-probability 0.3 --fps 15
```

# Experimentos

Ainda nao foram executados experimentos comparativos formais.

Arquivos de configuracao previstos:

- `config/pop50.yaml`
- `config/pop100.yaml`
- `config/pop500.yaml`

Proxima etapa: executar esses cenarios, registrar tempo, melhor fitness e curva de convergencia.

# Resultados

Resultado atual validado:

- TSP funcional com visualizacao;
- fitness com distancia, atraso, capacidade e autonomia;
- leitura de entregas e veiculos via CSV;
- CLI configuravel;
- suite de testes automatizados passando.

Ultima validacao conhecida:

```text
30 passed
```

# Trabalhos Futuros

Prioridades para aderencia completa ao enunciado:

1. Implementar VRP com multiplos veiculos.
2. Implementar camada LLM para instrucoes, relatorios e perguntas.
3. Executar experimentos comparativos.
4. Gerar graficos e artefatos de resultados.
5. Completar analise final e video de demonstracao.

# Referências

- Documento do Tech Challenge Fase 2.
- Codigo base em `references/`.
- Documentacao interna em `docs/`.
