PROJECT_CONTEXT — TAMBURETEI UnB
================================

1. VISÃO GERAL E PROPÓSITO
--------------------------

O Tamburetei UnB é uma plataforma aberta, colaborativa e analítica voltada à
comunidade acadêmica da Universidade de Brasília (UnB), hospedada sob a
organização OpenDevUnB.

O projeto faz parte do escopo da disciplina Métodos de Desenvolvimento de
Software (MDS 2026/2 — FCTE/UnB) e é inspirado no ecossistema do OpenDevUFCG.

O sistema atende a duas necessidades centrais dos estudantes:

1.1. Transparência e métricas acadêmicas

Ingestão, anonimização e disponibilização de dados analíticos sobre:

- taxas de aprovação;
- reprovação por nota;
- reprovação por falta;
- trancamentos;
- evasão;
- tempo médio de formação.

Os dados serão obtidos por meio do DPO, do INEP e da Lei de Acesso à
Informação (LAI).

1.2. Hub colaborativo de disciplinas (/cadeiras)

Centralização de recursos de apoio aos estudantes, incluindo:

- ementas;
- dificuldades comuns;
- dicas de estudo;
- resumos de conteúdos ("leites");
- links úteis;
- enunciados de avaliações públicas anteriores.


2. ESCOPO DAS ENTREGAS — RELEASES MDS 2026/2
---------------------------------------------

2.1. Release 1 (R1)

Prazo: Semana 7 — 28/09/2026
Foco: Engenharia de Dados e Infraestrutura

Entregáveis técnicos:

- Pipeline de ingestão e normalização de dados do DPO, INEP e Dados Abertos,
  executado em containers Docker.
- Algoritmo de mascaramento em conformidade com a LGPD, utilizando
  k-anonimato.
- Dataset limpo e documentado, com metadados e especificação OpenAPI.
- Modelos relacionais no PostgreSQL, versionados por meio de migrações
  Alembic.

2.2. Release 2 (R2)

Prazo: Semana 15 — 25/11/2026
Foco: Portal Web e Hub Comunitário

Entregáveis técnicos:

- Frontend em Next.js/React integrado à API pública.
- Dashboards interativos com taxas de aprovação e evasão.
- Hub modular por disciplina, acessível em /cadeiras/:slug.
- Sistema colaborativo para envio de links e resumos, com moderação de
  relatos.
- Deploy em nuvem com pipeline de CI/CD aprovado e SAST sem falhas.


3. STACK TECNOLÓGICA E DECISÕES DE ARQUITETURA (ADR)
----------------------------------------------------

3.1. Frontend

- Next.js com App Router;
- React;
- TypeScript;
- Tailwind CSS.

3.2. Backend

- Python 3.12 ou superior;
- FastAPI;
- arquitetura assíncrona;
- validação com Pydantic v2;
- documentação com OpenAPI/Swagger.

3.3. Banco de dados

- PostgreSQL 17, executado via Docker;
- SQLAlchemy como ORM;
- Alembic para controle de migrações no modelo Database-as-Code.

Decisão arquitetural (ADR): Redis e MongoDB foram explicitamente descartados
para evitar sobre-engenharia e complexidade desnecessária no CI/CD. O
PostgreSQL, com índices adequados, deve atender às leituras analíticas em menos
de 300 ms.

3.4. Infraestrutura

- Docker;
- Docker Compose;
- isolamento completo dos serviços db, backend e frontend.

3.5. Qualidade e testes

- Pytest;
- Mutmut para testes de mutação;
- Bandit e SonarQube para análise estática de segurança (SAST).


4. ARQUITETURA DE SOFTWARE
--------------------------

4.1. Backend — FastAPI em camadas

O backend será estruturado para garantir testabilidade unitária sem depender
de um banco de dados ativo.

backend/app/
|-- api/             Routers HTTP do FastAPI e schemas Pydantic para validação
|                    de entrada e saída.
|-- core/            Configurações de ambiente (.env) e segurança.
|-- domain/          Lógica de negócio pura: cálculo de evasão e aprovação,
|                    k-anonimato e moderação.
|-- services/        Casos de uso e orquestração entre API e repositórios.
|-- repositories/    Consultas SQL e persistência via SQLAlchemy ORM.
|-- models/          Entidades relacionais do banco de dados em SQLAlchemy.
`-- pipeline/        ETL: extração de DPO, INEP e Dados Abertos, limpeza e
                     anonimização.

4.2. Frontend — Next.js

frontend/src/
|-- app/             Rotas do Next.js: /, /cadeiras e /cadeiras/[slug].
|-- features/        Componentes agrupados por domínio: analytics, cadeiras e
|                    comentários.
|-- components/ui/   Design system atômico: botões, modais e cards.
`-- services/        Clientes HTTP para chamadas à API FastAPI.

4.3. Estrutura do banco de dados — PostgreSQL

cursos
  Metadados dos cursos: codigo_mec, nome, campus, grau e turno.

disciplinas
  Cadastro canônico: codigo, slug, nome, departamento, creditos e ementa.

cursos_disciplinas
  Matriz curricular e semestres sugeridos.

metricas_academicas
  Fato analítico agregado: ano, semestre, matriculados, aprovados,
  reprovados_nota, reprovados_falta, trancamentos, taxa_aprovacao e
  is_k_anonimizado.

conteudos
  Materiais colaborativos: tipo (LINK_UTIL, RESUMO, PROVA_ANTIGA ou DICA),
  status_curadoria e url_origem.

comentarios
  Relatos sobre dificuldades nas disciplinas: autor_alias,
  topico_dificuldade, conteudo e status_moderacao.


5. REGRAS DE NEGÓCIO E GOVERNANÇA
---------------------------------

Qualquer agente que gerar código deve obedecer obrigatoriamente às regras a
seguir.

[RN01] K-anonimato e LGPD

Agregações de turmas ou cursos com menos de cinco alunos devem ser suprimidas
ou agrupadas sob a indicação "< 5". Nunca devem ser expostos ou armazenados
identificadores diretos, como matrícula, CPF ou nome de aluno.

[RN02] Proteção a docentes

É proibida a inclusão ou publicação de juízos de valor depreciativos ou de
conteúdo difamatório contra professores. Os relatos devem se concentrar no
conteúdo e na metodologia da disciplina.

[RN03] Vedação de resoluções ativas

Não é permitido publicar respostas ou gabaritos de atividades aplicadas
repetidamente, como listas semanais e laboratórios avaliativos. São aceitos
somente provas antigas públicas e materiais conceituais.

[RN04] Cálculo de evasão

A taxa de evasão deve seguir a fórmula:

Taxa de evasão = (total de desligamentos / total de matriculados ativos) x 100


6. PORTAS DE QUALIDADE E CRITÉRIOS DA DISCIPLINA (MDS 2026/2)
----------------------------------------------------------------

6.1. Cobertura de código

Mínimo de 70% de cobertura de linhas no módulo de domínio.

6.2. Escore de mutação

Mínimo de 50% nas regras de negócio e no cálculo de métricas.

6.3. Testes de sabotagem

A suíte de testes deve falhar com 100% de eficácia quando forem injetadas
falhas no domínio.

6.4. Análise estática de segurança (SAST)

Nenhuma vulnerabilidade crítica ou alta pode permanecer em aberto no pipeline
de CI/CD.

6.5. Reprodutibilidade

Toda a aplicação deve ser executável via Docker, sem a necessidade de comandos
manuais no sistema operacional hospedeiro.


7. INSTRUÇÕES PARA O AGENTE DE IA
---------------------------------

7.1. Padrão de código

Escrever código limpo e tipado, utilizando TypeScript no frontend e Type Hints
no Python com Pydantic. Implementar tratamento explícito de erros.

7.2. Separação de camadas

Nunca realizar chamadas ao banco de dados diretamente nas rotas HTTP
(api/routers). As consultas devem permanecer nos repositories, enquanto as
regras de negócio devem ficar nos services e no domain.

7.3. Migrações

Nunca propor a criação de tabelas por meio de comandos SQL manuais e isolados.
Utilizar migrações do Alembic.

7.4. Controle de escopo

Não adicionar microsserviços, filas com RabbitMQ ou Celery, Redis ou bancos
NoSQL sem solicitação explícita. Manter a arquitetura simples e sólida.