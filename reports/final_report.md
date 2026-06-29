<div align="center">

# 🚚 Relatório Técnico — Projeto 2

## Otimização de Rotas Médicas com Algoritmos Genéticos

**Tech Challenge Fase 2 · Pós-Graduação em IA para Desenvolvedores · FIAP 2026**

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green?logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557c?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-62%20passed-0A9EDC?logo=pytest&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-opcional-412991?logo=openai&logoColor=white)

</div>

---

## 👥 Equipe

| # | Nome | E-mail |
|:-:|------|--------|
| 1 | Jefferson Antônio Pantoja Silva | jeffkd35@gmail.com |
| 2 | Wilson Lima da Silva | wilson.slima@gmail.com |
| 3 | Gustavo Lopes da Silva | gustavo_lsilva@hotmail.com |
| 4 | Felipe Soeiro Lopes | felipesoeiro.contato@outlook.com.br |
| 5 | Vinicius Tavares Sousa da Silva | viniciustavares2014@gmail.com |

---

## 📑 Sumário

1. [Introdução](#1-introdução)
2. [Fundamentação Teórica](#2-fundamentação-teórica)
3. [Tecnologias Utilizadas](#3-tecnologias-utilizadas)
4. [Metodologia](#4-metodologia)
5. [Implementação](#5-implementação)
6. [Experimentos VRP](#6-experimentos-vrp)
7. [Resultados Consolidados](#7-resultados-consolidados)
8. [Trabalhos Futuros](#8-trabalhos-futuros)
9. [Referências](#9-referências)

---

## 1. Introdução

Este relatório documenta o desenvolvimento completo do **Projeto 2 do Tech Challenge Fase 2**: um sistema de otimização de rotas médicas para distribuição de medicamentos e insumos hospitalares com Algoritmos Genéticos.

### 1.1 Contexto e Problema

A distribuição eficiente de medicamentos e insumos em redes hospitalares é um problema logístico crítico. Atrasos em entregas de alta prioridade podem impactar diretamente o atendimento ao paciente. O problema envolve:

- **Múltiplos pontos de entrega** com coordenadas geográficas
- **Prioridades diferenciadas** — medicamentos urgentes vs. materiais eletivos
- **Restrições de capacidade** — peso máximo por veículo
- **Restrições de autonomia** — distância máxima percorrida por rota
- **Frota heterogênea** — múltiplos veículos com características distintas

### 1.2 Abordagem Adotada

O projeto parte de um código base de TSP e evolui incrementalmente em **9 sprints** para um resolvedor completo com:

| Componente | Descrição |
|-----------|-----------|
| **TSP com AG** | Rota única com restrições operacionais e visualização em tempo real |
| **VRP com cromossomo de frota** | Múltiplos veículos com evolução conjunta da distribuição |
| **Visualização Pygame** | Animação 2D interativa com mapa do Brasil |
| **Camada LLM** | Relatórios, instruções e Q&A em linguagem natural |
| **Suite de experimentos** | 5 configurações comparadas com artefatos reproduzíveis |
| **Testes automatizados** | 62 testes pytest passando — 100% |

> 🔗 **Página de resultados:** [tech-challenge-fiap-grupo-2026.github.io/tech-challenge-fase2/index.html](https://tech-challenge-fiap-grupo-2026.github.io/tech-challenge-fase2/index.html)

---

## 2. Fundamentação Teórica

### 2.1 Algoritmos Genéticos

Algoritmos Genéticos (AG) são metaheurísticas de otimização inspiradas nos mecanismos de seleção natural e genética. Foram propostos por John Holland na década de 1970 e são amplamente utilizados em problemas combinatórios NP-difíceis como TSP e VRP.

**Ciclo evolutivo:**

```
Inicialização da população
         │
         ▼
Avaliação do fitness (função objetivo)
         │
         ▼
Critério de parada ──── Sim ──→ Melhor solução
         │ Não
         ▼
Seleção (torneio)
         │
         ▼
Crossover (recombinação genética)
         │
         ▼
Mutação (perturbação aleatória)
         │
         ▼
Elitismo (preservação dos melhores)
         │
         └──────────────────────────────▶ Nova geração
```

**Operadores implementados:**

| Operador | Mecanismo | Papel no AG |
|----------|-----------|-------------|
| **Seleção** | Torneio — compara `k` indivíduos aleatórios | Pressão seletiva — favorece os melhores |
| **Crossover OX** | Order Crossover — preserva sub-sequências | Herança de boas sub-rotas entre pais |
| **Mutação (swap)** | Troca aleatória de duas posições | Exploração de soluções vizinhas |
| **Mutação (inversão)** | Inverte um segmento da rota | Perturbação estrutural maior |
| **Elitismo** | Copia os `k` melhores para a próxima geração | Evita perda do melhor encontrado |

### 2.2 Problema do Caixeiro Viajante (TSP)

O **Travelling Salesman Problem** é um problema NP-difícil clássico: encontrar o menor ciclo hamiltoniano em um grafo completo — ou seja, a rota mais curta que visita todos os nós exatamente uma vez e retorna ao ponto inicial.

No contexto médico deste projeto:
- **Nós** = pontos de entrega de medicamentos + depósito
- **Arestas** = distâncias euclidianas entre os pontos
- **Restrição adicional** = prioridade, peso e prazo de cada entrega

**Representação:** cada indivíduo é uma permutação `[d₁, d₂, ..., dₙ]` dos índices das entregas. O depósito é mantido fixo no início e no fim.

### 2.3 Vehicle Routing Problem (VRP)

O **Vehicle Routing Problem** generaliza o TSP para múltiplos veículos: encontrar o conjunto ótimo de rotas para uma frota que sirva todos os clientes, minimizando o custo total.

No projeto, o VRP usa um **cromossomo de frota** — cada indivíduo representa a distribuição completa:

```
Cromossomo de frota (exemplo com 3 veículos, 7 entregas):

  Veículo 1 ──→ [A] ──→ [C] ──→ [F] ──→ depósito
  Veículo 2 ──→ [B] ──→ [D] ──→ depósito
  Veículo 3 ──→ [E] ──→ [G] ──→ depósito
```

O AG evolui simultaneamente:
- **Quais entregas** cada veículo realiza
- **Em que ordem** cada veículo as visita

### 2.4 Função de Fitness

O algoritmo **minimiza** o fitness. Valores menores = soluções melhores.

```
fitness = distância_total
        + penalidade_de_atraso
        + penalidade_de_capacidade
        + penalidade_de_autonomia
```

| Componente | Fórmula | Constante |
|-----------|---------|-----------|
| Distância total | `Σ dist(pᵢ, pᵢ₊₁)` — rota fechada incluindo retorno | — |
| Atraso `HIGH` | `(chegada − due_time) × 100.0` | `HIGH_PENALTY = 100.0` |
| Atraso `MEDIUM` | `(chegada − due_time) × 30.0` | `MEDIUM_PENALTY = 30.0` |
| Atraso `LOW` | `(chegada − due_time) × 10.0` | `LOW_PENALTY = 10.0` |
| Excesso de capacidade | `(peso_total − max_capacity) × 25.0` | `CAPACITY_PENALTY = 25.0` |
| Excesso de autonomia | `(distância − max_distance) × 25.0` | `DISTANCE_PENALTY = 25.0` |

> **Nota:** penalidades são aditivas — uma entrega pode acumular atraso + capacidade excedida simultaneamente.

### 2.5 Large Language Models (LLM)

LLMs transformam dados operacionais estruturados em linguagem natural. No projeto, a camada LLM recebe objetos `TSPSolution` ou `VRPSolution` e gera três tipos de saída:

| Modo | Descrição | Público-alvo |
|------|-----------|-------------|
| `report` | Relatório operacional com fitness, rotas e tempos | Gestores de logística |
| `instructions` | Lista de entregas ordenada por veículo | Motoristas |
| `question` | Resposta em linguagem natural sobre a rota | Qualquer usuário |

---

## 3. Tecnologias Utilizadas

| Biblioteca | Versão | Uso no Projeto |
|-----------|--------|---------------|
| `Python` | 3.12+ | Linguagem principal |
| `pygame` | 2.x | Visualização interativa das rotas em tempo real |
| `matplotlib` | 3.7+ | Gráfico de evolução do fitness por geração |
| `numpy` | 1.24+ | Operações numéricas no algoritmo genético |
| `pytest` | 7.x | Suite de 62 testes automatizados |
| `openai` | *(opcional)* | Integração com API da OpenAI para geração de texto |
| `python-dotenv` | *(opcional)* | Carregamento de `.env` com `OPENAI_API_KEY` |

**Padrões de desenvolvimento:**
- `dataclasses` e `type hints` para modelos tipados
- Separação de responsabilidades em módulos independentes
- Injeção de dependência na camada LLM (testável sem API externa)
- Configurações dos experimentos em arquivos YAML separados

---

## 4. Metodologia

O projeto foi conduzido em **9 sprints incrementais**, cada uma adicionando uma funcionalidade verificável e testada:

| Sprint | Funcionalidade | Entregável Principal |
|:------:|---------------|---------------------|
| **S1** | Análise do código base e plano de extensão | Plano de 9 sprints documentado |
| **S2** | Migração do TSP para `src/` com dataclasses, type hints e testes | `src/routing/tsp.py` + testes iniciais |
| **S3** | Prioridades de entrega (HIGH/MEDIUM/LOW) e penalidade por atraso | `src/models/priority.py` + penalidades |
| **S4** | Peso das entregas e capacidade máxima dos veículos | `src/models/vehicle.py` + restrição de carga |
| **S5** | Autonomia máxima por veículo | Restrição de distância no fitness |
| **S6** | VRP com múltiplos veículos e cromossomo de frota | `src/routing/vrp.py` + operadores de frota |
| **S7** | Camada LLM para relatórios, instruções e Q&A | `src/llm/` completo + testes offline |
| **S8** | Experimentos comparativos em VRP com 5 configurações | `src/metrics/` + artefatos em `artifacts/` |
| **S9** | Consolidação — relatório, roteiro de vídeo e manifesto | `reports/`, `docs/`, `artifacts/final/` |

**Princípios seguidos:**
- Cada sprint mantém todos os testes anteriores passando (regressão zero)
- Funcionalidades são adicionadas de forma retrocompatível
- Cada entregável é demonstrável de forma independente

---

## 5. Implementação

### 5.1 Estrutura do Projeto

```
tech-challenge-fase2/
│
├── src/                                      # Implementação principal
│   ├── ga/
│   │   └── genetic_algorithm.py             # AG completo: população, operadores, fitness
│   ├── routing/
│   │   ├── tsp.py                           # Resolvedor TSP (Sprint 2)
│   │   └── vrp.py                           # Resolvedor VRP — cromossomo de frota (Sprint 6)
│   ├── models/
│   │   ├── delivery.py                      # Dataclass Delivery (id, location, priority, weight, due_time)
│   │   ├── vehicle.py                       # Dataclass Vehicle (id, max_capacity, max_distance)
│   │   └── priority.py                      # Enum Priority (HIGH, MEDIUM, LOW)
│   ├── visualization/
│   │   ├── pygame_viz.py                    # Renderização da rota com Pygame
│   │   └── matplotlib_viz.py               # Gráfico de fitness com Matplotlib
│   ├── llm/
│   │   ├── prompts.py                       # Contexto da solução e prompts reutilizáveis
│   │   ├── report_generator.py             # Relatório operacional e instruções por motorista
│   │   ├── route_explainer.py              # Respostas e Q&A sobre rotas
│   │   ├── openai_client.py                # Cliente OpenAI opcional
│   │   └── __main__.py                     # Ponto de entrada: python -m src.llm
│   ├── metrics/
│   │   ├── experiments.py                  # Execução das 5 configurações VRP
│   │   ├── experiment_logger.py            # Exportação: CSV, JSON, Markdown, PNG
│   │   ├── statistics.py                   # Métricas: convergência, melhoria relativa
│   │   └── __main__.py                     # Ponto de entrada: python -m src.metrics
│   ├── data_loader.py                      # Leitura e validação dos CSVs
│   └── main.py                             # CLI configurável + demo visual TSP/VRP
│
├── tests/                                   # 62 testes automatizados (pytest)
│
├── data/
│   ├── deliveries_sample.csv               # Entregas sintéticas
│   ├── brazil_capitals_sample.csv          # 27 capitais brasileiras em plano 2D
│   └── vehicles_sample.csv                 # Frota com capacidade e autonomia
│
├── config/
│   ├── pop50.yaml                          # Cenário: exploração rápida
│   ├── pop100.yaml                         # Cenário: equilibrado
│   ├── pop100_no_elitism.yaml              # Cenário: sem elitismo
│   ├── pop500.yaml                         # Cenário: alta convergência
│   └── pop500_no_elitism.yaml              # Cenário: alta convergência sem elitismo
│
├── docs/                                    # Documentação técnica por sprint
├── reports/
│   └── final_report.md                     # Este relatório
├── artifacts/
│   ├── experiments/                        # CSV, JSON, Markdown dos experimentos
│   ├── charts/                             # Gráficos PNG gerados automaticamente
│   └── final/manifest.md                  # Índice final de artefatos
├── references/                             # Código base original e referências
├── requirements.txt                        # Dependências principais
└── requirements-llm.txt                    # Dependências opcionais (OpenAI)
```

### 5.2 Fluxo de Dados

```
CSV de entregas + CSV de veículos
         │
         ▼
 src/data_loader.py          ← lê, valida e converte para dataclasses
         │
         ▼
 Delivery[] / Vehicle[]      ← modelos tipados com type hints
         │
         ▼
 TSPProblem / VRPProblem     ← encapsula o problema de otimização
         │
         ▼
 Algoritmo Genético          ← src/ga/genetic_algorithm.py
  ┌──────┴──────┐
  │             │
TSP            VRP
(1 veículo)   (frota completa)
  │             │
  └──────┬──────┘
         │
         ▼
 TSPSolution / VRPSolution   ← melhor rota(s) + histórico de fitness
         │
         ├── Pygame           ← animação 2D da rota por geração
         ├── Matplotlib       ← curva de convergência do fitness
         └── Camada LLM       ← relatório / instruções / Q&A
```

### 5.3 Algoritmo Genético — Detalhes de Implementação

**Inicialização da população (VRP):**
- 1 solução heurística: entregas ordenadas por prioridade → prazo → id, alocadas respeitando `max_capacity`
- `N-1` soluções aleatórias: distribuição e ordem aleatórias para garantir diversidade

**Parâmetros configuráveis via CLI:**

| Parâmetro | Flag | Padrão | Impacto |
|-----------|------|--------|---------|
| Tamanho da população | `--population-size` | `100` | Diversidade vs. custo computacional |
| Probabilidade de mutação | `--mutation-probability` | `0.5` | Exploração vs. exploitação |
| Elitismo | `--elite-size` | `1` | Preservação da melhor solução |
| FPS da animação | `--fps` | `30` | Velocidade da visualização |
| Modo | `--mode` | `tsp` | `tsp` (1 veículo) ou `vrp` (frota) |

### 5.4 VRP — Operadores de Frota

**Crossover de frota:**
```
Pai 1: sequência global [A, B, C, D, E, F, G]  +  divisão [2, 3, 2]
Pai 2: sequência global [D, A, G, B, C, F, E]

Filho: sequência do Pai 2  +  divisão do Pai 1:
  Veículo 1: D, A
  Veículo 2: G, B, C
  Veículo 3: F, E
```

**Mutação de frota (3 tipos, escolhidos aleatoriamente):**

| Tipo | O que faz |
|------|-----------|
| Mover entrega | Retira entrega do veículo A e insere no veículo B |
| Trocar entregas | Troca uma entrega do veículo A por uma do veículo B |
| Reordenar rota | Faz swap de duas entregas dentro do mesmo veículo |

### 5.5 Camada LLM — Arquitetura

```
TSPSolution / VRPSolution
       │
       ▼
prompts.py
  ├── build_tsp_context(solution) → str
  └── build_vrp_context(solution) → str
       │
       ▼
report_generator.py / route_explainer.py
  ├── Sem cliente → resposta determinística offline
  └── Com cliente → envia para OpenAI (gpt-4o-mini, etc.)
       │
       ▼
Texto formatado (relatório / instruções / resposta)
```

**Uso programático:**
```python
# Offline (sem API key)
from src.llm import generate_operational_report
report = generate_operational_report(solution)

# Com cliente injetado (ideal para testes com mock)
report = generate_operational_report(solution, client=my_client)
```

### 5.6 Cobertura de Testes

| Área | Testes | Exemplos |
|------|:------:|---------|
| Algoritmo Genético | ~15 | Crossover OX, mutação por swap, população inicial, histórico de fitness |
| Função de Fitness | ~10 | Distância euclidiana, penalidade HIGH/MEDIUM/LOW, capacidade, autonomia |
| Leitura de Dados | ~8 | CSV de entregas, CSV de veículos, campos opcionais |
| CLI | ~6 | Parsing de argumentos, modo TSP/VRP, seleção de veículos |
| VRP | ~12 | Distribuição de entregas, fitness agregado, mutação inter-rota, população de frota |
| LLM | ~11 | Prompts, respostas offline, fallback sem API key, TSP e VRP |
| **Total** | **62** | **100% passando** |

---

## 6. Experimentos VRP

A Sprint 8 implementou um runner reproduzível em `src/metrics/` para comparar 5 configurações do AG em modo VRP.

### 6.1 Pergunta de Pesquisa

> *Como o tamanho da população e a presença de elitismo afetam a qualidade da solução, a velocidade de convergência e o custo computacional do AG no problema VRP com restrições operacionais?*

### 6.2 Setup Experimental

- **Dataset:** `data/deliveries_sample.csv`
- **Modo:** VRP com todos os veículos do CSV
- **Gerações:** 500 por configuração
- **Semente:** fixa — resultados reproduzíveis
- **Métrica principal:** fitness final, geração de convergência, tempo de execução

### 6.3 Configurações Testadas

| Configuração | Pop. | Mutação | Crossover | Elitismo | Pool | Característica |
|:------------|:----:|:-------:|:---------:|:--------:|:----:|---------------|
| `pop50` | 50 | 0.14 | 0.68 | 1 | 6 | Menor população, maior mutação |
| `pop100` | 100 | 0.08 | 0.80 | 2 | 10 | Configuração intermediária e balanceada |
| `pop100_no_elitism` | 100 | 0.08 | 0.80 | **0** | 10 | `pop100` sem preservação de elite |
| `pop500` | 500 | 0.02 | 0.90 | 6 | 20 | Grande população, menor mutação |
| `pop500_no_elitism` | 500 | 0.02 | 0.90 | **0** | 20 | `pop500` sem preservação de elite |

### 6.4 Resultados

| Configuração | Fitness Final | Convergência | Tempo Total | Melhoria | Veredicto |
|:------------|:-------------:|:------------:|:-----------:|:--------:|:----------|
| ⭐ **pop50** | **0.16** | **Gen. 103** | **1.323s** | **0.40** | **Melhor custo-benefício** |
| pop100 | 0.16 | Gen. 187 | 2.588s | 0.40 | Equilibrado |
| pop100_no_elitism | 0.16 | Gen. 176 | 2.639s | 0.40 | Convergiu antes do pop100 |
| pop500 | 0.16 | Gen. 33 | 13.404s | 0.35 | Rápido em gerações, caro no total |
| pop500_no_elitism | 0.16 | Gen. 33 | 13.425s | 0.35 | Similar ao pop500 |

**Estatísticas gerais:**
- Fitness médio final: `0.16` — desvio padrão: `0.00`
- Tempo médio de execução: `6.676s`
- Speedup pop50 vs pop500: **≈ 10×**

### 6.5 Análise e Conclusões

#### ✅ Robustez do algoritmo

Todas as 5 configurações atingiram **fitness = 0.16** — demonstrando que o algoritmo é robusto e encontra soluções de qualidade equivalente independentemente do tamanho da população neste dataset.

#### ⚡ pop50: melhor custo-benefício

```
pop50:   1.323s → fitness 0.16 → convergência na geração 103
pop500: 13.404s → fitness 0.16 → convergência na geração 33

Economia de tempo: 13.404 - 1.323 = 12.081s (91% menos tempo)
Speedup:           13.404 / 1.323 ≈ 10.1×
```

A configuração `pop50` entrega a mesma qualidade que `pop500` em **10 vezes menos tempo** — recomendada para demonstrações ao vivo e execuções repetitivas.

#### 🔍 Impacto do elitismo

| Par | Elitismo | Convergência | Tempo | Fitness |
|-----|:--------:|:------------:|:-----:|:-------:|
| pop100 | Sim | Gen. 187 | 2.588s | 0.16 |
| pop100_no_elitism | Não | **Gen. 176** | 2.639s | 0.16 |
| pop500 | Sim | Gen. 33 | 13.404s | 0.16 |
| pop500_no_elitism | Não | Gen. 33 | **13.425s** | 0.16 |

> **Conclusão:** o elitismo não foi fator determinante neste dataset. A versão sem elitismo de `pop100` convergiu **11 gerações antes**, sugerindo que a maior exploração sem preservação de elite foi ligeiramente vantajosa neste caso.

#### 📈 Custo por geração vs. custo total

Populações maiores convergem em menos gerações, mas cada geração é significativamente mais cara:

```
Custo por geração (estimado):
  pop50:  1.323s / 500 gerações ≈  2.6 ms/geração
  pop100: 2.588s / 500 gerações ≈  5.2 ms/geração  (2×  pop50)
  pop500: 13.40s / 500 gerações ≈ 26.8 ms/geração  (10× pop50)
```

O custo por geração escala aproximadamente de forma **linear** com o tamanho da população — o que é esperado para AG com avaliação de fitness O(N).

### 6.6 Artefatos Gerados

| Artefato | Localização | Formato |
|----------|-------------|---------|
| Tabela comparativa | `artifacts/experiments/sprint8_summary.csv` | CSV |
| Dados estruturados | `artifacts/experiments/sprint8_summary.json` | JSON |
| Resumo legível | `artifacts/experiments/sprint8_summary.md` | Markdown |
| Curvas de convergência | `artifacts/charts/fitness_curves.png` | PNG |
| Comparativo de fitness | `artifacts/charts/final_fitness.png` | PNG |
| Comparativo de tempo | `artifacts/charts/execution_time.png` | PNG |

**Comando para reproduzir:**
```bash
.venv/bin/python -m src.metrics \
  --deliveries-file data/deliveries_sample.csv \
  --vehicles-file  data/vehicles_sample.csv \
  --output-dir     artifacts
```

---

## 7. Resultados Consolidados

### 7.1 Funcionalidades Entregues

| Funcionalidade | Sprint | Status |
|---------------|:------:|:------:|
| TSP com AG e visualização Pygame em tempo real | S2 | ✅ |
| Prioridades de entrega e penalidade por atraso | S3 | ✅ |
| Restrição de capacidade máxima por veículo | S4 | ✅ |
| Restrição de autonomia máxima por veículo | S5 | ✅ |
| VRP com múltiplos veículos e cromossomo de frota | S6 | ✅ |
| Mapa do Brasil na visualização (dataset de capitais) | S6 | ✅ |
| Camada LLM offline e com OpenAI | S7 | ✅ |
| 3 modos de saída LLM (report, instructions, question) | S7 | ✅ |
| Runner de experimentos com 5 configurações VRP | S8 | ✅ |
| Artefatos CSV, JSON, Markdown e PNG automáticos | S8 | ✅ |
| CLI configurável com todos os parâmetros do AG | S2+ | ✅ |
| 62 testes automatizados passando | S2+ | ✅ |
| Documentação técnica por sprint | S9 | ✅ |
| Relatório técnico consolidado | S9 | ✅ |

### 7.2 Métricas de Qualidade

| Métrica | Valor |
|---------|-------|
| Testes automatizados | **62 passed** |
| Fitness final VRP (todas as configs) | **0.16** |
| Melhor tempo de execução (pop50) | **1.323s** |
| Speedup pop50 vs pop500 | **≈ 10×** |
| Melhoria de fitness (pop50 e pop100) | **0.40 (40%)** |
| Sprints concluídas | **9 / 9** |
| Modos LLM implementados | **3** |

### 7.3 Validação Final

```
$ .venv/bin/python -m pytest
...............................................................

62 passed in X.XXs
```

---

## 8. Trabalhos Futuros

| Prioridade | Melhoria | Impacto Esperado |
|:----------:|---------|----------------|
| 🔴 Alta | **Operadores VRP especializados** — crossover cluster-first para preservar agrupamentos geográficos | Rotas mais coerentes geograficamente e menor fitness |
| 🔴 Alta | **Malha viária real** — substituir distâncias euclidianas por rotas via OSMnx ou Google Maps API | Distâncias e tempos mais realistas |
| 🟡 Média | **VRPTW** — Vehicle Routing Problem with Time Windows | Modelagem mais precisa de janelas de entrega hospitalares |
| 🟡 Média | **AG híbrido** — busca local 2-opt ou Or-opt para refinamento pós-genético | Melhoria da qualidade das soluções sem custo de diversidade |
| 🟢 Baixa | **Cliente OpenAI em produção** — demonstração com GPT-4o-mini e casos reais de uso | Relatórios LLM de alta qualidade para gestores |
| 🟢 Baixa | **Interface web** — substituir ou complementar o Pygame com visualização no navegador | Acessibilidade sem instalação de dependências |

---

## 9. Referências

- **Documento do Tech Challenge Fase 2** — FIAP, 2026. Especificação do Projeto 2.
- **Holland, J. H.** (1975). *Adaptation in Natural and Artificial Systems*. University of Michigan Press.
- **Toth, P.; Vigo, D.** (2002). *The Vehicle Routing Problem*. SIAM Monographs on Discrete Mathematics and Applications.
- **Código base em `references/`** — ponto de partida do projeto, fornecido pela instituição.
- **Documentação técnica em `docs/`** — uma por sprint, gerada ao longo do desenvolvimento.
- **Repositório GitHub:** [github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2](https://github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2)
- **Página de resultados:** [tech-challenge-fiap-grupo-2026.github.io/tech-challenge-fase2/index.html](https://tech-challenge-fiap-grupo-2026.github.io/tech-challenge-fase2/index.html)

---

<div align="center">

*Desenvolvido por Grupo FIAP 2026 — Tech Challenge Fase 2*

</div>
