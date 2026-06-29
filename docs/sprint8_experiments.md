# 🏃 Sprint 8 — Experimentos Comparativos VRP

**Status:** ✅ Concluída

---

## 🎯 Objetivo

Implementar um **runner de experimentos reproduzível** para comparar sistematicamente 5 configurações do Algoritmo Genético em modo VRP — medindo fitness final, velocidade de convergência e tempo de execução.

---

## 📊 Motivação

Com o VRP implementado na Sprint 6, era necessário entender como os parâmetros do AG afetam:
1. **Qualidade da solução** (fitness final)
2. **Velocidade de convergência** (em quantas gerações estabiliza)
3. **Custo computacional** (tempo de execução)

A Sprint 8 responde a essas perguntas com evidências quantitativas e gráficos reproduzíveis.

---

## 📁 Arquivos Implementados

| Arquivo | Responsabilidade |
|---------|-----------------|
| `src/metrics/experiments.py` | Execução de cada configuração de experimento |
| `src/metrics/experiment_logger.py` | Exportação de CSV, JSON, Markdown e gráficos PNG |
| `src/metrics/statistics.py` | Métricas auxiliares (geração de convergência, melhoria relativa) |
| `src/metrics/__main__.py` | Ponto de entrada via `python -m src.metrics` |

---

## ⚙️ Configurações dos Experimentos

Cinco cenários foram definidos em `config/`:

| Configuração | Pop. | Mutação | Crossover | Elitismo | Pool | Gerações | Objetivo |
|:------------|:----:|:-------:|:---------:|:--------:|:----:|:--------:|---------|
| `pop50` | 50 | 0.14 | 0.68 | 1 | 6 | 500 | Exploração rápida com menor custo |
| `pop100` | 100 | 0.08 | 0.80 | 2 | 10 | 500 | Equilíbrio entre qualidade e velocidade |
| `pop100_no_elitism` | 100 | 0.08 | 0.80 | 0 | 10 | 500 | Exploração sem preservação de elite |
| `pop500` | 500 | 0.02 | 0.90 | 6 | 20 | 500 | Alta pressão de convergência |
| `pop500_no_elitism` | 500 | 0.02 | 0.90 | 0 | 20 | 500 | Alta pressão sem elitismo |

---

## 📈 Resultados Obtidos

Dataset: `data/deliveries_sample.csv` | Modo: VRP | Semente: fixa (reproduzível)

| Configuração | Fitness Final | Convergência | Tempo Total | Melhoria | Veredicto |
|:------------|:-------------:|:------------:|:-----------:|:--------:|:----------|
| **pop50** ⭐ | 0.16 | Gen. 103 | 1.323s | 0.40 | **Melhor custo-benefício** |
| pop100 | 0.16 | Gen. 187 | 2.588s | 0.40 | Equilibrado |
| pop100_no_elitism | 0.16 | Gen. 176 | 2.639s | 0.40 | Convergiu antes do pop100 |
| pop500 | 0.16 | Gen. 33 | 13.404s | 0.35 | Rápido em gerações, caro no total |
| pop500_no_elitism | 0.16 | Gen. 33 | 13.425s | 0.35 | Idêntico ao pop500 |

---

## 🔍 Análise dos Resultados

### 1. Fitness final igual para todos

Todas as 5 configurações atingiram **fitness = 0.16** — demonstrando que o algoritmo é robusto e encontra soluções de qualidade equivalente independentemente do tamanho da população.

### 2. pop50 é o grande vencedor

```
pop50:  1.323s → fitness 0.16 → convergência na geração 103
pop500: 13.40s → fitness 0.16 → convergência na geração 33

Speedup: 13.40 / 1.32 ≈ 10× mais rápido com a mesma qualidade
```

### 3. Elitismo: impacto moderado

| Comparação | Diferença observada |
|------------|---------------------|
| pop100 vs pop100_no_elitism | Sem elitismo convergiu 11 gerações antes (176 vs 187) |
| pop500 vs pop500_no_elitism | Sem diferença na convergência; tempo levemente maior sem elitismo |

> Conclusão: elitismo não é fator determinante neste dataset — a diversidade da população tem mais impacto.

### 4. Populações maiores: convergem mais rápido em gerações, mas pagam alto custo por geração

- `pop500` convergiu na geração 33, mas cada geração é 10× mais cara que `pop50`
- O custo total por geração escala com o tamanho da população

---

## 📦 Artefatos Gerados

Todos os artefatos ficam em `artifacts/` após a execução:

| Artefato | Formato | Conteúdo |
|----------|---------|----------|
| `artifacts/experiments/sprint8_summary.csv` | CSV | Tabela comparativa completa |
| `artifacts/experiments/sprint8_summary.json` | JSON | Dados estruturados para integração |
| `artifacts/experiments/sprint8_summary.md` | Markdown | Resumo legível com tabelas |
| `artifacts/charts/fitness_curves.png` | PNG | Curvas de evolução do fitness por geração |
| `artifacts/charts/final_fitness.png` | PNG | Comparativo do fitness final entre configurações |
| `artifacts/charts/execution_time.png` | PNG | Comparativo de tempo de execução |

---

## ▶️ Como Reproduzir

```bash
# Execução padrão (usa deliveries_sample.csv e vehicles_sample.csv)
.venv/bin/python -m src.metrics

# Execução com parâmetros explícitos
.venv/bin/python -m src.metrics \
  --deliveries-file data/deliveries_sample.csv \
  --vehicles-file  data/vehicles_sample.csv \
  --output-dir     artifacts
```

O runner executa os 5 cenários sequencialmente, salva todos os artefatos automaticamente e exibe um resumo no terminal ao final.

---

## ✅ Critérios de Aceite

| Critério | Status |
|----------|--------|
| Runner executa as 5 configurações por CLI | ✅ |
| Resultados comparáveis em tabela | ✅ |
| Gráficos de fitness e tempo gerados automaticamente | ✅ |
| Relatório final inclui análise da Sprint 8 | ✅ |
| Execução validada por testes automatizados | ✅ |
| Artefatos reproduzíveis com semente fixa | ✅ |
