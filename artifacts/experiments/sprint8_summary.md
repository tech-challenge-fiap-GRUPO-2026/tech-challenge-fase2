# Sprint 8 - Experimentos

## Resumo

- Melhor fitness: pop50 (0.16)
- Fitness medio final: 0.16
- Desvio padrao do fitness final: 0.00
- Tempo medio: 6.676s

## Configuracoes

| Configuracao | Populacao | Mutacao | Crossover | Elitismo | Pool | Geracoes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| pop50 | 50 | 0.14 | 0.68 | 1 | 6 | 500 |
| pop100 | 100 | 0.08 | 0.80 | 2 | 10 | 500 |
| pop100_no_elitism | 100 | 0.08 | 0.80 | 0 | 10 | 500 |
| pop500 | 500 | 0.02 | 0.90 | 6 | 20 | 500 |
| pop500_no_elitism | 500 | 0.02 | 0.90 | 0 | 20 | 500 |

## Comparativo

| Configuracao | Fitness final | Convergencia | Tempo | Melhoria |
| --- | ---: | ---: | ---: | ---: |
| pop50 | 0.16 | 103 | 1.323s | 0.40 |
| pop100 | 0.16 | 187 | 2.588s | 0.40 |
| pop100_no_elitism | 0.16 | 176 | 2.639s | 0.40 |
| pop500 | 0.16 | 33 | 13.404s | 0.35 |
| pop500_no_elitism | 0.16 | 33 | 13.425s | 0.35 |
