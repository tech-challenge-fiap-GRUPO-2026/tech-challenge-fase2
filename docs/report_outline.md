# Estrutura do Relatorio Tecnico

## 1. Introducao

- Contextualizar o Projeto 2.
- Explicar o problema logistico de distribuicao de medicamentos e insumos.
- Declarar o objetivo: otimizar rotas com Algoritmos Geneticos e integrar uma camada LLM.

## 2. Fundamentacao Teorica

- Algoritmos Geneticos.
- TSP.
- VRP.
- Restricoes logisticas.
- LLMs para relatorios e instrucoes.

## 3. Metodologia

- Descrever as sprints.
- Explicar a evolucao do codigo base para `src/`.
- Explicar estrategia de testes.

## 4. Implementacao

- Estrutura do projeto.
- Modelos `Delivery`, `Vehicle`, `Priority` e `City`.
- Algoritmo genetico.
- Operadores geneticos.
- Fitness com penalidades.
- Entrada de dados CSV.
- Visualizacao.
- CLI.

## 5. Restricoes Implementadas

- Prioridades de entrega.
- Penalizacao por atraso.
- Peso da entrega.
- Capacidade maxima do veiculo.
- Autonomia maxima do veiculo.

## 6. Experimentos

- Configuracoes `pop50`, `pop100`, `pop500`.
- Configuracao adicional `pop100_no_elitism` para comparar elitismo ligado e desligado.
- Configuracao adicional `pop500_no_elitism` para comparar elitismo ligado e desligado em populacao grande.
- Comparar melhor fitness.
- Comparar convergencia.
- Comparar tempo de execucao.
- Reportar artefatos gerados em `artifacts/experiments/` e `artifacts/charts/`.

## 7. Resultados

- Apresentar rotas visualizadas.
- Apresentar curva de fitness.
- Apresentar tabela comparativa.
- Discutir impacto das restricoes.

## 8. LLM

- Explicar proposta de prompts.
- Mostrar instrucoes para motoristas.
- Mostrar relatorio operacional.
- Mostrar resposta a pergunta sobre rota.

## 9. Limitacoes

- Distancia euclidiana, nao malha viaria.
- VRP implementado com frota completa, ainda com operadores geneticos simples.
- LLM implementada de forma testavel e opcionalmente integrada com OpenAI.
- Experimentos comparativos executados com `pop50`, `pop100` e `pop500`.
- Consolidacao final registrada em `docs/sprint9_consolidation.md` e `artifacts/final/manifest.md`.
- Dados de exemplo sinteticos.

## 10. Conclusao

- Resumir o que foi entregue.
- Indicar aderencia ao Projeto 2.
- Indicar proximos passos.
