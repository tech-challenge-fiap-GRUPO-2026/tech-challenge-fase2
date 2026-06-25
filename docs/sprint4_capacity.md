# Sprint 4 - Capacidade

## Objetivo

Adicionar peso por entrega e capacidade maxima por veiculo ao fitness.

## Modelo

O modelo `Delivery` agora inclui:

- `weight`: peso da entrega;
- `priority`: mantida da Sprint 3;
- `due_time`: mantido da Sprint 3.

O modelo `Vehicle` fica em `src/models/vehicle.py` e inclui:

- `id`
- `max_capacity`
- `max_distance` opcional

## Regra de fitness

O fitness continua sendo a distancia da rota somada as penalidades.

Para capacidade, o algoritmo soma o peso total da rota e compara com `max_capacity`.

Se houver excesso, aplica:

```text
penalty = excesso_de_peso * CAPACITY_EXCESS_PENALTY
```

Onde `CAPACITY_EXCESS_PENALTY` vale `25.0`.

## Dados

Os arquivos de exemplo usados nesta sprint sao:

- `data/deliveries_sample.csv`
- `data/vehicles_sample.csv`

## Execucao

O demo visual aceita a opcao:

- `--vehicle-id <id>`: seleciona qual veiculo do CSV sera usado. Padrao: primeiro veiculo do arquivo.
- `--population-size <n>`: define o tamanho da populacao. Padrao: `100`.
- `--mutation-probability <p>`: define a probabilidade de mutacao. Padrao: `0.5`.
- `--deliveries-file <path>`: define o arquivo de entregas. Padrao: `data/deliveries_sample.csv`.
- `--vehicles-file <path>`: define o arquivo de veiculos. Padrao: `data/vehicles_sample.csv`.

## Testes

Os testes cobrem:

- carregamento do CSV de veiculos;
- penalizacao quando a capacidade e excedida;
- ausencia de penalidade quando a carga cabe no veiculo.
