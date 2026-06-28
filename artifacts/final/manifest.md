# Manifesto Final de Artefatos

## Relatorio e Documentacao

- `reports/final_report.md`: relatorio tecnico consolidado.
- `docs/video_script.md`: roteiro final de apresentacao.
- `docs/sprint9_consolidation.md`: fechamento da Sprint 9.
- `docs/sprint8_experiments.md`: detalhes dos experimentos VRP.
- `README.md`: comandos principais e indice de documentacao.

## Artefatos de Experimentos

- `artifacts/experiments/sprint8_summary.md`
- `artifacts/experiments/sprint8_summary.csv`
- `artifacts/experiments/sprint8_summary.json`
- `artifacts/charts/fitness_curves.png`
- `artifacts/charts/final_fitness.png`
- `artifacts/charts/execution_time.png`

## Comandos Reproduziveis

Visualizacao VRP:

```bash
.venv/bin/python -m src.main --mode vrp --deliveries-file data/brazil_capitals_sample.csv --population-size 100 --mutation-probability 0.3 --elite-size 2 --fps 15
```

Relatorio LLM offline:

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

## Evidencia Atual

```text
62 passed
```

## Resultado dos Experimentos VRP

| Configuracao | Fitness final | Convergencia | Tempo | Melhoria |
| --- | ---: | ---: | ---: | ---: |
| pop50 | 0.16 | 103 | 1.323s | 0.40 |
| pop100 | 0.16 | 187 | 2.588s | 0.40 |
| pop100_no_elitism | 0.16 | 176 | 2.639s | 0.40 |
| pop500 | 0.16 | 33 | 13.404s | 0.35 |
| pop500_no_elitism | 0.16 | 33 | 13.425s | 0.35 |
