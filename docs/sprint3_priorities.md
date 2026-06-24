# Sprint 3 - Prioridades

## Objetivo

Adicionar prioridades de entrega e atualizar o fitness para penalizar atraso em entregas `HIGH`.

## Modelo

As prioridades ficam em `src/models/priority.py`:

- `HIGH`
- `MEDIUM`
- `LOW`

O modelo `Delivery` fica em `src/models/delivery.py` e contem:

- `id`: identificador da entrega;
- `location`: coordenada `(x, y)`;
- `priority`: prioridade da entrega;
- `due_time`: limite maximo de chegada usado para calcular atraso.

## Regra de fitness

O fitness continua sendo a distancia total da rota fechada.

Para entregas com prioridade `HIGH`, `MEDIUM` ou `LOW`, o fitness recebe penalizacao quando o tempo de chegada acumulado ultrapassa `due_time`.

O fator de penalizacao depende da prioridade:

| Prioridade | Fator   |
|------------|---------|
| `HIGH`     | `100.0` |
| `MEDIUM`   | `30.0`  |
| `LOW`      | `10.0`  |

Formula da penalizacao:

```text
penalty = (arrival_time - due_time) * fator_da_prioridade
```

Onde:

- `arrival_time` e a distancia acumulada ate a entrega;
- `due_time` e o prazo da entrega;
- `HIGH_PRIORITY_DELAY_PENALTY` vale `100.0`.

Entregas sem `due_time` nao recebem penalizacao.

## Compatibilidade

Rotas compostas apenas por tuplas `(x, y)` continuam funcionando como antes.

Isso preserva o TSP migrado na Sprint 2 e permite evoluir gradualmente para entregas medicas.

## Testes

Os testes da Sprint 3 cobrem:

- entrega `HIGH` sem atraso;
- entrega `HIGH` com atraso;
- entrega `MEDIUM` com atraso;
- entrega `LOW` com atraso.
