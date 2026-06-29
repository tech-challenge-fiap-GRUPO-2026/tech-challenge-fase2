# 🏃 Sprint 3 — Prioridades de Entrega

**Status:** ✅ Concluída

---

## 🎯 Objetivo

Adicionar **três níveis de prioridade** às entregas e atualizar a função de fitness para penalizar rotas que causem atrasos — especialmente em entregas críticas.

---

## 📦 Modelo de Prioridade

As prioridades são definidas em `src/models/priority.py` como um enum com três valores:

| Prioridade | Significado | Penalidade por unidade de atraso |
|:----------:|-------------|:--------------------------------:|
| `HIGH` | Medicamento urgente — tolerância zero | **100.0×** |
| `MEDIUM` | Insumo importante — prazo flexível | **30.0×** |
| `LOW` | Material eletivo — menor urgência | **10.0×** |

O modelo `Delivery` em `src/models/delivery.py` foi atualizado com:

```python
@dataclass
class Delivery:
    id: str                       # identificador único da entrega
    location: tuple[float, float] # coordenada (x, y)
    priority: Priority            # HIGH, MEDIUM ou LOW
    due_time: float | None        # prazo máximo de chegada (ou None)
```

---

## 📐 Regra de Fitness

O fitness continua sendo a **distância total da rota fechada**, agora somada às penalidades de atraso por prioridade.

### Cálculo da Penalidade

```
penalty = (arrival_time − due_time) × fator_da_prioridade
```

Onde:
- `arrival_time` = distância acumulada até a entrega (proxy de tempo)
- `due_time` = prazo definido na entrega
- A penalidade só é aplicada quando `arrival_time > due_time`

### Exemplo prático

```
Entrega HIGH com due_time = 50 chegando em t = 60:
  atraso = 60 − 50 = 10
  penalty = 10 × 100.0 = 1000.0 adicionado ao fitness
```

> Entregas sem `due_time` definido (valor `None`) **não recebem penalidade** — o algoritmo trata a ausência de prazo como tolerância ilimitada.

---

## 🔄 Compatibilidade com Sprint 2

A Sprint 3 foi implementada de forma **retrocompatível**:

- Rotas compostas apenas por tuplas `(x, y)` continuam funcionando sem alterações
- O TSP migrado na Sprint 2 não foi quebrado
- A adição de `priority` e `due_time` é opcional no modelo `Delivery`

Isso permite evoluir gradualmente do TSP genérico para entregas médicas com restrições reais.

---

## ✅ Testes Implementados

| Cenário | Resultado esperado |
|---------|--------------------|
| Entrega `HIGH` dentro do prazo | Fitness sem penalidade de atraso |
| Entrega `HIGH` com atraso | Fitness + `atraso × 100.0` |
| Entrega `MEDIUM` com atraso | Fitness + `atraso × 30.0` |
| Entrega `LOW` com atraso | Fitness + `atraso × 10.0` |
| Entrega sem `due_time` | Nenhuma penalidade aplicada |
