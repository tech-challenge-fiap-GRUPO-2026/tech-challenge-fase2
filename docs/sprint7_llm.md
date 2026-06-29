# 🏃 Sprint 7 — Camada LLM

**Status:** ✅ Concluída

---

## 🎯 Objetivo

Implementar uma **camada LLM testável e desacoplada** que transforma dados operacionais das rotas otimizadas em texto legível para humanos — relatórios, instruções para motoristas e respostas sobre as rotas.

---

## 🤖 O que a Camada LLM Faz?

Ao final da otimização (TSP ou VRP), a camada LLM recebe o objeto de solução e gera saídas em três modos:

| Modo | Flag | Saída |
|------|------|-------|
| **Relatório operacional** | `--output report` | Resumo da frota: fitness, distâncias, tempo estimado por veículo |
| **Instruções por motorista** | `--output instructions` | Lista ordenada de entregas para cada veículo, com observações |
| **Q&A sobre rotas** | `--output question` | Resposta em linguagem natural para uma pergunta sobre a rota |

---

## 📁 Arquivos Implementados

| Arquivo | Responsabilidade |
|---------|-----------------|
| `src/llm/prompts.py` | Monta o contexto da solução (entregas, fitness, rotas) e os prompts reutilizáveis |
| `src/llm/report_generator.py` | Gera o relatório operacional e as instruções por motorista |
| `src/llm/route_explainer.py` | Responde perguntas e explica rotas em linguagem natural |
| `src/llm/openai_client.py` | Cliente OpenAI opcional — injetável nos geradores |
| `src/llm/__main__.py` | Ponto de entrada via `python -m src.llm` |
| `tests/test_llm.py` | Testes sem chamada obrigatória a provedor externo |

---

## 🏗️ Estratégia de Design

O código separa claramente as responsabilidades:

```
1. Montagem de contexto     ← extrai dados da TSPSolution ou VRPSolution
         │
         ▼
2. Montagem do prompt       ← formata o contexto em texto para a LLM
         │
         ▼
3. Chamada ao provedor LLM  ← opcional: offline (determinístico) ou OpenAI
         │
         ▼
4. Formatação da resposta   ← limpa e estrutura o texto final
```

Essa separação permite **testar cada etapa isoladamente** sem depender de internet ou chave de API.

---

## ⌨️ Uso pela Linha de Comando

### Modo offline (padrão — sem chave de API)

```bash
# Relatório operacional VRP
.venv/bin/python -m src.llm \
  --mode vrp \
  --output report \
  --deliveries-file data/brazil_capitals_sample.csv \
  --generations 80 \
  --population-size 80

# Instruções para motoristas (veículos específicos)
.venv/bin/python -m src.llm \
  --mode vrp \
  --output instructions \
  --vehicle-ids 1 3 5 \
  --deliveries-file data/brazil_capitals_sample.csv

# Pergunta sobre rota TSP
.venv/bin/python -m src.llm \
  --mode tsp \
  --output question \
  --question "Qual é o fitness da rota?" \
  --deliveries-file data/brazil_capitals_sample.csv \
  --vehicle-id 3
```

### Modo com OpenAI (opcional)

```bash
# Instalar dependências extras
pip install openai python-dotenv

# Configurar chave (ou criar arquivo .env)
export OPENAI_API_KEY="sua-chave"

# Executar com GPT-4o-mini
.venv/bin/python -m src.llm \
  --provider openai \
  --model gpt-4o-mini \
  --mode vrp \
  --output report \
  --deliveries-file data/brazil_capitals_sample.csv
```

---

## 🐍 Uso Programático

### Sem cliente externo (respostas determinísticas)

```python
from src.llm import generate_operational_report

report = generate_operational_report(solution)
print(report)
```

### Com cliente externo injetado

```python
from src.llm import generate_operational_report

report = generate_operational_report(solution, client=my_llm_client)
```

O `client` pode ser qualquer objeto com o método `complete(messages: list) -> str` — ideal para mocks em testes.

---

## 🔌 Referência Técnica

A implementação usou `references/agent-llm.py` como referência de padrões de integração:

| Padrão | Uso na Sprint 7 |
|--------|----------------|
| Uso da API OpenAI com `dotenv` | Cliente em `src/llm/openai_client.py` |
| Histórico de mensagens | Estrutura de prompts em `src/llm/prompts.py` |
| Function calling | Referência de padrão (não usado diretamente) |
| Separação interface/lógica | Desacoplamento da visualização Pygame |

> O domínio financeiro do exemplo não foi reaproveitado — apenas os padrões de integração.

---

## 🚫 Fora do Escopo desta Sprint

- Dependência obrigatória de internet nos testes
- Interface Streamlit (visualização via Pygame é mantida)
- Cliente OpenAI obrigatório em produção
- Uso de dados financeiros do arquivo de referência

---

## ✅ Critérios de Aceite

| Critério | Status |
|----------|--------|
| Gera instruções legíveis para motoristas | ✅ |
| Gera relatório operacional textual da frota | ✅ |
| Monta prompts reutilizáveis e testáveis | ✅ |
| Funciona com mock/fake client nos testes | ✅ |
| Funciona sem OPENAI_API_KEY (modo offline) | ✅ |
| Integração real com OpenAI via `--provider openai` | ✅ |
| Suporta TSPSolution e VRPSolution | ✅ |
