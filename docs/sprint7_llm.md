# Sprint 7 - Camada LLM

## Objetivo

Iniciar a camada LLM do Projeto 2 para gerar textos operacionais a partir das rotas otimizadas.

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

Entregaveis esperados:

- `src/llm/prompts.py`: prompts reutilizaveis;
- `src/llm/report_generator.py`: geracao de relatorio operacional;
- `src/llm/route_explainer.py`: explicacao de rotas e respostas simples;
- testes sem chamada obrigatoria a provedor externo;
- documentacao de uso.

## Funcoes Esperadas

A Sprint 7 deve permitir:

- gerar instrucoes para motoristas;
- gerar relatorio operacional da rota ou frota;
- responder perguntas sobre entregas, atrasos, capacidade e autonomia;
- montar prompts a partir de `TSPSolution` ou `VRPSolution`.

## Estrategia Tecnica

O codigo de producao deve separar:

- montagem de contexto da rota;
- montagem do prompt;
- chamada opcional ao provedor LLM;
- formatacao da resposta.

Os testes devem validar principalmente:

- conteudo dos prompts;
- presenca de entregas, veiculos e metricas importantes;
- comportamento com TSP e VRP;
- fallback sem `OPENAI_API_KEY`.

## Fora do Escopo Inicial

- depender obrigatoriamente de internet nos testes;
- usar dados financeiros do exemplo;
- acoplar Streamlit ao nucleo de roteamento;
- substituir a visualizacao Pygame.

## Criterios de Aceite

- O projeto gera instrucoes legiveis para motoristas.
- O projeto gera um relatorio operacional textual.
- O projeto monta prompts reutilizaveis e testaveis.
- A camada LLM funciona com mock/fake client nos testes.
- A documentacao explica como configurar `OPENAI_API_KEY` para uso real.
