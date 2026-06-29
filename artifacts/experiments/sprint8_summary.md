# 📊 Sprint 8 — Resumo dos Experimentos VRP

---

## Estatísticas Gerais

| Métrica | Valor |
|---------|-------|
| **Melhor configuração** | pop50 (melhor custo-benefício) |
| **Fitness médio final** | 0.16 |
| **Desvio padrão do fitness** | 0.00 |
| **Tempo médio de execução** | 6.676s |
| **Speedup pop50 vs pop500** | ≈ 10× |

---

## Configurações Testadas

| Configuração | Pop. | Mutação | Crossover | Elitismo | Pool | Gerações |
|:------------|:----:|:-------:|:---------:|:--------:|:----:|:--------:|
| pop50 | 50 | 0.14 | 0.68 | 1 | 6 | 500 |
| pop100 | 100 | 0.08 | 0.80 | 2 | 10 | 500 |
| pop100_no_elitism | 100 | 0.08 | 0.80 | 0 | 10 | 500 |
| pop500 | 500 | 0.02 | 0.90 | 6 | 20 | 500 |
| pop500_no_elitism | 500 | 0.02 | 0.90 | 0 | 20 | 500 |

---

## Resultados Comparativos

| Configuração | Fitness Final | Convergência | Tempo Total | Melhoria |
|:------------|:-------------:|:------------:|:-----------:|:--------:|
| **pop50** ⭐ | 0.16 | Gen. 103 | 1.323s | 0.40 |
| pop100 | 0.16 | Gen. 187 | 2.588s | 0.40 |
| pop100_no_elitism | 0.16 | Gen. 176 | 2.639s | 0.40 |
| pop500 | 0.16 | Gen. 33 | 13.404s | 0.35 |
| pop500_no_elitism | 0.16 | Gen. 33 | 13.425s | 0.35 |

---

## Análise

### Todas as configurações atingiram o mesmo fitness final

O fitness 0.16 foi alcançado por **todas as 5 configurações**, demonstrando robustez do algoritmo independentemente do tamanho da população.

### pop50 entrega o melhor custo-benefício

- Mesmo fitness que pop500 em **10× menos tempo**
- Convergência na geração 103 — razoavelmente cedo
- Ideal para demonstrações ao vivo e execuções repetitivas

### Elitismo: impacto moderado neste dataset

- `pop100_no_elitism` convergiu na geração 176 — **11 gerações antes** do `pop100` com elitismo (187)
- `pop500_no_elitism` manteve a mesma convergência (33), com tempo levemente maior

### Populações maiores: rápidas em gerações, caras no total

- `pop500` convergiu na geração 33, mas cada geração é muito mais cara
- O custo por geração escala linearmente com o tamanho da população

---

## Artefatos Gerados

```
artifacts/experiments/sprint8_summary.csv    ← esta tabela em CSV
artifacts/experiments/sprint8_summary.json   ← dados estruturados
artifacts/charts/fitness_curves.png          ← curvas de convergência
artifacts/charts/final_fitness.png           ← comparativo de fitness final
artifacts/charts/execution_time.png          ← comparativo de tempo
```

## Como Reproduzir

```bash
.venv/bin/python -m src.metrics \
  --deliveries-file data/deliveries_sample.csv \
  --vehicles-file  data/vehicles_sample.csv \
  --output-dir     artifacts
```
