# 🏃 Sprint 5 — Autonomia Máxima dos Veículos

**Status:** ✅ Concluída

---

## 🎯 Objetivo

Adicionar **distância máxima percorrida por rota** às restrições do veículo — fazendo o algoritmo penalizar rotas que excedam o alcance operacional do veículo.

---

## 📦 Modelo Atualizado — `Vehicle`

O campo `max_distance` existia como opcional desde a Sprint 4 e foi ativado nesta sprint:

```python
@dataclass
class Vehicle:
    id: str
    max_capacity: float           # capacidade máxima de carga (Sprint 4)
    max_distance: float | None    # ← ATIVADO — autonomia máxima em unidades de distância
```

Quando `max_distance` é `None`, nenhuma penalidade de autonomia é aplicada — preservando retrocompatibilidade com rotas sem restrição de alcance.

---

## 📐 Regra de Fitness — Penalidade de Autonomia

O fitness agora inclui penalidade quando a **distância total da rota fechada** excede `max_distance` do veículo.

```
distância_total = Σ distância entre pontos consecutivos (incluindo retorno ao depósito)

if distância_total > max_distance:
    penalty = (distância_total − max_distance) × DISTANCE_EXCESS_PENALTY
```

Onde `DISTANCE_EXCESS_PENALTY = 25.0`.

### Exemplo prático

```
Veículo com max_distance = 200 unidades
Distância total da rota = 245 unidades

Excesso = 245 − 200 = 45
Penalidade = 45 × 25.0 = 1125.0 adicionado ao fitness
```

### Composição atual do fitness após Sprint 5

```
fitness = distância_total
        + penalidade_de_atraso         (Sprint 3)
        + penalidade_de_capacidade     (Sprint 4)
        + penalidade_de_autonomia      (Sprint 5 — NOVO)
```

---

## 🔄 Compatibilidade

- Rotas **sem veículo** associado não recebem penalidade de autonomia
- Veículos com `max_distance = None` também não são penalizados
- O TSP e os testes das sprints anteriores continuam passando sem alteração

---

## ✅ Testes Implementados

| Cenário | Resultado esperado |
|---------|--------------------|
| Rota dentro da autonomia | Nenhuma penalidade de distância |
| Rota acima da autonomia | `(excesso) × 25.0` adicionado ao fitness |
| Veículo sem `max_distance` | Nenhuma penalidade (campo `None`) |
| Propagação no TSP | O `TSPSolver` passa `max_distance` corretamente ao fitness |
| Propagação no AG | `genetic_algorithm.py` respeita a restrição de autonomia |

---

## 🔗 Relação com Outras Sprints

| Sprint | Penalidade adicionada |
|--------|-----------------------|
| Sprint 3 | Atraso por prioridade (HIGH/MEDIUM/LOW) |
| Sprint 4 | Excesso de capacidade do veículo |
| **Sprint 5** | **Excesso de autonomia do veículo** ← esta sprint |
| Sprint 6 | Fitness agregado da frota (VRP) |
