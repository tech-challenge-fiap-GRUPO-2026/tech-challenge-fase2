# Relatório Técnico — Projeto 2

**Tech Challenge Fase 2 · Pós-Graduação em IA para Desenvolvedores · FIAP 2026**

---

## Equipe

| Nome | E-mail |
|------|--------|
| Jefferson Antônio Pantoja Silva | jeffkd35@gmail.com |
| Wilson Lima da Silva | wilson.slima@gmail.com |
| Gustavo Lopes da Silva | gustavo_lsilva@hotmail.com |
| Felipe Soeiro Lopes | felipesoeiro.contato@outlook.com.br |
| Vinicius Tavares Sousa da Silva | viniciustavares2014@gmail.com |

---

## 1. Introdução

Este relatório documenta o desenvolvimento do **Projeto 2 do Tech Challenge Fase 2**: um sistema de otimização de rotas médicas para distribuição de medicamentos e insumos hospitalares.

O projeto parte de um código base de TSP (Travelling Salesman Problem) e evolui incrementalmente em **9 sprints** para um resolvedor completo com:
- Restrições operacionais reais (prioridade, capacidade, autonomia)
- VRP (Vehicle Routing Problem) com múltiplos veículos
- Visualização interativa com Pygame e mapa do Brasil
- Camada LLM para geração de relatórios e instruções
- Suite de experimentos comparativos com artefatos reproduzíveis
- **62 testes automatizados passando**

---

## 2. Fundamentação Teórica

### 2.1 Algoritmos Genéticos

Algoritmos Genéticos (AG) são métodos de otimização inspirados em processos evolutivos da natureza. Uma população de soluções candidatas é criada, avaliada por uma função fitness e evoluída ao longo de gerações por operadores de:

- **Seleção** — favorece soluções com melhor fitness (torneio)
- **Crossover** — combina material genético de dois pais para gerar filhos
- **Mutação** — introduz variações aleatórias para manter diversidade
- **Elitismo** — preserva os melhores indivíduos entre gerações

Ao longo das gerações, a população tende a convergir para soluções cada vez melhores — sem garantia de ótimo global, mas com boa aproximação prática para problemas combinatórios complexos.

### 2.2 Problema do Caixeiro Viajante (TSP)

O TSP busca encontrar a **rota mais curta** que visita todos os pontos exatamente uma vez e retorna ao ponto inicial. No contexto do projeto, os pontos representam pontos de entrega de medicamentos e o depósito é o ponto de partida da rota.

Representação: cada indivíduo é uma **permutação** dos pontos de entrega.

### 2.3 Vehicle Routing Problem (VRP)

O VRP generaliza o TSP para **múltiplos veículos e múltiplas rotas simultâneas**. O objetivo é distribuir as entregas entre os veículos e otimizar a ordem de visita de cada um, respeitando restrições de capacidade e autonomia.

No projeto, o VRP usa um **cromossomo de frota**: cada indivíduo representa toda a distribuição de entregas entre os veículos, permitindo que o AG evolua simultaneamente a distribuição e a ordem das rotas.

### 2.4 Large Language Models (LLM)

LLMs transformam dados operacionais estruturados em linguagem natural legível para humanos. No projeto, a camada LLM recebe objetos `TSPSolution` ou `VRPSolution` e gera relatórios, instruções por motorista e respostas a perguntas sobre as rotas.

A integração com OpenAI é opcional — o sistema funciona offline com respostas determinísticas.

---

## 3. Metodologia

O projeto foi conduzido em 9 sprints incrementais, cada uma adicionando uma funcionalidade verificável:

| Sprint | Funcionalidade |
|--------|---------------|
| 1 | Análise do código base e plano de extensão |
| 2 | Migração do TSP para `src/` com dataclasses, type hints e testes |
| 3 | Prioridades de entrega (HIGH/MEDIUM/LOW) e penalidade por atraso |
| 4 | Peso das entregas e capacidade máxima dos veículos |
| 5 | Autonomia máxima por veículo |
| 6 | VRP com múltiplos veículos e cromossomo de frota |
| 7 | Camada LLM para relatórios, instruções e Q&A |
| 8 | Experimentos comparativos em VRP com 5 configurações |
| 9 | Consolidação — relatório, roteiro de vídeo e manifesto de artefatos |

A validação foi feita com testes automatizados usando `pytest` ao longo de todas as sprints.

---

## 4. Implementação

### 4.1 Estrutura do Projeto

```
tech-challenge-fase2/
├── src/
│   ├── ga/genetic_algorithm.py     # AG: população, crossover, mutação, fitness
│   ├── routing/tsp.py              # Resolvedor TSP
│   ├── routing/vrp.py              # Resolvedor VRP (cromossomo de frota)
│   ├── models/                     # Delivery, Vehicle, City, Priority
│   ├── visualization/              # Pygame (rota) + Matplotlib (fitness)
│   ├── llm/                        # Prompts, relatórios, Q&A, cliente OpenAI
│   ├── metrics/                    # Runner de experimentos e exportação de artefatos
│   ├── data_loader.py              # Leitura de CSV
│   └── main.py                     # CLI + demo visual
├── tests/                          # 62 testes automatizados
├── data/                           # Datasets CSV de exemplo
├── config/                         # Configurações dos experimentos (YAML)
├── docs/                           # Documentação técnica por sprint
├── reports/                        # Relatório consolidado
└── artifacts/                      # Artefatos gerados pelos experimentos
```

### 4.2 Função de Fitness

O algoritmo **minimiza** o fitness — valores menores indicam soluções melhores.

```
fitness = distância_total
        + penalidade_de_atraso
        + penalidade_de_capacidade
        + penalidade_de_autonomia
```

Penalidades implementadas:

| Componente | Cálculo |
|-----------|---------|
| Atraso `HIGH` | `(chegada − due_time) × 100.0` |
| Atraso `MEDIUM` | `(chegada − due_time) × 30.0` |
| Atraso `LOW` | `(chegada − due_time) × 10.0` |
| Excesso de capacidade | `(peso_total − max_capacity) × 25.0` |
| Excesso de autonomia | `(distância − max_distance) × 25.0` |

### 4.3 Datasets

| Arquivo | Conteúdo |
|---------|----------|
| `data/deliveries_sample.csv` | Entregas sintéticas com prioridade, peso e prazo |
| `data/brazil_capitals_sample.csv` | 27 capitais brasileiras — ativa mapa do Brasil na visualização |
| `data/vehicles_sample.csv` | Veículos com capacidade máxima e autonomia máxima |

### 4.4 VRP — Cromossomo de Frota

Cada indivíduo no VRP representa a frota completa:

```
Indivíduo:
  Veículo 1: Entrega A → C → F
  Veículo 2: Entrega B → D
  Veículo 3: Entrega E → G → H
```

O fitness total é a soma dos fitness individuais de cada rota, avaliados com as restrições do próprio veículo.

Operadores específicos do VRP:
- **Crossover de frota** — combina sequência global de entregas de dois pais com a divisão de rotas de um deles
- **Mutação inter-rota** — move ou troca entregas entre veículos
- **Mutação intra-rota** — reordena entregas dentro de um único veículo

### 4.5 Camada LLM

A camada LLM em `src/llm/` funciona de forma desacoplada e testável:

```
TSPSolution / VRPSolution
       │
       ▼
prompts.py  → monta contexto e prompt
       │
       ▼
report_generator.py / route_explainer.py  → gera texto
       │
       ▼
openai_client.py  → opcional: envia ao provedor externo
```

Modos de saída disponíveis: `report`, `instructions`, `question`

---

## 5. Experimentos VRP

A Sprint 8 executou 5 configurações do AG em modo VRP para comparar qualidade, velocidade de convergência e custo computacional.

### 5.1 Configurações

| Configuração | Pop. | Mutação | Crossover | Elitismo | Pool | Gerações |
|:------------|:----:|:-------:|:---------:|:--------:|:----:|:--------:|
| pop50 | 50 | 0.14 | 0.68 | 1 | 6 | 500 |
| pop100 | 100 | 0.08 | 0.80 | 2 | 10 | 500 |
| pop100_no_elitism | 100 | 0.08 | 0.80 | 0 | 10 | 500 |
| pop500 | 500 | 0.02 | 0.90 | 6 | 20 | 500 |
| pop500_no_elitism | 500 | 0.02 | 0.90 | 0 | 20 | 500 |

### 5.2 Resultados

| Configuração | Fitness Final | Convergência | Tempo | Melhoria |
|:------------|:-------------:|:------------:|:-----:|:--------:|
| **pop50** ⭐ | 0.16 | Gen. 103 | 1.323s | 0.40 |
| pop100 | 0.16 | Gen. 187 | 2.588s | 0.40 |
| pop100_no_elitism | 0.16 | Gen. 176 | 2.639s | 0.40 |
| pop500 | 0.16 | Gen. 33 | 13.404s | 0.35 |
| pop500_no_elitism | 0.16 | Gen. 33 | 13.425s | 0.35 |

### 5.3 Análise

**Todas as 5 configurações atingiram fitness = 0.16** — demonstrando robustez do algoritmo.

**`pop50` apresentou o melhor equilíbrio:**
- Mesmo fitness final que `pop500`
- **10× mais rápido** (1.3s vs 13.4s)
- Convergência na geração 103 — razoavelmente eficiente

**Impacto do elitismo:**
- `pop100_no_elitism` convergiu 11 gerações antes do `pop100` sem perda de fitness
- `pop500_no_elitism` manteve a mesma convergência com tempo levemente maior
- Elitismo não foi fator determinante neste dataset

**Custo de populações maiores:**
- `pop500` convergiu mais rápido em número de gerações (33 vs 103)
- Porém cada geração é muito mais cara — custo total 10× maior

---

## 6. Resultados Consolidados

| Funcionalidade | Status |
|---------------|--------|
| TSP com AG e visualização Pygame | ✅ |
| VRP com múltiplos veículos e cromossomo de frota | ✅ |
| Fitness com distância, atraso, capacidade e autonomia | ✅ |
| Mapa do Brasil na visualização (dataset de capitais) | ✅ |
| Leitura de entregas e veículos via CSV | ✅ |
| CLI configurável com todos os parâmetros do AG | ✅ |
| Camada LLM testável — offline e com OpenAI | ✅ |
| 5 experimentos comparativos VRP com artefatos | ✅ |
| Suite de testes automatizados | ✅ |

**Última validação:**
```
62 passed
```

---

## 7. Trabalhos Futuros

1. **Operadores VRP especializados** — crossover cluster-first para preservar agrupamentos geográficos
2. **Malha viária real** — substituir distâncias euclidianas por rotas OSMnx ou Google Maps API
3. **VRPTW** — Vehicle Routing Problem with Time Windows para modelagem mais precisa
4. **AG híbrido** — busca local 2-opt ou Or-opt para refinamento pós-genético
5. **Cliente OpenAI concreto** — demonstração em produção com GPT-4o-mini e casos reais

---

## 8. Referências

- Documento do Tech Challenge Fase 2 — FIAP
- Código base em `references/` — ponto de partida do projeto
- Documentação técnica incremental em `docs/` — uma por sprint
- Repositório: [github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2](https://github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2)
