# Sprint 9 - Consolidacao Final

## Objetivo

Consolidar a entrega final do Projeto 2 com relatorio atualizado, roteiro de apresentacao, artefatos de experimentos e evidencias de validacao.

Status: concluida.

Resumo: a Sprint 9 fechou a documentacao final, organizou os artefatos gerados nas sprints anteriores e deixou comandos reproduziveis para demonstracao visual, LLM e experimentos VRP.

## Entregaveis

- `reports/final_report.md`: relatorio tecnico consolidado;
- `docs/video_script.md`: roteiro final de demonstracao;
- `docs/sprint8_experiments.md`: registro detalhado dos experimentos VRP;
- `artifacts/experiments/sprint8_summary.md`: resumo dos experimentos;
- `artifacts/experiments/sprint8_summary.csv`: tabela comparativa;
- `artifacts/experiments/sprint8_summary.json`: dados estruturados;
- `artifacts/charts/fitness_curves.png`: curvas de convergencia;
- `artifacts/charts/final_fitness.png`: comparativo de fitness final;
- `artifacts/charts/execution_time.png`: comparativo de tempo;
- `artifacts/final/manifest.md`: indice final de artefatos, comandos e evidencias.

## Escopo Consolidado

O projeto entregue cobre:

- TSP com Algoritmo Genetico;
- prioridades de entrega e penalidade por atraso;
- capacidade maxima dos veiculos;
- autonomia maxima por veiculo;
- VRP com multiplos veiculos e cromossomo de frota;
- visualizacao TSP/VRP com Pygame;
- fundo simplificado do Brasil para o dataset de capitais;
- camada LLM testavel, offline por padrao e com OpenAI opcional;
- experimentos comparativos em VRP;
- documentacao tecnica e roteiro de demonstracao;
- testes automatizados.

## Comandos de Demonstracao

Visualizacao TSP:

```bash
.venv/bin/python -m src.main --deliveries-file data/brazil_capitals_sample.csv --vehicle-id 3 --population-size 100 --mutation-probability 0.3 --elite-size 2 --fps 15
```

Visualizacao VRP:

```bash
.venv/bin/python -m src.main --mode vrp --deliveries-file data/brazil_capitals_sample.csv --population-size 100 --mutation-probability 0.3 --elite-size 2 --fps 15
```

Camada LLM offline:

```bash
.venv/bin/python -m src.llm --mode vrp --output report --deliveries-file data/brazil_capitals_sample.csv
```

Experimentos VRP:

```bash
.venv/bin/python -m src.metrics --deliveries-file data/deliveries_sample.csv --vehicles-file data/vehicles_sample.csv --output-dir artifacts
```

Testes:

```bash
.venv/bin/python -m pytest
```

## Evidencia de Validacao

Ultima validacao conhecida:

```text
62 passed
```

## Conclusao

A Sprint 9 encerra o ciclo de implementacao incremental. O projeto fica pronto para apresentacao com codigo executavel, testes automatizados, relatorio consolidado, artefatos de experimentos e roteiro de demonstracao.
