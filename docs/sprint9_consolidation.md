# 🏃 Sprint 9 — Consolidação Final

**Status:** ✅ Concluída

---

## 🎯 Objetivo

Fechar o ciclo de 9 sprints com **documentação técnica consolidada**, roteiro de apresentação, manifesto de artefatos e evidências de validação — deixando o projeto pronto para entrega e demonstração em vídeo.

---

## 📦 Entregáveis desta Sprint

| Arquivo | Conteúdo |
|---------|----------|
| `reports/final_report.md` | Relatório técnico consolidado — do problema à solução |
| `docs/video_script.md` | Roteiro detalhado para o vídeo de demonstração (≤15 min) |
| `docs/sprint8_experiments.md` | Registro detalhado dos experimentos VRP |
| `artifacts/experiments/sprint8_summary.md` | Resumo dos experimentos em Markdown |
| `artifacts/experiments/sprint8_summary.csv` | Tabela comparativa das 5 configurações |
| `artifacts/experiments/sprint8_summary.json` | Dados estruturados para integração |
| `artifacts/charts/fitness_curves.png` | Curvas de convergência do fitness |
| `artifacts/charts/final_fitness.png` | Comparativo de fitness final |
| `artifacts/charts/execution_time.png` | Comparativo de tempo de execução |
| `artifacts/final/manifest.md` | Índice final de artefatos com comandos reproduzíveis |

---

## ✅ Escopo Consolidado — 9 Sprints

| Sprint | Funcionalidade | Status |
|--------|---------------|--------|
| S1 | Análise do código base e plano de extensão | ✅ |
| S2 | Migração do TSP para `src/` com dataclasses e testes | ✅ |
| S3 | Prioridades de entrega (HIGH/MEDIUM/LOW) e penalidade por atraso | ✅ |
| S4 | Peso das entregas e capacidade máxima dos veículos | ✅ |
| S5 | Autonomia máxima por veículo | ✅ |
| S6 | VRP — múltiplos veículos e cromossomo de frota | ✅ |
| S7 | Camada LLM — relatórios, instruções e Q&A | ✅ |
| S8 | Experimentos comparativos VRP com artefatos | ✅ |
| S9 | Documentação final, roteiro e manifesto | ✅ |

---

## 🎬 Comandos de Demonstração

Use estes comandos para a gravação do vídeo de apresentação:

### Visualização TSP (capitais brasileiras)
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

### Camada LLM offline
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
# Resultado esperado: 62 passed
```

---

## 🧪 Evidência de Validação

Última execução da suite de testes:

```
62 passed
```

---

## 📊 Resumo dos Experimentos VRP

| Configuração | Fitness | Convergência | Tempo | Melhoria |
|:------------|:-------:|:------------:|:-----:|:--------:|
| **pop50** ⭐ | 0.16 | Gen. 103 | 1.323s | 0.40 |
| pop100 | 0.16 | Gen. 187 | 2.588s | 0.40 |
| pop100_no_elitism | 0.16 | Gen. 176 | 2.639s | 0.40 |
| pop500 | 0.16 | Gen. 33 | 13.404s | 0.35 |
| pop500_no_elitism | 0.16 | Gen. 33 | 13.425s | 0.35 |

> **`pop50` entrega o mesmo fitness que `pop500` em 10× menos tempo** — melhor configuração para demonstrações ao vivo.

---

## 🚀 Evolução Futura

1. **Operadores VRP especializados** — preservar agrupamentos geográficos (cluster-first route)
2. **Malha viária real** — substituir distâncias euclidianas por rotas OSMnx ou Google Maps
3. **VRPTW** — adicionar janelas de tempo reais às restrições
4. **AG híbrido** — refinamento pós-genético com busca local (2-opt ou Or-opt)
5. **Cliente OpenAI concreto** — demonstração em produção com GPT-4o-mini

---

## 🔗 Links

- Repositório: [github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2](https://github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2)
- Resultado visual: [`docs/resultado.html`](resultado.html)
- Relatório técnico: [`reports/final_report.md`](../reports/final_report.md)
