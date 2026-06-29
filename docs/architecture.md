# 🏗️ Arquitetura do Sistema

**Tech Challenge Fase 2 — Otimização de Rotas Médicas com Algoritmos Genéticos**

---

## 📋 Escopo

Este projeto implementa o **Projeto 2 do Tech Challenge Fase 2**: otimização de rotas para distribuição de medicamentos e insumos usando Algoritmos Genéticos.

A solução cobre:
- **TSP** (Travelling Salesman Problem) — rota única com restrições de prioridade, capacidade e autonomia
- **VRP** (Vehicle Routing Problem) — múltiplos veículos com evolução conjunta da frota
- **Camada LLM** — relatórios operacionais, instruções para motoristas e Q&A sobre rotas
- **Visualização interativa** — Pygame (rotas animadas) + Matplotlib (curvas de fitness)
- **Experimentos comparativos** — 5 configurações do AG em modo VRP

---

## 🔄 Fluxo Principal de Dados

```
CSV de entregas + CSV de veículos
         │
         ▼
 src/data_loader.py          ← lê e valida os arquivos CSV
         │
         ▼
 Delivery / Vehicle          ← dataclasses tipadas (src/models/)
         │
         ▼
 TSPProblem / VRPProblem     ← encapsula o problema de otimização
         │
         ▼
 Algoritmo Genético          ← src/ga/genetic_algorithm.py
         │
         ▼
 TSPSolution / VRPSolution   ← melhor rota(s) + histórico de fitness
         │
         ├── Visualização Pygame    ← rota animada em tempo real
         ├── Gráfico Matplotlib     ← curva de evolução do fitness
         └── Camada LLM             ← relatórios e instruções em texto
```

---

## 🧩 Componentes

### 📂 Entrada de Dados — `src/data_loader.py`

Responsável por carregar e validar os arquivos CSV de entrada.

| Dataset | Arquivo padrão | Campos principais |
|---------|----------------|-------------------|
| Entregas | `data/deliveries_sample.csv` | `delivery_id`, `latitude`, `longitude`, `priority`, `weight`, `due_time` |
| Capitais BR | `data/brazil_capitals_sample.csv` | Mesmos campos — ativa mapa do Brasil na visualização |
| Veículos | `data/vehicles_sample.csv` | `vehicle_id`, `max_capacity`, `max_distance` |

---

### 📦 Modelos — `src/models/`

Dataclasses tipadas que representam o domínio do problema.

**`src/models/delivery.py`**
- `City` — ponto base (depósito ou coordenada genérica)
- `Delivery` — ponto de entrega com prioridade, peso e prazo

**`src/models/vehicle.py`**
- `Vehicle` — veículo com capacidade máxima e autonomia máxima

**`src/models/priority.py`**
- `Priority.HIGH` — penalidade de atraso 100×
- `Priority.MEDIUM` — penalidade de atraso 30×
- `Priority.LOW` — penalidade de atraso 10×

---

### 🧬 Algoritmo Genético — `src/ga/genetic_algorithm.py`

Núcleo da otimização. Implementa o ciclo evolutivo completo.

**Responsabilidades:**
- Geração da população inicial (aleatória + heurística)
- Cálculo de distância euclidiana entre pontos
- Cálculo do fitness (distância + penalidades)
- Crossover por ordem (OX — Order Crossover)
- Mutação por troca de posições adjacentes
- Elitismo — preservação dos `k` melhores indivíduos
- Iteração por gerações até critério de parada

> **Representação:** No TSP, cada indivíduo é uma **permutação** dos pontos de entrega. O depósito é mantido como ponto fixo inicial quando fornecido.

---

### 🗺️ Função de Fitness

O algoritmo **minimiza** este valor — soluções com fitness menor são melhores.

```
fitness = distância_total
        + penalidade_de_atraso
        + penalidade_de_capacidade
        + penalidade_de_autonomia
```

| Componente | Cálculo |
|-----------|---------|
| **Distância total** | Soma das distâncias euclidianas entre pontos consecutivos (rota fechada) |
| **Atraso HIGH** | `(chegada − due_time) × 100.0` por unidade de atraso |
| **Atraso MEDIUM** | `(chegada − due_time) × 30.0` por unidade de atraso |
| **Atraso LOW** | `(chegada − due_time) × 10.0` por unidade de atraso |
| **Excesso de capacidade** | `(peso_total − max_capacity) × 25.0` por unidade acima do limite |
| **Excesso de autonomia** | `(distância − max_distance) × 25.0` por unidade acima do limite |

Entregas sem `due_time` definido não recebem penalidade de atraso.

---

### 🚗 Roteamento — `src/routing/`

#### TSP — `src/routing/tsp.py`

Adapta o algoritmo genético para o problema de rota única.

Recebe como entrada:
- Lista de entregas
- Depósito opcional
- Veículo opcional (para ativar restrições de capacidade e autonomia)

#### VRP — `src/routing/vrp.py`

Expande o TSP para múltiplos veículos com evolução conjunta.

| Classe / Função | Responsabilidade |
|----------------|-----------------|
| `VRPProblem` | Encapsula entregas, veículos e depósito |
| `VRPRoute` | Rota resolvida para um único veículo |
| `VRPSolution` | Conjunto de rotas + fitness agregado da frota |
| `distribute_deliveries` | Heurística de solução inicial por prioridade/prazo/capacidade |
| `generate_fleet_population` | Gera população de soluções completas de frota |
| `fleet_crossover` | Crossover entre cromossomos de frota |
| `mutate_fleet` | Mutações que movem/trocam entregas entre veículos |
| `iterate_vrp` | Evolução geracional da frota completa |

**Cromossomo VRP:**
```
Indivíduo = frota completa

Veículo 1: Entrega A → C → F
Veículo 2: Entrega B → D
Veículo 3: Entrega E → G → H
```

**Fitness agregado:**
```
fitness_total = Σ fitness(rota de cada veículo)
```

---

### 🎮 Visualização — `src/visualization/` + `src/main.py`

Executa o demo visual com Pygame e Matplotlib lado a lado.

**Pygame (rota 2D):**
- Modo TSP: melhor rota atual + rota secundária da população
- Modo VRP: uma cor diferente por veículo, tracado progressivo por geração
- Dataset de capitais brasileiras: fundo simplificado do mapa do Brasil
- Argumento `--fps` controla a velocidade da animação

**Matplotlib (fitness):**
- Curva de evolução do fitness por geração
- Atualizada em tempo real durante a execução

---

### 🤖 Camada LLM — `src/llm/`

Transforma dados operacionais das rotas em texto legível.

| Arquivo | Responsabilidade |
|---------|-----------------|
| `src/llm/prompts.py` | Contexto da solução e prompts reutilizáveis |
| `src/llm/report_generator.py` | Relatório operacional da frota e instruções por motorista |
| `src/llm/route_explainer.py` | Respostas e explicações sobre rotas |
| `src/llm/openai_client.py` | Cliente OpenAI opcional |
| `src/llm/__main__.py` | Ponto de entrada via `python -m src.llm` |

**Funcionamento:**
- Sem cliente externo → respostas **determinísticas offline** (ideal para testes)
- Com `--provider openai` → envia mensagens reais à API da OpenAI

---

### 📊 Experimentos — `src/metrics/`

Runner para comparação sistemática de configurações do AG em modo VRP.

| Arquivo | Responsabilidade |
|---------|-----------------|
| `src/metrics/experiments.py` | Execução das configurações de experimento |
| `src/metrics/experiment_logger.py` | Exportação de CSV, JSON, Markdown e gráficos PNG |
| `src/metrics/statistics.py` | Métricas auxiliares |
| `src/metrics/__main__.py` | Ponto de entrada via `python -m src.metrics` |

---

### ⌨️ CLI — `src/main.py`

Comando principal:

```bash
.venv/bin/python -m src.main [opções]
```

| Opção | Padrão | Descrição |
|-------|--------|-----------|
| `--mode` | `tsp` | Modo de otimização: `tsp` ou `vrp` |
| `--vehicle-id` | 1º do CSV | Veículo usado no modo TSP |
| `--vehicle-ids` | todos | Veículos usados no modo VRP |
| `--population-size` | `100` | Número de indivíduos na população |
| `--mutation-probability` | `0.5` | Probabilidade de mutação |
| `--elite-size` | `1` | Indivíduos preservados por elitismo |
| `--fps` | `30` | Taxa de quadros da animação |
| `--deliveries-file` | `data/deliveries_sample.csv` | CSV de entregas |
| `--vehicles-file` | `data/vehicles_sample.csv` | CSV de veículos |

---

## ✅ Cobertura de Testes — `tests/`

62 testes passando com pytest. Cobrem:

| Área | Exemplos de testes |
|------|--------------------|
| AG — núcleo | Distância euclidiana, população inicial, crossover, mutação, histórico de fitness |
| Fitness | Rota fechada, penalidade por atraso (HIGH/MEDIUM/LOW), capacidade, autonomia |
| Dados | Carregamento de CSV de entregas e veículos |
| CLI | Parsing de argumentos, modo TSP/VRP, seleção de veículos |
| VRP | Distribuição de entregas, fitness agregado, estados geracionais, mutação de frota |
| LLM | Prompts, respostas offline, fallback sem chave de API |

---

## ⚠️ Limitações Atuais

| Limitação | Impacto |
|-----------|---------|
| Distâncias euclidianas em 2D | Não reflete rotas reais por malha viária |
| Operadores VRP simples | Crossover pode não preservar agrupamentos geográficos |
| LLM determinística por padrão | Cliente OpenAI é opcional e não demonstrado em produção |
| Mapa do Brasil simplificado | Fundo visual apenas — sem georeferenciamento real |

---

## 🚀 Evolução Futura

1. **Operadores VRP especializados** — preservar agrupamentos geográficos (cluster-first)
2. **Malha viária real** — integração com OSMnx ou APIs de roteirização
3. **VRPTW** — Vehicle Routing Problem with Time Windows
4. **AG híbrido** — busca local 2-opt ou Or-opt para refinamento pós-genético
5. **Cliente OpenAI concreto** — demonstração em produção com GPT-4o-mini
