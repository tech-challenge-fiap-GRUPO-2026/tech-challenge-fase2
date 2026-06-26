# Estrutura do Relatorio Tecnico

## 1. Introducao

- Contextualizar o Projeto 2.
- Explicar o problema logistico de distribuicao de medicamentos e insumos.
- Declarar o objetivo: otimizar rotas com Algoritmos Geneticos e preparar integracao com LLM.

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
- Comparar melhor fitness.
- Comparar convergencia.
- Comparar tempo de execucao.

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
- VRP ainda pendente no estado atual.
- LLM ainda pendente no estado atual.
- Dados de exemplo sinteticos.

## 10. Conclusao

- Resumir o que foi entregue.
- Indicar aderencia ao Projeto 2.
- Indicar proximos passos.
