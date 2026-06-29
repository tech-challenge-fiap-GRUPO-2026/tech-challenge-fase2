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
| **Seleção** | Torneio por fitness — favorece os melhores indivíduos |
| **Crossover** | Combinação de sub-rotas entre pais (OX-style) |
| **Mutação** | Swap, inversão e relocação de entregas dentro e entre rotas |
| **Elitismo** | Preserva os `k` melhores indivíduos entre gerações |

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

---

## 📊 Experimentos VRP

Cinco configurações foram comparadas em modo VRP, executadas com o dataset de entregas sintéticas:

| Configuração | Fitness Final | Convergência | Tempo | Melhoria |
|:------------|:-------------:|:------------:|:-----:|:--------:|
| pop50 | 0.16 | 103 | 1.323s | 0.40 |
| pop100 | 0.16 | 187 | 2.588s | 0.40 |
| pop100_no_elitism | 0.16 | 176 | 2.639s | 0.40 |
| pop500 | 0.16 | 33 | 13.404s | 0.35 |
| pop500_no_elitism | 0.16 | 33 | 13.425s | 0.35 |

> **`pop50` apresentou o melhor equilíbrio** entre tempo de execução e convergência — atingindo o mesmo fitness final que populações 10× maiores.

Artefatos gerados em `artifacts/`:
- `experiments/sprint8_summary.csv` — tabela comparativa
- `experiments/sprint8_summary.json` — dados estruturados
- `charts/fitness_curves.png` — curvas de convergência
- `charts/final_fitness.png` — comparativo de fitness final
- `charts/execution_time.png` — comparativo de tempo

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

[![Assistir no YouTube](https://img.shields.io/badge/YouTube-Assistir%20Demo-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=DEMO_LINK)

---

## 🌐 Relatório de Resultados

O relatório visual completo com os resultados dos experimentos está disponível em:

> [`docs/index.html`](docs/index.html) — abra diretamente no navegador

---

## 🐙 Repositório GitHub

[https://github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2](https://github.com/tech-challenge-fiap-GRUPO-2026/tech-challenge-fase2)
