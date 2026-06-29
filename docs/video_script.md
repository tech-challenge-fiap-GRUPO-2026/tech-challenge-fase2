# 🎬 Roteiro do Vídeo de Demonstração

**Tech Challenge Fase 2 — Otimização de Rotas Médicas**
**Duração alvo: até 15 minutos**

---

## Estrutura Geral

| Seção | Tempo sugerido | Conteúdo |
|-------|:--------------:|---------|
| Abertura | 1 min | Contextualização do problema |
| Visão Geral | 2 min | Estrutura do repositório |
| Algoritmo Genético | 3 min | Núcleo da solução |
| Fitness e Restrições | 3 min | Penalidades do AG |
| Dados e Visualização | 3 min | Demo ao vivo TSP + VRP |
| Testes | 1 min | pytest passando |
| LLM e Experimentos | 2 min | Resultados e artefatos |
| Encerramento | 30 s | Resumo e próximos passos |

---

## 1. Abertura (1 min)

**O que falar:**
- Apresentar o Tech Challenge Fase 2 e o grupo
- Informar que o projeto escolhido foi o **Projeto 2**
- Explicar o problema: otimizar rotas de entrega de medicamentos e insumos em uma rede hospitalar
- Destacar o uso de **Algoritmos Genéticos** como solução

**Sugestão de fala:**
> "Nesta fase 2, resolvemos o Projeto 2: otimização de rotas médicas. O problema consiste em distribuir medicamentos e insumos hospitalares entre múltiplos pontos de entrega com restrições de prioridade, capacidade dos veículos e autonomia. A solução usa Algoritmos Genéticos para resolver o TSP e o VRP."

---

## 2. Visão Geral da Solução (2 min)

**O que mostrar:**
- Estrutura do repositório no editor ou terminal
- Explicar os diretórios principais: `src/`, `tests/`, `data/`, `docs/`, `config/`, `reports/`, `artifacts/`

**O que falar:**
- `src/` contém toda a lógica: AG, TSP, VRP, modelos, visualização, LLM, métricas
- `tests/` tem 62 testes automatizados
- `data/` contém os datasets CSV de entregas e veículos
- `config/` tem as configurações dos 5 experimentos VRP
- `artifacts/` guarda os resultados gerados automaticamente

---

## 3. Algoritmo Genético (3 min)

**O que mostrar:**
- Abrir `src/ga/genetic_algorithm.py` no editor

**O que falar:**
- Explicar a **representação**: no TSP, o indivíduo é uma permutação das entregas; no VRP, representa uma frota completa
- Explicar o ciclo evolutivo: população → avaliação → seleção por torneio → crossover → mutação → elitismo → nova geração
- Destacar que o objetivo é **minimizar o fitness** — soluções com valor menor são melhores
- Mencionar que no VRP, o crossover e a mutação operam sobre a frota inteira — podendo mover e trocar entregas entre veículos

---

## 4. Fitness e Restrições (3 min)

**O que mostrar:**
- A função de fitness no código (buscar o método correspondente)

**O que falar e mostrar:**

```
fitness = distância_total
        + penalidade_de_atraso
        + penalidade_de_capacidade
        + penalidade_de_autonomia
```

Detalhar cada componente:

| Componente | Implementado em | Penalidade |
|-----------|----------------|-----------|
| Distância da rota | Sprint 2 | Distância euclidiana total |
| Atraso por prioridade | Sprint 3 | HIGH: 100×, MEDIUM: 30×, LOW: 10× |
| Excesso de capacidade | Sprint 4 | 25× por kg acima do limite |
| Excesso de autonomia | Sprint 5 | 25× por unidade acima do alcance |

---

## 5. Dados e Visualização (3 min)

**O que mostrar antes de executar:**
- Mostrar `data/deliveries_sample.csv` — campos: id, x, y, weight, priority, deadline
- Mostrar `data/brazil_capitals_sample.csv` — 27 capitais brasileiras
- Mostrar `data/vehicles_sample.csv` — id, max_capacity, max_distance

**Executar e gravar: TSP com mapa do Brasil**
```bash
.venv/bin/python -m src.main \
  --deliveries-file data/brazil_capitals_sample.csv \
  --vehicle-id 3 \
  --population-size 100 \
  --mutation-probability 0.3 \
  --elite-size 2 \
  --fps 15
```

**O que destacar:**
- Fundo simplificado do mapa do Brasil aparece automaticamente com o dataset de capitais
- Rota vai melhorando geração a geração
- Gráfico de fitness ao lado mostra a curva de convergência

**Executar e gravar: VRP com múltiplos veículos**
```bash
.venv/bin/python -m src.main \
  --mode vrp \
  --vehicle-ids 1 3 5 \
  --deliveries-file data/brazil_capitals_sample.csv \
  --population-size 100 \
  --mutation-probability 0.3 \
  --elite-size 2 \
  --fps 15
```

**O que destacar:**
- Cada veículo tem uma cor diferente
- O tracado é progressivo — evolui junto com as gerações
- O gráfico mostra o fitness **agregado** da frota inteira
- O VRP distribui e otimiza a ordem das entregas em conjunto

---

## 6. Testes Automatizados (1 min)

**Executar e gravar:**
```bash
.venv/bin/python -m pytest
```

**O que destacar:**
- **62 testes passando** — cobertura de AG, fitness, TSP, VRP, LLM, CLI e dados
- Todos os testes funcionam offline, sem chave de API

---

## 7. LLM e Experimentos (2 min)

### Camada LLM

**Executar e mostrar a saída:**
```bash
.venv/bin/python -m src.llm \
  --mode vrp \
  --output report \
  --deliveries-file data/brazil_capitals_sample.csv
```

**O que falar:**
- A LLM funciona **sem chave de API** — modo offline determinístico
- Gera relatório textual com fitness, distâncias e entregas por veículo
- Com `--provider openai` usa a API real do GPT

### Experimentos VRP

**O que mostrar:**
- Abrir `artifacts/experiments/sprint8_summary.md` — tabela comparativa das 5 configurações
- Mostrar `artifacts/charts/fitness_curves.png` — curvas de convergência
- Mostrar `artifacts/charts/execution_time.png` — comparativo de tempo

**O que falar:**
- 5 configurações testadas em modo VRP: pop50, pop100, pop100_no_elitism, pop500, pop500_no_elitism
- Todas atingiram **fitness = 0.16** — mesma qualidade
- `pop50` foi **10× mais rápido** que `pop500` com o mesmo resultado

---

## 8. Encerramento (30 s)

**O que falar:**
> "O projeto entrega TSP e VRP com restrições operacionais reais, visualização interativa ao vivo, camada LLM para relatórios e instruções, 5 experimentos comparativos documentados e 62 testes automatizados passando. Como evolução futura, planejamos integrar malha viária real e operadores genéticos mais especializados para o VRP."

**Encerramento:**
- Mostrar o repositório: [github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2](https://github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2)
- Agradecer e encerrar

---

## ⚠️ Dicas de Gravação

- Use `--fps 15` para uma velocidade de animação visualmente clara no vídeo
- Grave o modo `brazil_capitals_sample.csv` — o mapa do Brasil torna a demonstração mais impactante
- Mostre o terminal com o pytest antes de encerrar
- Mantenha o terminal em fonte grande para legibilidade no vídeo
