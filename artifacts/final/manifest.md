# 📋 Manifesto Final de Artefatos

**Tech Challenge Fase 2 — Otimização de Rotas Médicas**
Gerado ao final da Sprint 9.

---

## 📄 Relatório e Documentação

| Arquivo | Descrição |
|---------|-----------|
| `reports/final_report.md` | Relatório técnico consolidado — do problema à solução |
| `docs/video_script.md` | Roteiro detalhado para o vídeo de demonstração (≤15 min) |
| `docs/architecture.md` | Arquitetura completa do sistema e fluxo de dados |
| `docs/sprint8_experiments.md` | Detalhamento técnico e análise dos experimentos VRP |
| `docs/sprint9_consolidation.md` | Fechamento da Sprint 9 e evidências de entrega |
| `docs/resultado.html` | Página de resultados visual — abrir diretamente no navegador |
| `README.md` | Comandos principais, CLI, dependências e índice de documentação |

---

## 🧪 Artefatos de Experimentos

| Arquivo | Formato | Conteúdo |
|---------|---------|----------|
| `artifacts/experiments/sprint8_summary.md` | Markdown | Resumo legível com configurações e resultados |
| `artifacts/experiments/sprint8_summary.csv` | CSV | Tabela comparativa das 5 configurações |
| `artifacts/experiments/sprint8_summary.json` | JSON | Dados estruturados para análise programática |
| `artifacts/charts/fitness_curves.png` | PNG | Curvas de evolução do fitness por geração |
| `artifacts/charts/final_fitness.png` | PNG | Comparativo do fitness final entre configurações |
| `artifacts/charts/execution_time.png` | PNG | Comparativo de tempo de execução |

---

## 📊 Resultado dos Experimentos VRP

Dataset: `data/deliveries_sample.csv` | Modo: VRP | 500 gerações

| Configuração | Fitness | Convergência | Tempo | Melhoria |
|:------------|:-------:|:------------:|:-----:|:--------:|
| **pop50** ⭐ | 0.16 | Gen. 103 | 1.323s | 0.40 |
| pop100 | 0.16 | Gen. 187 | 2.588s | 0.40 |
| pop100_no_elitism | 0.16 | Gen. 176 | 2.639s | 0.40 |
| pop500 | 0.16 | Gen. 33 | 13.404s | 0.35 |
| pop500_no_elitism | 0.16 | Gen. 33 | 13.425s | 0.35 |

**Estatísticas gerais:**
- Melhor configuração: `pop50` (melhor custo-benefício)
- Fitness médio final: 0.16 (desvio padrão: 0.00)
- Tempo médio de execução: 6.676s
- Speedup pop50 vs pop500: **≈ 10×**

---

## ▶️ Comandos Reproduzíveis

### Visualização TSP (mapa do Brasil)
```bash
.venv/bin/python -m src.main \
  --deliveries-file data/brazil_capitals_sample.csv \
  --vehicle-id 3 \
  --population-size 100 \
  --mutation-probability 0.3 \
  --elite-size 2 \
  --fps 15
```

### Visualização VRP (múltiplos veículos)
```bash
.venv/bin/python -m src.main \
  --mode vrp \
  --deliveries-file data/brazil_capitals_sample.csv \
  --population-size 100 \
  --mutation-probability 0.3 \
  --elite-size 2 \
  --fps 15
```

### Relatório LLM offline
```bash
.venv/bin/python -m src.llm \
  --mode vrp \
  --output report \
  --deliveries-file data/brazil_capitals_sample.csv
```

### Experimentos VRP completos
```bash
.venv/bin/python -m src.metrics \
  --deliveries-file data/deliveries_sample.csv \
  --vehicles-file  data/vehicles_sample.csv \
  --output-dir     artifacts
```

### Suite de testes
```bash
.venv/bin/python -m pytest
```

---

## ✅ Evidência de Validação

```
62 passed
```

---

## 🔗 Links

- Repositório: [github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2](https://github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2)
