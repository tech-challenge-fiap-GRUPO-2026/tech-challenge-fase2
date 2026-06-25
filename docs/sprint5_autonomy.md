# Sprint 5 - Autonomia

## Objetivo

Adicionar distancia maxima por veiculo e penalizar rotas que excedam a autonomia.

## Modelo

O modelo `Vehicle` em `src/models/vehicle.py` contem:

- `id`
- `max_capacity`
- `max_distance` opcional

## Regra de fitness

O fitness continua sendo a distancia total da rota fechada somada as penalidades.

Se a distancia total da rota for maior que `max_distance`, o excesso recebe:

```text
penalty = excesso_de_distancia * DISTANCE_EXCESS_PENALTY
```

Onde `DISTANCE_EXCESS_PENALTY` vale `25.0`.

## Compatibilidade

Rotas sem veiculo continuam funcionando sem penalidade de autonomia.

## Testes

Os testes cobrem:

- penalizacao quando a distancia maxima e excedida;
- ausencia de penalizacao quando a distancia fica dentro do limite;
- propagacao da autonomia no TSP e no algoritmo genetico.
