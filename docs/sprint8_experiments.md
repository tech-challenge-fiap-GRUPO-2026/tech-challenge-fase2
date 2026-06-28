# Sprint 8 - Experimentos

## Objetivo

Concluir a camada de experimentos comparativos do Projeto 2 com foco em VRP, medindo fitness final, convergencia e tempo de execucao.

Status: concluida.

Resumo: a Sprint 8 foi finalizada com um runner em `src/metrics/`, cinco cenarios de configuracao e geracao automatica de tabelas e graficos em `artifacts/`.

## Escopo da Sprint

Implementar um fluxo reproduzivel para comparar configuracoes do algoritmo genetico em modo VRP.

Entregaveis implementados:

- `src/metrics/experiments.py`: execucao dos experimentos;
- `src/metrics/experiment_logger.py`: exportacao de CSV, JSON, markdown e graficos;
- `src/metrics/statistics.py`: metricas auxiliares;
- `src/metrics/__main__.py`: execucao por CLI com `python -m src.metrics`;
- `config/pop50.yaml`: cenario de exploracao rapida;
- `config/pop100.yaml`: cenario balanceado;
- `config/pop100_no_elitism.yaml`: cenario balanceado sem elitismo;
- `config/pop500.yaml`: cenario de convergencia mais agressiva;
- `config/pop500_no_elitism.yaml`: cenario de convergencia mais agressiva sem elitismo;
- `artifacts/experiments/sprint8_summary.csv`: tabela consolidada;
- `artifacts/experiments/sprint8_summary.json`: saida estruturada para analise;
- `artifacts/experiments/sprint8_summary.md`: resumo legivel;
- `artifacts/charts/fitness_curves.png`: curvas de convergencia;
- `artifacts/charts/final_fitness.png`: comparativo de fitness final;
- `artifacts/charts/execution_time.png`: comparativo de tempo de execucao.

## Estrategia Experimental

Os experimentos usam o algoritmo genetico do proprio projeto em `src/routing/vrp.py` e `src/ga/genetic_algorithm.py`.

Cada configuracao controla:

- `population_size`;
- `mutation_rate`;
- `crossover_rate`;
- `elitism_size`;
- `parent_pool_size`;
- `max_generations`.

Os cinco cenarios finais sao:

- `pop50`: menor populacao, mais mutacao e menor elitismo para favorecer exploracao;
- `pop100`: cenario intermediario e balanceado;
- `pop100_no_elitism`: mesmo perfil do `pop100`, mas com `elitism_size = 0`;
- `pop500`: maior populacao, menor mutacao e maior pressao de convergencia;
- `pop500_no_elitism`: mesmo perfil do `pop500`, mas com `elitism_size = 0`.

## Execucao

Comando principal:

```bash
.venv/bin/python -m src.metrics
```

Execucao equivalente usada no dataset sintetico:

```bash
.venv/bin/python -m src.metrics --deliveries-file data/deliveries_sample.csv --vehicles-file data/vehicles_sample.csv --output-dir artifacts
```

Por padrao, o runner executa em modo `vrp` e usa todos os veiculos do CSV quando `--vehicle-ids` nao e informado.

## Resultado de Referencia

Resultado atual registrado em `artifacts/experiments/sprint8_summary.md`:

| Configuracao | Fitness final | Convergencia | Tempo | Melhoria |
| --- | ---: | ---: | ---: | ---: |
| pop50 | 0.16 | 103 | 1.251s | 0.40 |
| pop100 | 0.16 | 187 | 2.477s | 0.40 |
| pop100_no_elitism | 0.16 | 176 | 2.464s | 0.40 |
| pop500 | 0.16 | 33 | 13.404s | 0.35 |
| pop500_no_elitism | 0.16 | 33 | 13.425s | 0.35 |

Leituras principais:

- as cinco configuracoes alcancaram o mesmo fitness final no smoke test VRP;
- `pop500` convergiu mais cedo, mas com custo de tempo muito maior;
- `pop50` teve o melhor equilibrio entre convergencia e tempo;
- `pop100_no_elitism` convergiu um pouco antes que o `pop100` com elitismo, sem mudar o fitness final;
- `pop500_no_elitism` manteve a mesma convergencia do `pop500`, mas com tempo levemente maior.

## Criterios de Aceite

- O projeto executa os cenarios configurados por CLI.
- Os resultados ficam comparaveis em tabela.
- Os graficos de fitness e tempo sao gerados automaticamente.
- O relatorio final inclui a analise da Sprint 8.
- A execucao e validada por testes automatizados.
