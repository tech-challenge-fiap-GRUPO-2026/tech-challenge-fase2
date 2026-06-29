# 🏃 Sprint 6 — VRP: Múltiplos Veículos e Frota Evolutiva

**Status:** ✅ Concluída

---

## 🎯 Objetivo

Expandir o TSP para um **Vehicle Routing Problem (VRP)** completo — com múltiplos veículos, cromossomo de frota e evolução conjunta da distribuição de entregas entre os veículos.

---

## 🗺️ O que é o VRP?

Enquanto o TSP encontra a rota mais curta para **um único veículo**, o VRP otimiza **toda a frota simultaneamente**:

- Cada veículo recebe um subconjunto das entregas
- A ordem de visita dentro de cada rota também é otimizada
- As restrições de capacidade e autonomia de cada veículo são respeitadas

---

## 📦 Novos Modelos — `src/routing/vrp.py`

| Classe | Responsabilidade |
|--------|-----------------|
| `VRPProblem` | Encapsula entregas, lista de veículos e depósito opcional |
| `VRPRoute` | Rota resolvida para um único veículo — inclui lista de entregas e fitness individual |
| `VRPSolution` | Conjunto completo de rotas da frota + fitness agregado |

---

## 🧬 Cromossomo de Frota

No VRP, cada **indivíduo** da população representa uma **frota completa** — não apenas uma rota:

```
Indivíduo (frota):
  Veículo 1: Entrega A → C → F  (retorna ao depósito)
  Veículo 2: Entrega B → D      (retorna ao depósito)
  Veículo 3: Entrega E → G → H  (retorna ao depósito)
```

Isso significa que o algoritmo evolui ao mesmo tempo:
- **Quais entregas** cada veículo faz
- **Em que ordem** cada veículo as visita

---

## 🏁 Geração da População Inicial

A população inicial combina dois tipos de soluções para equilibrar qualidade e diversidade:

**1. Solução Heurística (determinística)**

Ordena as entregas por prioridade → prazo → id e distribui nos veículos tentando respeitar `max_capacity`:

```
prioridade: HIGH primeiro → MEDIUM → LOW
dentro da mesma prioridade: menor due_time primeiro
```

**2. Soluções Aleatórias (estocásticas)**

Distribuições e ordens aleatórias para garantir diversidade genética na população.

---

## ⚙️ Operadores Genéticos do VRP

### Crossover de Frota — `fleet_crossover`

Combina a sequência global de entregas de dois indivíduos (pais) e reaproveita a divisão de rotas de um deles:

```
Pai 1: sequência global [A, B, C, D, E, F]  +  divisão [2, 2, 2]
Pai 2: sequência global [D, A, F, B, C, E]

Filho: sequência do Pai 2  +  divisão do Pai 1
  → Veículo 1: D, A
  → Veículo 2: F, B
  → Veículo 3: C, E
```

### Mutação de Frota — `mutate_fleet`

Três tipos de mutação, escolhidos aleatoriamente:

| Tipo | Descrição |
|------|-----------|
| **Mover entrega** | Move uma entrega de um veículo para outro |
| **Trocar entregas** | Troca uma entrega entre dois veículos diferentes |
| **Reordenar rota** | Altera a ordem de visita dentro de uma rota (swap interno) |

---

## 📐 Fitness Agregado da Frota

Cada rota de veículo é avaliada individualmente com as **suas próprias restrições**:

```
fitness(rota_v) = distância(rota_v)
               + penalidade_atraso(rota_v)
               + penalidade_capacidade(rota_v, veículo_v.max_capacity)
               + penalidade_autonomia(rota_v, veículo_v.max_distance)
```

O fitness total da frota é a **soma de todos os fitness individuais**:

```
fitness_total = Σ fitness(rota_v)  para todo veículo v
```

O algoritmo minimiza `fitness_total` — a frota inteira melhora em conjunto.

---

## 🎮 Visualização VRP

O demo visual em modo `vrp` usa `iterate_vrp` para animar a evolução por geração:

- Cada veículo recebe uma **cor diferente** na visualização
- O tracado é **progressivo** — evita mostrar todas as rotas completas no primeiro frame
- O gráfico de fitness exibe o **histórico agregado da frota** por geração
- Dataset de capitais brasileiras ativa o **fundo simplificado do mapa do Brasil**

### Comandos de execução

```bash
# Todos os veículos do CSV
.venv/bin/python -m src.main \
  --mode vrp \
  --deliveries-file data/brazil_capitals_sample.csv \
  --population-size 100 \
  --mutation-probability 0.3 \
  --elite-size 2 \
  --fps 15

# Frota específica (veículos 1, 3 e 5)
.venv/bin/python -m src.main \
  --mode vrp \
  --vehicle-ids 1 3 5 \
  --deliveries-file data/brazil_capitals_sample.csv \
  --population-size 100
```

---

## ✅ Testes Implementados

| Cenário | Resultado esperado |
|---------|--------------------|
| Alocação de entregas | Todas as entregas aparecem em alguma rota (nenhuma perdida) |
| Sem veículos | Erro descritivo levantado |
| Uma rota por veículo | Cada veículo tem exatamente uma rota |
| Fitness agregado | Soma correta dos fitness individuais |
| Penalidade de capacidade | Aplicada por rota individualmente |
| Parsing CLI | `--mode vrp` reconhecido corretamente |
| Seleção de veículos | `--vehicle-ids` filtra corretamente a frota |
| Histórico de fitness | Registrado por geração para todos os veículos |
| Estados geracionais | `iterate_vrp` retorna estados intermediários corretos |
| População inicial | Cada entrega aparece exatamente uma vez por solução |
| Mutação de frota | Distribuição/rotas alteradas sem perder ou duplicar entregas |

---

## ⚠️ Limitações desta Sprint

- Os operadores genéticos ainda são simples — o crossover pode não preservar agrupamentos geográficos ideais
- As distâncias continuam euclidianas em 2D (sem malha viária real)
- A visualização é abstrata — sem georeferenciamento real mesmo com o dataset de capitais
