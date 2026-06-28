# Prompts das Sprints

Este arquivo registra os prompts usados para evoluir o Projeto 2 do Tech Challenge Fase 2.

Legenda:

- `Concluida`: implementada e documentada no estado atual.
- `Pendente`: ainda precisa ser implementada.
- `Planejada`: prevista para fechamento do projeto.

# Sprint 1 - Analise do Baseline

Status: Concluida.

Compare a implementacao da pasta `references/` com os requisitos do Projeto 2.

Identifique:

- requisitos ja atendidos;
- requisitos ausentes;
- riscos tecnicos;
- possiveis refatoracoes.

Produza:

- `references/docs/extension_plan.md`

Nao implementar codigo.

# Sprint 2 - Migracao para src

Status: Concluida.

Utilizando o codigo da pasta `references/` como base, crie uma nova implementacao em `src/`.

Objetivos:

- adicionar type hints;
- adicionar dataclasses;
- melhorar legibilidade;
- preservar comportamento do TSP basico;
- separar o nucleo genetico da visualizacao.

Criar testes unitarios.

Nao adicionar novas funcionalidades nesta sprint.

# Sprint 3 - Prioridades

Status: Concluida.

Implementar prioridades:

- `HIGH`
- `MEDIUM`
- `LOW`

Atualizar fitness para considerar penalizacoes por atraso de entregas.

Criar testes.

Documentar alteracoes em:

- `docs/sprint3_priorities.md`

# Sprint 4 - Capacidade

Status: Concluida.

Adicionar:

- peso da entrega;
- capacidade maxima do veiculo.

Atualizar fitness para penalizar excesso de capacidade.

Criar testes.

Gerar exemplos em `data/`.

Documentar alteracoes em:

- `docs/sprint4_capacity.md`

# Sprint 5 - Autonomia

Status: Concluida.

Adicionar:

- distancia maxima por veiculo.

Aplicar penalidade quando a rota exceder a autonomia do veiculo.

Criar testes.

Documentar alteracoes em:

- `docs/sprint5_autonomy.md`

# Sprint 5.1 - CLI, Dados e Documentacao

Status: Concluida.

Atualizar o demo visual para aceitar parametros via CLI:

- `--vehicle-id`
- `--population-size`
- `--mutation-probability`
- `--elite-size`
- `--fps`
- `--deliveries-file`
- `--vehicles-file`

Adicionar dataset de capitais brasileiras em 2D:

- `data/brazil_capitals_sample.csv`

Atualizar documentacao:

- `README.md`
- `docs/architecture.md`
- `reports/final_report.md`
- `docs/report_outline.md`
- `docs/video_script.md`

# Sprint 6 - VRP com Multiplos Veiculos

Status: Concluida.

Expandir TSP para VRP.

Criar ou preencher:

- `src/routing/vrp.py`
- `tests/test_vrp.py`

Implementar:

- representacao de multiplas rotas;
- distribuicao de entregas entre veiculos;
- fitness agregado da frota;
- validacao de capacidade e autonomia por veiculo;
- testes de alocacao;
- modo visual `--mode vrp` animado com uma rota por veiculo;
- `--vehicle-ids` para selecionar a frota do modo VRP, mantendo todos os veiculos como padrao.

Documentar alteracoes em:

- `docs/sprint6_vrp.md`

# Sprint 7 - Camada LLM

Status: Concluida.

Referencia adicionada:

- `references/agent-llm.py`

Usar esse arquivo como referencia de arquitetura para:

- historico de mensagens;
- chamada da API da OpenAI;
- function calling;
- funcoes locais acionadas pela LLM;
- carregamento de variaveis com `dotenv`.

Nao reaproveitar o dominio financeiro do exemplo; adaptar o padrao para rotas medicas.

Implementado:

- `src/llm/report_generator.py`
- `src/llm/route_explainer.py`
- `src/llm/prompts.py`
- `src/llm/openai_client.py`
- `src/llm/__main__.py`

Funcoes esperadas:

- gerar relatorio operacional;
- gerar instrucoes para motoristas;
- responder perguntas sobre rotas;
- criar prompts reutilizaveis;
- executar a camada por CLI com `python -m src.llm`;
- permitir integracao externa via cliente injetado compatível com `complete(messages)`;
- manter a chamada real a OpenAI como opcional via `--provider openai`.

Criados testes sem depender de chamada externa obrigatoria a provedor LLM.

Documentar alteracoes em:

- `docs/sprint7_llm.md`

# Sprint 8 - Experimentos

Status: Concluida.

Executar configuracoes em modo VRP:

- `config/pop50.yaml`
- `config/pop100.yaml`
- `config/pop100_no_elitism.yaml`
- `config/pop500.yaml`
- `config/pop500_no_elitism.yaml`

Comparar:

- fitness final;
- convergencia;
- tempo de execucao.

Gerar:

- artefatos em `artifacts/charts/`;
- tabelas de resultados;
- atualizacao de `reports/final_report.md`.

Implementado:

- `src/metrics/experiments.py`
- `src/metrics/experiment_logger.py`
- `src/metrics/statistics.py`
- `src/metrics/__main__.py`
- saídas em `artifacts/experiments/` e `artifacts/charts/`
- comparacao de fitness final, convergencia e tempo de execucao

Resultado de referencia obtido no dataset de entregas sinteticas em VRP:

- `pop50`: melhor fitness `0.16`, convergencia na geracao `103`, tempo `1.323s`
- `pop100`: melhor fitness `0.16`, convergencia na geracao `187`, tempo `2.588s`
- `pop100_no_elitism`: melhor fitness `0.16`, convergencia na geracao `176`, tempo `2.639s`
- `pop500`: melhor fitness `0.16`, convergencia na geracao `33`, tempo `13.404s`
- `pop500_no_elitism`: melhor fitness `0.16`, convergencia na geracao `33`, tempo `13.425s`

Conclusoes iniciais:

- as cinco configuracoes chegaram ao mesmo fitness final no smoke test VRP;
- o experimento sem elitismo convergiu antes que o `pop100` com elitismo;
- `pop500` convergiu muito antes, mas com custo de execucao muito maior;
- `pop500_no_elitism` manteve a mesma convergencia do `pop500`, mas com tempo levemente maior;
- `pop50` teve o melhor equilibrio entre tempo e convergencia observada;
- `pop100` foi a configuracao intermediaria mais lenta para convergir.

# Sprint 9 - Consolidacao Final

Status: Concluida.

Gerar:

- graficos finais;
- mapas finais;
- relatorio consolidado;
- roteiro final de apresentacao.

Atualizar:

- `docs/video_script.md`
- `reports/final_report.md`

Implementado:

- `docs/sprint9_consolidation.md`
- `artifacts/final/manifest.md`
- roteiro de video atualizado com LLM e experimentos;
- relatorio final consolidado;
- indice de artefatos finais.
