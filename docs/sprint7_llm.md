# Sprint 7 - Camada LLM

## Objetivo

Iniciar a camada LLM do Projeto 2 para gerar textos operacionais a partir das rotas otimizadas.

Status: concluida.

## Referencia Adicionada

Foi adicionado o arquivo:

- `references/agent-llm.py`

Esse arquivo e uma referencia de agente com:

- interface Streamlit;
- uso da API da OpenAI;
- carregamento de variaveis com `dotenv`;
- historico de mensagens em `session_state`;
- chamada de ferramentas via function calling;
- execucao de funcoes locais a partir de chamadas da LLM.

O exemplo esta no dominio financeiro, entao nao deve ser copiado diretamente para producao do projeto de rotas. A referencia util para a Sprint 7 e o padrao de integracao entre interface, LLM, mensagens e ferramentas.

## Escopo da Sprint

Implementar uma camada LLM testavel e desacoplada da visualizacao.

Entregaveis implementados:

- `src/llm/prompts.py`: prompts reutilizaveis;
- `src/llm/report_generator.py`: geracao de relatorio operacional;
- `src/llm/route_explainer.py`: explicacao de rotas e respostas simples;
- `src/llm/openai_client.py`: cliente OpenAI opcional;
- `src/llm/__main__.py`: execucao demonstravel por CLI;
- `tests/test_llm.py`: testes sem chamada obrigatoria a provedor externo;
- documentacao de uso.

## Funcoes Esperadas

A Sprint 7 permite:

- gerar instrucoes para motoristas;
- gerar relatorio operacional da rota ou frota;
- responder perguntas sobre entregas, atrasos, capacidade e autonomia;
- montar prompts a partir de `TSPSolution` ou `VRPSolution`;
- executar por `python -m src.llm`;
- permitir integracao externa por cliente injetado;
- usar OpenAI de forma opcional com `--provider openai`.

## Estrategia Tecnica

O codigo de producao separa:

- montagem de contexto da rota;
- montagem do prompt;
- chamada opcional ao provedor LLM;
- formatacao da resposta.

Os testes validam principalmente:

- conteudo dos prompts;
- presenca de entregas, veiculos e metricas importantes;
- comportamento com TSP e VRP;
- fallback sem `OPENAI_API_KEY`.

## Uso Basico

Pela linha de comando:

```bash
.venv/bin/python -m src.llm --mode vrp --output report --deliveries-file data/brazil_capitals_sample.csv
```

Outros tipos de saida:

```bash
.venv/bin/python -m src.llm --mode vrp --output instructions --vehicle-ids 1 3 5
.venv/bin/python -m src.llm --mode tsp --output question --question "Qual e o fitness da rota?"
```

Sem cliente externo, o sistema gera uma resposta textual deterministica:

```python
from src.llm import generate_operational_report

report = generate_operational_report(solution)
```

Com cliente externo, injete um objeto com metodo `complete(messages)`:

```python
from src.llm import generate_operational_report

report = generate_operational_report(solution, client=my_llm_client)
```

Essa abordagem permite testar a camada LLM sem depender de internet ou chave de API.

## Uso com OpenAI

A chamada real ao provedor e opcional.

Instalacao opcional:

```bash
.venv/bin/pip install openai python-dotenv
```

Configure a chave:

```bash
export OPENAI_API_KEY="sua-chave"
```

Ou crie um arquivo `.env` com:

```text
OPENAI_API_KEY=sua-chave
```

Execucao:

```bash
.venv/bin/python -m src.llm --provider openai --model gpt-4o-mini --mode vrp --output report --deliveries-file data/brazil_capitals_sample.csv
```

## Fora do Escopo Inicial

- depender obrigatoriamente de internet nos testes;
- usar dados financeiros do exemplo;
- acoplar Streamlit ao nucleo de roteamento;
- substituir a visualizacao Pygame.
- tornar o cliente OpenAI obrigatorio.

## Criterios de Aceite

- O projeto gera instrucoes legiveis para motoristas.
- O projeto gera um relatorio operacional textual.
- O projeto monta prompts reutilizaveis e testaveis.
- A camada LLM funciona com mock/fake client nos testes.
- O uso real com provedor externo pode ser feito por cliente injetado ou `--provider openai`.
