<div align="center">

# 🚚 Otimização de Rotas Médicas — VRP com Algoritmos Genéticos

**Tech Challenge Fase 2 · Pós-Graduação IA Para Desenvolvedores · FIAP**

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green?logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557c?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-7.x-0A9EDC?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

</div>

---

## 👥 Equipe

| Nome | E-mail |
|------|--------|
| Jefferson Antônio Pantoja Silva | jeffkd35@gmail.com |
| Wilson Lima da Silva | wilson.slima@gmail.com |
| Gustavo Lopes da Silva | gustavo_lsilva@hotmail.com |
| Felipe Soeiro Lopes | felipesoeiro.contato@outlook.com.br |
| Vinicius Tavares Sousa da Silva | viniciustavares2014@gmail.com |

---

## 📋 Visão Geral

Projeto de otimização combinatória para **distribuição de medicamentos e insumos em rotas médicas**, utilizando **Algoritmos Genéticos** para resolver o Problema do Caixeiro Viajante (TSP) e o Problema de Roteamento de Veículos (VRP).

O sistema parte de um código base de TSP e evolui incrementalmente em **9 sprints** para um resolvedor completo com restrições operacionais, visualização interativa, integração com LLMs e suite de experimentos comparativos.

> Repositório: **[github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2](https://github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2)**

---

## 🧬 Algoritmo Genético

O núcleo da solução é um **Algoritmo Genético (AG)** capaz de operar em dois modos:

| Modo | Representação | Objetivo |
|------|:-------------:|---------|
| **TSP** | Permutação de entregas | Encontrar a rota mínima para um único veículo |
| **VRP** | Cromossomo de frota completa | Otimizar simultaneamente distribuição e ordem das entregas entre múltiplos veículos |

### Operadores Implementados

| Operador | Descrição |
|----------|-----------|
| **Seleção** | Pool dos `parent_pool_size` melhores — filhos gerados por amostragem aleatória do pool |
| **Crossover** | Order Crossover (OX) adaptado para frotas em modo VRP |
| **Mutação** | Swap, reorder e move de entregas dentro e entre rotas (VRP) |
| **Elitismo** | Preserva os `k` melhores indivíduos entre gerações |

### Crossover VRP — `fleet_crossover`

O crossover em modo VRP adapta o OX clássico ao cromossomo de frota completa em **três etapas**:

1. **Achatamento** — as rotas de cada pai são concatenadas em uma sequência plana de entregas
2. **OX sobre a sequência plana** — um segmento aleatório do pai 1 é copiado para o filho; as entregas ausentes são preenchidas na ordem em que aparecem no pai 2
3. **Repartição** — a sequência filho é redistribuída em rotas usando os tamanhos de rota herdados de um dos pais (sorteio 50/50)

Essa estratégia garante que **nenhuma entrega seja duplicada ou perdida** e que o filho herde a estrutura de distribuição de frota de um dos pais.

### Mutação VRP — `mutate_fleet`

Em modo VRP, a mutação sorteaia aleatoriamente um dos três operadores:

| Tipo | Ação | Escopo |
|------|------|--------|
| **`move`** | Remove uma entrega de uma rota e a insere em posição aleatória de qualquer outra rota | Inter-rota |
| **`swap`** | Troca uma entrega entre duas rotas distintas | Inter-rota |
| **`reorder`** | Troca dois elementos adjacentes dentro de uma mesma rota | Intra-rota |

Os operadores `move` e `swap` permitem que o algoritmo redistribua carga entre veículos, essencial para satisfazer restrições de capacidade e autonomia.

---

## 📐 Função de Fitness

O fitness de cada solução é calculado como:

```
fitness = distância_total
        + penalidade_de_atraso
        + penalidade_de_capacidade
        + penalidade_de_autonomia
```

| Componente | Penalidade |
|-----------|:-----------:|
| Atraso `HIGH` | `100.0` × unidades de atraso |
| Atraso `MEDIUM` | `30.0` × unidades de atraso |
| Atraso `LOW` | `10.0` × unidades de atraso |
| Excesso de capacidade | `25.0` × unidades acima do limite |
| Excesso de autonomia | `25.0` × unidades acima do limite |

> O algoritmo **minimiza** o fitness — soluções melhores têm valores menores.

### Fitness Agregado VRP

Em modo VRP, o fitness total é a **soma do fitness individual de cada rota**:

```
fitness_total = Σ fitness(rota_i, veículo_i)
             = Σ (distância_i + penalidade_atraso_i + penalidade_capacidade_i + penalidade_autonomia_i)
```

Cada veículo tem seu próprio `max_capacity` e `max_distance`, e as penalidades são calculadas individualmente por rota. Isso incentiva o AG a equilibrar a carga entre veículos e respeitar as restrições de cada um.

---

## 📊 Experimentos VRP

> *Como o tamanho da população e o elitismo afetam a qualidade da solução, a convergência e o custo computacional?*

Cinco configurações foram comparadas em modo VRP com `data/deliveries_sample.csv` — 500 gerações cada, semente fixa para reprodutibilidade:

| Configuração | Pop. | Elitismo | Fitness Final | Convergência | Tempo | Melhoria |
|:------------|:----:|:--------:|:-------------:|:------------:|:-----:|:--------:|
| ⭐ **pop50** | 50 | 1 | **0.16** | Gen. 103 | **1.323s** | 0.40 |
| pop100 | 100 | 2 | 0.16 | Gen. 187 | 2.588s | 0.40 |
| pop100_no_elitism | 100 | 0 | 0.16 | Gen. 176 | 2.639s | 0.40 |
| pop500 | 500 | 6 | 0.16 | Gen. 33 | 13.404s | 0.35 |
| pop500_no_elitism | 500 | 0 | 0.16 | Gen. 33 | 13.425s | 0.35 |

**Conclusões:**
- Todas as 5 configurações atingiram o **mesmo fitness final (0.16)** — o algoritmo é robusto
- **`pop50` é 10× mais rápido** que `pop500` com qualidade idêntica (1.3s vs 13.4s)
- Elitismo não foi determinante neste dataset — `pop100_no_elitism` convergiu 11 gerações antes
- O custo por geração escala linearmente com o tamanho da população (~2.6 ms vs ~26.8 ms)

Artefatos gerados em `artifacts/` ao executar `python -m src.metrics`:
- `experiments/sprint8_summary.csv` — tabela comparativa
- `experiments/sprint8_summary.json` — dados estruturados
- `charts/fitness_curves.png` — curvas de convergência por geração
- `charts/final_fitness.png` — comparativo de fitness final
- `charts/execution_time.png` — comparativo de tempo de execução

---

## 📁 Estrutura do Projeto

```
tech-challenge-fase2/
│
├── src/                                      # Implementação principal
│   ├── ga/
│   │   └── genetic_algorithm.py             # Algoritmo genético e operadores
│   ├── routing/
│   │   ├── tsp.py                           # Resolvedor TSP
│   │   └── vrp.py                           # Resolvedor VRP (cromossomo de frota)
│   ├── models/                              # Dataclasses: Entrega, Veículo, Cidade
│   ├── visualization/                       # Pygame (rota) + Matplotlib (fitness)
│   ├── llm/                                 # Camada LLM — relatórios e instruções
│   ├── metrics/                             # Runner de experimentos comparativos
│   ├── data_loader.py                       # Leitura de CSV
│   └── main.py                              # CLI e demo visual
│
├── tests/                                   # Testes automatizados (62 passing)
│
├── data/
│   ├── deliveries_sample.csv               # Entregas sintéticas
│   ├── brazil_capitals_sample.csv          # Capitais brasileiras em plano 2D
│   └── vehicles_sample.csv                 # Veículos com capacidade e autonomia
│
├── config/                                  # Configurações dos experimentos
├── docs/                                    # Documentação técnica por sprint
├── reports/
│   └── final_report.md                     # Relatório técnico consolidado
├── artifacts/
│   ├── experiments/                        # Resultados dos experimentos VRP
│   └── final/                              # Manifesto final de artefatos
├── references/                             # Baseline TSP e referências técnicas
├── requirements.txt                        # Dependências principais
└── requirements-llm.txt                    # Dependências opcionais (OpenAI)
```

---

## 🚀 Instruções de Execução

### ✅ Pré-requisitos

- Python 3.12 ou superior
- pip

---

### 1. 📥 Clonar o repositório

```bash
git clone https://github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2
cd tech-challenge-fase2
```

### 2. 🐍 Criar ambiente virtual

```bash
python -m venv .venv

# Linux / Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. 📦 Instalar as dependências

```bash
pip install -r requirements.txt
```

Dependências opcionais para integração real com OpenAI:

```bash
pip install -r requirements-llm.txt
```

---

### 4. 🖥️ Executar a visualização (modo TSP)

```bash
.venv/bin/python -m src.main
```

Exemplo com capitais brasileiras e parâmetros customizados:

```bash
.venv/bin/python -m src.main \
  --deliveries-file data/brazil_capitals_sample.csv \
  --vehicle-id 3 \
  --population-size 200 \
  --mutation-probability 0.3 \
  --elite-size 2 \
  --fps 15
```

### 5. 🚛 Executar a visualização (modo VRP)

```bash
.venv/bin/python -m src.main \
  --mode vrp \
  --deliveries-file data/brazil_capitals_sample.csv \
  --population-size 100 \
  --mutation-probability 0.3 \
  --elite-size 2 \
  --fps 15
```

Com veículos específicos:

```bash
.venv/bin/python -m src.main \
  --mode vrp \
  --vehicle-ids 1 3 5 \
  --deliveries-file data/brazil_capitals_sample.csv \
  --population-size 100
```

---

### 6. 🤖 Executar a camada LLM

A camada LLM funciona **sem chave de API** — retorna respostas determinísticas por padrão.

**Gerar relatório operacional:**

```bash
.venv/bin/python -m src.llm \
  --mode vrp \
  --output report \
  --deliveries-file data/brazil_capitals_sample.csv \
  --generations 80 \
  --population-size 80
```

**Gerar instruções para motoristas:**

```bash
.venv/bin/python -m src.llm \
  --mode vrp \
  --output instructions \
  --vehicle-ids 1 3 5 \
  --deliveries-file data/brazil_capitals_sample.csv
```

**Responder pergunta sobre a rota:**

```bash
.venv/bin/python -m src.llm \
  --mode tsp \
  --output question \
  --question "Qual é o fitness da rota?" \
  --deliveries-file data/brazil_capitals_sample.csv \
  --vehicle-id 3
```

**Com OpenAI (opcional):**

```bash
export OPENAI_API_KEY="sua-chave"
.venv/bin/python -m src.llm \
  --provider openai \
  --model gpt-4o-mini \
  --mode vrp \
  --output report \
  --deliveries-file data/brazil_capitals_sample.csv
```

---

### 7. 🔬 Executar experimentos VRP

```bash
.venv/bin/python -m src.metrics \
  --deliveries-file data/deliveries_sample.csv \
  --vehicles-file data/vehicles_sample.csv \
  --output-dir artifacts
```

Executa os cenários `pop50`, `pop100`, `pop100_no_elitism`, `pop500` e `pop500_no_elitism` e salva artefatos em `artifacts/`.

### 8. ✅ Executar os testes

```bash
.venv/bin/python -m pytest
```

Resultado esperado: **62 passed**.

---

## ⚙️ Opções da CLI

| Opção | Padrão | Descrição |
|-------|:------:|-----------|
| `--mode <tsp\|vrp>` | `tsp` | Modo de execução |
| `--vehicle-id <id>` | 1º do CSV | Veículo usado no modo TSP |
| `--vehicle-ids <ids>` | todos | Veículos usados no modo VRP |
| `--population-size <n>` | `100` | Tamanho da população |
| `--mutation-probability <p>` | `0.5` | Probabilidade de mutação |
| `--elite-size <n>` | `1` | Indivíduos preservados por elitismo |
| `--fps <n>` | `30` | Taxa de quadros da animação |
| `--deliveries-file <path>` | `data/deliveries_sample.csv` | CSV de entregas |
| `--vehicles-file <path>` | `data/vehicles_sample.csv` | CSV de veículos |

> Para fechar a janela: pressione `q` ou feche a janela do Pygame.

---

## 📈 Métricas da Entrega Final

| Métrica | Resultado |
|---------|-----------|
| Testes automatizados | **62 passed** |
| Fitness final VRP (todas as configs) | **0.16** |
| Melhor tempo de execução | **1.323s** (pop50) |
| Speedup pop50 vs pop500 | **≈ 10×** |
| Melhoria de fitness | **40%** (pop50 e pop100) |
| Sprints concluídas | **9 / 9** |
| Modos de saída LLM | **3** (report, instructions, question) |

---

## 🧩 Dependências

| Biblioteca | Uso |
|------------|-----|
| `pygame` | Visualização interativa das rotas em tempo real |
| `matplotlib` | Gráfico de evolução do fitness por geração |
| `numpy` | Operações numéricas no algoritmo genético |
| `pytest` | Suite de testes automatizados |
| `openai` *(opcional)* | Integração real com LLM OpenAI |
| `python-dotenv` *(opcional)* | Carregamento de `.env` com `OPENAI_API_KEY` |

---

## 📚 Documentação

| Arquivo | Conteúdo |
|---------|----------|
| `reports/final_report.md` | Relatório técnico consolidado |
| `docs/video_script.md` | Roteiro do vídeo de demonstração |
| `docs/architecture.md` | Arquitetura do sistema |
| `docs/sprint8_experiments.md` | Detalhamento dos experimentos VRP |
| `docs/sprint9_consolidation.md` | Fechamento e evidências da entrega final |
| `artifacts/final/manifest.md` | Manifesto de artefatos com comandos reproduzíveis |

---

## 🎬 Vídeo Demonstração

[![Assistir no YouTube](https://img.shields.io/badge/YouTube-Assistir%20Demo-FF0000?logo=youtube&logoColor=white)](https://youtu.be/tCo0JeZm52g)

---

## 🌐 Relatório de Resultados

O relatório visual completo com os resultados dos experimentos está disponível em:

> 🔗 **[tech-challenge-fiap-grupo-2026.github.io/tech-challenge-fase2/index.html](https://tech-challenge-fiap-grupo-2026.github.io/tech-challenge-fase2/index.html)**

Ou abra localmente: [`index.html`](index.html)

---

## 🐙 Repositório GitHub

[https://github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2](https://github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2)
