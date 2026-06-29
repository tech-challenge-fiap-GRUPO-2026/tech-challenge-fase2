# 🏃 Sprint 4 — Capacidade Máxima dos Veículos

**Status:** ✅ Concluída

---

## 🎯 Objetivo

Adicionar **peso por entrega** e **capacidade máxima por veículo** ao problema de otimização — fazendo o algoritmo penalizar rotas que excedam a carga suportada pelo veículo.

---

## 📦 Modelos Atualizados

### `Delivery` — `src/models/delivery.py`

O campo `weight` foi adicionado ao modelo de entrega:

```python
@dataclass
class Delivery:
    id: str
    location: tuple[float, float]
    priority: Priority
    due_time: float | None
    weight: float                 # ← NOVO — peso da entrega em kg
```

### `Vehicle` — `src/models/vehicle.py`

O modelo de veículo foi criado nesta sprint:

```python
@dataclass
class Vehicle:
    id: str
    max_capacity: float           # capacidade máxima de carga (kg)
    max_distance: float | None    # autonomia máxima — adicionada na Sprint 5
```

---

## 📐 Regra de Fitness — Penalidade de Capacidade

O fitness agora inclui penalidade quando a **soma dos pesos das entregas da rota** excede `max_capacity` do veículo designado.

```
peso_total = Σ weight de todas as entregas da rota

if peso_total > max_capacity:
    penalty = (peso_total − max_capacity) × CAPACITY_EXCESS_PENALTY
```

Onde `CAPACITY_EXCESS_PENALTY = 25.0`.

### Exemplo prático

```
Veículo com max_capacity = 100 kg
Entregas: 40 kg + 35 kg + 40 kg = 115 kg

Excesso = 115 − 100 = 15 kg
Penalidade = 15 × 25.0 = 375.0 adicionado ao fitness
```

> O algoritmo **não impede** a alocação de entregas acima da capacidade — ele penaliza economicamente essa escolha para que soluções válidas sejam favorecidas pela seleção natural.

---

## 📂 Datasets

Dois arquivos CSV são usados nesta sprint:

| Arquivo | Conteúdo |
|---------|----------|
| `data/deliveries_sample.csv` | Entregas com campo `weight` preenchido |
| `data/vehicles_sample.csv` | Veículos com `max_capacity` definido |

---

## ⌨️ CLI — Novas Opções

O demo visual recebeu opções adicionais nesta sprint:

| Opção | Padrão | Descrição |
|-------|--------|-----------|
| `--vehicle-id <id>` | 1º do CSV | Seleciona o veículo pelo `id` no arquivo CSV |
| `--population-size <n>` | `100` | Tamanho da população do AG |
| `--mutation-probability <p>` | `0.5` | Probabilidade de mutação |
| `--deliveries-file <path>` | `data/deliveries_sample.csv` | Arquivo de entregas |
| `--vehicles-file <path>` | `data/vehicles_sample.csv` | Arquivo de veículos |

---

## ✅ Testes Implementados

| Cenário | Resultado esperado |
|---------|--------------------|
| Carregamento do CSV de veículos | Veículo com `id`, `max_capacity` e `max_distance` carregados corretamente |
| Rota dentro da capacidade | Nenhuma penalidade adicionada ao fitness |
| Rota acima da capacidade | `(excesso) × 25.0` adicionado ao fitness |
| Excesso zero (exatamente no limite) | Nenhuma penalidade (limite é inclusivo) |
